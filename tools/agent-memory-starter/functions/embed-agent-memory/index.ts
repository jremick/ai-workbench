import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "@supabase/supabase-js";

const MEMORY_SCHEMA = "agent_memory";
const DEFAULT_MODEL = "text-embedding-3-small";
const DEFAULT_DIMENSIONS = 1536;
const MAX_MATCH_COUNT = 50;
const MAX_BATCH_SIZE = 100;

type BackfillRequest = {
  mode: "backfill";
  batch_size?: number;
};

type StatsRequest = {
  mode: "stats";
};

type SearchRequest = {
  mode: "query" | "text_search";
  query: string;
  match_count?: number;
  include_scopes?: string[];
};

type PageRequest = {
  mode: "page";
  slug: string;
  include_embeddings?: boolean;
};

type ProposalRequest = {
  mode: "propose_update";
  proposed_by?: string;
  target_slug?: string;
  change_type: "create_page" | "update_compiled_truth" | "append_timeline" | "add_chunk" | "archive_page";
  proposed_text: string;
  reason?: string;
  scope?: "personal" | "team" | "shared" | "public";
  sensitivity?: "public" | "internal" | "private" | "restricted";
  source_uri?: string;
  metadata?: Record<string, unknown>;
};

type FunctionRequest =
  | BackfillRequest
  | StatsRequest
  | SearchRequest
  | PageRequest
  | ProposalRequest;

type PendingChunk = {
  chunk_id: string;
  content: string;
  content_hash: string;
};

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

function requireEnv(name: string): string {
  const value = Deno.env.get(name);
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

function embeddingModel(): string {
  return Deno.env.get("AGENT_MEMORY_EMBEDDING_MODEL") || DEFAULT_MODEL;
}

function embeddingDimensions(): number {
  const raw = Deno.env.get("AGENT_MEMORY_EMBEDDING_DIMENSIONS");
  if (!raw) {
    return DEFAULT_DIMENSIONS;
  }

  const parsed = Number.parseInt(raw, 10);
  if (!Number.isFinite(parsed) || parsed <= 0) {
    throw new Error("AGENT_MEMORY_EMBEDDING_DIMENSIONS must be a positive integer");
  }
  return parsed;
}

function authorizeRequest(request: Request): Response | null {
  const expectedToken = requireEnv("AGENT_MEMORY_FUNCTION_TOKEN");
  const providedToken = request.headers.get("x-agent-memory-token");

  if (!providedToken || providedToken !== expectedToken) {
    return jsonResponse({ error: "Unauthorized" }, 401);
  }

  return null;
}

function boundedCount(value: number | undefined, fallback: number, max: number): number {
  return Math.max(1, Math.min(value ?? fallback, max));
}

function vectorLiteral(values: number[], dimensions: number): string {
  if (values.length !== dimensions) {
    throw new Error(`Expected ${dimensions} embedding dimensions, received ${values.length}`);
  }
  return `[${values.join(",")}]`;
}

function safeError(error: unknown): string {
  const message = error instanceof Error ? error.message : String(error);
  return message
    .replace(/Bearer\s+[A-Za-z0-9._-]+/g, "Bearer [redacted]")
    .replace(/sk-[A-Za-z0-9_-]{20,}/g, "[redacted-api-key]");
}

async function createEmbeddings(input: string[]): Promise<number[][]> {
  const apiKey = requireEnv("OPENAI_API_KEY");
  const model = embeddingModel();
  const dimensions = embeddingDimensions();

  const response = await fetch("https://api.openai.com/v1/embeddings", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model,
      input,
      dimensions,
      encoding_format: "float",
    }),
  });

  if (!response.ok) {
    throw new Error(`Embedding request failed with status ${response.status}`);
  }

  const data = await response.json();
  return data.data
    .sort((a: { index: number }, b: { index: number }) => a.index - b.index)
    .map((item: { embedding: number[] }) => item.embedding);
}

Deno.serve(async (request: Request) => {
  if (request.method !== "POST") {
    return jsonResponse({ error: "Method not allowed" }, 405);
  }

  try {
    const authError = authorizeRequest(request);
    if (authError) {
      return authError;
    }

    const supabase = createClient(
      requireEnv("SUPABASE_URL"),
      requireEnv("SUPABASE_SERVICE_ROLE_KEY"),
      {
        auth: {
          autoRefreshToken: false,
          persistSession: false,
        },
        db: {
          schema: MEMORY_SCHEMA,
        },
      },
    );

    const payload = (await request.json()) as FunctionRequest;

    if (payload.mode === "stats") {
      const { data, error } = await supabase.rpc("stats");
      if (error) {
        throw error;
      }
      return jsonResponse({ schema: MEMORY_SCHEMA, ...(data ?? {}) });
    }

    if (payload.mode === "text_search") {
      if (!payload.query || typeof payload.query !== "string") {
        return jsonResponse({ error: "query is required" }, 400);
      }

      const { data, error } = await supabase.rpc("search_chunks", {
        query_text: payload.query,
        query_embedding: null,
        match_count: boundedCount(payload.match_count, 10, MAX_MATCH_COUNT),
        include_scopes: payload.include_scopes ?? null,
      });
      if (error) {
        throw error;
      }
      return jsonResponse({ results: data ?? [] });
    }

    if (payload.mode === "query") {
      if (!payload.query || typeof payload.query !== "string") {
        return jsonResponse({ error: "query is required" }, 400);
      }

      const dimensions = embeddingDimensions();
      const [embedding] = await createEmbeddings([payload.query]);
      const { data, error } = await supabase.rpc("search_chunks", {
        query_text: payload.query,
        query_embedding: vectorLiteral(embedding, dimensions),
        match_count: boundedCount(payload.match_count, 10, MAX_MATCH_COUNT),
        include_scopes: payload.include_scopes ?? null,
      });
      if (error) {
        throw error;
      }
      return jsonResponse({ results: data ?? [] });
    }

    if (payload.mode === "page") {
      if (!payload.slug || typeof payload.slug !== "string") {
        return jsonResponse({ error: "slug is required" }, 400);
      }

      const { data, error } = await supabase.rpc("page_bundle", {
        target_slug: payload.slug,
        include_embeddings: payload.include_embeddings ?? false,
      });
      if (error) {
        throw error;
      }
      return jsonResponse(data ?? { page: null, timeline: [], chunks: [] });
    }

    if (payload.mode === "propose_update") {
      if (!payload.change_type || !payload.proposed_text) {
        return jsonResponse({ error: "change_type and proposed_text are required" }, 400);
      }

      const { data, error } = await supabase.rpc("propose_update", {
        p_proposed_by: payload.proposed_by ?? "unknown-agent",
        p_target_slug: payload.target_slug ?? null,
        p_change_type: payload.change_type,
        p_proposed_text: payload.proposed_text,
        p_reason: payload.reason ?? "",
        p_scope: payload.scope ?? "shared",
        p_sensitivity: payload.sensitivity ?? "internal",
        p_source_uri: payload.source_uri ?? null,
        p_metadata: payload.metadata ?? {},
      });
      if (error) {
        throw error;
      }
      return jsonResponse({ proposal_id: data });
    }

    if (payload.mode === "backfill") {
      const batchSize = boundedCount(payload.batch_size, 25, MAX_BATCH_SIZE);
      const { data: pending, error: queueError } = await supabase.rpc("embedding_queue", {
        p_batch_size: batchSize,
      });
      if (queueError) {
        throw queueError;
      }

      const chunks = (pending ?? []) as PendingChunk[];
      if (chunks.length === 0) {
        const { data: stats } = await supabase.rpc("embedding_stats");
        return jsonResponse({ embedded: 0, failed: 0, stats });
      }

      const model = embeddingModel();
      const dimensions = embeddingDimensions();
      const embeddings = await createEmbeddings(chunks.map((chunk) => chunk.content));
      const failures: Array<{ chunk_id: string; error: string }> = [];

      for (let index = 0; index < chunks.length; index += 1) {
        const chunk = chunks[index];
        const { data: updated, error } = await supabase.rpc("store_embedding", {
          p_chunk_id: chunk.chunk_id,
          p_content_hash: chunk.content_hash,
          p_embedding: vectorLiteral(embeddings[index], dimensions),
          p_embedding_model: model,
          p_embedding_dimensions: dimensions,
        });

        if (error || updated !== true) {
          failures.push({
            chunk_id: chunk.chunk_id,
            error: error ? error.message : "chunk changed before embedding could be stored",
          });
        }
      }

      const { data: stats } = await supabase.rpc("embedding_stats");
      return jsonResponse({
        embedded: chunks.length - failures.length,
        failed: failures.length,
        failures,
        stats,
      });
    }

    return jsonResponse({ error: "Unsupported mode" }, 400);
  } catch (error) {
    return jsonResponse({ error: safeError(error) }, 500);
  }
});

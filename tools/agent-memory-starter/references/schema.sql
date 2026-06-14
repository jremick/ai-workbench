-- Agent Memory Starter schema
-- Apply as a migration in a private Supabase/Postgres project.

create extension if not exists vector;
create extension if not exists pg_trgm;
create extension if not exists pgcrypto;

create schema if not exists agent_memory;

create table if not exists agent_memory.sources (
  id uuid primary key default gen_random_uuid(),
  source_system text not null,
  source_uri text,
  source_ref text,
  sensitivity text not null default 'internal'
    check (sensitivity in ('public', 'internal', 'private', 'restricted')),
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists agent_memory.pages (
  id uuid primary key default gen_random_uuid(),
  slug text not null unique,
  title text not null,
  page_type text not null
    check (page_type in ('project', 'system', 'person', 'decision', 'runbook', 'preference', 'workflow', 'concept', 'source')),
  scope text not null default 'shared'
    check (scope in ('personal', 'team', 'shared', 'public')),
  sensitivity text not null default 'internal'
    check (sensitivity in ('public', 'internal', 'private', 'restricted')),
  summary text not null default '',
  compiled_truth text not null default '',
  tags text[] not null default '{}',
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  archived_at timestamptz
);

create table if not exists agent_memory.timeline_entries (
  id uuid primary key default gen_random_uuid(),
  page_id uuid not null references agent_memory.pages(id) on delete cascade,
  source_id uuid references agent_memory.sources(id) on delete set null,
  occurred_at timestamptz not null default now(),
  event_text text not null,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists agent_memory.chunks (
  id uuid primary key default gen_random_uuid(),
  page_id uuid not null references agent_memory.pages(id) on delete cascade,
  source_id uuid references agent_memory.sources(id) on delete set null,
  chunk_type text not null
    check (chunk_type in ('compiled_truth', 'timeline', 'source', 'proposal', 'example')),
  content text not null,
  content_hash text generated always as (md5(content)) stored,
  search_vector tsvector generated always as (to_tsvector('english', coalesce(content, ''))) stored,
  embedding vector(1536),
  embedding_model text,
  embedding_dimensions integer,
  embedding_content_hash text,
  embedded_at timestamptz,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists agent_memory.memory_update_proposals (
  id uuid primary key default gen_random_uuid(),
  proposed_by text not null default 'unknown-agent',
  target_slug text,
  change_type text not null
    check (change_type in ('create_page', 'update_compiled_truth', 'append_timeline', 'add_chunk', 'archive_page')),
  proposed_text text not null,
  reason text not null default '',
  scope text not null default 'shared'
    check (scope in ('personal', 'team', 'shared', 'public')),
  sensitivity text not null default 'internal'
    check (sensitivity in ('public', 'internal', 'private', 'restricted')),
  source_uri text,
  status text not null default 'pending'
    check (status in ('pending', 'approved', 'rejected', 'applied')),
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  reviewed_at timestamptz,
  reviewed_by text
);

create index if not exists pages_slug_idx on agent_memory.pages (slug);
create index if not exists pages_scope_idx on agent_memory.pages (scope);
create index if not exists pages_tags_idx on agent_memory.pages using gin (tags);
create index if not exists timeline_page_idx on agent_memory.timeline_entries (page_id, occurred_at desc);
create index if not exists chunks_page_idx on agent_memory.chunks (page_id);
create index if not exists chunks_search_idx on agent_memory.chunks using gin (search_vector);
create index if not exists chunks_trgm_idx on agent_memory.chunks using gin (content gin_trgm_ops);
create index if not exists chunks_embedding_idx on agent_memory.chunks using hnsw (embedding vector_cosine_ops);
create index if not exists proposals_status_idx on agent_memory.memory_update_proposals (status, created_at desc);

create or replace function agent_memory.touch_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists pages_touch_updated_at on agent_memory.pages;
create trigger pages_touch_updated_at
before update on agent_memory.pages
for each row
execute function agent_memory.touch_updated_at();

create or replace function agent_memory.embedding_stats()
returns jsonb
language sql
stable
as $$
  select jsonb_build_object(
    'total_chunks', count(*)::int,
    'embedded_chunks', count(*) filter (where embedding is not null)::int,
    'pending_chunks', count(*) filter (where embedding is null)::int,
    'stale_chunks', count(*) filter (
      where embedding is not null and embedding_content_hash is distinct from content_hash
    )::int
  )
  from agent_memory.chunks;
$$;

create or replace function agent_memory.stats()
returns jsonb
language sql
stable
as $$
  select jsonb_build_object(
    'pages', (select count(*)::int from agent_memory.pages where archived_at is null),
    'sources', (select count(*)::int from agent_memory.sources),
    'timeline_entries', (select count(*)::int from agent_memory.timeline_entries),
    'chunks', (select count(*)::int from agent_memory.chunks),
    'proposals_pending', (
      select count(*)::int from agent_memory.memory_update_proposals where status = 'pending'
    ),
    'embeddings', agent_memory.embedding_stats()
  );
$$;

create or replace function agent_memory.embedding_queue(p_batch_size integer default 25)
returns table (
  chunk_id uuid,
  content text,
  content_hash text
)
language sql
stable
as $$
  select c.id, c.content, c.content_hash
  from agent_memory.chunks c
  join agent_memory.pages p on p.id = c.page_id
  where p.archived_at is null
    and (c.embedding is null or c.embedding_content_hash is distinct from c.content_hash)
  order by c.created_at
  limit greatest(1, least(coalesce(p_batch_size, 25), 100));
$$;

create or replace function agent_memory.store_embedding(
  p_chunk_id uuid,
  p_content_hash text,
  p_embedding vector(1536),
  p_embedding_model text,
  p_embedding_dimensions integer default 1536
)
returns boolean
language plpgsql
as $$
declare
  updated_count integer;
begin
  update agent_memory.chunks
  set
    embedding = p_embedding,
    embedding_model = p_embedding_model,
    embedding_dimensions = p_embedding_dimensions,
    embedding_content_hash = p_content_hash,
    embedded_at = now()
  where id = p_chunk_id
    and content_hash = p_content_hash;

  get diagnostics updated_count = row_count;
  return updated_count = 1;
end;
$$;

create or replace function agent_memory.search_chunks(
  query_text text,
  query_embedding vector(1536) default null,
  match_count integer default 10,
  include_scopes text[] default null
)
returns table (
  page_slug text,
  page_title text,
  page_type text,
  scope text,
  sensitivity text,
  chunk_id uuid,
  chunk_type text,
  content text,
  source_id uuid,
  score double precision,
  score_parts jsonb
)
language sql
stable
as $$
  with input as (
    select
      nullif(trim(query_text), '') as q,
      greatest(1, least(coalesce(match_count, 10), 50)) as limit_count
  ),
  query as (
    select
      q,
      websearch_to_tsquery('english', coalesce(q, '')) as tsq,
      limit_count
    from input
  ),
  scored as (
    select
      p.slug as page_slug,
      p.title as page_title,
      p.page_type,
      p.scope,
      p.sensitivity,
      c.id as chunk_id,
      c.chunk_type,
      c.content,
      c.source_id,
      case
        when query_embedding is null or c.embedding is null then 0.0
        else greatest(0.0, 1.0 - (c.embedding <=> query_embedding))
      end as vector_score,
      case
        when q.q is null then 0.0
        else ts_rank_cd(c.search_vector, q.tsq)::double precision
      end as text_score,
      case
        when q.q is null then 0.0
        else similarity(c.content, q.q)::double precision
      end as trigram_score,
      q.limit_count
    from query q
    join agent_memory.chunks c on true
    join agent_memory.pages p on p.id = c.page_id
    where q.q is not null
      and p.archived_at is null
      and (include_scopes is null or p.scope = any(include_scopes))
  ),
  ranked as (
    select
      *,
      ((0.45 * vector_score) + (0.40 * text_score) + (0.15 * trigram_score)) as final_score
    from scored
    where vector_score > 0
       or text_score > 0
       or trigram_score > 0.04
  )
  select
    page_slug,
    page_title,
    page_type,
    scope,
    sensitivity,
    chunk_id,
    chunk_type,
    content,
    source_id,
    final_score as score,
    jsonb_build_object(
      'vector', vector_score,
      'text', text_score,
      'trigram', trigram_score
    ) as score_parts
  from ranked
  order by final_score desc, page_slug asc
  limit (select limit_count from input);
$$;

create or replace function agent_memory.page_bundle(
  target_slug text,
  include_embeddings boolean default false
)
returns jsonb
language sql
stable
as $$
  select jsonb_build_object(
    'page', jsonb_build_object(
      'slug', p.slug,
      'title', p.title,
      'page_type', p.page_type,
      'scope', p.scope,
      'sensitivity', p.sensitivity,
      'summary', p.summary,
      'compiled_truth', p.compiled_truth,
      'tags', p.tags,
      'metadata', p.metadata,
      'created_at', p.created_at,
      'updated_at', p.updated_at
    ),
    'timeline', coalesce((
      select jsonb_agg(jsonb_build_object(
        'occurred_at', t.occurred_at,
        'event_text', t.event_text,
        'source_id', t.source_id,
        'metadata', t.metadata
      ) order by t.occurred_at desc)
      from agent_memory.timeline_entries t
      where t.page_id = p.id
    ), '[]'::jsonb),
    'chunks', coalesce((
      select jsonb_agg(jsonb_build_object(
        'chunk_id', c.id,
        'chunk_type', c.chunk_type,
        'content', c.content,
        'source_id', c.source_id,
        'content_hash', c.content_hash,
        'embedding_model', c.embedding_model,
        'embedding_dimensions', c.embedding_dimensions,
        'embedded_at', c.embedded_at,
        'embedding', case when include_embeddings then c.embedding::text else null end,
        'metadata', c.metadata
      ) order by c.created_at)
      from agent_memory.chunks c
      where c.page_id = p.id
    ), '[]'::jsonb)
  )
  from agent_memory.pages p
  where p.slug = target_slug
    and p.archived_at is null;
$$;

create or replace function agent_memory.propose_update(
  p_proposed_by text,
  p_target_slug text,
  p_change_type text,
  p_proposed_text text,
  p_reason text default '',
  p_scope text default 'shared',
  p_sensitivity text default 'internal',
  p_source_uri text default null,
  p_metadata jsonb default '{}'::jsonb
)
returns uuid
language plpgsql
as $$
declare
  proposal_id uuid;
begin
  insert into agent_memory.memory_update_proposals (
    proposed_by,
    target_slug,
    change_type,
    proposed_text,
    reason,
    scope,
    sensitivity,
    source_uri,
    metadata
  )
  values (
    coalesce(nullif(p_proposed_by, ''), 'unknown-agent'),
    nullif(p_target_slug, ''),
    p_change_type,
    p_proposed_text,
    coalesce(p_reason, ''),
    coalesce(nullif(p_scope, ''), 'shared'),
    coalesce(nullif(p_sensitivity, ''), 'internal'),
    nullif(p_source_uri, ''),
    coalesce(p_metadata, '{}'::jsonb)
  )
  returning id into proposal_id;

  return proposal_id;
end;
$$;

grant usage on schema agent_memory to service_role;
grant all on all tables in schema agent_memory to service_role;
grant all on all sequences in schema agent_memory to service_role;
grant execute on all functions in schema agent_memory to service_role;

alter default privileges in schema agent_memory grant all on tables to service_role;
alter default privileges in schema agent_memory grant all on sequences to service_role;
alter default privileges in schema agent_memory grant execute on functions to service_role;

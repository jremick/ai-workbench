#!/usr/bin/env python3
"""Plan, validate, and execute deterministic model-council runs."""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
WORKER_TEMPLATE = ROOT / "templates" / "worker.md"
SYNTH_TEMPLATE = ROOT / "templates" / "synthesizer.md"
SCHEMA_VERSION = "model-council-runner/v1"
ADAPTERS = {
    "codex_exec",
    "claude_code",
    "antigravity_cli",
    "grok_cli",
    "vercel_ai_gateway",
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def render_template(path: Path, values: dict[str, str]) -> str:
    text = path.read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def clean_id(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in ("-", "_") else "-" for ch in value).strip("-")


def validate_config(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if config.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    roles = config.get("roles")
    if not isinstance(roles, list) or not roles:
        errors.append("roles must be a non-empty list")
    else:
        seen: set[str] = set()
        for index, role in enumerate(roles):
            prefix = f"roles[{index}]"
            role_id = role.get("id")
            if not role_id:
                errors.append(f"{prefix}.id is required")
            elif role_id in seen:
                errors.append(f"{prefix}.id duplicates {role_id}")
            seen.add(role_id)
            if role.get("adapter") not in ADAPTERS:
                errors.append(f"{prefix}.adapter must be one of {sorted(ADAPTERS)}")
            if not role.get("provider"):
                errors.append(f"{prefix}.provider is required")
            if not role.get("label"):
                errors.append(f"{prefix}.label is required")
            if not role.get("focus"):
                errors.append(f"{prefix}.focus is required")
            if role.get("adapter") == "vercel_ai_gateway" and not role.get("model"):
                errors.append(f"{prefix}.model is required for Vercel AI Gateway")

    synth = config.get("synthesizer")
    if not isinstance(synth, dict):
        errors.append("synthesizer must be an object")
    else:
        if synth.get("adapter") not in ADAPTERS:
            errors.append(f"synthesizer.adapter must be one of {sorted(ADAPTERS)}")
        if synth.get("adapter") == "vercel_ai_gateway" and not synth.get("model"):
            errors.append("synthesizer.model is required for Vercel AI Gateway")

    return errors


def validate_task(task: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not task.get("id"):
        errors.append("task.id is required")
    if not task.get("question"):
        errors.append("task.question is required")
    return errors


def command_for_entry(entry: dict[str, Any], prompt_text: str | None = None) -> list[str] | None:
    adapter = entry["adapter"]
    route = entry["route"]
    cwd = entry["cwd"]
    output_path = entry["output_path"]
    prompt_path = entry["prompt_path"]
    model = route.get("model")

    if adapter == "codex_exec":
        command = [
            "codex",
            "exec",
            "--ephemeral",
            "--json",
            "-C",
            cwd,
            "-s",
            route.get("sandbox", "read-only"),
            "-o",
            output_path,
        ]
        if model:
            command.extend(["-m", str(model)])
        if route.get("reasoning_effort"):
            command.extend(["-c", f"model_reasoning_effort={json.dumps(str(route['reasoning_effort']))}"])
        command.append("-")
        return command

    if adapter == "claude_code":
        if prompt_text is None:
            prompt_text = Path(prompt_path).read_text(encoding="utf-8")
        command = [
            "claude",
            "--bare",
            "-p",
            prompt_text,
            "--output-format",
            "json",
            "--no-session-persistence",
            "--permission-mode",
            route.get("permission_mode", "plan"),
        ]
        if model:
            command.extend(["--model", str(model)])
        if route.get("effort"):
            command.extend(["--effort", str(route["effort"])])
        if route.get("max_budget_usd") is not None:
            command.extend(["--max-budget-usd", str(route["max_budget_usd"])])
        return command

    if adapter == "antigravity_cli":
        if prompt_text is None:
            prompt_text = Path(prompt_path).read_text(encoding="utf-8")
        command = ["agy", "--print", prompt_text, "--print-timeout", str(route.get("timeout", "20m"))]
        if model:
            command.extend(["--model", str(model)])
        if route.get("sandbox", True):
            command.append("--sandbox")
        return command

    if adapter == "grok_cli":
        command = [
            "grok",
            "--no-auto-update",
            "--prompt-file",
            prompt_path,
            "--output-format",
            "json",
            "--permission-mode",
            route.get("permission_mode", "plan"),
            "--no-subagents",
            "--no-memory",
            "--cwd",
            cwd,
        ]
        if model:
            command.extend(["--model", str(model)])
        if route.get("effort"):
            command.extend(["--effort", str(route["effort"])])
        return command

    if adapter == "vercel_ai_gateway":
        return None

    raise ValueError(f"unknown adapter: {adapter}")


def command_preview(entry: dict[str, Any]) -> list[str] | None:
    return command_for_entry(entry, prompt_text="<prompt text>")


def build_worker_entry(route: dict[str, Any], task: dict[str, Any], run_dir: Path) -> dict[str, Any]:
    role_id = clean_id(route["id"])
    prompt_path = run_dir / "prompts" / f"{role_id}.md"
    output_path = run_dir / "outputs" / f"{role_id}.txt"
    stdout_path = run_dir / "logs" / f"{role_id}.stdout"
    stderr_path = run_dir / "logs" / f"{role_id}.stderr"
    prompt = render_template(
        WORKER_TEMPLATE,
        {
            "label": route["label"],
            "focus": route["focus"],
            "task_json": json.dumps(task, indent=2, sort_keys=True),
            "role_id": role_id,
        },
    )
    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.write_text(prompt, encoding="utf-8")
    entry = {
        "id": role_id,
        "kind": "worker",
        "label": route["label"],
        "provider": route["provider"],
        "adapter": route["adapter"],
        "model": route.get("model"),
        "route": route,
        "cwd": str(Path.cwd()),
        "prompt_path": str(prompt_path),
        "output_path": str(output_path),
        "stdout_path": str(stdout_path),
        "stderr_path": str(stderr_path),
        "status": "planned",
    }
    entry["command"] = command_preview(entry)
    return entry


def build_synth_entry(route: dict[str, Any], run_dir: Path) -> dict[str, Any]:
    role_id = clean_id(route.get("id", "synthesizer"))
    entry = {
        "id": role_id,
        "kind": "synthesizer",
        "label": route.get("label", "Council Synthesizer"),
        "provider": route["provider"],
        "adapter": route["adapter"],
        "model": route.get("model"),
        "route": route,
        "cwd": str(Path.cwd()),
        "prompt_path": str(run_dir / "prompts" / f"{role_id}.md"),
        "output_path": str(run_dir / "outputs" / f"{role_id}.txt"),
        "stdout_path": str(run_dir / "logs" / f"{role_id}.stdout"),
        "stderr_path": str(run_dir / "logs" / f"{role_id}.stderr"),
        "status": "planned_after_workers",
    }
    entry["command"] = command_preview(entry)
    return entry


def build_plan(config_path: Path, task_path: Path, run_dir: Path, force: bool) -> dict[str, Any]:
    if run_dir.exists() and any(run_dir.iterdir()) and not force:
        raise SystemExit(f"run directory is not empty: {run_dir}")
    run_dir.mkdir(parents=True, exist_ok=True)
    for subdir in ("prompts", "outputs", "logs"):
        (run_dir / subdir).mkdir(exist_ok=True)

    config = read_json(config_path)
    task = read_json(task_path)
    errors = validate_config(config) + validate_task(task)
    if errors:
        raise SystemExit("\n".join(errors))

    saved_config = run_dir / "config.json"
    saved_task = run_dir / "task.json"
    write_json(saved_config, config)
    write_json(saved_task, task)

    workers = [build_worker_entry(role, task, run_dir) for role in config["roles"]]
    synthesizer = build_synth_entry(config["synthesizer"], run_dir)
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "created_at": utc_now(),
        "config_path": str(config_path),
        "task_path": str(task_path),
        "saved_config_path": str(saved_config),
        "saved_task_path": str(saved_task),
        "run_dir": str(run_dir),
        "execution": config.get("execution", {}),
        "workers": workers,
        "synthesizer": synthesizer,
        "status": "planned",
    }
    write_json(run_dir / "manifest.json", manifest)
    write_json(
        run_dir / "commands.json",
        {
            "workers": [
                {
                    "id": worker["id"],
                    "adapter": worker["adapter"],
                    "provider": worker["provider"],
                    "model": worker["model"],
                    "command": worker["command"],
                }
                for worker in workers
            ],
            "synthesizer": {
                "id": synthesizer["id"],
                "adapter": synthesizer["adapter"],
                "provider": synthesizer["provider"],
                "model": synthesizer["model"],
                "command": synthesizer["command"],
                "note": "The synthesizer prompt is populated after worker outputs are available.",
            },
        },
    )
    return manifest


def find_gateway_token(config: dict[str, Any]) -> str | None:
    for name in config.get("gateway", {}).get("auth_env", ["AI_GATEWAY_API_KEY", "VERCEL_OIDC_TOKEN"]):
        value = os.environ.get(name)
        if value:
            return value
    return None


def execute_gateway(entry: dict[str, Any], prompt: str, config: dict[str, Any]) -> int:
    token = find_gateway_token(config)
    stdout_path = Path(entry["stdout_path"])
    stderr_path = Path(entry["stderr_path"])
    output_path = Path(entry["output_path"])
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not token:
        stderr_path.write_text("Missing AI_GATEWAY_API_KEY or VERCEL_OIDC_TOKEN.\n", encoding="utf-8")
        return 2

    base_url = config.get("gateway", {}).get("base_url", "https://ai-gateway.vercel.sh/v1")
    body = {
        "model": entry["model"],
        "messages": [{"role": "user", "content": prompt}],
        "temperature": config.get("execution", {}).get("temperature", 0),
    }
    request = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=config.get("execution", {}).get("timeout_seconds", 1800)) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raw_error = exc.read().decode("utf-8", errors="replace")
        stderr_path.write_text(f"HTTP {exc.code}\n{raw_error}\n", encoding="utf-8")
        return 1
    except Exception as exc:  # noqa: BLE001 - CLI wrapper should record all runtime failures.
        stderr_path.write_text(f"{type(exc).__name__}: {exc}\n", encoding="utf-8")
        return 1

    stdout_path.write_text(raw, encoding="utf-8")
    try:
        parsed = json.loads(raw)
        text = parsed["choices"][0]["message"]["content"]
    except Exception:
        text = raw
    output_path.write_text(text, encoding="utf-8")
    stderr_path.write_text("", encoding="utf-8")
    return 0


def list_gateway_models(config: dict[str, Any]) -> dict[str, Any]:
    token = find_gateway_token(config)
    if not token:
        raise SystemExit("Missing AI_GATEWAY_API_KEY or VERCEL_OIDC_TOKEN.")
    base_url = config.get("gateway", {}).get("base_url", "https://ai-gateway.vercel.sh/v1")
    request = urllib.request.Request(
        base_url.rstrip("/") + "/models",
        headers={"Authorization": f"Bearer {token}"},
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def execute_subprocess(entry: dict[str, Any], prompt: str, config: dict[str, Any]) -> int:
    command = command_for_entry(entry, prompt_text=prompt)
    if command is None:
        return execute_gateway(entry, prompt, config)

    stdout_path = Path(entry["stdout_path"])
    stderr_path = Path(entry["stderr_path"])
    output_path = Path(entry["output_path"])
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    timeout = int(config.get("execution", {}).get("timeout_seconds", 1800))
    try:
        result = subprocess.run(
            command,
            input=prompt if entry["adapter"] == "codex_exec" else None,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError as exc:
        stderr_path.write_text(f"{exc}\n", encoding="utf-8")
        return 127
    except subprocess.TimeoutExpired as exc:
        stdout_path.write_text(exc.stdout or "", encoding="utf-8")
        stderr_path.write_text((exc.stderr or "") + f"\nTimed out after {timeout} seconds.\n", encoding="utf-8")
        return 124

    stdout_path.write_text(result.stdout, encoding="utf-8")
    stderr_path.write_text(result.stderr, encoding="utf-8")
    if not output_path.exists() or not output_path.read_text(encoding="utf-8", errors="replace").strip():
        output_path.write_text(result.stdout, encoding="utf-8")
    return result.returncode


def update_synth_prompt(manifest: dict[str, Any]) -> str:
    task = read_json(Path(manifest["saved_task_path"]))
    worker_sections: list[str] = []
    for worker in manifest["workers"]:
        output_path = Path(worker["output_path"])
        output = output_path.read_text(encoding="utf-8", errors="replace") if output_path.exists() else ""
        worker_sections.append(
            "\n".join(
                [
                    f"## {worker['id']} ({worker['label']})",
                    f"Provider: {worker['provider']}",
                    f"Adapter: {worker['adapter']}",
                    f"Model: {worker.get('model')}",
                    "",
                    output.strip() or "[no output]",
                ]
            )
        )
    prompt = render_template(
        SYNTH_TEMPLATE,
        {
            "task_json": json.dumps(task, indent=2, sort_keys=True),
            "worker_outputs": "\n\n".join(worker_sections),
        },
    )
    synth_path = Path(manifest["synthesizer"]["prompt_path"])
    synth_path.parent.mkdir(parents=True, exist_ok=True)
    synth_path.write_text(prompt, encoding="utf-8")
    return prompt


def execute_manifest(manifest_path: Path) -> dict[str, Any]:
    manifest = read_json(manifest_path)
    config = read_json(Path(manifest["saved_config_path"]))
    parallel = bool(config.get("execution", {}).get("parallel_workers", True))

    def run_worker(worker: dict[str, Any]) -> dict[str, Any]:
        prompt = Path(worker["prompt_path"]).read_text(encoding="utf-8")
        started = utc_now()
        code = execute_subprocess(worker, prompt, config)
        worker["started_at"] = started
        worker["finished_at"] = utc_now()
        worker["exit_code"] = code
        worker["status"] = "succeeded" if code == 0 else "failed"
        return worker

    if parallel:
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(manifest["workers"])) as pool:
            manifest["workers"] = list(pool.map(run_worker, manifest["workers"]))
    else:
        manifest["workers"] = [run_worker(worker) for worker in manifest["workers"]]

    synth_prompt = update_synth_prompt(manifest)
    synthesizer = manifest["synthesizer"]
    synthesizer["started_at"] = utc_now()
    code = execute_subprocess(synthesizer, synth_prompt, config)
    synthesizer["finished_at"] = utc_now()
    synthesizer["exit_code"] = code
    synthesizer["status"] = "succeeded" if code == 0 else "failed"
    synthesizer["command"] = command_preview(synthesizer)

    manifest["status"] = "succeeded" if all(worker["status"] == "succeeded" for worker in manifest["workers"]) and code == 0 else "failed"
    manifest["finished_at"] = utc_now()
    write_json(manifest_path, manifest)
    return manifest


def validate_manifest(path: Path) -> list[str]:
    errors: list[str] = []
    manifest = read_json(path)
    if manifest.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"manifest schema_version must be {SCHEMA_VERSION}")
    for key in ("run_dir", "saved_config_path", "saved_task_path", "workers", "synthesizer"):
        if key not in manifest:
            errors.append(f"manifest missing {key}")
    for worker in manifest.get("workers", []):
        for key in ("prompt_path", "output_path", "stdout_path", "stderr_path"):
            if key not in worker:
                errors.append(f"worker {worker.get('id')} missing {key}")
        if worker.get("adapter") not in ADAPTERS:
            errors.append(f"worker {worker.get('id')} has unknown adapter {worker.get('adapter')}")
    return errors


def cli_available(name: str) -> bool:
    return shutil.which(name) is not None


def adapter_binary(adapter: str) -> str | None:
    return {
        "codex_exec": "codex",
        "claude_code": "claude",
        "antigravity_cli": "agy",
        "grok_cli": "grok",
        "vercel_ai_gateway": None,
    }[adapter]


def cmd_validate(args: argparse.Namespace) -> int:
    errors: list[str] = []
    if args.config:
        config = read_json(args.config)
        errors.extend(validate_config(config))
        for route in [*config.get("roles", []), config.get("synthesizer", {})]:
            binary = adapter_binary(route.get("adapter"))
            if binary and not cli_available(binary):
                errors.append(f"missing CLI for adapter {route.get('adapter')}: {binary}")
    if args.task:
        errors.extend(validate_task(read_json(args.task)))
    if args.manifest:
        errors.extend(validate_manifest(args.manifest))
    result = {"passed": not errors, "errors": errors}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


def cmd_plan(args: argparse.Namespace) -> int:
    manifest = build_plan(args.config, args.task, args.run_dir, args.force)
    print(json.dumps({"manifest": str(Path(manifest["run_dir"]) / "manifest.json"), "status": "planned"}, indent=2))
    return 0


def cmd_execute(args: argparse.Namespace) -> int:
    manifest = execute_manifest(args.manifest)
    print(json.dumps({"manifest": str(args.manifest), "status": manifest["status"]}, indent=2))
    return 0 if manifest["status"] == "succeeded" else 1


def cmd_models(args: argparse.Namespace) -> int:
    config = read_json(args.config)
    models = list_gateway_models(config)
    configured = [
        route.get("model")
        for route in [*config.get("roles", []), config.get("synthesizer", {})]
        if route.get("adapter") == "vercel_ai_gateway"
    ]
    available = {model.get("id") for model in models.get("data", []) if isinstance(model, dict)}
    missing = sorted(model for model in configured if model and model not in available)
    print(
        json.dumps(
            {
                "configured_models": configured,
                "missing_configured_models": missing,
                "models": models,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if not missing else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Validate config, task, and optional manifest.")
    validate.add_argument("--config", type=Path)
    validate.add_argument("--task", type=Path)
    validate.add_argument("--manifest", type=Path)
    validate.set_defaults(func=cmd_validate)

    plan = subparsers.add_parser("plan", help="Create prompts, command arrays, and manifest without model calls.")
    plan.add_argument("--config", type=Path, required=True)
    plan.add_argument("--task", type=Path, required=True)
    plan.add_argument("--run-dir", type=Path, required=True)
    plan.add_argument("--force", action="store_true")
    plan.set_defaults(func=cmd_plan)

    execute = subparsers.add_parser("execute", help="Execute an existing manifest.")
    execute.add_argument("--manifest", type=Path, required=True)
    execute.set_defaults(func=cmd_execute)

    models = subparsers.add_parser("models", help="List Vercel AI Gateway models and check configured IDs.")
    models.add_argument("--config", type=Path, required=True)
    models.set_defaults(func=cmd_models)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

# Model Council

`model-council` runs independent model workers and a separate synthesis pass.

It is useful for difficult decisions, research synthesis, high-risk claims, and benchmark comparisons where a single model answer is not enough evidence.

## What It Does

- defines council roles with distinct responsibilities
- keeps worker prompts isolated before synthesis
- routes OpenAI, Anthropic, Google, and xAI workers through local CLIs first
- provides a Vercel AI Gateway config as an API alternate option
- records prompts, command arrays, raw logs, model outputs, and synthesis output

## Install

Copy this directory into your agent skill directory:

```text
skills/model-council/
```

The minimum install is `SKILL.md`. Keep `references/` when you want the full workflow notes.

## Runner

The companion runner lives at:

```text
tools/model-council-runner/
```

Base runner flow:

```mermaid
flowchart TD
  Task["Task or evidence packet"] --> Config["Council config<br/>roles and routes"]
  Config --> Plan["Plan<br/>validate, render prompts, write manifest"]
  Plan --> Gate{"Execute now?"}
  Gate -->|No| Review["Review prompts and route plan"]
  Review --> Revise["Revise task, roles, prompts, or routes"]
  Revise --> Config
  Gate -->|Yes| Fanout["Fan out council workers"]
  Fanout --> Structural["Structural analyst<br/>problem frame and assumptions"]
  Fanout --> Empirical["Empirical analyst<br/>evidence and falsifiable claims"]
  Fanout --> Contrarian["Contrarian analyst<br/>failure modes and alternatives"]
  Fanout --> Reviewer["Implementation reviewer<br/>operational risks and controls"]
  Structural --> StructuralOut["Structural output<br/>claims, evidence, uncertainty"]
  Empirical --> EmpiricalOut["Empirical output<br/>claims, evidence, uncertainty"]
  Contrarian --> ContrarianOut["Contrarian output<br/>claims, evidence, uncertainty"]
  Reviewer --> ReviewerOut["Reviewer output<br/>claims, evidence, uncertainty"]
  StructuralOut --> SynthPrompt["Synthesis prompt<br/>task plus worker outputs"]
  EmpiricalOut --> SynthPrompt
  ContrarianOut --> SynthPrompt
  ReviewerOut --> SynthPrompt
  SynthPrompt --> Synth["Separate synthesizer<br/>consensus, disagreements, gaps"]
  Synth --> Final["Final answer plus verification gaps"]
```

The full documentation includes separate workflow diagrams for the `base`, `adversarial`, `stress-test`, and `extended` council levels: [Model Council And Deep Research](../../docs/model-council-and-deep-research.md).

Validate and dry-plan the base local CLI council:

```bash
python3 tools/model-council-runner/scripts/council_runner.py validate \
  --config tools/model-council-runner/configs/local-cli.base.json \
  --task tools/model-council-runner/fixtures/smoke-task.json

python3 tools/model-council-runner/scripts/council_runner.py plan \
  --config tools/model-council-runner/configs/local-cli.base.json \
  --task tools/model-council-runner/fixtures/smoke-task.json \
  --run-dir /tmp/model-council-smoke \
  --force
```

Run `execute` only when you intend to spend model tokens:

```bash
python3 tools/model-council-runner/scripts/council_runner.py execute \
  --manifest /tmp/model-council-smoke/manifest.json
```

## Related Skills

- `deep-research` uses this skill when research claims need independent review.
- `deterministic-controls` is useful when turning council routing into production policy.
- `verification-harness-router` is useful when deciding what proof is enough after synthesis.

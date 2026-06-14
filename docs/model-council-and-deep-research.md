# Model Council And Deep Research

This package adds two skills plus a deterministic runner.

## Skills

| Skill | Purpose |
| --- | --- |
| `model-council` | Runs independent model workers and a separate synthesis pass. |
| `deep-research` | Performs source-backed research and escalates hard synthesis to a council. |

## Workflow Routing

```mermaid
flowchart TD
  Request["User task or benchmark item"] --> Scope{"What does the task need?"}
  Scope -->|Current facts or sources| DeepSkill["deep-research skill"]
  Scope -->|Independent model judgment| CouncilSkill["model-council skill"]
  Scope -->|Repeatable evaluation| BenchmarkHarness["External benchmark harness"]

  DeepSkill --> SourcePlan["Define source plan<br/>primary sources, dates, scope"]
  SourcePlan --> Evidence["Extract evidence packet<br/>claims, conflicts, uncertainty"]
  Evidence --> Escalate{"Need independent synthesis?"}
  Escalate -->|No| ResearchAnswer["Research synthesis<br/>findings, implications, gaps"]
  Escalate -->|Yes| CouncilBrief["Council task packet<br/>same evidence for every worker"]

  CouncilSkill --> CouncilBrief
  BenchmarkHarness --> BenchPrep["Prepare sample<br/>generation tasks and scoring material"]
  BenchPrep --> CouncilBrief

  CouncilBrief --> RunnerPlan["Runner plan<br/>validate config, render prompts, write manifest"]
  RunnerPlan --> Approval{"Execute model calls?"}
  Approval -->|No| Planned["Review prompts and route plan<br/>prompts, commands, manifest"]
  Planned --> Revise["Revise task packet, roles, routes, or sample"]
  Revise --> RunnerPlan
  Approval -->|Yes| Fanout["Fan out council workers"]
  Fanout --> WorkerOutputs["Structured worker outputs<br/>claims, evidence, uncertainty, failure modes"]
  WorkerOutputs --> Synth["Return to synthesizer<br/>consensus, disagreement, accepted claims, gaps"]
  Synth --> Final["Final answer or benchmark output<br/>with disagreements and gaps"]
  ResearchAnswer --> Final
```

Source: [skill-workflow-routing.mmd](../tools/model-council-runner/diagrams/skill-workflow-routing.mmd)

## Base Council Flow

```mermaid
flowchart TD
  Task["Task JSON<br/>question, context, success criteria"] --> Config["Council config<br/>roles, adapters, models, timeouts"]
  Config --> Validate["Validate<br/>schema, task shape, route binaries"]
  Validate --> PromptBuild["Render isolated worker prompts<br/>same task frame, role-specific lens"]
  PromptBuild --> Manifest["Write run manifest<br/>task, config, prompts, command arrays"]
  Manifest --> ExecuteGate{"Execute now?"}
  ExecuteGate -->|No| DryRun["Review prompts and route plan<br/>planned prompts, commands, manifest"]
  DryRun --> RevisePlan["Revise task, roles, prompts, models, or routes"]
  RevisePlan --> Config
  ExecuteGate -->|Yes| WorkerFanout["Parallel worker fan-out"]

  WorkerFanout --> W1["Structural analyst<br/>problem frame and assumptions"]
  WorkerFanout --> W2["Empirical analyst<br/>evidence and falsifiable claims"]
  WorkerFanout --> W3["Contrarian analyst<br/>failure modes and alternatives"]
  WorkerFanout --> W4["Implementation reviewer<br/>operational risks and controls"]

  W1 --> WorkerOutputs["Structured worker outputs<br/>claims, evidence, uncertainty, failure modes"]
  W2 --> WorkerOutputs
  W3 --> WorkerOutputs
  W4 --> WorkerOutputs

  WorkerOutputs --> Logs["Per-route stdout, stderr, output text"]
  Logs --> Barrier["Barrier<br/>all worker statuses recorded"]
  Barrier --> SynthPrompt["Build synthesizer prompt<br/>task plus worker outputs"]
  SynthPrompt --> SynthRoute["Run synthesizer route"]
  SynthRoute --> Synthesis["Synthesis JSON<br/>consensus, disagreements, accepted claims, gaps"]
  Synthesis --> Verification["Verification gate<br/>parse quality, missing routes, unresolved disagreement"]
  Verification --> Output["Run artifacts<br/>manifest, prompts, logs, outputs"]
```

Source: [base-council-flow.mmd](../tools/model-council-runner/diagrams/base-council-flow.mmd)

## Council Level Workflows

### Base

```mermaid
flowchart TD
  Task["Task or evidence packet"] --> RolePlan["Choose base roles<br/>structural, empirical, contrarian"]
  RolePlan --> PromptSet["Render isolated prompts<br/>same task, different lens"]
  PromptSet --> Fanout["Fan out workers in parallel"]

  Fanout --> Structural["Structural analyst<br/>frame, constraints, assumptions"]
  Fanout --> Empirical["Empirical analyst<br/>evidence, sources, falsifiable claims"]
  Fanout --> Contrarian["Contrarian analyst<br/>failure modes, alternatives, weak framing"]

  Structural --> Outputs["Structured worker outputs<br/>answer, claims, evidence, uncertainty"]
  Empirical --> Outputs
  Contrarian --> Outputs

  Outputs --> SynthesisPrompt["Synthesis prompt<br/>task plus independent outputs"]
  SynthesisPrompt --> Synthesizer["Synthesizer<br/>consensus, disagreements, accepted claims, gaps"]
  Synthesizer --> Final["Final answer<br/>with confidence and next checks"]
```

Source: [council-level-base.mmd](../tools/model-council-runner/diagrams/council-level-base.mmd)

### Adversarial

```mermaid
flowchart TD
  Task["High-risk task or claim"] --> Base["Run base council<br/>independent workers and synthesis"]
  Base --> Provisional["Provisional synthesis<br/>accepted claims and gaps"]
  Provisional --> CriticPrompt["Adversarial prompt<br/>task, worker outputs, synthesis, risk rubric"]
  CriticPrompt --> Critic["Critic or red-team worker<br/>attack assumptions and unsupported claims"]
  Critic --> Challenge["Challenge report<br/>severity, evidence, proposed fixes"]
  Challenge --> Decision{"Material issue found?"}
  Decision -->|No| Final["Finalize synthesis<br/>note adversarial pass"]
  Decision -->|Yes| TargetedReview["Targeted review<br/>rerun narrow worker or revise synthesis"]
  TargetedReview --> Revised["Revised synthesis<br/>accepted, rejected, unresolved claims"]
  Revised --> Final
```

Source: [council-level-adversarial.mmd](../tools/model-council-runner/diagrams/council-level-adversarial.mmd)

### Stress-Test

```mermaid
flowchart TD
  Task["Claim, plan, or answer to stress-test"] --> Base["Run base council<br/>frame, evidence, contradictions"]
  Base --> Draft["Draft synthesis<br/>claims and confidence"]
  Draft --> FailureModes["Failure-mode generation<br/>ways the answer could break"]
  FailureModes --> TestDesign["Test design<br/>counterexamples, edge cases, probes"]
  TestDesign --> CheckRoute{"Can checks run now?"}
  CheckRoute -->|Yes| RunChecks["Run deterministic or manual checks"]
  CheckRoute -->|No| CheckPlan["Record recommended checks<br/>owners, data, stop conditions"]
  RunChecks --> Findings["Stress-test findings<br/>passed, failed, unknown"]
  CheckPlan --> Findings
  Findings --> Update["Update synthesis<br/>downgrade, qualify, or reject claims"]
  Update --> Final["Final answer<br/>with stress-test evidence and remaining risk"]
```

Source: [council-level-stress-test.mmd](../tools/model-council-runner/diagrams/council-level-stress-test.mmd)

### Extended

```mermaid
flowchart TD
  Task["Large research, strategy, or architecture task"] --> Decompose["Decompose into packets<br/>sources, domains, decisions, risks"]
  Decompose --> PacketA["Packet A<br/>source or domain lane"]
  Decompose --> PacketB["Packet B<br/>source or domain lane"]
  Decompose --> PacketC["Packet C<br/>implementation or risk lane"]

  PacketA --> LaneA["Lane council<br/>specialist workers and mini-synthesis"]
  PacketB --> LaneB["Lane council<br/>specialist workers and mini-synthesis"]
  PacketC --> LaneC["Lane council<br/>specialist workers and mini-synthesis"]

  LaneA --> Cross["Cross-lane synthesis<br/>dedupe, reconcile, identify conflicts"]
  LaneB --> Cross
  LaneC --> Cross

  Cross --> Review["Independent verification pass<br/>source checks, red-team, feasibility review"]
  Review --> Integration{"Major gap or conflict?"}
  Integration -->|Yes| Rework["Targeted packet rework<br/>rerun lane or gather evidence"]
  Rework --> Cross
  Integration -->|No| Final["Final deliverable<br/>decision, tradeoffs, evidence, open questions"]
```

Source: [council-level-extended.mmd](../tools/model-council-runner/diagrams/council-level-extended.mmd)

## Routing

The default route order is:

1. Local CLIs for interactive developer machines.
2. Vercel AI Gateway as an API alternate option for execution and deployment.

Local CLI roles:

| Provider | Route |
| --- | --- |
| OpenAI | Codex CLI |
| Anthropic | Claude Code CLI |
| Google | Antigravity CLI |
| xAI | Grok Build CLI |

```mermaid
flowchart TD
  Role["Role route<br/>provider, adapter, model, timeout"] --> Adapter{"Adapter"}
  Adapter -->|codex_exec| CodexCheck["Check codex CLI<br/>build codex exec command"]
  Adapter -->|claude_code| ClaudeCheck["Check claude CLI<br/>build claude -p command"]
  Adapter -->|antigravity_cli| AgyCheck["Check agy CLI<br/>build agy --print command"]
  Adapter -->|grok_cli| GrokCheck["Check grok CLI<br/>build grok --prompt-file command"]
  Adapter -->|vercel_ai_gateway| GatewayCheck["Check Gateway auth<br/>optionally list model IDs"]

  CodexCheck --> LocalExec["Local process execution<br/>prompt via stdin or argument"]
  ClaudeCheck --> LocalExec
  AgyCheck --> LocalExec
  GrokCheck --> LocalExec

  GatewayCheck --> GatewayExec["Gateway API execution<br/>OpenAI-compatible chat completions"]

  LocalExec --> Capture["Capture stdout, stderr, output text, exit code"]
  GatewayExec --> Capture
  Capture --> Status{"Route succeeded?"}
  Status -->|Yes| WorkerOutput["Worker output available for synthesis"]
  Status -->|No| RouteFailure["Route failure recorded<br/>no silent provider substitution"]
  WorkerOutput --> Manifest["Update manifest"]
  RouteFailure --> Manifest
```

Source: [provider-routing.mmd](../tools/model-council-runner/diagrams/provider-routing.mmd)

## Research Escalation

```mermaid
flowchart TD
  Question["Research question<br/>decision context and scope"] --> Recency{"Current-state claim?"}
  Recency -->|Yes| LiveSources["Verify current sources<br/>official docs, APIs, releases, datasets"]
  Recency -->|No| StableSources["Use stable sources<br/>papers, specs, code, archived docs"]
  LiveSources --> Extract
  StableSources --> Extract
  Extract["Extract evidence<br/>source, date, claim, caveat"] --> Conflict{"Conflicts or hard synthesis?"}
  Conflict -->|No| DirectSynthesis["Research synthesis<br/>findings, implications, confidence"]
  Conflict -->|Yes| EvidencePacket["Evidence packet<br/>same facts for every council worker"]
  EvidencePacket --> CouncilPlan["model-council plan<br/>roles, prompts, route config"]
  CouncilPlan --> CouncilWorkers["Independent council workers<br/>structural, empirical, contrarian, optional domain"]
  CouncilWorkers --> CouncilSynth["Council synthesis<br/>accepted claims, rejected claims, gaps"]
  CouncilSynth --> DirectSynthesis
  DirectSynthesis --> FinalChecks["Final checks<br/>citation coverage, date clarity, unresolved gaps"]
```

Source: [deep-research-council-escalation.mmd](../tools/model-council-runner/diagrams/deep-research-council-escalation.mmd)

## Deterministic Controls

The runner enforces:

- JSON config for role routing
- isolated worker prompts
- dry-run planning before execution
- command arrays instead of shell strings
- no silent provider fallback
- per-route raw stdout and stderr logs
- explicit manifest status
- credentials read from environment only
- benchmark prompts and grading material can be kept separate by external benchmark harnesses

## Quick Checks

```bash
python3 scripts/validate_model_council_package.py
```

Dry-plan a run:

```bash
python3 tools/model-council-runner/scripts/council_runner.py plan \
  --config tools/model-council-runner/configs/local-cli.base.json \
  --task tools/model-council-runner/fixtures/smoke-task.json \
  --run-dir /tmp/model-council-smoke \
  --force
```

## Benchmarking

Benchmarks are separate from the skills. Use the runner to plan and execute council runs, then use benchmark packages to prepare datasets and scoring material.

The DRACO benchmark package lives at [benchmarks/model-council-draco](../benchmarks/model-council-draco/README.md).

# TAC Prompt Types — Field Guide for `.claude/commands` & `/adws` (Lesson 10)

> Purpose: Give agents a single, consistent reference for understanding, mapping, planning, and building prompts & workflows using the **seven TAC prompt types** from Lesson 10.

---

## Quick Map of the Seven Types

| Type | Name | One‑liner | Typical Artifact(s) |
|---:|---|---|---|
| **1** | **High‑Level Prompt (HLP)** | One‑shot instruction to do a bounded task. | Single `.md` command |
| **2** | **Workflow Prompt (WFP)** | Multi‑step checklist with clear I/O across steps. | Command with steps |
| **3** | **Control‑Flow Prompt (CFP)** | Workflow with **branching** or loop logic. | Command that chooses paths |
| **4** | **Delegation Prompt (DLP)** | Kick off **other prompts/agents**; orchestrates sub‑work. | Supervisor command |
| **5** | **Higher‑Order Prompt (HOP)** | Composes/arranges **other prompts**; swaps components. | Orchestrator command |
| **6** | **Template‑Meta Prompt (TMP)** | Prompt that **creates prompts** (templates, skeletons). | Generator command |
| **7** | **Self‑Improving Prompt (SIP)** | Prompt that **evaluates & updates** prompts/workflows. | Auto‑refiner + tests |

_Source: Lesson 10 loot‑box — “Level 1” through “Level 7” prompt types and capabilities._

---

## Working Definitions & How to Use Them

### **TAC‑1 · High‑Level Prompt (HLP)**
**Use when:** You need a single deliverable (doc, analysis, code snippet) with minimal orchestration.  
**Shape:** short context → task list → deliverable spec → constraints.  
**Anti‑patterns:** hidden dependencies, vague outputs.

### **TAC‑2 · Workflow Prompt (WFP)**
**Use when:** A task needs ordered steps and hand‑offs (clear inputs/outputs per step).  
**Shape:** numbered steps, each with purpose, inputs, outputs, acceptance criteria.  
**Notes:** This is the 80/20 for real work—prefer TAC‑2 before jumping higher.

### **TAC‑3 · Control‑Flow Prompt (CFP)**
**Use when:** The path depends on conditions (file present? tests pass?).  
**Shape:** explicit `if/else` or loop criteria; log which branch was taken.  
**Notes:** Keep branch criteria **observable** (artifacts or flags).

### **TAC‑4 · Delegation Prompt (DLP)**
**Use when:** Work must be split across **specialist prompts/agents**.  
**Shape:** roles → responsibilities → hand‑off contracts → guardrails.  
**Notes:** Delegate by **interfaces** (what & when), not by implementation details.

### **TAC‑5 · Higher‑Order Prompt (HOP)**
**Use when:** You need a **conductor** that selects/configures other prompts.  
**Shape:** declare available components; selection policy; composition plan.  
**Notes:** Keep pluggable—swap TAC‑1..4 units without editing the HOP.

### **TAC‑6 · Template‑Meta Prompt (TMP)**
**Use when:** You want to **generate prompts** that follow TAC standards.  
**Shape:** takes a goal + context → outputs a ready‑to‑use `.md` command with front‑matter.  
**Notes:** Great for bootstrapping new repos or repeated patterns.

### **TAC‑7 · Self‑Improving Prompt (SIP)**
**Use when:** You need a closed loop: **map → run → test → learn → update**.  
**Shape:** runs a prompt/workflow, evaluates against tests, writes PRs to improve.  
**Notes:** Always log diffs & decisions; require human review for riskier changes.

---

## Standard Front‑Matter for `.claude/commands/*.md`

```yaml
---
tac_type: 1  # 1..7
title: ""    # short human title
summary: ""  # what this command achieves
inputs: []   # files, parameters, env vars
outputs: []  # files, artifacts, side effects
owner: ""    # person or team
related_prompts: []   # paths to other commands
adws: []     # related /adws workflows
version: "0.1.0"
---
```

> If missing, mapping tools **infer `tac_type`** using the heuristics below.

---

## Heuristics to Infer `tac_type` (when metadata is missing)

- Mentions “steps”, “step X of Y”, acceptance criteria → **TAC‑2**.  
- Contains `if`/`else`, “choose”, “branch”, “loop”, exit criteria → **TAC‑3**.  
- Contains “call/run/execute” other `.md` commands or agents → **TAC‑4**.  
- Describes “compose/orchestrate/mix & match prompts/components” → **TAC‑5**.  
- Says “generate a prompt/template/command from …” → **TAC‑6**.  
- Says “measure, test, evaluate, update prompts, write PRs” → **TAC‑7**.  
- None of the above, mostly a one‑shot instruction → **TAC‑1**.

---

## Repository Conventions

- **Commands:** place in `.claude/commands/` (repo may also support `.claude/command/`).  
- **Workflows (ADWs):** place in `/adws/` (Python or shell that orchestrates commands).  
- **Docs:** place in `/ai_docs/` (maps, plans, reports).

**Labeling in diagrams:** `my_command (TAC-2)` → shows basename plus type.

---

## Minimal Templates

### Command Skeleton (any type)
```markdown
---
tac_type: 2
title: Example command
summary: Short description
inputs: []
outputs: []
owner: "@owner"
related_prompts: []
adws: []
version: "0.1.0"
---

# Goal
…

# Steps
1. …

# Deliverables
- …

# Guardrails
- …
```

### ADW Skeleton
```python
# /adws/example.py
# Orchestrate `.claude/commands` with a local CLI if present.
```

---

## How these types connect

- Use **TAC‑2** as your default.  
- Add **TAC‑3** when the workflow truly needs branches.  
- Split into **TAC‑4** when specialists or parallelism help.  
- Introduce **TAC‑5/6** to scale composition & generation.  
- Close the loop with **TAC‑7** to continuously improve.


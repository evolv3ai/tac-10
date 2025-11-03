---
tac_type: 6
title: Plan TAC prompts & workflows (from map → plan)
summary: Given a goal and the repository map, plan a set of prompts/workflows using TAC templates and principles.
inputs:
  - goal (text) or ai_docs/tac_goal.md (optional)
  - map_json: ai_docs/tac_map.json
  - constraints (optional): timeline, reviewers, risk limits
outputs:
  - ai_docs/tac_prompt_plan.md
  - ai_docs/tac_components/** (optional skeletons)
owner: "@repo-owner"
version: "0.1.0"
---

# Task

Create a **plan** to add or improve prompts/workflows using TAC types.

## Steps

1. **Load context**
   - Read `.claude/commands/tac_prompts.md` to align on types and standards.
   - Load `ai_docs/tac_map.json`. Also read `goal` (argument or `ai_docs/tac_goal.md`).

2. **Identify gaps & opportunities**
   - Missing types (e.g., all TAC‑2 but no TAC‑7 loop).
   - Unused prompts, dead ends, or duplicated roles.
   - Hand‑off friction (unclear inputs/outputs).

3. **Propose components**
   - For each needed capability, pick a **TAC type**:
     - Simple output → **TAC‑1**.
     - Ordered multi‑step → **TAC‑2**.
     - Conditional path → **TAC‑3**.
     - Role split / sub‑agents → **TAC‑4**.
     - Composition/orchestration → **TAC‑5**.
     - Generate standardized commands → **TAC‑6**.
     - Continuous improvement loop → **TAC‑7**.
   - For each proposed component, draft a **front‑matter block** and a **one‑paragraph goal**.

4. **Produce skeletons (optional)**
   - Emit ready‑to‑fill files under `ai_docs/tac_components/` that include the standard front‑matter and placeholders for **Steps**, **Deliverables**, and **Guardrails**.

5. **Integration plan**
   - Describe how new components connect to existing ones (edges), and where ADWs will orchestrate.
   - Add a **Mermaid** block showing the target architecture, with nodes labeled `(TAC-#)`.

6. **Test & acceptance**
   - Define smoke‑tests for each component (inputs → expected artifacts).
   - Define a minimal **SIP** (TAC‑7) loop: what to measure and how to approve updates.

7. **Delivery**
   - Write `ai_docs/tac_prompt_plan.md` containing: background, current map summary, proposed components, skeletons list, target diagram, tests, and a **checklist to PR** (file paths, reviewers, owners).

## Acceptance Criteria

- Plan includes at least one **concrete file path** per proposed component.
- Each component indicates a **TAC type** and intended **inputs/outputs**.
- Target Mermaid diagram is consistent with the map.
- Tests are specific and runnable with local data.


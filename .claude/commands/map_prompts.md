---
tac_type: 5
title: Map existing prompts & workflows (label TAC-1..7)
summary: Scan a repository for `.claude/commands/*.md` and `/adws/*` workflows, infer each prompt's TAC type (1..7), and emit a JSON + Mermaid map.
inputs:
  - repo_root (default: .)
  - include_globs (default: [.claude/**/*.md, adws/**/*])
  - exclude_globs (default: ["**/.git/**", "**/node_modules/**", "**/.venv/**"]
outputs:
  - ai_docs/tac_map.json
  - ai_docs/tac_map.mmd
owner: "@repo-owner"
version: "0.1.0"
---

# Task

Map the current repo's commands & workflows and **label each with TAC type**.

## Steps

1. **Collect files**
   - Search for Markdown commands under `.claude/commands/**` and `.claude/command/**`.
   - Search for workflows under `/adws/**` (Python, shell).
   - Respect `include_globs`/`exclude_globs` if provided.

2. **Parse metadata**
   - For each command file, read YAML front‑matter. If `tac_type` is missing, **infer** using the heuristics in `.claude/commands/tac_prompts.md`.
   - Extract: `title`, `summary`, `inputs`, `outputs`, `related_prompts`, `adws`.

3. **Find relationships**
   - In Markdown: lines that mention **running other commands** (e.g., `Run .claude/commands/...`, `Use`, `Call`, `Include`), collect referenced paths.
   - In ADWs: grep for any `.claude/commands/*.md` paths and note direction `workflow -> command`.
   - Build a directed graph of nodes (commands + workflows) and edges (calls/uses).

4. **Emit outputs**
   - **JSON** → `ai_docs/tac_map.json` with entries:
     ```json
     {
       "nodes": [
         {"id": 1, "path": ".claude/commands/plan_prompts.md", "kind": "command",
          "tac_type": 5, "title": "…", "calls": ["…"], "used_by": []}
       ],
       "edges": [{"from": "adws/example.py", "to": ".claude/commands/plan_prompts.md", "why": "uses"}]
     }
     ```
   - **Mermaid** → `ai_docs/tac_map.mmd` (graph LR). **Label every node** with basename and `(TAC-#)`:
     ```mermaid
     graph LR
       A[map_prompts (TAC-5)] --> B[plan_prompts (TAC-6)]
       A --> C[adw_implement_tac_prompts.py (workflow)]
     ```

5. **Write a short Markdown report** at the end of `ai_docs/tac_map.mmd` describing gaps: commands with missing `tac_type`, unreachable nodes, or unused prompts.

## Acceptance Criteria

- Every discovered command/workflow appears once in the JSON and Mermaid outputs.
- Nodes without `tac_type` are still labeled using **inference** and flagged `inferred: true` in JSON.
- Mermaid renders without errors; node labels include **(TAC-#)** when applicable.
- Outputs are reproducible by re‑running this command.

## Notes

- Reference `.claude/commands/tac_prompts.md` for definitions and inference criteria.
- Prefer relative paths. If a command references a path that doesn't exist, include it as a **dashed** node in Mermaid and mark `missing: true` in JSON.


#!/usr/bin/env python3
"""
/adws/adw_implement_tac_prompts.py

Orchestrate three phases using local `.claude/commands`:

  1. Map existing commands/workflows  -> ai_docs/tac_map.json + ai_docs/tac_map.mmd
  2. Plan new/updated TAC components  -> ai_docs/tac_prompt_plan.md
  3. Build prompts/workflows per plan -> via a builder command (configurable)
"""
from __future__ import annotations
import argparse, json, os, shutil, subprocess, sys, textwrap, pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
CLAUDE_DIR = REPO_ROOT / ".claude" / "commands"
AI_DOCS = REPO_ROOT / "ai_docs"

MAP_CMD = CLAUDE_DIR / "map_prompts.md"
PLAN_CMD = CLAUDE_DIR / "plan_prompts.md"

# Default builder candidates (first found will be used)
BUILDER_CANDIDATES = [
    CLAUDE_DIR / "build.md",  # preferred conventional builder
    CLAUDE_DIR / "t_metaprompt_workflow.md",  # existing orchestrator in this repo
    CLAUDE_DIR / "experts" / "build" / "expert_build_workflow.md",  # fallback
]

def which_cli() -> list[list[str]]:
    """
    Return a list of CLI invocation patterns to try, in order.
    We try to be resilient to different local setups.
    """
    patterns = []
    if shutil.which("claude"):
        patterns.append(["claude", "run"])
    if shutil.which("cc"):
        patterns.append(["cc", "run"])
    if shutil.which("codex"):
        patterns.append(["codex", "run"])
    # Last resort: try `npx claude` if available
    if shutil.which("npx"):
        patterns.append(["npx", "claude", "run"])
    return patterns

def run_command(cmd_path: pathlib.Path, extra_env: dict[str, str] | None = None) -> int:
    env = os.environ.copy()
    if extra_env:
        env.update({k: str(v) for k, v in extra_env.items()})
    for base in which_cli():
        try:
            print(f"→ Running: {' '.join(base + [str(cmd_path)])}")
            return subprocess.call(base + [str(cmd_path)], cwd=str(REPO_ROOT), env=env)
        except FileNotFoundError:
            continue
    print("! No supported CLI found to run Claude commands. Searched for: claude, cc, codex, npx claude.")
    print(f"  Please run the command manually: {cmd_path}")
    return 127

def ensure_dirs():
    AI_DOCS.mkdir(parents=True, exist_ok=True)

def detect_builder() -> pathlib.Path | None:
    for p in BUILDER_CANDIDATES:
        if p.exists():
            return p
    return None

def main(argv=None):
    parser = argparse.ArgumentParser(description="Implement TAC prompts: map → plan → build")
    parser.add_argument("--goal", help="Goal text for planning (overrides ai_docs/tac_goal.md if provided)")
    parser.add_argument("--dry-run", action="store_true", help="Prepare and print steps but do not invoke CLI")
    parser.add_argument("--builder", help="Path to builder command (.md) to use instead of autodetect")
    args = parser.parse_args(argv)

    ensure_dirs()

    if args.goal:
        (AI_DOCS / "tac_goal.md").write_text(args.goal, encoding="utf-8")

    # 1) Map
    if not MAP_CMD.exists():
        print(f"! Missing {MAP_CMD}. Aborting.")
        return 2
    if args.dry_run:
        print(f"[dry-run] Would run map: {MAP_CMD}")
    else:
        code = run_command(MAP_CMD)
        if code != 0:
            print(f"! map_prompts command exited with code {code}")
            return code

    # 2) Plan
    if not PLAN_CMD.exists():
        print(f"! Missing {PLAN_CMD}. Aborting.")
        return 2
    if args.dry_run:
        print(f"[dry-run] Would run plan: {PLAN_CMD}")
    else:
        code = run_command(PLAN_CMD)
        if code != 0:
            print(f"! plan_prompts command exited with code {code}")
            return code

    # 3) Build
    builder = pathlib.Path(args.builder) if args.builder else detect_builder()
    if not builder:
        print("! Could not find a builder command (build.md / t_metaprompt_workflow.md / experts/build/expert_build_workflow.md).")
        print("  You can supply one via --builder PATH")
        return 0
    if args.dry_run:
        print(f"[dry-run] Would run builder: {builder}")
    else:
        code = run_command(builder)
        if code != 0:
            print(f"! builder command exited with code {code}")
            return code

    print("✓ Completed map → plan → build pipeline.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

---
name: uber-implement
description: End-to-end autonomous pipeline -- plans with /plan-4.8 (3 scouts, deliberator, plan-writer, reducer-critic), then implements with /wt-implement in an isolated worktree. No manual approval between plan and implementation.
---

# Uber Implement

End-to-end pipeline: plan a change with the full `/plan-4.8` pipeline, then immediately implement it in a worktree via `/wt-implement`. No manual approval gate between planning and implementation.

## Usage

`/uber-implement <request> [merge when done]`

The request is the same natural language you would pass to `/plan-4.8`. Append "merge when done" to auto-merge the PR after implementation.

## Phase A: Plan (plan-4.8 phases 0--5)

Run `/plan-4.8` phases 0 through 5 exactly as documented in that skill:

1. **Phase 0: Setup** -- create the plan note (`dendron-cli note write --fname "plan.<slug>.YYYY.MM.DD"`)
2. **Phase 1: Three Parallel Scouts** -- codebase, design history, gotchas (single message, three Agent calls)
3. **Phase 2: Deliberation** -- one agent reconciles scout reports
4. **Phase 3: Plan Draft** -- plan-writer edits the dendron note (~300 lines, dense)
5. **Phase 4: Reducer-Critic Loop** -- tighten the plan (max 3 iterations)
6. **Phase 5: Weekly Task Note + Stage** -- append the pending bullet to the weekly task note, stage plan note + weekly note. **Skip** the `code notes/<fname>.md` editor open and the printed `## Summary` block -- those exist to hand control back to the user, and uber-implement does not hand back.

**Skip the "Interactive Revision" section entirely.** Do not present and do not enter the revision loop -- hand off straight to Phase B. The reducer-critic in Phase 4 is the only quality gate.

## Phase B: Commit + Implement

1. **Commit the staged plan note + weekly note** so they exist in git history even if implementation fails:

    ```bash
    git commit -m "plan: <slug>"
    ```

2. **Hand off to `/wt-implement`:**
   - Pass the plan note path: `notes/plan.<slug>.YYYY.MM.DD.md`
   - If the user said "merge when done", include that modifier
   - Otherwise default to "just PR"

The `/wt-implement` skill handles everything from here: worktree creation, implementation, verification, rebase, PR, and optional merge.

## Phase C: Report

After `/wt-implement` completes, print a final summary:

```text
## Uber Implement Complete

Plan:   notes/plan.<slug>.YYYY.MM.DD.md ([[plan.<slug>.YYYY.MM.DD]])
Branch: plan/<slug>
PR:     <PR URL>
Status: <merged | PR created>

Files changed:
  - path/to/file1.py (NEW)
  - path/to/file2.py (MODIFY)
  ...
```

## Important Rules

- **No approval gate between plan and implement.** The reducer-critic in `/plan-4.8` Phase 4 is the only quality gate.
- **All `/plan-4.8` rules apply** during Phase A (no H1 headers, no emojis, escape issue numbers, web-search policy, 3 scouts + 1 deliberator + 1 plan-writer + 1 reducer-critic, etc.)
- **All `/wt-implement` rules apply** during Phase B (edits in worktree only, follow specs exactly, rebase retry, etc.)
- **Commit the plan note before implementation** so it exists in git history even if implementation fails.
- **Do NOT use EnterPlanMode/ExitPlanMode** -- this skill replaces built-in plan mode.
- **Do NOT ask extra approval questions** -- tool approval prompts are the gates.
- **Token budget**: this skill uses significant context across both phases. If the codebase is very large, use targeted `/read-codebase <prefix>` filters.
- **Use high or xhigh effort** for the wt-implement phase -- Anthropic's recommendation for agentic coding tasks on Opus 4.8.

## Example

```text
/uber-implement Add an exact chunk-to-time mapping helper and an /audio-fix-from-annotations skill that maps orange Zotero/ABS annotations to chunks for precise re-TTS. merge when done
```

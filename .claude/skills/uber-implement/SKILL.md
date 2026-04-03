---
name: uber-implement
description: End-to-end autonomous pipeline -- plans with /uber-plan (scouts, lead, critic), then implements with /wt-implement in an isolated worktree. No manual approval between plan and implementation. Stops only if critic rates any file spec RED.
---

# Uber Implement

End-to-end pipeline: plan a change with the full `/uber-plan` pipeline, then immediately implement it in a worktree via `/wt-implement`. No manual approval gate between planning and implementation.

## Usage

`/uber-implement <request> [merge when done]`

The request is the same natural language you would pass to `/uber-plan`. Append "merge when done" to auto-merge the PR after implementation.

## Phase A: Plan (uber-plan phases 0--5)

Run `/uber-plan` phases 0 through 5 exactly as documented in that skill:

1. **Phase 0: Setup** -- create the plan note
2. **Phase 1: Discovery** -- two parallel scout agents
3. **Phase 2: Load Codebase** -- lead reads full source
4. **Phase 3: Draft Plan** -- lead writes file specifications
5. **Phase 4: Critique** -- critic reviews with full codebase context
6. **Phase 5: Final Plan** -- lead addresses critic findings

**Skip Phase 6 (Present and Open) entirely.** Do not enter the interactive revision loop.

## Phase B: Gate Check

After Phase 5 completes, read the plan note and check the Critic Review section:

1. Parse the **Specification Quality** ratings for each file spec
2. **If ALL specs are GREEN**: proceed to Phase C
3. **If any spec is RED**: stop and present the plan to the user with the critic findings. Enter the interactive revision loop from `/uber-plan` Phase 6. After the user approves revisions, ask whether to proceed to implementation.
4. **If specs are YELLOW but none RED**: proceed to Phase C (minor ambiguities are acceptable)

Print a one-line gate status before proceeding:

```
Gate: all specs GREEN -- proceeding to implementation.
```

or

```
Gate: RED specs found -- stopping for review.
  - path/to/file.py: <issue summary>
```

## Phase C: Implement (wt-implement)

Invoke `/wt-implement` with the plan note path and any modifiers extracted from the original request:

1. Stage the plan note: `git add notes/<fname>.md`
2. Add a pending bullet to the weekly task note. Stage the weekly note.
3. Commit the plan note + weekly note before implementation: `git commit -m "plan: <slug>"`
4. Hand off to `/wt-implement`:
   - Pass the plan note path: `notes/<fname>.md`
   - If the user said "merge when done", include that modifier
   - Otherwise default to "just PR"

The `/wt-implement` skill handles everything from here: worktree creation, implementation, verification, rebase, PR, and optional merge.

## Phase D: Report

After `/wt-implement` completes, print a final summary:

```
## Uber Implement Complete

Plan:   notes/<fname>.md ([[plan.<slug>.YYYY.MM.DD]])
Branch: plan/<slug>
PR:     <PR URL>
Status: <merged | PR created>

Files changed:
  - path/to/file1.py (NEW)
  - path/to/file2.py (MODIFY)
  ...
```

## Important Rules

- **No approval gate between plan and implement** unless critic finds RED specs
- **All `/uber-plan` rules apply** during Phase A
- **All `/wt-implement` rules apply** during Phase C
- **Commit the plan note before implementation** so it exists in git history even if implementation fails
- **Do NOT use EnterPlanMode/ExitPlanMode** -- this skill replaces built-in plan mode
- **Do NOT ask extra approval questions** -- tool approval prompts are the gates

## Example

```
/uber-implement Add cloze deletion support for audio cards with proper field masking. merge when done
```

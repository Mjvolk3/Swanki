---
name: uber-plan
description: Multi-agent planning pipeline that replaces built-in plan mode. Two scouts read the full codebase, lead drafts a plan, one critic reviews with full codebase context, lead writes a final Dendron note ready for autonomous execution.
---

# Uber Plan

Multi-phase, multi-agent planning pipeline. Produces a Dendron note detailed enough for a separate Claude Code session to implement autonomously.

## Usage

`/uber-plan <request>`

The request is a natural language description of what you want built, changed, or fixed. Can be a single sentence or multiple paragraphs.

## Phase 0: Setup

1. Summarize the user's request into a short title (5-8 words max).
2. Slugify the title: lowercase, non-alphanumeric chars become hyphens, collapse runs, max 60 chars.
3. Compute the Dendron fname: `plan.<slug>.YYYY.MM.DD`
4. Create the note immediately so it exists for later writes:

```bash
dendron-cli note write --fname "plan.<slug>.YYYY.MM.DD"
```

5. Print the plan fname so the user knows where output will land.

## Phase 1: Discovery (2 parallel general-purpose agents)

Launch **two** Scout agents simultaneously using the Agent tool (subagent_type: general-purpose). Both run in **foreground** (you need their results before proceeding).

Each scout reads the **full codebase** (source + paired dendron notes) via the `/read-codebase` skill before doing its analysis.

### Scout 1: Codebase Analysis

> You are analyzing a codebase to inform a plan for this request: `<request>`.
>
> **Step 1:** Run `/read-codebase` to load all source files and their paired dendron notes. If the request is clearly scoped to a specific subpackage, use a prefix filter (e.g., `/read-codebase audio`), but when in doubt load everything.
>
> **Step 2:** With the full codebase in context, report:
> 1. **Relevant modules**: which files/functions/classes are directly relevant to this request. Include file paths and key line numbers.
> 2. **Architecture**: import chains, patterns, config models, how the relevant parts connect.
> 3. **Existing patterns**: how similar functionality is already implemented elsewhere in the codebase. What conventions must the plan follow.
> 4. **Design history**: key decisions and rationale from the dendron notes that are relevant to this request.
> 5. **Potential conflicts**: files or patterns that might break or need updating as a side effect.

### Scout 2: Project Context

> You are gathering project context to inform a plan for this request: `<request>`.
>
> **Step 1:** Run `/read-codebase` to load all source files and their paired dendron notes.
>
> **Step 2:** Check GitHub for relevant issues:
> - `gh issue list --state open --json number,title,body,labels --limit 50`
>
> **Step 3:** Read the current weekly task note carefully (find with: `ls -t notes/user.mjvolk3.swanki.tasks.weekly.*.md | head -1`). Pay special attention to:
> - Which tasks are in progress (`- [ ]`) vs completed (`- [x]`)
> - Which worktrees/branches are active and what they're working on
> - Any tasks tagged `#future` (deferred work that may relate to this request)
> - Recent completed work that provides context or dependencies
>
> **Step 4:** Report:
> 1. **Related issues**: which GitHub issues relate to this request, with numbers and titles.
> 2. **Weekly task context**: relevant in-progress and recently completed tasks.
> 3. **Constraints and deadlines**: anything that constrains this work.
> 4. **In-flight work**: what's currently in progress that might conflict or overlap.
> 5. **Test coverage**: what existing tests cover the relevant modules, and what gaps exist.

## Phase 2: Load Codebase (lead)

While still in this session (you ARE the lead), run `/read-codebase` to load the full source + notes into context.

Wait for both scouts from Phase 1 to complete. Read their reports.

## Phase 3: Draft Plan (lead)

With the full codebase in context + scout reports, write the **draft plan** to the Dendron note. Use the Edit tool to append after the frontmatter.

### Required Plan Structure

The note content (no H1 headers -- H2 and below only):

```markdown
Plan: <Title>

## Context

<Why this work is needed. What problem it solves. Reference issues if relevant (use backtick-wrapped `#N` to prevent Dendron tag parsing).>

## Approach

<High-level strategy. Key design decisions and why.>

## File Specifications

<This is the most critical section. Each file gets its own H3 with enough detail for an execution agent to implement without ambiguity.>

### `path/to/file.py` (NEW)

**Purpose:** <what this file does>
**Depends on:** <imports from other project modules>

**Types:**

- `ClassName(BaseModel)` -- <description>
  - `field_name: type = Field(description="...")` -- <purpose>

**Functions:**

- `function_name(arg: Type, ...) -> ReturnType` -- <what it does>
  - <key logic steps>
  - <edge cases to handle>

**Skeleton:**

\`\`\`python
# Key code structure -- not necessarily complete, but enough to disambiguate intent
\`\`\`

### `path/to/existing.py` (MODIFY)

**Current state:** <what the file does now, key functions>
**Changes:**

1. <Change 1>: <what to add/modify and where>
2. <Change 2>: ...

### `tests/path/test_file.py` (NEW)

**Test cases:**

- `test_<name>` -- <what it verifies, inputs, expected output>

## Edge Cases

<Numbered list of edge cases the implementation must handle.>

## Verification

<Step-by-step verification plan:>
1. Unit tests: `pytest tests/path/test_file.py -xvs`
2. Type check: `mypy swanki/path/file.py`
3. Lint: `ruff check swanki/path/file.py`

## Execution

To implement, start a new Claude Code session:

\`\`\`
/read-codebase <prefix1> <prefix2>
\`\`\`

Then:

\`\`\`
Implement the plan at notes/<fname>.md. Read the plan first, then implement each file specification in order. Run verification after each file. Commit with /update-notes -> /stage -> /commit after each logical unit.
\`\`\`
```

## Phase 4: Critique (1 general-purpose agent)

Launch **one** Critic agent using the Agent tool (subagent_type: general-purpose). Runs in **foreground**. Pass the critic the **full draft plan text** in the prompt (read it from the note file first).

### Critic: Full Review

> You are the sole reviewer of a plan that an autonomous Claude Code agent will implement. You must be thorough. Here is the plan:
>
> <full plan text>
>
> **Step 1:** Run `/read-codebase` to load all source files and their paired dendron notes.
>
> **Step 2: Feasibility** -- verify every proposed change is compatible with the existing codebase:
> 1. If MODIFY: check that referenced functions/classes actually exist. Check that proposed changes don't break existing callers.
> 2. If NEW: check that proposed imports exist. Check that module location follows project conventions. Check that names don't collide.
>
> **Step 3: Completeness** -- find what's missing:
> 1. Are there files that need to change but aren't listed? (e.g., __init__.py re-exports, config models)
> 2. Are there edge cases not covered?
> 3. Are tests comprehensive?
> 4. Does the plan follow project conventions? (check CLAUDE.md)
>
> **Step 4: Specification Quality** -- evaluate whether each file spec is detailed enough for autonomous implementation:
> 1. Could an agent implement each file spec without asking clarifying questions?
> 2. Are function signatures complete?
> 3. Are Pydantic models fully specified?
>
> **Report format:**
>
> ### Feasibility
> List of issues (or "No issues found").
>
> ### Completeness
> List of gaps (or "No gaps found").
>
> ### Specification Quality
> Rate each file spec as GREEN (ready) / YELLOW (minor clarification needed) / RED (significant ambiguity).

## Phase 5: Final Plan (lead)

Read the critic report. Update the plan note:

1. Address every critic finding -- either fix the plan or note why the finding was rejected.
2. Append a "Critic Review" section at the bottom of the plan.
3. Save the updated note.

## Phase 6: Present and Open

1. Stage the note: `git add notes/<fname>.md`
2. **Add a pending bullet to the weekly task note** linking to the plan. Stage the weekly note too.
3. Try to open in VSCode: `code notes/<fname>.md`
4. Print a **brief summary** followed by file paths as the final output:

```
## Summary

<Concise summary of the plan. MAX 500 words.>

## Files

Plan note:   notes/<fname>.md
Dendron link: [[plan.<slug>.YYYY.MM.DD]]

Files specified in plan:
  - path/to/file1.py (NEW)
  - path/to/file2.py (MODIFY)
  ...

Read the plan in your editor. Ask questions or request revisions here.
When satisfied, spawn a new Claude Code session and follow the Execution section.
```

## Interactive Revision

After presenting the plan, enter an interactive loop. The user may:

- Ask questions about the plan -- answer using your full codebase context
- Request specific revisions -- edit the note directly
- Ask to re-run the critic
- Approve -- confirm the plan is ready

Do NOT exit this loop until the user explicitly approves or moves on.

## Important Rules

- **No H1 headers** in the plan note. H2 and below only.
- **No Unicode emojis** in the note (breaks xelatex export).
- **Escape issue numbers**: use backtick-wrapped `` `#N` `` to prevent Dendron tag parsing.
- **File specs are the product.** Spend the most effort here.
- **Critics must read actual code**, not just reason about the plan text.
- **Sequential file processing for execution**: the plan should specify an implementation order that respects dependencies.
- **Do NOT use EnterPlanMode/ExitPlanMode.** This skill replaces built-in plan mode entirely.

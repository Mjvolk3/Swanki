---
name: plan-4.7
description: Three scouts explore the codebase in parallel, argue the approach, and a plan-writer agent synthesizes the deliberation into a concise Dendron note. A reducer-critic then smart-tightens the plan (flagging low-value content for cuts, not truncating) until the plan is dense and human-readable. Built for Claude Opus 4.7 -- literal instruction-following, self-verification, long-running coherence -- so plans describe what and why, not every line of code.
---

# Plan-4.7

A lightweight, high-level planning skill built for Opus 4.7 implementation agents.

## Why this skill exists

Anthropic's Opus 4.7 release notes ([anthropic.com/news/claude-opus-4-7](https://www.anthropic.com/news/claude-opus-4-7)) surface three behaviors that reshape how planning should work:

1. **"Opus 4.7 takes the instructions literally."** Loose, over-constrained plans now get copy-pasted into shallow implementations. Leave judgment room -- 4.7 will use it.
2. **"Catches its own logical faults during the planning phase"** and **"devises ways to verify its own outputs before reporting back."** Implementation agents self-correct; plans do not need to enumerate every edge case.
3. **"Works coherently for hours"**, with "loop resistance" and "graceful error recovery." Plans can describe broad strokes; the implementer sustains the multi-step work.

Together: a plan that reads like a design memo -- file paths, gotchas, key decisions, narrative approach -- outperforms a plan stuffed with Pydantic class bodies and function skeletons.

**Target length: ~300 lines.** Enforced by a reducer-critic that identifies low-value content and proposes cuts. A dense 310-line plan beats a mutilated 250-line plan.

## Usage

`/plan-4.7 <request>`

Freeform request. Scouts read the codebase to ground the plan -- you don't have to hand-hold.

## Web-search policy (library currency)

The model's training cutoff is January 2026; today's date may be later. Any claim about a third-party library -- current stable version, new API, deprecation, breaking change, release date -- can be stale from the model alone. Agents in this skill **must** web-search before recommending library-specific patterns.

Rules for agents:

- **Repo-pinned version first.** Before citing a library, check `requirements.txt`, `pyproject.toml`, and any lock file for the version actually installed. Plan recommendations must work with that version.
- **Web-search if recommending a newer version or new feature.** Use WebSearch (or WebFetch on the project's release-notes URL) to confirm the feature exists in a version available *today*. State the version explicitly.
- **Do not rely on model memory for release dates, version numbers, or API deprecations.** If the plan says "added in 2.x" or "deprecated since N", the source for that claim must be a web fetch, not model recall.
- **Cite sources briefly in the plan.** One-line citation is enough: `pydantic-ai 0.4+ (confirmed 2026-05-13 via ai.pydantic.dev/changelog)`. No long quotes.

This applies to every agent in this skill (scouts, deliberator, plan-writer, reducer-critic) that makes a library claim.

## Phase 0: Setup

1. Summarize the request into a 5-8 word title.
2. Slugify: lowercase, non-alphanumeric -> hyphen, collapse runs, max 60 chars.
3. Dendron fname: `plan.<slug>.YYYY.MM.DD` (today's date).
4. Create the note immediately:

    ```bash
    dendron-cli note write --fname "plan.<slug>.YYYY.MM.DD"
    ```

5. Announce the fname so the user knows where output lands.

## Phase 1: Three Parallel Scouts

Launch **three** Agent calls (subagent_type: Explore, thoroughness: "medium") in a single message so they run concurrently in the foreground. Each scout receives the same `<request>` but with a distinct angle.

No word caps. Scouts report honestly; the critic trims later.

### Scout A - Codebase reconnaissance

> You are Scout A. Gather codebase context for this request: `<request>`.
>
> Find: (1) existing files/modules directly in-scope; (2) integration points -- what imports what, what calls what; (3) patterns already used for this kind of change; (4) tests covering the affected area; (5) the **pinned versions** of any third-party libraries that show up in the in-scope files (check `requirements.txt`, `pyproject.toml`).
>
> Return: a bulleted list of relevant file paths with a one-line purpose each; bullets on integration points; and a short block listing pinned library versions relevant to the request. Do NOT paste file contents. Describe patterns in your own words. Focus on *where* things live and *how* they connect, not *how* to change them.

### Scout B - Design history + conventions

> You are Scout B. Gather design context for this request: `<request>`.
>
> Read: (1) paired dendron notes (`notes/swanki.<module>.md`) for the relevant files; (2) prior plan notes (`notes/plan.*.md`) touching the same subsystem; (3) CLAUDE.md + `.claude/rules/*.md` conventions that apply (if `.claude/rules/` is absent, just CLAUDE.md); (4) auto-memory feedback at `~/.claude/projects/-home-michaelvolk-Documents-projects-Swanki/memory/feedback_*.md` relevant to this area.
>
> Return: (1) prior design decisions that constrain this work, with dendron links and dates; (2) conventions the plan MUST follow; (3) user-stated feedback rules ("do X", "don't do Y") with a pointer to the memory file.

### Scout C - Gotchas + failure modes

> You are Scout C. Find hazards for this request: `<request>`.
>
> Look for: (1) open GitHub issues touching affected files (`gh issue list --state open --json number,title,labels,body --limit 50`); (2) infra quirks that could bite (pre-commit hooks, conda env, hydra config, worktree setup, Fish Speech server, Mathpix CLI TTY requirement); (3) related in-flight work on other branches (`git branch -vv`, recent commits on active branches and worktrees under `~/Documents/projects/Swanki.worktrees/`); (4) data-layout assumptions (`SWANKI_DATA`, `/scratch` paths on gilahyper); (5) **library-version hazards** -- if the request touches a third-party library, web-search the library's recent release notes (WebSearch or WebFetch on the project's release-notes URL) for deprecations, breaking changes, or security advisories since January 2026. Compare findings against the pinned version in `requirements.txt` / `pyproject.toml`.
>
> Return: a numbered list of gotchas, each with (a) what the gotcha is, (b) where it would bite, (c) how to sidestep it. For library-version hazards, cite the source (URL + date fetched).

## Phase 2: Deliberation (one agent)

Launch **one** Agent call (subagent_type: general-purpose) in the foreground. Pass it the full text of all three scout reports.

### Deliberator

> You are reading three scout reports for this request: `<request>`. Argue the approach: identify where scouts converge, where they conflict, and what the right decision is at each conflict.
>
> Scout A (codebase): `<report A>`
>
> Scout B (design + conventions): `<report B>`
>
> Scout C (gotchas): `<report C>`
>
> You are expected to think critically, not just reconcile. If a scout recommended something that conflicts with a documented rule or a gotcha, say so -- do not paper over it.
>
> Produce:
>
> 1. **Agreements:** bullet list of points all three scouts agree on.
> 2. **Disagreements + resolutions:** for each conflict, state both sides in one sentence each, then resolve with rationale (cite conventions, gotchas, or prior design).
> 3. **Uncovered ground:** anything important none of the scouts mentioned. Flag as `AMBIGUOUS -- ask user` if it cannot be resolved without user input.
> 4. **Recommended approach:** 3-6 sentences of broad strokes. What's new, what's modified, what's deleted. No code. No file-by-file specs.

## Phase 3: Plan Draft

Launch **one** Agent call (subagent_type: general-purpose) in the foreground. Pass it the request, all three scout reports, and the deliberator's synthesis. The plan-writer edits the Dendron note from Phase 0.

### Plan-Writer

> You are the plan-writer. Edit `notes/<fname>.md`. Aim for ~300 lines but prioritize density -- a dense 350-line plan beats a hollow 250-line one. A reducer-critic will tighten your output afterward.
>
> Inputs:
>
> - Request: `<request>`
> - Scout A: `<A>`
> - Scout B: `<B>`
> - Scout C: `<C>`
> - Deliberation: `<D>`
>
> Required sections (H2, in this order, no H1):
>
> 1. `## Context` -- why this work, what it solves, what it replaces. Reference kanban issues as backtick-wrapped `` `#N` ``.
> 2. `## Relevant Files` -- table or bullet list. Each row: path + one-line purpose + tag (NEW / MODIFY / DELETE / REFERENCE).
> 3. `## Key Design Decisions` -- numbered list. Lead with the decision, follow with why. Include rejected alternatives when illuminating.
> 4. `## Approach` -- narrative, not a file-by-file spec. Describe the shape of the work: libraries, patterns, execution order, what stays out of scope. May name specific validators, classes, libraries. NOT allowed: long function skeletons, per-field model definitions, multi-page code listings. One 3-10 line snippet is fine when it disambiguates a subtle pattern; more is a failure.
> 5. `## Gotchas` -- numbered list from Scout C + deliberation. Each: hazard + sidestep.
> 6. `## Verification` -- bullet list: tests, commands, manual smoke checks that confirm it works.
> 7. `## Open Questions` -- only if the deliberator flagged AMBIGUOUS. One sentence per question. Omit entirely if none.
>
> Do NOT include:
>
> - `## File Specifications` sections with per-file `**Purpose:**` / `**Depends on:**` / `**Types:**` sub-blocks.
> - Huge Pydantic class bodies.
> - Multi-page code listings.
>
> Style:
>
> - Intentional stance: *why* before *what*.
> - Humans read this -- write for them.
> - Reference specific paths and line numbers when it sharpens the point.
> - Backtick-wrap `` `#N` `` for issue numbers (Dendron tag guard).
> - No Unicode emojis (breaks xelatex export).
>
> **Before reporting done, self-verify:**
>
> 1. Every file path you mention exists on disk OR is explicitly tagged NEW.
> 2. Every design decision has a one-sentence rationale.
> 3. The approach is consistent with the deliberator's resolutions (no silent pivots).
> 4. No section duplicates content from another section.
> 5. Gotchas are specific, not generic ("Fish Speech `[long pause]` renders as audible breath at chunk boundaries -- use `[pause]` instead" is specific; "TTS can be slow" is not).
> 6. **Every library claim has a source.** If the plan mentions a feature, minimum version, or deprecation for any third-party library, confirm via WebSearch / WebFetch (not model recall) and cite the URL + fetch date inline. Match against the pinned version in `requirements.txt` / `pyproject.toml`.
>
> If self-verification surfaces a problem, fix it before handing off.

## Phase 4: Reducer-Critic Loop

Launch **one** Agent call (subagent_type: general-purpose) in the foreground with the current plan text. Max 3 iterations.

The critic does NOT truncate. It identifies low-value content and applies cuts, preserving high-value content and cross-references.

### Reducer-Critic

> You are the reducer-critic for `notes/<fname>.md`. Current line count: `<N>`. Target: ~300 lines, but signal density matters more than raw count.
>
> Current plan:
>
> `<full plan text>`
>
> Identify **low-value content** -- material that, if cut, would not degrade the implementer's ability to execute:
>
> 1. **Redundancy.** Same point made in two sections (e.g., gotcha also stated in a design decision).
> 2. **Convention restatement.** Anything already in CLAUDE.md or `.claude/rules/*.md` -- the implementer reads those anyway. Example: "follow the commit trio rule" -- cut, it IS a rule.
> 3. **Obvious context.** Sentences a practitioner would assume ("tests go in `tests/`", "imports at the top").
> 4. **Template filler.** Intros, summaries, transitions, header restatements.
> 5. **Code-as-prose candidates.** A 15-line code block that boils down to "use a Pydantic BaseModel with these four fields" -- prose is denser and matches this skill's philosophy.
> 6. **Implementation-level detail.** Specifics that belong in code comments or the commit message, not the plan.
>
> Preserve **high-value content**:
>
> - Specific file paths and line numbers.
> - Unique design decisions with rationale.
> - Non-obvious gotchas with sidesteps.
> - Tradeoffs (rejected alternative vs chosen path).
> - Constraints from prior decisions (with dendron links).
> - Cross-references between sections (do not cut one side of a reference).
>
> Produce a report with two parts:
>
> A. **Proposed cuts** -- each cut as: section + quote of removed content + one-sentence justification (which low-value category).
>
> B. **Apply cuts** -- edit the file. If two sections say the same thing, keep the clearer one. If a code block is denser as prose, convert rather than delete. Verify cross-references still resolve after your edits.
>
> After editing, run `wc -l notes/<fname>.md` and report the new line count.
>
> **Termination signal.** If no high-quality cuts remain (every line earns its place), state exactly: `"No further cuts available without cost."` The outer loop exits on that phrase.

Loop logic:

- Critic reports `"No further cuts available without cost."` -> exit, continue to Phase 5 regardless of line count.
- Plan is under ~310 lines and critic applied cuts -> exit, continue to Phase 5.
- Plan is over ~310 lines and critic still finds cuts -> run another pass (max 3 total).
- Over ~310 after 3 passes -> exit. Do NOT truncate. Tell the user the plan came in long and let them decide.

## Phase 5: Weekly Task Note + Present

1. Append one pending bullet to the current weekly task note (`notes/user.mjvolk3.swanki.tasks.weekly.YYYY.WW.md` -- find with `ls -t notes/user.mjvolk3.swanki.tasks.weekly.*.md | head -1`) under today's `## YYYY.MM.DD` H2: `- [ ] <one-sentence plan summary> [[plan.<slug>.YYYY.MM.DD]]`. Create the date H2 if missing.
2. Stage the plan note + weekly note.
3. Try `code notes/<fname>.md` -- swallow IPC errors silently.
4. Print the summary block as your **last output**:

    ```text
    ## Summary

    <2-4 sentences: problem, approach, key files, primary risk>

    ## Files

    Plan note:    notes/<fname>.md
    Dendron link: [[plan.<slug>.YYYY.MM.DD]]
    Line count:   <wc -l result>

    Read the plan in your editor. Ask questions or request revisions here.
    When ready to implement: /wt-implement notes/<fname>.md
    (Use high or xhigh effort for implementation -- Anthropic's recommendation for agentic coding tasks on Opus 4.7.)
    ```

Nothing after this block.

## Interactive Revision

After presenting, enter a revision loop. The user may:

- Ask questions -- answer from your context (scout reports, deliberation, critic cuts are still in scope).
- Request specific edits -- edit the note directly.
- Reject a design decision -- revise the relevant section, don't restart.
- Ask for another reducer-critic pass -- run it.

Exit when the user approves or pivots.

## Rules (Opus 4.7 takes these literally)

- **3 scouts, 1 deliberator, 1 plan-writer, 1 reducer-critic (looped).** Do not add agents.
- **Scouts run in parallel** in a single message with multiple Agent calls.
- **No artificial word caps on scouts.** The reducer-critic trims; scouts report honestly.
- **Reducer removes low-value content categories, not line count.** After 3 passes, if still over target, stop -- signal density beats arbitrary length.
- **Self-verify before reporting.** Plan-writer and reducer-critic must each self-check their output (Opus 4.7 does this well when instructed explicitly).
- **No EnterPlanMode / ExitPlanMode.** This skill replaces plan mode.
- **Leave judgment room.** If the plan specifies every detail, the implementer stops thinking and starts templating. That is the failure mode this skill is built against.
- **Verify library currency from the web, not memory.** Training cutoff is January 2026; library versions, APIs, and deprecations have moved on. See the "Web-search policy" section above.

## Example

```text
/plan-4.7 Fix Hamming lecture audio quality regressions surfaced by ABS bookmarks: tighter fish-speech chunks, per-chunk leading-edge fade, deterministic acronym + forbidden-tag passes, humanized chapter intros, and narrative critic checks (repeated phrases, chronology, connectives).
```

Scouts fan out over `swanki/audio/`, `swanki/conf/models/`, `swanki/models/cards.py`, `tests/test_audio_*.py`. Deliberator resolves "ship the per-chunk leading fade as a `combine_audio_with_section_pauses` parameter or a per-provider postprocess?" Plan-writer drafts ~360 lines. Reducer-critic flags ~50 lines of low-value content (a 25-line Pydantic skeleton that reads better as prose, two convention restatements, an obvious-context paragraph) and applies cuts. Final plan: ~310 lines, dense. User reads in a few minutes.

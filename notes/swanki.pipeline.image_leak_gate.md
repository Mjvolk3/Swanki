---
id: 8kq3m7x2vnr5wp9tzc4bdha
title: Image_leak_gate
desc: Semantic gate on the figure description spoken on a card FRONT — judge against the card's own answer, rewrite question-aware until it stops leaking
updated: 1786000000000
created: 1786000000000
---

## 2026.08.10 - Why this gate exists

A card's figure description is spoken aloud on the FRONT, before the learner
answers. It is written during image processing, **before any card exists**, so it
cannot know what the card ends up asking. That ordering is the whole problem: a
description faithful to the figure is frequently a spoiler for the one question
that figure supports.

[[plan.two-field-image-descriptions-audio-only.2026.06.12]] already split the
description in two — a perceptual half (front) and an interpretive half (back) —
so the front no longer narrates the takeaway. That helped a great deal but does
not close the gap, because *perceptual* is not the same as *answer-blind*: the
generator still never sees the question.

Measured on the live collection with an LLM judge (2026.08.10):

| deck                            | live front-figure cards | leaking    |
|---------------------------------|-------------------------|------------|
| alcamo (pre-fix)                | 60                      | 43 (72%)   |
| kuchel (pre-fix)                | 257                     | 174 (68%)  |
| hamming (pre-fix)               | 89                      | 29 (33%)   |
| ahlmann (post-fix, regenerated) | 36                      | **2 (6%)** |

The perceptual split takes ~70% down to ~6%. This gate targets the residue.

## Design

Runs in `generate_outputs` immediately **after** the correctness gate, so cards
dropped for factual errors are never assessed. For each card with a front image
and a description:

1. **Judge** the description against the card's own question and answer.
2. If it leaks, **rewrite** it with the question in hand and an explicit
   instruction not to answer it — and tell the rewriter *what leaked last time*
   so it does not repeat the mistake.
3. Re-judge. Loop to `max_attempts` (default 2).

Judging is **semantic, not lexical**. This is load-bearing: a word-overlap metric
both over-flags (a description and an answer share vocabulary because they are
about the same figure — a sighted learner reads those labels anyway) and
under-flags (a description that paraphrases the answer in different words leaks
completely while scoring low). An overlap-based sweep of the same corpus found
~85 leaks where the judge found 249; the card that originally prompted this work
scored 58% and would have been missed by any threshold set high enough to avoid
false positives.

**Cards are never dropped.** A description that cannot be cleaned keeps its best
answer-blind attempt — the original was already judged to leak, so the rewrite is
strictly better — and is logged `unresolved` for a human look. Judge failure,
missing image, and rewrite failure all fail open with the card intact; the audit
records which. Every assessed card is written to `image-leak-assessment.json`.

`ImageLeakVerdict` ties `leaks` and `severity` together with a model validator so
the gate can branch on either without them disagreeing. See
[[swanki.models.cards]], [[swanki.llm.agents]], [[tests.test_image_leak_gate]].

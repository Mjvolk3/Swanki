---
id: 7hqz2m9xvbnr48tcwkdpsla
title: Pricing
desc: Sourced per-model token prices so a run's accounting reports dollars, not just counts
updated: 1786510000000
created: 1786510000000
---

## 2026.08.11 - Prices live in one table with a stated source

Token counts alone could not answer the question that prompted this work ("was
the record spend the model or the volume?"), because the answer turns on a 25x
price gap between models in the *same* family.

Published rates, USD per 1M tokens
(<https://developers.openai.com/api/docs/pricing>, fetched 2026-08-11):

| model         | input | cached | output |
|---------------|-------|--------|--------|
| gpt-5.6-sol   | 5.00  | 0.50   | 30.00  |
| gpt-5.6-terra | 2.00  | 0.20   | 12.00  |
| gpt-5.6-luna  | 0.20  | 0.02   | 1.20   |
| gpt-5.5       | 5.00  | 0.50   | 30.00  |
| gpt-5.4-mini  | 0.75  | 0.075  | 4.50   |
| gpt-5.4-nano  | 0.20  | 0.02   | 1.25   |

**`gpt-5.6-luna` is 25x cheaper than `gpt-5.6-sol` on both input and output**,
same family and same `openai-responses` provider. That makes the utility tier a
model swap within a family rather than a cross-family downgrade -- a much
smaller behavioural risk than the split originally assumed.

Two billing facts the arithmetic must respect, both easy to get wrong:

- **`input_tokens` already includes the cached portion.** The cached tokens are
  billed at the cached rate and only the remainder at the full input rate;
  adding them double-charges.
- **`output_tokens` already includes reasoning tokens.** Reasoning is therefore
  never billed as a separate line -- it is already inside the output figure at
  the output rate, which is precisely why reasoning on a $30/1M model is
  expensive.

**An unpriced model reports `None`, never a guess**, and the rollups count
`unpriced_calls` so a missing entry is visible rather than silently reading as
zero. Prices move out of band; `merge_overrides` lets a run correct a stale
entry from config without a code change.

See [[swanki.pipeline.usage_ledger]].

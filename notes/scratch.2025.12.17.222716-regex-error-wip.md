---
id: 9p0pwe4mx0wo72cev3yil06
title: Fix LaTeX Validation - Subscript+Superscript Pattern
desc: ''
updated: 1766032045780
created: 1766032045780
---

# Fix LaTeX Validation Crash for Subscript-Superscript Combinations

## Problem

Card generation crashes with:

```
pydantic_core._pydantic_core.ValidationError: 1 validation error for CardGenerationResponse
cards.0.front.text
  Value error, Please ensure ALL mathematical content uses proper LaTeX formatting with $ delimiters.
  Specific fixes needed: Ensure all subscripted variables are wrapped in $ delimiters
```

**Example**: Card contains `M_{m}^{(s)}` outside $ delimiters

## Root Cause

**File**: `/Users/michaelvolk/Documents/projects/Swanki/swanki/models/cards.py:335`

Current regex pattern: `\b([A-Z])_\{?([a-z0-9]+)\}?\b`

**Why it fails**:

1. Pattern requires word boundary (`\b`) at end
2. When matching `M_{m}^{(s)}`:
   - Matches: `M`, `_`, `{m}` ✓
   - Needs word boundary after `}`
   - But next char is `^` (superscript) - NOT a word boundary
   - Result: **Partial match** `M_{m` (incomplete!)
3. Error message suggests invalid: `$M_{m$` (malformed LaTeX)
4. LLM can't fix it after 3 retries → **crash**

**Test cases**:

- `M_{m}^{(s)}` → Flags as `M_{m` (WRONG - incomplete)
- `M_{m} text` → Should flag as `M_{m}` (correct)
- `$M_{m}^{(s)}$` → No match (correct - already in $ delimiters)

## Solution: Two-Stage Regex

Use TWO patterns instead of one:

1. **Pattern 1** (more specific): Match subscript+superscript combinations
2. **Pattern 2** (fallback): Match subscript-only

Check pattern 1 FIRST, then fall back to pattern 2 if no match.

## Implementation

### File to Modify

`/Users/michaelvolk/Documents/projects/Swanki/swanki/models/cards.py`

### Lines to Change: 333-345

**BEFORE** (current code):

```python
# Check for unformatted subscripted variables (e.g., X_i should be $X_i$)
pattern = r'\b([A-Z])_\{?([a-z0-9]+)\}?\b'
match = re.search(pattern, text_without_latex)
if match:
    issues.append(
        f"Subscripted variable '{match.group(0)}' should be wrapped in $ delimiters: "
        f"${match.group(0)}$. For example: $X_j$, $W_{{ij}}$"
    )
```

**AFTER** (new code):

```python
# Check for unformatted subscripted variables
# Two-stage matching:
# 1. First check for subscript+superscript (e.g., M_{m}^{(s)})
# 2. Then check subscript-only (e.g., M_{m})
# This prevents incomplete matches when superscripts follow subscripts

# Stage 1: Match subscript+superscript combinations
pattern_sub_super = r'\b([A-Z])_\{?([a-z0-9]+)\}?\^\{?[^}]+\}?'
match_super = re.search(pattern_sub_super, text_without_latex)

if match_super:
    full_expr = match_super.group(0)
    issues.append(
        f"Mathematical expression '{full_expr}' with subscript and superscript "
        f"should be wrapped in $ delimiters: ${full_expr}$"
    )
else:
    # Stage 2: Fallback to subscript-only pattern
    pattern_sub_only = r'\b([A-Z])_\{?([a-z0-9]+)\}?\b'
    match_sub = re.search(pattern_sub_only, text_without_latex)
    if match_sub:
        issues.append(
            f"Subscripted variable '{match_sub.group(0)}' should be wrapped "
            f"in $ delimiters: ${match_sub.group(0)}$. For example: $X_j$, $W_{{ij}}$"
        )
```

## Pattern Explanations

### Pattern 1: Subscript + Superscript

`r'\b([A-Z])_\{?([a-z0-9]+)\}?\^\{?[^}]+\}?'`

- `\b([A-Z])` - Uppercase letter with word boundary
- `_\{?([a-z0-9]+)\}?` - Underscore + subscript (optional braces)
- `\^` - Literal caret (superscript marker)
- `\{?[^}]+\}?` - Superscript content (optional braces, anything except `}`)

Matches: `M_{m}^{(s)}`, `X_i^2`, `W_{ij}^{(k)}`

### Pattern 2: Subscript Only

`r'\b([A-Z])_\{?([a-z0-9]+)\}?\b'`

- Same as before but requires word boundary at end
- Only matches when NOT followed by superscript

Matches: `M_{m} text`, `X_i.`, `W_{ij},`

## Expected Behavior

### Before Fix

```
Input: "The model M_{m}^{(s)} predicts"
Match: "M_{m" (incomplete)
Error: "Subscripted variable 'M_{m' should be wrapped in $ delimiters: $M_{m$"
LLM tries to fix with: "$M_{m$^{(s)}" (invalid LaTeX)
After 3 retries: CRASH ❌
```

### After Fix

```
Input: "The model M_{m}^{(s)} predicts"
Match: "M_{m}^{(s)}" (complete)
Error: "Mathematical expression 'M_{m}^{(s)}' should be wrapped in $ delimiters: $M_{m}^{(s)}$"
LLM fixes with: "$M_{m}^{(s)}$" (valid LaTeX)
Validation passes: SUCCESS ✅
```

## Test Cases

After implementing, these should work:

1. **Properly formatted** (should PASS validation):
   - `"The model $M_{m}^{(s)}$ predicts"`
   - `"Variable $X_i$ represents"`

2. **Missing delimiters** (should FAIL but give fixable error):
   - `"The model M_{m}^{(s)} predicts"` → Error suggests `$M_{m}^{(s)}$`
   - `"Variable X_i represents"` → Error suggests `$X_i$`

3. **Already fixed** (should PASS):
   - `"Use $W_{ij}^{(k)}$ for weights"`

## Summary

**Change**: Replace single regex pattern with two-stage check in `cards.py:333-345`

**Why**: Current pattern produces incomplete matches for subscript+superscript, causing crashes

**Fix**: Check specific pattern first (sub+super), then fallback to general pattern (sub-only)

**Result**: Accurate error messages that LLM can fix on retry

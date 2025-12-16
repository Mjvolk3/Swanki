---
id: a9qt3fkfk98c6dooku507y6
title: 2025-12-08 Fixing Audio Lecture Generation - Critical Bug Fixes
desc: 'Fixed 4 critical bugs preventing lecture audio from working correctly'
updated: 1765438519392
created: 1765214116594
---

# Audio Lecture Generation Bug Fixes

## Problem Summary

After testing the lecture audio generation feature, we discovered **4 critical bugs** that completely broke the system:

1. **Prompt Instructions Appearing in Transcript** - LLM was echoing instructions instead of following them
2. **Critique Crashes with KeyError 'tabular'** - LaTeX curly braces broke Python string formatting
3. **LaTeX Not Converted** - Raw LaTeX commands throughout the transcript
4. **Metadata Not Filtered** - References sections, competing interests, author info included

These issues made lecture audio completely unusable - it was longer than the original reading audio and contained the wrong content.

---

## Root Causes

### Bug 1: Prompt Architecture Problem

**Previous approach (BROKEN):**

```python
user_message = """Create an engaging educational lecture from this document.

CONTENT GOALS:
- Capture the SHAPE...
[... hundreds of lines of instructions ...]

Content to present:
{content}"""
```

The LLM saw instructions mixed with content in the user message and treated the ENTIRE thing as content to lecture about, so it echoed back the instructions verbatim.

**Correct approach:**

- **System message**: ALL instructions (what to do, how to format, what to skip)
- **User message**: ONLY the content to process

### Bug 2: String Formatting Conflict

**The problem:**

```python
critique_prompt.format(transcript=full_transcript)
```

When `full_transcript` contained LaTeX like `\begin{tabular}{|l|l|}`, Python's `.format()` saw `{|l|l|}` as a format placeholder and raised `KeyError: 'tabular'`.

**The fix:** Escape curly braces before formatting:

```python
transcript_escaped = full_transcript.replace('{', '{{').replace('}', '}}')
```

### Bug 3: No Pre-processing

Raw markdown was sent directly to the LLM without filtering out:

- References sections
- "Competing interests"
- Author affiliations
- Email addresses
- Publication metadata

---

## Changes Made

### Files Modified

- `swanki/config/generator.py` - Prompt restructuring (52 lines changed)
- `swanki/utils/audio.py` - Core fixes (402 lines added/changed)

### Change 1: Added `filter_metadata()` Function

**Location:** `swanki/utils/audio.py` (lines 1295-1364)

New function that strips unwanted sections from academic papers before lecture generation:

- References sections
- Competing interests
- Author info and affiliations
- Email addresses
- DOIs and publication dates
- LaTeX document metadata (`\author{}`, `\title{}`, etc.)

```python
def filter_metadata(content: str) -> str:
    """Remove metadata sections from academic papers."""
    # Uses regex patterns to identify and skip sections
    # Handles both markdown headers and LaTeX commands
    # Returns cleaned content ready for lecture generation
```

### Change 2: Restructured `generate_lecture_audio()`

**Location:** `swanki/utils/audio.py` (lines 1476-1565)

**Key changes:**

1. **Calls `filter_metadata()`** before processing
2. **System prompt**: Now contains ALL instructions (rules 1-6 about lists, LaTeX, metadata, tone, summary, length)
3. **User prompt**: Only contains minimal framing + content
   - First chunk: `"Begin your lecture on: {citation_key}\n\nContent:\n{content_chunk}"`
   - Subsequent chunks: `"Continue the lecture:\n\n{content_chunk}"`

**Before:**

```python
messages = [
    {"role": "system", "content": short_system_prompt},
    {"role": "user", "content": long_instructions_plus_content}  # WRONG!
]
```

**After:**

```python
messages = [
    {"role": "system", "content": comprehensive_instructions},  # ALL instructions
    {"role": "user", "content": content_only}  # ONLY content
]
```

### Change 3: Fixed Critique String Formatting

**Location:** `swanki/utils/audio.py` (line 1646)

Added escaping before format string:

```python
# Escape curly braces to avoid LaTeX conflicts
transcript_sample = full_transcript[:8000].replace('{', '{{').replace('}', '}}')

critique = openai_client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "You are an expert educational content reviewer."},
        {"role": "user", "content": critique_prompt.format(transcript=transcript_sample)}
    ],
    max_completion_tokens=1500,
)
```

### Change 4: Fixed Refinement String Formatting

**Location:** `swanki/utils/audio.py` (lines 1742-1759)

Applied same escaping fix to refinement stage:

```python
# Escape curly braces in both critique and transcript
critique_escaped = critique_response.replace('{', '{{').replace('}', '}}')
chunk_escaped = chunk.replace('{', '{{').replace('}', '}}')

refinement = openai_client.chat.completions.create(
    model=model,
    temperature=0.3,
    messages=[
        {"role": "system", "content": full_system_prompt},
        {"role": "user", "content": refinement_prompt.format(
            critique=critique_escaped,
            transcript=chunk_escaped
        )}
    ],
    max_completion_tokens=max_output_tokens,
)
```

### Change 5: Simplified Generator Prompts

**Location:** `swanki/config/generator.py` (lines 729-761)

**Before:**

- `lecture_system`: Short, vague instructions
- `lecture_generation`: Long template with instructions mixed into user message

**After:**

- `lecture_system`: Comprehensive instructions (ALL rules in system message)
- `lecture_generation`: Minimal template: `"Begin your lecture on: {citation_key}\n\nContent:\n{content}"`
- `lecture_prefix`: New field for flexibility

This ensures all processing uses the correct prompt architecture by default.

---

## Audio Generation Pipeline Overview

*(Reference: `/Users/michaelvolk/Documents/projects/Swanki/docs/pipeline.md`)*

### High-Level Flow

```
PDF Input
  ↓
Split into Pages (PyMuPDF)
  ↓
Convert to Markdown (Mathpix API)
  ↓
Clean Markdown Files
  ↓
Process Images & Generate Summaries (OpenAI Vision)
  ↓
Generate Document Summary (OpenAI)
  ↓
Generate Flashcards (Instructor/OpenAI)
  ↓
[AUDIO GENERATION STAGE] ← Our fixes are here
  ├─ Complementary Audio (card front/back)
  ├─ Summary Audio (document overview)
  ├─ Reading Audio (full document TTS)
  └─ Lecture Audio (educational presentation) ← Main focus of fixes
  ↓
Optionally Send to Anki (AnkiConnect)
```

### Audio Generation Types

The pipeline supports 4 types of audio (see pipeline.md section 4):

1. **Complementary Audio** (`generate_complementary`)
   - Generates TTS for each flashcard (front and back)
   - Handles cloze cards by masking with "blank" on front, revealing on back
   - Files saved in `gen-md-complementary-audio/` directory
   - Speed: 1.6x (configurable)

2. **Summary Audio** (`generate_summary`)
   - Narration of document summary
   - Uses document summary (not full content)
   - Professional, informative tone
   - Speed: 1.1x (configurable)

3. **Reading Audio** (`generate_reading`)
   - Full document narration
   - Converts LaTeX/math to natural speech
   - Expands acronyms and technical terms
   - Speed: 1.2x (configurable)

4. **Lecture Audio** (`generate_lecture`) ← **We fixed this one**
   - Educational presentation style
   - **NEW:** Pre-processes content with `filter_metadata()`
   - **NEW:** System prompt contains ALL instructions
   - **NEW:** User prompt contains ONLY content
   - Embeds image summaries inline
   - Two-stage critique and refinement
   - Speed: 1.1x (configurable)

### Lecture Audio Generation (Detailed)

**Step 1: Content Preparation**

```python
# Load and combine markdown files
for md_file in markdown_files:
    content = md_file.read_text()
    # Replace image placeholders with narrative-integrated summaries
    full_content += content

# Filter out metadata (NEW!)
cleaned_content = filter_metadata(full_content)
```

**Step 2: System Prompt Setup**

```python
# ALL instructions go in system message (NEW!)
system_instructions = """You are an expert educator creating an audio lecture...

CRITICAL OUTPUT RULES:
1. NO LISTS: Never use numbered lists...
2. NO LATEX: Convert ALL LaTeX to natural language...
3. SKIP METADATA: Completely omit References, competing interests...
4. CONVERSATIONAL TONE: Explain to a curious student...
5. CONCLUDE WITH SUMMARY: End with 3-5 main takeaways...
6. TARGET LENGTH: Aim for 50% of source content..."""

full_system_prompt = f"{system_instructions}\n\nCitation: {humanized_key}"
```

**Step 3: Chunk Processing**

```python
# Chunk CONTENT only (not prompt template)
content_tokens = enc.encode(cleaned_content)
for chunk_idx, start in enumerate(range(0, len(content_tokens), 4000)):
    content_chunk = enc.decode(content_tokens[start:start+4000])

    # User message: ONLY content (NEW!)
    if chunk_idx == 0:
        user_message = f"Begin your lecture on: {humanized_key}\n\nContent:\n{content_chunk}"
    else:
        user_message = f"Continue the lecture:\n\n{content_chunk}"

    # Generate transcript
    response = openai_client.chat.completions.create(
        model=model,
        temperature=0.7,
        messages=[
            {"role": "system", "content": full_system_prompt},  # Instructions
            {"role": "user", "content": user_message}  # Content only
        ],
        max_completion_tokens=3000
    )
```

**Step 4: Critique Stage**

```python
# Review transcript for quality issues
transcript_sample = full_transcript[:8000].replace('{', '{{').replace('}', '}}')  # NEW: Escape LaTeX

critique = openai_client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "You are an expert educational content reviewer."},
        {"role": "user", "content": critique_prompt.format(transcript=transcript_sample)}
    ]
)

# Checks for: lists, LaTeX, length, flow, further reading, summary, figure integration
```

**Step 5: Refinement Stage (if needed)**

```python
if "NEEDS_REFINEMENT" in critique_response:
    # Refine transcript based on critique
    for chunk in transcript_chunks:
        # Escape LaTeX in both critique and chunk (NEW!)
        critique_escaped = critique_response.replace('{', '{{').replace('}', '}}')
        chunk_escaped = chunk.replace('{', '{{').replace('}', '}}')

        refinement = openai_client.chat.completions.create(
            model=model,
            temperature=0.3,
            messages=[
                {"role": "system", "content": full_system_prompt},
                {"role": "user", "content": refinement_prompt.format(
                    critique=critique_escaped,
                    transcript=chunk_escaped
                )}
            ]
        )
```

**Step 6: TTS Conversion**

```python
# Split transcript into 2000-char chunks for TTS
audio_chunks = chunk_text(full_transcript, max_chars=2000)

# Generate audio for each chunk
for i, chunk in enumerate(audio_chunks):
    text_to_speech(chunk, voice_id, chunk_path, elevenlabs_api_key, speed=1.1)

# Combine audio chunks with 200ms crossfade
combine_audio(chunk_paths, output_path)
```

---

## Expected Results

After these fixes, lecture audio should:

- ✅ **No prompt in transcript** - Only actual lecture content
- ✅ **Critique works** - No KeyError, proper analysis
- ✅ **LaTeX converted** - Natural language summaries
- ✅ **No metadata** - References/affiliations filtered out
- ✅ **Conversational** - Flowing narrative, no lists
- ✅ **Proper length** - Target ~50% reduction from current
- ✅ **Summary at end** - 3-5 main points

---

## Testing

Run on test document:

```bash
cd /Users/michaelvolk/Documents/projects/Swanki_Data/luoWhenCausalInference2020
./luoWhenCausalInference2020.sh
```

Check these files:

- `lecture_transcript/*_transcript.md` - Should start with actual lecture (not prompt)
- `lecture_transcript/*_critique.md` - Should show real critique (not "PASS - Unable to critique")
- `lecture_transcript/*_refined.md` - Should exist if refinement was needed
- Logs - Should have no 'tabular' KeyErrors

---

## Git Changes Summary

```
 swanki/config/generator.py |  52 ++++--
 swanki/utils/audio.py      | 423 +++++++++++++++++++++++++++++++++++++++------
 2 files changed, 402 insertions(+), 73 deletions(-)
```

**Key additions:**

- New `filter_metadata()` function (69 lines)
- Complete rewrite of lecture generation logic (200+ lines)
- String escaping for LaTeX safety (multiple locations)
- Simplified default prompts in generator.py

---

## Configuration

Users can customize lecture generation via `.swanki_config/prompts/default.yaml`:

```yaml
lecture_system: |
  You are an expert educator creating an audio lecture...
  [customizable instructions]

lecture_generation: |
  Begin your lecture on: {citation_key}

  Content:
  {content}

lecture_prefix: "Begin your lecture on"
```

The system now properly separates instructions (system) from content (user), preventing the prompt-echoing bug.

---

## 2025-12-11 UPDATE: Why Critique Still Fails After 3 Iterations

### Observation

After implementing the self-refine loop, the Feldmann yeast chapter STILL has 20 issues after 3 iterations:

**Transcript analysis:**

- **Lines 1-60**: ✅ Perfect - conversational, clean, no LaTeX, engaging
- **Lines 62+**: ❌ Completely breaks down - raw LaTeX tables, citations, "Further Reading"

**Example issues found by critique:**

1. Raw LaTeX tables present (\\begin{tabular}, \\hline, etc.)
2. Citations included "(Hughes and Stephens, 2008)", "Nakano et al. 1989"
3. "Further Reading" section with full bibliography
4. LaTeX math: $30 \\%$, $\\boldsymbol{\\gamma}$, $\\alpha$-tubulin
5. Cross-references: "see Figure 2.12", "cf. Section 8.1"

### Root Cause: Chunked Generation Loses Context

The lecture is generated in **4000-token chunks**, but each chunk has **no memory** of previous chunks:

```python
# Current implementation (BROKEN)
for chunk_idx, content_chunk in enumerate(content_chunks):
    if chunk_idx == 0:
        user_message = f"Begin your lecture on: {citation_key}\n\nContent:\n{content_chunk}"
    else:
        user_message = f"Continue the lecture:\n\n{content_chunk}"

    # ❌ No context of what was already generated!
    # ❌ No memory of the clean style from chunk 1
    # ❌ Just processes raw content → copies LaTeX verbatim
```

**What happens:**

1. **Chunk 1**: LLM sees instructions + first content → generates clean, conversational lecture
2. **Chunk 2**: LLM sees "Continue" + raw content → no context → copies LaTeX/citations
3. **Chunk 3+**: Same problem, gets worse

**Why critique doesn't help:**

- Critique runs AFTER all chunks are combined
- Refinement tries to fix the mess, but can't overcome the fundamental context loss
- Each iteration improves slightly but never fully fixes it

### Solution: Stateful Chunked Generation

Pass **summary of already-generated content** to each chunk:

```python
# Proposed fix
generated_transcript = ""

for chunk_idx, content_chunk in enumerate(content_chunks):
    if chunk_idx == 0:
        user_message = f"Begin your lecture on: {citation_key}\n\nContent:\n{content_chunk}"
    else:
        # Summarize what we've covered so far (last ~500 tokens)
        previous_context = summarize_previous_section(generated_transcript)

        user_message = f"""Previously in this lecture, you covered:
{previous_context}

Now continue the lecture by covering this next section. Maintain the same conversational, engaging style with no LaTeX or citations:

{content_chunk}"""

    response = generate_chunk(user_message)
    generated_transcript += response
```

### Evidence: Summary Audio Works Perfectly

The **summary audio** (`feldmannYeastMolecularCell2012_02-yeast-cell-architecture-and-functions-summary-audio_transcript.md`) is **perfect**:

- ✅ No LaTeX
- ✅ No citations
- ✅ No tables
- ✅ Clean, professional, flowing narrative
- ✅ Proper summaries and takeaways

**Why?** Summary is generated in a **single pass** with full context, not chunked. This proves the prompts work when context is preserved.

### Comparison: Lecture vs Summary Quality

**Lecture (chunked, broken):**

```
...great content...

Golgi-localized protein with homology to $\boldsymbol{\gamma}$-adaptin...
\hline & & Gga2 & protein that regulates Arf1p...
\end{tabular}
\end{table}
and its destination, the vesicles...
(Hughes and Stephens, 2008). COPII-coated vesicles...
```

**Summary (single-pass, perfect):**

```
The envelope—plasma membrane, periplasm, and cell wall—mediates protection,
osmotic stability, signaling, and transport. The wall is a rigid, dynamic
composite of mannoproteins, β-glucans, and chitin that remodels during budding
and septation. Cell–cell adhesion (flocculation) arises from lectin-like
flocculins (FLO genes), while sexual agglutinins (Aga/Sag) mediate mating.
```

### Next Steps

1. **Implement stateful chunking** - Pass context summary to each chunk
2. **Alternative**: Generate summary first, then expand section-by-section
3. **Alternative**: Use larger chunks (8k tokens) to reduce number of context switches
4. **Alternative**: Single-pass generation for shorter documents (<20k tokens)

### Related Files

- Lecture (broken): `feldmannYeastMolecularCell2012_02-yeast-cell-architecture-and-functions-lecture-audio_transcript.md`
- Critique (20 issues): `feldmannYeastMolecularCell2012_02-yeast-cell-architecture-and-functions-lecture-audio_critique.md`
- Summary (perfect): `feldmannYeastMolecularCell2012_02-yeast-cell-architecture-and-functions-summary-audio_transcript.md`
- Implementation: `/Users/michaelvolk/Documents/projects/Swanki/swanki/utils/audio.py:1520-1580` (chunked generation)

---

## Related Documentation

- [Pipeline Architecture](../docs/pipeline.md) - Complete pipeline flow
- [Configuration Guide](../docs/configuration.md) - Audio settings
- Implementation files:
  - `/Users/michaelvolk/Documents/projects/Swanki/swanki/utils/audio.py`
  - `/Users/michaelvolk/Documents/projects/Swanki/swanki/config/generator.py`

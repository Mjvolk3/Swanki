# Update After Deep Learning Revolution Review

## Summary

Fix critical card generation issues discovered during review of Bishop Deep Learning Revolution cards, focusing on self-contained cards, proper audio humanization, and format validation.

## Issues to Address

1. **Image card audio not humanizing math** - Math equations in image descriptions are read as raw LaTeX
2. **Missing image summaries** - Some image cards have no summaries, breaking audio generation
3. **Image description placement** - Should come after question for better learning flow
4. **External references** - Cards reference images/equations not available to students
5. **Cloze cards with extra questions** - Violates cloze format rules
6. **Duplicate answers** - Regular cards showing answer on both front and back
7. **Default card counts** - Update to 4 regular + 1 cloze per page

## Implementation Plan

### 1. Add LLM-Based Math Humanization for Audio

**File**: `swanki/utils/audio.py`

Update `generate_card_transcript` to:

- When processing image summaries, always use LLM to humanize math
- Add specific prompt for converting LaTeX/math to natural speech
- Ensure image description math is as clear as card content math

```python
# In generate_card_transcript, when image_summary_included:
if image_summary_included:
    # Force LLM processing for image descriptions with math
    has_math = True  # Always process through LLM
```

### 2. Enforce Image Summary Requirements

**File**: `swanki/models/cards.py`

Add validator to PlainCard:

```python
@model_validator(mode='after')
def validate_image_summary(self):
    """Ensure image cards have summaries."""
    if (self.front.image_path or self.back.image_path) and not (self.front.image_summary or self.back.image_summary):
        raise ValueError("Image cards must have image summaries for accessibility")
    return self
```

### 3. Move Image Descriptions After Questions

**File**: `swanki/utils/audio.py`

In `generate_card_transcript`:

- Move image description to AFTER the main content
- Format: "Question content... [pause] Image description: ..."
- Update both front and back audio generation

```python
# Instead of prepending, append image description
if is_front and has_image and card.front.image_summary:
    # Add image description at END, not beginning
    content = content.strip() + ". Image description: " + card.front.image_summary
```

### 4. Add Self-Criticism Validation System

**File**: `swanki/models/cards.py`

Create new validation class:

```python
class CardValidator:
    """Validates card quality using LLM self-criticism."""
    
    def __init__(self, openai_client: OpenAI):
        self.client = openai_client
    
    def validate_card(self, card: PlainCard) -> tuple[bool, str]:
        """Check if card is self-contained and well-formatted."""
        is_cloze = "{{c" in card.front.text
        
        validation_prompt = f"""
        Evaluate this flashcard for quality and format issues:
        
        Front: {card.front.text}
        Back: {card.back.text if not is_cloze else "[Cloze card - no back content]"}
        Has Image: {bool(card.front.image_path or card.back.image_path)}
        
        Check for these CRITICAL issues:
        1. Does the card reference external content not provided (figures, equations, "the image" without having an image)?
        2. For regular cards: Does the front reveal the answer?
        3. For cloze cards: Does it ask additional questions after the cloze?
        4. Is the card self-contained - can a student understand it without external context?
        
        Return JSON: {{"valid": true/false, "issues": ["list of issues"], "suggestion": "how to fix"}}
        """
        
        # Use structured output with instructor
        # Return validation result
```

### 5. Update Card Generation Prompts

**File**: `swanki/config/generator.py`

Add to prompts:

```python
# Add to FORBIDDEN CONTENT section:
"- ANY reference to 'the image', 'the figure', 'the diagram' in non-image cards"
"- References like 'equation 1.1' or 'formula above' without providing the equation"
"- For image cards: assuming student can see details not in the description"

# Add to CRITICAL CLOZE RULES:
"- Cloze cards must be COMPLETE STATEMENTS, not questions"
"- NEVER add questions after the cloze deletion"
"- BAD: 'The algorithm is {{c1::O(n log n)}}. Why is this important?'"
"- GOOD: 'The algorithm has time complexity {{c1::O(n log n)}}'"

# Add to REGULAR Q&A rules:
"- The question MUST NOT contain the answer"
"- Front and back must be completely distinct"
"- If you reveal the answer in the question, the card is useless"
```

### 6. Add Validation Pipeline

**File**: `swanki/pipeline/pipeline.py`

After card generation:

```python
# Validate each card with self-criticism
validator = CardValidator(openai_client)
validated_cards = []

for card in generated_cards:
    is_valid, issues = validator.validate_card(card)
    if not is_valid:
        logger.warning(f"Card failed validation: {issues}")
        # Either regenerate or skip
        if "answer in question" in issues:
            # Regenerate with specific prompt to fix
            regenerated = regenerate_card_fixing_issues(card, issues)
            validated_cards.append(regenerated)
        else:
            # Skip problematic cards
            continue
    else:
        validated_cards.append(card)
```

### 7. Update Default Configuration

**File**: `swanki/config/generator.py`

Change pipeline defaults:

```python
"processing": {
    "num_cards_per_page": 4,  # Changed from 3
    "cloze_cards_per_page": 1,  # Changed from 2
    ...
}
```

### 8. Enhanced Error Messages

**File**: `swanki/processing/anki_processor.py`

When cards fail validation, provide clear feedback:

- Which specific validation rule was violated
- Suggestion for how to fix
- Whether it's a format issue or content issue

## Testing Plan

1. Generate cards from a document with complex math in images
2. Verify image descriptions are humanized properly
3. Test validation catches:
   - Cards referencing missing content
   - Cloze cards with extra questions
   - Regular cards with answers in questions
4. Confirm audio places image descriptions after questions
5. Validate new default counts (4+1 per page)

## Files to Modify

1. `swanki/utils/audio.py` - Math humanization, image description placement
2. `swanki/models/cards.py` - Add validators and self-criticism
3. `swanki/config/generator.py` - Update prompts and defaults
4. `swanki/pipeline/pipeline.py` - Add validation pipeline
5. `swanki/processing/anki_processor.py` - Enhanced error reporting

## Expected Outcomes

- All image descriptions in audio will have properly humanized math
- No cards will reference external content not available to students
- Cloze cards will be pure cloze format without extra questions
- Regular cards will have clear Q&A separation
- Image descriptions will enhance, not interrupt, the question flow
- Failed cards will be regenerated or skipped with clear explanations

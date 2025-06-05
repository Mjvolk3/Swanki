---
id: fttgy1tk7pqnu50dmvnh8qr
title: '21'
desc: ''
updated: 1748992333802
created: 1748056813358
---

## 2025.05.23

- [x] Claude refactor for more reliable output

## 2025.05.27

![](./assets/images/user.mjvolk3.swanki.tasks.weekly.2025.21.md.tags-not-being-parsed.png)
![](./assets/images/user.mjvolk3.swanki.tasks.weekly.2025.21.md.tags-still-not-parsed_00.png)

## 2025.05.29

**Issue**

![](./assets/images/user.mjvolk3.swanki.tasks.weekly.2025.21.md.cloze-audio-both-on-front.png)

The audio for this cards reads like this.
What does the images equation X equals I W top maps to X equals f two I W top minus one f one Z represent. Major issues are that it forgot the minus sign and it should read minus one as inverse. The math should read like this. "X equals I minus W transpose maps to X equals f two of the inverse of I minus W transpose times f one of Z."

**Issue**

@chiaEngineeringNewGeneration2025: ## What technological advancement has revolutionized biology by enabling precise DNA and RNA edits?

## 2025.05.31

**Issue**

I don't think it is possible to make Latex table $/tabular$ we should probably prompt to not make tables

## 2025.06.01

**Issue**

Complementary audio is cut off a few letters two short.

**Issue**

Swanki_Data/luoWhenCausalInference2020_43/anki-cards-with-audio.md

The cards with images now only have one image per card which is good, but we need to make sure when we add complementary audio that it is paired appropriately with the question. For example, this is one of the cards. For this card it would probably make most sense to put in the image summary, without giving away the answer to the card before we ask the question.

```
@luoWhenCausalInference2020: What is the data matrix labeled in the image and what does it represent in the framework? [image]
```

I point to where we should probably put the image summary without giving away the answer.

```
@luoWhenCausalInference2020: {complementary audio summary of image without giving away the answer and with providing enough context to help someone who is only listening}. What is the data matrix labeled in the image and what does it represent in the framework? [image]
```

Also in this particular example some of the math was read and sounded alien suggesting the humanization of latex did not work correctly.

**Issue**

Swanki_Data/luoWhenCausalInference2020_43/anki-cards-with-audio.md

This example does a very good job of summarizing the image and asking teh question. The question if first asked and the image summarized. I would like this reversed. But the question is basically answered by the summary of the image. I think the question isn't great because it is basically asking to summarize part of the image instead of asking about the content.

```@luoWhenCausalInference2020: How are causal inference and deep learning pathways represented in this image? [image]```

**Issue**

Bad card... How is the student supposed to know what "this framework" means?

```@luoWhenCausalInference2020: What transformation is applied to the problem of data analysis in this framework?

%

[image]
```

**Issue**

If the citation key gets bungled we reused the same complementary audio for the citation key for all complementary audio so it messes up every card... For robustness it almost seems like we should call the api multiple times. But if we get it right once it is never an issue... Not sure how to deal with this. Maybe extra checks on the humanization of the citation key string would help.

**Issue**

We should probably never have more than one cloze text per card. When there are 3 or more it is too difficult there aren't enough context clues to be able to infer the hidden text.

***

**Issue**

Summaries for cards with images work well but there is an issue. It seems that the audio summary for complementary images is not properly humanizing math notation for a listening. The text sounds garbled when explaining math equations. We have handled this elsewhere in complementary audio. Can you try to fix it.

**Issue**

```bash
(swanki) michaelvolk@M1-MV Swanki % swanki pdf_path=/Users/michaelvolk/Documents/projects/Swanki/Luo_2020.pdf citation_key=luoWhenCausalInference2020 audio=full anki=auto_send
[2025-06-01 20:50:22,419][swanki.processing.pdf_processor][INFO] - Splitting PDF with 2 pages: Luo_2020.pdf
[2025-06-01 20:50:22,483][swanki.processing.pdf_processor][INFO] - Successfully split PDF into 2 pages
[2025-06-01 20:50:22,483][swanki.pipeline.pipeline][INFO] - Converting 2 PDF pages to markdown
(node:78631) [DEP0040] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead.
(Use `node --trace-deprecation ...` to show where the warning was created)
(node:78631) [DEP0044] DeprecationWarning: The `util.isArray` API is deprecated. Please use `Array.isArray()` instead.
Converted /Users/michaelvolk/Documents/projects/Swanki_Data/luoWhenCausalInference2020_55/pdf-singles/page-1.pdf to /Users/michaelvolk/Documents/projects/Swanki_Data/luoWhenCausalInference2020_55/md-singles/page-1.md in 10182ms
(node:78914) [DEP0040] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead.
(Use `node --trace-deprecation ...` to show where the warning was created)
(node:78914) [DEP0044] DeprecationWarning: The `util.isArray` API is deprecated. Please use `Array.isArray()` instead.
Converted /Users/michaelvolk/Documents/projects/Swanki_Data/luoWhenCausalInference2020_55/pdf-singles/page-2.pdf to /Users/michaelvolk/Documents/projects/Swanki_Data/luoWhenCausalInference2020_55/md-singles/page-2.md in 15206ms
[2025-06-01 20:50:50,396][swanki.pipeline.pipeline][INFO] - Successfully converted 2 pages to markdown
[2025-06-01 20:50:50,396][swanki.processing.markdown_cleaner][INFO] - Cleaning 2 markdown files
[2025-06-01 20:50:55,522][httpx][INFO] - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
[2025-06-01 20:50:55,529][swanki.processing.image_processor][INFO] - Processed 1 images total
[2025-06-01 20:51:03,033][httpx][INFO] - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
[2025-06-01 20:51:09,331][httpx][INFO] - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"

=== CARD GENERATION PROMPT ===
Requesting 6 regular cards and 4 cloze cards
First 500 chars of prompt: You are required to generate 6 regular cards AND 4 cloze deletion cards.

MANDATORY DISTRIBUTION:
- Regular Q&A cards: 6
- Cloze deletion cards: 4
- Total cards to generate: 6 + 4

Context from document summary:
Title: When causal inference meets deep learning
Acronyms: {'BN': 'Bayesian Network', 'DAG': 'Directed Acyclic Graph', 'SEM': 'Structural Equation Model', 'NAS': 'Neural Architecture Search'}
Technical terms: {'Bayesian Network': 'A statistical model that represents a set of variables an...
=== END PROMPT ===

Generating regular Q&A cards...
[2025-06-01 20:51:16,670][httpx][INFO] - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
Generating cloze deletion cards...
[2025-06-01 20:51:21,056][httpx][INFO] - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
[2025-06-01 20:51:23,225][httpx][INFO] - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
Error executing job with overrides: ['pdf_path=/Users/michaelvolk/Documents/projects/Swanki/Luo_2020.pdf', 'citation_key=luoWhenCausalInference2020', 'audio=full', 'anki=auto_send']
Traceback (most recent call last):
  File "/Users/michaelvolk/opt/miniconda3/envs/swanki/lib/python3.11/site-packages/instructor/retry.py", line 191, in retry_sync
    raise e
  File "/Users/michaelvolk/opt/miniconda3/envs/swanki/lib/python3.11/site-packages/instructor/retry.py", line 174, in retry_sync
    return process_response(  # type: ignore
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/michaelvolk/opt/miniconda3/envs/swanki/lib/python3.11/site-packages/instructor/process_response.py", line 170, in process_response
    model = response_model.from_response(
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/michaelvolk/opt/miniconda3/envs/swanki/lib/python3.11/site-packages/instructor/function_calls.py", line 266, in from_response
    return cls.parse_tools(completion, validation_context, strict)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/michaelvolk/opt/miniconda3/envs/swanki/lib/python3.11/site-packages/instructor/function_calls.py", line 580, in parse_tools
    return cls.model_validate_json(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/michaelvolk/opt/miniconda3/envs/swanki/lib/python3.11/site-packages/pydantic/main.py", line 656, in model_validate_json
    return cls.__pydantic_validator__.validate_json(json_data, strict=strict, context=context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pydantic_core._pydantic_core.ValidationError: 1 validation error for CardGenerationResponse
cards.3.front.text
  Value error, Math equation appears to be outside cloze deletion. Found cloze with content '0' but math notation exists outside. For math cloze cards, the entire equation should be inside {{c1::equation}}. Example: 'The equation {{c1::\(E = mc^2\)}} shows mass-energy equivalence.' [type=value_error, input_value='If for all paths leading...d for causal inference.', input_type=str]
    For further information visit https://errors.pydantic.dev/2.10/v/value_error

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Users/michaelvolk/opt/miniconda3/envs/swanki/lib/python3.11/site-packages/instructor/retry.py", line 163, in retry_sync
    for attempt in max_retries:
  File "/Users/michaelvolk/opt/miniconda3/envs/swanki/lib/python3.11/site-packages/tenacity/__init__.py", line 445, in __iter__
    do = self.iter(retry_state=retry_state)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/michaelvolk/opt/miniconda3/envs/swanki/lib/python3.11/site-packages/tenacity/__init__.py", line 378, in iter
    result = action(retry_state)
             ^^^^^^^^^^^^^^^^^^^
  File "/Users/michaelvolk/opt/miniconda3/envs/swanki/lib/python3.11/site-packages/tenacity/__init__.py", line 421, in exc_check
    raise retry_exc from fut.exception()
tenacity.RetryError: RetryError[<Future at 0x11097ffd0 state=finished raised ValidationError>]

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Users/michaelvolk/Documents/projects/Swanki/swanki/__main__.py", line 131, in cli_main
    process_with_config(cfg)
  File "/Users/michaelvolk/Documents/projects/Swanki/swanki/__main__.py", line 95, in process_with_config
    outputs = pipeline.process_full(
              ^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/michaelvolk/Documents/projects/Swanki/swanki/pipeline/pipeline.py", line 273, in process_full
    all_cards = self.generate_cards_with_window(
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/michaelvolk/Documents/projects/Swanki/swanki/pipeline/pipeline.py", line 724, in generate_cards_with_window
    cloze_response = self.instructor.chat.completions.create(
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/michaelvolk/opt/miniconda3/envs/swanki/lib/python3.11/site-packages/instructor/patch.py", line 193, in new_create_sync
    response = retry_sync(
               ^^^^^^^^^^^
  File "/Users/michaelvolk/opt/miniconda3/envs/swanki/lib/python3.11/site-packages/instructor/retry.py", line 194, in retry_sync
    raise InstructorRetryException(
instructor.exceptions.InstructorRetryException: 1 validation error for CardGenerationResponse
cards.3.front.text
  Value error, Math equation appears to be outside cloze deletion. Found cloze with content '0' but math notation exists outside. For math cloze cards, the entire equation should be inside {{c1::equation}}. Example: 'The equation {{c1::\(E = mc^2\)}} shows mass-energy equivalence.' [type=value_error, input_value='If for all paths leading...d for causal inference.', input_type=str]
    For further information visit https://errors.pydantic.dev/2.10/v/value_error

Set the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace.
```


Michael Volk, Huimin Zhao

## ABSTRACT

The abstract.



## GRAPHICAL ABSTRACT

![](./assets/drawio/graphical_abstract.drawio.png)

## INTRODUCTION

Common learning and memory best practices including retrieval practice, spaced repetition, interleaved practice, and elaborative encoding are all supported by Anki, the spaced repetition flashcard application [@bradshawElaborativeEncodingExplanation1982; @polkLearningBrain; @kornellOptimisingSelfregulatedStudy2008; @santos-ferreiraDigitalFlashcardsMedical2024] . Anki is popular among medical students United States Medical Licensing Exam (USMLE) Step exams where students can download pre-made flashcards developed by by the community. Anki usage has been shown to be associated with higher USMLE Step 1 scores where more consistent users achieved higher scores @luEnhancedLearningRetention2021 . Anki offers extensive digital content formats including text, images, audio, and mathematical notation with LaTEX. Despite effectiveness of Anki and other flashcard apps in learning and memory, they are underutilized in other STEM disciplines. This could be due to a variety of reasons like long chains of reasoning not being easily amenable to flashcards, but we suspect that that a large reason is simply due to the cost of card creation or a limited view of flashcards only supporting rote memorization but the can also be viewed as quizzes of comprehension @senzakiReinventingFlashcardsIncrease2017 .

To fill this perceived gap we developed a python application named Swanki (pronounced "swanky") that takes pdfs as input and produces anki cards as output. We've additionally additionally optional audio including audio summaries, audio books, and complementary card audio that allow users to interact with material through their preferred medium.

There are recent anki plugins [AnkiBrain](https://github.com/RosettaTechnologies/AnkiBrain) for supporting the use of LLMs for card generation from source material. There also a number of online services that now allow for similar types of content creation including [NotebookLM](https://notebooklm.google/), [Limbiks](https://www.limbiks.com/), [Anki-decks](https://anki-decks.com/), [Algor Education](https://www.algoreducation.com/en), [Knowt](https://knowt.com/), and many more. We differentiate primarily by making the entire content creation process configurable by the user so they can modify prompt to customize output and by supporting the creation of image cards and other optional audio options. During development we have found that it is difficult to know the depth of information that any one individual may desire. For example it can be difficult to create cards on implementation details of a multiline algorithm, but if the user specifies this by modifying provided prompt it become feasible.



## METHODS

### Architecture

Swanki is implemented as a modular Python application built on a pipeline-driven architecture that converts PDFs into Anki flashcards through sequential processing stages. The core pipeline orchestrates PDF splitting using PyPDF2, OCR conversion via Mathpix API, and AI-powered content generation using OpenAI's GPT models with Instructor for structured outputs. The system employs a sliding window approach over the PDF with configurable window sizes to maintain contextual coherence and for guaranteeing full coverage during card generation. Pydantic data models used by Instructor ensure content validation and type safety throughout the processing workflow.

### Configuration

The software utilizes Hydra's hierarchical configuration system to provide comprehensive customization through automatically generated configuration files stored in `.swanki_config`. Users can modify processing parameters including window size, cards per page, image processing settings, and modify AI model prompts to their liking. The configuration system supports runtime overrides via command-line arguments and includes preset profiles (default, comprehensive, fast) for different use cases. Output files and Anki decks use citation keys so users can mix cards into large decks without losing context which supports elaborative encoding.

### Cards

The system generates three primary card types: standard question-answer cards, cloze deletion cards that mask information, and image-based cards derived from figures and diagrams. Cards are tagged using configurable hierarchical systems with citation keys automatically prepended to maintain source attribution. LaTeX mathematical notation is preserved for visual display and converted to natural language for audio compatibility.

### Audio

Swanki's complementary audio system generates four distinct audio types: complementary audio providing front/back narration for each flashcard, summary audio for rapid content review, reading audio containing complete document narration, and lecture audio formatted as educational presentations. The system uses LLMs to convert academic text into transcripts for text-to-speech (TTS) models, automatically humanizing mathematical expressions and adding descriptions for images. Audio generation supports variable playback speeds.

The audio system outputs enable different use cases. Lecture audio is good for first time listening and is similar to a solo podcast. Summaries can help for quick paper review, but are often difficult to digest with no previous familiarity with the pdf. Complete document narration can help serve as a pacer while reading and can help students from spending too much time reading instead of practicing via card review. Given a set amount of time, it is often a better use of time to reduce time spent reading and increase time being quizzed, that is reviewing cards. Lastly complementary card audio supports hands-free review sessions using gamepad controllers which can be easily setup with mobile devices with the Anki app. This can gamify the flashcard experience allowing users to participate in other activities like exercise as they listen to questions from the app and respond using small hand held controllers like the micro controller from 8BitDo.



## DISCUSSION

Using LLMs poses a risk of hallucination but by providing source material of a PDF the LLMs task becomes easier turning the task into educational material generation from scratch to a translation task, translating from PDF content to card format. Cards should always be reviewed prior to using them as serious educational content. One of the major goals of developing Swanki was to produce better cards, but this criteria is often ill-defined and depends on aesthetics and expertise of the educator. We choose to use a sliding window technique to get content over the entire document allowing the educator to prune cards to their needs. Reviewing material is often faster than generating it from scratch.

On April 23, 2025 the executive order Advancing Artificial Intelligence Education for American Youth was signed in the United States  @ordersAdvancingArtificialIntelligence2025a . The policy aims at increasing AI proficiency by integrating AI into education. Since Swanki can be used for any PDF we believe the software supports the Sec. 6 "Improving Education Through Artificial Intelligence," as students and teachers can use the software to learn about AI by creating content on AI, but also by inspecting the open source software. We also believe that it supports Sec. 7 "Enhancing Training for Educations on Artificial Intelligence," by reducing the time intensive task of educational content creation. The app can also be used to help educators learn about modern AI techniques.

While we push the limits of the types of content that Anki can natively represent, there are additional card types that we plan to support given enough community interest. To further democratize the tool, our first step will be to support open sourced models that can be run locally to reduce total cost of card generation. Additionally we would like to find an open source drop in for mathpix but bad optical character recognition at the start of the pipeline leads to garbled outputs. The most obvious card to develop next is image occlusion, where the content of interest is occluded by a bounding box. This could be achieved using a semantic segmentation model to draw bounding boxes according to concepts elicited from the figure descriptions and the text. While the current pipeline can account for chemical structures via images support of smiles rendering would be beneficial to parse apart long synthesis diagrams into component parts for more atomized card generation. Another feature would be to expand the scope of inputs to include videos. We find that pdfs cover most use cases since pptx, docx, etc. can often just be converted to pdf without any meaningful information loss. Video poses a larger challenge to synchronize transcripts with frames to extract meaningful images and text for card generation. Cards generated from video could also alow for gifs which are supported by anki. This would involve bounding frames of interest then simply converting video to gif and asking appropriately related questions. We show such a gif for linear algebra vector operations which can be found on github. Lastly, our most ambitious idea is to auto generate gifs programmatically via libraries such as manim that were developed for producing programmatic visualizations of mathematical concepts. The idea is to go from text to program to gif output paired with appropriate questions.



## ASSOCIATED CONTENT

The Supporting Information is available on the ACS Publications website at DOI: 10.1021/acs.jchemed.XXXXXXX. [ACS will fill this in.]

Example brief descriptions with file formats indicated are shown below; customize for your material.

Notes for Instructors (DOCX)
Survey Instrument (DOCX)

* * *

We provide links here to the source:

- [pypi-swanki](https://pypi.org/project/swanki)
- [github-Swanki](https://github.com/Mjvolk3/Swanki)
- [docs-swanki](https://swanki.readthedocs.io/en/latest/)

Open Source'd Swanki library on Zotero.

## AUTHOR INFORMATION

Corresponding Author
\*E-mail:

## REFERENCES
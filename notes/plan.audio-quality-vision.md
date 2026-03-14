---
id: n8kperg63xb0ryfw7t3cyif
title: Audio Quality Vision
desc: ''
updated: 1773521388020
created: 1773521388020
---

Audio quality design principles, learning workflow vision, and ongoing improvement areas for non-complementary audio (transcript, lecture, summary). Originated from [[scratch.2026.03.13.205400-]].

## Learning Workflow Vision

The audio types serve different stages of the study cycle:

- **Lecture** is the hook. It draws the reader into the field, the study, the experiments. It is borderline performance -- a sort of solo podcast derived from published work. Scientists are often too busy to deliver such a thing to the public because they have to go back to working on the next project, to get the next grant. Lecture is the ticket winner of the audio formats.
- **Transcript** is for deep dive. If the lecture hooks interest, the reader follows up with the transcript for full paper immersion. The goal of using transcript is to reduce pausing. Pausing is necessary for understanding and reviewing figures.
- **Summary** is for teleportation through mind-time. For refreshing a topic from things already read -- quickly compile a list of papers, collect audio files, put them in a dir, zip, import to Book Player. Sit down in a dark room and jam it all. Summary follows paper structure with nice spacing, pauses between sections.

## Lecture Design Principles

- Analogies help memory but must illuminate, not obscure. Every analogy must be followed by the precise technical statement. Over-analogizing turns into "the land of wiggeldy worp."
- Needs clear structure: intro (longer, colorful), results sections (combined into a story, punchy, adventurous, detective-like), then conclusion and discussion with research opportunities to facilitate the possibility of related or additional research.
- Don't overdo the humanizing. People are sensitive to AI acting human, and too much makes us a nonplussed cipher.
- One voice, one teacher. You get used to a voice and their pronunciations, and this actually helps improve delivery of information. Mispronunciations trip up and lose the thread on abstract points.

## Transcript Design Principles

- No filler between sections -- just real silence. The pauses are the feature.
- Figures: pause, "Figure X", pause, then read the description. Helps reader jump to figure to crank through it.
- Acronyms expanded on first use -- helps link acronyms to concepts while reading. Provides read enhancement to the experience.
- Metadata (addresses, dates, emails) must be filtered before processing.

## Bookend Announcements

All non-complementary audio types have bookend announcements with humanized citation key. Same pattern as complementary audio where citation key is read at the beginning of each question -- helps audio-only learners quickly gain context.

- Summary/Transcript: "START: citation_key" / "END: citation_key"
- Lecture: "Today's lecture is posted as: citation_key" / "And with that we conclude: citation_key"

## Implemented (2026.03.13)

- Section-aware assembly with real silence between sections
- Bookend announcements for all 3 audio types
- Metadata filtering in reading pipeline
- No-filler section breaks (reading)
- Figure announce pattern (reading)
- Acronym extraction and injection
- Lecture structure enforcement (Intro, Results, Conclusion)
- Analogy rule tightened in lecture prompt
- Zotero annotation extraction script + skill

## Future Possibilities

- Voice cloning -- if the author created a voice clone it could always be in their own voice
- Config options to let users steer lecture style
- Zotero integration -- if you provide your Zotero API key, AI could know current project collection for context enrichment
- Author approval of transcript for quality assurance

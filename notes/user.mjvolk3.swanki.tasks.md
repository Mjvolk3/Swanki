---
id: wfacxevpjhl5s73ktns52b5
title: Tasks
desc: ''
updated: 1746127831445
created: 1710035491559
---


## 2025.05.01

- [x] Interactive with 8 bitdo works well with 🚘
- [x] Review written cards for `@radivojevicMachineLearningAutomated2020`
- [ ] We have issue with placement of % indicating front and back of cards. Really should be using pydantic model for controlled generation.

## 2025.04.26

- [x] complementary audio with image cards.
- [x] complementary audio override for `swanki-out`
- [x] Inject media reference for cards to call out which paper is being discussed. We can add an instruction like in every card start with this reference. Best thing to do is use the zotero pinned key... This will also make it easier to find where cards come from which can be an issue in merged anki libraries.

## 2025.04.25

- [x] New parser to avoid need vscode anki plugin → we are doing this to avoid annoying issues with converting latex to mathjax issues. I have posted on their issues... Basically would need to submit a PR. Also I want to have audio inclusion. Audio doesn't make much sense unless you have some automated pipeline because it is so cumbersome. With all of the necessary files.
- [x] gen md with complementary audio → haven't yet checked how this works with cloze cards... will most likely mess things up. → Might have to adjust paths for parsers too. Were set up with dendron in mind.

## 2024.08.25

- [x] Update pypi
- [x] Now works in standalone repo. Move Bishop Deep Learning to new repo.
- [x] Idea. Video to anki application - [Lawrence Leemis](https://www.youtube.com/@LawrenceLeemis/playlists)

## 2024.05.03

- [x] Get all cards for a chapter of DL Bishop. Make sure all images get cards.

## 2024.03.21

- [x] Can anki send http images? → yes.

## 2024.03.10

- [x] Show how images can be read and used to create additional text → [[swanki.image_reader]]

## 2024.03.09

- [x] Create MVP
- 🔲 My thought is to take a purely functional route, Use part path for now based on first pdf, then can thinking about alternate routes by alternating a configuration.
- 🔲 Find out how to create structured output. [Langchain pydantic output parser](https://python.langchain.com/docs/modules/model_io/output_parsers/types/pydantic)

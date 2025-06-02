---
id: fttgy1tk7pqnu50dmvnh8qr
title: '21'
desc: ''
updated: 1748827410535
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



- [ ] Cite pydantic in paper.
- [ ] Integrate edits from @Shekhar-Mishra
- 


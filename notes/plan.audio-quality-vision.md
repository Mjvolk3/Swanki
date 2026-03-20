---
id: 9ksk7m7mblhl3onc5hja5om
title: Audio Quality Vision
desc: ''
updated: 1773523431051
created: 1773523431051
---
/Users/michaelvolk/Documents/projects/Swanki_Data/merzbacherAccuratePredictionGene2025/merzbacherAccuratePredictionGene2025_0

on the most recent successful run.for merzbacher... I do not like the transcript. query eleven labs api we need better spacing. In fact if you could write me a skill to fetch the pink highlights from zotero I have left comments on areas where I detect issues in the transcript. See how we are pulling data from our zotero with the citation key. Then you will find 2 pdfs. see if you can just query the pink comments this is where there are mistakes in the reading transcript. They are of the kind. In general I think I will start marking up pdfs with orange, grey, and magenta for indicating information for use to improve on. Maybe just magenta for now. i called it pink earlier I looked it is magenta.

## Transcript

- Says words between sections that are unnecessary. filler not in the text - instead just pause (see how eleven labs can create pauses between sessions). In fact we also need to use this in lecture.
- The addresses were in the paper were read. There is some jumping around from reading figure to not reading it. This was very confusing. I think on figures we give `pause`, `figure x`, `pause` then read. This helps reader to jump to figure to crank through it. For actual inspection of the image I just do quick pausing of audio so we don't need to create pauses for this. It is too unpredictable. Pauses for sections are so important for reading here we must get them right.
- There are some small issues with pronunciation.
- Also we previously had some mechanism where acronym cache or something like it where if acronymns are introduced, especially for ones just created, but that we would read these aloud. This is very helpful to a new or unskilled reader like me 😊. Helps us link acronymns to concept while reading and actual can provide read enhancement to the experience.
- The goal of using transcript is to reduce pausing. Pausing is necessary for understanding and reviewing figures. Some people only read the figures, but we have always believed that science is more than data. It is also about its stories.

## Lecture Criticism

The lecture is a bit sloppy. We want lecture to be the highlight of the provided audios that are disconnected from cards. `transcript`, `lecture`, `summary`. I listened to the lecture and it was a bit meandering it seemed. We previously cited popular science, philisophical, but pretty technical writers who like to analogize, express, etc. But it can turn into the land of wiggeldy worp. Gibberish. I've found analogy helps but only up to a point and for a highly technical audience if we are warping language to obscure important truth it will be an issue. There are also no natural pauses and movements between sections. This lecture is borderline performance of sorts. It is a bit of a new category I imagine. Not podcast. Maybe a sort of solo podcast. But it is derived from published work. Scientists are often too busy to deliver such a thing to the public because they have to go back to working on the next project, to get the next grant. It would be even better if the author gave a thumbs up on the transcript. If they created a voice clone it could just always be put in their own voice. Probably worth getting some professional recording. Lecture is the ticket winner of the audio formats. The hook and the closer. We want them to be Classic. Personally I have found that I don't love changing narrators but I actually don't know what is better for learning. Sometimes mispronunciations trip me up and I loose the thread on more abstract points. You gt used to a voice and their pronunciations, and this actually helps improve delivery of information. We will make it up to people what they want, but for now I expect to stick with one lecturer. One teacher. You do want to find the right teacher, and once you do things should be a breeze.

So the first issues was sloppy writing. anal-ogizing. But we still must analogize. This is another one of the primary features. From listening to lectures there have been times where I thought there was some clever, or creative analogy. I found these stick in my head longer. This is maybe when in one of those author's books that I read he warns of analogizing, but we love them because they actually are good for memory.

We need more structures. It was like getting hit by a wave of prose then end. We need sections and we need more pauses. I suspect this should be less than the total number of sections because this must be shorter than a straight reading of the transcript I think we said approximately <50% or something like that. Maybe sections can be combined. intro can be longer and colorful. results sections could be combined into the story, be a bit punchy, a bit adventurous, detective like, sometimes taking the stance of what it might of been like. But don't over due it. People are sensitive to AI acting human, and tool much of this will make us a nonplussed cipher. The lecture is hooking the reader into the field, into the study, the experiments, then basically we want to formulate conclusion and discussion with research opportunities. We want to facilitate the possibility related or additional research. This could evolve as we add some more parts to the config st the user could steer this a bit. Actually default integration - if you provide your zotero api key you gives permission to read and write to your lib. We suggest doing it on a collection to get used to. Maybe config collection. I don't I do it on main bc it makes dev easier for me. This would be able to be enriched if the AI just new current project collection. or give it a git repo. can do check if zendron is enabled.

I just realized comments are kind of dead in zendron. maybe they create too much complexity. Like if we just make it import period delimited annotation graphs with comments. This is great!!!! This is great for the writing environment. This is more easily transportable. We just have to keep them synced. I think we need some better syncing method bc the current one is a bit slow on full import maybe it is faster without.. No I change my mind comments are still needed. Bc I forgot the whole point was to write a lot about a paper in a particular place that would get synced with zotero. I don't think our solution to this was great, but maybe we can fix it. Also read only on annotations. The major feature I really wanted was if we could make the links clickable with uri st that would open that comment in the zotero window. This would make the whole package complete. We would have a complete writing, developing, learning, publishing environment. Maybe this belongs in zendron repo. proably copy this to there.

## Summary

I kind of hate summary, but you really aren't supposed to like it. Summary is basically for teleportation. But through mind-time. I imagine the cycle being used like this. You listen lecture for interest, if actually interesting read the papers with transcript, that is really for deep dive. Then if we want to add it to the canon of knowledge we practice the cards and had them in the mix. If want to do a refresh of a particular topic from things we have already read we quickly compile a list of papers with the content we have queried over collect all audio files which we plan to put on zotero, then we collect all this put them in dir, zip, import to Book Player. Then sit down in dark room and jam it all. Its SW light speed traveling back to a previous world. This is the complete vision. So obviously summary is important, but it needs to follow paper structure have nice spacing, with pauses between reading sections and getting into them.

## All Audio

In complementary audio we always read the citation key and in the case of a book we append the chapter. This helps an audio only learner quickly gain context when cards are pooled so it can be difficult to quickly understand what materials are being discussed. I have found this tremendously helpful it helps me keep an index in my mind of papers. I want the same thing done for the other audio forms. I think for all of these it can take the same form, but I really don't want to get tired of it because this is a sort of standard formatting type thing. The first thing that came to mind is.

summary and transcript

```
"START : <citation_key>"

reading

"END : <citation_key>"
```

lecture

```
"Today's lecture is posted as : <citation_key>"

reading

"And with that we conclude : <citation_key>" #don't love it
```

If we hate the lecture idea we can make them all start and end.

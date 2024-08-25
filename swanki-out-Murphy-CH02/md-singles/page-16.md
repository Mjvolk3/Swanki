\begin{tabular}{lllll} 
Door 1 & Door 2 & Door 3 & Switch & Stay \\
\hline Car & - & - & Lose & Win \\
- & Car & - & Win & Lose \\
- & - & Car & Win & Lose
\end{tabular}

Table 2.2: 3 possible states for the Monty Hall game, showing that switching doors is two times better (on average) than staying with your original choice. Adapted from Table 6.1 of [PM18].

Intuitively, it seems it should make no difference, since your initial choice of door cannot influence the location of the prize. However, the fact that the host opened door 3 tells us something about the location of the prize, since he made his choice conditioned on the knowledge of the true location and on your choice. As we show below, you are in fact twice as likely to win the prize if you switch to door 2 .

To show this, we will use Bayes' rule. Let \(H_{i}\) denote the hypothesis that the prize is behind door \(i\). We make the following assumptions: the three hypotheses \(H_{1}, H_{2}\) and \(H_{3}\) are equiprobable a priori, i.e.,

\[
P\left(H_{1}\right)=P\left(H_{2}\right)=P\left(H_{3}\right)=\frac{1}{3}
\]

The datum we receive, after choosing door 1, is either \(Y=3\) and \(Y=2\) (meaning door 3 or 2 is opened, respectively). We assume that these two possible outcomes have the following probabilities. If the prize is behind door 1 , then the host selects at random between \(Y=2\) and \(Y=3\). Otherwise the choice of the host is forced and the probabilities are 0 and 1.

![](https://cdn.mathpix.com/cropped/2024_06_13_ed018759cfa69e78e314g-1.jpg?height=107&width=887&top_left_y=1176&top_left_x=301)

Now, using Bayes' theorem, we evaluate the posterior probabilities of the hypotheses:

\[
\begin{aligned}
& P\left(H_{i} \mid Y=3\right)=\frac{P\left(Y=3 \mid H_{i}\right) P\left(H_{i}\right)}{P(Y=3)} \\
& \left|P\left(H_{1} \mid Y=3\right)=\frac{(1 / 2)(1 / 3)}{P(Y=3)}\right| P\left(H_{2} \mid Y=3\right)=\frac{(1)(1 / 3)}{P(Y=3)}\left|P\left(H_{3} \mid Y=3\right)=\frac{(0)(1 / 3)}{P(Y=3)}\right|
\end{aligned}
\]

The denominator \(P(Y=3)\) is \(P(Y=3)=\frac{1}{6}+\frac{1}{3}=\frac{1}{2}\). So

\[
\left.\left|P\left(H_{1} \mid Y=3\right)=\frac{1}{3}\right| P\left(H_{2} \mid Y=3\right)=\frac{2}{3} \right\rvert\, P\left(H_{3} \mid Y=3\right)=0
\]

So the contestant should switch to door 2 in order to have the biggest chance of getting the prize. See Table 2.2 for a worked example.

Many people find this outcome surprising. One way to make it more intuitive is to perform a thought experiment in which the game is played with a million doors. The rules are now that the contestant chooses one door, then the game show host opens 999,998 doors in such a way as not to reveal the prize, leaving the contestant's selected door and one other door closed. The contestant may now stick or switch. Imagine the contestant confronted by a million doors, of which doors 1 and 234,598 have not been opened, door 1 having been the contestant's initial guess. Where do you think the prize is?

Draft of "Probabilistic Machine Learning: An Introduction". August 8, 2022
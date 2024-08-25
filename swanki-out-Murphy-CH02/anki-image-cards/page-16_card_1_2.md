## Using Bayes' Theorem to evaluate posterior probabilities

![](https://cdn.mathpix.com/cropped/2024_06_13_ed018759cfa69e78e314g-1.jpg?height=107&width=887&top_left_y=1176&top_left_x=301)

What are the posterior probabilities $P\left(H_{1} \mid Y=3\right)$, $P\left(H_{2} \mid Y=3\right)$, and $P\left(H_{3} \mid Y=3\right)$ using Bayes' theorem?

%

From Bayes' theorem:

$$
\begin{aligned}
P\left(H_{i} \mid Y=3\right) &= \frac{P\left(Y=3 \mid H_{i}\right) P\left(H_{i}\right)}{P(Y=3)} \\
P\left(H_{1} \mid Y=3\right) &= \frac{(1/2)(1/3)}{1/2} = \frac{1}{3} \\
P\left(H_{2} \mid Y=3\right) &= \frac{(1)(1/3)}{1/2} = \frac{2}{3} \\
P\left(H_{3} \mid Y=3\right) &= \frac{(0)(1/3)}{1/2} = 0
\end{aligned}
$$

Therefore, the posterior probabilities are:

$$
\left|P\left(H_{1} \mid Y=3\right)=\frac{1}{3}\right| \\
P\left(H_{2} \mid Y=3\right)=\frac{2}{3} \\
P\left(H_{3} \mid Y=3\right) = 0
$$

- #probability-theory, #bayes-theorem, #monty-hall-problem

## Determining the best strategy in the Monty Hall problem

![](https://cdn.mathpix.com/cropped/2024_06_13_ed018759cfa69e78e314g-1.jpg?height=107&width=887&top_left_y=1176&top_left_x=301)

Based on the calculated posterior probabilities, what should the contestant do to maximize their chances of winning the prize in the Monty Hall problem?

%

The contestant should switch to door 2 because the probability $P\left(H_{2} \mid Y=3\right)$ is $\frac{2}{3}$, which is higher than the probability $P\left(H_{1} \mid Y=3\right)$ of $\frac{1}{3}$. Switching doors will give the contestant the highest chance of winning the prize.

- #decision-theory, #probability-theory, #monty-hall-problem
### Card 1

The Monty Hall problem demonstrates a counterintuitive result in probability. Given doors 1, 2, and 3, the host opens one door without revealing the prize. Explain how the probabilities change using Bayes' theorem when initially choosing door 1 and the host opens door 3.

Bayes' theorem helps to update the probability of our hypothesis given new evidence. Here, the priors are:

$$
P\left(H_{1}\right)=P\left(H_{2}\right)=P\left(H_{3}\right)=\frac{1}{3}
$$

When the host opens door 3, we calculate:

$$
\begin{aligned}
& P\left(H_{i} \mid Y=3\right)=\frac{P\left(Y=3 \mid H_{i}\right) P\left(H_{i}\right)}{P(Y=3)} \\
& P\left(H_{1} \mid Y=3\right)=\frac{(1 / 2)(1 / 3)}{1 / 2} = \frac{1}{3} \\
& P\left(H_{2} \mid Y=3\right)=\frac{(1)(1 / 3)}{1 / 2} = \frac{2}{3} \\
& P\left(H_{3} \mid Y=3\right)=\frac{(0)(1 / 3)}{1 / 2} = 0
\end{aligned}
$$

The denominator, $P(Y=3)$, is $P(Y=3)=\frac{1}{6}+\frac{1}{3}=\frac{1}{2}$.

- #probability, #bayes-theorem, #monty-hall

### Card 2

Given that all doors are initially equally likely, describe the probabilities $P(H_i)$ before any doors are opened.

The initial probabilities, assuming each door has an equal chance of hiding the prize, are:

$$
P\left(H_{1}\right)=P\left(H_{2}\right)=P\left(H_{3}\right)=\frac{1}{3}
$$

These represent an equal likelihood for each hypothesis $H_i$ that the prize is behind door $i$.

- #probability, #hypothesis, #monty-hall

### Card 3

Why does switching doors in the Monty Hall problem increase your odds of winning compared to sticking with your initial choice?

Switching doors increases the winning probability because the host's action of opening a door is dependent on the prize's location. Initially, the probabilities are equal ($P(H_{i}) = \frac{1}{3}$). After the host reveals a goat behind one of the unchosen doors, the probability distribution changes:

$$
\begin{aligned}
& P\left(H_{1} \mid Y=3\right)=\frac{1}{3} \\
& P\left(H_{2} \mid Y=3\right)=\frac{2}{3} \\
& P\left(H_{3} \mid Y=3\right)=0
\end{aligned}
$$

Thus, switching doubles your odds of winning to $\frac{2}{3}$ compared to staying.

- #probability, #decision-theory, #monty-hall

### Card 4

In the context of the Monty Hall problem, define the term "equiprobable a priori" and its significance.

"Equiprobable a priori" means that before any information is revealed, all outcomes are considered equally likely. For the Monty Hall problem:

$$
P\left(H_{1}\right)=P\left(H_{2}\right)=P\left(H_{3}\right)=\frac{1}{3}
$$

This assumption allows us to use Bayes' theorem effectively to update the probabilities when new information (host opening a door) is provided.

- #probability-theory, #prior-probility, #monty-hall

### Card 5

Apply Bayes' theorem to calculate $P\left(H_{2} \mid Y=3\right)$, given the following probabilities: $P\left(H_{2}\right) = \frac{1}{3}$ and $P(Y=3|H_{2}) = 1$.

Using Bayes' theorem:

$$
P\left(H_{i} \mid Y=3\right) = \frac{P\left(Y=3 \mid H_{i}\right) P\left(H_{i}\right)}{P(Y=3)}
$$

Given:

$$
P\left(H_{2}\right) = \frac{1}{3}, \quad P(Y=3|H_{2}) = 1
$$

We calculate:

$$
P\left(H_{2} \mid Y=3\right) = \frac{(1) \cdot \left(\frac{1}{3}\right)}{\frac{1}{2}} = \frac{2}{3}
$$

The denominator $P(Y=3)$ was previously found to be $\frac{1}{2}$.

- #bayes-theorem, #conditional-probability, #monty-hall

### Card 6

Describe the thought experiment involving a million doors in the Monty Hall problem and explain how it clarifies the benefit of switching.

In the thought experiment with a million doors, the contestant chooses one door, and the host opens 999,998 doors without revealing the prize, leaving only the contestant's door and one other door closed. Given the small initial probability of $\frac{1}{1,000,000}$ for the chosen door having the prize and the high probability of $\frac{999,999}{1,000,000}$ that it's in the remaining unopened door, switching is clearly advantageous.

This vastly larger scale makes the counterintuitive nature of the original problem more intuitive by highlighting the disparity in probabilities even more starkly.

- #probability, #decision-theory, #monty-hall
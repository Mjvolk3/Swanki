## What is the definition of an inverse probability problem, and how does it differ from regular probability problems?

Inverse probability is concerned with inferring the state of the world ($h$) from observations of outcomes ($y$), in contrast to regular probability, which predicts a distribution over outcomes given knowledge about the state of the world.

$$
\text{Regular: } p(y \mid h)
$$
$$
\text{Inverse: } p(h \mid y)
$$

- #probability-theory, #inverse-problems

## Consider trying to infer a 3D shape $h$ from a 2D image $y$. What makes this an ill-posed problem, and which figure illustrates this concept?

Inferring a 3D shape $h$ from a 2D image $y$ is an ill-posed problem because there are multiple possible hidden $h$'s consistent with the same observed $y$. This concept is illustrated in Figure 2.8 of the paper.

- #visual-scene-understanding, #ill-posed-problems

## How can Bayes' rule be applied to solve inverse problems? Include the relevant expressions for forward model and prior.

Bayes' rule is applied to solve inverse problems by computing the posterior distribution $p(h \mid y)$, which requires specifying the forward model $p(y \mid h)$ and a prior $p(h)$. 

$$
p(h \mid y) \propto p(y \mid h) p(h)
$$

- #probability-theory, #bayes-rule

## What is the Bernoulli distribution, and how is it used to model binary events? Include the expression for a Bernoulli trial.

The Bernoulli distribution models binary events, such as coin tosses. If $Y=1$ denotes heads and $Y=0$ denotes tails, with $p(Y=1)=\theta$ and $p(Y=0)=1-\theta$, this is expressed as:

$$
Y \sim \operatorname{Ber}(\theta)
$$

- #probability-distributions, #bernoulli-distribution

## Given a coin with a probability $\theta$ of landing heads, what are $p(Y=1)$ and $p(Y=0)$ in a Bernoulli trial?

In a Bernoulli trial for a coin with probability $\theta$ of landing heads:
- $p(Y=1) = \theta$
- $p(Y=0) = 1 - \theta$

- #probability-distributions, #bernoulli-trial

## In the context of inverse problems, what role do the prior $p(h)$ and the forward model $p(y \mid h)$ play in Bayesian inference?

In Bayesian inference for inverse problems:
- The **prior** $p(h)$ represents prior knowledge about the state's distribution.
- The **forward model** $p(y \mid h)$ describes the probability of observing outcomes given the state.

Both are used to compute the posterior distribution $p(h \mid y)$:

$$
p(h \mid y) \propto p(y \mid h) p(h)
$$

- #probability-theory, #bayesian-inference
Here are the six flashcards generated from the chunk of text you provided:

---

## Describe Bayes' rule and its components.

Bayes' rule is a formula for computing the probability distribution over possible values of an unknown quantity $H$ given some observed data $Y=y$.

$$
p(H=h \mid Y=y)=\frac{p(H=h) p(Y=y \mid H=h)}{p(Y=y)}
$$

- The term $p(H)$ represents the prior distribution.
- The term $p(Y \mid H=h)$ represents the observation distribution.
- When we evaluate $p(Y \mid H=h)$ at $y$, we get the likelihood, $p(Y=y \mid H=h)$.
- $p(Y=y)$ is the marginal likelihood.

- #probability-theory.bayes-rule, #statistics.bayesian-inference

---

## What is the product rule of probability and how is it related to Bayes' rule?

The product rule of probability states that the joint probability $p(h, y)$ can be expressed as:

$$
p(h \mid y) p(y) = p(h) p(y \mid h) = p(h, y)
$$

This identity directly leads to the formulation of Bayes' rule:

$$
p(H=h \mid Y=y)=\frac{p(H=h) p(Y=y \mid H=h)}{p(Y=y)}
$$

- #probability-theory.product-rule, #statistics.bayesian-inference

---

## Explain the prior distribution and observation distribution in the context of Bayes' rule.

In Bayes' rule:
- The prior distribution $p(H)$ represents our knowledge about possible values of $H$ before any data is observed.
- The observation distribution $p(Y \mid H=h)$ represents the expected distribution over outcomes $Y$ given that $H=h$.

This can be written as:

$$
p(H=h \mid Y=y)=\frac{p(H=h) p(Y=y \mid H=h)}{p(Y=y)}
$$

- #statistics.bayesian-inference, #probability-theory.bayes-rule

---

## Define the likelihood function in Bayes' rule.

The likelihood function in Bayes' rule is given by:

$$
p(Y=y \mid H=h)
$$

It represents the probability of the observed data $Y=y$ given the hypothesis $H=h$. Importantly, it is a function of $h$ because $y$ is fixed, but it is not a probability distribution since it does not sum to one.

- #statistics.likelihood, #probability-theory.bayes-rule

---

## What is the marginal likelihood in Bayes' rule?

The marginal likelihood, $p(Y=y)$, is computed by marginalizing over the unknown $H$:

$$
p(Y=y)=\sum_{h' \in \mathcal{H}} p(H=h') p(Y=y \mid H=h')
$$

It is necessary to convert the unnormalized joint distribution to a normalized distribution.

- #probability-theory.marginal-likelihood, #statistics.bayesian-inference

---

## Derive the expression for the marginal likelihood in Bayes' rule.

The marginal likelihood is derived by summing over all possible values of the hidden variable $H$:

$$
p(Y=y)=\sum_{h^{\prime} \in \mathcal{H}} p(H=h') p(Y=y \mid H=h') = \sum_{h^{\prime} \in \mathcal{H}} p(H=h', Y = y)
$$

This is necessary for normalizing the joint distribution $p(H=h, Y=y)$.

- #probability-theory.marginal-likelihood.derivation, #statistics.bayesian-inference

---
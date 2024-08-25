## Explain the concept of conditional independence in the context of Exercise 2.1.

The concept of conditional independence is best illustrated using Bayes' rule. For random variables $E_1$ and $E_2$ to be conditionally independent given $H$, denote:

$$
P(E_1 \perp E_2 \mid H)
$$

Mathematically, $E_1$ and $E_2$ being conditionally independent given $H$ can be expressed as:

$$
P(E_1, E_2 \mid H) = P(E_1 \mid H) P(E_2 \mid H)
$$

Let's consider the three given sets of numbers to determine their sufficiency for calculating $\vec{P}(H \mid e_1, e_2)$:

- Set 1: $P(e_1, e_2)$, $P(H)$, $P(e_1 \mid H)$, $P(e_2 \mid H)$
- Set 2: $P(e_1, e_2)$, $P(H)$, $P(e_1, e_2 \mid H)$
- Set 3: $P(e_1 \mid H)$, $P(e_2 \mid H)$, $P(H)$

By applying Bayes' rule and the conditional independence assumption, verify which set(s) are sufficient for computing $\vec{P}(H \mid e_1, e_2)$.

- #probability-theory, #statistical-inference

## Given the three sets of numbers in Exercise 2.1, which are sufficient to compute $\vec{P}(H \mid e_1, e_2)$ without the conditional independence assumption?

The goal is to compute the vector:

$$
\vec{P}(H \mid e_1, e_2) = \left(P(H=1 \mid e_1, e_2), \ldots, P(H=K \mid e_1, e_2)\right)
$$

Using Bayes' rule:

$$
P(H \mid e_1, e_2) = \frac{P(e_1, e_2 \mid H) P(H)}{P(e_1, e_2)}
$$

Set 2 is sufficient because it directly provides $P(e_1, e_2 \mid H)$, $P(H)$, and $P(e_1, e_2)$:

$$
\text {ii.} \ P(e_1, e_2), \ P(H), \ P(e_1, e_2 \mid H) 
$$
are sufficient for the calculation.

- #probability-theory, #conditional-independence, #bayesian-inference

## Given the assumption $E_1 \perp E_2 \mid H$, which sets from Exercise 2.1 are sufficient to compute $\vec{P}(H \mid e_1, e_2)$?

Under the assumption $E_1 \perp E_2 \mid H$, we have:

$$
P(E_1, E_2 \mid H) = P(E_1 \mid H) P(E_2 \mid H)
$$

Thus, the calculation of $\vec{P}(H \mid e_1, e_2)$ simplifies to:

$$
P(H \mid e_1, e_2) = \frac{P(e_1 \mid H) P(e_2 \mid H) P(H)}{P(e_1, e_2)}
$$

Sets 1 and 3 are sufficient due to the provided conditional independence condition. Specifically, Set 1 provides all needed conditional probabilities directly:

$$
\text {i. } P(e_1, e_2), P(H), P(e_1 \mid H), P(e_2 \mid H)
$$

and Set 3 also suffices:

$$
\text {iii. } P(e_1 \mid H), P(e_2 \mid H), P(H)
$$

- #probability-theory, #conditional-independence, #bayesian-inference

## Demonstrate that pairwise independence does not imply mutual independence by considering random variables $X_1$, $X_2$, and $X_3$.

Consider three random variables $X_1$, $X_2$, and $X_3$. If $X_1$ and $X_2$ are independent and $X_1$ and $X_3$ are independent, it does not necessarily mean that $X_1, X_2, X_3$ are mutually independent.

To be mutually independent, the joint probability, $P(X_1, X_2, X_3)$, must factorize as:

$$
P(X_1, X_2, X_3) = P(X_1) P(X_2) P(X_3)
$$

However, pairwise independence only ensures:

$$
P(X_1, X_2) = P(X_1) P(X_2)
$$

$$
P(X_1, X_3) = P(X_1) P(X_3)
$$

Imagine a scenario with unequal marginal probabilities for non-mutual independence to persist even with pairwise independence.

- #probability-theory, #independence

## Explain the technique of computing a distribution via the change of variables demonstrated in the figure from the paper.

In the context of Figure 2.24, suppose $y = x^2$, where $p(x)$ follows a uniform distribution. To find the distribution $p(y)$, use the change of variables technique:

If $X \sim \text{Uniform}(a, b)$, then $p(X) = \frac{1}{b-a}$.

1. Define the new variable $Y = g(X) = X^2$.
2. Compute the Jacobian determinant: $\left| \frac{dX}{dY} \right|$.
3. Use the formula for transformation of variables in probability distributions:

$$
p_Y(y) = p_X(x) \left| \frac{dx}{dy} \right|
$$

Apply these steps to generate $p_Y(y)$ from a uniform $p_X(x)$. Here, $X$ is mapped to $Y$ through a quadratic transformation affecting the distribution.

- #probability-theory, #change-of-variables

## Describe the Monte Carlo approximation method as applied in the figure from the paper.

Monte Carlo approximation involves using random sampling to estimate the distribution of a function of random variables. For $y = x^2$:

1. Draw several random samples from the distribution $p(x)$.
2. Compute $y_i = x_i^2$ for each sample $x_i$.
3. Construct an empirical histogram of $y_i$ to approximate $p(y)$.

In Figure 2.24, the left plot shows the uniform distribution $p(x)$, the middle plot shows the analytical result of $p(y)$, and the right plot shows the Monte Carlo approximation of $p(y)$. This method is often useful when analytical solutions are difficult.

- #monte-carlo, #probability-theory, #approximation

## Using Exercise 2.2, define pairwise independence and give an example where it does not imply mutual independence.

Pairwise independence for two random variables $X_1$ and $X_2$ means:

$$
p(X_2 \mid X_1) = p(X_2)
$$

and hence:

$$
p(X_2, X_1) = p(X_1) p(X_2)
$$

However, if we have three variables $X_1$, $X_2$, and $X_3$ that are pairwise independent:

$$
p(X_2, X_1) = p(X_1) p(X_2)
$$

$$
p(X_3, X_1) = p(X_1) p(X_3)
$$

$$
p(X_3, X_2) = p(X_2) p(X_3)
$$

They are not necessarily mutually independent, which requires:

$$
p(X_1, X_2, X_3) = p(X_1) p(X_2) p(X_3)
$$

Example: Consider $X_1, X_2, X_3$ where each can independently take values $+1$ or $-1$, but we ensure that the product always equals $+1$. Then $X_1$ and $X_2$ are independent, but $X_1$, $X_2$, $X_3$ are not mutually independent.

- #probability-theory, #independence
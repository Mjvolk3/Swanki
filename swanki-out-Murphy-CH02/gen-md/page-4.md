## What is the definition of a probability mass function (pmf)?
 
A probability mass function (pmf) is defined as the function that computes the probability of events corresponding to each possible value of a discrete random variable: 

$$ p(x) \triangleq \operatorname{Pr}(X=x) $$

The pmf satisfies the following properties: 

$$ 0 \leq p(x) \leq 1 $$
and 
$$ \sum_{x \in \mathcal{X}} p(x)=1 $$

- #probability-theory, #pmf.definition

## What are the properties that a probability mass function (pmf) must satisfy?

A probability mass function (pmf), $p(x)$, must satisfy the properties:

$$ 0 \leq p(x) \leq 1 $$
and
$$ \sum_{x \in \mathcal{X}} p(x)=1 $$

- #probability-theory, #pmf.properties

## Can two pmf's be defined on the same state space? Use Figure 2.1 as context to explain.

Yes, two different pmf's can be defined on the same state space $\mathcal{X}$. For example, Figure 2.1 shows two pmf's defined on $\mathcal{X}=\{1,2,3,4\}$: 

1. A uniform distribution where $p(x)=\frac{1}{4}$.
2. A degenerate distribution where $p(x)=\mathbb{I}(x=1)$, meaning all probability mass is on $x=1$.

$$ \mathbb{I}(x=1) = \begin {cases} 
1 & \text{if } x = 1 \\
0 & \text{otherwise} 
\end{cases}
$$

- #probability-theory, #pmf.multiple-distributions

## What is the formula to compute the probability of being in an interval $(X \in \mathcal{C})$ in terms of cumulative distribution functions (cdf)?

The formula to compute the probability of being in an interval $C=(a < X \leq b)$ is:

$$
\operatorname{Pr}(C) = \operatorname{Pr}(B) - \operatorname{Pr}(A)
$$

where:
- $A = (X \leq a)$
- $B = (X \leq b)$

Both $A$ and $C$ are mutually exclusive, and $B=A \vee C$.

- #probability-theory, #cdf.interval-probability

## Define a continuous random variable and explain how it can be related to discrete random variables using intervals.

A continuous random variable $X \in \mathbb{R}$ is a real-valued quantity that does not have a finite or countable set of distinct possible values. However, we can partition the real line into countable intervals and consider the probability of $X$ residing in these intervals. By shrinking the size of these intervals to zero, we can approximate the behavior similar to discrete random variables.

- #probability-theory, #continuous-rv.definition

## How does the sum rule apply to mutually exclusive events in relation to cumulative distribution functions (cdf)?

The sum rule states that if two events, $A$ and $C$, are mutually exclusive (i.e., they cannot occur simultaneously), then the probability of their union is the sum of their individual probabilities. In terms of cumulative distribution functions, for events $A=(X \leq a)$ and $C=(a < X \leq b)$ where $a < b$ and $B=A \vee C$:

$$
\operatorname{Pr}(B) = \operatorname{Pr}(A) + \operatorname{Pr}(C)
$$

Consequently, 

$$
\operatorname{Pr}(C) = \operatorname{Pr}(B) - \operatorname{Pr}(A)
$$

- #probability-theory, #cdf.sum-rule
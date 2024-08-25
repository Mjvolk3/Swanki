## How is the marginal probability $p(X=x_i)$ defined in terms of $c_i$ and $N$?

The marginal probability $p(X=x_i)$ is defined as the ratio of the number of instances where the random variable $X$ takes the value $x_i$ to the total number of instances $N$, expressed mathematically as:

$$
p(X=x_i) = \frac{c_i}{N}
$$

Here, $c_i$ represents the number of instances in column $i$, corresponding to $X=x_i$.

- #probability, #statistics.marginal-probability, #math-formulas

## How do we derive the sum rule of probability for a random variable $X$?

The sum rule of probability for $X$ is derived using the relationship:

$$
p(X=x_i) = \sum_{j=1}^{M} p(X=x_i, Y=y_j)
$$

This is achieved by recognizing that the marginal probability $p(X=x_i)$ can be represented as the sum of the joint probabilities over all possible values of $Y$, taking into account all cells in the corresponding column of the two-dimensional frequency array. 

- #probability, #statistics.sum-rule, #math-formulas

## Derive the formula for the conditional probability $p(Y=y_j | X=x_i)$.

The conditional probability $p(Y=y_j | X=x_i)$ is derived as follows:

1. Identify the subset of instances where $X=x_i$, which totals $c_i$. 
2. From that subset, determine $n_{ij}$, the number of instances where $Y=y_j$.
3. The conditional probability is then given by the fraction of $n_{ij}$ within $c_i$, formalized as:

$$
p(Y=y_j | X=x_i) = \frac{n_{ij}}{c_i}
$$

This reflects the probability of $Y$ being $y_j$, given that $X$ has already occurred as $x_i$.

- #probability, #statistics.conditional-probability, #math-formulas

## What ensures that the sum of all marginal probabilities $p(X=x_i)$ over all possible values of $X$ equals one?

The condition that the sum of all marginal probabilities equals one is derived from the total probability law and the completeness of the sample space of $X$. It is formalized as:

$$
\sum_{i=1}^{L} p(X=x_i) = 1
$$

This result follows from the fact that the sum of counts in all columns equals $N$, and each marginal probability is a fraction of $N$, ensuring their sum is unity.

- #probability, #statistics.total-probability-theorem, #math-formulas

## Explain the normalization condition for conditional probabilities $p(Y=y_j | X=x_i)$.

This normalization condition states that the sum of conditional probabilities over all possible outcomes of $Y$, given a specific $X=x_i$, must equal one:

$$
\sum_{j=1}^{M} p(Y=y_j | X=x_i) = 1
$$

This is derived by summing the conditional probabilities, each defined as $p(Y=y_j | X=x_i) = \frac{n_{ij}}{c_i}$, over all $j$, and using the fact that $\sum_{j} n_{ij} = c_i$. This condition reflects the completeness of the probability distribution for $Y$ given $X=x_i$.

- #probability, #statistics.conditional-probability, #math-formulas
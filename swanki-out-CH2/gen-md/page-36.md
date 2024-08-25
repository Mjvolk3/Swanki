## Given a prior probability of cancer $p(C=1)=0.001$, calculate the posterior probability of having cancer given a positive test result, $p(C=1 \mid T=1)$.

The Bayes' theorem provides a way to calculate the posterior probability as follows:
$$
p(C=1 \mid T=1) = \frac{p(T=1 \mid C=1) \cdot p(C=1)}{p(T=1)}
$$
You need to substitute values for $p(T=1 \mid C=1)$ (the probability of a positive test given the presence of cancer) and $p(T=1)$ (the total probability of a positive test) into the equation.

- #statistics.probability-theory, #medical-screening.bayesian-updating

## Describe the concept of non-transitivity in random variables and how it applies to Efron's dice.

Non-transitivity in random variables means that if we have $x, y, z$ such that $x>y$ and $y>z$, it doesn't necessarily follow that $x>z$. For Efron's dice, each pair of dice can be ordered such that one more frequently shows a higher face value than the other. Surprisingly, for Efron's dice, the order can create a cyclical dominance where each die has a $2/3$ probability of rolling a higher number than the previous die in the cycle.

- #mathematics.statistics, #mathematics.probability.non-transitivity, #games-and-puzzles.dice-games

## Derive the formula for the convolution of two independent random variable distributions, $p_{\mathbf{y}}(\mathbf{y})$.

Given two independent random variables $\mathbf{u} \sim p_{\mathbf{u}}(\mathbf{u})$ and $\mathbf{v} \sim p_{\mathbf{v}}(\mathbf{v})$, the distribution for their sum $\mathbf{y} = \mathbf{u} + \mathbf{v}$ is given by:
$$
p(\mathbf{y}) = \int p_{\mathbf{u}}(\mathbf{u}) p_{\mathbf{v}}(\mathbf{y}-\mathbf{u}) \mathrm{d}\mathbf{u}
$$
This operation is a convolution, reflecting how the probability density of $\mathbf{y}$ at any point is the integral of the product of the densities of $\mathbf{u}$ and a shifted $\mathbf{v}$ over all possible values of $\mathbf{u}$.

- #mathematics.probability-theory, #mathematics.convolution, #statistics.random-variables

## Verify the normalization of the uniform distribution as defined in the text and calculate its mean and variance.

Assuming the uniform distribution over interval $[a, b]$, normalization requires:
$$
\int_a^b \frac{1}{b-a} \, dx = 1
$$
The mean ($\mu$) and variance ($\sigma^2$) for the uniform distribution are calculated as follows:
$$
\mu = \frac{a+b}{2}, \quad \sigma^2 = \frac{(b-a)^2}{12}
$$
These results demonstrate basic properties of the uniform distribution and ensure that the basic statistical measures are appropriately represented.

- #mathematics.probability-theory, #statistics.distribution-properties, #mathematics.uniform-distribution

## Verify the normalization of the exponential and Laplace distributions mentioned in the paper.

For the exponential distribution defined by parameter $λ$:
$$
\int_0^\infty \lambda e^{-\lambda x} \, dx = 1
$$
For the Laplace distribution with mean zero and diversity $b$:
$$
\int_{-\infty}^\infty \frac{1}{2b} e^{-|x|/b} \, dx = 1
$$
These integrations confirm that both distributions are normalized, satisfying the property that the total area under the distribution's probability density function is 1.

- #mathematics.probability-theory, #statistics.distribution-properties, #mathematics.exponential-distribution, #mathematics.laplace-distribution
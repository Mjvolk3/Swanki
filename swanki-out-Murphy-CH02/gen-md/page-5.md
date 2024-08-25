## Derive the probability of a random variable $X$ being within the interval $(a, b]$ using the cdf.

Given the cumulative distribution function (cdf) $P(x) = \operatorname{Pr}(X \leq x)$, we can compute the probability of $X$ being in the interval $(a, b]$ as:

$$
\operatorname{Pr}(a < X \leq b) = P(b) - P(a)
$$

- #probability-theory, #statistics.cdf


## What is the probability density function (pdf) and how is it related to the cdf?

The probability density function (pdf) $p(x)$ is defined as the derivative of the cumulative distribution function (cdf) $P(x)$. Mathematically, this is expressed as:

$$
p(x) \triangleq \frac{d}{d x} P(x)
$$

(Note that this derivative does not always exist, in which case the pdf is not defined.)

- #probability-theory, #statistics.pdf

## How can we compute the probability of a random variable $X$ being within the interval $(a, b]$ using the pdf?

Given the pdf $p(x)$, the probability of a continuous variable $X$ being in the interval $(a, b]$ is computed as:

$$
\operatorname{Pr}(a < X \leq b) = \int_{a}^{b} p(x) d x = P(b) - P(a)
$$

- #probability-theory, #statistics.pdf

## Explain the approximation for the probability of $X$ being in a small interval around $x$.

For a small interval around $x$, the probability of $X$ being within $(x, x + dx]$ is approximately:

$$
\operatorname{Pr}(x < X \leq x + dx) \approx p(x) dx
$$

This implies that the probability of $X$ being in a small interval around $x$ is the density at $x$ times the width of the interval.

- #probability-theory, #statistics.approximation

## Define the non-shaded probability region in Figure 2.2b and the corresponding cutoff points using the cdf $\Phi$.

In Figure 2.2b, the non-shaded region contains $1 - \alpha$ of the probability mass. The cutoff points for this region are defined as $\Phi^{-1}(\alpha / 2)$ and $\Phi^{-1}(1 - \alpha / 2)$. By symmetry, we have:

$$
\Phi^{-1}(1 - \alpha / 2) = -\Phi^{-1}(\alpha / 2)
$$

where $\Φ$ is the cdf of the Gaussian distribution.

- #probability-theory, #statistics.cdf

## Provide an example of how a cdf can be used to find the probability of a random variable within a specified interval.

Consider a standard normal distribution $\mathcal{N}(0,1)$ with cdf $\Phi(x)$. To find the probability of $X$ being within the interval $(-1, 1]$, we use:

$$
P(-1 < X \leq 1) = \Phi(1) - \Phi(-1)
$$

Knowing that $\Phi(-x) = 1 - \Phi(x)$ for the standard normal distribution, it follows:

$$
P(-1 < X \leq 1) = \Phi(1) - (1 - \Phi(1)) = 2\Phi(1) - 1
$$

- #probability-theory, #statistics.cdf
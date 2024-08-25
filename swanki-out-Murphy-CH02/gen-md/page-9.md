## What is the expected value of $X^2$ in terms of the mean $\mu$ and variance $\sigma^2$?

The expected value of $X^2$ is given by:

$$
\mathbb{E}\left[X^{2}\right]=\sigma^{2}+\mu^{2}
$$

Where:
- $\mathbb{E}\left[X^{2}\right]$ is the expected value of $X^2$
- $\sigma^2$ is the variance of $X$
- $\mu$ is the mean of $X$

The relation $\mathbb{E}\left[X^{2}\right]=\sigma^{2}+\mu^{2}$ captures how the second moment of a random variable can be decomposed into its variance and the square of its mean.

- #statistics, #moments.expected-value

## Define the standard deviation of a random variable $X$.

The standard deviation of a random variable $X$ is defined as:

$$
\operatorname{std}[X] \triangleq \sqrt{\mathbb{V}[X]}=\sigma
$$

Where:
- $\operatorname{std}[X]$ is the standard deviation of $X$
- $\mathbb{V}[X]$ is the variance of $X$
- $\sigma$ is another symbol representing the standard deviation, having the same units as $X$ itself.

- #statistics, #dispersion.standard-deviation

## What is the variance of a linear transformation $aX + b$ of a random variable $X$?

The variance of $aX + b$ is given by:

$$
\mathbb{V}[aX + b] = a^{2} \mathbb{V}[X]
$$

Where:
- $\mathbb{V}[X]$ is the variance of the original random variable $X$
- $a$ and $b$ are constants.

The constant $b$ does not affect the variance, while the constant $a$ scales the variance by $a^2$.

- #statistics, #variance.transformation

## What is the variance of the sum of $n$ independent random variables $X_i$?

The variance of the sum of $n$ independent random variables is:

$$
\mathbb{V}\left[\sum_{i=1}^{n} X_{i}\right] = \sum_{i=1}^{n} \mathbb{V}[X_i]
$$

Where:
- $X_i$ are the independent random variables
- $\mathbb{V}[X_i]$ are their variances
- $i$ ranges from $1$ to $n$

This property arises because the covariance terms are zero for independent random variables.

- #statistics, #variance.sum

## Derive the variance of the product of $n$ random variables $X_i$.

The variance of the product of $n$ random variables $X_i$ is derived as follows:

$$
\begin{aligned}
\mathbb{V}\left[\prod_{i=1}^{n} X_{i}\right] & =\mathbb{E}\left[\left(\prod_{i} X_{i}\right)^{2}\right]-\left(\mathbb{E}\left[\prod_{i} X_{i}\right]\right)^{2} \\
& =\mathbb{E}\left[\prod_{i} X_{i}^{2}\right] - \left(\prod_{i} \mathbb{E}[X_i]\right)^{2} \\
& =\prod_{i} \mathbb{E}[X_i^2] - \prod_{i} \left(\mathbb{E}[X_i]\right)^2 \\
& =\prod_{i} (\mathbb{V}[X_i] + (\mathbb{E}[X_i])^2) - \prod_{i} (\mathbb{E}[X_i])^2 \\
& =\prod_{i} (\sigma_i^2 + \mu_i^2) - \prod_{i} \mu_i^2
\end{aligned}
$$

Where:
- $\sigma_i^2$ is the variance of $X_i$
- $\mu_i$ is the mean of $X_i$

- #statistics, #variance.product

## What is the mode of a distribution?

The mode of a distribution is the value with the highest probability mass or probability density:

$$
\boldsymbol{x}^{*} = \underset{\boldsymbol{x}}{\operatorname{argmax}} p(\boldsymbol{x})
$$

Where:
- $p(\boldsymbol{x})$ is the probability mass function (PMF) for discrete distributions or the probability density function (PDF) for continuous distributions
- $\boldsymbol{x}^{*}$ is the mode

If the distribution is multimodal, the mode may not be unique.

- #statistics, #mode.mode

## State and explain the law of iterated expectations.

The law of iterated expectations, also known as the law of total expectation, states that:

$$
\mathbb{E}[X] = \mathbb{E}_{Y}[\mathbb{E}[X \mid Y]]
$$

Where:
- $\mathbb{E}[X]$ is the expected value of $X$
- $\mathbb{E}[X \mid Y]$ is the conditional expectation of $X$ given $Y$

This law expresses that the expected value of $X$ is the expected value of the conditional expectation of $X$ given $Y$, averaged over the distribution of $Y$.

- #statistics, #expectations.iterated-expectations
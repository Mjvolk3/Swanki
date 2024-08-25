## Explain what the mean (or expected value) of a distribution is for continuous random variables (rv's).

For continuous random variables, the mean or expected value is defined as:

$$
\mathbb{E}[X] \triangleq \int_{\mathcal{X}} x p(x) \, dx
$$

Where $\mathbb{E}[X]$ is the expected value of the random variable $X$, $\mathcal{X}$ is the domain of $X$, and $p(x)$ is the probability density function of $X$.

- #mathematics, #probability.mean

## Explain what the mean (or expected value) of a distribution is for discrete random variables (rv's).

For discrete random variables, the mean or expected value is defined as:

$$
\mathbb{E}[X] \triangleq \sum_{x \in \mathcal{X}} x p(x)
$$

Where $\mathbb{E}[X]$ is the expected value of the random variable $X$, $\mathcal{X}$ is the domain of $X$, and $p(x)$ is the probability mass function of $X$. This is meaningful only if the values of $x$ are ordered in some way.

- #mathematics, #probability.mean

## Describe the linearity of expectation with an example involving a random variable $X$ and constants $a$ and $b$.

The linearity of expectation is expressed as:

$$
\mathbb{E}[aX + b] = a \mathbb{E}[X] + b
$$

Where $\mathbb{E}$ denotes expectation, $a$ and $b$ are constants, and $X$ is a random variable.

- #mathematics, #probability.linearity-of-expectation

## Describe the expectation of the sum of $n$ random variables $\{X_i\}$.

For a set of $n$ random variables $\{X_i\}$, the expectation of their sum is:

$$
\mathbb{E}\left[\sum_{i=1}^{n} X_{i}\right] = \sum_{i=1}^{n} \mathbb{E}[X_{i}]
$$

Where $\mathbb{E}$ denotes expectation.

- #mathematics, #probability.sum-of-expectations

## Describe the expectation of the product of $n$ independent random variables $\{X_i\}$.

For $n$ independent random variables $\{X_i\}$, the expectation of their product is given by:

$$
\mathbb{E}\left[\prod_{i=1}^{n} X_{i}\right] = \prod_{i=1}^{n} \mathbb{E}[X_{i}]
$$

Where $\mathbb{E}$ denotes expectation, and the independence of the random variables $X_i$ is crucial.

- #mathematics, #probability.product-of-expectations

## Define the variance of a distribution and provide its mathematical expression.

The variance, denoted by $\sigma^2$, is a measure of the "spread" of a distribution. It is defined as follows:

$$
\mathbb{V}[X] \triangleq \mathbb{E}\left[(X - \mu)^2\right] = \int (x - \mu)^2 p(x) \, dx
$$

This can also be expressed as:

$$
\mathbb{V}[X] = \mathbb{E}[X^2] - \mu^2
$$

Where $\mu$ is the mean (expected value) of $X$.

- #mathematics, #probability.variance
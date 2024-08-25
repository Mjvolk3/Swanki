Here are six Anki-style cards based on the provided chunk of the paper:

## What is the probability density function (pdf) and how is it related to the cumulative distribution function (cdf)?

The pdf is defined as the derivative of the cdf:

$$
p(y) \triangleq \frac{d}{d y} P(y)
$$

The cdf, $P(y)$, is the integral of the pdf from $-\infty$ to $y$.

- #statistics, #probability.cdf-pdf-relationship

## How is the pdf of a Gaussian distribution represented mathematically?

For a Gaussian distribution, the pdf is given by:

$$
\mathcal{N}\left(y \mid \mu, \sigma^{2}\right) \triangleq \frac{1}{\sqrt{2 \pi \sigma^{2}}} e^{-\frac{1}{2 \sigma^{2}}(y-\mu)^{2}}
$$

where $\sqrt{2 \pi \sigma^{2}}$ is the normalization constant.

- #statistics, #probability.gaussian-pdf

## How do you compute the probability of a continuous variable being in a finite interval using the pdf?

Given a pdf $p(y)$, the probability of a continuous variable $Y$ being in a finite interval $(a, b]$ is computed as:

$$
\operatorname{Pr}(a<Y \leq b)=\int_{a}^{b} p(y) d y = P(b) - P(a)
$$

where $P(y)$ is the cdf.

- #statistics, #probability.probability-interval

## What is the expected value (mean) of a distribution and how is it computed using the pdf?

The expected value or mean of a distribution is computed using the pdf as follows:

$$
\mathbb{E}[Y] \triangleq \int_{\mathcal{Y}} y p(y) d y
$$

For a Gaussian distribution, $\mathbb{E}\left[\mathcal{N}\left(\cdot \mid \mu, \sigma^{2}\right)\right] = \mu$.

- #statistics, #probability.expected-value

## How is the variance of a distribution defined and computed using the pdf? What is the relationship between the second moment and the variance?

The variance of a distribution, $\mathbb{V}[Y]$, is defined as:

$$
\mathbb{V}[Y] \triangleq \mathbb{E}\left[(Y-\mu)^{2}\right] = \int (y-\mu)^{2} p(y) d y
$$

It can be reformulated as:

$$
\mathbb{V}[Y] = \mathbb{E}\left[Y^{2}\right] - \mu^{2}
$$

From which we derive:

$$
\mathbb{E}\left[Y^{2}\right] = \sigma^{2} + \mu^{2}
$$

- #statistics, #probability.variance-computation

## What is the standard deviation and how is it related to the variance?

The standard deviation of a distribution is defined as:

$$
\operatorname{std}[Y] \triangleq \sqrt{\mathbb{V}[Y]} = \sigma
$$

The standard deviation is often more interpretable than the variance since it has the same units as $Y$. For a Gaussian distribution, $\operatorname{std}\left[\mathcal{N}\left(\cdot \mid \mu, \sigma^{2}\right)\right] = \sigma$.

- #statistics, #probability.standard-deviation
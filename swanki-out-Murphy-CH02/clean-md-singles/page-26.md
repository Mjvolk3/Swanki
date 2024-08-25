\title{
2.6.2 Probability density function
}

We define the probability density function or pdf as the derivative of the cdf:

$$
p(y) \triangleq \frac{d}{d y} P(y)
$$

The pdf of the Gaussian is given by

$$
\mathcal{N}\left(y \mid \mu, \sigma^{2}\right) \triangleq \frac{1}{\sqrt{2 \pi \sigma^{2}}} e^{-\frac{1}{2 \sigma^{2}}(y-\mu)^{2}}
$$

where $\sqrt{2 \pi \sigma^{2}}$ is the normalization constant needed to ensure the density integrates to 1 (see Exercise 2.12). See Figure 2.2b for a plot.

Given a pdf, we can compute the probability of a continuous variable being in a finite interval as follows:

$$
\operatorname{Pr}(a<Y \leq b)=\int_{a}^{b} p(y) d y=P(b)-P(a)
$$

As the size of the interval gets smaller, we can write

$$
\operatorname{Pr}(y \leq Y \leq y+d y) \approx p(y) d y
$$

Intuitively, this says the probability of $Y$ being in a small interval around $y$ is the density at $y$ times the width of the interval. One important consequence of the above result is that the pdf at a point can be larger than 1 . For example, $\mathcal{N}(0 \mid 0,0.1)=3.99$.

We can use the pdf to compute the mean, or expected value, of the distribution:

$$
\mathbb{E}[Y] \triangleq \int_{\mathcal{Y}} y p(y) d y
$$

For a Gaussian, we have the familiar result that $\mathbb{E}\left[\mathcal{N}\left(\cdot \mid \mu, \sigma^{2}\right)\right]=\mu$. (Note, however, that for some distributions, this integral is not finite, so the mean is not defined.)

We can also use the pdf to compute the variance of a distribution. This is a measure of the "spread", and is often denoted by $\sigma^{2}$. The variance is defined as follows:

$$
\begin{aligned}
\mathbb{V}[Y] & \triangleq \mathbb{E}\left[(Y-\mu)^{2}\right]=\int(y-\mu)^{2} p(y) d y \\
& =\int y^{2} p(y) d y+\mu^{2} \int p(y) d y-2 \mu \int y p(y) d y=\mathbb{E}\left[Y^{2}\right]-\mu^{2}
\end{aligned}
$$

from which we derive the useful result

$$
\mathbb{E}\left[Y^{2}\right]=\sigma^{2}+\mu^{2}
$$

The standard deviation is defined as

$$
\operatorname{std}[Y] \triangleq \sqrt{\mathbb{V}[Y]}=\sigma
$$

(The standard deviation can be more intepretable than the variance since it has the same units as $Y$ itself.) For a Gaussian, we have the familiar result that std $\left[\mathcal{N}\left(\cdot \mid \mu, \sigma^{2}\right)\right]=\sigma$.

Draft of "Probabilistic Machine Learning: An Introduction". August 8, 2022
## Define the cumulative distribution function (cdf) of a continuous random variable $Y$.

The cumulative distribution function (cdf) of a continuous random variable $Y$ is defined as:

$$
P(y) \triangleq \operatorname{Pr}(Y \leq y)
$$

This function is useful for computing the probability that $Y$ falls within any specific interval $(a, b]$:

$$
\operatorname{Pr}(a<Y \leq b)=P(b)-P(a)
$$

Cdf's are monotonically non-decreasing functions, meaning they either increase or remain constant as $y$ increases.

- #probability, #statistics.cdf

## What is the cdf of the Gaussian distribution?

The cdf of the Gaussian distribution $\Phi(y; \mu, \sigma^2)$ is defined by:

$$
\Phi\left(y ; \mu, \sigma^{2}\right) \triangleq \int_{-\infty}^{y} \mathcal{N}\left(z \mid \mu, \sigma^{2}\right) d z
$$

An alternative implementation uses the error function, $\operatorname{erf}(u)$:

$$
\Phi\left(y ; \mu, \sigma^{2}\right) = \frac{1}{2} \left[ 1 + \operatorname{erf} \left( \frac{y - \mu}{\sigma \sqrt{2}} \right) \right]
$$

where 

$$
\operatorname{erf}(u) = \frac{2}{\sqrt{\pi}} \int_{0}^{u} e^{-t^{2}} d t
$$

- #probability, #statistics.gaussian

## Describe the error function $\operatorname{erf}(u)$.

The error function $\operatorname{erf}(u)$ is defined as:

$$
\operatorname{erf}(u) \triangleq \frac{2}{\sqrt{\pi}} \int_{0}^{u} e^{-t^{2}} d t
$$

It is used in various statistical computations, including the cdf of the Gaussian distribution:

$$
\Phi\left(y ; \mu, \sigma^{2}\right) = \frac{1}{2} \left[ 1 + \operatorname{erf} \left( \frac{y - \mu}{\sigma \sqrt{2}} \right) \right]
$$

The error function quantifies the probability that a random variable with a normal distribution falls within a certain range.

- #error-function, #statistics.gaussian

## What is the $q^{th}$ quantile of $P$, and what is it used for?

If $P$ is the cdf of $Y$, then $P^{-1}(q)$ is the value $y_q$ such that:

$$
p\left(Y \leq y_{q}\right) = q
$$

This is called the $q^{\prime}$-th quantile of $P$. Quantiles are used to divide the probability distribution into intervals with equal probabilities. For example, the median of the distribution is $P^{-1}(0.5)$, which has half of the probability mass on the left and half on the right.

- #probability, #statistics.quantiles

## How is the central interval for the normal distribution defined?

For a Gaussian distribution $\mathcal{N}(0,1)$, the central interval containing $1-\alpha$ of the mass is given by:

$$
\left(\Phi^{-1}(\alpha / 2), \Phi^{-1}(1-\alpha / 2)\right)
$$

For example, setting $\alpha = 0.05$ gives:

$$
\left(\Phi^{-1}(0.025), \Phi^{-1}(0.975)\right) = (-1.96, 1.96)
$$

This interval contains $95\%$ of the probability mass.

- #statistics, #probability.central-interval

## What is the $95\%$ interval for a Gaussian distribution $\mathcal{N}(\mu, \sigma^2)$?

For a Gaussian distribution $\mathcal{N}\left(\mu, \sigma^{2}\right)$, the $95\%$ central interval is:

$$
(\mu - 1.96 \sigma, \mu + 1.96 \sigma)
$$

This interval contains $95\%$ of the probability mass and is often approximated as $\mu \pm 2 \sigma$.

- #statistics, #probability.gaussian-interval
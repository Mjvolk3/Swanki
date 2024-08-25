## What is the inverse cumulative distribution function (cdf) also known as?

The inverse cumulative distribution function (cdf) is also known as the percent point function (ppf) or the quantile function.

- #statistics, #cdf.inverse-quantile-function


## How is the $q$th quantile of the cumulative distribution function (cdf) $P$ defined?

If $P$ is the cdf of $X$, then the $q$th quantile of $P$ is defined as $x_q$ such that:

$$
\operatorname{Pr}\left(X \leq x_q\right) = q
$$

where $P^{-1}(q) = x_q$ represents the quantile function.

- #statistics, #quantile-quantile-function


## What is the median of a distribution in terms of its cumulative distribution function (cdf)?

The median of the distribution is the value $P^{-1}(0.5)$, where half of the distribution's probability mass lies to the left and half to the right.

- #statistics, #quantiles.median


## What is the central interval that contains 95% of the mass for a standard Gaussian distribution $\mathcal{N}(0,1)$?

For a standard Gaussian distribution $\mathcal{N}(0,1)$, the central interval containing 95% of the mass is:

$$
\left(\Phi^{-1}(0.025), \Phi^{-1}(0.975)\right) = (-1.96, 1.96)
$$

where $\Phi$ is the cdf of the Gaussian distribution and $\Phi^{-1}$ is the inverse cdf.

- #statistics, #gaussian.central-interval


## How do you express the 95% interval for a Gaussian distribution $\mathcal{N}(\mu, \sigma^2)$?

For a Gaussian distribution $\mathcal{N}(\mu, \sigma^2)$, the 95% interval is given by:

$$
(\mu - 1.96 \sigma, \mu + 1.96 \sigma)
$$

This is often approximated as $\mu \pm 2\sigma$.

- #statistics, #gaussian.confidence-interval


## How is the marginal distribution of a random variable $X$ derived from the joint distribution of $X$ and $Y$?

The marginal distribution of $X$ is derived from the joint distribution of $X$ and $Y$ by summing over all possible states of $Y$:

$$
p(X=x) = \sum_{y} p(X=x, Y=y)
$$

This is sometimes called the sum rule or the rule of total probability.

- #probability, #joint-distribution.marginal-distribution
\title{
2.6 Univariate Gaussian (normal) distribution
}

The most widely used distribution of real-valued random variables $y \in \mathbb{R}$ is the Gaussian distribution, also called the normal distribution (see Section 2.6.4 for a discussion of these names).

\subsection*{2.6.1 Cumulative distribution function}

We define the cumulative distribution function or cdf of a continuous random variable $Y$ as follows:

$$
P(y) \triangleq \operatorname{Pr}(Y \leq y)
$$

(Note that we use a capital $P$ to represent the cdf.) Using this, we can compute the probability of being in any interval as follows:

$$
\operatorname{Pr}(a<Y \leq b)=P(b)-P(a)
$$

Cdf's are monotonically non-decreasing functions.

The cdf of the Gaussian is defined by

$$
\Phi\left(y ; \mu, \sigma^{2}\right) \triangleq \int_{-\infty}^{y} \mathcal{N}\left(z \mid \mu, \sigma^{2}\right) d z
$$

See Figure 2.2a for a plot. Note that the cdf of the Gaussian is often implemented using $\Phi\left(y ; \mu, \sigma^{2}\right)=$ $\frac{1}{2}[1+\operatorname{erf}(z / \sqrt{2})]$, where $z=(y-\mu) / \sigma$ and $\operatorname{erf}(u)$ is the error function, defined as

$$
\operatorname{erf}(u) \triangleq \frac{2}{\sqrt{\pi}} \int_{0}^{u} e^{-t^{2}} d t
$$

The parameter $\mu$ encodes the mean of the distribution, which is the same as the mode, since the distribution is unimodal. The parameter $\sigma^{2}$ encodes the variance. (Sometimes we talk about the precision of a Gaussian, which is the inverse variance, denoted $\lambda=1 / \sigma^{2}$.) When $\mu=0$ and $\sigma=1$, the Gaussian is called the standard normal distribution.

If $P$ is the cdf of $Y$, then $P^{-1}(q)$ is the value $y_{q}$ such that $p\left(Y \leq y_{q}\right)=q$; this is called the $q^{\prime}$ 'th quantile of $P$. The value $P^{-1}(0.5)$ is the median of the distribution, with half of the probability mass on the left, and half on the right. The values $P^{-1}(0.25)$ and $P^{-1}(0.75)$ are the lower and upper quartiles.

For example, let $\Phi$ be the cdf of the Gaussian distribution $\mathcal{N}(0,1)$, and $\Phi^{-1}$ be the inverse cdf (also known as the probit function). Then points to the left of $\Phi^{-1}(\alpha / 2)$ contain $\alpha / 2$ of the probability mass, as illustrated in Figure 2.2b. By symmetry, points to the right of $\Phi^{-1}(1-\alpha / 2)$ also contain $\alpha / 2$ of the mass. Hence the central interval $\left(\Phi^{-1}(\alpha / 2), \Phi^{-1}(1-\alpha / 2)\right)$ contains $1-\alpha$ of the mass. If we set $\alpha=0.05$, the central $95 \%$ interval is covered by the range

$$
\left(\Phi^{-1}(0.025), \Phi^{-1}(0.975)\right)=(-1.96,1.96)
$$

If the distribution is $\mathcal{N}\left(\mu, \sigma^{2}\right)$, then the $95 \%$ interval becomes $(\mu-1.96 \sigma, \mu+1.96 \sigma)$. This is often approximated by writing $\mu \pm 2 \sigma$.

Author: Kevin P. Murphy. (C) MIT Press. CC-BY-NC-ND license
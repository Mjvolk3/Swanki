## How is $\mu_k$ derived from the maximum likelihood estimation given its constraint and the Lagrange multiplier in the optimization process?

To find $\mu_k$, we start with the expression $$
\frac{\partial}{\partial \mu_k} \left( \text{Expression involving } \mu_k \right) = 0
$$
yielding $$
\mu_k = -\frac{m_k}{\lambda}
$$
Setting this equation under the constraint $\sum_k \mu_k = 1$ and solving for $\lambda$ gives $\lambda = -N$. Thus we derive $$
\mu_k^{\text{ML}} = \frac{m_k}{N}
$$
This represents the fraction of the $N$ observations for which $x_k = 1$.

- #statistical-methods, #parameter-estimation.maximum-likelihood

## Define the multinomial distribution as it is conditioned on the parameter vector ${\boldsymbol{\mu}}$ and the total number $N$ of observations.

The conditional joint distribution of $(m_1, \dots, m_K)$ given ${\boldsymbol{\mu}}$ and $N$ is expressed as $$
\operatorname{Mult}(m_1, m_2, \dots, m_K \mid {\boldsymbol{\mu}}, N) = \binom{N}{m_1 m_2 \ldots m_K} \prod_{k=1}^K \mu_k^{m_k}
$$
This represents the probability of observing the specific counts $m_1, \dots, m_K$ across $K$ categories, given total observations $N$ and probabilities $\mu_k$ for each category.

- #probability-distributions, #statistical-methods.multinomial-distribution

## How is the normalization coefficient for the multinomial distribution computed?

The normalization coefficient for the multinomial distribution is given by the multinomial coefficient $$
\binom{N}{m_{1} m_{2} \ldots m_{K}} = \frac{N!}{m_{1}! m_{2}!\ldots m_{K}!}
$$
which represents the number of ways to partition $N$ items into $K$ groups where the $k$-th group has exactly $m_k$ items.

- #combinatorics, #probability-distributions.normalization-coefficients

## Explain the form of the Gaussian distribution for a single variable $x$.

The Gaussian distribution for a variable $x$, with mean $\mu$ and variance $\sigma^2$, is described by the probability density function $$
\mathcal{N}(x \mid \mu, \sigma^2) = \frac{1}{\sqrt{2\pi \sigma^2}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)
$$
This represents how $x$ is distributed around the mean $\mu$, with spread determined by $\sigma^2$.

- #probability-distributions, #statistics.gaussian-distribution

## Describe the form and components of the multivariate Gaussian distribution for a $D$-dimensional vector $\mathbf{x}$.

The multivariate Gaussian distribution for a $D$-dimensional vector $\mathbf{x}$, with mean vector $\boldsymbol{\mu}$ and covariance matrix $\boldsymbol{\Sigma}$, is given by $$
\mathcal{N}(\mathbf{x} \mid {\boldsymbol{\mu}}, {\boldsymbol{\Sigma}}) = \frac{1}{(2\pi)^{D/2} |\boldsymbol{\Sigma}|^{1/2}} \exp \left(-\frac{1}{2} (\mathbf{x}-{\boldsymbol{\mu}})^{\text{T}} {\boldsymbol{\Sigma}}^{-1} (\mathbf{x}-{\boldsymbol{\mu}})\right)
$$
Here, $|\boldsymbol{\Sigma}|$ is the determinant of the covariance matrix $\boldsymbol{\Sigma}$, affecting the distribution's spread in the multivariate space.

- #probability-distributions, #statistics.multivariate-gaussian-distribution
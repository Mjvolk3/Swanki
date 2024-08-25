## What are the mean and variance of a normalized variable $x$ assumed in the paper?

The mean $\mathbb{E}[x]$ and variance $\operatorname{var}[x]$ of the variable $x$ are given as:
$$
\mathbb{E}[x] = \mu, \quad \operatorname{var}[x] = \mu(1-\mu)
$$

These values characterize $x$ as a Bernoulli random variable, where $\mu$ is the probability of $x = 1$. 

- #statistics, #bernoulli-distribution, #mean-variance

## How is the likelihood function $p(\mathcal{D} \mid \mu)$ for the dataset $\mathcal{D}$ defined in terms of $\mu$?

The likelihood function, assuming independence of observations, is given by:
$$
p(\mathcal{D} \mid \mu) = \prod_{n=1}^{N} p(x_n \mid \mu) = \prod_{n=1}^{N} \mu^{x_n}(1-\mu)^{1-x_n}
$$
This expression facilitates the estimation of $\mu$ by linking it directly with each observation's probability under the Bernoulli distribution.

- #statistics, #likelihood-function, #bernoulli-distribution

## How can the log likelihood function of the Bernoulli distribution be expressed in terms of data observations $\{x_n\}$?

The log likelihood function is expressed as:
$$
\ln p(\mathcal{D} \mid \mu) = \sum_{n=1}^{N} \ln p(x_n \mid \mu) = \sum_{n=1}^{N} (x_n \ln \mu + (1-x_n) \ln (1-\mu))
$$
This rearrangement shows the dependency of the log likelihood on the data solely through the sum $\sum_n x_n$, which is a sufficient statistic for this model. 

- #statistics, #log-likelihood, #bernoulli-distribution

## Derive the formula for the Maximum Likelihood Estimator $\mu_{\mathrm{ML}}$ of $\mu$ from the log likelihood function.

Starting from the derivative of $\ln p(\mathcal{D} \mid \mu)$ set to zero:
$$
\frac{d}{d\mu} \left(\sum_{n=1}^{N} (x_n \ln \mu + (1-x_n) \ln (1-\mu))\right) = 0
$$
Solving this equation yields:
$$
\mu_{\mathrm{ML}} = \frac{1}{N} \sum_{n=1}^{N} x_n
$$
indicating that $\mu_{\mathrm{ML}}$ is the sample mean, i.e., the proportion of occurrences of $x=1$ in the dataset.

- #statistics, #maximum-likelihood-estimation, #bernoulli-distribution

## Explain and derive the form of the binomial distribution $\operatorname{Bin}(m \mid N, \mu)$ from given assumptions.

Given that the variable $x$ counts the number of observations $x=1$ in $N$ trials, the binomial probability can be expressed as:
$$
\operatorname{Bin}(m \mid N, \mu) = \binom{N}{m} \mu^m (1-\mu)^{N-m}
$$
Here, $\binom{N}{m}$ represents the number of ways to choose $m$ successes (heads) in $N$ trials, and $\mu^m(1-\mu)^{N-m}$ is the probability of any specific arrangement of those $m$ successes.

- #statistics, #binomial-distribution, #probability-distributions
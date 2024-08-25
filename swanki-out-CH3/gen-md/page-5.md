## Explain the representation and normalization condition of a vector $\mathbf{x}$ in a multinomial setting

For a given state in a sample space of $K$ possible states, $\mathbf{x}$ is represented as a binary vector where exactly one element is 1 and all other elements are 0. In the case of $x_3=1$, $\mathbf{x}$ is $$\mathbf{x}=(0,0,1,0,0,0)^{\mathrm{T}}.$$ This representation ensures $\sum_{k=1}^{K} x_k = 1$, implying that only one state can occur at a time in any given trial.

- #probability-distributions, #multinomial-distribution, #vector-normalization

## Describe the probability mass function of $\mathbf{x}$ under the multinomial distribution parameters $\boldsymbol{\mu}$

The probability mass function (PMF) for $\mathbf{x}$, given the parameter vector $\boldsymbol{\mu}$, is defined as $$p(\mathbf{x} \mid \boldsymbol{\mu}) = \prod_{k=1}^{K} \mu_k^{x_k},$$ where $\mu_k$ is the probability of the $k$-th state occurring and is subject to the constraints $\mu_k \geq 0$ and $\sum_{k=1}^{K} \mu_k = 1$. This formula represents a generalization of the Bernoulli distribution to more than two outcomes.

- #probability-distributions, #multinomial-distribution, #pmf

## How is the expectation $\mathbb{E}[\mathbf{x} \mid \boldsymbol{\mu}]$ computed under the multinomial model?

The expected value of the vector $\mathbf{x}$, given the distribution parameters $\boldsymbol{\mu}$, is calculated as $$\mathbb{E}[\mathbf{x} \mid \boldsymbol{\mu}] = \sum_{\mathbf{x}} p(\mathbf{x} \mid \boldsymbol{\mu}) \mathbf{x}.$$ Given the properties of the multinomial distribution, this simplifies directly to $\boldsymbol{\mu}$. This result aligns with intuition since $\mu_k$ is the probability of $x_k = 1$ occurring.

- #probability-distributions, #multinomial-distribution, #expected-value

## Define the likelihood function for a dataset $\mathcal{D} = \{\mathbf{x}_1, \ldots, \mathbf{x}_N\}$ under the multinomial model

The likelihood function for a dataset $\mathcal{D}$ consisting of $N$ independent observations under the multinomial model parameters $\boldsymbol{\mu}$ is $$p(\mathcal{D} \mid \boldsymbol{\mu}) = \prod_{n=1}^{N} \prod_{k=1}^{K} \mu_k^{x_{nk}} = \prod_{k=1}^{K} \mu_k^{m_k},$$ where $m_k = \sum_{n=1}^{N} x_{nk}$ represents the total number of times the $k$-th state occurred in all $N$ observations and is known as a sufficient statistic.

- #probability-distributions, #multinomial-distribution, #likelihood-function

## How is the maximum likelihood estimate of $\boldsymbol{\mu}$ derived in the context of the multinomial distribution?

To find the maximum likelihood estimate of $\boldsymbol{\mu}$, the objective is to maximize $$\ln p(\mathcal{D} \mid \boldsymbol{\mu}) = \sum_{k=1}^{K} m_k \ln \mu_k$$ subject to the constraint that $\sum_{k=1}^{K} \mu_k = 1$. This is typically accomplished using a Lagrange multiplier $\lambda$ to incorporate the constraint, leading to the optimization of $$\sum_{k=1}^{K} m_k \ln \mu_k + \lambda \left(\sum_{k=1}^{K} \mu_k - 1\right).$$ 

- #probability-distributions, #multinomial-distribution, #mle-maximum-likelihood-estimation
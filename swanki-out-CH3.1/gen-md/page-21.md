## Derive the maximum likelihood estimate for the covariance matrix $\boldsymbol{\Sigma}_{\mathrm{ML}}$

Given the equation for estimating the covariance matrix from a set of data points provided in the text,

$$
\boldsymbol{\Sigma}_{\mathrm{ML}}=\frac{1}{N} \sum_{n=1}^{N}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{\mathrm{ML}}\right)\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{\mathrm{ML}}\right)^{\mathrm{T}}
$$

where $\mathbf{x}_{n}$ are data points and $\boldsymbol{\mu}_{\mathrm{ML}}$ is the mean estimated maximizing the likelihood simultaneously with $\boldsymbol{\Sigma}$. This equation shows us that $\boldsymbol{\Sigma}_{\mathrm{ML}}$ accounts for deviations of each data point from the mean, and then averaging these discrepancies across all data points.

- #statistics, #maximum-likelihood, #covariance-matrix

## Explain why $\boldsymbol{\Sigma}_{\mathrm{ML}}$ is evaluated after computing $\boldsymbol{\mu}_{\mathrm{ML}}$

The maximum likelihood estimation process of $\boldsymbol{\mu}_{\mathrm{ML}}$ and $\boldsymbol{\Sigma}_{\mathrm{ML}}$ is a joint maximization. However, it is crucial to first compute $\boldsymbol{\mu}_{\mathrm{ML}}$ because:

$$
\boldsymbol{\Sigma}_{\mathrm{ML}}=\frac{1}{N} \sum_{n=1}^{N}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{\mathrm{ML}}\right)\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{\mathrm{ML}}\right)^{\mathrm{T}}
$$

involves $\boldsymbol{\mu}_{\mathrm{ML}}$ in its calculation. Hence, $\boldsymbol{\mu}_{\mathrm{ML}}$ being independent of $\boldsymbol{\Sigma}_{\mathrm{ML}}$ allows for its prior estimation simplifying the sequential calculation in this maximization approach.

- #statistics, #maximum-likelihood, #calculation-order

## Discuss the biased nature of $\boldsymbol{\Sigma}_{\mathrm{ML}}$ and how it is corrected

From the text, it is revealed that the expectation of the maximum likelihood estimate for the covariance $\boldsymbol{\Sigma}_{\mathrm{ML}}$ underestimates the true covariance $\boldsymbol{\Sigma}$ as indicated by:

$$
\mathbb{E}\left[\boldsymbol{\Sigma}_{\mathrm{ML}}\right] = \frac{N-1}{N} \boldsymbol{\Sigma}
$$

This bias is corrected through defining the estimator $\widetilde{\boldsymbol{\Sigma}}$:

$$
\widetilde{\boldsymbol{\Sigma}}=\frac{1}{N-1} \sum_{n=1}^{N}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{\mathrm{ML}}\right)\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{\mathrm{ML}}\right)^{\mathrm{T}}
$$

ensuring that $\mathbb{E}[\widetilde{\boldsymbol{\Sigma}}] = \boldsymbol{\Sigma}$, providing a correctly adjusted and unbiased estimation of the true covariance.

- #statistics, #bias-correction, #covariance-estimation

## Highlight the differences between batch and sequential methods in maximum likelihood estimation

The discussion in the text outlines the contrast between batch methods, which consider all data points at once, and sequential methods, which process data points individually. The key advantage of sequential methods is their applicability in situations where:

- Online computation is necessary.
- Handling large data sets, where batch processing of all data would be computationally infeasible.

Sequential methods thus provide flexibility and scalability, making them suitable for real-time applications and systems constrained by memory or processing power.

- #statistics, #maximum-likelihood, #sequential-methods

## Analyze the impact of increasing data points on $\boldsymbol{\mu}_{\mathrm{ML}}$'s estimation in sequential methods

Considering the result for the maximum likelihood estimator of the mean $\boldsymbol{\mu}_{\mathrm{ML}}$, denoted $\boldsymbol{\mu}_{\mathrm{ML}}^{(N)}$ for $N$ observations,

$$
\boldsymbol{\mu}_{\mathrm{ML}}^{(N)} = \frac{1}{N} \sum_{n=1}^{N} \mathbf{x}_n
$$

As more data points are considered ($N$ increases), the estimator becomes increasingly accurate assuming the additional data are representative. In sequential methods, this means that each new data point refines the estimate, ideally leading to convergence towards the true parameter value as $N$ approaches infinity.

- #statistics, #maximum-likelihood, #data-scaling
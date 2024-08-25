## What is the formula for updating the maximum likelihood estimate of the mean, $\boldsymbol{\mu}_{\mathrm{ML}}$, after observing an additional data point $\mathbf{x}_N$?

The updated maximum likelihood estimate $\boldsymbol{\mu}_{\mathrm{ML}}^{(N)}$ after observing the $N^{th}$ data point $\mathbf{x}_N$ is given by:
$$
\boldsymbol{\mu}_{\mathrm{ML}}^{(N)} = \boldsymbol{\mu}_{\mathrm{ML}}^{(N-1)} + \frac{1}{N}(\mathbf{x}_N - \boldsymbol{\mu}_{\mathrm{ML}}^{(N-1)})
$$

- #statistics.mathematical-statistics, #probability.maximum-likelihood-estimation

## How does the contribution of each data point to the mean, $\boldsymbol{\mu}_{\mathrm{ML}}$, change as more data points are observed?

As more data points ($N$) are observed, the contribution of each individual data point to the maximum likelihood estimate of the mean, $\boldsymbol{\mu}_{\mathrm{ML}}$, decreases. This is because each additional data point affects the mean by a factor of $\frac{1}{N}$. Hence, earlier observations have a diminishing influence as the sample size grows.

- #statistics.mathematical-statistics, #probability.convergence-properties

## Contrast the performance of a single Gaussian model versus a mixture of Gaussians in modeling the Old Faithful data set based on the given descriptions.

The single Gaussian model fails to adequately capture the structure of the Old Faithful data set as it places much of its probability mass in the central region between two prominent clumps where data are sparse. In contrast, a mixture of two Gaussians provides a superior representation by accurately modeling the two distinct clumps observed in the data.

- #statistics.data-modeling, #probability.distribution-analysis

## What quantitative impact does the final data point $\mathbf{x}_N$ have on the updated mean $\boldsymbol{\mu}_{\mathrm{ML}}^{(N)}$?

The quantitative impact of the final data point $\mathbf{x}_N$ on the updated mean $\boldsymbol{\mu}_{\mathrm{ML}}^{(N)}$ is directly proportionate to $\frac{1}{N}$, revealing that as the number of data points increases, each new data point exerts a progressively smaller influence on the updated mean.

- #statistics.mathematical-statistics, #data-analysis.data-point-impact

## Why does a simple Gaussian distribution struggle to describe data with multiple subgroups such as in the Old Faithful data set?

A simple Gaussian distribution is characterized by a single peak and symmetric decay, which makes it intrinsically unsuitable for accurately describing datasets with multiple distinct subgroups or clumps. This limitation leads to significant errors in probability estimation for data sets like Old Faithful that exhibit clearly separated groupings.

- #statistics.data-modeling, #probability.distribution-limitations
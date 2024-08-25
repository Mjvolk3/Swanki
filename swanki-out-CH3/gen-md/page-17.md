## What are the expressions for the mean and covariance of the marginal distribution $\mathbf{x}_a$ in a partitioned Gaussian distribution?

The mean and covariance of the marginal distribution $\mathbf{x}_a$ are given by:
$$
\begin{aligned}
\mathbb{E}\left[\mathbf{x}_{a}\right] & =\boldsymbol{\mu}_{a} \\
\operatorname{cov}\left[\mathbf{x}_{a}\right] & =\boldsymbol{\Sigma}_{a a}
\end{aligned}
$$

- #statistics.gaussian-distribution, #mathematics.expectation-and-covariance

## How can you express the conditional distribution $p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right)$ in terms of its mean and covariance for a partitioned Gaussian?

The conditional distribution $p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right)$ is expressed as:
$$
p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right) = \mathcal{N}\left(\mathbf{x}_{a} \mid \boldsymbol{\mu}_{a \mid b}, \boldsymbol{\Lambda}_{a a}^{-1}\right)
$$
where $\boldsymbol{\mu}_{a \mid b}$ is defined as:
$$
\boldsymbol{\mu}_{a \mid b} = \boldsymbol{\mu}_{a}-\boldsymbol{\Lambda}_{a a}^{-1} \boldsymbol{\Lambda}_{a b}\left(\mathbf{x}_{b}-\boldsymbol{\mu}_{b}\right)
$$

- #statistics.gaussian-distribution, #mathematics.conditional-distribution

## Define $\boldsymbol{\Lambda}$ and its role in a Gaussian distribution.

In a Gaussian distribution, $\boldsymbol{\Lambda}$ is defined as the inverse of the covariance matrix $\boldsymbol{\Sigma}$:
$$
\boldsymbol{\Lambda} \equiv \boldsymbol{\Sigma}^{-1}
$$
This matrix, also called the precision matrix, plays a crucial role in defining the relationships and conditional independencies between the variables of a multivariate Gaussian distribution.

- #statistics.gaussian-distribution, #mathematics.precision-matrix

## In the context of Gaussian distributions, how does partitioning the covariance $\boldsymbol{\Sigma}$ affect the expressions for conditional distributions?

When partitioning the covariance matrix $\boldsymbol{\Sigma}$ as shown,
$$
\boldsymbol{\Sigma}=\left(\begin{array}{ll}
\boldsymbol{\Sigma}_{a a} & \boldsymbol{\Sigma}_{a b} \\
\boldsymbol{\Sigma}_{b a} & \boldsymbol{\Sigma}_{b b}
\end{array}\right)
$$
the conditional distribution expressions become simpler using the partitioned precision matrix $\boldsymbol{\Lambda}$. This matrix provides a straightforward way to derive the conditional means and covariances as it directly incorporates the dependencies between partitioned variables.

- #statistics.matrix-partitioning, #mathematics.gaussian-distribution

## Discuss the relevance and applications of linear-Gaussian models in real-world scenarios.

Linear-Gaussian models, where the mean of the conditional distribution is a linear function of another variable and the covariance is independent of this variable, are fundamental in many statistical learning scenarios. Applications include Kalman filters for time series analysis and control systems, and general state-space models in econometrics and finance. These models facilitate analytically tractable solutions and efficient computation, pivotal in real-world data analytics and predictive modeling.

- #statistics.linear-gaussian-model, #applications.control-systems-and-finance
## How can we express the exponent in a Gaussian distribution as a quadratic form?

The exponent in a Gaussian distribution, $\mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}, \boldsymbol{\Sigma})$, can be written as a quadratic form:

$$
-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu}) = -\frac{1}{2} \mathbf{x}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \mathbf{x} + \mathbf{x}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \boldsymbol{\mu} + \text{const}
$$

where "const" denotes terms independent of $\mathbf{x}$.

- #mathematics.distribution-theory, #gaussian-distribution, #quadratic-forms

## How do we identify the inverse covariance matrix from a quadratic form?

Given a general quadratic form in the exponent of a Gaussian distribution:

$$
-\frac{1}{2} \mathbf{x}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \mathbf{x} + \mathbf{x}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \boldsymbol{\mu} + \text{const}
$$

we can equate the matrix of coefficients of the second-order term in $\mathbf{x}$ to $\boldsymbol{\Sigma}^{-1}$, the inverse covariance matrix.

- #probability.distributions, #gaussian-distribution, #covariance-matrix

## How is the conditional mean $\boldsymbol{\mu}_{a \mid b}$ derived from the quadratic form of a conditional Gaussian distribution?

For the conditional Gaussian distribution $p(\mathbf{x}_a \mid \mathbf{x}_b)$, after extracting terms linear in $\mathbf{x}_a$, we obtain:

$$
\mathbf{x}_a^{\mathrm{T}}\left\{\boldsymbol{\Lambda}_{aa} \boldsymbol{\mu}_a - \boldsymbol{\Lambda}_{ab}(\mathbf{x}_b - \boldsymbol{\mu}_b)\right\}
$$

From which we derive that:

$$
\boldsymbol{\mu}_{a \mid b} = \boldsymbol{\mu}_a - \boldsymbol{\Lambda}_{aa}^{-1} \boldsymbol{\Lambda}_{ab}(\mathbf{x}_b - \boldsymbol{\mu}_b)
$$

- #statistics.conditional-probability, #gaussian-distribution, #mean-estimation

## What does $\boldsymbol{\Sigma}_{a \mid b}=\boldsymbol{\Lambda}_{aa}^{-1}$ represent in the context of Gaussian distributions?

In the conditional Gaussian distribution $p(\mathbf{x}_a \mid \mathbf{x}_b)$, $\boldsymbol{\Sigma}_{a \mid b}$ represents the covariance of $\mathbf{x}_a$ given $\mathbf{x}_b$, derived from the quadratic term:

$$
-\frac{1}{2} \mathbf{x}_a^{\mathrm{T}} \boldsymbol{\Lambda}_{aa} \mathbf{x}_a
$$

indicating that $\boldsymbol{\Sigma}_{a \mid b}=\boldsymbol{\Lambda}_{aa}^{-1}$ is the inverse of $\boldsymbol{\Lambda}_{aa}$, or the precision matrix.

- #statistics.conditional-probability, #covariance-matrix, #gaussian-distribution

## How is the inverse of a partitioned matrix relevant in deriving properties of conditional Gaussian distributions?

The inverse of a partitioned matrix is given by:

$$
\left(\begin{array}{cc}
\mathbf{A} & \mathbf{B} \\
\mathbf{C} & \mathbf{D}
\end{array}\right)^{-1} = \left(\begin{array}{cc}
\mathbf{M} & -\mathbf{M B D}^{-1} \\
-\mathbf{D}^{-1} \mathbf{C M} & \mathbf{D}^{-1} + \mathbf{D}^{-1} \mathbf{C M B D}^{-1}
\end{array}\right)
$$

where $\mathbf{M} = (\mathbf{A} - \mathbf{B D}^{-1} \mathbf{C})^{-1}$. This formula is crucial for computing the conditional means and covariances in multivariate Gaussian distributions when considering conditional dependencies.

- #mathematics.matrix-algebra, #gaussian-distribution, #covariance-matrix
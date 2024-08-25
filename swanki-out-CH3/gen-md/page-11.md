## Explain the significance of the integral transformation used in the Gaussian density integration process and derive the expression for the covariance matrix.

The transformation used in the integration process converts the Gaussian density integral into a sum of integrals over the individual orthogonal components $y_i$, where $y_j = \mathbf{u}_j^\mathrm{T} \mathbf{z}$. This allows the integration to be treated independently for each dimension. Here's the derivation showing how the initial integral expression evaluates to $ \boldsymbol{\Sigma} $:

$$
\begin{aligned}
\int \exp\left\{-\frac{1}{2} \mathbf{z}^\mathrm{T} \boldsymbol{\Sigma}^{-1} \mathbf{z}\right\} \mathbf{z} \mathbf{z}^\mathrm{T} \mathrm{d} \mathbf{z}
&= \sum_{i=1}^{D} \mathbf{u}_{i} \mathbf{u}_{i}^\mathrm{T} \lambda_{i} \\
&= \boldsymbol{\Sigma}
\end{aligned}
$$
This step utilizes eigen-decomposition of $\boldsymbol{\Sigma}$, revealing that the integrals of non-diagonal terms vanish by symmetry and only diagonal terms contribute, each weighed by their corresponding eigenvalues.

- #mathematics, #gaussian-distribution.covariance-matrix

## Describe the eigenvector equation (3.28) and its relevance in simplifying the Gaussian density integral.

The eigenvector equation typically takes the form $\mathbf{A} \mathbf{v} = \lambda \mathbf{v}$, where $\mathbf{A}$ is a matrix (here $\boldsymbol{\Sigma}$), $\mathbf{v}$ is an eigenvector, and $\lambda$ is the corresponding eigenvalue. In the Gaussian density integration:

$$
\frac{1}{(2 \pi)^{D / 2}} \frac{1}{|\boldsymbol{\Sigma}|^{1 / 2}} \int \exp \left\{-\frac{1}{2} \mathbf{z}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \mathbf{z}\right\} \mathbf{zz}^{\mathrm{T}} \mathrm{d} \mathbf{z} = \boldsymbol{\Sigma}
$$

use of the eigenvector equation allows the matrix $\boldsymbol{\Sigma}$ to be expressed as a sum of its eigenvectors scaled by their eigenvalues, simplifying the integral significantly.

- #linear-algebra, #eigenvalues-eigenvectors

## Clarify how the covariance matrix $\boldsymbol{\Sigma}$ is derived for a multivariate Gaussian distribution.

In the context of the Gaussian distribution, $\operatorname{cov}[\mathbf{x}] = \boldsymbol{Sigma}$. This expression is obtained from:

$$
\mathbb{E}\left[(\mathbf{x}-\mathbb{E}[\mathbf{x}])(\mathbf{x}-\mathbb{E}[\mathbf{x}])^\mathrm{T}\right]
$$

Since $\mathbb{E}[\mathbf{x}] = \boldsymbol{\mu}$, subtracting $\boldsymbol{\mu}$ from $\mathbf{x}$ allows for focusing on the variance of the distribution around its mean. This measure of spread, represented by $\boldsymbol{\Sigma}$, directly quantifies the covariance among all dimensions.

- #statistics, #gaussian-distribution.covariance-analysis

## Discuss the computational implications of the number of parameters in a Gaussian distribution's covariance matrix.

The general covariance matrix $\boldsymbol{\Sigma}$ for a Gaussian distribution in $D$ dimensions contains $D(D + 1)/2$ independent parameters due to its symmetric nature. Together with $D$ parameters from the mean vector $\boldsymbol{\mu}$, this leads to $D(D + 3) / 2$ total independent parameters. As $D$ increases, these parameters grow quadratically, intensifying the computational cost related to matrix operations such as inversion, which is critical in many statistical procedures including likelihood maximization and prediction.

- #computational-complexity, #gaussian-distribution.parameter-scaling

## Analyze alternative covariance structures to reduce the dimensionality issues highlighted in Gaussian distributions.

To mitigate the computational difficulties associated with large $D$ in Gaussian distributions, alternative, less parameter-intensive forms of $\boldsymbol{\Sigma}$ can be employed:
- Diagonal covariance matrix, $\boldsymbol{\Sigma} = \operatorname{diag}(\sigma_i^2)$, has $2D$ parameters.
- Isotropic covariance matrix, $\boldsymbol{\Sigma} = \sigma^2 \mathbf{I}$, has only $D+1$ parameters.
These structures simplify the contours of constant density to axis-aligned and spherical, respectively, significantly easing computations yet at the cost of flexibility in capturing covariances across different dimensions.

- #statistical-modeling, #gaussian-distribution.covariance-reduction
## What does the expectation $\mathbb{E}[\mathbf{x}]$ represent in the context of the Gaussian distribution, and how is it derived?

The expectation $\mathbb{E}[\mathbf{x}]$ of a multivariate Gaussian distribution represents the mean vector $\boldsymbol{\mu}$ of the distribution. This is derived using the integral of the product of the multivariate Gaussian probability density function and the vector $\mathbf{x}$, followed by a change of variables to $\mathbf{z} = \mathbf{x} - \boldsymbol{\mu}$, simplifying the integrand and recognizing symmetry in the resulting expectation integral. The detailed derivation is:

$$
\mathbb{E}[\mathbf{x}] = \frac{1}{(2\pi)^{D/2}} \frac{1}{|\boldsymbol{\Sigma}|^{1/2}} \int \exp\left\{-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})\right\} \mathbf{x} \mathrm{d} \mathbf{x}
$$
Taking a change of variable $\mathbf{z} = \mathbf{x} - \boldsymbol{\mu}$, the integral simplifies to $\boldsymbol{\mu}$ due to the symmetry of the exponent term and vanishing of the integral involving $\mathbf{z}$ terms.

- #statistics, #gaussian-distribution.moments, #expectation-mean

## How do we compute the second-order moments matrix $\mathbb{E}[\mathbf{x}\mathbf{x}^{\mathrm{T}}]$ for a multivariate Gaussian distribution?

The second-order moments matrix $\mathbb{E}[\mathbf{x}\mathbf{x}^{\mathrm{T}}]$ for a multivariate Gaussian distribution is derived by integrating the outer product $\mathbf{x} \mathbf{x}^{\mathrm{T}}$ over the multivariate Gaussian distribution. This involves a similar change of variables to $\mathbf{z} = \mathbf{x} - \boldsymbol{\mu}$, leading to:
$$
\mathbb{E}[\mathbf{x} \mathbf{x}^{\mathrm{T}}] = \frac{1}{(2\pi)^{D/2}} \frac{1}{|\boldsymbol{\Sigma}|^{1/2}} \int \exp \left\{-\frac{1}{2} \mathbf{z}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \mathbf{z}\right\}(\mathbf{z}+\boldsymbol{\mu})(\mathbf{z}+\boldsymbol{\mu})^{\mathrm{T}} \mathrm{d} \mathbf{z},
$$
where the integral of the product $(\mathbf{z}+\boldsymbol{\mu})(\mathbf{z}+\boldsymbol{\mu})^{\mathrm{T}}$ simplifies by symmetry to $\boldsymbol{\mu} \boldsymbol{\mu}^{\mathrm{T}} + \boldsymbol{\Sigma}$.

- #statistics, #gaussian-distribution.moments, #second-order-moments

## What symmetry properties of the Gaussian distribution aid in simplifying the integrals when computing expectations and second-order moments?

The symmetry properties of the Gaussian distribution that aid in simplifying the integrals include the even nature of the exponent term and the symmetry associated with ranges taken over all space ($-\infty$ to $\infty$). For instance:
1. The exponent in the integrals is a quadratic form, which is even, thus simplifying terms involving odd functions or asymmetric products.
2. When computing expectations or moments, terms involving $\mathbf{z}$ (where $\mathbf{z} = \mathbf{x} - \boldsymbol{\mu}$) without an even power vanish due to the symmetry over $\mathbf{z}$ being integrated from $-\infty$ to $\infty$.

These symmetries result in the integral of $\mathbf{z}$ terms vanishing, and thus simplifying the expressions.

- #statistics, #gaussian-distribution.symmetry-properties, #integral-simplification

## Explain the role of the covariance matrix $\boldsymbol{\Sigma}$ and its inverse in the context of Gaussian distribution's probability density function.

The covariance matrix $\boldsymbol{\Sigma}$ and its inverse $\boldsymbol{\Sigma}^{-1}$ play crucial roles in defining the shape and orientation of the Gaussian distribution's probability contours. In the probability density function:
$$
f(\mathbf{x}) = \frac{1}{(2\pi)^{D/2}|\boldsymbol{\Sigma}|^{1/2}} \exp\left\{-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})\right\},
$$
$\boldsymbol{\Sigma}$ determines the spread (variance) along different directions in the feature space, and $\boldsymbol{\Sigma}^{-1}$ is used in the exponent to "weight" these deviations. Larger eigenvalues of $\boldsymbol{\Sigma}$ correspond to greater variance along their associated directions, influencing the density and the elongation of the distribution's contours.

- #statistics, #gaussian-distribution.properties, #covariance-matrix

## How does changing variables to $\mathbf{z} = \mathbf{x} - \boldsymbol{\mu}$ simplify the computation of expectations and moments in a Gaussian distribution?

Changing variables to $\mathbf{z} = \mathbf{x} - \boldsymbol{\mu}$ centralizes the variable around zero, simplifying the integral computations by reducing the integrand to a function of $\mathbf{z}$ only. This transformation leads to:
1. Removal of the mean vector $\boldsymbol{\mu}$ from the variables of integration, simplifying the exponent to a quadratic form in $\mathbf{z}$.
2. Simplifying symmetry considerations, as integrals involving odd powers of $\mathbf{z}$ over symmetric limits (from $-\infty$ to $\infty$) will vanish. 

This method is integral in deriving expressions such as $\mathbb{E}[\mathbf{x}] = \boldsymbol{\mu}$ and $\mathbb{E}[\mathbf{x}\mathbf{x}^{\mathrm{T}}] = \boldsymbol{\mu} \boldsymbol{\mu}^{\mathrm{T}} + \boldsymbol{\Sigma}$.

- #statistics, #gaussian-distribution.transformation, #variable-change
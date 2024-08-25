## Describe the shapes of the probability contours in a multivariate Gaussian distribution when the covariance matrix is of general form. 
The contours of constant probability density for a multivariate Gaussian distribution are shaped like ellipses when the covariance matrix is of a general form. 
- #statistics, #probability.multivariate-gaussian, #distribution-shapes

## What changes occur to the contours of a Gaussian distribution when the covariance matrix is diagonal?
When the covariance matrix is diagonal in a Gaussian distribution, the elliptical contours align with the coordinate axes. This configuration simplifies the expression of the distribution as it involves no off-diagonal terms representing covariances between different variables.
- #statistics, #probability.multivariate-gaussian, #covariance-matrix

## Explain the contour shape of a multivariate Gaussian distribution when the covariance matrix is proportional to the identity.

In a multivariate Gaussian distribution, when the covariance matrix is proportional to the identity matrix, the contours of constant probability density are concentric circles. This implies uniform variance across all dimensions and no covariance between them.
- #statistics, #probability.multivariate-gaussian, #covariance-identity

## How does partitioning a $D$-dimensional Gaussian vector into $\mathbf{x}_a$ and $\mathbf{x}_b$ align with their mean vectors?

Suppose $\mathbf{x}$ is a $D$-dimensional Gaussian vector partitioned into $\mathbf{x}_a$ (first $M$ components) and $\mathbf{x}_b$ (remaining $D-M$ components). The corresponding mean vectors are partitioned likewise, where $\boldsymbol{\mu}_a$ refers to the first $M$ components of the mean, and $\boldsymbol{\mu}_b$ to the remaining components, formulated as:
$$
\boldsymbol{\mu}=\binom{\boldsymbol{\mu}_a}{\boldsymbol{\mu}_b}
$$
This partitioning helps in simplifying calculations in problems involving conditional distributions.
- #statistics, #probability.multivariate-gaussian, #mean-vector

## Discuss the intrinsic limitations of Gaussian distributions concerning their modal properties.

Gaussian distributions are intrinsically unimodal, meaning they possess a single peak or maximum. This characteristic restricts their ability to approximate multimodal distributions which have multiple peaks. Such a limitation makes Gaussian distributions inadequate in scenarios where the data exhibits multiple dominant clusters.
- #statistics, #probability.gaussian-distribution, #distribution-limitations
## What does the red curve in Figure 3.3 represent?

The red curve in Figure 3.3 represents an elliptical surface of constant probability density for a two-dimensional Gaussian distribution, where the density value is $\exp(-1/2)$ of its maximum value at the mean $\mathbf{x} = \mu$. This surface is crucial in understanding the characteristics of multivariate Gaussian distributions, indicating how the probability density decreases as one moves away from the mean.

- #statistics, #probability-theory.gaussian-distribution

## What role do the eigenvectors $\mathbf{u}_{i}$ and eigenvalues $\lambda_{i}$ play in defining the Gaussian distribution's elliptical contours?

The eigenvectors $\mathbf{u}_{i}$ of the covariance matrix define the principal axes of the ellipse representing contours of equal probability density in the Gaussian distribution. The eigenvalues $\lambda_{i}$, corresponding to these eigenvectors, determine the length of each axis. Larger eigenvalues imply a greater spread along that axis.

- #linear-algebra, #statistics.covariance-matrix, #probability-theory.gaussian-distribution

## What is the significance of the determinant of the Jacobian matrix being 1 in the transformation from $\mathbf{x}$ to $\mathbf{y}$ coordinates?

The determinant of the Jacobian matrix being 1 implies that the transformation between the $\mathbf{x}$ coordinate system and the $\mathbf{y}$ coordinate system, defined by the matrix $\mathbf{J}$, preserves volume. In the context of the Gaussian distribution, this ensures that probabilities remain consistent when transitioning between these coordinate systems, crucial for maintaining the properties of the distribution under transformation.

$$
|\mathbf{J}| = |\mathbf{U}^{\mathrm{T}}| = 1
$$

- #calculus, #linear-algebra.jacobian-matrix, #probability-theory.transformation-properties

## Describe how the covariance matrix's determinant relates to its eigenvalues and the implications for the transformed Gaussian distribution in $y_{i}$ coordinates.

The determinant of the covariance matrix, denoted $|\boldsymbol{\Sigma}|$, is the product of its eigenvalues:

$$
|\boldsymbol{\Sigma}|^{1/2} = \prod_{j=1}^{D} \lambda_j^{1/2}
$$

In the $y_{i}$ coordinates, where the Gaussian distribution factors into $D$ independent univariate Gaussians, the determinant and the eigenvalues shape the individual distributions by determining their variances. This factorial decomposition is fundamental in simplifying the computation and understanding of the multivariate Gaussian distribution.

- #linear-algebra.eigenvalues, #statistics.covariance-matrix, #probability-theory.gaussian-distribution

## How does the integral of the Gaussian distribution in the $\mathbf{y}$ coordinate system confirm the distribution's normalization?

The integral of the Gaussian distribution $p(\mathbf{y})$ over the $\mathbf{y}$ coordinate system equals 1, which confirms the normalization of the distribution:

$$
\int p(\mathbf{y}) \mathrm{d} \mathbf{y} = 1
$$

This integral demonstrating that the total probability mass equals one is essential for any probability distribution and is particularly noteworthy here as it confirms the preservation of Gaussian properties post transformation using eigendecomposition.

- #calculus.integrals, #statistics.normalization, #probability-theory.gaussian-distribution
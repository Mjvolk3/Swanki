## How can the covariance matrix $\boldsymbol{\Sigma}$ be expressed using its eigenvectors and eigenvalues?

The covariance matrix $\boldsymbol{\Sigma}$ can be expressed as an expansion in terms of its eigenvectors $\mathbf{u}_{i}$ and corresponding eigenvalues $\lambda_i$:
$$
\boldsymbol{\Sigma}=\sum_{i=1}^{D} \lambda_{i} \mathbf{u}_{i} \mathbf{u}_{i}^{\mathrm{T}}
$$
This expression demonstrates the reconstruction of the covariance matrix from its eigen-decomposition, where each term $\lambda_{i} \mathbf{u}_{i} \mathbf{u}_{i}^{\mathrm{T}}$ represents the contribution of each eigenvector scaled by its corresponding eigenvalue.

- #linear-algebra.eigen-decomposition, #statistics.covariance-matrix

## What is the orthonormal condition for the eigenvectors of a real symmetric matrix $\boldsymbol{\Sigma}$?

For a real symmetric matrix $\boldsymbol{\Sigma}$, its eigenvectors $\mathbf{u}_{i}$ can be chosen to form an orthonormal set. This is expressed mathematically as:
$$
\mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{j}=I_{i j}
$$
where $I_{i j}$ is the $i, j$ element of the identity matrix:
$$
I_{i j}= \begin{cases}1, & \text{ if } i=j \\ 0, & \text{ otherwise }\end{cases}
$$
This orthonormality condition implies that any two distinct eigenvectors are orthogonal ($\mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{j}=0$ for $i \neq j$) and each eigenvector is normalized ($\mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{i}=1$).

- #linear-algebra.orthogonality, #linear-algebra.eigenvectors

## How is the inverse covariance matrix $\boldsymbol{\Sigma}^{-1}$ represented in terms of the eigenvalues and eigenvectors?

The inverse of the covariance matrix $\boldsymbol{\Sigma}$, denoted as $\boldsymbol{\Sigma}^{-1}$, is represented as:
$$
\boldsymbol{\Sigma}^{-1}=\sum_{i=1}^{D} \frac{1}{\lambda_{i}} \mathbf{u}_{i} \mathbf{u}_{i}^{\mathrm{T}}
$$
This formulation follows directly from the spectral decomposition of $\boldsymbol{\Sigma}$, where the inverse of each eigenvalue $\lambda_i$ scales the corresponding outer product of the eigenvector $\mathbf{u}_{i}$.

- #linear-algebra.inverse-matrix, #linear-algebra.eigen-decomposition

## What does the quadratic form $\Delta^2$ represent in the context of a transformed coordinate system using eigenvectors?

The quadratic form $\Delta^2$ is defined in the coordinate system transformed by the eigenvectors $\mathbf{u}_i$ of the covariance matrix $\boldsymbol{\Sigma}$:
$$
\Delta^{2}=\sum_{i=1}^{D} \frac{y_{i}^{2}}{\lambda_{i}}
$$
This expression arises from substituting the transformed coordinates $y_i = \mathbf{u}_i^\mathrm{T}(\mathbf{x}-\boldsymbol{\mu})$ into a general expression for calculating squared distances in the space defined by these new coordinates. This form is crucial for understanding the geometry of Gaussian distributions, especially their constant-density surfaces.

- #statistics.quadratic-form, #linear-algebra.transformation

## When is a Gaussian distribution well defined in terms of the positivity of the eigenvalues of its covariance matrix?

A Gaussian distribution requires that all eigenvalues $\lambda_i$ of the covariance matrix $\boldsymbol{\Sigma}$ be strictly positive. This ensures that the matrix is positive definite, which is a necessary condition for the distribution to be properly normalized:
$$
\lambda_i > 0 \quad \forall i
$$
If any $\lambda_i \leq 0$, the covariance matrix cannot define a Gaussian distribution, as it lacks a full-rank inverse necessary for defining the density function. This attribute is integral in ensuring the mathematical soundness and applicability of Gaussian models in statistical analysis.

- #statistics.gaussian-distribution, #linear-algebra.positive-definite
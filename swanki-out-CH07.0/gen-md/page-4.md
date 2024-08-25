## What is the local approximation to the gradient of the error function $E(\mathbf{w})$? Include the equation and its components in your answer.

The local approximation to the gradient of the error function $E(\mathbf{w})$ is given by:

$$
\nabla E(\mathbf{w})=\mathbf{b}+\mathbf{H}(\mathbf{w}-\widehat{\mathbf{w}})
$$

where:
- $\mathbf{b}$ is a vector of biases.
- $\mathbf{H}$ is the Hessian matrix.
- $\mathbf{w}$ is the current weight vector.
- $\widehat{\mathbf{w}}$ is the weight vector at the point of approximation.

- .neural-networks, .gradient-descent, .mathematics

## How is the local quadratic approximation of the error function $E(\mathbf{w})$ around a minimum point $\mathbf{w}^{\star}$ expressed?

The local quadratic approximation of the error function $E(\mathbf{w})$ around a minimum point $\mathbf{w}^{\star}$ is given by:

$$
E(\mathbf{w})=E\left(\mathbf{w}^{\star}\right)+\frac{1}{2}\left(\mathbf{w}-\mathbf{w}^{\star}\right)^{\mathrm{T}} \mathbf{H}\left(\mathbf{w}-\mathbf{w}^{\star}\right)
$$

where:
- $E\left(\mathbf{w}^{\star}\right)$ is the error at the minimum point.
- $\mathbf{H}$ is the Hessian matrix evaluated at $\mathbf{w}^{\star}$.
- $\mathbf{w}$ is the weight vector.
- $\mathbf{w}^{\star}$ is the weight vector at the minimum point.

- .neural-networks, .quadratic-approximation, .mathematics

## What is the eigenvalue equation for the Hessian matrix $\mathbf{H}$, and what are its components?

The eigenvalue equation for the Hessian matrix $\mathbf{H}$ is:

$$
\mathbf{H} \mathbf{u}_{i}=\lambda_{i} \mathbf{u}_{i}
$$

where:
- $\mathbf{H}$ is the Hessian matrix.
- $\mathbf{u}_{i}$ are the eigenvectors.
- $\lambda_{i}$ are the eigenvalues corresponding to the eigenvectors $\mathbf{u}_{i}$.

- .linear-algebra.eigenvalues, .mathematics, .quadratic-approximation
  
## When expanding $\left(\mathbf{w}-\mathbf{w}^{\star}\right)$ as a linear combination of the eigenvectors, what form does it take?

The expansion of $\left(\mathbf{w}-\mathbf{w}^{\star}\right)$ as a linear combination of the eigenvectors is given by:

$$
\mathbf{w}-\mathbf{w}^{\star}=\sum_{i} \alpha_{i} \mathbf{u}_{i}
$$

where:
- $\alpha_{i}$ are the coefficients.
- $\mathbf{u}_{i}$ are the eigenvectors.

This expansion represents a transformation of the coordinate system with the origin translated to $\mathbf{w}^{\star}$ and the axes aligned with the eigenvectors.

- .linear-algebra.eigenvectors, .neural-networks, .mathematics

## How can the error function $E(\mathbf{w})$ be represented when $\left(\mathbf{w}-\mathbf{w}^{\star}\right)$ is expanded as a linear combination of the eigenvectors?

When $\left(\mathbf{w}-\mathbf{w}^{\star}\right)$ is expanded as a linear combination of the eigenvectors, the error function $E(\mathbf{w})$ is represented as:

$$
E(\mathbf{w})=E\left(\mathbf{w}^{\star}\right)+\frac{1}{2} \sum_{i} \lambda_{i} \alpha_{i}^{2}
$$

where:
- $E\left(\mathbf{w}^{\star}\right)$ is the error at the minimum point.
- $\lambda_{i}$ are the eigenvalues.
- $\alpha_{i}$ are the coefficients in the eigenvector expansion.

- .neural-networks, .quadratic-approximation, .mathematics

## What is the criteria for a matrix $\mathbf{H}$ to be positive definite?

A matrix $\mathbf{H}$ is said to be positive definite if, and only if:

$$
\mathbf{v}^{\mathrm{T}} \mathbf{H} \mathbf{v}>0, \quad \text { for all } \mathbf{v}
$$

This implies that for any non-zero vector $\mathbf{v}$, the quadratic form $\mathbf{v}^{\mathrm{T}} \mathbf{H} \mathbf{v}$ is always positive.

- .linear-algebra.positive-definite-matrix, .mathematics
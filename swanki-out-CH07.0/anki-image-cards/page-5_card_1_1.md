## What do the eigenvalues and eigenvectors tell us about the error function near the minimum point $\mathbf{w}^{\star}$ in Figure 7.2?

![](https://cdn.mathpix.com/cropped/2024_05_26_2a651def79b1bf34dbe2g-1.jpg?height=451&width=767&top_left_y=219&top_left_x=877)

%

In the neighborhood of the minimum $\mathbf{w}^{\star}$, the error function can be approximated by a quadratic form. The axes of constant error contours are ellipses aligned with the eigenvectors $\mathbf{u}_{i}$ of the Hessian matrix $\mathbf{H}$, with lengths inversely proportional to the square roots of the corresponding eigenvalues $\lambda_i$. Therefore, the eigenvectors provide directions of principal curvature of the error function, and the eigenvalues indicate the steepness of the error function along those directions.

- #optimization, #quadratic-approximation, #eigenvalues-eigenvectors

---

## How can a vector $\mathbf{v}$ be expressed using the eigenvectors $\left\{\mathbf{u}_{i}\right\}$ of the Hessian matrix, and what is the result of the product $\mathbf{v}^{\mathrm{T}} \mathbf{H} \mathbf{v}$?

![](https://cdn.mathpix.com/cropped/2024_05_26_2a651def79b1bf34dbe2g-1.jpg?height=451&width=767&top_left_y=219&top_left_x=877)

%

Any arbitrary vector $\mathbf{v}$ can be expressed as 
$$
\mathbf{v} = \sum_{i} c_{i} \mathbf{u}_{i}
$$
where $c_i$ are coefficients and $\mathbf{u}_{i}$ are the eigenvectors of the Hessian matrix. The product $\mathbf{v}^{\mathrm{T}} \mathbf{H} \mathbf{v}$ can then be written as 
$$
\mathbf{v}^{\mathrm{T}} \mathbf{H} \mathbf{v} = \sum_{i} c_{i}^{2} \lambda_{i}
$$
This expression shows that $\mathbf{H}$ will be positive definite if, and only if, all its eigenvalues $\lambda_i$ are positive.

- #linear-algebra, #eigenvalues-eigenvectors, #hessian-matrix
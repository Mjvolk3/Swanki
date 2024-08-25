## The error function's quadratic approximation near a local minimum

![](https://cdn.mathpix.com/cropped/2024_05_26_2a651def79b1bf34dbe2g-1.jpg?height=451&width=767&top_left_y=219&top_left_x=877)

What is the geometric interpretation of the error function's quadratic approximation near a local minimum \( \mathbf{w}^{\star} \) as illustrated in Figure 7.2?

%

In the neighbourhood of a local minimum \( \mathbf{w}^{\star} \), the error function can be approximated by a quadratic function. The contours of constant error are ellipses aligned with the eigenvectors \( \mathbf{u}_i \) of the Hessian matrix. The lengths of these axes are inversely proportional to the square roots of the corresponding eigenvalues.

- #optimization, #error-function, #quadratic-approximation

## Condition for a local minimum in terms of the Hessian matrix

![](https://cdn.mathpix.com/cropped/2024_05_26_2a651def79b1bf34dbe2g-1.jpg?height=451&width=767&top_left_y=219&top_left_x=877)

What is the necessary and sufficient condition for \( \mathbf{w}^{\star} \) to be a local minimum?

%

A necessary and sufficient condition for \( \mathbf{w}^{\star} \) to be a local minimum is that the gradient of the error function should vanish at \( \mathbf{w}^{\star} \) and the Hessian matrix evaluated at \( \mathbf{w}^{\star} \) must be positive definite. 

- #optimization, #hessian-matrix, #local-minimum
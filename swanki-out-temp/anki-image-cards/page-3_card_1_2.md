### Card 1

![](https://cdn.mathpix.com/cropped/2024_05_26_a967798669c3977bb507g-1.jpg?height=469&width=515&top_left_y=212&top_left_x=1130)
%
Explain how the Lagrange multipliers method is applied to maximize the function \( f(x_1, x_2) = 1 - x_1^2 - x_2^2 \) subject to the constraint \( g(x_1, x_2) = 0 \), with \( g(x_1, x_2) = x_1 + x_2 - 1 \).
%
The Lagrange multipliers method involves introducing a new variable, $\lambda$, called the Lagrange multiplier, and forming the Lagrangian:

$$
\mathcal{L}(x_1, x_2, \lambda) = f(x_1, x_2) + \lambda g(x_1, x_2)
$$

For this problem:

$$
\mathcal{L}(x_1, x_2, \lambda) = (1 - x_1^2 - x_2^2) + \lambda (x_1 + x_2 - 1)
$$

We then set the partial derivatives of $\mathcal{L}$ with respect to $x_1$, $x_2$, and $\lambda$ equal to zero:

\[
\begin{cases}
\frac{\partial \mathcal{L}}{\partial x_1} = -2x_1 + \lambda = 0 \\
\frac{\partial \mathcal{L}}{\partial x_2} = -2x_2 + \lambda = 0 \\
\frac{\partial \mathcal{L}}{\partial \lambda} = x_1 + x_2 - 1 = 0
\end{cases}
\]

Solving these equations, we find the stationary point $\left(x_1^{\star}, x_2^{\star}\right)=(\frac{1}{2}, \frac{1}{2})$, and the corresponding value for the Lagrange multiplier is $\lambda = 1$.

- #optimization, #lagrange-multipliers, #constrained-optimization

### Card 2

![](https://cdn.mathpix.com/cropped/2024_05_26_a967798669c3977bb507g-1.jpg?height=469&width=515&top_left_y=212&top_left_x=1130)
%
Describe the geometric interpretation of the stationary point \(\left(x_{1}^{\star}, x_{2}^{\star}\right)=\left(\frac{1}{2}, \frac{1}{2}\right)\) in the context of Lagrange multipliers.
%
At the stationary point \(\left(x_{1}^{\star}, x_{2}^{\star}\right)=\left(\frac{1}{2}, \frac{1}{2}\right)\), the gradient of the function $f$ is perpendicular (orthogonal) to the constraint surface $g(x_1, x_2) = x_1 + x_2 - 1 = 0$. This means:

1. **Contours of \( f \)**: The concentric circles in the graph represent the contours of \( f(x_1, x_2) = 1 - x_1^2 - x_2^2 \). Each contour line corresponds to a constant value of \( f \).

2. **Constraint Surface**: The straight red line represents the constraint \( g(x_1, x_2) = x_1 + x_2 - 1 = 0 \).

3. **Stationary Point**: The point \(\left(\frac{1}{2}, \frac{1}{2}\right)\) is marked on the graph where the function \( f \) achieves its maximum value subject to the constraint \( g(x_1, x_2) = 0 \). At this point, the gradient of \( f \) is parallel to the gradient of \( g \), indicating orthogonality to the constraint surface.

- #visualization, #optimization, #lagrange-multipliers
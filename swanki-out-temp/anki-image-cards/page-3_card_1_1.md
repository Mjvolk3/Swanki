## How is the stationary point determined using Lagrange multipliers for the given optimization problem?

![](https://cdn.mathpix.com/cropped/2024_05_26_a967798669c3977bb507g-1.jpg?height=469&width=515&top_left_y=212&top_left_x=1130)

%

The stationary point is determined by solving the equations derived from the Lagrangian function. Given the objective function $f\left(x_{1}, x_{2}\right)=1 - x_{1}^{2} - x_{2}^{2}$ and the constraint $g\left(x_{1}, x_{2}\right)=x_{1}+x_{2}-1 = 0$, the Lagrangian is defined as:

$$
\mathcal{L}(x_{1}, x_{2}, \lambda) = f(x_{1}, x_{2}) - \lambda g(x_{1}, x_{2}).
$$

Substituting $f$ and $g$,

$$
\mathcal{L}(x_{1}, x_{2}, \lambda) = (1 - x_{1}^{2} - x_{2}^{2}) - \lambda (x_{1} + x_{2} - 1).
$$

Taking partial derivatives with respect to $x_{1}$, $x_{2}$, and $\lambda$, and setting them to zero, we find:

\[
\left\{
\begin{aligned}
\frac{\partial \mathcal{L}}{\partial x_{1}} &= -2x_{1} - \lambda = 0, \\
\frac{\partial \mathcal{L}}{\partial x_{2}} &= -2x_{2} - \lambda = 0, \\
\frac{\partial \mathcal{L}}{\partial \lambda} &= -(x_{1} + x_{2} - 1) = 0. \\
\end{aligned}
\right.
\]

Solving these equations simultaneously, we obtain the stationary point $\left(x_{1}^{\star}, x_{2}^{\star}\right) = \left(\frac{1}{2}, \frac{1}{2}\right)$ and the Lagrange multiplier $\lambda = 1$.

- #mathematics, #optimisation, #lagrange-multipliers
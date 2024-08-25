Figure C. 2 A simple example of the use of Lagrange multipliers in which the aim is to maximize $f\left(x_{1}, x_{2}\right)=1-$ $x_{1}^{2}-x_{2}^{2}$ subject to the constraint $g\left(x_{1}, x_{2}\right)=0$ where $g\left(x_{1}, x_{2}\right)=x_{1}+x_{2}-1$. The circles show contours of the function $f\left(x_{1}, x_{2}\right)$, and the diagonal line shows the constraint surface $g\left(x_{1}, x_{2}\right)=0$.

![](https://cdn.mathpix.com/cropped/2024_05_26_ffad232c340143af6219g-1.jpg?height=469&width=515&top_left_y=212&top_left_x=1130)

Solving these equations then gives the stationary point as $\left(x_{1}^{\star}, x_{2}^{\star}\right)=(1 / 2,1 / 2)$, and the corresponding value for the Lagrange multiplier is $\lambda=1$.

So far, we have considered the problem of maximizing a function subject to an equality constraint of the form $g(\mathbf{x})=0$. We now consider the problem of maximizing $f(\mathbf{x})$ subject to an inequality constraint of the form $g(\mathbf{x}) \geqslant 0$, as illustrated in Figure C.3.

There are now two kinds of solution possible, according to whether the constrained stationary point lies in the region where $g(\mathbf{x})>0$, in which case the constraint is inactive, or whether it lies on the boundary $g(\mathbf{x})=0$, in which case the constraint is said to be active. In the former case, the function $g(\mathbf{x})$ plays no role and so the stationary condition is simply $\nabla f(\mathbf{x})=0$. This again corresponds to a stationary point of the Lagrange function (C.4) but this time with $\lambda=0$. The latter case, where the solution lies on the boundary, is analogous to the equality constraint discussed previously and corresponds to a stationary point of the Lagrange function (C.4) with $\lambda \neq 0$. Now, however, the sign of the Lagrange multiplier is crucial, because the function $f(\mathbf{x})$ is at a maximum only if its gradient is oriented away from the region $g(\mathbf{x})>0$, as illustrated in Figure C.3. We therefore have $\nabla f(\mathbf{x})=-\lambda \nabla g(\mathbf{x})$ for some value of $\lambda>0$.

For either of these two cases, the product $\lambda g(\mathbf{x})=0$. Thus, the solution to

Figure C. 3 Illustration of the problem of maximizing $f(\mathbf{x})$ subject to the inequality constraint $g(\mathbf{x}) \geqslant 0$.

![](https://cdn.mathpix.com/cropped/2024_05_26_ffad232c340143af6219g-1.jpg?height=511&width=611&top_left_y=1591&top_left_x=1033)
Figure C. 1 A geometrical picture of the technique of Lagrange multipliers in which we seek to maximize a function $f(\mathbf{x})$, subject to the constraint $g(\mathbf{x})=0$. If $\mathbf{x}$ is $D$ dimensional, the constraint $g(\mathbf{x})=0$ corresponds to a subspace of dimensionality $D-1$, as indicated by the red curve. The problem can be solved by optimizing the Lagrangian function $L(\mathbf{x}, \lambda)=f(\mathbf{x})+\lambda g(\mathbf{x})$.

![](https://cdn.mathpix.com/cropped/2024_05_26_57d37ae5bb94cf2241e6g-1.jpg?height=509&width=535&top_left_y=212&top_left_x=1110)

then parallel to the constraint surface $g(\mathbf{x})=0$, we see that the vector $\nabla g$ is normal to the surface.

Next we seek a point $\mathbf{x}^{\star}$ on the constraint surface such that $f(\mathbf{x})$ is maximized. Such a point must have the property that the vector $\nabla f(\mathbf{x})$ is also orthogonal to the constraint surface, as illustrated in Figure C.1, because otherwise we could increase the value of $f(\mathbf{x})$ by moving a short distance along the constraint surface. Thus, $\nabla f$ and $\nabla g$ are parallel (or anti-parallel) vectors, and so there must exist a parameter $\lambda$ such that

$$
\nabla f+\lambda \nabla g=0
$$

where $\lambda \neq 0$ is known as a Lagrange multiplier. Note that $\lambda$ can have either sign.

At this point, it is convenient to introduce the Lagrangian function defined by

$$
L(\mathbf{x}, \lambda) \equiv f(\mathbf{x})+\lambda g(\mathbf{x})
$$

The constrained stationarity condition (C.3) is obtained by setting $\nabla_{\mathbf{x}} L=0$. Furthermore, the condition $\partial L / \partial \lambda=0$ leads to the constraint equation $g(\mathbf{x})=0$.

Thus, to find the maximum of a function $f(\mathbf{x})$ subject to the constraint $g(\mathbf{x})=0$, we define the Lagrangian function given by (C.4) and we then find the stationary point of $L(\mathbf{x}, \lambda)$ with respect to both $\mathbf{x}$ and $\lambda$. For a $D$-dimensional vector $\mathbf{x}$, this gives $D+1$ equations that determine both the stationary point $\mathbf{x}^{\star}$ and the value of $\lambda$. If we are interested only in $\mathbf{x}^{\star}$, then we can eliminate $\lambda$ from the stationarity equations without needing to find its value (hence, the term 'undetermined multiplier').

As a simple example, suppose we wish to find the stationary point of the function $f\left(x_{1}, x_{2}\right)=1-x_{1}^{2}-x_{2}^{2}$ subject to the constraint $g\left(x_{1}, x_{2}\right)=x_{1}+x_{2}-1=0$, as illustrated in Figure C.2. The corresponding Lagrangian function is given by

$$
L(\mathbf{x}, \lambda)=1-x_{1}^{2}-x_{2}^{2}+\lambda\left(x_{1}+x_{2}-1\right)
$$

The conditions for this Lagrangian to be stationary with respect to $x_{1}, x_{2}$, and $\lambda$ give the following coupled equations:

$$
\begin{aligned}
-2 x_{1}+\lambda & =0 \\
-2 x_{2}+\lambda & =0 \\
x_{1}+x_{2}-1 & =0
\end{aligned}
$$
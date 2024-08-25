## When solving for the stationary points of a function $f(x_1, x_2)$ subject to a constraint $g(x_1, x_2) = 0$, why might solving the constraint equation directly to express $x_2$ as a function of $x_1$ be challenging?

Solving the constraint equation directly may be challenging because it might not be possible to find an analytic solution that allows $x_2$ to be expressed explicitly as a function of $x_1$. Additionally, this method treats $x_1$ and $x_2$ differently, destroying the natural symmetry between these variables.

- #optimization, #constraints, #lagrange-multipliers

---

## Describe how a Lagrange multiplier, $\lambda$, is used in the method of Lagrange multipliers to address the problem of finding the stationary points of a function $f(x_1, x_2)$ subject to a constraint $g(x_1, x_2)=0$.

A Lagrange multiplier, $\lambda$, is introduced to transform the original problem into finding the stationary points of the Lagrangian function:

$$
\mathcal{L}(x_1, x_2, \lambda) = f(x_1, x_2) - \lambda g(x_1, x_2)
$$

The stationary points are then found by setting the gradients with respect to $x_1$, $x_2$, and $\lambda$ to zero.

- #optimization, #constraints, #lagrange-multipliers

---

## Explain how the gradient of the constraint function $g(\mathbf{x})$ is related to the constraint surface in $\mathbf{x}$-space.

At any point on the constraint surface, the gradient $\nabla g(\mathbf{x})$ of the constraint function is orthogonal to the surface. This can be demonstrated by considering a small perturbation $\boldsymbol{\epsilon}$ and using a Taylor expansion around a point $\mathbf{x}$ on the constraint surface:

$$
g(\mathbf{x} + \boldsymbol{\epsilon}) \sims g(\mathbf{x}) + \boldsymbol{\epsilon}^{\mathrm{T}} \nabla g(\mathbf{x})
$$

Given $g(\mathbf{x}) = g(\mathbf{x} + \boldsymbol{\epsilon})$, it follows that $\boldsymbol{\epsilon}^{\mathrm{T}} \nabla g(\mathbf{x}) \sims 0$.

- #geometry, #optimization, #lagrange-multipliers

---

## In Lagrange multipliers, why is the gradient $\nabla g(\mathbf{x})$ orthogonal to the surface of the constraint function $g(\mathbf{x})=0$?

At any point $\mathbf{x}$ on the constraint surface, a nearby point $\mathbf{x} + \boldsymbol{\epsilon}$ also lies on the surface. Using a Taylor expansion:

$$
g(\mathbf{x} + \boldsymbol{\epsilon}) \sims g(\mathbf{x}) + \boldsymbol{\epsilon}^{\mathrm{T}} \nabla g(\mathbf{x})
$$

Given both $\mathbf{x}$ and $\mathbf{x} + \boldsymbol{\epsilon}$ satisfy the constraint $g(\mathbf{x}) = g(\mathbf{x} + \boldsymbol{\epsilon})$, $\boldsymbol{\epsilon}^{\mathrm{T}} \nabla g(\mathbf{x}) \sims 0$ in the limit $\|\boldsymbol{\epsilon}\| \rightarrow 0$.

- #geometry, #optimization, #lagrange-multipliers

---

## How can the technique of Lagrange multipliers be motivated from a geometrical perspective in $\mathbf{x}$-space?

From a geometrical perspective, the constraint $g(\mathbf{x}) = 0$ represents a $(D-1)$-dimensional surface in $D$-dimensional $\mathbf{x}$-space. The gradient $\nabla g(\mathbf{x})$ is orthogonal to this constraint surface. This orthogonality ensures that any perturbation $\boldsymbol{\epsilon}$ within the surface satisfies $\boldsymbol{\epsilon}^{\mathrm{T}} \nabla g(\mathbf{x}) \sims 0$.

- #geometry, #optimization, #lagrange-multipliers

---

## Explain the step-by-step process of finding a stationary point using Lagrange multipliers for a function $f(x_1, x_2)$ subject to $g(x_1, x_2) = 0$.

1. Construct the Lagrangian function:
   $$
   \mathcal{L}(x_1, x_2, \lambda) = f(x_1, x_2) - \lambda g(x_1, x_2)
   $$

2. Find the partial derivatives:
   $$
   \begin{aligned}
   \frac{\partial \mathcal{L}}{\partial x_1} &= \frac{\partial f}{\partial x_1} - \lambda \frac{\partial g}{\partial x_1} \\
   \frac{\partial \mathcal{L}}{\partial x_2} &= \frac{\partial f}{\partial x_2} - \lambda \frac{\partial g}{\partial x_2} \\
   \frac{\partial \mathcal{L}}{\partial \lambda} &= -g(x_1, x_2)
   \end{aligned}
   $$

3. Set each partial derivative to zero and solve the resulting system of equations to find $x_1, x_2$, and $\lambda$.

- #optimization, #calculus, #lagrange-multipliers
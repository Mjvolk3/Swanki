Here's a set of six Anki cards based on the provided chunk of text on Lagrange multipliers.

### Card 1
## What is the primary purpose of Lagrange multipliers in optimization problems?

Lagrange multipliers, also sometimes called undetermined multipliers, are used to find the stationary points of a function of several variables subject to one or more constraints.

- #optimization, #lagrange-multipliers

---

### Card 2
## Describe the constraint equation in the context of Lagrange multipliers and provide the equation.

In the context of Lagrange multipliers, the constraint equation relates the variables $x_1$ and $x_2$ in the form:

$$
g(x_1, x_2) = 0
$$

- #optimization, #constraints

---

### Card 3
## Explain why the direct approach of solving the constraint equation and substituting into the objective function can be cumbersome. What is the alternative?

The direct approach can be cumbersome because:
1. It may be difficult to find an analytic solution of the constraint equation.
2. It treats $x_1$ and $x_2$ differently, spoiling the natural symmetry.

The alternative is to introduce a Lagrange multiplier $\lambda$.

- #optimization, #direct-approach, #lagrange-multipliers

---

### Card 4
## What is the significance of the gradient $\nabla g(\mathbf{x})$ on the constraint surface?

At any point on the constraint surface, the gradient $\nabla g(\mathbf{x})$ of the constraint function is orthogonal to the surface.

This is shown by considering a Taylor expansion around a point $\mathbf{x}$ on the constraint surface to a nearby point $\mathbf{x} + \boldsymbol{\epsilon}$ which also lies on the surface.

- #calculus, #gradients, #constraints

---

### Card 5
## Derive the result showing why the gradient $\nabla g(\mathbf{x})$ is orthogonal to the constraint surface.

Given:

$$
g(\mathbf{x} + \boldsymbol{\epsilon}) \simeq g(\mathbf{x}) + \boldsymbol{\epsilon}^{\mathrm{T}} \nabla g(\mathbf{x})
$$

Since $\mathbf{x}$ and $\mathbf{x}+\boldsymbol{\epsilon}$ lie on the constraints surface:

$$
\boldsymbol{\epsilon}^{\mathrm{T}} \nabla g(\mathbf{x}) \simeq 0
$$

In the limit $\|\boldsymbol{\epsilon}\| \rightarrow 0$:

$$
\boldsymbol{\epsilon}^{\mathrm{T}} \nabla g(\mathbf{x}) = 0
$$

This shows $\nabla g(\mathbf{x})$ is orthogonal to $\boldsymbol{\epsilon}$.

- #derivation, #constraints, #gradients

---

### Card 6
## How does introducing a Lagrange multiplier $\lambda$ simplify finding the stationary points under constraints?

By introducing a Lagrange multiplier $\lambda$, we can define a new function $\mathcal{L}(x_1, x_2, \lambda)$ such that:

$$
\mathcal{L}(x_1, x_2, \lambda) = f(x_1, x_2) + \lambda g(x_1, x_2)
$$

Setting the partial derivatives of $\mathcal{L}$ equal to zero simplifies the problem by transforming it into a system of equations that can be solved more easily.

- #optimization, #lagrange-multipliers, #simplification
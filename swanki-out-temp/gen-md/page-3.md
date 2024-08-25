### Card 1

## How do you express the objective and constraint functions for maximizing $f(x_1, x_2) = 1 - x_1^2 - x_2^2$ with a constraint $g(x_1, x_2) = 0$?

$$
\text{Objective: } f(x_1, x_2) = 1 - x_1^2 - x_2^2
$$
$$
\text{Constraint: } g(x_1, x_2) = x_1 + x_2 - 1
$$

- #optimization, #lagrange-multipliers


### Card 2

## What system of equations do you need to solve to find the stationary points in a constrained optimization problem using Lagrange multipliers?

You need to solve the system given by the gradients of the Lagrange function set to zero:

$$
\nabla f(\mathbf{x}) = -\lambda \nabla g(\mathbf{x})
$$
$$
g(\mathbf{x}) = 0
$$

Where $\mathbf{x}$ represents the variables vector and $\lambda$ is the Lagrange multiplier.

- #optimization, #lagrange-multipliers


### Card 3

## What are the values of $x_1$ and $x_2$ that maximize $f(x_1, x_2)$ subject to $g(x_1, x_2) = 0$ in the given problem?

Solving the system gives the stationary point as:

$$
(x_1^{\star}, x_2^{\star}) = \left(\frac{1}{2}, \frac{1}{2}\right)
$$

- #optimization, #lagrange-multipliers

### Card 4

## Describe the case when the constraint $g(\mathbf{x}) \geq 0$ is active or inactive in inequality-constrained optimization.

1. **Active Constraint**: The constrained stationary point lies on the boundary $g(\mathbf{x}) = 0$, and $\lambda \neq 0$.
   
2. **Inactive Constraint**: The constrained stationary point lies in the region $g(\mathbf{x}) > 0$, and $\lambda = 0$.

In the inactive case, the constraint plays no role, hence:

$$
\nabla f(\mathbf{x}) = 0
$$

- #optimization, #inequality-constraints


### Card 5

## How does the sign of the Lagrange multiplier $\lambda$ influence the solution for inequality constraints in Lagrangian optimization?

The solution to the inequality constraint problem is valid only if $\lambda > 0$, ensuring that the gradient is oriented away from the region where $g(\mathbf{x}) > 0$:

$$
\nabla f(\mathbf{x}) = -\lambda \nabla g(\mathbf{x}) \text{ for some } \lambda > 0
$$

- #optimization, #lagrange-multipliers


### Card 6

## What is the complementary slackness condition in the context of inequality constraints in optimization?

For either the active or inactive constraint cases, the product $\lambda g(\mathbf{x})$ must satisfy:

$$
\lambda g(\mathbf{x}) = 0
$$

This condition implies that either $\lambda = 0$ (inactive constraint) or $g(\mathbf{x}) = 0$ (active constraint).

- #optimization, #lagrange-multipliers
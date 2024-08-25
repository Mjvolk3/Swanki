```markdown
## Define the constrained optimization problem described in the paper chunk with given constraints.

The paper describes maximizing the function $f(x_1, x_2) = 1 - x_1^2 - x_2^2$ subject to the constraint $g(x_1, x_2) = x_1 + x_2 - 1 = 0$.

%
This is a classic example of a constrained optimization problem, where:

1. $f(x_1, x_2) = 1 - x_1^2 - x_2^2$ is the objective function to be maximized.
2. $g(x_1, x_2) = x_1 + x_2 - 1$ is the constraint that must be satisfied.

- #optimization, #math.constrained-optimization

## What are the values of the stationary point and the Lagrange multiplier for the given problem?

The stationary point is $\left( \frac{1}{2}, \frac{1}{2} \right)$, and the corresponding value for the Lagrange multiplier is $\lambda = 1$.

- #optimization, #math.lagrange-multipliers

## Describe what happens when the constraint $g(\mathbf{x}) \geqslant 0$ is inactive.

When the constraint $g(\mathbf{x}) > 0$ is inactive, the stationary condition is simply $\nabla f(\mathbf{x}) = 0$. This corresponds to a stationary point of the Lagrange function with $\lambda = 0$.

%
In this case, since $\lambda = 0$ and $\nabla f(\mathbf{x}) = 0$, the constraint does not affect the optimization problem. The problem reduces to unconstrained optimization of $f(\mathbf{x})$.

- #optimization, #math.constrained-optimization

## What equation must be satisfied by the product of the Lagrange multiplier and the constraint function in either of the cases considered?

For either of the cases, the product $\lambda g(\mathbf{x}) = 0$ must be satisfied.

%
This implies that either the Lagrange multiplier $\lambda$ is zero, or the constraint $g(\mathbf{x}) = 0$ is active. 

- #optimization, #math.lagrange-multipliers

## What is the condition for the function $f(\mathbf{x})$ to reach its maximum when the constraint boundary is active?

When the constraint boundary $g(\mathbf{x}) = 0$ is active, $f(\mathbf{x})$ is at a maximum only if $\nabla f(\mathbf{x}) = -\lambda \nabla g(\mathbf{x})$ for some $\lambda > 0$.

%
This condition indicates that the gradient of $f$ must be oriented away from the region where $g(\mathbf{x}) > 0$. 

- #optimization, #math.constrained-optimization

## Explain the significance of the sign of the Lagrange multiplier $\lambda$ in constrained optimization problems.

The sign of the Lagrange multiplier $\lambda$ is crucial because $f(\mathbf{x})$ is at a maximum only if its gradient is oriented away from the region $g(\mathbf{x}) > 0$, implying $\lambda > 0$.

%
In the context of maximizing $f(\mathbf{x})$ subject to $g(\mathbf{x}) \geq 0$, a positive $\lambda$ ensures that the optimization respects the constraint by pushing $f(\mathbf{x})$ away from the boundary defined by the constraint.

- #optimization, #math.lagrange-multipliers
```
### Card 1

**Q: Explain the geometrical interpretation of Lagrange multipliers for finding the extrema of a function subject to a constraint.**

![](https://cdn.mathpix.com/cropped/2024_05_26_57d37ae5bb94cf2241e6g-1.jpg?height=509&width=535&top_left_y=212&top_left_x=1110)

%

To find the extrema of a function $f(\mathbf{x})$ subject to a constraint $g(\mathbf{x})=0$, the technique of Lagrange multipliers introduces an auxiliary function called the Lagrangian:

$$
L(\mathbf{x}, \lambda)=f(\mathbf{x})+\lambda g(\mathbf{x})
$$

where $\lambda$ is the Lagrange multiplier. The problem is reduced to finding points where the gradients of $f$ and $g$ are parallel (or anti-parallel), meaning there exists a $\lambda$ such that:

$$
\nabla f(\mathbf{x}) + \lambda \nabla g(\mathbf{x}) = 0
$$

Here, $\nabla g$ is orthogonal to the constraint surface $g(\mathbf{x})=0$, and $\nabla f$ must be parallel to $\nabla g$ at the optimal points on the constraint.

- #mathematics, #optimization.lagrange-multipliers, #calculus.gradient

---

### Card 2

**Q: What is the significance of the gradients $\nabla f$ and $\nabla g$ in the context of Lagrange multipliers, as depicted in the image?**

![](https://cdn.mathpix.com/cropped/2024_05_26_57d37ae5bb94cf2241e6g-1.jpg?height=509&width=535&top_left_y=212&top_left_x=1110)

%

In Lagrange multipliers, the gradients $\nabla f$ and $\nabla g$ at the point $\mathbf{x}^\star$ where the function $f(\mathbf{x})$ is maximized (or minimized) subject to $g(\mathbf{x})=0$ are crucial. The illustration indicates that:

1. $\nabla g$ is normal (orthogonal) to the constraint surface defined by $g(\mathbf{x}) = 0$.
2. For the optimal solution, $\nabla f$ must also be orthogonal to the constraint surface.

This implies that $\nabla f$ and $\nabla g$ are parallel (or anti-parallel), leading to the condition:

$$
\nabla f + \lambda \nabla g = 0
$$

where $\lambda$ is the Lagrange multiplier. This condition ensures that moving along the constraint surface does not increase $f(\mathbf{x})$ further at the optimal point.

- #mathematics, #optimization.gradient, #calculus.lagrange-multipliers
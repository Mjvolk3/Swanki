### Card 1

How does the method of Lagrange multipliers ensure that the constraint surface $g(\mathbf{x})=0$ is respected while maximizing the function $f(\mathbf{x})$?

![](https://cdn.mathpix.com/cropped/2024_05_26_879d27325c75f8de5f2eg-1.jpg?height=509&width=535&top_left_y=212&top_left_x=1110)

%

The method involves constructing the Lagrangian function $L(\mathbf{x}, \lambda) = f(\mathbf{x}) + \lambda g(\mathbf{x})$, where $\lambda$ is the Lagrange multiplier. By requiring that the gradients of $f$ and $g$ are parallel (or anti-parallel) at the point $\mathbf{x}^{\star}$ on the constraint surface, we guarantee that the function $f(\mathbf{x})$ is optimized while still satisfying $g(\mathbf{x})=0$. Mathematically, this is expressed as:

$$
\nabla f + \lambda \nabla g = 0
$$

- #mathematics, #optimization.lagrange-multipliers, #geometry

### Card 2

What geometric relationship between $\nabla f$ and $\nabla g$ is critical for the method of Lagrange multipliers?

![](https://cdn.mathpix.com/cropped/2024_05_26_879d27325c75f8de5f2eg-1.jpg?height=509&width=535&top_left_y=212&top_left_x=1110)

%

The critical geometric relationship is that $\nabla f$ and $\nabla g$ must be parallel (or anti-parallel) at the optimization point $\mathbf{x}^{\star}$. This ensures that any movement along the constraint surface $g(\mathbf{x}) = 0$ does not increase the value of $f(\mathbf{x})$. Mathematically, this is represented by:

$$
\nabla f + \lambda \nabla g = 0
$$

- #mathematics, #optimization.lagrange-multipliers, #geometry
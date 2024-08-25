## What does the provided image represent in terms of linear classifiers?

![](https://cdn.mathpix.com/cropped/2024_05_26_54f3776e893a83ecd076g-1.jpg?height=698&width=898&top_left_y=215&top_left_x=760)

%

The image is a two-dimensional representation of a linear discriminant function. It showcases:
- Two input feature axes, $x_1$ and $x_2$.
- A red decision boundary (line) labeled $y = 0$ dividing two regions, $R_1$ and $R_2$.
- The boundary is perpendicular to the weight vector $\mathbf{w}$, indicated by a green arrow.
- The displacements from a point $\mathbf{x}$ to the boundary and the orthogonal projection are highlighted. The distance is given by $\frac{y(\mathbf{x})}{\|\mathbf{w}\|}$.
- The bias term $\frac{-w_{0}}{\|\mathbf{w}\|}$ is shown on the $x_1$ axis, indicating the decision boundary's position relative to the origin.

- #machine-learning, #classification, #linear-discriminant-analysis


## Explain how the bias term \( w_0 \) influences the decision boundary in a linear discriminant function.

![](https://cdn.mathpix.com/cropped/2024_05_26_54f3776e893a83ecd076g-1.jpg?height=698&width=898&top_left_y=215&top_left_x=760)

%

The bias parameter \( w_0 \) controls the displacement of the decision boundary from the origin. The normal distance from the origin to the decision surface is given by:

$$
\frac{\mathbf{w}^{\mathrm{T}} \mathbf{x}}{\|\mathbf{w}\|} = -\frac{w_0}{\|\mathbf{w}\|}
$$

Hence, \( w_0 \) shifts the decision boundary closer or farther from the origin based on its value.

- #machine-learning, #mathematics, #classification
## What does the decision surface in a linear discriminant function depend on?

![](https://cdn.mathpix.com/cropped/2024_05_26_54f3776e893a83ecd076g-1.jpg?height=698&width=898&top_left_y=215&top_left_x=760)

%

The decision surface is perpendicular to the weight vector $\mathbf{w}$ and its displacement from the origin is controlled by the bias parameter $w_{0}$. The signed orthogonal distance of a general point $\mathbf{x}$ from the decision surface is given by $\frac{y(\mathbf{x})}{\|\mathbf{w}\|}$.

- #machine-learning, #linear-classifier, #decision-boundary

---

## How is the normal distance from the origin to the decision surface determined in a linear discriminant function?

![](https://cdn.mathpix.com/cropped/2024_05_26_54f3776e893a83ecd076g-1.jpg?height=698&width=898&top_left_y=215&top_left_x=760)

%

The normal distance from the origin to the decision surface is given by 

$$
\frac{\mathbf{w}^{\mathrm{T}} \mathbf{x}}{\|\mathbf{w}\|} = -\frac{w_{0}}{\|\mathbf{w}\|}
$$

Thus, the bias parameter $w_{0}$ determines the location of the decision surface.

- #geometry, #linear-discriminant, #machine-learning
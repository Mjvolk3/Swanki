## Card 1

Illustrate the decision regions for a multi-class linear discriminant based on the image provided.

![](https://cdn.mathpix.com/cropped/2024_05_26_c6820e8ed9a153596826g-1.jpg?height=418&width=581&top_left_y=211&top_left_x=1065)

% 

The decision regions for a multi-class linear discriminant are composed of separate, convex decision regions demarcated by decision boundaries (in red). If two points $\mathrm{x}_{\mathrm{A}}$ and $\mathrm{x}_{\mathrm{B}}$ lie within the same decision region $\mathcal{R}_{k}$, any point $\widehat{\mathrm{x}}$ on the line connecting these points will also lie in $\mathcal{R}_{k}$, proving the region's convex nature.

- #machine-learning, #classification.linear-discriminant, #geometry.convex-regions

## Card 2

Describe the formula defining a $(D-1)$-dimensional hyperplane as a decision boundary in a multi-class discriminant scenario based on the given text and image.

![](https://cdn.mathpix.com/cropped/2024_05_26_c6820e8ed9a153596826g-1.jpg?height=418&width=581&top_left_y=211&top_left_x=1065)

%

The decision boundary for a multi-class linear discriminant is represented by the $(D-1)$-dimensional hyperplane, given by:

$$
\left(\mathbf{w}_{k}-\mathbf{w}_{j}\right)^{\mathrm{T}} \mathbf{x}+\left(w_{k 0}-w_{j 0}\right)=0
$$

It shares the same form as the decision boundary in a two-class case, where analogous geometrical properties apply. This hyperplane divides the input space into distinct, convex decision regions.

- #machine-learning, #classification.multi-class, #linear-algebra.hyperplane
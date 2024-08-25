## Explain how the mode of a density transforms under a nonlinear variable change. Why does this differ from transforming the density as a simple function of the variable?

When transforming a density $p_x(x)$ under a nonlinear change of variables using a function $g(y)$, the mode of the original density does not necessarily correspond to the mode of the transformed density $p_x(g(y))$, illustrated as the green curve in the example. This discrepancy arises because the mode of $p_x(x)$, when passed through the nonlinear function $g$, results in a different location on the transformed curve compared to direct transformation of the density itself according to the specialized formula for density transformation under change of variables.
  
$$
p_y(y) = p_x(x) |\operatorname{det} \mathbf{J}|
$$
  
where $\mathbf{J}$ is the Jacobian matrix of partial derivatives of $\mathbf{g}^{-1}$. This transformation takes into account the change in volume element in the variable space, which affects the mode's location unlike the simple transformation $p_x(g(y))$.
  
- #probability.distributions, #statistics.nonlinear-transformation, #mathematical-concepts.density-transformation

## What equation describes the transformed density under a variable change, including its Jacobian matrix representation?

The transformed density $p_{\mathbf{y}}(\mathbf{y})$ when changing variables from $\mathbf{x}$ to $\mathbf{y}$, where $\mathbf{y} = \mathbf{g}(\mathbf{x})$, is given by:

$$
p_{\mathbf{y}}(\mathbf{y}) = p_{\mathbf{x}}(\mathbf{x}) |\operatorname{det} \mathbf{J}|
$$

Here, $\mathbf{J}$ is the Jacobian matrix whose elements are the partial derivatives $J_{ij} = \partial g_i / \partial y_j$. The Jacobian matrix is given by:

$$
\mathbf{J} = \left[\begin{array}{ccc}
\frac{\partial g_1}{\partial y_1} & \cdots & \frac{\partial g_1}{\partial y_D} \\
\vdots & \ddots & \vdots \\
\frac{\partial g_D}{\partial y_1} & \cdots & \frac{\partial g_D}{\partial y_D}
\end{array}\right]
$$

This represents how local volume elements transform under the mapping $\mathbf{g}$, affecting the density by the absolute value of the determinant of $\mathbf{J}$.

- #probability.distributions, #mathematics.jacobian, #mathematical-concepts.variable-change

## Distinguish between the "direct" transformation of a probability density and its proper transformation under a change of variables.

Direct transformation of a density $p_x(x)$ by simply substituting the transformation function, yielding $p_x(g(y))$, does not account for how differential volume elements are distorted by the variable change. This method often results in an incorrect density on the transformed space and fails to preserve the total probability. The correct transformation, however, involves the modified Jacobian determinant approach:

$$
p_y(y) = p_x(g(y)) |\operatorname{det} \mathbf{J}|^{-1}
$$

This approach ensures that the density is properly scaled to account for the expansion or contraction of volume elements in the transformed space, thereby maintaining the integrity of the probability distribution.

- #statistics.transformation-techniques, #probability.correct-density-transformation, #mathematical-concepts.jacobian-determinant

## How does the concept of variable space transformation relate to the physical idea of space contraction and expansion?

In the context of variable transformations, such as $\mathbf{x} = \mathbf{g}(\mathbf{y})$, the transformation conceptually maps an infinitesimal region $\Delta \mathbf{x}$ around a point $\mathbf{x}$ to a new region $\Delta \mathbf{y}$ around $\mathbf{y}$. The determinant of the Jacobian matrix $\operatorname{det} \mathbf{J}$ quantifies the ratio of the volumes of these infinitesimal regions, essentially measuring how much a certain volume in the $\mathbf{x}$-space is expanded or contracted when transformed to $\mathbf{y}$-space. This determinant being positive or negative also indicates whether the transformation preserves or reverses the orientation of the space.

- #mathematics.spatial-transformation, #math.translation-expansion-contraction, #probability.density-properties

## How can the visualization of density transformations help in understanding their behavior under nonlinear transformations?

Visualizing the transformation of densities, such as in the given example with the green and magenta curves, offers a concrete interpretation of the abstract concepts involved in density transformations. The modes of these curves illustrate the differences between a simple function application, which results in the mode of $p_x(x)$ being directly transformed, and the proper density transformation formula, which integrates the effects of volume change. This visual representation helps clarify why different methodologies (direct substitution vs. using the Jacobian determinant formula) lead to discrepancies in the resulting densities' properties, such as their modes.

- #education.visualization, #probability.transformation-understanding, #statistics.teaching-methods

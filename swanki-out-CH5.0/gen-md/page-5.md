## What does the equation $(\mathbf{w}_{k}-\mathbf{w}_{j})^{\mathrm{T}} \mathbf{x} + (w_{k0} - w_{j0}) = 0$ represent?

This equation defines a $(D-1)$-dimensional hyperplane, acting as a decision boundary between classes $k$ and $j$.

$$
(\mathbf{w}_{k}-\mathbf{w}_{j})^{\mathrm{T}} \mathbf{x} + (w_{k0} - w_{j0}) = 0
$$

- $\mathbf{w}_{k}$ and $\mathbf{w}_{j}$ are weight vectors.
- $w_{k0}$ and $w_{j0}$ are biases.
- $\mathbf{x}$ is the input vector.

This form is similar to the two-class decision boundary, highlighting the geometric properties of linear discriminants.

- #mathematics.linear-algebra, #classification.linear-discriminant-analysis

## Explain why the decision regions of a multi-class linear discriminant are always singly connected and convex.

Based on the linearity of discriminant functions, for two points $\mathbf{x}_{\mathrm{A}}$ and $\mathbf{x}_{\mathrm{B}}$ in decision region $\mathcal{R}_{k}$, any point $\widehat{\mathbf{x}}$ on the line connecting them lies within $\mathcal{R}_{k}$. This implies:

$$
\widehat{\mathbf{x}} = \lambda \mathbf{x}_{\mathrm{A}} + (1 - \lambda) \mathbf{x}_{\mathrm{B}}, \quad 0 \leq \lambda \leq 1
$$

The linearity ensures that:

$$
y_{k}(\widehat{\mathbf{x}}) = \lambda y_{k}(\mathbf{x}_{\mathrm{A}}) + (1 - \lambda) y_{k}(\mathbf{x}_{\mathrm{B}})
$$

Since $\mathbf{x}_{\mathrm{A}}$ and $\mathbf{x}_{\mathrm{B}}$ belong to $\mathcal{R}_{k}$, $\widehat{\mathbf{x}}$ must also lie in $\mathcal{R}_{k}$, ensuring $\mathcal{R}_{k}$ is singly connected and convex.

- #mathematics.geomery, #classification.linear-discriminant-analysis

## How is 1-of-$K$ coding (or one-hot encoding) used in classification problems for $K > 2$ classes?

In 1-of-$K$ (one-hot) encoding for $K > 2$ class classification, the target variable $\mathbf{t}$ is a vector of length $K$. If the instance belongs to class $\mathcal{C}_{j}$, then $t_{j} = 1$ and all other elements $t_{k}$ are zero:

$$
\mathbf{t} = [0, 0, \ldots, 1, \ldots, 0] \quad \text{(1 at the $j$-th position)}
$$

This method differentiates each class distinctly with a unique vector representation.

- #classification.one-hot-encoding, #data-representation

## How can we interpret the target variable $t$ in a two-class classification problem?

In two-class classification, the target variable $t \in \{0,1\}$ represents class labels:

$$
t = 
\begin{cases} 
1 & \text{for class } \mathcal{C}_1 \\
0 & \text{for class } \mathcal{C}_2 
\end{cases}
$$

This binary encoding implies the probability of being in class $\mathcal{C}_1$ when $t=1$, and $\mathcal{C}_2$ when $t=0$.

- #classification.binary-encoding, #classification.probability-representation

## Derive the expression for a point $\widehat{\mathbf{x}}$ on the line connecting two points $\mathbf{x}_{\mathrm{A}}$ and $\mathbf{x}_{\mathrm{B}}$ in the same decision region.

A point $\widehat{\mathbf{x}}$ on the line connecting $\mathbf{x}_{\mathrm{A}}$ and $\mathbf{x}_{\mathrm{B}}$ in the decision region $\mathcal{R}_{k}$ can be expressed as a convex combination:

$$
\widehat{\mathbf{x}} = \lambda \mathbf{x}_{\mathrm{A}} + (1 - \lambda) \mathbf{x}_{\mathrm{B}}, \quad 0 \leq \lambda \leq 1
$$

This ensures $\widehat{\mathbf{x}}$ lies in $\mathcal{R}_{k}$, maintaining the region as singly connected and convex.

- #mathematics.linear-combination, #classification.decision-regions

## What is the form of the linear discriminant function $y_k(\mathbf{x})$ used in multiclass classification?

For multiclass classification, the linear discriminant function for class $k$ is given by:

$$
y_k(\mathbf{x}) = \mathbf{w}_k^{\mathrm{T}} \mathbf{x} + w_{k0}
$$

- $\mathbf{w}_k$ is the weight vector for class $k$.
- $w_{k0}$ is the bias term for class $k$.
- $\mathbf{x}$ is the input vector.

The class with the highest $y_k(\mathbf{x})$ value is the predicted class.

- #classification.linear-discriminant, #machine-learning.discriminant-function
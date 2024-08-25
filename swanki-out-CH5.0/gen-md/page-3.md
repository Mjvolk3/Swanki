Here are six Anki-style cards, formatted using LaTeX, based on the given text:

---

## What controls the orientation of the decision surface in a linear discriminant function?

The orientation of the decision surface is controlled by the weight vector $\mathbf{w}$, which is orthogonal to the decision surface. This is derived from the condition that for any points $\mathbf{x}_{\mathrm{A}}$ and $\mathbf{x}_{\mathrm{B}}$ lying on the decision surface:

$$
\mathbf{w}^{\mathrm{T}}(\mathbf{x}_{\mathrm{A}} - \mathbf{x}_{\mathrm{B}}) = 0
$$

This implies that $\mathbf{w}$ is orthogonal to any vector lying within the decision surface.

- .geometry, .linear-discriminant

---

## What role does the bias parameter $w_0$ play in a linear discriminant function?

The bias parameter $w_0$ determines the displacement of the decision surface from the origin. The normal distance from the origin to the decision surface is given by:

$$
\frac{\mathbf{w}^{\mathrm{T}} \mathbf{x}}{\|\mathbf{w}\|} = -\frac{w_0}{\|\mathbf{w}\|}
$$

- .geometry, .bias-parameter

---

## How do you calculate the perpendicular distance $r$ of a point $\mathbf{x}$ from the decision surface in a linear discriminant function?

The perpendicular distance $r$ of a point $\mathbf{x}$ from the decision surface is given by:

$$
r = \frac{y(\mathbf{x})}{\|\mathbf{w}\|}
$$

where $y(\mathbf{x}) = \mathbf{w}^{\mathrm{T}} \mathbf{x} + w_0$ is the signed measure of the distance.

- .geometry, .distance-calculation

---

## What is the equation for $y(\mathbf{x})$ in terms of compact notation with dummy input?

In compact notation, introducing an additional dummy input $x_0 = 1$, the equation for $y(\mathbf{x})$ is:

$$
y(\mathbf{x}) = \widetilde{\mathbf{w}}^{\mathrm{T}} \widetilde{\mathbf{x}}
$$

where $\widetilde{\mathbf{w}} = (w_0, \mathbf{w})$ and $\widetilde{\mathbf{x}} = (x_0, \mathbf{x})$.

- .geometry, .compact-notation

---

## What condition must be satisfied for points lying on the decision surface in a linear discriminant function?

For points lying on the decision surface, the condition is:

$$
y(\mathbf{x}) = 0
$$

which translates to:

$$
\mathbf{w}^{\mathrm{T}} \mathbf{x} + w_0 = 0
$$

- .geometry, #decision-surface

---

## Explain the process of finding the normal distance from the origin to the decision surface in a linear discriminant function.

To find the normal distance from the origin to the decision surface, consider a point $\mathbf{x}$ on the decision surface where $y(\mathbf{x}) = 0$. The normal distance $d$ is given by:

$$
d = \frac{\mathbf{w}^{\mathrm{T}} \mathbf{x}}{\|\mathbf{w}\|}
$$

For points on the decision surface, $\mathbf{w}^{\mathrm{T}} \mathbf{x}$ is equal to $-w_0$. Thus, the distance is:

$$
d = -\frac{w_0}{\|\mathbf{w}\|}
$$

- .geometry, .normal-distance

---

These cards include detailed contextual information and thorough explanations regarding the concepts and equations, adhering to your requirements.
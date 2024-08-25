## What does the orthonormality condition for an $M \times M$ matrix $\mathbf{U}$ imply?
The orthonormality condition for an $M \times M$ matrix $\mathbf{U}$ implies that the product of $\mathbf{U}$ and its transpose $\mathbf{U}^{\mathrm{T}}$ results in the identity matrix $\mathbf{I}$.

$$
\mathbf{U}^{\mathrm{T}} \mathbf{U} = \mathbf{I}
$$

This also means that $\mathbf{U}$ is an orthogonal matrix. Consequently, the rows and columns of $\mathbf{U}$ are orthogonal and normalized to unit length.

- #linear-algebra, #orthogonal-matrix, #eigenvectors

## How can we express any $M$-dimensional vector in terms of the eigenvectors of a matrix with $M$ eigenvalues?
Any $M$-dimensional vector can be expressed as a linear combination of the $M$ orthonormal eigenvectors of a matrix with $M$ eigenvalues. The eigenvectors form a complete set, allowing for this representation.

For a given matrix $\mathbf{A}$ with eigenvectors $\mathbf{u}_i$, an $M$-dimensional vector $\mathbf{x}$ can be expressed as:

$$
\mathbf{x} = \sum_{i=1}^{M} c_i \mathbf{u}_i
$$

where $c_i$ are coefficients.

- #linear-algebra, #eigenvectors, #vector-representation

## How is the matrix $\mathbf{A}$ diagonalized using an orthogonal matrix $\mathbf{U}$ and what does it achieve?
The matrix $\mathbf{A}$ is diagonalized using an orthogonal matrix $\mathbf{U}$ by the transformation:

$$
\mathbf{U}^{\mathrm{T}} \mathbf{A} \mathbf{U} = \boldsymbol{\Lambda}
$$

where $\boldsymbol{\Lambda}$ is a diagonal matrix with eigenvalues $\lambda_i$ on the diagonal. This transformation simplifies $\mathbf{A}$ into a diagonal form, making it easier to analyze.

- #linear-algebra, #matrix-diagonalization, #orthogonal-matrix

## How can we find the inverse of a matrix $\mathbf{A}$ using its diagonalization and an orthogonal matrix $\mathbf{U}$?
To find the inverse of a matrix $\mathbf{A}$, given its diagonal representation with an orthogonal matrix $\mathbf{U}$, we use:

$$
\mathbf{A} = \mathbf{U} \boldsymbol{\Lambda} \mathbf{U}^{\mathrm{T}}
$$

Taking the inverse, and knowing $\mathbf{U}^{-1} = \mathbf{U}^{\mathrm{T}}$, we have:

$$
\mathbf{A}^{-1} = \mathbf{U} \boldsymbol{\Lambda}^{-1} \mathbf{U}^{\mathrm{T}}
$$

This method leverages the simplified diagonal form $\boldsymbol{\Lambda}$.

- #linear-algebra, #matrix-inversion, #orthogonal-matrix

## What property of an orthogonal matrix $\mathbf{U}$ verifies that the transformation $\widetilde{\mathbf{x}} = \mathbf{U x}$ preserves vector length?
The transformation $\widetilde{\mathbf{x}} = \mathbf{U x}$ preserves vector length due to the property:

$$
\widetilde{\mathbf{x}}^{\mathrm{T}} \widetilde{\mathbf{x}} = \mathbf{x}^{\mathrm{T}} \mathbf{U}^{\mathrm{T}} \mathbf{U} \mathbf{x} = \mathbf{x}^{\mathrm{T}} \mathbf{x}
$$

This ensures that the original length of vector $\mathbf{x}$ is maintained in the transformed vector $\widetilde{\mathbf{x}}$.

- #linear-algebra, #orthogonal-transformation, #vector-length-preservation

## How does the orthogonal transformation $\widetilde{\mathbf{x}} = \mathbf{U x}$ preserve the angle between two vectors $\mathbf{x}$ and $\mathbf{y}$?
The orthogonal transformation $\widetilde{\mathbf{x}} = \mathbf{U x}$ preserves the angle between two vectors $\mathbf{x}$ and $\mathbf{y}$ through:

$$
\widetilde{\mathbf{x}}^{\mathrm{T}} \widetilde{\mathbf{y}} = \mathbf{x}^{\mathrm{T}} \mathbf{U}^{\mathrm{T}} \mathbf{U} \mathbf{y} = \mathbf{x}^{\mathrm{T}} \mathbf{y}
$$

This implies that the dot product (and thus the angle) between $\mathbf{x}$ and $\mathbf{y}$ remains unchanged after the transformation.

- #linear-algebra, #orthogonal-transformation, #angle-preservation
## Define the characteristic equation for eigenvalues $\lambda_i$.

The characteristic equation is defined as:

$$
\left|\mathbf{A}-\lambda_{i} \mathbf{I}\right|=0
$$

It is a polynomial of order $M$ in $\lambda_{i}$ and must have $M$ solutions. The rank of matrix $\mathbf{A}$ is equal to the number of non-zero eigenvalues.

- #linear-algebra, #eigenvalues.characteristic-equation


## What property do the eigenvalues of a symmetric matrix possess according to the given paper?

For symmetric matrices, the eigenvalues $\lambda_{i}$ are:

$$
\lambda_{i}^{\star}=\lambda_{i}
$$

Hence, $\lambda_{i}$ must be real.

- #linear-algebra, #symmetric-matrices.eigenvalues


## Describe the orthonormal property of eigenvectors $\mathbf{u}_i$ of a real symmetric matrix.

The eigenvectors $\mathbf{u}_{i}$ of a real symmetric matrix can be chosen to be orthonormal such that:

$$
\mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{j}=I_{i j}
$$

where $I_{i j}$ are the elements of the identity matrix $\mathbf{I}$.

- #linear-algebra, #eigenvectors.orthonormal-property


## How do you demonstrate the orthogonality of eigenvectors $\mathbf{u}_i$ and $\mathbf{u}_j$ with distinct eigenvalues?

To prove this, we consider:

$$
\mathbf{u}_{j}^{\mathrm{T}} \mathbf{A} \mathbf{u}_{i}=\lambda_{i} \mathbf{u}_{j}^{\mathrm{T}} \mathbf{u}_{i}
$$

and

$$
\mathbf{u}_{i}^{\mathrm{T}} \mathbf{A} \mathbf{u}_{j}=\lambda_{j} \mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{j}
$$

Subtracting these equations after taking the transpose, we get:

$$
\left(\lambda_{i}-\lambda_{j}\right) \mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{j}=0
$$

For $\lambda_{i} \neq \lambda_{j}$, $\mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{j} = 0$ which indicates orthogonality.

- #linear-algebra, #eigenvectors.orthogonality


## Why are the eigenvalues of symmetric matrices real?

Taking the complex conjugate and left-multiplying yields:

$$
\mathbf{u}_{i}^{\mathrm{T}} \mathbf{A} \mathbf{u}_{i}^{\star}=\lambda_{i}^{\star} \mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{i}^{\star}
$$

Due to the symmetry property $\mathbf{A}^{\mathrm{T}}=\mathbf{A}$ and using real matrices $\mathbf{A}$, we equate the left-hand sides of two equations to show $\lambda_{i}^{\star} = \lambda_{i}$, implying $\lambda_{i}$ must be real.

- #linear-algebra, #eigenvalues.real-symmetry


## What is the condition for a solution to the set of simultaneous homogeneous linear equations involving the eigenvector $\mathbf{u}_{i}$ and eigenvalue $\lambda_{i}$?

The given condition is:

$$
\left|\mathbf{A}-\lambda_{i} \mathbf{I}\right|=0
$$

This is known as the characteristic equation of the matrix $\mathbf{A}$.

- #linear-algebra, #homogeneous-equations.solution-criteria
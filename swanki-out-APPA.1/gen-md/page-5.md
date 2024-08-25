### Card 1

## What is the condition for a solution in the set of $M$ simultaneous homogeneous linear equations involving eigenvalues $\lambda_i$ and eigenvectors $\mathbf{u}_i$?

The condition for a solution in the set of $M$ simultaneous homogeneous linear equations is given by the characteristic equation:

$$
\left|\mathbf{A}-\lambda_{i} \mathbf{I}\right|=0
$$

- #linear-algebra.eigenvalues, #characteristic-equation

---

### Card 2

## In the context of eigenvalue problems, what property is unique to symmetric matrices regarding eigenvalues and eigenvectors?

For symmetric matrices $\mathbf{A}$:
- The eigenvalues $\lambda_{i}$ are always real.
- The eigenvectors $\mathbf{u}_{i}$ can be chosen to be orthonormal, i.e., $\mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{j}=I_{i j}$, where $I_{i j}$ are elements of the identity matrix $\mathbf{I}$.

- #linear-algebra.symmetric-matrices, #eigenvalues

---

### Card 3

## How can it be shown that the eigenvalues $\lambda_i$ of a symmetric real matrix are real numbers?

For a symmetric real matrix $\mathbf{A}$, the eigenvalues $\lambda_{i}$ are shown to be real by the following process:

1. Left-multiply the eigenvalue equation $\mathbf{A} \mathbf{u}_{i} = \lambda_{i} \mathbf{u}_{i}$ by $\left(\mathbf{u}_{i}^{\star}\right)^{\mathrm{T}}$ (where $\star$ denotes complex conjugate):

   $$
   \left(\mathbf{u}_{i}^{\star}\right)^{\mathrm{T}} \mathbf{A} \mathbf{u}_{i}=\lambda_{i}\left(\mathbf{u}_{i}^{\star}\right)^{\mathrm{T}} \mathbf{u}_{i}
   $$

2. Take the complex conjugate of $\mathbf{A} \mathbf{u}_{i} = \lambda_{i} \mathbf{u}_{i}$ and left-multiply by $\mathbf{u}_{i}^{\mathrm{T}}$:

   $$
   \mathbf{u}_{i}^{\mathrm{T}} \mathbf{A} \mathbf{u}_{i}^{\star}=\lambda_{i}^{\star} \mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{i}^{\star}
   $$

Since $\mathbf{A}$ is symmetric, it implies $\mathbf{A}=\mathbf{A}^{\mathrm{T}}$ and $\mathbf{A}^{\star}=\mathbf{A}$. Hence, $\lambda_{i}^{\star}=\lambda_{i}$, proving that $\lambda_{i}$ is real.

- #linear-algebra.eigenvalues, #proof.real-eigenvalues

---

### Card 4

## Explain why the rank of matrix $\mathbf{A}$ is related to the number of non-zero eigenvalues. 

The rank of a matrix $\mathbf{A}$ is equal to the number of non-zero eigenvalues because the rank is defined as the dimension of the column space (or row space) of $\mathbf{A}$, which corresponds to the number of linearly independent rows or columns. Non-zero eigenvalues indicate linearly independent eigenvectors, contributing to the rank of $\mathbf{A}$.

- #linear-algebra.rank, #eigenvalues

---

### Card 5

## Using the symmetry property of $\mathbf{A}$, derive that $\mathbf{u}_{i}$ and $\mathbf{u}_{j}$ are orthogonal for $\lambda_{i} \neq \lambda_{j}$.

To show that $\mathbf{u}_{i}$ and $\mathbf{u}_{j}$ are orthogonal for $\lambda_{i} \neq \lambda_{j}$ for a symmetric matrix $\mathbf{A}$:

1. Left-multiply $\mathbf{A} \mathbf{u}_{i} = \lambda_{i} \mathbf{u}_{i}$ by $\mathbf{u}_{j}^{\mathrm{T}}$:

   $$
   \mathbf{u}_{j}^{\mathrm{T}} \mathbf{A} \mathbf{u}_{i}=\lambda_{i} \mathbf{u}_{j}^{\mathrm{T}} \mathbf{u}_{i}
   $$

2. Similarly, left-multiply $\mathbf{A} \mathbf{u}_{j} = \lambda_{j} \mathbf{u}_{j}$ by $\mathbf{u}_{i}^{\mathrm{T}}$:

   $$
   \mathbf{u}_{i}^{\mathrm{T}} \mathbf{A} \mathbf{u}_{j}=\lambda_{j} \mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{j}
   $$

3. Taking the transpose of the second equation and using the symmetry property $\mathbf{A}^{\mathrm{T}} = \mathbf{A}$, subtract the equations:

   $$
   \left(\lambda_{i}-\lambda_{j}\right) \mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{j}=0
   $$

For $\lambda_{i} \neq \lambda_{j}$, $\mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{j}=0$, implying $\mathbf{u}_{i}$ and $\mathbf{u}_{j}$ are orthogonal.

- #linear-algebra.eigenvectors, #proof.orthogonal

---

### Card 6

## What happens to eigenvectors $\mathbf{u}_{i}$ and $\mathbf{u}_{j}$ if their corresponding eigenvalues $\lambda_{i}$ and $\lambda_{j}$ are equal?

If the eigenvalues $\lambda_{i}$ and $\lambda_{j}$ of a symmetric matrix are equal, then any linear combination $\alpha \mathbf{u}_{i} + \beta \mathbf{u}_{j}$ is also an eigenvector corresponding to that eigenvalue. This is due to the fact that the eigenspace associated with a specific eigenvalue may have more than one dimension, allowing for linear combinations.

- #linear-algebra.eigenvectors, #eigenspace
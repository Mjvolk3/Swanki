with the same eigenvalue, so we can select one linear combination arbitrarily, and then choose the second to be orthogonal to the first (it can be shown that the degenerate eigenvectors are never linearly dependent). Hence, the eigenvectors can be chosen to be orthogonal, and by normalizing can be set to unit length. Because there are $M$ eigenvalues, the corresponding $M$ orthogonal eigenvectors form a complete set and so any $M$-dimensional vector can be expressed as a linear combination of the eigenvectors.

We can take the eigenvectors $\mathbf{u}_{i}$ to be the columns of an $M \times M$ matrix $\mathbf{U}$, which from orthonormality satisfies

$$
\mathbf{U}^{\mathrm{T}} \mathbf{U}=\mathbf{I}
$$

Such a matrix is said to be orthogonal. Interestingly, the rows of this matrix are also orthogonal, so that $\mathbf{U} \mathbf{U}^{\mathrm{T}}=\mathbf{I}$. To show this, note that (A.37) implies $\mathbf{U}^{\mathrm{T}} \mathbf{U U}^{-1}=$ $\mathbf{U}^{-1}=\mathbf{U}^{\mathrm{T}}$ and so $\mathbf{U U}^{-1}=\mathbf{U U}^{\mathrm{T}}=\mathbf{I}$. Using (A.12), it also follows that $|\mathbf{U}|=1$.

The eigenvector equation (A.29) can be expressed in terms of $\mathbf{U}$ in the form

$$
\mathbf{A U}=\mathbf{U} \boldsymbol{\Lambda}
$$

where $\boldsymbol{\Lambda}$ is an $M \times M$ diagonal matrix whose diagonal elements are given by the eigenvalues $\lambda_{i}$.

If we consider a column vector $\mathrm{x}$ that is transformed by an orthogonal matrix $\mathbf{U}$ to give a new vector

$$
\widetilde{\mathbf{x}}=\mathbf{U x}
$$

then the length of the vector is preserved because

$$
\widetilde{\mathbf{x}}^{\mathrm{T}} \widetilde{\mathbf{x}}=\mathbf{x}^{\mathrm{T}} \mathbf{U}^{\mathrm{T}} \mathbf{U} \mathbf{x}=\mathbf{x}^{\mathrm{T}} \mathbf{x}
$$

and similarly the angle between any two such vectors is preserved because

$$
\widetilde{\mathbf{x}}^{\mathrm{T}} \widetilde{\mathbf{y}}=\mathbf{x}^{\mathrm{T}} \mathbf{U}^{\mathrm{T}} \mathbf{U} \mathbf{y}=\mathbf{x}^{\mathrm{T}} \mathbf{y}
$$

Thus, multiplication by $\mathbf{U}$ can be interpreted as a rigid rotation of the coordinate system.

From (A.38), it follows that

$$
\mathbf{U}^{\mathrm{T}} \mathbf{A} \mathbf{U}=\boldsymbol{\Lambda}
$$

and because $\boldsymbol{\Lambda}$ is a diagonal matrix, we say that the matrix $\mathbf{A}$ is diagonalized by the matrix U. If we left-multiply by $\mathbf{U}$ and right-multiply by $\mathbf{U}^{\mathrm{T}}$, we obtain

$$
\mathbf{A}=\mathbf{U} \boldsymbol{\Lambda} \mathbf{U}^{\mathrm{T}}
$$

Taking the inverse of this equation and using (A.3) together with $\mathbf{U}^{-1}=\mathbf{U}^{\mathrm{T}}$, we have

$$
\mathbf{A}^{-1}=\mathbf{U} \boldsymbol{\Lambda}^{-1} \mathbf{U}^{\mathrm{T}}
$$
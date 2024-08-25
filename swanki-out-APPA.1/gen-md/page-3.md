## What is the determinant of a $2 \times 2$ matrix given by, and how is it expressed?

The determinant of a $2 \times 2$ matrix is given by the product of the elements on the leading diagonal minus the product of the off-diagonal elements. For a matrix 

$$
\mathbf{A} = \begin{pmatrix}
a_{11} & a_{12} \\
a_{21} & a_{22}
\end{pmatrix},
$$

the determinant is 

$$
|\mathbf{A}| = a_{11} a_{22} - a_{12} a_{21}.
$$

- #linear-algebra.determinants, #matrix-algebra

## How is the determinant of a product of two matrices defined?

The determinant of a product of two matrices $\mathbf{A}$ and $\mathbf{B}$ is given by the product of their determinants:

$$
|\mathbf{A B}| = |\mathbf{A}| |\mathbf{B}|.
$$

This property ensures that the determinants multiply in a similar manner to scalar multiplication.

- #linear-algebra.determinants, #matrix-algebra

## What is the determinant of an inverse matrix given by?

The determinant of an inverse matrix $\mathbf{A}^{-1}$ is the reciprocal of the determinant of the matrix $\mathbf{A}$. Specifically, if $\mathbf{A}$ is invertible, then

$$
|\mathbf{A}^{-1}| = \frac{1}{|\mathbf{A}|}.
$$

This results from the property that the product of a matrix and its inverse is the identity matrix, whose determinant is 1.

- #linear-algebra.determinants, #matrix-algebra

## What important identity involving determinants holds when $\mathbf{A}$ and $\mathbf{B}$ are matrices of size $N \times M$?

When $\mathbf{A}$ and $\mathbf{B}$ are matrices of size $N \times M$, the following identity holds:

$$
\left|\mathbf{I}_N + \mathbf{A} \mathbf{B}^{\mathrm{T}}\right| = \left|\mathbf{I}_M + \mathbf{A}^{\mathrm{T}} \mathbf{B}\right|.
$$

This identity is useful in simplifying the manipulation and comparison of determinants in matrix algebra.

- #linear-algebra.determinants, #matrix-identity

## What is a useful special case of the determinant identity when $\mathbf{a}$ and $\mathbf{b}$ are $N$-dimensional column vectors?

A useful special case of the determinant identity is when $\mathbf{a}$ and $\mathbf{b}$ are $N$-dimensional column vectors. The identity simplifies to:

$$
\left|\mathbf{I}_N + \mathbf{a b}^{\mathrm{T}}\right| = 1 + \mathbf{a}^{\mathrm{T}} \mathbf{b}.
$$

This result connects the determinant of certain rank-1 updates to the dot product of vectors.

- #linear-algebra.determinants, #matrix-identity

## What is the derivative of a vector $\mathbf{a}$ with respect to a scalar $x$?

The derivative of a vector $\mathbf{a}$ with respect to a scalar $x$ is a vector where each component is the partial derivative of the corresponding component of $\mathbf{a}$ with respect to $x$:

$$
\left(\frac{\partial \mathbf{a}}{\partial x}\right)_i = \frac{\partial a_i}{\partial x}.
$$

This component-wise definition extends to matrices analogously.

- #calculus, #matrix-derivatives
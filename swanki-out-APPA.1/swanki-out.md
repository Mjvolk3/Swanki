## Explain the identity $\mathbf{A} \mathbf{A}^{-1}=\mathbf{I}$ in matrix algebra.

The equation $\mathbf{A} \mathbf{A}^{-1}$ represents the product of a matrix $\mathbf{A}$ and its inverse $\mathbf{A}^{-1}$. This product equals the identity matrix $\mathbf{I}$.

$$
\mathbf{A} \mathbf{A}^{-1} = \mathbf{A}^{-1} \mathbf{A} = \mathbf{I}
$$

Here, $\mathbf{A}^{-1}$ is defined as the matrix that, when multiplied by $\mathbf{A}$, yields the identity matrix $\mathbf{I}$. The identity matrix serves as the multiplicative identity in matrix algebra, meaning that any matrix multiplied by the identity matrix remains unchanged. The requirement that $\mathbf{A}$ has an inverse implies that it is a square matrix (same number of rows and columns) and is non-singular (its determinant is non-zero).

- #math, #linear-algebra.matrix-inverse

## Verify the transpose property $(\mathbf{A B})^{\mathrm{T}} = \mathbf{B}^{\mathrm{T}} \mathbf{A}^{\mathrm{T}}$

The property of matrix transpose for the product of two matrices states that the transpose of the product is equal to the product of their transposes in reverse order.

$$
(\mathbf{A B})^{\mathrm{T}} = \mathbf{B}^{\mathrm{T}} \mathbf{A}^{\mathrm{T}}
$$

To verify this, consider the elements of the product matrix $(\mathbf{A B})$, which are given by the summation:

$$
(\mathbf{A B})_{ij} = \sum_{k} A_{ik} B_{kj}
$$

Taking the transpose of $\mathbf{A B}$, we switch rows and columns:

$$
(\mathbf{A B})^{\mathrm{T}}_{ij} = (\mathbf{A B})_{ji} = \sum_{k} A_{jk} B_{ki}
$$

By definition of matrix transpose for individual matrices, we have:

$$
(\mathbf{B}^{\mathrm{T}} \mathbf{A}^{\mathrm{T}})_{ij} = \sum_{k} (\mathbf{B}^{\mathrm{T}})_{ik} (\mathbf{A}^{\mathrm{T}})_{kj} = \sum_{k} B_{ki} A_{jk}
$$

Hence, 

$$
(\mathbf{A B})^{\mathrm{T}}_{ij} = (\mathbf{B}^{\mathrm{T}} \mathbf{A}^{\mathrm{T}})_{ij}
$$

which confirms the identity.

- #math, #linear-algebra.matrix-transpose

## Show the identity $(\mathbf{A B})^{-1} = \mathbf{B}^{-1} \mathbf{A}^{-1}$.

The inverse of the matrix product $\mathbf{A B}$ is given by the product of their individual inverses in reverse order:

$$
(\mathbf{A B})^{-1} = \mathbf{B}^{-1} \mathbf{A}^{-1}
$$

To show this, consider multiplying both sides by $\mathbf{A B}$:

$$
\mathbf{A B} (\mathbf{A B})^{-1} = \mathbf{A B} (\mathbf{B}^{-1} \mathbf{A}^{-1})
$$

Using the associative property of matrix multiplication, we get:

$$
\mathbf{A} (\mathbf{B} \mathbf{B}^{-1}) \mathbf{A}^{-1} = \mathbf{A} \mathbf{I} \mathbf{A}^{-1} = \mathbf{A} \mathbf{A}^{-1} = \mathbf{I}
$$

Thus, 

$$
\mathbf{A B} (\mathbf{B}^{-1} \mathbf{A}^{-1}) = \mathbf{I}
$$

indicating that $(\mathbf{A B})^{-1} = \mathbf{B}^{-1} \mathbf{A}^{-1}$.
 
- #math, #linear-algebra.matrix-inverse

## Derive the property $(\mathbf{A}^{\mathrm{T}})^{-1} = (\mathbf{A}^{-1})^{\mathrm{T}}$.

The inverse of the transpose of a matrix $\mathbf{A}$ is equal to the transpose of the inverse of $\mathbf{A}$:

$$
\left(\mathbf{A}^{\mathrm{T}}\right)^{-1}=\left(\mathbf{A}^{-1}\right)^{\mathrm{T}}
$$

To derive this property, consider the transpose of $\mathbf{A}^{-1}$, denoted as $(\mathbf{A}^{-1})^{\mathrm{T}}$. By definition, $\mathbf{A}^{-1}$ satisfies:

$$
\mathbf{A} \mathbf{A}^{-1} = \mathbf{I}
$$

Taking the transpose on both sides:

$$
(\mathbf{A} \mathbf{A}^{-1})^{\mathrm{T}} = \mathbf{I}^{\mathrm{T}} = \mathbf{I}
$$

Using the property of transposition for products of matrices:

$$
(\mathbf{A}^{-1})^{\mathrm{T}} (\mathbf{A})^{\mathrm{T}} = \mathbf{I}
$$

Thus, $(\mathbf{A}^{-1})^{\mathrm{T}}$ is the inverse of $\mathbf{A}^{\mathrm{T}}$, proving the identity:

$$
(\mathbf{A}^{\mathrm{T}})^{-1} = (\mathbf{A}^{-1})^{\mathrm{T}}
$$

- #math, #linear-algebra.matrix-inverse

## Define the identity matrix $\mathbf{I}$ and its role in linear algebra.

The identity matrix, denoted by $\mathbf{I}_{N}$ for an $N \times N$ matrix, is a special kind of matrix where all the diagonal elements are $1$ and all off-diagonal elements are $0$.

$$
\mathbf{I}_N = \begin{pmatrix}
1 & 0 & \cdots & 0 \\
0 & 1 & \cdots & 0 \\
\vdots & \vdots & \ddots & \vdots \\
0 & 0 & \cdots & 1
\end{pmatrix}
$$

In linear algebra, the identity matrix acts as the multiplicative identity in matrix multiplication, meaning that for any matrix $\mathbf{A}$, the following holds:

$$
\mathbf{A} \mathbf{I} = \mathbf{I} \mathbf{A} = \mathbf{A}
$$

This property is crucial for defining the inverse of a matrix $\mathbf{A}$,  $\mathbf{A}^{-1}$, as it satisfies the equation:

$$
\mathbf{A} \mathbf{A}^{-1} = \mathbf{A}^{-1} \mathbf{A} = \mathbf{I}
$$

- #math, #linear-algebra.matrix-identity

## Explain the notation $\left(\mathbf{A}^{\mathrm{T}}\right)_{ij} = A_{ji}$ and its relevance.

The notation $\left(\mathbf{A}^{\mathrm{T}}\right)_{ij} = A_{ji}$ indicates that the element at the $(i,j)$ position of the transpose matrix $\mathbf{A}^{\mathrm{T}}$ is the same as the element in the $(j,i)$ position of the original matrix $\mathbf{A}$.

Given a matrix $\mathbf{A}$ with elements $A_{ij}$, the transpose $\mathbf{A}^{\mathrm{T}}$ is obtained by flipping $\mathbf{A}$ over its diagonal, so that:

$$
\left(\mathbf{A}^{\mathrm{T}}\right)_{ij} = A_{ji}
$$

This operation is crucial in numerous mathematical contexts and applications, such as solving systems of linear equations, eigenvalue problems, and in various properties and identities involving products, inverses, and determinants of matrices.

- #math, #linear-algebra.matrix-transpose

### Anki Card 1

![](https://cdn.mathpix.com/cropped/2024_05_27_25fa23d4d21ea443ccefg-1.jpg?height=44&width=544&top_left_y=1888&top_left_x=412)

What is the relationship between the transpose of a product of two matrices $(\mathbf{A B})$ and the transposes of the matrices $\mathbf{A}$ and $\mathbf{B}$?

%

The relationship is given by:

$$
(\mathbf{A B})^{\mathrm{T}} = \mathbf{B}^{\mathrm{T}} \mathbf{A}^{\mathrm{T}}
$$

This can be verified by writing out the indices.

- #linear-algebra, #matrices.transpose, #products

### Anki Card 2

![](https://cdn.mathpix.com/cropped/2024_05_27_25fa23d4d21ea443ccefg-1.jpg?height=44&width=544&top_left_y=1888&top_left_x=412)

What are the properties of the inverse of a product of two matrices $(\mathbf{A B})$ and the transpose of the inverse of a matrix $\mathbf{A}$?

%

The properties are given by:

$$
(\mathbf{A B})^{-1} = \mathbf{B}^{-1} \mathbf{A}^{-1}
$$

and

$$
\left(\mathbf{A}^{\mathrm{T}}\right)^{-1} = \left(\mathbf{A}^{-1}\right)^{\mathrm{T}}
$$

- #linear-algebra, #matrices.inverse, #properties

## A question or demand. The front side of the card
  
![](https://cdn.mathpix.com/cropped/2024_05_27_25fa23d4d21ea443ccefg-1.jpg?height=44&width=544&top_left_y=1888&top_left_x=412)

%

What is the definition of the transpose and the inverse of a matrix as given in the context?

%

The transpose of a matrix $\mathbf{A}$, denoted $\mathbf{A}^{\mathrm{T}}$, has elements $\left(\mathbf{A}^{\mathrm{T}}\right)_{ij} = A_{ji}$. The inverse of matrix $\mathbf{A}$, denoted $\mathbf{A}^{-1}$, satisfies

$$
\mathbf{A} \mathbf{A}^{-1} = \mathbf{A}^{-1} \mathbf{A} = \mathbf{I}
$$

- linear-algebra, matrices.transposition, matrices.inversion

## A question or demand. The front side of the card
    
![](https://cdn.mathpix.com/cropped/2024_05_27_25fa23d4d21ea443ccefg-1.jpg?height=44&width=544&top_left_y=1888&top_left_x=412)
    
%

What are the properties of transposes and inverses of matrices when multiplied as given in the context?

%

The properties of transposes and inverses of matrix multiplication are:

$$
(\mathbf{A B})^{\mathrm{T}} = \mathbf{B}^{\mathrm{T}} \mathbf{A}^{\mathrm{T}}
$$

$$
(\mathbf{A B})^{-1} = \mathbf{B}^{-1} \mathbf{A}^{{-1}}
$$

$$
\left( \mathbf{A}^{\mathrm{T}} \right)^{-1} = \left( \mathbf{A}^{-1} \right)^{\mathrm{T}}
$$

- linear-algebra, matrices.properties, matrices.inverse

## Matrix inverse identity involving $ \mathbf{P}, \mathbf{B}, \mathbf{R}$

Describe the useful matrix identity involving $ \mathbf{P}, \mathbf{B}, \mathbf{R}$ and its verification process.

The identity is given by:

$$
\left(\mathbf{P}^{-1}+\mathbf{B}^{\mathrm{T}} \mathbf{R}^{-1} \mathbf{B}\right)^{-1} \mathbf{B}^{\mathrm{T}} \mathbf{R}^{-1}=\mathbf{P B}^{\mathrm{T}}\left(\mathbf{B} \mathbf{P} \mathbf{B}^{\mathrm{T}}+\mathbf{R}\right)^{-1}
$$

To verify, right-multiply both sides by $\left(\mathbf{B P B}^{\mathrm{T}}+\mathbf{R}\right)$.

- #linear-algebra, #matrix-identities

---

## The Woodbury identity

State and explain the Woodbury identity, including the context in which it is useful.

The Woodbury identity is given by:

$$
\left(\mathbf{A}+\mathbf{B D}^{-1} \mathbf{C}\right)^{-1}=\mathbf{A}^{-1}-\mathbf{A}^{-1} \mathbf{B}\left(\mathbf{D}+\mathbf{C A}^{-1} \mathbf{B}\right)^{-1} \mathbf{C A}^{-1}
$$

This identity is particularly useful when $\mathbf{A}$ is large and diagonal (and hence easy to invert), and when $\mathbf{B}$ has many rows but few columns (and conversely for $\mathbf{C}$).

- #linear-algebra, #matrix-identities.woodbury-identity

---

## Linear independence definition

Define linear independence for a set of vectors $\{ \mathbf{a}_{1}, \ldots, \mathbf{a}_{N} \}$.

A set of vectors $\{ \mathbf{a}_{1}, \ldots, \mathbf{a}_{N} \}$ is said to be linearly independent if the relation $\sum_{n} \alpha_{n} \mathbf{a}_{n}=0$ holds only if all $\alpha_{n}=0$. This implies that none of the vectors can be expressed as a linear combination of the remainder.

- #linear-algebra, #vector-spaces.linear-independence

---

## Matrix rank explanation

Explain the rank of a matrix.

The rank of a matrix is the maximum number of linearly independent rows (or equivalently the maximum number of linearly independent columns).

- #linear-algebra, #matrix-properties.rank

---

## Trace operator's cyclic property

Explain the cyclic property of the trace operator for matrices $\mathbf{A}, \mathbf{B}, \mathbf{C}$.

The cyclic property of the trace operator is given by:

$$
\operatorname{Tr}(\mathbf{A B C})=\operatorname{Tr}(\mathbf{C A B})=\operatorname{Tr}(\mathbf{B C A})
$$

This property extends to the product of any number of matrices.

- #linear-algebra, #matrix-properties.trace

---

## Determinant definition for an $N \times N$ matrix

Define the determinant $|\mathbf{A}|$ of an $N \times N$ matrix $\mathbf{A}$.

The determinant $|\mathbf{A}|$ is defined by:

$$
|\mathbf{A}|=\sum( \pm 1) A_{1 i_{1}} A_{2 i_{2}} \cdots A_{N i_{N}}
$$

where the sum is taken over all products consisting of precisely one element from each row and one element from each column, with a coefficient +1 or -1 according to whether the permutation $i_{1} i_{2} \ldots i_{N}$ is even or odd, respectively.

- #linear-algebra, #matrix-properties.determinant

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

## Differentiate the product of two matrices with respect to a variable \( x \).

Using the product rule of derivatives, express the differentiation of the product of two matrices \( \mathbf{A} \) and \( \mathbf{B} \) with respect to a variable \( x \).

$$
\frac{\partial}{\partial x}(\mathbf{A B}) = \frac{\partial \mathbf{A}}{\partial x} \mathbf{B} + \mathbf{A} \frac{\partial \mathbf{B}}{\partial x}
$$

- #calculus, #linear-algebra.matrix-differentiation


## Differentiate the inverse of a matrix with respect to a variable \( x \).

How do you express the differentiation of the inverse of a matrix \( \mathbf{A} \) with respect to a variable \( x \)?

$$
\frac{\partial}{\partial x}\left(\mathbf{A}^{-1}\right)=-\mathbf{A}^{-1} \frac{\partial \mathbf{A}}{\partial x} \mathbf{A}^{-1} 
$$

- #calculus, #linear-algebra.matrix-differentiation


## Prove $\frac{\partial}{\partial x}\left(\mathbf{A}^{-1}\right)=-\mathbf{A}^{-1} \frac{\partial \mathbf{A}}{\partial x} \mathbf{A}^{-1}$.

Given $\mathbf{A}^{-1} \mathbf{A}=\mathbf{I}$, differentiate this equation and show that the derivative of the inverse of a matrix can be expressed as $\frac{\partial}{\partial x}\left(\mathbf{A}^{-1}\right)=-\mathbf{A}^{-1} \frac{\partial \mathbf{A}}{\partial x} \mathbf{A}^{-1}$.

%
Differentiating $\mathbf{A}^{-1} \mathbf{A}=\mathbf{I}$ with respect to \( x \):

$$
\frac{\partial}{\partial x}(\mathbf{A}^{-1} \mathbf{A}) = \frac{\partial \mathbf{A}^{-1}}{\partial x}\mathbf{A} + \mathbf{A}^{-1} \frac{\partial \mathbf{A}}{\partial x} = 0
$$

We then isolate $\frac{\partial \mathbf{A}^{-1}}{\partial x}$:

$$
\frac{\partial \mathbf{A}^{-1}}{\partial x} \mathbf{A} = - \mathbf{A}^{-1} \frac{\partial \mathbf{A}}{\partial x}
$$

Finally, right-multiplying both sides by $\mathbf{A}^{-1}$, we get:

$$
\frac{\partial \mathbf{A}^{-1}}{\partial x} = - \mathbf{A}^{-1} \frac{\partial \mathbf{A}}{\partial x} \mathbf{A}^{-1}
$$

- #calculus, #linear-algebra.matrix-differentiation


## Trace of a product differentiation with respect to a matrix element.

If we choose $x$ to be one of the elements of $\mathbf{A}$, how can we express the differentiation of the trace of product $\mathbf{A B}$ with respect to $A_{ij}$?

$$
\frac{\partial}{\partial A_{i j}} \operatorname{Tr}(\mathbf{A B}) = B_{j i} 
$$

- #calculus, #linear-algebra.matrix-differentiation


## Properties of the trace differentiation with respect to a matrix.

What are the properties of differentiating the trace of certain matrix expressions with respect to a matrix \( \mathbf{A} \)?

$$
\begin{aligned}
\frac{\partial}{\partial \mathbf{A}} \operatorname{Tr}\left(\mathbf{A}^{\mathrm{T}} \mathbf{B}\right) & =\mathbf{B} \\
\frac{\partial}{\partial \mathbf{A}} \operatorname{Tr}(\mathbf{A}) & =\mathbf{I} \\
\frac{\partial}{\partial \mathbf{A}} \operatorname{Tr}\left(\mathbf{A B} \mathbf{A}^{\mathrm{T}}\right) & =\mathbf{A}\left(\mathbf{B} + \mathbf{B}^{\mathrm{T}}\right)
\end{aligned}
$$

- #calculus, #linear-algebra.traces


## Eigenvector equation for a square matrix.

For a square matrix $\mathbf{A}$ of size $M \times M$, what is the eigenvector equation?

$$
\mathbf{A} \mathbf{u}_{i} = \lambda_{i} \mathbf{u}_{i} 
$$

where \( \mathbf{u}_{i} \) is the eigenvector and \( \lambda_{i} \) is the corresponding eigenvalue.

- #linear-algebra, #eigenvectors.matrix-equation

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

Here are six Anki cards based on the provided text chunk, focusing on the scientific details and mathematical equations:

### Card 1

Given a context where we have $M$ orthogonal eigenvectors corresponding to $M$ eigenvalues, how can any $M$-dimensional vector be represented?

Any $M$-dimensional vector can be expressed as a linear combination of the $M$ orthogonal eigenvectors. 

- #linear-algebra, #eigenvectors.representation

### Card 2

What does the equation $\mathbf{U} \mathbf{U}^{\mathrm{T}} = \mathbf{I}$ indicate about the matrix $\mathbf{U}$?

The equation $\mathbf{U} \mathbf{U}^{\mathrm{T}} = \mathbf{I}$ indicates that the matrix $\mathbf{U}$ is an orthogonal matrix. This implies that both the rows and columns of $\mathbf{U}$ are orthonormal vectors.

- #linear-algebra, #matrices.orthogonal

### Card 3

Express the eigenvector equation in matrix form using $\mathbf{U}$ and the eigenvalue matrix $\boldsymbol{\Lambda}$.

$$
\mathbf{A U} = \mathbf{U} \boldsymbol{\Lambda}
$$

Here, $\mathbf{A}$ is the original matrix, $\mathbf{U}$ is the orthogonal matrix formed by eigenvectors, and $\boldsymbol{\Lambda}$ is the diagonal matrix containing eigenvalues.

- #linear-algebra, #eigenvalues.eigenvectors

### Card 4

What transformation does the orthogonal matrix $\mathbf{U}$ perform on a vector $\mathbf{x}$, and how does it affect the length and angle of the vector?

The orthogonal matrix $\mathbf{U}$ transforms the vector $\mathbf{x}$ into a new vector $\widetilde{\mathbf{x}}=\mathbf{U} \mathbf{x}$. This transformation preserves the length of the vector and the angle between any two vectors. Specifically:

$$
\widetilde{\mathbf{x}}^{\mathrm{T}} \widetilde{\mathbf{x}} = \mathbf{x}^{\mathrm{T}} \mathbf{U}^{\mathrm{T}} \mathbf{U} \mathbf{x} = \mathbf{x}^{\mathrm{T}} \mathbf{x}
$$

$$
\widetilde{\mathbf{x}}^{\mathrm{T}} \widetilde{\mathbf{y}} = \mathbf{x}^{\mathrm{T}} \mathbf{U}^{\mathrm{T}} \mathbf{U} \mathbf{y} = \mathbf{x}^{\mathrm{T}} \mathbf{y}
$$

Thus, $\mathbf{U}$ performs a rigid rotation of the coordinate system.

- #linear-algebra, #transformations.orthogonal

### Card 5

When we diagonalize a matrix $\mathbf{A}$ using an orthogonal matrix $\mathbf{U}$, what equation do we obtain?

If we diagonalize a matrix $\mathbf{A}$ using an orthogonal matrix $\mathbf{U}$, we obtain:

$$
\mathbf{A} = \mathbf{U} \boldsymbol{\Lambda} \mathbf{U}^{\mathrm{T}}
$$

where $\boldsymbol{\Lambda}$ is a diagonal matrix containing the eigenvalues of $\mathbf{A}$.

- #linear-algebra, #matrices.diagonalization

### Card 6

What is the equation for the inverse of matrix $\mathbf{A}$ when it is diagonalized by $\mathbf{U}$ and $\boldsymbol{\Lambda}$, and what properties do we use?

For the inverse of $\mathbf{A}$ when it is diagonalized by $\mathbf{U}$ and $\boldsymbol{\Lambda}$, we use the equation:

$$
\mathbf{A}^{-1} = \mathbf{U} \boldsymbol{\Lambda}^{-1} \mathbf{U}^{\mathrm{T}}
$$

The properties used here include $\mathbf{U}^{-1} = \mathbf{U}^{\mathrm{T}}$ due to the orthogonality of $\mathbf{U}$.

- #linear-algebra, #matrices.inverse

## Given the matrix $\mathbf{A}$, what is the formula to represent it in terms of its eigenvalues $\lambda_i$ and corresponding eigenvectors $\mathbf{u}_i$? How can you represent the inverse of $\mathbf{A}$ in a similar form?

\[
\begin{aligned}
\mathbf{A} & =\sum_{i=1}^{M} \lambda_{i} \mathbf{u}_{i} \mathbf{u}_{i}^{\mathrm{T}} \\
\mathbf{A}^{-1} & =\sum_{i=1}^{M} \frac{1}{\lambda_{i}} \mathbf{u}_{i} \mathbf{u}_{i}^{\mathrm{T}}
\end{aligned}
\]

In these equations, $\mathbf{A}$ is described in terms of summation over its eigenvalues $\lambda_i$ and the outer product of its eigenvectors $\mathbf{u}_i$. The inverse of $\mathbf{A}$ follows a similar structure but inversely weights each term by $\frac{1}{\lambda_i}$. 

- #matrix-theory, #eigenvalues, #eigenvectors


## What is the result when you take the determinant of matrix $\mathbf{A}$, expressed as $\mathbf{A} = \sum_{i=1}^{M} \lambda_{i} \mathbf{u}_{i} \mathbf{u}_{i}^{\mathrm{T}}$?

$$
|\mathbf{A}|=\prod_{i=1}^{M} \lambda_{i}
$$

Taking the determinant of matrix $\mathbf{A}$ reveals that it is the product of its eigenvalues, $\lambda_i$. This stems from the property of determinants in eigen-decomposition.

- #determinants, #matrix-theory


## Explain how to obtain the trace of the matrix $\mathbf{A}$ using its eigenvalues $\lambda_i$.

$$
\operatorname{Tr}(\mathbf{A})=\sum_{i=1}^{M} \lambda_{i}
$$

The trace of matrix $\mathbf{A}$ is the sum of its eigenvalues. This outcome comes from the cyclic property of the trace operator and the fact that $\mathbf{U}^{\mathrm{T}} \mathbf{U}=\mathbf{I}$ where $\mathbf{U}$ is the matrix of eigenvectors.

- #trace-operator, #matrix-theory


## What defines a matrix $\mathbf{A}$ as positive definite, and how is this related to its eigenvalues $\lambda_i$?

A matrix $\mathbf{A}$ is said to be positive definite, denoted by $\mathbf{A} \succ 0$, if $\mathbf{w}^{\mathrm{T}} \mathbf{A w}>0$ for all non-zero values of vector $\mathbf{w}$. This is equivalently ensured if all eigenvalues $\lambda_i$ are greater than zero.

Positive definiteness of a matrix ensures that all its eigenvalues are positive, ensuring $\mathbf{A}\mathbf{w}$ does not invert the direction of $\mathbf{w}$ for any non-zero $\mathbf{w}$. An arbitrary vector $\mathbf{w}$ can be expressed as a linear combination of eigenvectors.

- #positive-definiteness, #eigenvalues

## What does it mean for a matrix to be positive semidefinite and how is it different from being positive definite?

A matrix is said to be positive semidefinite if $\mathbf{w}^{\mathrm{T}} \mathbf{A} \mathbf{w} \geqslant 0$ for all vectors $\mathbf{w}$, denoted $\mathbf{A} \succeq 0$, and this is equivalent to all eigenvalues $\lambda_i$ being nonnegative.

A positive semidefinite matrix allows zero eigenvalues while a positive definite matrix does not. The matrix retains some properties (like not inverting the direction of $\mathbf{w}$), but may map some vectors to zero (if they are eigenvectors corresponding to zero eigenvalues).

- #positive-semi-definiteness, #eigenvalues

## What is the condition number of a matrix and how is it calculated using its eigenvalues?

The condition number $\mathrm{CN}$ of a matrix is given by

$$
\mathrm{CN}=\left(\frac{\lambda_{\max }}{\lambda_{\min }}\right)^{1 / 2}
$$

where $\lambda_{\max }$ is the largest eigenvalue and $\lambda_{\min }$ is the smallest eigenvalue. 

The condition number indicates how sensitive the matrix is to small changes; larger values suggest greater sensitivity or ill-conditioning.

- #condition-number, #matrix-stability


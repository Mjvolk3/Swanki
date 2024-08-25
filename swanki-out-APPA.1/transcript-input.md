\title{
Appendix A. Linear Algebra
}

In this appendix, we gather together some useful properties and identities involving matrices and determinants. This is not intended to be an introductory tutorial, and it is assumed that the reader is already familiar with basic linear algebra. For some results, we indicate how to prove them, whereas in more complex cases we leave the interested reader to refer to standard textbooks on the subject. In all cases, we assume that inverses exist and that matrix dimensions are such that the formulae are correctly defined. A comprehensive discussion of linear algebra can be found in Golub and Van Loan (1996), and an extensive collection of matrix properties is given by Lütkepohl (1996). Matrix derivatives are discussed in Magnus and Neudecker $(1999)$.

\section*{A.1. Matrix Identities}

A matrix A has elements $A_{i j}$ where $i$ indexes the rows and $j$ indexes the columns. We use $\mathbf{I}_{N}$ to denote the $N \times N$ identity matrix (also called the unit matrix), and if there is no ambiguity over dimensionality, we simply use $\mathbf{I}$. The transpose matrix $\mathbf{A}^{\mathrm{T}}$ has elements $\left(\mathbf{A}^{\mathrm{T}}\right)_{i j}=A_{j i}$. From the definition of a transpose, we have

$$
(\mathbf{A B})^{\mathrm{T}}=\mathbf{B}^{\mathrm{T}} \mathbf{A}^{\mathrm{T}}
$$

which can be verified by writing out the indices. The inverse of $\mathbf{A}$, denoted $\mathbf{A}^{-1}$, satisfies

$$
\mathbf{A} \mathbf{A}^{-1}=\mathbf{A}^{-1} \mathbf{A}=\mathbf{I}
$$

![](https://cdn.mathpix.com/cropped/2024_05_27_25fa23d4d21ea443ccefg-1.jpg?height=44&width=544&top_left_y=1888&top_left_x=412

ChatGPT figure/image summary: The image appears to contain mathematical text related to linear algebra, specifically an equation or identity likely involving matrices and is part of the paper you mentioned in the provided context. However, since the image looks like a cropped in-line formula from a text, the exact details are cut off, and I cannot provide the complete equation or formula shown.

From the partial textual content, we can speculate that the formula may relate to properties of matrix multiplication or the relationship between the matrices A, B, and their inverses. The expression begins with "Because \( AB B^{-1} A^{-1} = I \)", where the identity matrix is denoted as \( I \), and then it seems to lead into the derivation of a property or identity based on this equation.

To fully understand this part, I would need to either see the complete equation or have further context from the paper.)

$$
(\mathbf{A B})^{-1}=\mathbf{B}^{-1} \mathbf{A}^{-1}
$$

Also we have

$$
\left(\mathbf{A}^{\mathrm{T}}\right)^{-1}=\left(\mathbf{A}^{-1}\right)^{\mathrm{T}}
$$

which is easily proven by taking the transpose of (A.2) and applying (A.1).

A useful identity involving matrix inverses is the following:

$$
\left(\mathbf{P}^{-1}+\mathbf{B}^{\mathrm{T}} \mathbf{R}^{-1} \mathbf{B}\right)^{-1} \mathbf{B}^{\mathrm{T}} \mathbf{R}^{-1}=\mathbf{P B}^{\mathrm{T}}\left(\mathbf{B} \mathbf{P} \mathbf{B}^{\mathrm{T}}+\mathbf{R}\right)^{-1}
$$

which is easily verified by right-multiplying both sides by $\left(\mathbf{B P B}^{\mathrm{T}}+\mathbf{R}\right)$. Suppose that $\mathbf{P}$ has dimensionality $N \times N$ and that $\mathbf{R}$ has dimensionality $M \times M$, so that $\mathbf{B}$ is $M \times N$. Then if $M \ll N$, it will be much cheaper to evaluate the right-hand side of (A.5) than the left-hand side. A special case that sometimes arises is

$$
(\mathbf{I}+\mathbf{A B})^{-1} \mathbf{A}=\mathbf{A}(\mathbf{I}+\mathbf{B A})^{-1}
$$

Another useful identity involving inverses is the following:

$$
\left(\mathbf{A}+\mathbf{B D}^{-1} \mathbf{C}\right)^{-1}=\mathbf{A}^{-1}-\mathbf{A}^{-1} \mathbf{B}\left(\mathbf{D}+\mathbf{C A}^{-1} \mathbf{B}\right)^{-1} \mathbf{C A}^{-1}
$$

which is known as the Woodbury identity. It can be verified by multiplying both sides by $\left(\mathbf{A}+\mathbf{B D}^{-1} \mathbf{C}\right)$. This is useful, for instance, when $\mathbf{A}$ is large and diagonal and hence easy to invert, and when $\mathbf{B}$ has many rows but few columns (and conversely for $\mathbf{C}$ ), so that the right-hand side is much cheaper to evaluate than the left-hand side.

A set of vectors $\left\{\mathbf{a}_{1}, \ldots, \mathbf{a}_{N}\right\}$ is said to be linearly independent if the relation $\sum_{n} \alpha_{n} \mathbf{a}_{n}=0$ holds only if all $\alpha_{n}=0$. This implies that none of the vectors can be expressed as a linear combination of the remainder. The rank of a matrix is the maximum number of linearly independent rows (or equivalently the maximum number of linearly independent columns).

\title{
A.2. Traces and Determinants
}

Square matrices have traces and determinants. The trace $\operatorname{Tr}(\mathbf{A})$ of a matrix $\mathbf{A}$ is defined as the sum of the elements on the leading diagonal. By writing out the indices, we see that

$$
\operatorname{Tr}(\mathbf{A B})=\operatorname{Tr}(\mathbf{B A})
$$

By applying this formula multiple times to the product of three matrices, we see that

$$
\operatorname{Tr}(\mathbf{A B C})=\operatorname{Tr}(\mathbf{C A B})=\operatorname{Tr}(\mathbf{B C A})
$$

which is known as the cyclic property of the trace operator. It clearly extends to the product of any number of matrices. The determinant $|\mathbf{A}|$ of an $N \times N$ matrix $\mathbf{A}$ is defined by

$$
|\mathbf{A}|=\sum( \pm 1) A_{1 i_{1}} A_{2 i_{2}} \cdots A_{N i_{N}}
$$

in which the sum is taken over all products consisting of precisely one element from each row and one element from each column, with a coefficient +1 or -1 according to whether the permutation $i_{1} i_{2} \ldots i_{N}$ is even or odd, respectively. Note that $|\mathbf{I}|=1$,

and that the determinant of a diagonal matrix is given by the product of the elements on the leading diagonal. Thus, for a $2 \times 2$ matrix, the determinant takes the form

$$
|\mathbf{A}|=\left|\begin{array}{ll}
a_{11} & a_{12} \\
a_{21} & a_{22}
\end{array}\right|=a_{11} a_{22}-a_{12} a_{21}
$$

The determinant of a product of two matrices is given by

$$
|\mathbf{A B}|=|\mathbf{A} \| \mathbf{B}|
$$

as can be shown from (A.10). Also, the determinant of an inverse matrix is given by

$$
\left|\mathbf{A}^{-1}\right|=\frac{1}{|\mathbf{A}|}
$$

which can be shown by taking the determinant of (A.2) and applying (A.12).

If $\mathbf{A}$ and $\mathbf{B}$ are matrices of size $N \times M$, then

$$
\left|\mathbf{I}_{N}+\mathbf{A} \mathbf{B}^{\mathrm{T}}\right|=\left|\mathbf{I}_{M}+\mathbf{A}^{\mathrm{T}} \mathbf{B}\right| .
$$

A useful special case is

$$
\left|\mathbf{I}_{N}+\mathbf{a b}^{\mathrm{T}}\right|=1+\mathbf{a}^{\mathrm{T}} \mathbf{b}
$$

where $\mathbf{a}$ and $\mathbf{b}$ are $N$-dimensional column vectors.

\title{
A.3. Matrix Derivatives
}

Sometimes we need to consider derivatives of vectors and matrices with respect to scalars. The derivative of a vector a with respect to a scalar $x$ is a vector whose components are given by

$$
\left(\frac{\partial \mathbf{a}}{\partial x}\right)_{i}=\frac{\partial a_{i}}{\partial x}
$$

with an analogous definition for the derivative of a matrix. Derivatives with respect to vectors and matrices can also be defined, for instance

$$
\left(\frac{\partial x}{\partial \mathbf{a}}\right)_{i}=\frac{\partial x}{\partial a_{i}}
$$

and similarly

$$
\left(\frac{\partial \mathbf{a}}{\partial \mathbf{b}}\right)_{i j}=\frac{\partial a_{i}}{\partial b_{j}}
$$

The following is easily proven by writing out the components:

$$
\frac{\partial}{\partial \mathbf{x}}\left(\mathbf{x}^{\mathrm{T}} \mathbf{a}\right)=\frac{\partial}{\partial \mathbf{x}}\left(\mathbf{a}^{\mathrm{T}} \mathbf{x}\right)=\mathbf{a}
$$

\title{
A. LINEAR ALGEBRA
}

Similarly

$$
\frac{\partial}{\partial x}(\mathbf{A B})=\frac{\partial \mathbf{A}}{\partial x} \mathbf{B}+\mathbf{A} \frac{\partial \mathbf{B}}{\partial x}
$$

The derivative of the inverse of a matrix can be expressed as

$$
\frac{\partial}{\partial x}\left(\mathbf{A}^{-1}\right)=-\mathbf{A}^{-1} \frac{\partial \mathbf{A}}{\partial x} \mathbf{A}^{-1}
$$

as can be shown by differentiating the equation $\mathbf{A}^{-1} \mathbf{A}=\mathbf{I}$ using (A.20) and then right-multiplying by $\mathbf{A}^{-1}$. Also

$$
\frac{\partial}{\partial x} \ln |\mathbf{A}|=\operatorname{Tr}\left(\mathbf{A}^{-1} \frac{\partial \mathbf{A}}{\partial x}\right)
$$

which we shall prove later. If we choose $x$ to be one of the elements of $\mathbf{A}$, we have

$$
\frac{\partial}{\partial A_{i j}} \operatorname{Tr}(\mathbf{A B})=B_{j i}
$$

as can be seen by writing out the matrices using index notation. We can write this result more compactly in the form

$$
\frac{\partial}{\partial \mathbf{A}} \operatorname{Tr}(\mathbf{A B})=\mathbf{B}^{\mathrm{T}}
$$

With this notation, we have the following properties:

$$
\begin{aligned}
\frac{\partial}{\partial \mathbf{A}} \operatorname{Tr}\left(\mathbf{A}^{\mathrm{T}} \mathbf{B}\right) & =\mathbf{B} \\
\frac{\partial}{\partial \mathbf{A}} \operatorname{Tr}(\mathbf{A}) & =\mathbf{I} \\
\frac{\partial}{\partial \mathbf{A}} \operatorname{Tr}\left(\mathbf{A B} \mathbf{A}^{\mathrm{T}}\right) & =\mathbf{A}\left(\mathbf{B}+\mathbf{B}^{\mathrm{T}}\right)
\end{aligned}
$$

which can again be proven by writing out the matrix indices. We also have

$$
\frac{\partial}{\partial \mathbf{A}} \ln |\mathbf{A}|=\left(\mathbf{A}^{-1}\right)^{\mathrm{T}}
$$

which follows from (A.22) and (A.24).

\section*{A.4. Eigenvectors}

For a square matrix $\mathbf{A}$ of size $M \times M$, the eigenvector equation is defined by

$$
\mathbf{A} \mathbf{u}_{i}=\lambda_{i} \mathbf{u}_{i}
$$

for $i=1, \ldots, M$, where $\mathbf{u}_{i}$ is an eigenvector and $\lambda_{i}$ is the corresponding eigenvalue. This can be viewed as a set of $M$ simultaneous homogeneous linear equations, and the condition for a solution is that

$$
\left|\mathbf{A}-\lambda_{i} \mathbf{I}\right|=0
$$

which is known as the characteristic equation. Because this is a polynomial of order $M$ in $\lambda_{i}$, it must have $M$ solutions (though these need not all be distinct). The rank of $\mathbf{A}$ is equal to the number of non-zero eigenvalues.

Of particular interest are symmetric matrices, which arise as covariance matrices, kernel matrices, and Hessians. Symmetric matrices have the property that $A_{i j}=A_{j i}$, or equivalently $\mathbf{A}^{\mathrm{T}}=\mathbf{A}$. The inverse of a symmetric matrix is also symmetric, as can be seen by taking the transpose of $\mathbf{A}^{-1} \mathbf{A}=\mathbf{I}$ and using $\mathbf{A A}^{-1}=\mathbf{I}$ together with the symmetry of $\mathbf{I}$.

In general, the eigenvalues of a matrix are complex numbers, but for symmetric matrices, the eigenvalues $\lambda_{i}$ are real. This can be seen by first left-multiplying (A.29) by $\left(\mathbf{u}_{i}^{\star}\right)^{\mathrm{T}}$, where $\star$ denotes the complex conjugate, to give

$$
\left(\mathbf{u}_{i}^{\star}\right)^{\mathrm{T}} \mathbf{A} \mathbf{u}_{i}=\lambda_{i}\left(\mathbf{u}_{i}^{\star}\right)^{\mathrm{T}} \mathbf{u}_{i} .
$$

Next we take the complex conjugate of (A.29) and left-multiply by $\mathbf{u}_{i}^{\mathrm{T}}$ to give

$$
\mathbf{u}_{i}^{\mathrm{T}} \mathbf{A} \mathbf{u}_{i}^{\star}=\lambda_{i}^{\star} \mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{i}^{\star}
$$

where we have used $\mathbf{A}^{\star}=\mathbf{A}$ because we are considering only real matrices $\mathbf{A}$. Taking the transpose of the second of these equations and using $\mathbf{A}^{\mathrm{T}}=\mathbf{A}$, we see that the left-hand sides of the two equations are equal and hence that $\lambda_{i}^{\star}=\lambda_{i}$, and so $\lambda_{i}$ must be real.

The eigenvectors $\mathbf{u}_{i}$ of a real symmetric matrix can be chosen to be orthonormal (i.e., orthogonal and of unit length) so that

$$
\mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{j}=I_{i j}
$$

where $I_{i j}$ are the elements of the identity matrix $\mathbf{I}$. To show this, we first left-multiply (A.29) by $\mathbf{u}_{j}^{\mathrm{T}}$ to give

$$
\mathbf{u}_{j}^{\mathrm{T}} \mathbf{A} \mathbf{u}_{i}=\lambda_{i} \mathbf{u}_{j}^{\mathrm{T}} \mathbf{u}_{i}
$$

and hence, by exchanging the indices, we have

$$
\mathbf{u}_{i}^{\mathrm{T}} \mathbf{A} \mathbf{u}_{j}=\lambda_{j} \mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{j}
$$

We now take the transpose of the second equation and make use of the symmetry property $\mathbf{A}^{\mathrm{T}}=\mathbf{A}$, and then subtract the two equations to give

$$
\left(\lambda_{i}-\lambda_{j}\right) \mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{j}=0
$$

Hence, for $\lambda_{i} \neq \lambda_{j}$, we have $\mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{j}=0$ so that $\mathbf{u}_{i}$ and $\mathbf{u}_{j}$ are orthogonal. If the two eigenvalues are equal, then any linear combination $\alpha \mathbf{u}_{i}+\beta \mathbf{u}_{j}$ is also an eigenvector

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

These last two equations can also be written in the form

$$
\begin{aligned}
\mathbf{A} & =\sum_{i=1}^{M} \lambda_{i} \mathbf{u}_{i} \mathbf{u}_{i}^{\mathrm{T}} \\
\mathbf{A}^{-1} & =\sum_{i=1}^{M} \frac{1}{\lambda_{i}} \mathbf{u}_{i} \mathbf{u}_{i}^{\mathrm{T}}
\end{aligned}
$$

If we take the determinant of (A.43) and use (A.12), we obtain

$$
|\mathbf{A}|=\prod_{i=1}^{M} \lambda_{i}
$$

Similarly, taking the trace of (A.43), and using the cyclic property (A.8) of the trace operator together with $\mathbf{U}^{\mathrm{T}} \mathbf{U}=\mathbf{I}$, we have

$$
\operatorname{Tr}(\mathbf{A})=\sum_{i=1}^{M} \lambda_{i}
$$

We leave it as an exercise for the reader to verify (A.22) by making use of the results (A.33), (A.45), (A.46), and (A.47).

A matrix $\mathbf{A}$ is said to be positive definite, denoted by $\mathbf{A} \succ 0$, if $\mathbf{w}^{\mathrm{T}} \mathbf{A w}>0$ for all non-zero values of the vector w. Equivalently, a positive definite matrix has $\lambda_{i}>$ 0 for all of its eigenvalues (as can be seen by setting $\mathbf{w}$ to each of the eigenvectors in turn and noting that an arbitrary vector can be expanded as a linear combination of the eigenvectors). Note that having all positive elements does not necessarily mean that a matrix is that positive definite. For example, the matrix

$$
\left(\begin{array}{ll}
1 & 2 \\
3 & 4
\end{array}\right)
$$

has eigenvalues $\lambda_{1} \simeq 5.37$ and $\lambda_{2} \simeq-0.37$. A matrix is said to be positive semidefinite if $\mathbf{w}^{\mathrm{T}} \mathbf{A} \mathbf{w} \geqslant 0$ holds for all values of $\mathbf{w}$, which is denoted $\mathbf{A} \succeq 0$ and is equivalent to $\lambda_{i} \geqslant 0$.

The condition number of a matrix is given by

$$
\mathrm{CN}=\left(\frac{\lambda_{\max }}{\lambda_{\min }}\right)^{1 / 2}
$$

where $\lambda_{\max }$ is the largest eigenvalue and $\lambda_{\min }$ is the smallest eigenvalue.


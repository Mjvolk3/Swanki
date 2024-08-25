### Appendix A: Linear Algebra

In this appendix, we explore various useful properties and identities involving matrices and determinants. This assumes familiarity with basic linear algebra concepts. For some results, I will indicate how to prove them, while for more complex cases, I will suggest consulting standard textbooks on the subject. A comprehensive discussion can be found in Golub and Van Loan, and an extensive collection of matrix properties is available in Lütkepohl. For matrix derivatives, Magnus and Neudecker's work is highly recommended.

### Section A.1: Matrix Identities

Let's start with some important matrix identities. Consider a matrix 'A' with elements denoted as 'A_i_j', where 'i' represents the row index and 'j' the column index. The identity matrix, often called the unit matrix, is denoted as 'I_N' for an N by N matrix. If there's no ambiguity about the dimensions, we simply use 'I'. The transpose of a matrix 'A', denoted as 'A^T', switches its rows with columns. Mathematically, the element in the i-th row and j-th column of 'A^T' is the element in the j-th row and i-th column of 'A'.

One important property of transposes is that the transpose of the product of two matrices 'A' and 'B' is the product of their transposes in reverse order. In other words, the transpose of the product 'A B' is 'B^T A^T'. The inverse of a matrix 'A', denoted 'A inverse', satisfies the property that 'A' times 'A inverse' equals the identity matrix 'I'. This holds true in both orders: 'A A inverse' and 'A inverse A' both equal 'I'.

Another useful property relates to the inverse of a product of two matrices. The inverse of the product 'A B' is the product of the inverses in reverse order, 'B inverse A inverse'. Additionally, the inverse of a transpose of a matrix 'A' is the transpose of the inverse of 'A'.

One particularly useful identity involving matrix inverses is the following: If 'P' is an N by N matrix and 'R' is an M by M matrix, then a certain inverse expression involving 'P', 'R', and another matrix 'B' can be simplified. This simplification is computationally cheaper when M is much smaller than N. Another special case that sometimes arises involves a matrix identity where the inverse of 'I + A B' times 'A' equals 'A' times the inverse of 'I + B A'.

### Section A.2: Traces and Determinants

Moving on to square matrices, we discuss traces and determinants. The trace of a matrix 'A', denoted as 'Tr(A)', is the sum of the elements on its main diagonal. An interesting property of the trace is its cyclic nature. For any matrices 'A' and 'B', the trace of their product 'A B' is the same as the trace of 'B A'. This cyclic property extends to products of three or more matrices.

The determinant of a square matrix 'A', denoted as '|A|', is a scalar value that can be computed from the elements of the matrix. For a two by two matrix, the determinant is computed as the product of the elements on the main diagonal minus the product of the off-diagonal elements. The determinant of a product of two matrices is the product of their determinants. Additionally, the determinant of an inverse matrix 'A inverse' is the reciprocal of the determinant of 'A'.

A useful identity involving determinants is that for matrices 'A' and 'B' of sizes N by M, the determinant of 'I_N + A B^T' equals the determinant of 'I_M + A^T B'. A special case of this identity involves column vectors 'a' and 'b', where the determinant of 'I_N + a b^T' equals one plus the inner product of 'a^T' and 'b'.

### Section A.3: Matrix Derivatives

Sometimes, we need to consider derivatives of vectors and matrices with respect to scalars. The derivative of a vector 'a' with respect to a scalar 'x' is another vector where each component is the partial derivative of the corresponding component of 'a' with respect to 'x'. Similarly, the derivative of a matrix 'A' with respect to a scalar 'x' is a matrix where each element is the partial derivative of the corresponding element of 'A' with respect to 'x'.

We can also define derivatives with respect to vectors and matrices. For example, the derivative of a scalar 'x' with respect to a vector 'a' is a vector where each component is the partial derivative of 'x' with respect to the corresponding component of 'a'. The derivative of a vector 'a' with respect to another vector 'b' is a matrix where each element is the partial derivative of the corresponding component of 'a' with respect to the corresponding component of 'b'.

One useful result is that the derivative of the product of two matrices 'A' and 'B' with respect to a scalar 'x' is the sum of the derivative of 'A' with respect to 'x' times 'B' and 'A' times the derivative of 'B' with respect to 'x'. The derivative of the inverse of a matrix 'A' with respect to a scalar 'x' is given by a specific formula involving the inverse of 'A' and the derivative of 'A' with respect to 'x'.

### Section A.4: Eigenvectors

For a square matrix 'A' of size M by M, the eigenvector equation is defined by 'A u_i = lambda_i u_i', where 'u_i' is an eigenvector and 'lambda_i' is the corresponding eigenvalue. The condition for a solution is that the determinant of 'A - lambda_i I' equals zero, which is known as the characteristic equation. This equation is a polynomial of order M in 'lambda_i' and must have M solutions, although they may not all be distinct.

Symmetric matrices, which have the property that their elements are symmetric about the main diagonal, are particularly important. For symmetric matrices, the eigenvalues are always real, and the eigenvectors can be chosen to be orthonormal. This means that the eigenvectors are both orthogonal and of unit length.

The orthogonality of the eigenvectors can be shown by considering the eigenvalue equations for two different eigenvectors and taking the transpose of one of the equations. If the eigenvalues are distinct, the corresponding eigenvectors are orthogonal. If the eigenvalues are the same, any linear combination of the corresponding eigenvectors is also an eigenvector, and we can choose an orthogonal combination.

This appendix provides a foundation for understanding the key properties and identities of matrices and determinants, which are essential for various applications in linear algebra and beyond.
### Orthogonality and Orthonormality of Eigenvectors

When dealing with matrices and their eigenvectors, a crucial property is orthogonality. Orthogonal vectors are vectors that are at right angles to each other, and their dot product is zero. For any given matrix, the eigenvectors can be chosen to be orthogonal. This is particularly useful, as it simplifies many calculations and makes it easier to understand the structure of the matrix. To further refine this, we can normalize these orthogonal eigenvectors, making them unit vectors (vectors with a length of one). This process leads to what we call an orthonormal set of eigenvectors.

Given a matrix with \(M\) eigenvalues, we can form an \(M \times M\) matrix, \(\mathbf{U}\), where each column is an eigenvector. Since the eigenvectors are orthonormal, the matrix \(\mathbf{U}\) satisfies the property that the product of its transpose and itself is the identity matrix, denoted as \(\mathbf{U}^{\mathrm{T}} \mathbf{U} = \mathbf{I}\). This is what defines \(\mathbf{U}\) as an orthogonal matrix. Interestingly, the rows of this matrix are also orthogonal, so multiplying \(\mathbf{U}\) by its transpose also yields the identity matrix, \(\mathbf{U} \mathbf{U}^{\mathrm{T}} = \mathbf{I}\).

### Diagonalization of Matrices

The eigenvector equation can be rewritten using the matrix \(\mathbf{U}\) and a diagonal matrix \(\boldsymbol{\Lambda}\), which contains the eigenvalues on its diagonal. This relationship is expressed as \(\mathbf{A U} = \mathbf{U} \boldsymbol{\Lambda}\). This signifies that the matrix \(\mathbf{A}\) can be 'diagonalized' by the orthogonal matrix \(\mathbf{U}\), simplifying many operations involving \(\mathbf{A}\).

For example, if we transform any vector \(\mathbf{x}\) using the orthogonal matrix \(\mathbf{U}\), the length (or norm) of the vector remains unchanged. This is a property of orthogonal transformations; they preserve both lengths and angles. This can be seen through the equation \(\widetilde{\mathbf{x}}^{\mathrm{T}} \widetilde{\mathbf{x}} = \mathbf{x}^{\mathrm{T}} \mathbf{U}^{\mathrm{T}} \mathbf{U} \mathbf{x} = \mathbf{x}^{\mathrm{T}} \mathbf{x}\). Similarly, the angle between any two vectors is preserved under this transformation.

### Practical Implications and Further Properties

From these properties, we derive that \(\mathbf{U}^{\mathrm{T}} \mathbf{A} \mathbf{U} = \boldsymbol{\Lambda}\), indicating that the matrix \(\mathbf{A}\) can be expressed as \(\mathbf{U} \boldsymbol{\Lambda} \mathbf{U}^{\mathrm{T}}\). Consequently, the inverse of \(\mathbf{A}\) can be represented as \(\mathbf{U} \boldsymbol{\Lambda}^{-1} \mathbf{U}^{\mathrm{T}}\). These forms are very useful in computations, as they simplify the manipulation of the matrix \(\mathbf{A}\).

Furthermore, we can express \(\mathbf{A}\) and its inverse as sums involving the eigenvalues and eigenvectors. Specifically, \(\mathbf{A} = \sum_{i=1}^{M} \lambda_{i} \mathbf{u}_{i} \mathbf{u}_{i}^{\mathrm{T}}\) and \(\mathbf{A}^{-1} = \sum_{i=1}^{M} \frac{1}{\lambda_{i}} \mathbf{u}_{i} \mathbf{u}_{i}^{\mathrm{T}}\). This approach not only aids in understanding the matrix better but also in practical applications such as solving systems of linear equations.

### Determinant and Trace

The determinant of \(\mathbf{A}\), a scalar value that can provide insights into the properties of the matrix, is the product of its eigenvalues, \(|\mathbf{A}| = \prod_{i=1}^{M} \lambda_{i}\). Similarly, the trace of \(\mathbf{A}\), which is the sum of the elements on its main diagonal, equals the sum of its eigenvalues, \(\operatorname{Tr}(\mathbf{A}) = \sum_{i=1}^{M} \lambda_{i}\). These properties are instrumental in various fields, including physics and engineering, where such matrices frequently arise.

### Positive Definiteness and Condition Number

A matrix \(\mathbf{A}\) is considered positive definite if for all non-zero vectors \(\mathbf{w}\), the product \(\mathbf{w}^{\mathrm{T}} \mathbf{A} \mathbf{w}\) is greater than zero. This implies that all the eigenvalues of \(\mathbf{A}\) are positive. Positive definite matrices are important in optimization problems and in ensuring stability in numerical methods. Conversely, a matrix is positive semidefinite if this product is greater than or equal to zero for all \(\mathbf{w}\), meaning all eigenvalues are non-negative.

Finally, the condition number of a matrix, which provides a measure of how well-conditioned a matrix is for inversion, is given by the square root of the ratio of the largest eigenvalue to the smallest eigenvalue. This ratio can indicate how sensitive a matrix is to numerical errors, which is significant in practical computations.
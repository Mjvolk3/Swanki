Section: Appendix A: Linear Algebra

In this appendix, we delve into some essential properties and identities involving matrices and determinants. This isn't a beginner's tutorial; instead, it's aimed at those who already have a grounding in basic linear algebra. For some results, we will indicate how to prove them, whereas more complex cases are referenced to standard textbooks on the subject. We assume that matrix inverses exist and that the matrix dimensions are such that the formulas are correctly defined. For a comprehensive discussion, refer to works by Golub and Van Loan, and for an extensive collection of matrix properties, Lütkepohl’s publication is a great resource. Matrix derivatives are discussed in detail by Magnus and Neudecker.

Section: Matrix Identities

Let's start with the basics. A matrix, which we will call A, has elements A sub i j, where i indexes the rows and j indexes the columns. The identity matrix of size N by N is denoted by I sub N, and if there's no ambiguity about its size, we simply use I. The transpose of matrix A, denoted A transpose, switches its rows and columns, meaning the element at row i and column j of A transpose is the element at row j and column i of A. This gives us the property that the transpose of the product of A and B is equal to the product of B transpose and A transpose, which can be verified by writing out the indices.

The inverse of matrix A, denoted A inverse, satisfies the equation where the product of A and A inverse, as well as the product of A inverse and A, equals the identity matrix. This means that when you multiply a matrix by its inverse, you get the identity matrix. Another important property is that the inverse of the product of A and B is equal to the product of B inverse and A inverse. Taking the transpose of the inverse of a matrix gives us that the transpose of A inverse is equal to the inverse of A transpose. This can be proven by taking the transpose of the product of A and A inverse and applying the previously mentioned transpose property.

One useful identity involving matrix inverses is that the inverse of the sum of P inverse and the product of B transpose, R inverse, and B, multiplied by B transpose and R inverse, is equal to the product of P, B transpose, and the inverse of the sum of the product of B, P, and B transpose, and R. Suppose P is an N by N matrix, and R is an M by M matrix, making B an M by N matrix. If M is much smaller than N, it is computationally cheaper to evaluate the right-hand side of this identity than the left-hand side.

Additionally, a special case that sometimes arises is that the inverse of the sum of the identity matrix and the product of A and B, multiplied by A, is equal to the product of A and the inverse of the sum of the identity matrix and the product of B and A. Another useful inverse identity is the Woodbury identity, which states that the inverse of the sum of A and the product of B, D inverse, and C, is equal to the difference between A inverse and the product of A inverse, B, the inverse of the sum of D and the product of C, A inverse, and B, and C, A inverse. This is particularly useful when A is large and diagonal, hence easier to invert, and when B has many rows but few columns, making the right-hand side of the equation much cheaper to evaluate.

In linear algebra, a set of vectors is said to be linearly independent if the relation that the sum of alpha sub n times a sub n equals zero holds only if all alpha sub n equals zero. This implies that none of the vectors in the set can be expressed as a linear combination of the others. The rank of a matrix is the maximum number of linearly independent rows or, equivalently, the maximum number of linearly independent columns.

Section: Traces and Determinants

Moving on to square matrices, these have traces and determinants. The trace of a matrix A, denoted Trace of A, is the sum of the elements on the leading diagonal. By writing out the indices, we see that the trace of the product of A and B is equal to the trace of the product of B and A. This property, known as the cyclic property of the trace operator, extends to the product of any number of matrices, making it a very powerful tool in linear algebra.

The determinant of an N by N matrix A, denoted as the absolute value of A, is defined as the sum of products of elements, with each product containing precisely one element from each row and each column. The sign of each product is positive or negative according to whether the permutation of the indices is even or odd, respectively. For a simple 2 by 2 matrix, the determinant is calculated as the product of the elements in the leading diagonal minus the product of the elements in the other diagonal.

One important property of determinants is that the determinant of a product of two matrices is the product of their determinants. The determinant of the inverse of a matrix is given by one divided by the determinant of the matrix.

If A and B are matrices of size N by M, then the determinant of the sum of the identity matrix and the product of A and B transpose is equal to the determinant of the sum of the identity matrix and the product of A transpose and B. A useful special case is when A and B are column vectors, in which case the determinant simplifies to one plus the dot product of the transpose of a and b.

Section: Matrix Derivatives

Sometimes we need to consider derivatives of vectors and matrices with respect to scalars. The derivative of a vector a with respect to a scalar x is a vector whose components are given by the partial derivatives of each component of a with respect to x. Similarly, the derivative of a matrix with respect to a scalar is a matrix of the partial derivatives of each element of the matrix with respect to the scalar.

Derivatives with respect to vectors and matrices can also be defined. This means taking the derivative of a function that outputs a matrix or a vector with respect to another matrix or vector. These kinds of derivatives are useful in various applications, particularly in optimization problems and in the field of machine learning.
Section: Matrix Derivatives (Continued)

The derivative of a vector a with respect to another vector b is a matrix whose i,j element is the partial derivative of the i-th component of a with respect to the j-th component of b. One useful result is that the derivative of the product of a row vector a transpose and a column vector x with respect to x is the row vector a. Similarly, the derivative of the product of two matrices A and B with respect to a scalar x is given by the product of the derivatives of each matrix with respect to x.

The derivative of the inverse of a matrix A with respect to a scalar x is the negative product of A inverse, the derivative of A with respect to x, and A inverse. This can be shown by differentiating the equation that states that the product of A inverse and A equals the identity matrix and then right-multiplying by A inverse. Additionally, the derivative of the logarithm of the determinant of a matrix A with respect to a scalar x is given by the trace of the product of the inverse of A and the derivative of A with respect to x.

Section: Eigenvectors and Eigenvalues

For a square matrix A of size M by M, the eigenvector equation is defined by A times u sub i equals lambda sub i times u sub i for i ranging from 1 to M, where u sub i is an eigenvector and lambda sub i is the corresponding eigenvalue. This can be viewed as a set of M simultaneous homogeneous linear equations, and the condition for a solution is that the determinant of the difference between A and lambda sub i times the identity matrix is zero, known as the characteristic equation. This polynomial equation of order M in lambda sub i must have M solutions, though they need not all be distinct. The rank of A is equal to the number of non-zero eigenvalues.

Symmetric matrices, which appear frequently as covariance matrices, kernel matrices, and Hessians, have the property that their elements are symmetric, meaning the element in row i, column j is equal to the element in row j, column i, or equivalently, the transpose of A is equal to A. The inverse of a symmetric matrix is also symmetric. The eigenvalues of a symmetric matrix are real numbers, which can be shown by considering the complex conjugate of the eigenvector equation and using the symmetry property of the matrix.

The eigenvectors of a real symmetric matrix can be chosen to be orthonormal. This means that the eigenvectors are orthogonal and normalized to unit length, which can be shown by manipulating the eigenvector equations and using the properties of symmetric matrices. When we have two different eigenvalues, say lambda sub i and lambda sub j, the corresponding eigenvectors u sub i and u sub j are orthogonal. This orthogonality condition is expressed by the equation stating that the dot product of u sub i and u sub j equals zero. Essentially, if the eigenvalues are distinct, the eigenvectors point in completely different directions.

Now, if the eigenvalues are the same, things get a bit more interesting. Any linear combination of the eigenvectors associated with that eigenvalue is also an eigenvector. This means we can choose one combination arbitrarily and the second one to be orthogonal to the first. Importantly, even if the eigenvalues are the same, the eigenvectors are never linearly dependent—meaning one cannot be expressed as a multiple of the other. This orthogonality and normalization process allows us to form a complete set of M orthogonal eigenvectors, which means any M-dimensional vector can be expressed as a combination of these eigenvectors.

Section: Orthogonal Matrices and Diagonalization

Next, let's consider the matrix U, which has these orthogonal eigenvectors as its columns. This matrix U satisfies the condition that when you multiply U by its transpose, you get an identity matrix. This property defines U as an orthogonal matrix. Moreover, the rows of this matrix are also orthogonal, which implies that multiplying U by its transpose from the other side also gives an identity matrix. This orthonormality is crucial for many applications, as it ensures that the transformations we perform using U preserve lengths and angles.

When we express the eigenvector equation in matrix form, we have matrix A multiplied by U equals U multiplied by a diagonal matrix Lambda. This diagonal matrix Lambda contains the eigenvalues on its diagonal. If we transform a vector x by this orthogonal matrix U, the length of the vector remains unchanged. This preservation of length and the angles between vectors means that multiplication by U can be interpreted as a rigid rotation of the coordinate system. This is a powerful concept in linear algebra, as it allows for transformations without distorting the underlying geometry of the space.

Finally, let's talk about the diagonalization process of matrix A. When we multiply A by U and then by the transpose of U, we get the diagonal matrix Lambda. This means U diagonalizes A. If we left-multiply by U and right-multiply by the transpose of U, we can reconstitute A from its eigenvalues and eigenvectors. Similarly, the inverse of A can be expressed by inverting its eigenvalues. The determinant of A is the product of its eigenvalues, while the trace of A, which is the sum of its diagonal elements, is the sum of its eigenvalues.

Regarding matrix properties, a matrix is positive definite if, for any non-zero vector w, the quadratic form w transpose A w is greater than zero. This condition is equivalent to all eigenvalues being positive. For instance, a matrix with all positive elements is not necessarily positive definite. A matrix is positive semidefinite if the quadratic form is non-negative, meaning all eigenvalues are non-negative. The condition number of a matrix, which measures its sensitivity to numerical operations, is defined as the square root of the ratio of its largest to smallest eigenvalue. This gives a sense of the matrix's stability and robustness in calculations.

Section: Chapter Summary

1. **Matrix Basics and Transposition**: Discusses basic properties of matrices, including the identity matrix, transposition, and their properties such as the product of transposed matrices.

2. **Matrix Inverses**: Explains the properties of matrix inverses, including the inverse of products and sums of matrices, and useful identities like the Woodbury identity, which can simplify computational processes.

3. **Linear Independence and Rank**: Defines linear independence of vectors and the rank of a matrix, which is the number of linearly independent rows or columns.

4. **Traces and Determinants**: Covers the trace and determinant of square matrices, including properties like the cyclic property of the trace and the product of determinants.

5. **Matrix Derivatives**: Introduces derivatives of vectors and matrices with respect to scalars, explaining their utility in optimization and machine learning.

6. **Eigenvectors and Eigenvalues**: Details the eigenvector equation, the characteristic polynomial, and properties of symmetric matrices, including real eigenvalues and orthogonal eigenvectors.

7. **Orthogonal Matrices and Diagonalization**: Discusses matrices with orthogonal eigenvectors, the concept of orthogonality, and the diagonalization process, emphasizing the preservation of lengths and angles in transformations.

8. **Positive Definite Matrices**: Defines positive definite and positive semidefinite matrices, relating these properties to their eigenvalues and their implications for numerical stability and robustness of the matrix.
Section: Appendix A: Linear Algebra

In this appendix, we explore various useful properties and identities involving matrices and determinants. This assumes familiarity with basic linear algebra concepts. For some results, I will indicate how to prove them, while for more complex cases, I will suggest consulting standard textbooks on the subject. A comprehensive discussion can be found in Golub and Van Loan, and an extensive collection of matrix properties is available in Lütkepohl. For matrix derivatives, Magnus and Neudecker's work is highly recommended.

Section: Matrix Identities

Let's start with some important matrix identities. Consider a matrix 'A' with elements denoted as 'A sub i j', where 'i' represents the row index and 'j' the column index. The identity matrix, often called the unit matrix, is denoted as 'I sub N' for an N by N matrix. If there's no ambiguity about the dimensions, we simply use 'I'. The transpose of a matrix 'A', denoted as 'A transpose', switches its rows with columns. Mathematically, the element in the i-th row and j-th column of 'A transpose' is the element in the j-th row and i-th column of 'A'.

One important property of transposes is that the transpose of the product of two matrices 'A' and 'B' is the product of their transposes in reverse order. In other words, the transpose of the product 'A B' is 'B transpose A transpose'. The inverse of a matrix 'A', denoted 'A inverse', satisfies the property that 'A' times 'A inverse' equals the identity matrix 'I'. This holds true in both orders: 'A A inverse' and 'A inverse A' both equal 'I'.

Another useful property relates to the inverse of a product of two matrices. The inverse of the product 'A B' is the product of the inverses in reverse order, 'B inverse A inverse'. Additionally, the inverse of a transpose of a matrix 'A' is the transpose of the inverse of 'A'. One particularly useful identity involving matrix inverses is the following: If 'P' is an N by N matrix and 'R' is an M by M matrix, then a certain inverse expression involving 'P', 'R', and another matrix 'B' can be simplified. This simplification is computationally cheaper when M is much smaller than N. Another special case that sometimes arises involves a matrix identity where the inverse of 'I plus A B' times 'A' equals 'A' times the inverse of 'I plus B A'.

Section: Traces and Determinants

Moving on to square matrices, we discuss traces and determinants. The trace of a matrix 'A', denoted as 'Tr(A)', is the sum of the elements on its main diagonal. An interesting property of the trace is its cyclic nature. For any matrices 'A' and 'B', the trace of their product 'A B' is the same as the trace of 'B A'. This cyclic property extends to products of three or more matrices.

The determinant of a square matrix 'A', denoted as the determinant of 'A', is a scalar value that can be computed from the elements of the matrix. For a two by two matrix, the determinant is computed as the product of the elements on the main diagonal minus the product of the off-diagonal elements. The determinant of a product of two matrices is the product of their determinants. Additionally, the determinant of an inverse matrix 'A inverse' is the reciprocal of the determinant of 'A'.

A useful identity involving determinants is that for matrices 'A' and 'B' of sizes N by M, the determinant of 'I sub N plus A B transpose' equals the determinant of 'I sub M plus A transpose B'. A special case of this identity involves column vectors 'a' and 'b', where the determinant of 'I sub N plus a b transpose' equals one plus the inner product of 'a transpose' and 'b'.

Section: Matrix Derivatives

Sometimes, we need to consider derivatives of vectors and matrices with respect to scalars. The derivative of a vector 'a' with respect to a scalar 'x' is another vector where each component is the partial derivative of the corresponding component of 'a' with respect to 'x'. Similarly, the derivative of a matrix 'A' with respect to a scalar 'x' is a matrix where each element is the partial derivative of the corresponding element of 'A' with respect to 'x'.

We can also define derivatives with respect to vectors and matrices. For example, the derivative of a scalar 'x' with respect to a vector 'a' is a vector where each component is the partial derivative of 'x' with respect to the corresponding component of 'a'. The derivative of a vector 'a' with respect to another vector 'b' is a matrix where each element is the partial derivative of the corresponding component of 'a' with respect to the corresponding component of 'b'.

One useful result is that the derivative of the product of two matrices 'A' and 'B' with respect to a scalar 'x' is the sum of the derivative of 'A' with respect to 'x' times 'B' and 'A' times the derivative of 'B' with respect to 'x'. The derivative of the inverse of a matrix 'A' with respect to a scalar 'x' is given by a specific formula involving the inverse of 'A' and the derivative of 'A' with respect to 'x'.

Section: Eigenvectors

For a square matrix 'A' of size M by M, the eigenvector equation is defined by 'A u sub i equals lambda sub i u sub i', where 'u sub i' is an eigenvector and 'lambda sub i' is the corresponding eigenvalue. The condition for a solution is that the determinant of 'A minus lambda sub i I' equals zero, which is known as the characteristic equation. This equation is a polynomial of order M in 'lambda sub i' and must have M solutions, although they may not all be distinct.

Symmetric matrices, which have the property that their elements are symmetric about the main diagonal, are particularly important. For symmetric matrices, the eigenvalues are always real, and the eigenvectors can be chosen to be orthonormal. This means that the eigenvectors are both orthogonal and of unit length.

The orthogonality of the eigenvectors can be shown by considering the eigenvalue equations for two different eigenvectors and taking the transpose of one of the equations. If the eigenvalues are distinct, the corresponding eigenvectors are orthogonal.
Section: Orthogonality and Orthonormality of Eigenvectors

When dealing with matrices and their eigenvectors, a crucial property is orthogonality. Orthogonal vectors are vectors that are at right angles to each other, and their dot product is zero. For any given matrix, the eigenvectors can be chosen to be orthogonal. This is particularly useful, as it simplifies many calculations and makes it easier to understand the structure of the matrix. To further refine this, we can normalize these orthogonal eigenvectors, making them unit vectors (vectors with a length of one). This process leads to what we call an orthonormal set of eigenvectors.

Given a matrix with M eigenvalues, we can form an M by M matrix, often denoted as 'U', where each column is an eigenvector. Since the eigenvectors are orthonormal, the matrix 'U' satisfies the property that the product of its transpose and itself is the identity matrix. This means 'U transpose times U equals the identity matrix I'. This is what defines 'U' as an orthogonal matrix. Interestingly, the rows of this matrix are also orthogonal, so multiplying 'U' by its transpose also yields the identity matrix, denoted as 'U times U transpose equals I'.

Section: Diagonalization of Matrices

The eigenvector equation can be rewritten using the matrix 'U' and a diagonal matrix 'Lambda', which contains the eigenvalues on its diagonal. This relationship is expressed as 'A times U equals U times Lambda'. This signifies that the matrix 'A' can be 'diagonalized' by the orthogonal matrix 'U', simplifying many operations involving 'A'.

For example, if we transform any vector 'x' using the orthogonal matrix 'U', the length or norm of the vector remains unchanged. This is a property of orthogonal transformations; they preserve both lengths and angles. This can be seen through the equation where the transformed vector's transpose times the transformed vector equals the original vector's transpose times the original vector. Similarly, the angle between any two vectors is preserved under this transformation.

Section: Practical Implications and Further Properties

From these properties, we derive that 'U transpose times A times U equals Lambda', indicating that the matrix 'A' can be expressed as 'U times Lambda times U transpose'. Consequently, the inverse of 'A' can be represented as 'U times the inverse of Lambda times U transpose'. These forms are very useful in computations, as they simplify the manipulation of the matrix 'A'.

Furthermore, we can express 'A' and its inverse as sums involving the eigenvalues and eigenvectors. Specifically, 'A equals the sum from i equals 1 to M of lambda sub i times u sub i times u sub i transpose' and 'A inverse equals the sum from i equals 1 to M of one over lambda sub i times u sub i times u sub i transpose'. This approach not only aids in understanding the matrix better but also in practical applications such as solving systems of linear equations.

Section: Determinant and Trace

The determinant of 'A', a scalar value that can provide insights into the properties of the matrix, is the product of its eigenvalues. In other words, the determinant of 'A' equals the product of lambda sub i for i from 1 to M. Similarly, the trace of 'A', which is the sum of the elements on its main diagonal, equals the sum of its eigenvalues. Thus, the trace of 'A' equals the sum of lambda sub i for i from 1 to M. These properties are instrumental in various fields, including physics and engineering, where such matrices frequently arise.

Section: Positive Definiteness and Condition Number

A matrix 'A' is considered positive definite if for all non-zero vectors 'w', the product 'w transpose times A times w' is greater than zero. This implies that all the eigenvalues of 'A' are positive. Positive definite matrices are important in optimization problems and in ensuring stability in numerical methods. Conversely, a matrix is positive semidefinite if this product is greater than or equal to zero for all 'w', meaning all eigenvalues are non-negative.

Finally, the condition number of a matrix, which provides a measure of how well-conditioned a matrix is for inversion, is given by the square root of the ratio of the largest eigenvalue to the smallest eigenvalue. This ratio can indicate how sensitive a matrix is to numerical errors, which is significant in practical computations.

Section: Chapter Summary

1. **Introduction to Linear Algebra Properties**:
   - Discusses various matrix properties and identities assuming prior knowledge of basic linear algebra.
   - Recommends specific textbooks for deeper understanding and proofs.

2. **Matrix Identities**:
   - Key identities such as transpose and inverse properties.
   - Important relations involving the product and inverse of matrices.

3. **Traces and Determinants**:
   - Trace is the sum of diagonal elements and is cyclic in nature.
   - Determinants can be computed from the matrix elements and have specific properties, including the determinant of a product and the inverse.

4. **Matrix Derivatives**:
   - Derivatives of vectors/matrices with respect to scalars and other vectors/matrices.
   - Key results include the derivative of matrix products and inverses.

5. **Eigenvectors and Eigenvalues**:
   - Eigenvector equation and characteristic equation for finding eigenvalues.
   - Properties of symmetric matrices, including the orthogonality and orthonormality of eigenvectors.

6. **Orthogonality and Orthonormality of Eigenvectors**:
   - Eigenvectors can be chosen orthogonal, forming an orthogonal matrix 'U'.
   - 'U' satisfies 'U transpose U equals I' and 'U U transpose equals I'.

7. **Diagonalization of Matrices**:
   - Matrix 'A' can be diagonalized using eigenvalues and an orthogonal matrix 'U'.
   - Orthogonal transformations preserve vector norms and angles.

8. **Practical Implications and Further Properties**:
   - Simplifying matrix computations using eigenvalue and eigenvector decompositions.
   - Representations of 'A' and 'A inverse' using sums involving eigenvalues and eigenvectors.

9. **Determinant and Trace**:
   - Determinant and trace can be expressed in terms of eigenvalues.
   - Determinant equals the product of eigenvalues; trace equals the sum of eigenvalues.

10. **Positive Definiteness and Condition Number**:

- A matrix is positive definite if all eigenvalues are positive.
- Condition number indicates matrix sensitivity to numerical errors, calculated from the ratio of the largest to smallest eigenvalue.

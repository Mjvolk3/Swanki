for \(i=1, \ldots, M\), where \(\mathbf{u}_{i}\) is an eigenvector and \(\lambda_{i}\) is the corresponding eigenvalue. This can be viewed as a set of \(M\) simultaneous homogeneous linear equations, and the condition for a solution is that

\[
\left|\mathbf{A}-\lambda_{i} \mathbf{I}\right|=0
\]

which is known as the characteristic equation. Because this is a polynomial of order \(M\) in \(\lambda_{i}\), it must have \(M\) solutions (though these need not all be distinct). The rank of \(\mathbf{A}\) is equal to the number of non-zero eigenvalues.

Of particular interest are symmetric matrices, which arise as covariance matrices, kernel matrices, and Hessians. Symmetric matrices have the property that \(A_{i j}=A_{j i}\), or equivalently \(\mathbf{A}^{\mathrm{T}}=\mathbf{A}\). The inverse of a symmetric matrix is also symmetric, as can be seen by taking the transpose of \(\mathbf{A}^{-1} \mathbf{A}=\mathbf{I}\) and using \(\mathbf{A A}^{-1}=\mathbf{I}\) together with the symmetry of \(\mathbf{I}\).

In general, the eigenvalues of a matrix are complex numbers, but for symmetric matrices, the eigenvalues \(\lambda_{i}\) are real. This can be seen by first left-multiplying (A.29) by \(\left(\mathbf{u}_{i}^{\star}\right)^{\mathrm{T}}\), where \(\star\) denotes the complex conjugate, to give

\[
\left(\mathbf{u}_{i}^{\star}\right)^{\mathrm{T}} \mathbf{A} \mathbf{u}_{i}=\lambda_{i}\left(\mathbf{u}_{i}^{\star}\right)^{\mathrm{T}} \mathbf{u}_{i} .
\]

Next we take the complex conjugate of (A.29) and left-multiply by \(\mathbf{u}_{i}^{\mathrm{T}}\) to give

\[
\mathbf{u}_{i}^{\mathrm{T}} \mathbf{A} \mathbf{u}_{i}^{\star}=\lambda_{i}^{\star} \mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{i}^{\star}
\]

where we have used \(\mathbf{A}^{\star}=\mathbf{A}\) because we are considering only real matrices \(\mathbf{A}\). Taking the transpose of the second of these equations and using \(\mathbf{A}^{\mathrm{T}}=\mathbf{A}\), we see that the left-hand sides of the two equations are equal and hence that \(\lambda_{i}^{\star}=\lambda_{i}\), and so \(\lambda_{i}\) must be real.

The eigenvectors \(\mathbf{u}_{i}\) of a real symmetric matrix can be chosen to be orthonormal (i.e., orthogonal and of unit length) so that

\[
\mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{j}=I_{i j}
\]

where \(I_{i j}\) are the elements of the identity matrix \(\mathbf{I}\). To show this, we first left-multiply (A.29) by \(\mathbf{u}_{j}^{\mathrm{T}}\) to give

\[
\mathbf{u}_{j}^{\mathrm{T}} \mathbf{A} \mathbf{u}_{i}=\lambda_{i} \mathbf{u}_{j}^{\mathrm{T}} \mathbf{u}_{i}
\]

and hence, by exchanging the indices, we have

\[
\mathbf{u}_{i}^{\mathrm{T}} \mathbf{A} \mathbf{u}_{j}=\lambda_{j} \mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{j}
\]

We now take the transpose of the second equation and make use of the symmetry property \(\mathbf{A}^{\mathrm{T}}=\mathbf{A}\), and then subtract the two equations to give

\[
\left(\lambda_{i}-\lambda_{j}\right) \mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{j}=0
\]

Hence, for \(\lambda_{i} \neq \lambda_{j}\), we have \(\mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{j}=0\) so that \(\mathbf{u}_{i}\) and \(\mathbf{u}_{j}\) are orthogonal. If the two eigenvalues are equal, then any linear combination \(\alpha \mathbf{u}_{i}+\beta \mathbf{u}_{j}\) is also an eigenvector
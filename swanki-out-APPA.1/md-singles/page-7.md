These last two equations can also be written in the form

\[
\begin{aligned}
\mathbf{A} & =\sum_{i=1}^{M} \lambda_{i} \mathbf{u}_{i} \mathbf{u}_{i}^{\mathrm{T}} \\
\mathbf{A}^{-1} & =\sum_{i=1}^{M} \frac{1}{\lambda_{i}} \mathbf{u}_{i} \mathbf{u}_{i}^{\mathrm{T}}
\end{aligned}
\]

If we take the determinant of (A.43) and use (A.12), we obtain

\[
|\mathbf{A}|=\prod_{i=1}^{M} \lambda_{i}
\]

Similarly, taking the trace of (A.43), and using the cyclic property (A.8) of the trace operator together with \(\mathbf{U}^{\mathrm{T}} \mathbf{U}=\mathbf{I}\), we have

\[
\operatorname{Tr}(\mathbf{A})=\sum_{i=1}^{M} \lambda_{i}
\]

We leave it as an exercise for the reader to verify (A.22) by making use of the results (A.33), (A.45), (A.46), and (A.47).

A matrix \(\mathbf{A}\) is said to be positive definite, denoted by \(\mathbf{A} \succ 0\), if \(\mathbf{w}^{\mathrm{T}} \mathbf{A w}>0\) for all non-zero values of the vector w. Equivalently, a positive definite matrix has \(\lambda_{i}>\) 0 for all of its eigenvalues (as can be seen by setting \(\mathbf{w}\) to each of the eigenvectors in turn and noting that an arbitrary vector can be expanded as a linear combination of the eigenvectors). Note that having all positive elements does not necessarily mean that a matrix is that positive definite. For example, the matrix

\[
\left(\begin{array}{ll}
1 & 2 \\
3 & 4
\end{array}\right)
\]

has eigenvalues \(\lambda_{1} \simeq 5.37\) and \(\lambda_{2} \simeq-0.37\). A matrix is said to be positive semidefinite if \(\mathbf{w}^{\mathrm{T}} \mathbf{A} \mathbf{w} \geqslant 0\) holds for all values of \(\mathbf{w}\), which is denoted \(\mathbf{A} \succeq 0\) and is equivalent to \(\lambda_{i} \geqslant 0\).

The condition number of a matrix is given by

\[
\mathrm{CN}=\left(\frac{\lambda_{\max }}{\lambda_{\min }}\right)^{1 / 2}
\]

where \(\lambda_{\max }\) is the largest eigenvalue and \(\lambda_{\min }\) is the smallest eigenvalue.
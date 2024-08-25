Exercise 3.12

Exercise 3.13

\section*{Appendix A}

Chapter 16 where \(i=1, \ldots, D\). Because \(\boldsymbol{\Sigma}\) is a real, symmetric matrix, its eigenvalues will be real, and its eigenvectors can be chosen to form an orthonormal set, so that

\[
\mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{j}=I_{i j}
\]

where \(I_{i j}\) is the \(i, j\) element of the identity matrix and satisfies

\[
I_{i j}= \begin{cases}1, & \text { if } i=j \\ 0, & \text { otherwise }\end{cases}
\]

The covariance matrix \(\Sigma\) can be expressed as an expansion in terms of its eigenvectors in the form

\[
\boldsymbol{\Sigma}=\sum_{i=1}^{D} \lambda_{i} \mathbf{u}_{i} \mathbf{u}_{i}^{\mathrm{T}}
\]

and similarly the inverse covariance matrix \(\boldsymbol{\Sigma}^{-1}\) can be expressed as

\[
\boldsymbol{\Sigma}^{-1}=\sum_{i=1}^{D} \frac{1}{\lambda_{i}} \mathbf{u}_{i} \mathbf{u}_{i}^{\mathrm{T}}
\]

Substituting (3.32) into (3.27), the quadratic form becomes

\[
\Delta^{2}=\sum_{i=1}^{D} \frac{y_{i}^{2}}{\lambda_{i}}
\]

where we have defined

\[
y_{i}=\mathbf{u}_{i}^{\mathrm{T}}(\mathbf{x}-\boldsymbol{\mu})
\]

We can interpret \(\left\{y_{i}\right\}\) as a new coordinate system defined by the orthonormal vectors \(\mathbf{u}_{i}\) that are shifted and rotated with respect to the original \(x_{i}\) coordinates. Forming the vector \(\mathbf{y}=\left(y_{1}, \ldots, y_{D}\right)^{\mathrm{T}}\), we have

\[
\mathbf{y}=\mathbf{U}(\mathbf{x}-\boldsymbol{\mu})
\]

where \(\mathbf{U}\) is a matrix whose rows are given by \(\mathbf{u}_{i}^{\mathrm{T}}\). From (3.29) it follows that \(\mathbf{U}\) is an orthogonal matrix, i.e., it satisfies \(\mathbf{U} \mathbf{U}^{\mathrm{T}}=\mathbf{U}^{\mathrm{T}} \mathbf{U}=\mathbf{I}\), where \(\mathbf{I}\) is the identity matrix.

The quadratic form, and hence the Gaussian density, is constant on surfaces for which (3.33) is constant. If all the eigenvalues \(\lambda_{i}\) are positive, then these surfaces represent ellipsoids, with their centres at \(\boldsymbol{\mu}\) and their axes oriented along \(\mathbf{u}_{i}\), and with scaling factors in the directions of the axes given by \(\lambda_{i}^{1 / 2}\), as illustrated in Figure 3.3.

For the Gaussian distribution to be well defined, it is necessary for all the eigenvalues \(\lambda_{i}\) of the covariance matrix to be strictly positive, otherwise the distribution cannot be properly normalized. A matrix whose eigenvalues are strictly positive is said to be positive definite. When we discuss latent variable models, we will encounter Gaussian distributions for which one or more of the eigenvalues are zero, in
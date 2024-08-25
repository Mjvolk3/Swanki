and of the covariance matrix \(\Sigma\) given by

\[
\boldsymbol{\Sigma}=\left(\begin{array}{ll}
\boldsymbol{\Sigma}_{a a} & \boldsymbol{\Sigma}_{a b} \\
\boldsymbol{\Sigma}_{b a} & \boldsymbol{\Sigma}_{b b}
\end{array}\right)
\]

Note that the symmetry \(\boldsymbol{\Sigma}^{\mathrm{T}}=\boldsymbol{\Sigma}\) of the covariance matrix implies that \(\boldsymbol{\Sigma}_{a a}\) and \(\boldsymbol{\Sigma}_{b b}\) are symmetric and that \(\boldsymbol{\Sigma}_{b a}=\boldsymbol{\Sigma}_{a b}^{\mathrm{T}}\).

In many situations, it will be convenient to work with the inverse of the covariance matrix:

\[
\mathbf{\Lambda} \equiv \boldsymbol{\Sigma}^{-1}
\]

which is known as the precision matrix. In fact, we will see that some properties of Gaussian distributions are most naturally expressed in terms of the covariance, whereas others take a simpler form when viewed in terms of the precision. We therefore also introduce the partitioned form of the precision matrix:

\[
\boldsymbol{\Lambda}=\left(\begin{array}{ll}
\boldsymbol{\Lambda}_{a a} & \boldsymbol{\Lambda}_{a b} \\
\boldsymbol{\Lambda}_{b a} & \boldsymbol{\Lambda}_{b b}
\end{array}\right)
\]

corresponding to the partitioning (3.49) of the vector \(\mathrm{x}\). Because the inverse of a symmetric matrix is also symmetric, we see that \(\boldsymbol{\Lambda}_{a a}\) and \(\boldsymbol{\Lambda}_{b b}\) are symmetric and that \(\boldsymbol{\Lambda}_{b a}=\boldsymbol{\Lambda}_{a b}^{\mathrm{T}}\). It should be stressed at this point that, for instance, \(\boldsymbol{\Lambda}_{a a}\) is not simply given by the inverse of \(\boldsymbol{\Sigma}_{a a}\). In fact, we will shortly examine the relation between the inverse of a partitioned matrix and the inverses of its partitions.

We begin by finding an expression for the conditional distribution \(p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right)\). From the product rule of probability, we see that this conditional distribution can be evaluated from the joint distribution \(p(\mathbf{x})=p\left(\mathbf{x}_{a}, \mathbf{x}_{b}\right)\) simply by fixing \(\mathbf{x}_{b}\) to the observed value and normalizing the resulting expression to obtain a valid probability distribution over \(\mathbf{x}_{a}\). Instead of performing this normalization explicitly, we can obtain the solution more efficiently by considering the quadratic form in the exponent of the Gaussian distribution given by (3.27) and then reinstating the normalization coefficient at the end of the calculation. If we make use of the partitioning (3.49), (3.50), and (3.53), we obtain

\[
\begin{aligned}
& -\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})= \\
& \quad-\frac{1}{2}\left(\mathbf{x}_{a}-\boldsymbol{\mu}_{a}\right)^{\mathrm{T}} \boldsymbol{\Lambda}_{a a}\left(\mathbf{x}_{a}-\boldsymbol{\mu}_{a}\right)-\frac{1}{2}\left(\mathbf{x}_{a}-\boldsymbol{\mu}_{a}\right)^{\mathrm{T}} \boldsymbol{\Lambda}_{a b}\left(\mathbf{x}_{b}-\boldsymbol{\mu}_{b}\right) \\
& \quad-\frac{1}{2}\left(\mathbf{x}_{b}-\boldsymbol{\mu}_{b}\right)^{\mathrm{T}} \boldsymbol{\Lambda}_{b a}\left(\mathbf{x}_{a}-\boldsymbol{\mu}_{a}\right)-\frac{1}{2}\left(\mathbf{x}_{b}-\boldsymbol{\mu}_{b}\right)^{\mathrm{T}} \boldsymbol{\Lambda}_{b b}\left(\mathbf{x}_{b}-\boldsymbol{\mu}_{b}\right) .
\end{aligned}
\]

We see that as a function of \(\mathbf{x}_{a}\), this is again a quadratic form, and hence, the corresponding conditional distribution \(p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right)\) will be Gaussian. Because this distribution is completely characterized by its mean and its covariance, our goal will be to identify expressions for the mean and covariance of \(p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right)\) by inspection of (3.54).

This is an example of a rather common operation associated with Gaussian distributions, sometimes called 'completing the square', in which we are given a
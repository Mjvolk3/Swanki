given by

$$
\mathbf{R}=\left(\begin{array}{cc}
\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm{T}} \mathbf{L} \mathbf{A} & -\mathbf{A}^{\mathrm{T}} \mathbf{L} \\
-\mathbf{L} \mathbf{A} & \mathbf{L}
\end{array}\right)
$$

\section*{Exercise 3.23}

Exercise 3.24

Section 3.2

Section 3.2

The covariance matrix is found by taking the inverse of the precision, which can be done using the matrix inversion formula (3.60) to give

$$
\operatorname{cov}[\mathbf{z}]=\mathbf{R}^{-1}=\left(\begin{array}{cc}
\boldsymbol{\Lambda}^{-1} & \boldsymbol{\Lambda}^{-1} \mathbf{A}^{\mathrm{T}} \\
\mathbf{A} \boldsymbol{\Lambda}^{-1} & \mathbf{L}^{-1}+\mathbf{A} \boldsymbol{\Lambda}^{-1} \mathbf{A}^{\mathrm{T}}
\end{array}\right)
$$

Similarly, we can find the mean of the Gaussian distribution over z by identifying the linear terms in (3.86), which are given by

$$
\mathbf{x}^{\mathrm{T}} \boldsymbol{\Lambda} \boldsymbol{\mu}-\mathbf{x}^{\mathrm{T}} \mathbf{A}^{\mathrm{T}} \mathbf{L} \mathbf{b}+\mathbf{y}^{\mathrm{T}} \mathbf{L} \mathbf{b}=\binom{\mathbf{x}}{\mathbf{y}}^{\mathrm{T}}\binom{\boldsymbol{\Lambda} \boldsymbol{\mu}-\mathbf{A}^{\mathrm{T}} \mathbf{L} \mathbf{b}}{\mathbf{L} \mathbf{b}}
$$

Using our earlier result (3.55) obtained by completing the square over the quadratic form of a multivariate Gaussian, we find that the mean of $\mathbf{z}$ is given by

$$
\mathbb{E}[\mathbf{z}]=\mathbf{R}^{-1}\binom{\boldsymbol{\Lambda} \boldsymbol{\mu}-\mathbf{A}^{\mathrm{T}} \mathbf{L} \mathbf{b}}{\mathbf{L b}}
$$

Making use of (3.89), we then obtain

$$
\mathbb{E}[\mathbf{z}]=\binom{\boldsymbol{\mu}}{\mathbf{A} \boldsymbol{\mu}+\mathbf{b}}
$$

Next we find an expression for the marginal distribution $p(\mathbf{y})$ in which we have marginalized over $\mathbf{x}$. Recall that the marginal distribution over a subset of the components of a Gaussian random vector takes a particularly simple form when expressed in terms of the partitioned covariance matrix. Specifically, its mean and covariance are given by (3.76) and (3.77), respectively. Making use of (3.89) and (3.92), we see that the mean and covariance of the marginal distribution $p(\mathbf{y})$ are given by

$$
\begin{aligned}
\mathbb{E}[\mathbf{y}] & =\mathbf{A} \boldsymbol{\mu}+\mathbf{b} \\
\operatorname{cov}[\mathbf{y}] & =\mathbf{L}^{-1}+\mathbf{A} \mathbf{\Lambda}^{-1} \mathbf{A}^{\mathrm{T}}
\end{aligned}
$$

A special case of this result is when $\mathbf{A}=\mathbf{I}$, in which case the marginal distribution reduces to the convolution of two Gaussians, for which we see that the mean of the convolution is the sum of the means of the two Gaussians and the covariance of the convolution is the sum of their covariances.

Finally, we seek an expression for the conditional $p(\mathbf{x} \mid \mathbf{y})$. Recall that the results for the conditional distribution are most easily expressed in terms of the partitioned precision matrix, using (3.57) and (3.59). Applying these results to (3.89) and (3.92), we see that the conditional distribution $p(\mathbf{x} \mid \mathbf{y})$ has mean and covariance given by

$$
\begin{aligned}
\mathbb{E}[\mathbf{x} \mid \mathbf{y}] & =\left(\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm{T}} \mathbf{L} \mathbf{A}\right)^{-1}\left\{\mathbf{A}^{\mathrm{T}} \mathbf{L}(\mathbf{y}-\mathbf{b})+\boldsymbol{\Lambda} \boldsymbol{\mu}\right\} \\
\operatorname{cov}[\mathbf{x} \mid \mathbf{y}] & =\left(\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm{T}} \mathbf{L} \mathbf{A}\right)^{-1}
\end{aligned}
$$
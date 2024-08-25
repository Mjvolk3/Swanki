\title{
3. STANDARD DISTRIBUTIONS
}

where we have used the result (2.51) for the normalization of the univariate Gaussian. This confirms that the multivariate Gaussian (3.26) is indeed normalized.

\subsection*{3.2.2 Moments}

We now look at the moments of the Gaussian distribution and thereby provide an interpretation of the parameters \(\boldsymbol{\mu}\) and \(\boldsymbol{\Sigma}\). The expectation of \(\mathbf{x}\) under the Gaussian distribution is given by

\[
\begin{aligned}
\mathbb{E}[\mathbf{x}] & =\frac{1}{(2 \pi)^{D / 2}} \frac{1}{|\boldsymbol{\Sigma}|^{1 / 2}} \int \exp \left\{-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})\right\} \mathbf{x} \mathrm{d} \mathbf{x} \\
& =\frac{1}{(2 \pi)^{D / 2}} \frac{1}{|\boldsymbol{\Sigma}|^{1 / 2}} \int \exp \left\{-\frac{1}{2} \mathbf{z}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \mathbf{z}\right\}(\mathbf{z}+\boldsymbol{\mu}) \mathrm{d} \mathbf{z}
\end{aligned}
\]

where we have changed variables using \(\mathbf{z}=\mathbf{x}-\boldsymbol{\mu}\). Note that the exponent is an even function of the components of \(\mathbf{z}\), and because the integrals over these are taken over the range \((-\infty, \infty)\), the term in \(\mathbf{z}\) in the factor \((\mathbf{z}+\boldsymbol{\mu})\) will vanish by symmetry. Thus,

\[
\mathbb{E}[\mathbf{x}]=\boldsymbol{\mu}
\]

and so we refer to \(\boldsymbol{\mu}\) as the mean of the Gaussian distribution.

We now consider second-order moments of the Gaussian. In the univariate case, we considered the second-order moment given by \(\mathbb{E}\left[x^{2}\right]\). For the multivariate Gaussian, there are \(D^{2}\) second-order moments given by \(\mathbb{E}\left[x_{i} x_{j}\right]\), which we can group together to form the matrix \(\mathbb{E}\left[\mathbf{x x}^{\mathrm{T}}\right]\). This matrix can be written as

\[
\begin{aligned}
\mathbb{E}\left[\mathbf{x} \mathbf{x}^{\mathrm{T}}\right] & =\frac{1}{(2 \pi)^{D / 2}} \frac{1}{|\boldsymbol{\Sigma}|^{1 / 2}} \int \exp \left\{-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})\right\} \mathbf{x x}^{\mathrm{T}} \mathrm{d} \mathbf{x} \\
& =\frac{1}{(2 \pi)^{D / 2}} \frac{1}{|\boldsymbol{\Sigma}|^{1 / 2}} \int \exp \left\{-\frac{1}{2} \mathbf{z}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \mathbf{z}\right\}(\mathbf{z}+\boldsymbol{\mu})(\mathbf{z}+\boldsymbol{\mu})^{\mathrm{T}} \mathrm{d} \mathbf{z}
\end{aligned}
\]

where again we have changed variables using \(\mathbf{z}=\mathrm{x}-\boldsymbol{\mu}\). Note that the cross-terms involving \(\boldsymbol{\mu} \mathbf{z}^{\mathrm{T}}\) and \(\boldsymbol{\mu}^{\mathrm{T}} \mathbf{z}\) will again vanish by symmetry. The term \(\boldsymbol{\mu} \boldsymbol{\mu}^{\mathrm{T}}\) is constant and can be taken outside the integral, which itself is unity because the Gaussian distribution is normalized. Consider the term involving \(\mathbf{z z}^{\mathrm{T}}\). Again, we can make use of the eigenvector expansion of the covariance matrix given by (3.28), together with the completeness of the set of eigenvectors, to write

\[
\mathbf{z}=\sum_{j=1}^{D} y_{j} \mathbf{u}_{j}
\]
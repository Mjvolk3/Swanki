where \(y_{j}=\mathbf{u}_{j}^{\mathrm{T}} \mathbf{z}\), which gives

\[
\begin{aligned}
& \frac{1}{(2 \pi)^{D / 2}} \frac{1}{|\boldsymbol{\Sigma}|^{1 / 2}} \int \exp \left\{-\frac{1}{2} \mathbf{z}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \mathbf{z}\right\} \mathbf{z z}^{\mathrm{T}} \mathrm{d} \mathbf{z} \\
& =\frac{1}{(2 \pi)^{D / 2}} \frac{1}{|\boldsymbol{\Sigma}|^{1 / 2}} \sum_{i=1}^{D} \sum_{j=1}^{D} \mathbf{u}_{i} \mathbf{u}_{j}^{\mathrm{T}} \int \exp \left\{-\sum_{k=1}^{D} \frac{y_{k}^{2}}{2 \lambda_{k}}\right\} y_{i} y_{j} \mathrm{~d} \mathbf{y} \\
& =\sum_{i=1}^{D} \mathbf{u}_{i} \mathbf{u}_{i}^{\mathrm{T}} \lambda_{i}=\boldsymbol{\Sigma}
\end{aligned}
\]

where we have made use of the eigenvector equation (3.28), together with the fact that the integral on the middle line vanishes by symmetry unless \(i=j\). In the final line we have made use of the results (2.53) and (3.38), together with (3.31). Thus, we have

\[
\mathbb{E}\left[\mathbf{x x}^{\mathrm{T}}\right]=\boldsymbol{\mu} \boldsymbol{\mu}^{\mathrm{T}}+\boldsymbol{\Sigma}
\]

When defining the variance for a single random variable, we subtracted the mean before taking the second moment. Similarly, in the multivariate case it is again convenient to subtract off the mean, giving rise to the covariance of a random vector \(\mathrm{x}\) defined by

\[
\operatorname{cov}[\mathbf{x}]=\mathbb{E}\left[(\mathbf{x}-\mathbb{E}[\mathbf{x}])(\mathbf{x}-\mathbb{E}[\mathbf{x}])^{\mathrm{T}}\right]
\]

For the specific case of a Gaussian distribution, we can make use of \(\mathbb{E}[\mathbf{x}]=\boldsymbol{\mu}\), together with the result (3.46), to give

\[
\operatorname{cov}[\mathbf{x}]=\mathbf{\Sigma}
\]

Because the parameter matrix \(\boldsymbol{\Sigma}\) governs the covariance of \(\mathbf{x}\) under the Gaussian distribution, it is called the covariance matrix.

\title{
3.2.3 Limitations
}

Although the Gaussian distribution (3.26) is often used as a simple density model, it suffers from some significant limitations. Consider the number of free parameters in the distribution. A general symmetric covariance matrix \(\boldsymbol{\Sigma}\) will have \(D(D+1) / 2\) independent parameters, and there are another \(D\) independent parameters in \(\boldsymbol{\mu}\), giving \(D(D+3) / 2\) parameters in total. For large \(D\), the total number of parameters therefore grows quadratically with \(D\), and the computational task of manipulating and inverting the large matrices can become prohibitive. One way to address this problem is to use restricted forms of the covariance matrix. If we consider covariance matrices that are diagonal, so that \(\boldsymbol{\Sigma}=\operatorname{diag}\left(\sigma_{i}^{2}\right)\), we then have a total of \(2 D\) independent parameters in the density model. The corresponding contours of constant density are given by axis-aligned ellipsoids. We could further restrict the covariance matrix to be proportional to the identity matrix, \(\boldsymbol{\Sigma}=\sigma^{2} \mathbf{I}\), known as an isotropic covariance, giving \(D+1\) independent parameters in the model together with spherical surfaces of constant density. The three possibilities of general, diagonal, and isotropic covariance matrices are illustrated in Figure 3.4. Unfortunately,
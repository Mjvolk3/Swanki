We see that the dependence on \(\mathbf{x}_{b}\) has been cast into the standard quadratic form of a Gaussian distribution corresponding to the first term on the right-hand side of (3.68) plus a term that does not depend on \(\mathbf{x}_{b}\) (but that does depend on \(\mathbf{x}_{a}\) ). Thus, when we take the exponential of this quadratic form, we see that the integration over \(\mathbf{x}_{b}\) required by (3.67) will take the form

\[
\int \exp \left\{-\frac{1}{2}\left(\mathbf{x}_{b}-\boldsymbol{\Lambda}_{b b}^{-1} \mathbf{m}\right)^{\mathrm{T}} \boldsymbol{\Lambda}_{b b}\left(\mathbf{x}_{b}-\boldsymbol{\Lambda}_{b b}^{-1} \mathbf{m}\right)\right\} \mathrm{d} \mathbf{x}_{b}
\]

This integration is easily performed by noting that it is the integral over an unnormalized Gaussian, and so the result will be the reciprocal of the normalization coefficient. We know from the form of the normalized Gaussian given by (3.26) that this coefficient is independent of the mean and depends only on the determinant of the covariance matrix. Thus, by completing the square with respect to \(\mathbf{x}_{b}\), we can integrate out \(\mathbf{x}_{b}\) so that the only term remaining from the contributions on the left-hand side of (3.68) that depends on \(\mathbf{x}_{a}\) is the last term on the right-hand side of (3.68) in which \(\mathbf{m}\) is given by (3.69). Combining this term with the remaining terms from (3.54) that depend on \(\mathbf{x}_{a}\), we obtain

\[
\begin{aligned}
& \frac{1}{2}\left[\boldsymbol{\Lambda}_{b b} \boldsymbol{\mu}_{b}-\boldsymbol{\Lambda}_{b a}\left(\mathbf{x}_{a}-\boldsymbol{\mu}_{a}\right)\right]^{\mathrm{T}} \boldsymbol{\Lambda}_{b b}^{-1}\left[\boldsymbol{\Lambda}_{b b} \boldsymbol{\mu}_{b}-\boldsymbol{\Lambda}_{b a}\left(\mathbf{x}_{a}-\boldsymbol{\mu}_{a}\right)\right] \\
&-\frac{1}{2} \mathbf{x}_{a}^{\mathrm{T}} \boldsymbol{\Lambda}_{a a} \mathbf{x}_{a}+\mathbf{x}_{a}^{\mathrm{T}}\left(\boldsymbol{\Lambda}_{a a} \boldsymbol{\mu}_{a}+\boldsymbol{\Lambda}_{a b} \boldsymbol{\mu}_{b}\right)+\text { const } \\
&=-\frac{1}{2} \mathbf{x}_{a}^{\mathrm{T}}\left(\boldsymbol{\Lambda}_{a a}-\boldsymbol{\Lambda}_{a b} \boldsymbol{\Lambda}_{b b}^{-1} \boldsymbol{\Lambda}_{b a}\right) \mathbf{x}_{a} \\
&+\mathbf{x}_{a}^{\mathrm{T}}\left(\boldsymbol{\Lambda}_{a a}-\boldsymbol{\Lambda}_{a b} \boldsymbol{\Lambda}_{b b}^{-1} \boldsymbol{\Lambda}_{b a}\right) \boldsymbol{\mu}_{a}+\text { const }
\end{aligned}
\]

where 'const' denotes quantities independent of \(\mathbf{x}_{a}\). Again, by comparison with (3.55), we see that the covariance of the marginal distribution \(p\left(\mathbf{x}_{a}\right)\) is given by

\[
\boldsymbol{\Sigma}_{a}=\left(\boldsymbol{\Lambda}_{a a}-\boldsymbol{\Lambda}_{a b} \boldsymbol{\Lambda}_{b b}^{-1} \boldsymbol{\Lambda}_{b a}\right)^{-1}
\]

Similarly, the mean is given by

\[
\boldsymbol{\Sigma}_{a}\left(\boldsymbol{\Lambda}_{a a}-\boldsymbol{\Lambda}_{a b} \boldsymbol{\Lambda}_{b b}^{-1} \boldsymbol{\Lambda}_{b a}\right) \boldsymbol{\mu}_{a}=\boldsymbol{\mu}_{a}
\]

where we have used (3.72). The covariance (3.72) is expressed in terms of the partitioned precision matrix given by (3.53). We can rewrite this in terms of the corresponding partitioning of the covariance matrix given by (3.51), as we did for the conditional distribution. These partitioned matrices are related by

\[
\left(\begin{array}{ll}
\boldsymbol{\Lambda}_{a a} & \boldsymbol{\Lambda}_{a b} \\
\boldsymbol{\Lambda}_{b a} & \boldsymbol{\Lambda}_{b b}
\end{array}\right)^{-1}=\left(\begin{array}{ll}
\boldsymbol{\Sigma}_{a a} & \boldsymbol{\Sigma}_{a b} \\
\boldsymbol{\Sigma}_{b a} & \boldsymbol{\Sigma}_{b b}
\end{array}\right)
\]

Making use of (3.60), we then have

\[
\left(\boldsymbol{\Lambda}_{a a}-\boldsymbol{\Lambda}_{a b} \boldsymbol{\Lambda}_{b b}^{-1} \boldsymbol{\Lambda}_{b a}\right)^{-1}=\boldsymbol{\Sigma}_{a a}
\]
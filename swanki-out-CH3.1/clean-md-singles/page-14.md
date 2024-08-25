quadratic form defining the exponent terms in a Gaussian distribution and we need to determine the corresponding mean and covariance. Such problems can be solved straightforwardly by noting that the exponent in a general Gaussian distribution $\mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}, \boldsymbol{\Sigma})$ can be written as

$$
-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})=-\frac{1}{2} \mathbf{x}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \mathbf{x}+\mathbf{x}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}+\text { const }
$$

where 'const' denotes terms that are independent of $\mathbf{x}$, We have also made use of the symmetry of $\Sigma$. Thus, if we take our general quadratic form and express it in the form given by the right-hand side of (3.55), then we can immediately equate the matrix of coefficients entering the second-order term in $\mathrm{x}$ to the inverse covariance matrix $\boldsymbol{\Sigma}^{-1}$ and the coefficient of the linear term in $\mathrm{x}$ to $\boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}$, from which we can obtain $\boldsymbol{\mu}$.

Now let us apply this procedure to the conditional Gaussian distribution $p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right)$ for which the quadratic form in the exponent is given by (3.54). We will denote the mean and covariance of this distribution by $\boldsymbol{\mu}_{a \mid b}$ and $\boldsymbol{\Sigma}_{a \mid b}$, respectively. Consider the functional dependence of (3.54) on $\mathbf{x}_{a}$ in which $\mathbf{x}_{b}$ is regarded as a constant. If we pick out all terms that are second order in $\mathbf{x}_{a}$, we have

$$
-\frac{1}{2} \mathbf{x}_{a}^{\mathrm{T}} \boldsymbol{\Lambda}_{a a} \mathbf{x}_{a}
$$

from which we can immediately conclude that the covariance (inverse precision) of $p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right)$ is given by

$$
\boldsymbol{\Sigma}_{a \mid b}=\boldsymbol{\Lambda}_{a a}^{-1}
$$

Now consider all the terms in (3.54) that are linear in $\mathbf{x}_{a}$ :

$$
\mathbf{x}_{a}^{\mathrm{T}}\left\{\boldsymbol{\Lambda}_{a a} \boldsymbol{\mu}_{a}-\boldsymbol{\Lambda}_{a b}\left(\mathbf{x}_{b}-\boldsymbol{\mu}_{b}\right)\right\}
$$

where we have used $\boldsymbol{\Lambda}_{b a}^{\mathrm{T}}=\boldsymbol{\Lambda}_{a b}$. From our discussion of the general form (3.55), the coefficient of $\mathbf{x}_{a}$ in this expression must equal $\boldsymbol{\Sigma}_{a \mid b}^{-1} \boldsymbol{\mu}_{a \mid b}$ and, hence,

$$
\begin{aligned}
\boldsymbol{\mu}_{a \mid b} & =\boldsymbol{\Sigma}_{a \mid b}\left\{\boldsymbol{\Lambda}_{a a} \boldsymbol{\mu}_{a}-\boldsymbol{\Lambda}_{a b}\left(\mathbf{x}_{b}-\boldsymbol{\mu}_{b}\right)\right\} \\
& =\boldsymbol{\mu}_{a}-\boldsymbol{\Lambda}_{a a}^{-1} \boldsymbol{\Lambda}_{a b}\left(\mathbf{x}_{b}-\boldsymbol{\mu}_{b}\right)
\end{aligned}
$$

where we have made use of (3.57).

The results (3.57) and (3.59) are expressed in terms of the partitioned precision matrix of the original joint distribution $p\left(\mathbf{x}_{a}, \mathbf{x}_{b}\right)$. We can also express these results in terms of the corresponding partitioned covariance matrix. To do this, we make use of the following identity for the inverse of a partitioned matrix:

$$
\left(\begin{array}{ll}
\mathbf{A} & \mathbf{B} \\
\mathbf{C} & \mathbf{D}
\end{array}\right)^{-1}=\left(\begin{array}{cc}
\mathbf{M} & -\mathbf{M B D}^{-1} \\
-\mathbf{D}^{-1} \mathbf{C M} & \mathbf{D}^{-1}+\mathbf{D}^{-1} \mathbf{C M B D}^{-1}
\end{array}\right)
$$

where we have defined

$$
\mathbf{M}=\left(\mathbf{A}-\mathbf{B D}^{-1} \mathbf{C}\right)^{-1}
$$
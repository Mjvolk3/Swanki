The quantity $\mathbf{M}^{-1}$ is known as the Schur complement of the matrix on the left-hand side of (3.60) with respect to the submatrix D. Using the definition

$$
\left(\begin{array}{ll}
\boldsymbol{\Sigma}_{a a} & \boldsymbol{\Sigma}_{a b} \\
\boldsymbol{\Sigma}_{b a} & \boldsymbol{\Sigma}_{b b}
\end{array}\right)^{-1}=\left(\begin{array}{ll}
\boldsymbol{\Lambda}_{a a} & \boldsymbol{\Lambda}_{a b} \\
\boldsymbol{\Lambda}_{b a} & \boldsymbol{\Lambda}_{b b}
\end{array}\right)
$$

and making use of (3.60), we have

$$
\begin{aligned}
\boldsymbol{\Lambda}_{a a} & =\left(\boldsymbol{\Sigma}_{a a}-\boldsymbol{\Sigma}_{a b} \boldsymbol{\Sigma}_{b b}^{-1} \boldsymbol{\Sigma}_{b a}\right)^{-1} \\
\boldsymbol{\Lambda}_{a b} & =-\left(\boldsymbol{\Sigma}_{a a}-\boldsymbol{\Sigma}_{a b} \boldsymbol{\Sigma}_{b b}^{-1} \boldsymbol{\Sigma}_{b a}\right)^{-1} \boldsymbol{\Sigma}_{a b} \boldsymbol{\Sigma}_{b b}^{-1}
\end{aligned}
$$

From these we obtain the following expressions for the mean and covariance of the conditional distribution $p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right)$ :

$$
\begin{aligned}
\boldsymbol{\mu}_{a \mid b} & =\boldsymbol{\mu}_{a}+\boldsymbol{\Sigma}_{a b} \boldsymbol{\Sigma}_{b b}^{-1}\left(\mathbf{x}_{b}-\boldsymbol{\mu}_{b}\right) \\
\boldsymbol{\Sigma}_{a \mid b} & =\boldsymbol{\Sigma}_{a a}-\boldsymbol{\Sigma}_{a b} \boldsymbol{\Sigma}_{b b}^{-1} \boldsymbol{\Sigma}_{b a}
\end{aligned}
$$

Comparing (3.57) and (3.66), we see that the conditional distribution $p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right)$ takes a simpler form when expressed in terms of the partitioned precision matrix than when it is expressed in terms of the partitioned covariance matrix. Note that the mean of the conditional distribution $p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right)$, given by (3.65), is a linear function of $\mathbf{x}_{b}$ and that the covariance, given by (3.66), is independent of $\mathbf{x}_{b}$. This represents an example of a linear-Gaussian model.

\title{
3.2.5 Marginal distribution
}

We have seen that if a joint distribution $p\left(\mathbf{x}_{a}, \mathbf{x}_{b}\right)$ is Gaussian, then the conditional distribution $p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right)$ will again be Gaussian. Now we turn to a discussion of the marginal distribution given by

$$
p\left(\mathbf{x}_{a}\right)=\int p\left(\mathbf{x}_{a}, \mathbf{x}_{b}\right) \mathrm{d} \mathbf{x}_{b}
$$

which, as we will see, is also Gaussian. Once again, our strategy for calculating this distribution will be to focus on the quadratic form in the exponent of the joint distribution and thereby to identify the mean and covariance of the marginal distribution $p\left(\mathbf{x}_{a}\right)$.

The quadratic form for the joint distribution can be expressed, using the partitioned precision matrix, in the form (3.54). Our goal is to integrate out $\mathbf{x}_{b}$, which is most easily achieved by first considering the terms involving $\mathbf{x}_{b}$ and then completing the square to facilitate the integration. Picking out just those terms that involve $\mathbf{x}_{b}$, we have

$$
-\frac{1}{2} \mathbf{x}_{b}^{\mathrm{T}} \boldsymbol{\Lambda}_{b b} \mathbf{x}_{b}+\mathbf{x}_{b}^{T} \mathbf{m}=-\frac{1}{2}\left(\mathbf{x}_{b}-\boldsymbol{\Lambda}_{b b}^{-1} \mathbf{m}\right)^{\mathrm{T}} \boldsymbol{\Lambda}_{b b}\left(\mathbf{x}_{b}-\boldsymbol{\Lambda}_{b b}^{-1} \mathbf{m}\right)+\frac{1}{2} \mathbf{m}^{\mathrm{T}} \boldsymbol{\Lambda}_{b b}^{-1} \mathbf{m}
$$

where we have defined

$$
\mathbf{m}=\boldsymbol{\Lambda}_{b b} \boldsymbol{\mu}_{b}-\boldsymbol{\Lambda}_{b a}\left(\mathbf{x}_{a}-\boldsymbol{\mu}_{a}\right)
$$
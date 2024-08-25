![](https://cdn.mathpix.com/cropped/2024_06_13_54c60bf0fccf07f0954bg-1.jpg?height=510&width=561&top_left_y=199&top_left_x=730)

Figure 2.21: Change of variables from polar to Cartesian. The area of the shaded patch is \(r d r d \theta\). Adapted from Figure 3.16 of [Ric95].

\title{
2.8.4 Moments of a linear transformation
}

Suppose \(f\) is an affine function, so \(\boldsymbol{y}=\boldsymbol{A} \boldsymbol{x}+\boldsymbol{b}\). In this case, we can easily derive the mean and covariance of \(\boldsymbol{y}\) as follows. First, for the mean, we have

\[
\mathbb{E}[\boldsymbol{y}]=\mathbb{E}[\mathbf{A} \boldsymbol{x}+\boldsymbol{b}]=\mathbf{A} \boldsymbol{\mu}+\boldsymbol{b}
\]

where \(\boldsymbol{\mu}=\mathbb{E}[\boldsymbol{x}]\). If \(f\) is a scalar-valued function, \(f(\boldsymbol{x})=\boldsymbol{a}^{\top} \boldsymbol{x}+b\), the corresponding result is

\[
\mathbb{E}\left[\boldsymbol{a}^{\top} \boldsymbol{x}+b\right]=\boldsymbol{a}^{\top} \boldsymbol{\mu}+b
\]

For the covariance, we have

\[
\operatorname{Cov}[\boldsymbol{y}]=\operatorname{Cov}[\mathbf{A} \boldsymbol{x}+\boldsymbol{b}]=\mathbf{A} \boldsymbol{\Sigma} \mathbf{A}^{\top}
\]

where \(\boldsymbol{\Sigma}=\operatorname{Cov}[\boldsymbol{x}]\). We leave the proof of this as an exercise.

As a special case, if \(y=\boldsymbol{a}^{\top} \boldsymbol{x}+b\), we get

\[
\mathbb{V}[y]=\mathbb{V}\left[\boldsymbol{a}^{\top} \boldsymbol{x}+b\right]=\boldsymbol{a}^{\top} \boldsymbol{\Sigma} \boldsymbol{a}
\]

For example, to compute the variance of the sum of two scalar random variables, we can set \(\boldsymbol{a}=[1,1]\) to get

\[
\begin{aligned}
\mathbb{V}\left[x_{1}+x_{2}\right] & =\left(\begin{array}{ll}
1 & 1
\end{array}\right)\left(\begin{array}{ll}
\Sigma_{11} & \Sigma_{12} \\
\Sigma_{21} & \Sigma_{22}
\end{array}\right)\binom{1}{1} \\
& =\Sigma_{11}+\Sigma_{22}+2 \Sigma_{12}=\mathbb{V}\left[x_{1}\right]+\mathbb{V}\left[x_{2}\right]+2 \operatorname{Cov}\left[x_{1}, x_{2}\right]
\end{aligned}
\]

Note, however, that although some distributions (such as the Gaussian) are completely characterized by their mean and covariance, in general we must use the techniques described above to derive the full distribution of \(\boldsymbol{y}\).

Author: Kevin P. Murphy. (C) MIT Press. CC-BY-NC-ND license
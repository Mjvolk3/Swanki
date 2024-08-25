Thus, we obtain the intuitively satisfying result that the marginal distribution \(p\left(\mathbf{x}_{a}\right)\) has mean and covariance given by

\[
\begin{aligned}
\mathbb{E}\left[\mathbf{x}_{a}\right] & =\boldsymbol{\mu}_{a} \\
\operatorname{cov}\left[\mathbf{x}_{a}\right] & =\boldsymbol{\Sigma}_{a a}
\end{aligned}
\]

We see that for a marginal distribution, the mean and covariance are most simply expressed in terms of the partitioned covariance matrix, in contrast to the conditional distribution for which the partitioned precision matrix gives rise to simpler expressions.

Our results for the marginal and conditional distributions of a partitioned Gaussian can be summarized as follows. Given a joint Gaussian distribution \(\mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}, \boldsymbol{\Sigma})\) with \(\boldsymbol{\Lambda} \equiv \boldsymbol{\Sigma}^{-1}\) and the following partitions

\[
\begin{aligned}
\mathbf{x}=\binom{\mathbf{x}_{a}}{\mathbf{x}_{b}}, & \boldsymbol{\mu}=\binom{\boldsymbol{\mu}_{a}}{\boldsymbol{\mu}_{b}} \\
\boldsymbol{\Sigma}=\left(\begin{array}{ll}
\boldsymbol{\Sigma}_{a a} & \boldsymbol{\Sigma}_{a b} \\
\boldsymbol{\Sigma}_{b a} & \boldsymbol{\Sigma}_{b b}
\end{array}\right), & \boldsymbol{\Lambda}=\left(\begin{array}{ll}
\boldsymbol{\Lambda}_{a a} & \boldsymbol{\Lambda}_{a b} \\
\boldsymbol{\Lambda}_{b a} & \boldsymbol{\Lambda}_{b b}
\end{array}\right)
\end{aligned}
\]

then the conditional distribution is given by

\[
\begin{aligned}
p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right) & =\mathcal{N}\left(\mathbf{x} \mid \boldsymbol{\mu}_{a \mid b}, \boldsymbol{\Lambda}_{a a}^{-1}\right) \\
\boldsymbol{\mu}_{a \mid b} & =\boldsymbol{\mu}_{a}-\boldsymbol{\Lambda}_{a a}^{-1} \boldsymbol{\Lambda}_{a b}\left(\mathbf{x}_{b}-\boldsymbol{\mu}_{b}\right)
\end{aligned}
\]

and the marginal distribution is given by

\[
p\left(\mathbf{x}_{a}\right)=\mathcal{N}\left(\mathbf{x}_{a} \mid \boldsymbol{\mu}_{a}, \boldsymbol{\Sigma}_{a a}\right)
\]

We illustrate the idea of conditional and marginal distributions associated with a multivariate Gaussian using an example involving two variables in Figure 3.5.

\title{
3.2.6 Bayes' theorem
}

In Sections 3.2.4 and 3.2.5 we considered a Gaussian \(p(\mathbf{x})\) in which we partitioned the vector \(\mathbf{x}\) into two subvectors \(\mathbf{x}=\left(\mathbf{x}_{a}, \mathbf{x}_{b}\right)\) and then found expressions for the conditional distribution \(p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right)\) and the marginal distribution \(p\left(\mathbf{x}_{a}\right)\). We noted that the mean of the conditional distribution \(p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right)\) was a linear function of \(\mathbf{x}_{b}\). Here we will suppose that we are given a Gaussian marginal distribution \(p(\mathbf{x})\) and a Gaussian conditional distribution \(p(\mathbf{y} \mid \mathbf{x})\) in which \(p(\mathbf{y} \mid \mathbf{x})\) has a mean that is a linear function of \(\mathbf{x}\) and a covariance that is independent of \(\mathbf{x}\). This is an example of a linear-Gaussian model (Roweis and Ghahramani, 1999). We wish to find the marginal distribution \(p(\mathbf{y})\) and the conditional distribution \(p(\mathbf{x} \mid \mathbf{y})\). This is a structure that arises in several types of generative model and it will prove convenient to derive the general results here.

We will take the marginal and conditional distributions to be

\[
\begin{aligned}
p(\mathbf{x}) & =\mathcal{N}\left(\mathbf{x} \mid \boldsymbol{\mu}, \boldsymbol{\Lambda}^{-1}\right) \\
p(\mathbf{y} \mid \mathbf{x}) & =\mathcal{N}\left(\mathbf{y} \mid \mathbf{A} \mathbf{x}+\mathbf{b}, \mathbf{L}^{-1}\right)
\end{aligned}
\]
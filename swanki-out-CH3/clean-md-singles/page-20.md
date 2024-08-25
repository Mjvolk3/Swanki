The evaluation of this conditional distribution can be seen as an example of Bayes' theorem, in which we interpret $p(\mathbf{x})$ as a prior distribution over $\mathbf{x}$. If the variable $\mathbf{y}$ is observed, then the conditional distribution $p(\mathbf{x} \mid \mathbf{y})$ represents the corresponding posterior distribution over $\mathrm{x}$. Having found the marginal and conditional distributions, we have effectively expressed the joint distribution $p(\mathbf{z})=p(\mathbf{x}) p(\mathbf{y} \mid \mathbf{x})$ in the form $p(\mathbf{x} \mid \mathbf{y}) p(\mathbf{y})$.

These results can be summarized as follows. Given a marginal Gaussian distribution for $\mathrm{x}$ and a conditional Gaussian distribution for $\mathrm{y}$ given $\mathrm{x}$ in the form

$$
\begin{aligned}
p(\mathbf{x}) & =\mathcal{N}\left(\mathbf{x} \mid \boldsymbol{\mu}, \boldsymbol{\Lambda}^{-1}\right) \\
p(\mathbf{y} \mid \mathbf{x}) & =\mathcal{N}\left(\mathbf{y} \mid \mathbf{A} \mathbf{x}+\mathbf{b}, \mathbf{L}^{-1}\right)
\end{aligned}
$$

then the marginal distribution of $\mathbf{y}$ and the conditional distribution of $\mathbf{x}$ given $\mathbf{y}$ are given by

$$
\begin{aligned}
p(\mathbf{y}) & =\mathcal{N}\left(\mathbf{y} \mid \mathbf{A} \boldsymbol{\mu}+\mathbf{b}, \mathbf{L}^{-1}+\mathbf{A} \boldsymbol{\Lambda}^{-1} \mathbf{A}^{\mathrm{T}}\right) \\
p(\mathbf{x} \mid \mathbf{y}) & =\mathcal{N}\left(\mathbf{x} \mid \boldsymbol{\Sigma}\left\{\mathbf{A}^{\mathrm{T}} \mathbf{L}(\mathbf{y}-\mathbf{b})+\boldsymbol{\Lambda} \boldsymbol{\mu}\right\}, \boldsymbol{\Sigma}\right)
\end{aligned}
$$

where

$$
\boldsymbol{\Sigma}=\left(\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm{T}} \mathbf{L} \mathbf{A}\right)^{-1}
$$

\title{
3.2.7 Maximum likelihood
}

Given a data set $\mathbf{X}=\left(\mathbf{x}_{1}, \ldots, \mathbf{x}_{N}\right)^{\mathrm{T}}$ in which the observations $\left\{\mathbf{x}_{n}\right\}$ are assumed to be drawn independently from a multivariate Gaussian distribution, we can estimate the parameters of the distribution by maximum likelihood. The log likelihood function is given by

$$
\ln p(\mathbf{X} \mid \boldsymbol{\mu}, \boldsymbol{\Sigma})=-\frac{N D}{2} \ln (2 \pi)-\frac{N}{2} \ln |\boldsymbol{\Sigma}|-\frac{1}{2} \sum_{n=1}^{N}\left(\mathbf{x}_{n}-\boldsymbol{\mu}\right)^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}\left(\mathbf{x}_{n}-\boldsymbol{\mu}\right)
$$

By simple rearrangement, we see that the likelihood function depends on the data set only through the two quantities

$$
\sum_{n=1}^{N} \mathbf{x}_{n}, \quad \sum_{n=1}^{N} \mathbf{x}_{n} \mathbf{x}_{n}^{\mathrm{T}}
$$

These are known as the sufficient statistics for the Gaussian distribution. Using (A.19), the derivative of the $\log$ likelihood with respect to $\boldsymbol{\mu}$ is given by

$$
\frac{\partial}{\partial \boldsymbol{\mu}} \ln p(\mathbf{X} \mid \boldsymbol{\mu}, \boldsymbol{\Sigma})=\sum_{n=1}^{N} \boldsymbol{\Sigma}^{-1}\left(\mathbf{x}_{n}-\boldsymbol{\mu}\right)
$$

and setting this derivative to zero, we obtain the solution for the maximum likelihood estimate of the mean:

$$
\boldsymbol{\mu}_{\mathrm{ML}}=\frac{1}{N} \sum_{n=1}^{N} \mathbf{x}_{n}
$$
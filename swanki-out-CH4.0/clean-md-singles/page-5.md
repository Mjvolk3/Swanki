Now consider a data set of inputs $\mathbf{X}=\left\{\mathbf{x}_{1}, \ldots, \mathbf{x}_{N}\right\}$ with corresponding target values $t_{1}, \ldots, t_{N}$. We group the target variables $\left\{t_{n}\right\}$ into a column vector that we denote by $\mathbf{t}$ where the typeface is chosen to distinguish it from a single observation of a multivariate target, which would be denoted $\mathbf{t}$. Making the assumption that these data points are drawn independently from the distribution (4.8), we obtain an expression for the likelihood function, which is a function of the adjustable parameters $\mathbf{w}$ and $\sigma^{2}$ :

$$
p\left(\mathbf{t} \mid \mathbf{X}, \mathbf{w}, \sigma^{2}\right)=\prod_{n=1}^{N} \mathcal{N}\left(t_{n} \mid \mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right), \sigma^{2}\right)
$$

where we have used (4.3). Taking the logarithm of the likelihood function and making use of the standard form (2.49) for the univariate Gaussian, we have

$$
\begin{aligned}
\ln p\left(\mathbf{t} \mid \mathbf{X}, \mathbf{w}, \sigma^{2}\right) & =\sum_{n=1}^{N} \ln \mathcal{N}\left(t_{n} \mid \mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right), \sigma^{2}\right) \\
& =-\frac{N}{2} \ln \sigma^{2}-\frac{N}{2} \ln (2 \pi)-\frac{1}{\sigma^{2}} E_{D}(\mathbf{w})
\end{aligned}
$$

where the sum-of-squares error function is defined by

$$
E_{D}(\mathbf{w})=\frac{1}{2} \sum_{n=1}^{N}\left\{t_{n}-\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right)\right\}^{2}
$$

The first two terms in (4.10) can be treated as constants when determining $\mathbf{w}$ because they are independent of $\mathbf{w}$. Therefore, as we saw previously, maximizing the likelihood function under a Gaussian noise distribution is equivalent to minimizing the sum-of-squares error function (4.11).

\title{
4.1.3 Maximum likelihood
}

Having written down the likelihood function, we can use maximum likelihood to determine $\mathbf{w}$ and $\sigma^{2}$. Consider first the maximization with respect to $\mathbf{w}$. The gradient of the $\log$ likelihood function (4.10) with respect to $\mathrm{w}$ takes the form

$$
\nabla_{\mathbf{w}} \ln p\left(\mathbf{t} \mid \mathbf{X}, \mathbf{w}, \sigma^{2}\right)=\frac{1}{\sigma^{2}} \sum_{n=1}^{N}\left\{t_{n}-\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right)\right\} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right)^{\mathrm{T}}
$$

Setting this gradient to zero gives

$$
0=\sum_{n=1}^{N} t_{n} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right)^{\mathrm{T}}-\mathbf{w}^{\mathrm{T}}\left(\sum_{n=1}^{N} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right) \boldsymbol{\phi}\left(\mathbf{x}_{n}\right)^{\mathrm{T}}\right)
$$

Solving for $\mathbf{w}$ we obtain

$$
\mathbf{w}_{\mathrm{ML}}=\left(\boldsymbol{\Phi}^{\mathrm{T}} \boldsymbol{\Phi}\right)^{-1} \boldsymbol{\Phi}^{\mathrm{T}} \mathbf{t}
$$
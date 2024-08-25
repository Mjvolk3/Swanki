## What is the likelihood function for the given data set of inputs  $\mathbf{X}$ and target values  $\mathbf{t}$?

The likelihood function for the given data set is:

$$
p\left(\mathbf{t} \mid \mathbf{X}, \mathbf{w}, \sigma^{2}\right)=\prod_{n=1}^{N} \mathcal{N}\left(t_{n} \mid \mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right), \sigma^{2}\right)
$$


- #statistics, #probability.likelihood-function


## What is the expression for the log-likelihood function $\ln p\left(\mathbf{t} \mid \mathbf{X}, \mathbf{w}, \sigma^{2}\right)$ for the given data set?

The log-likelihood function is given by:

$$
\begin{aligned}
\ln p\left(\mathbf{t} \mid \mathbf{X}, \mathbf{w}, \sigma^{2}\right) & =\sum_{n=1}^{N} \ln \mathcal{N}\left(t_{n} \mid \mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right), \sigma^{2}\right) \\
& =-\frac{N}{2} \ln \sigma^{2}-\frac{N}{2} \ln (2 \pi)-\frac{1}{\sigma^{2}} E_{D}(\mathbf{w})
\end{aligned}
$$

where $E_{D}(\mathbf{w})$ is the sum-of-squares error function.


- #statistics, #probability.log-likelihood


## Define the sum-of-squares error function $E_{D}(\mathbf{w})$ used in the log-likelihood function.

The sum-of-squares error function $E_{D}(\mathbf{w})$ is defined by:

$$
E_{D}(\mathbf{w})=\frac{1}{2} \sum_{n=1}^{N}\left\{t_{n}-\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right)\right\}^{2}
$$


- #statistics, #error.sum-of-squares-error


## What is the gradient of the log-likelihood function with respect to $\mathbf{w}$?

The gradient of the log-likelihood function with respect to $\mathbf{w}$ is:

$$
\nabla_{\mathbf{w}} \ln p\left(\mathbf{t} \mid \mathbf{X}, \mathbf{w}, \sigma^{2}\right)=\frac{1}{\sigma^{2}} \sum_{n=1}^{N}\left\{t_{n}-\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right)\right\} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right)^{\mathrm{T}}
$$


- #statistics, #optimization.gradient


## How do you determine the parameter $\mathbf{w}$ that maximizes the likelihood function?

Setting the gradient to zero gives:

$$
0=\sum_{n=1}^{N} t_{n} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right)^{\mathrm{T}}-\mathbf{w}^{\mathrm{T}}\left(\sum_{n=1}^{N} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right) \boldsymbol{\phi}\left(\mathbf{x}_{n}\right)^{\mathrm{T}}\right)
$$

Solving for $\mathbf{w}$ we obtain:

$$
\mathbf{w}_{\mathrm{ML}}=\left(\boldsymbol{\Phi}^{\mathrm{T}} \boldsymbol{\Phi}\right)^{-1} \boldsymbol{\Phi}^{\mathrm{T}} \mathbf{t}
$$


- #optimization, #statistics.maximum-likelihood


## Why are the first two terms in $\ln p\left(\mathbf{t} \mid \mathbf{X}, \mathbf{w}, \sigma^{2}\right)$ treated as constants when determining $\mathbf{w}$?

The first two terms in

$$
\ln p\left(\mathbf{t} \mid \mathbf{X}, \mathbf{w}, \sigma^{2}\right) = -\frac{N}{2} \ln \sigma^{2} - \frac{N}{2} \ln (2 \pi) - \frac{1}{\sigma^{2}} E_{D}(\mathbf{w})
$$

are independent of $\mathbf{w}$, allowing us to treat them as constants while maximizing the likelihood function.


- #statistics, #optimization.constants-in-likelihood
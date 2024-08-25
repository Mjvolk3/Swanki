## Define the design matrix $\boldsymbol{\Phi}$ in the least-squares problem.

$$
\boldsymbol{\Phi}=\left(\begin{array}{cccc}
\phi_{0}\left(\mathbf{x}_{1}\right) & \phi_{1}\left(\mathbf{x}_{1}\right) & \cdots & \phi_{M-1}\left(\mathbf{x}_{1}\right) \\
\phi_{0}\left(\mathbf{x}_{2}\right) & \phi_{1}\left(\mathbf{x}_{2}\right) & \cdots & \phi_{M-1}\left(\mathbf{x}_{2}\right) \\
\vdots & \vdots & \ddots & \vdots \\
\phi_{0}\left(\mathbf{x}_{N}\right) & \phi_{1}\left(\mathbf{x}_{N}\right) & \cdots & \phi_{M-1}\left(\mathbf{x}_{N}\right)
\end{array}\right)
$$

- #linear-algebra, #matrix-operations

## What is the Moore-Penrose pseudo-inverse of a matrix $\boldsymbol{\Phi}$, and how is it defined?

The Moore-Penrose pseudo-inverse of $\boldsymbol{\Phi}$ is given by:

$$
\boldsymbol{\Phi}^{\dagger} \equiv\left(\boldsymbol{\Phi}^{\mathrm{T}} \boldsymbol{\Phi}\right)^{-1} \boldsymbol{\Phi}^{\mathrm{T}}
$$

It acts as a generalization of the matrix inverse for non-square matrices. For square and invertible matrices, it simplifies as $\boldsymbol{\Phi}^{\dagger} = \boldsymbol{\Phi}^{-1}$. 

- #linear-algebra, #pseudo-inverse

## Derive the value of $w_{0}$ by setting the derivative of $E_D(\mathbf{w})$ with respect to $w_{0}$ equal to zero.

The error function is given by:

$$
E_{D}(\mathbf{w})=\frac{1}{2} \sum_{n=1}^{N}\left\{t_{n}-w_{0}-\sum_{j=1}^{M-1} w_{j} \phi_{j}\left(\mathbf{x}_{n}\right)\right\}^{2}
$$

Setting its derivative wrt \(w_0\) to zero:

\[
\frac{\partial E_D(\mathbf{w})}{\partial w_0} = -\sum_{n=1}^N (t_n - w_0 - \sum_{j=1}^{M-1} w_j \phi_j(\mathbf{x}_n)) = 0
\]

Solving for $w_0$:

$$
w_{0}=\bar{t}-\sum_{j=1}^{M-1} w_{j} \overline{\phi_{j}}
$$

- #optimization, #derivation

## Define the terms $\bar{t}$ and $\overline{\phi_{j}}$ in the context of the least-squares problem.

$$
\bar{t}=\frac{1}{N} \sum_{n=1} t_{n}, \quad \overline{\phi_{j}}=\frac{1}{N} \sum_{n=1}^N \phi_{j}\left(\mathbf{x}_{n}\right)
$$

Here, $\bar{t}$ is the average of the target values in the training set, while $\overline{\phi_{j}}$ is the average of the basis function values over the training set.

- #statistics, #terminology

## What does the bias parameter $w_{0}$ compensate for in the least-squares problem?

The bias \(w_0\) compensates for the difference between the averages of the target values and the weighted sum of the averages of the basis function values:

$$
w_{0}=\bar{t}-\sum_{j=1}^{M-1} w_{j} \overline{\phi_{j}}
$$

- #regression, #parameter-interpretation

## How is the maximum likelihood estimate of the variance $\sigma^2$ in the least-squares problem derived?

The maximum likelihood estimate of the variance $\sigma^2$ is given by the residual variance:

$$
\sigma_{\mathrm{ML}}^{2}=\frac{1}{N} \sum_{n=1}^{N}\left\{t_{n}-\mathbf{w}_{\mathrm{ML}}^{\mathrm{T}} \phi\left(\mathbf{x}_{n}\right)\right\}^{2}
$$

This represents the variance of the target values around the regression fit.

- #statistics, #maximum-likelihood, #variance
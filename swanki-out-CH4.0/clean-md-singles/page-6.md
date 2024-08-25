which are known as the normal equations for the least-squares problem. Here $\boldsymbol{\Phi}$ is an $N \times M$ matrix, called the design matrix, whose elements are given by $\Phi_{n j}=\phi_{j}\left(\mathbf{x}_{n}\right)$, so that

$$
\boldsymbol{\Phi}=\left(\begin{array}{cccc}
\phi_{0}\left(\mathbf{x}_{1}\right) & \phi_{1}\left(\mathbf{x}_{1}\right) & \cdots & \phi_{M-1}\left(\mathbf{x}_{1}\right) \\
\phi_{0}\left(\mathbf{x}_{2}\right) & \phi_{1}\left(\mathbf{x}_{2}\right) & \cdots & \phi_{M-1}\left(\mathbf{x}_{2}\right) \\
\vdots & \vdots & \ddots & \vdots \\
\phi_{0}\left(\mathbf{x}_{N}\right) & \phi_{1}\left(\mathbf{x}_{N}\right) & \cdots & \phi_{M-1}\left(\mathbf{x}_{N}\right)
\end{array}\right)
$$

The quantity

$$
\boldsymbol{\Phi}^{\dagger} \equiv\left(\boldsymbol{\Phi}^{\mathrm{T}} \boldsymbol{\Phi}\right)^{-1} \boldsymbol{\Phi}^{\mathrm{T}}
$$

is known as the Moore-Penrose pseudo-inverse of the matrix $\boldsymbol{\Phi}$ (Rao and Mitra, 1971; Golub and Van Loan, 1996). It can be regarded as a generalization of the notion of a matrix inverse to non-square matrices. Indeed, if $\boldsymbol{\Phi}$ is square and invertible, then using the property $(\mathbf{A B})^{-1}=\mathbf{B}^{-1} \mathbf{A}^{-1}$ we see that $\boldsymbol{\Phi}^{\dagger} \equiv \boldsymbol{\Phi}^{-1}$.

At this point, we can gain some insight into the role of the bias parameter $w_{0}$. If we make the bias parameter explicit, then the error function (4.11) becomes

$$
E_{D}(\mathbf{w})=\frac{1}{2} \sum_{n=1}^{N}\left\{t_{n}-w_{0}-\sum_{j=1}^{M-1} w_{j} \phi_{j}\left(\mathbf{x}_{n}\right)\right\}^{2}
$$

Setting the derivative with respect to $w_{0}$ equal to zero and solving for $w_{0}$, we obtain

$$
w_{0}=\bar{t}-\sum_{j=1}^{M-1} w_{j} \overline{\phi_{j}}
$$

where we have defined

$$
\bar{t}=\frac{1}{N} \sum_{n=1}^{N} t_{n}, \quad \overline{\phi_{j}}=\frac{1}{N} \sum_{n=1}^{N} \phi_{j}\left(\mathbf{x}_{n}\right)
$$

Thus, the bias $w_{0}$ compensates for the difference between the averages (over the training set) of the target values and the weighted sum of the averages of the basis function values.

We can also maximize the log likelihood function (4.10) with respect to the variance $\sigma^{2}$, giving

$$
\sigma_{\mathrm{ML}}^{2}=\frac{1}{N} \sum_{n=1}^{N}\left\{t_{n}-\mathbf{w}_{\mathrm{ML}}^{\mathrm{T}} \phi\left(\mathbf{x}_{n}\right)\right\}^{2}
$$

and so we see that the maximum likelihood value of the variance parameter is given by the residual variance of the target values around the regression function.
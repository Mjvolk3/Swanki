Figure 3.7 Example of a Gaussian mixture distribution in one dimension showing three Gaussians (each scaled by a coefficient) in blue and their sum in red.

![](https://cdn.mathpix.com/cropped/2024_05_13_7914fb982b6a4f2206b4g-1.jpg?height=416&width=606&top_left_y=217&top_left_x=1055)

this proves to be the case, as can be seen from Figure 3.6(b). Such superpositions, formed by taking linear combinations of more basic distributions such as Gaussians, can be formulated as probabilistic models known as mixture distributions. In this section we will consider Gaussians to illustrate the framework of mixture models. More generally, mixture models can comprise linear combinations of other distributions, for example mixtures of Bernoulli distributions for binary variables. In Figure 3.7 we see that a linear combination of Gaussians can give rise to very complex densities. By using a sufficient number of Gaussians and by adjusting their means and covariances as well as the coefficients in the linear combination, almost any continuous distribution can be approximated to arbitrary accuracy.

We therefore consider a superposition of $K$ Gaussian densities of the form

$$
p(\mathbf{x})=\sum_{k=1}^{K} \pi_{k} \mathcal{N}\left(\mathbf{x} \mid \boldsymbol{\mu}_{k}, \boldsymbol{\Sigma}_{k}\right)
$$

which is called a mixture of Gaussians. Each Gaussian density $\mathcal{N}\left(\mathbf{x} \mid \boldsymbol{\mu}_{k}, \boldsymbol{\Sigma}_{k}\right)$ is called a component of the mixture and has its own mean $\boldsymbol{\mu}_{k}$ and covariance $\boldsymbol{\Sigma}_{k}$. Contour and surface plots for a Gaussian mixture in two dimensions having three components are shown in Figure 3.8.

The parameters $\pi_{k}$ in (3.111) are called mixing coefficients. If we integrate both sides of (3.111) with respect to $\mathbf{x}$, and note that both $p(\mathbf{x})$ and the individual Gaussian components are normalized, we obtain

$$
\sum_{k=1}^{K} \pi_{k}=1
$$

Also, given that $\mathcal{N}\left(\mathbf{x} \mid \boldsymbol{\mu}_{k}, \boldsymbol{\Sigma}_{k}\right) \geqslant 0$, a sufficient condition for the requirement $p(\mathbf{x}) \geqslant$ 0 is that $\pi_{k} \geqslant 0$ for all $k$. Combining this with the condition (3.112), we obtain

$$
0 \leqslant \pi_{k} \leqslant 1
$$

We can therefore see that the mixing coefficients satisfy the requirements to be probabilities, and we will show that this probabilistic interpretation of mixture distributions is very powerful.
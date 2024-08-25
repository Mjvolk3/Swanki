![](https://cdn.mathpix.com/cropped/2024_05_13_bbb54caf8784589780acg-1.jpg?height=510&width=518&top_left_y=214&top_left_x=110)

(a)

![](https://cdn.mathpix.com/cropped/2024_05_13_bbb54caf8784589780acg-1.jpg?height=452&width=510&top_left_y=214&top_left_x=624)

$x_{1}$

(b)

![](https://cdn.mathpix.com/cropped/2024_05_13_bbb54caf8784589780acg-1.jpg?height=427&width=435&top_left_y=292&top_left_x=1148)

(c)

Figure 3.8 Illustration of a mixture of three Gaussians in a two-dimensional space. (a) Contours of constant density for each of the mixture components, in which the three components are denoted red, blue, and green, and the values of the mixing coefficients are shown below each component. (b) Contours of the marginal probability density $p(\mathbf{x})$ of the mixture distribution. (c) A surface plot of the distribution $p(\mathbf{x})$.

From the sum and product rules of probability, the marginal density can be written as

$$
p(\mathbf{x})=\sum_{k=1}^{K} p(k) p(\mathbf{x} \mid k)
$$

which is equivalent to (3.111) in which we can view $\pi_{k}=p(k)$ as the prior probability of picking the $k$ th component, and the density $\mathcal{N}\left(\mathbf{x} \mid \boldsymbol{\mu}_{k}, \boldsymbol{\Sigma}_{k}\right)=p(\mathbf{x} \mid k)$ as the probability of $\mathrm{x}$ conditioned on $k$. As we will see in later chapters, an important role is played by the corresponding posterior probabilities $p(k \mid \mathbf{x})$, which are also known as responsibilities. From Bayes' theorem, these are given by

$$
\begin{aligned}
\gamma_{k}(\mathbf{x}) & \equiv p(k \mid \mathbf{x}) \\
& =\frac{p(k) p(\mathbf{x} \mid k)}{\sum_{l} p(l) p(\mathbf{x} \mid l)} \\
& =\frac{\pi_{k} \mathcal{N}\left(\mathbf{x} \mid \boldsymbol{\mu}_{k}, \boldsymbol{\Sigma}_{k}\right)}{\sum_{l} \pi_{l} \mathcal{N}\left(\mathbf{x} \mid \boldsymbol{\mu}_{l}, \boldsymbol{\Sigma}_{l}\right)}
\end{aligned}
$$

The form of the Gaussian mixture distribution is governed by the parameters $\pi$, $\boldsymbol{\mu}$, and $\boldsymbol{\Sigma}$, where we have used the notation $\boldsymbol{\pi} \equiv\left\{\pi_{1}, \ldots, \pi_{K}\right\}, \boldsymbol{\mu} \equiv\left\{\boldsymbol{\mu}_{1}, \ldots, \boldsymbol{\mu}_{K}\right\}$, and $\boldsymbol{\Sigma} \equiv\left\{\boldsymbol{\Sigma}_{1}, \ldots \boldsymbol{\Sigma}_{K}\right\}$. One way to set the values of these parameters is to use maximum likelihood. From (3.111), the log of the likelihood function is given by

$$
\ln p(\mathbf{X} \mid \boldsymbol{\pi}, \boldsymbol{\mu}, \boldsymbol{\Sigma})=\sum_{n=1}^{N} \ln \left\{\sum_{k=1}^{K} \pi_{k} \mathcal{N}\left(\mathbf{x}_{n} \mid \boldsymbol{\mu}_{k}, \boldsymbol{\Sigma}_{k}\right)\right\}
$$

where $\mathbf{X}=\left\{\mathbf{x}_{1}, \ldots, \mathbf{x}_{N}\right\}$. We immediately see that the situation is now much more complex than with a single Gaussian, due to the summation over $k$ inside the log-
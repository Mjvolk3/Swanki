Figure 6.18 The mixture density network can represent general conditional probability densities \(p(\mathbf{t} \mid \mathbf{x})\) by considering a parametric mixture model for the distribution of \(t\) whose parameters are determined by the outputs of a neural network that takes \(\mathrm{x}\) as its input vector.

![](https://cdn.mathpix.com/cropped/2024_05_26_fdc10e06182b216dcb8fg-1.jpg?height=442&width=952&top_left_y=221&top_left_x=696)

both the mixing coefficients as well as the component densities are flexible functions of the input vector \(\mathbf{x}\), giving rise to a mixture density network. For any given value of \(\mathbf{x}\), the mixture model provides a general formalism for modelling an arbitrary conditional density function \(p(\mathbf{t} \mid \mathbf{x})\). Provided we consider a sufficiently flexible network, we then have a framework for approximating arbitrary conditional distributions.

Here we will develop the model explicitly for Gaussian components, so that

\[
p(\mathbf{t} \mid \mathbf{x})=\sum_{k=1}^{K} \pi_{k}(\mathbf{x}) \mathcal{N}\left(\mathbf{t} \mid \boldsymbol{\mu}_{k}(\mathbf{x}), \sigma_{k}^{2}(\mathbf{x})\right)
\]

This is an example of a heteroscedastic model in which the noise variance on the data is a function of the input vector \(\mathbf{x}\). Instead of Gaussians, we can use other distributions for the components, such as Bernoulli distributions if the target variables are binary rather than continuous. We have also specialized to the case of isotropic covariances for the components, although the mixture density network can readily be extended to allow for general covariance matrices by representing the covariances using a Cholesky factorization (Williams, 1996). Even with isotropic components, the conditional distribution \(p(\mathbf{t} \mid \mathbf{x})\) does not assume factorization with respect to the components of \(t\) (in contrast to the standard sum-of-squares regression model) as a consequence of the mixture distribution.

We now take the various parameters of the mixture model, namely the mixing coefficients \(\pi_{k}(\mathbf{x})\), the means \(\boldsymbol{\mu}_{k}(\mathbf{x})\), and the variances \(\sigma_{k}^{2}(\mathbf{x})\), to be governed by the outputs of a neural network that takes \(\mathrm{x}\) as its input. The structure of this mixture density network is illustrated in Figure 6.18. The mixture density network is closely related to the mixture-of-experts model (Jacobs et al., 1991). The principal difference is that a mixture of experts has independent parameters for each component model in the mixture, whereas in a mixture density network, the same function is used to predict the parameters of all the component densities as well as the mixing coefficients, and so the nonlinear hidden units are shared amongst the input-dependent functions.

The neural network in Figure 6.18 can, for example, be a two-layer network having sigmoidal \((\tanh )\) hidden units. If there are \(K\) components in the mixture model (6.38), and if \(\mathbf{t}\) has \(L\) components, then the network will have \(K\) output-
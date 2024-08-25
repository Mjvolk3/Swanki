2 classes) or softmax ( \(K \geqslant 2\) classes) activation functions. These are particular cases of a more general result obtained by assuming that the class-conditional densities \(p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)\) are members of the subset of the exponential family of distributions given by

\[
p\left(\mathbf{x} \mid \boldsymbol{\lambda}_{k}, s\right)=\frac{1}{s} h\left(\frac{1}{s} \mathbf{x}\right) g\left(\boldsymbol{\lambda}_{k}\right) \exp \left\{\frac{1}{s} \boldsymbol{\lambda}_{k}^{\mathrm{T}} \mathbf{x}\right\}
\]

Here the scaling parameter \(s\) is shared across all the classes.

For the two-class problem, we substitute this expression for the class-conditional densities into (5.41) and we see that the posterior class probability is again given by a logistic sigmoid acting on a linear function \(a(\mathbf{x})\), which is given by

\[
a(\mathbf{x})=\left(\boldsymbol{\lambda}_{1}-\boldsymbol{\lambda}_{2}\right)^{\mathrm{T}} \mathbf{x}+\ln g\left(\boldsymbol{\lambda}_{1}\right)-\ln g\left(\boldsymbol{\lambda}_{2}\right)+\ln p\left(\mathcal{C}_{1}\right)-\ln p\left(\mathcal{C}_{2}\right)
\]

Similarly, for the \(K\)-class problem, we substitute the class-conditional density expression into (5.46) to give

\[
a_{k}(\mathbf{x})=\boldsymbol{\lambda}_{k}^{\mathrm{T}} \mathbf{x}+\ln g\left(\boldsymbol{\lambda}_{k}\right)+\ln p\left(\mathcal{C}_{k}\right)
\]

and so again is a linear function of \(\mathbf{x}\).

\title{
5.4. Discriminative Classifiers
}

For the two-class classification problem, we have seen that the posterior probability of class \(\mathcal{C}_{1}\) can be written as a logistic sigmoid acting on a linear function of \(\mathbf{x}\), for a wide choice of class-conditional distributions \(p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)\) from the exponential family. Similarly, for the multi-class case, the posterior probability of class \(\mathcal{C}_{k}\) is given by a softmax transformation of linear functions of \(\mathbf{x}\). For specific choices of the class-conditional densities \(p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)\), we have used maximum likelihood to determine the parameters of the densities as well as the class priors \(p\left(\mathcal{C}_{k}\right)\) and then used Bayes' theorem to find the posterior class probabilities. This represents an example of generative modelling, because we could take such a model and generate synthetic data by drawing values of \(\mathbf{x}\) from the marginal distribution \(p(\mathbf{x})\) or from any of the class-conditional densities \(p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)\).

However, an alternative approach is to use the functional form of the generalized linear model explicitly and to determine its parameters directly by using maximum likelihood. In this direct approach, we maximize a likelihood function defined through the conditional distribution \(p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)\), which represents a form of discriminative probabilistic modelling. One advantage of the discriminative approach is that there will typically be fewer learnable parameters to be determined, as we will see shortly. It may also lead to improved predictive performance, particularly when the assumed forms for the class-conditional densities represent a poor approximation to the true distributions.
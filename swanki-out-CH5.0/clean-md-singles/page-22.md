However, it will have significance provided $a(\mathbf{x})$ has a constrained functional form. We will shortly consider situations in which $a(\mathbf{x})$ is a linear function of $\mathbf{x}$, in which case the posterior probability is governed by a generalized linear model.

If there are $K>2$ classes, we have

$$
\begin{aligned}
p\left(\mathcal{C}_{k} \mid \mathbf{x}\right) & =\frac{p\left(\mathbf{x} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right)}{\sum_{j} p\left(\mathbf{x} \mid \mathcal{C}_{j}\right) p\left(\mathcal{C}_{j}\right)} \\
& =\frac{\exp \left(a_{k}\right)}{\sum_{j} \exp \left(a_{j}\right)},
\end{aligned}
$$

which is known as the normalized exponential and can be regarded as a multi-class generalization of the logistic sigmoid. Here the quantities $a_{k}$ are defined by

$$
a_{k}=\ln \left(p\left(\mathbf{x} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right)\right)
$$

The normalized exponential is also known as the softmax function, as it represents a smoothed version of the ' $m$ max' function because, if $a_{k} \gg a_{j}$ for all $j \neq k$, then $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right) \simeq 1$, and $p\left(\mathcal{C}_{j} \mid \mathbf{x}\right) \simeq 0$.

We now investigate the consequences of choosing specific forms for the classconditional densities, looking first at continuous input variables $\mathbf{x}$ and then discussing briefly discrete inputs.

\title{
5.3.1 Continuous inputs
}

Let us assume that the class-conditional densities are Gaussian. We will then explore the resulting form for the posterior probabilities. To start with, we will assume that all classes share the same covariance matrix $\boldsymbol{\Sigma}$. Thus, the density for class $\mathcal{C}_{k}$ is given by

$$
p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)=\frac{1}{(2 \pi)^{D / 2}} \frac{1}{|\boldsymbol{\Sigma}|^{1 / 2}} \exp \left\{-\frac{1}{2}\left(\mathbf{x}-\boldsymbol{\mu}_{k}\right)^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}\left(\mathbf{x}-\boldsymbol{\mu}_{k}\right)\right\}
$$

First, suppose that we have two classes. From (5.40) and (5.41), we have

$$
p\left(\mathcal{C}_{1} \mid \mathbf{x}\right)=\sigma\left(\mathbf{w}^{\mathrm{T}} \mathbf{x}+w_{0}\right)
$$

where we have defined

$$
\begin{aligned}
\mathbf{w} & =\boldsymbol{\Sigma}^{-1}\left(\boldsymbol{\mu}_{1}-\boldsymbol{\mu}_{2}\right) \\
w_{0} & =-\frac{1}{2} \boldsymbol{\mu}_{1}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}_{1}+\frac{1}{2} \boldsymbol{\mu}_{2}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}_{2}+\ln \frac{p\left(\mathcal{C}_{1}\right)}{p\left(\mathcal{C}_{2}\right)}
\end{aligned}
$$

We see that the quadratic terms in $\mathrm{x}$ from the exponents of the Gaussian densities have cancelled (due to the assumption of common covariance matrices), leading to a linear function of $\mathrm{x}$ in the argument of the logistic sigmoid. This result is illustrated for a two-dimensional input space $\mathrm{x}$ in Figure 5.13. The resulting decision boundaries correspond to surfaces along which the posterior probabilities $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$
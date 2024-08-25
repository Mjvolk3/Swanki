$$
\begin{aligned}
\boldsymbol{\eta} & =\binom{\mu / \sigma^{2}}{-1 / 2 \sigma^{2}} \\
\mathbf{u}(x) & =\binom{x}{x^{2}} \\
h(\mathbf{x}) & =(2 \pi)^{-1 / 2} \\
g(\boldsymbol{\eta}) & =\left(-2 \eta_{2}\right)^{1 / 2} \exp \left(\frac{\eta_{1}^{2}}{4 \eta_{2}}\right)
\end{aligned}
$$

Finally, we shall sometimes make use of a restricted form of (3.138) in which we choose $\mathbf{u}(\mathrm{x})=\mathrm{x}$. However, this can be somewhat generalized by noting that if $f(\mathbf{x})$ is a normalized density then

$$
\frac{1}{s} f\left(\frac{1}{s} \mathbf{x}\right)
$$

is also a normalized density, where $s>0$ is a scale parameter. Combining these, we arrive at a restricted set of exponential family class-conditional densities of the form

$$
p\left(\mathbf{x} \mid \boldsymbol{\lambda}_{k}, s\right)=\frac{1}{s} h\left(\frac{1}{s} \mathbf{x}\right) g\left(\boldsymbol{\lambda}_{k}\right) \exp \left\{\frac{1}{s} \boldsymbol{\lambda}_{k}^{\mathrm{T}} \mathbf{x}\right\}
$$

Note that we are allowing each class to have its own parameter vector $\boldsymbol{\lambda}_{k}$ but we are assuming that the classes share the same scale parameter $s$.

\title{
3.4.1 Sufficient statistics
}

Let us now consider the problem of estimating the parameter vector $\boldsymbol{\eta}$ in the general exponential family distribution (3.138) using the technique of maximum likelihood. Taking the gradient of both sides of (3.139) with respect to $\boldsymbol{\eta}$, we have

$$
\begin{aligned}
& \nabla g(\boldsymbol{\eta}) \int h(\mathbf{x}) \exp \left\{\boldsymbol{\eta}^{\mathrm{T}} \mathbf{u}(\mathbf{x})\right\} \mathrm{d} \mathbf{x} \\
& \quad+g(\boldsymbol{\eta}) \int h(\mathbf{x}) \exp \left\{\boldsymbol{\eta}^{\mathrm{T}} \mathbf{u}(\mathbf{x})\right\} \mathbf{u}(\mathbf{x}) \mathrm{d} \mathbf{x}=0
\end{aligned}
$$

Rearranging and making use again of (3.139) then gives

$$
-\frac{1}{g(\boldsymbol{\eta})} \nabla g(\boldsymbol{\eta})=g(\boldsymbol{\eta}) \int h(\mathbf{x}) \exp \left\{\boldsymbol{\eta}^{\mathrm{T}} \mathbf{u}(\mathbf{x})\right\} \mathbf{u}(\mathbf{x}) \mathrm{d} \mathbf{x}=\mathbb{E}[\mathbf{u}(\mathbf{x})]
$$

We therefore obtain the result

$$
-\nabla \ln g(\boldsymbol{\eta})=\mathbb{E}[\mathbf{u}(\mathbf{x})]
$$

Note that the covariance of $\mathbf{u}(\mathbf{x})$ can be expressed in terms of the second derivatives of $g(\boldsymbol{\eta})$, and similarly for higher-order moments. Thus, provided we can normalize a distribution from the exponential family, we can always find its moments by simple differentiation.
```markdown
## Define the normalized exponential provided in the text chunk.

The normalized exponential is given by:

$$
\begin{aligned}
p\left(\mathcal{C}_{k} \mid \mathbf{x}\right) & =\frac{p\left(\mathbf{x} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right)}{\sum_{j} p\left(\mathbf{x} \mid \mathcal{C}_{j}\right) p\left(\mathcal{C}_{j}\right)}
& =\frac{\exp \left(a_{k}\right)}{\sum_{j} \exp \left(a_{j}\right)},
\end{aligned}
$$

where $a_{k}=\ln \left(p\left(\mathbf{x} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right)\right)$.

- #machine-learning, #probability.softmax-function
```

```markdown
## What is the softmax function and what does it represent?

The softmax function is defined as follows:

$$
p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)=\frac{\exp \left(a_{k}\right)}{\sum_{j} \exp \left(a_{j}\right)},
$$

where $a_{k}=\ln \left(p\left(\mathbf{x} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right)\right)$.

The softmax is a smooth approximation of the 'arg max' function, making it widely applicable in multi-class classification problems.

- #machine-learning, #probability.softmax-function
```

```markdown
## Show the Gaussian density for class $\mathcal{C}_{k}$ assuming continuous input variables $\mathbf{x}$ and the same covariance matrix $\boldsymbol{\Sigma}$ for all classes.

The density for class $\mathcal{C}_{k}$ is given by:

$$
p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)=\frac{1}{(2 \pi)^{D / 2}} \frac{1}{|\boldsymbol{\Sigma}|^{1 / 2}} \exp \left\{-\frac{1}{2}\left(\mathbf{x}-\boldsymbol{\mu}_{k}\right)^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}\left(\mathbf{x}-\boldsymbol{\mu}_{k}\right)\right\}
$$

where $\boldsymbol{\mu}_{k}$ is the mean and $\boldsymbol{\Sigma}$ is the shared covariance matrix.

- #statistical-models, #machine-learning.gaussian-distributions
```

```markdown
## Describe the resulting form for posterior probabilities when the class-conditional densities are Gaussian and all classes share the same covariance matrix $\boldsymbol{\Sigma}$ for two classes.

For two classes $\mathcal{C}_1$ and $\mathcal{C}_2$, the posterior probability is given by:

$$
p\left(\mathcal{C}_{1} \mid \mathbf{x}\right)=\sigma\left(\mathbf{w}^{\mathrm{T}} \mathbf{x}+w_{0}\right)
$$

where $\mathbf{w}$ and $w_{0}$ are defined as follows:

$$
\begin{aligned}
\mathbf{w} & =\boldsymbol{\Sigma}^{-1}\left(\boldsymbol{\mu}_{1}-\boldsymbol{\mu}_{2}\right) \\
w_{0} & =-\frac{1}{2} \boldsymbol{\mu}_{1}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}_{1}+\frac{1}{2} \boldsymbol{\mu}_{2}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}_{2}+\ln \frac{p\left(\mathcal{C}_{1}\right)}{p\left(\mathcal{C}_{2}\right)}
\end{aligned}
$$

- #machine-learning, #probability.posterior-probabilities
```

```markdown
## Explain why the posterior probabilities for two Gaussian class-conditional densities with a shared covariance matrix $\boldsymbol{\Sigma}$ lead to a linear function of $\mathbf{x}$ in the logistic sigmoid argument.

The quadratic terms in $\mathbf{x}$ from the exponents of the Gaussian densities cancel due to the assumption of common covariance matrices $\boldsymbol{\Sigma}$. This cancellation results in a linear function of $\mathbf{x}$ in the argument of the logistic sigmoid function:

$$
p\left(\mathcal{C}_{1} \mid \mathbf{x}\right)=\sigma\left(\mathbf{w}^{\mathrm{T}} \mathbf{x}+w_{0}\right)
$$

This linear relationship simplifies the computational complexity and is crucial in discriminant analysis.

- #statistical-models, #machine-learning.linear-discriminants
```

```markdown
## Derive the weights $\mathbf{w}$ and bias $w_{0}$ used in the logistic sigmoid function for the two-class posterior probability model.

The weights $\mathbf{w}$ and bias $w_{0}$ are derived based on the following definitions:

$$
\begin{aligned}
\mathbf{w} & =\boldsymbol{\Sigma}^{-1}\left(\boldsymbol{\mu}_{1}-\boldsymbol{\mu}_{2}\right) \\
w_{0} & =-\frac{1}{2} \boldsymbol{\mu}_{1}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}_{1}+\frac{1}{2} \boldsymbol{\mu}_{2}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}_{2}+\ln \frac{p\left(\mathcal{C}_{1}\right)}{p\left(\mathcal{C}_{2}\right)}
\end{aligned}
$$

These expressions leverage the shared covariance assumption to simplify the Gaussian distribution exponentials.

- #machine-learning, #statistical-models.parameter-derivation
```
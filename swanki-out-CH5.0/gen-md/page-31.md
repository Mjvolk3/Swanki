```markdown
## Why can maximum likelihood exhibit severe over-fitting for linearly separable data sets?

The over-fitting arises because the hyperplane corresponding to $\sigma=0.5$, equivalent to $\mathrm{w}^{\mathrm{T}} \phi=0$, separates the two classes, and the magnitude of $\mathbf{w}$ goes to infinity, making the logistic sigmoid function infinitely steep. 

This corresponds to a Heaviside step function, so that every training point from each class $k$ is assigned a posterior probability $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)=1$.

Maximum likelihood provides no way to favour one solution over another, which in practice will depend on the optimization algorithm and parameter initialization.

- #machine-learning, #maximum-likelihood, #over-fitting
```

```markdown
## What is the mathematical expression for the posterior probabilities in multi-class logistic regression?

The posterior probabilities are given by the softmax transformation of the linear functions of the feature variables:

$$
p\left(\mathcal{C}_{k} \mid \boldsymbol{\phi}\right)=y_{k}(\boldsymbol{\phi})=\frac{\exp \left(a_{k}\right)}{\sum_{j} \exp \left(a_{j}\right)}
$$

where $a_{k}$ is defined as:

$$
a_{k}=\mathbf{w}_{k}^{\mathrm{T}} \boldsymbol{\phi}
$$

- #machine-learning, #logistic-regression, #softmax
```

```markdown
## What is the derivative of the posterior probability $y_k$ with respect to the pre-activation $a_j$ in multi-class logistic regression?

The derivative is given by:

$$
\frac{\partial y_{k}}{\partial a_{j}}=y_{k}\left(I_{k j}-y_{j}\right)
$$

where $I_{k j}$ are the elements of the identity matrix.

- #machine-learning, #logistic-regression, #derivatives
```

```markdown
## Write down the likelihood function using the 1-of-K coding scheme for multi-class logistic regression.

Using the 1-of-K coding scheme, the likelihood function for a feature vector $\phi_n$ belonging to class $\mathcal{C}_k$ is expressed as:

$$
p\left(\mathbf{T} \mid \mathbf{w}_{1}, \ldots, \mathbf{w}_{K}\right)=\prod_{n=1}^{N} \prod_{k=1}^{K} p\left(\mathcal{C}_{k} \mid \boldsymbol{\phi}_{n}\right)^{t_{n k}}=\prod_{n=1}^{N} \prod_{k=1}^{K} y_{n k}^{t_{n k}}
$$

where $\mathbf{t}_n$ is a binary vector with all elements zero except for element $k$, which equals one.

- #machine-learning, #logistic-regression, #likelihood
```

```markdown
## What happens to the logistic sigmoid function in the case of severe over-fitting in maximum likelihood?

In the case of severe over-fitting, the magnitude of $\mathbf{w}$ goes to infinity, making the logistic sigmoid function infinitely steep.

This corresponds to a Heaviside step function, where every training point from each class $k$ is assigned a posterior probability of 1:

$$
p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)=1
$$

- #machine-learning, #maximum-likelihood, #logistic-sigmoid
```

```markdown
## Why does the issue of severe over-fitting in maximum likelihood not depend on the number of data points relative to the number of parameters?

The problem of severe over-fitting arises even if the number of data points is large compared with the number of parameters in the model, as long as the training data set is linearly separable.

This is because the separating hyperplane leads to a continuum of solutions where any hyperplane will give the same posterior probabilities.

- #machine-learning, #maximum-likelihood, #over-fitting
```
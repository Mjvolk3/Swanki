### Card 1

$$
a_{k}(\mathbf{x})=\mathbf{w}_{k}^{\mathrm{T}} \mathbf{x}+w_{k 0}
$$

What defines $a_{k}(\mathbf{x})$ in terms of $\mathbf{w}_{k}$ and $w_{k 0}$ for class $k$?

% 

$a_{k}(\mathbf{x})$ is defined as a linear function of $\mathbf{x}$:

$$
a_{k}(\mathbf{x})=\mathbf{w}_{k}^{\mathrm{T}} \mathbf{x}+w_{k 0}
$$

Where:

- $\mathbf{w}_{k}$ is a weight vector for class $k$
- $w_{k 0}$ is the bias term for class $k$

These parameters incorporate the mean $\boldsymbol{\mu}_{k}$ and covariances $\boldsymbol{\Sigma}$ associated with class $k$

- .machine-learning.linear-models, .probability-posterior-probability

### Card 2

$$
\mathbf{w}_{k}=\boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}_{k}
$$

Define $\mathbf{w}_{k}$ in the context of a general class-conditional density.

% 

$\mathbf{w}_{k}$ is defined as:

$$
\mathbf{w}_{k}=\boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}_{k}
$$

Where:

- $\mathbf{w}_{k}$ is the weight vector for class $k$
- $\boldsymbol{\Sigma}$ is the shared covariance matrix
- $\boldsymbol{\mu}_{k}$ is the mean vector for class $k$

The weight vector $\mathbf{w}_{k}$ incorporates both the inverse of the shared covariance matrix and the mean vector for class $k$.

- .machine-learning.linear-models, .statistics.linear-functions

### Card 3

Explain why the decision boundaries in the given model are linear in the input space.

% 

The decision boundaries are linear in the input space because $a_{k}(\mathbf{x})$ depends linearly on $\mathbf{x}$:

$$
a_{k}(\mathbf{x})=\mathbf{w}_{k}^{\mathrm{T}} \mathbf{x}+w_{k 0}
$$

Additionally, the posterior probabilities $p(\mathcal{C}_{k} \mid \mathbf{x})$ result in linear decision functions due to the shared covariance matrix $\boldsymbol{\Sigma}$. The bias term $w_{k 0}$ incorporates prior probabilities $p(\mathcal{C}_{k})$ causing parallel shifts but not altering the linearity.

- .machine-learning.decision-boundaries, .statistics.posterior-probability

### Card 4

$$
w_{k 0} = -\frac{1}{2} \boldsymbol{\mu}_{k}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}_{k} + \ln p(\mathcal{C}_{k})
$$

Define $w_{k 0}$ and explain its components.

% 

$w_{k 0}$ is the bias term for class $k$ and is defined as:

$$
w_{k 0} = -\frac{1}{2} \boldsymbol{\mu}_{k}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}_{k} + \ln p(\mathcal{C}_{k})
$$

Components:

- $-\frac{1}{2} \boldsymbol{\mu}_{k}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}_{k}$: Incorporates the quadratic term associated with the mean $\boldsymbol{\mu}_{k}$ and covariance $\boldsymbol{\Sigma}$.
- $\ln p(\mathcal{C}_{k})$: Logarithm of the prior probability for class $k$.

- .machine-learning.bias-term, .probability-posterior-probability

### Card 5

Under what conditions do the earlier cancellations no longer occur, leading to quadratic functions of $\mathbf{x}$?

% 

Cancellations no longer occur when each class-conditional density $p(\mathbf{x} \mid \mathcal{C}_{k})$ has its own covariance matrix $\boldsymbol{\Sigma}_{k}$ instead of a shared covariance matrix $\boldsymbol{\Sigma}$. In this case, quadratic terms do not cancel out, yielding quadratic functions of $\mathbf{x}$ and resulting in quadratic discriminant boundaries.

- .machine-learning.covariance-matrix, .statistics.quadratic-functions

### Card 6

Derive the expression for $\mathbf{w}_{k}$ given the shared covariance matrix $\boldsymbol{\Sigma}$ and mean vector $\boldsymbol{\mu}_{k}$.

% 

Given that:

$$
a_{k}(\mathbf{x})=\mathbf{w}_{k}^{\mathrm{T}} \mathbf{x}+w_{k 0}
$$

And 

$$
a_{k}(\mathbf{x})=\ln p(\mathbf{x} \mid \mathcal{C}_{k}) + \ln p(\mathcal{C}_{k}) - \ln p(\mathbf{x})
$$

We have:

$$
\mathbf{w}_{k} = \boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}_{k}
$$

This relation is derived from the quadratic expression in the multivariate normal density when using a shared covariance matrix $\boldsymbol{\Sigma}$. The inverse covariance matrix $\boldsymbol{\Sigma}^{-1}$ weights the mean vector $\boldsymbol{\mu}_{k}$ to produce the weight vector $\mathbf{w}_{k}$ for class $k$.

- .machine-learning.parameter-derivation, .statistics.normal-density
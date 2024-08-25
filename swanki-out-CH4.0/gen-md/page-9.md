Here are six Anki cards generated from the provided text, focusing on the mathematical content and providing detailed context and explanation.

---

## What does the neural network representation of a linear regression model with a single layer of connections include?

Each basis function is represented by a node, with the solid node representing the 'bias' basis function $\phi_{0}$. The outputs $y_{1}, \ldots, y_{K}$ are also represented by nodes. The links between the nodes represent the corresponding weight and bias parameters.

- #neural-networks, #linear-regression

---

## What is the prediction model for multiple outputs in terms of $\mathbf{y}$, $\mathbf{W}$, and $\boldsymbol{\phi}(\mathbf{x})$?

The prediction model for multiple outputs, where $\mathbf{y}$ is a $K$-dimensional column vector, is given by:

$$
\mathbf{y}(\mathbf{x}, \mathbf{w}) = \mathbf{W}^{\mathrm{T}} \boldsymbol{\phi}(\mathbf{x})
$$

where $\mathbf{W}$ is an $M \times K$ matrix of parameters, and $\phi(\mathbf{x})$ is an $M$-dimensional column vector with elements $\phi_{j}(\mathbf{x})$.

- #neural-networks, #linear-regression

---

## What is the form of the conditional distribution of the target vector $\mathbf{t}$ given by an isotropic Gaussian?

The conditional distribution of the target vector $\mathbf{t}$ given $\mathbf{x}$, $\mathbf{W}$, and $\sigma^2$ is:

$$
p\left( \mathbf{t} \mid \mathbf{x}, \mathbf{W}, \sigma^2 \right) = \mathcal{N}\left( \mathbf{t} \mid \mathbf{W}^{\mathrm{T}} \boldsymbol{\phi}(\mathbf{x}), \sigma^2 \mathbf{I} \right)
$$

where $\mathcal{N}$ denotes a Gaussian (normal) distribution with mean $\mathbf{W}^{\mathrm{T}} \boldsymbol{\phi}(\mathbf{x})$ and variance $\sigma^2 \mathbf{I}$.

- #probability-distribution, #neural-networks, #linear-regression

---

## How is the log likelihood function for a set of observations $\mathbf{t}_{1}, \ldots, \mathbf{t}_{N}$ expressed in terms of $\mathbf{T}$, $\mathbf{X}$, $\mathbf{W}$, and $\sigma^2$?

The log likelihood function is given by:

$$
\ln p\left( \mathbf{T} \mid \mathbf{X}, \mathbf{W}, \sigma^2 \right) = \sum_{n=1}^{N} \ln \mathcal{N}\left( \mathbf{t}_n \mid \mathbf{W}^{\mathrm{T}} \boldsymbol{\phi}\left( \mathbf{x}_n \right), \sigma^2 \mathbf{I} \right)
$$

Expanding it, we get:

$$
-\frac{N K}{2} \ln \left( 2 \pi \sigma^2 \right) - \frac{1}{2 \sigma^2} \sum_{n=1}^{N} \left\| \mathbf{t}_n - \mathbf{W}^{\mathrm{T}} \boldsymbol{\phi}\left( \mathbf{x}_n \right) \right\|^2
$$

- #probability-distribution, #log-likelihood, #neural-networks

---

## What is the maximum likelihood estimate $\mathbf{W}_{\mathrm{ML}}$ in terms of $\boldsymbol{\Phi}$ and $\mathbf{T}$?

The maximum likelihood estimate $\mathbf{W}_{\mathrm{ML}}$ is given by:

$$
\mathbf{W}_{\mathrm{ML}} = \left( \boldsymbol{\Phi}^{\mathrm{T}} \boldsymbol{\Phi} \right)^{-1} \boldsymbol{\Phi}^{\mathrm{T}} \mathbf{T}
$$

where $\boldsymbol{\Phi}$ is the matrix containing the input feature vectors, and $\mathbf{T}$ is the matrix of target vectors.

- #maximum-likelihood-estimate, #neural-networks, #linear-regression

---

## Express the estimation of each target variable $t_{k}$ in terms of pseudoinverse $\boldsymbol{\Phi}^{\dagger}$ and $\mathbf{t}_{k}$.

The estimation of each target variable $t_{k}$ is given by:

$$
\mathbf{w}_{k} = \left( \boldsymbol{\Phi}^{\mathrm{T}} \boldsymbol{\Phi} \right)^{-1} \boldsymbol{\Phi}^{\mathrm{T}} \mathbf{t}_{k} = \boldsymbol{\Phi}^{\dagger} \mathbf{t}_{k}
$$

where $\boldsymbol{\Phi}^{\dagger}$ denotes the Moore-Penrose pseudoinverse of $\boldsymbol{\Phi}$.

- #linear-regression, #pseudoinverse, #neural-networks
## What is the equation for the mixing coefficients $\pi_{k}(\mathbf{x})$ in terms of the network pre-activations $a_{k}^{\pi}$?

The mixing coefficients $\pi_{k}(\mathbf{x})$ are given by:

$$
\pi_{k}(\mathbf{x})=\frac{\exp \left(a_{k}^{\pi}\right)}{\sum_{l=1}^{K} \exp \left(a_{l}^{\pi}\right)}
$$

This representation ensures that the mixing coefficients satisfy the constraints $\sum_{k=1}^{K} \pi_{k}(\mathbf{x})=1$ and $0 \leq \pi_{k}(\mathbf{x}) \leq 1$.

- #machine-learning.mixtures, #neural-networks.activations

---

## How are Gaussian standard deviations $\sigma_{k}(\mathbf{x})$ represented to ensure non-negativity?

The Gaussian standard deviations $\sigma_{k}(\mathbf{x})$ are represented using the exponentials of the corresponding network pre-activations $a_{k}^{\sigma}$:

$$
\sigma_{k}(\mathbf{x})=\exp \left(a_{k}^{\sigma}\right)
$$

This form ensures that $\sigma_{k}^{2}(\mathbf{x}) \geq 0$.

- #machine-learning.gaussian, #neural-networks.activations

---

## What is the equation for the Gaussian means $\mu_{k j}(\mathbf{x})$ in terms of the network outputs $a_{k j}^{\mu}$?

The Gaussian means $\mu_{k j}(\mathbf{x})$ are given by:

$$
\mu_{k j}(\mathbf{x})=a_{k j}^{\mu}
$$

Here, the output-unit activation function is the identity function $f(a)=a$.

- #machine-learning.gaussian, #neural-networks.activations

---

## Describe the error function $E(\mathbf{w})$ used for training the mixture density network.

The error function used for training, defined as the negative logarithm of the likelihood, is:

$$
E(\mathbf{w})=-\sum_{n=1}^{N} \ln \left\{\sum_{k=1}^{K} \pi_{k}\left(\mathbf{x}_{n}, \mathbf{w}\right) \mathcal{N}\left(\mathbf{t}_{n} \mid \boldsymbol{\mu}_{k}\left(\mathbf{x}_{n}, \mathbf{w}\right), \sigma_{k}^{2}\left(\mathbf{x}_{n}, \mathbf{w}\right)\right)\right\}
$$

Here, $\mathbf{w}$ represents the weights and biases in the neural network, and the dependencies on $\mathbf{w}$ are made explicit.

- #machine-learning.loss-functions, #optimization.likelihood

---

## How are the derivatives of the error function $E(\mathbf{w})$ with respect to the components of $\mathbf{w}$ obtained, particularly focusing on an input vector $\mathbf{x}_{n}$ and target vector $\mathbf{t}_{n}$?

To minimize the error function, the derivatives of the error $E(\mathbf{w})$ with respect to the components of $\mathbf{w}$ need to be calculated. This involves:

1. Considering the derivatives for a particular input vector $\mathbf{x}_{n}$ with associated target vector $\mathbf{t}_{n}$.
2. Summing these derivatives over all training data points:

$$
\frac{\partial E(\mathbf{w})}{\partial \mathbf{w}} = \sum_{n=1}^{N} \frac{\partial E_{n}(\mathbf{w})}{\partial \mathbf{w}}
$$

where $E_{n}(\mathbf{w})$ is the error associated with the $n$-th data point.

- #machine-learning.optimization, #gradient-descent

---

## What constraint must the mixing coefficients $\pi_{k}(\mathbf{x})$ satisfy, and how is this achieved?

The mixing coefficients $\pi_{k}(\mathbf{x})$ must satisfy the constraints:

$$
\sum_{k=1}^{K} \pi_{k}(\mathbf{x})=1 \quad \text{and} \quad 0 \leq \pi_{k}(\mathbf{x}) \leq 1
$$

These constraints are achieved using a softmax function which normalizes the pre-activations $a_{k}^{\pi}$:

$$
\pi_{k}(\mathbf{x})=\frac{\exp \left(a_{k}^{\pi}\right)}{\sum_{l=1}^{K} \exp \left(a_{l}^{\pi}\right)}
$$

- #machine-learning.mixtures, #neural-networks.activations
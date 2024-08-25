## Explain the mathematical relationship between $y$ and $\eta$.

Using the conditional mean of $t$, denoted $y = \mathbb{E}[t \mid \eta]$, the relationship between $y$ and $\eta$ is given by:

$$
y \equiv \mathbb{E}[t \mid \eta] = -s \frac{d}{d\eta} \ln g(\eta)
$$

Given that $y$ and $\eta$ are related, we denote this relationship through $\eta = \psi(y)$.

- #statistics.generalized-linear-model, #mathematics.conditional-expectation

## Define a generalized linear model in the context of this paper.

A generalized linear model is defined as one where $y$ is a nonlinear function of a linear combination of the input (or feature) variables, represented by:

$$
y = f\left(\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}\right)
$$

Here, $f(\cdot)$ is known as the activation function, and $f^{-1}(\cdot)$ is known as the link function.

- #machine-learning.activation-function, #statistics.link-function

## Show the log likelihood function for the model as a function of $\eta$ and explain its components.

The log likelihood function for the model, as a function of $\eta$, is given by:

$$
\ln p(\mathbf{t} \mid \eta, s) = \sum_{n=1}^{N} \ln p\left(t_{n} \mid \eta, s\right) = \sum_{n=1}^{N}\left\{\ln g\left(\eta_{n}\right) + \frac{\eta_{n} t_{n}}{s}\right\} + \text{const}
$$

where:
- $\mathbf{t}$ is the observed data,
- $\eta$ encapsulates the parameters,
- $s$ is the scale parameter,
- $g(\eta)$ is some function related to the distribution of the data.

The term 'const' indicates a constant that does not depend on the parameters.

- #statistics.log-likelihood, #probability.distribution

## Derive the gradient of the log likelihood function with respect to the model parameters $\mathbf{w}$.

The derivative of the log likelihood with respect to the model parameters $\mathbf{w}$ is:

$$
\begin{aligned}
\nabla_{\mathbf{w}} \ln p(\mathbf{t} \mid \eta, s) & = \sum_{n=1}^{N}\left\{\frac{\mathrm{d}}{\mathrm{d} \eta_{n}} \ln g\left(\eta_{n}\right)+\frac{t_{n}}{s}\right\} \frac{\mathrm{d} \eta_{n}}{\mathrm{~d} y_{n}} \frac{\mathrm{d} y_{n}}{\mathrm{~d} a_{n}} \nabla_{\mathbf{w}} a_{n} \\
& = \sum_{n=1}^{N} \frac{1}{s}\left\{t_{n}-y_{n}\right\} \psi^{\prime}\left(y_{n}\right) f^{\prime}\left(a_{n}\right) \phi_{n}
\end{aligned}
$$

where:
- $a_{n} = \mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}_{n}$,
- $y_{n} = f\left(a_{n}\right)$,
- $\psi'(y_n)$ and $f'(a_n)$ are derivatives of the respective functions.

- #statistics.gradient, #machine-learning.parameter-estimation

## Explain the significance of choosing the link function $f^{-1}(y) = \psi(y)$.

Choosing the link function $f^{-1}(y) = \psi(y)$ simplifies the gradient of the error function substantially. This results in:

$$
f(\psi(y)) = y
$$

thus $f^{\prime}(\psi) \psi^{\prime}(y) = 1$, and for $a = \psi(y)$, we have $f^{\prime}(a) \psi^{\prime}(y) = 1$. Consequently, the gradient of the error function reduces to:

$$
\nabla \ln E(\mathbf{w}) = \frac{1}{s} \sum_{n=1}^{N}\left\{y_{n} - t_{n}\right\} \boldsymbol{\phi}_{n}
$$

- #statistics.link-function, #machine-learning.simplification

## What natural pairing is observed between the choice of error function and the output-unit activation function?

There is a natural pairing between the choice of error function and the choice of output-unit activation function. This implies that the form of the link function and consequently the activation function can simplify the gradient of the error function significantly.

Even though this result is derived in the context of single-layer network models, the same considerations apply to deep neural networks discussed in later chapters.

- #machine-learning.activation-function, #statistics.error-function
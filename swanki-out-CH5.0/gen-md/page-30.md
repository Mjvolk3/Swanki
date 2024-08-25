## What is the derivative of the logistic sigmoid function in terms of the sigmoid function itself?

The derivative of the logistic sigmoid function $\sigma$ can be expressed in terms of the sigmoid function itself as:

$$
\frac{\mathrm{d} \sigma}{\mathrm{d} a} = \sigma(1 - \sigma)
$$

This relation is useful for simplifying expressions and computations in logistic regression and neural networks.

- #mathematics, #logistic-regression

---

## How is the likelihood function for given data in a logistic regression model expressed?

For a data set $\left\{\boldsymbol{\phi}_{n}, t_{n}\right\}$, where $\boldsymbol{\phi}_{n}=\boldsymbol{\phi}\left(\mathbf{x}_{n}\right)$ and $t_{n} \in \{0, 1\}$, with $n=1, \ldots, N$, the likelihood function can be written as:

$$
p(\mathbf{t} \mid \mathbf{w}) = \prod_{n=1}^{N} y_{n}^{t_{n}}\left\{1-y_{n}\right\}^{1-t_{n}}
$$

where $\mathbf{t}=(t_{1}, \ldots, t_{N})^{\mathrm{T}}$ and $y_{n}=p(\mathcal{C}_{1} \mid \boldsymbol{\phi}_{n})$.

- #statistical-models, #logistic-regression

---

## What is the crossentropy error function for logistic regression?

The crossentropy error function $E(\mathbf{w})$ for logistic regression is derived by taking the negative logarithm of the likelihood function:

$$
E(\mathbf{w}) = -\ln p(\mathbf{t} \mid \mathbf{w}) = -\sum_{n=1}^{N} \left\{ t_{n} \ln y_{n} + (1 - t_{n}) \ln (1 - y_{n}) \right\}
$$

where $y_{n} = \sigma(a_{n})$ and $a_{n} = \mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}_{n}$.

- #statistical-models, #error-functions

---

## Derive the gradient of the crossentropy error function with respect to the weight vector $\mathbf{w}$.

The gradient of the error function $E(\mathbf{w})$ with respect to the weight vector $\mathbf{w}$ is:

$$
\nabla E(\mathbf{w}) = \sum_{n=1}^{N} (y_{n} - t_{n}) \boldsymbol{\phi}_{n}
$$

Here, $y_{n} = \sigma(a_{n})$ and $a_{n} = \mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}_{n}$. This gradient is obtained by differentiating the crossentropy error function.

- #mathematics, #logistic-regression.gradients

---

## What condition does the maximum likelihood solution satisfy in logistic regression?

The maximum likelihood solution corresponds to the condition:

$$
\nabla E(\mathbf{w}) = 0
$$

However, due to the nonlinearity in $y(\cdot)$, this equation no longer corresponds to a set of linear equations and does not have a closed-form solution.

- #statistical-models, #logistic-regression

---

## Describe the iterative approach used to find the maximum likelihood solution in logistic regression.

One approach to finding a maximum likelihood solution is **stochastic gradient descent**. In this method, $\nabla E_{n}$ is the $n$th term on the right-hand side of the gradient equation:

$$
\nabla E(\mathbf{w}) = \sum_{n=1}^{N} (y_{n} - t_{n}) \boldsymbol{\phi}_{n}
$$

This technique is useful for training highly nonlinear models, including deep neural networks.

- #optimization, #gradient-descent

---

## Explain why the maximum likelihood equation in logistic regression doesn't have a closed-form solution.

The maximum likelihood equation for logistic regression:

$$
\nabla E(\mathbf{w}) = \sum_{n=1}^{N} (y_{n} - t_{n}) \boldsymbol{\phi}_{n}
$$

does not have a closed-form solution because of the nonlinearity in $y(\cdot)$. The resulting equation is inherently nonlinear and requires iterative methods like stochastic gradient descent or IRLS (Iterative Reweighted Least Squares) for solution.

- #optimization, #logistic-regression.iterative-solutions

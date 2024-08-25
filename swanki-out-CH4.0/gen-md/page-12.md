## What is the conditional mean of $t$ given $\mathbf{x}$?

The conditional mean of $t$ given $\mathbf{x}$ is

$$
\mathbb{E}[t \mid \mathbf{x}] = y(\mathbf{x}, \mathbf{w})
$$

where $y(\mathbf{x}, \mathbf{w})$ is a function of $\mathbf{x}$ and potentially other parameters $\mathbf{w}$.

- #statistics.conditional-mean, #probability.bayes-theorem

## Explain how the calculus of variations is used in the context of the paper and its limitations.

The calculus of variations is used to derive equation (4.37) by optimizing over all possible functions $f(\mathbf{x})$. However, in practice, any parametric model, such as those implemented using deep neural networks, is limited in the range of functions it can represent. Nevertheless, deep neural networks provide a highly flexible class of functions that can approximate any desired function to high accuracy for many practical purposes.

- #mathematics.calculus-of-variations, #machine-learning.neural-networks

## Rearrange and expand the squared term $\{f(\mathbf{x}) - t\}^2$ using the conditional mean $\mathbb{E}[t \mid \mathbf{x}]$.
 
Rearranged and expanded form using the conditional mean:

$$
\begin{aligned}
& \{f(\mathbf{x}) - t\}^2 = \{f(\mathbf{x}) - \mathbb{E}[t \mid \mathbf{x}] + \mathbb{E}[t \mid \mathbf{x}] - t\}^2 \\
& = \{f(\mathbf{x}) - \mathbb{E}[t \mid \mathbf{x}]\}^2 + 2\{f(\mathbf{x}) - \mathbb{E}[t \mid \mathbf{x}]\}\{\mathbb{E}[t \mid \mathbf{x}] - t\} + \{\mathbb{E}[t \mid \mathbf{x}] - t\}^2
\end{aligned}
$$

This expansion is useful for analyzing the components of the squared term.

- #math.algebra, #statistics.conditional-mean

## What does the equation for the expected loss $\mathbb{E}[L]$ look like after substituting into the loss function (4.35) and evaluating the integral over $t$?

After substituting and integrating over $t$, the expected loss $\mathbb{E}[L]$ is:

$$
\mathbb{E}[L] = \int \{f(\mathbf{x}) - \mathbb{E}[t \mid \mathbf{x}]\}^2 p(\mathbf{x}) \mathrm{d} \mathbf{x} + \int \operatorname{var}[t \mid \mathbf{x}] p(\mathbf{x}) \mathrm{d} \mathbf{x}
$$

- #statistics.conditional-mean, #probability.loss-function

## Why does the cross term vanish in the expected loss function derivation?

The cross term vanishes because the conditional mean $\mathbb{E}[t \mid \mathbf{x}]$ is used. When performing the integral over $t$, the cross term $\int 2\{f(\mathbf{x}) - \mathbb{E}[t \mid \mathbf{x}]\}\{\mathbb{E}[t \mid \mathbf{x}] - t\} p(t \mid \mathbf{x}) \mathrm{d}t$ evaluates to zero due to the properties of expectation and variance.

- #statistics.integral-calculation, #probability.conditional-expectation

## What does the Minkowski loss function generalize and what is its expectation given by?

The Minkowski loss function generalizes the squared loss. Its expectation is given by:

$$
\mathbb{E}\left[L_{q}\right]=\iint|f(\mathbf{x}) - t|^{q} p(\mathbf{x}, t) \mathrm{d} \mathbf{x} \mathrm{d} t
$$

For specific values of $q$, the Minkowski loss reduces to the expected squared loss ($q=2$), conditional median loss ($q=1$), and conditional mode loss ($q \rightarrow 0$).

- #statistics.loss-function, #probability.expectation


Sure, here are six cards based on the given chunk of the paper:

---

## Derive the mean of $ \mathbf{y} = \mathbf{A} \mathbf{x} + \mathbf{b} $ given that $\mathbf{y}$ is an affine function and $\mathbf{\mu} = \mathbb{E}[\mathbf{x}]$.

To find the mean, we use the linearity of expectation:

$$
\mathbb{E}[\boldsymbol{y}] = \mathbb{E}[\mathbf{A} \boldsymbol{x} + \boldsymbol{b}] = \mathbf{A} \mathbb{E}[\boldsymbol{x}] + \mathbb{E}[\boldsymbol{b}]
$$

Given that $\boldsymbol{b}$ is a constant vector, $\mathbb{E}[\boldsymbol{b}] = \boldsymbol{b}$, we find:

$$
\mathbb{E}[\boldsymbol{y}] = \mathbf{A} \boldsymbol{\mu} + \boldsymbol{b}
$$

- #linear-algebra, #probability

---

## Derive the mean of $y = \boldsymbol{a}^{\top} \boldsymbol{x} + b$ given $\mathbf{\mu} = \mathbb{E}[\mathbf{x}]$.

For a scalar-valued function:

$$
f(\boldsymbol{x}) = \boldsymbol{a}^{\top} \boldsymbol{x} + b
$$

The mean is:

$$
\mathbb{E}[y] = \mathbb{E}[ \boldsymbol{a}^{\top} \boldsymbol{x} + b ] = \boldsymbol{a}^{\top} \mathbb{E}[\boldsymbol{x}] + \mathbb{E}[b]
$$

Given that $b$ is a constant, $\mathbb{E}[b] = b$, so we get:

$$
\mathbb{E}[y] = \boldsymbol{a}^{\top} \boldsymbol{\mu} + b
$$

- #probability, #scalar-valued-functions

---

## Derive the covariance of $\mathbf{y} = \mathbf{A} \mathbf{x} + \mathbf{b}$.

The covariance of a linear transformation is given by:

$$
\operatorname{Cov}[\mathbf{y}] = \operatorname{Cov}[\mathbf{A}\mathbf{x} + \mathbf{b}]
$$

Since $\mathbf{b}$ is a constant vector, the covariance reduces to:

$$
\operatorname{Cov}[\mathbf{y}] = \mathbf{A} \operatorname{Cov}[\mathbf{x}] \mathbf{A}^{\top}
$$

Denoting $\boldsymbol{\Sigma} = \operatorname{Cov}[\mathbf{x}]$, we have:

$$
\operatorname{Cov}[\mathbf{y}] = \mathbf{A} \boldsymbol{\Sigma} \mathbf{A}^{\top}
$$

- #linear-algebra, #probability, #covariance

---

## Derive the variance $\mathbb{V}[y]$ for $y = \boldsymbol{a}^{\top} \boldsymbol{x} + b$.

To find the variance:

$$
\mathbb{V}[y] = \mathbb{V}[\boldsymbol{a}^{\top} \boldsymbol{x} + b]
$$

Since $b$ is a constant, it does not affect the variance:

$$
\mathbb{V}[y] = \boldsymbol{a}^{\top} \operatorname{Cov}[\boldsymbol{x}] \boldsymbol{a}
$$

Denoting $\boldsymbol{\Sigma} = \operatorname{Cov}[\boldsymbol{x}]$, we get:

$$
\mathbb{V}[y] = \boldsymbol{a}^{\top} \boldsymbol{\Sigma} \boldsymbol{a}
$$

- #linear-algebra, #probability, #variance

---

## Compute the variance $\mathbb{V}[x_1 + x_2]$ for scalar random variables $x_1$ and $x_2$ given $\boldsymbol{a} = [1, 1]$.

To find the variance:

$$
\boldsymbol{a} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}, \boldsymbol{\Sigma} = \begin{bmatrix} \Sigma_{11} & \Sigma_{12} \\ \Sigma_{21} & \Sigma_{22} \end{bmatrix}
$$

Thus,

$$
\mathbb{V}[x_1 + x_2] = \begin{bmatrix} 1 & 1 \end{bmatrix} \begin{bmatrix} \Sigma_{11} & \Sigma_{12} \\ \Sigma_{21} & \Sigma_{22} \end{bmatrix} \begin{bmatrix} 1 \\ 1 \end{bmatrix}
$$

Simplifying, we get:

$$
\mathbb{V}[x_1 + x_2] = \Sigma_{11} + \Sigma_{22} + 2 \Sigma_{12}
$$

Which is:

$$
\mathbb{V}[x_1 + x_2] = \mathbb{V}[x_1] + \mathbb{V}[x_2] + 2 \operatorname{Cov}[x_1, x_2]
$$

- #probability, #variance, #covariance

---

## What needs to be considered when characterizing the full distribution of $\mathbf{y}$ beyond the mean and covariance?

Although some distributions, like the Gaussian, are fully characterized by their mean and covariance, in general, to derive the full distribution of $\mathbf{y}$, one must use other techniques as well.

**Key points:**
- Gaussian distributions are fully described by mean and covariance.
- For other distributions, mean and covariance are not sufficient.

- #probability, #distribution

---


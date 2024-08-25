## Explain the maximization with respect to $\pi$ in the log likelihood function.

The log likelihood function for $\pi$ is given by:

$$
\sum_{n=1}^{N}\left\{t_{n} \ln \pi+\left(1-t_{n}\right) \ln (1-\pi)\right\}
$$

To find the maximum likelihood estimate for $\pi$, we set the derivative with respect to $\pi$ to zero and rearrange:

$$
\pi=\frac{1}{N} \sum_{n=1}^{N} t_{n}=\frac{N_{1}}{N}=\frac{N_{1}}{N_{1}+N_{2}}
$$

where $N_{1}$ and $N_{2}$ are the counts of data points in classes $\mathcal{C}_{1}$ and $\mathcal{C}_{2}$, respectively. Thus, $\pi$ is the fraction of points in class $\mathcal{C}_{1}$. This can be generalized for multiple classes.

- #probability #statistical-methods.maximum-likelihood-estimate

## What is the generalized form of $\pi$ for multi-class cases in maximum likelihood estimation?

In the multi-class case, the maximum likelihood estimate of the prior probability $\pi_k$ associated with class $\mathcal{C}_k$ is given by the fraction of the training set points assigned to that class. Mathematically,

$$
\pi_k = \frac{N_k}{N}
$$

where $N_k$ is the number of data points in class $\mathcal{C}_k$ and $N$ is the total number of data points.

- #probability #statistical-methods.multi-class

## Derive and explain the maximization with respect to $\boldsymbol{\mu}_{1}$ in the log likelihood function.

The relevant part of the log likelihood function for $\boldsymbol{\mu}_{1}$ is:

$$
\sum_{n=1}^{N} t_{n} \ln \mathcal{N}\left(\mathbf{x}_{n} \mid \boldsymbol{\mu}_{1}, \boldsymbol{\Sigma}\right) = -\frac{1}{2} \sum_{n=1}^{N} t_{n}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{1}\right)^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{1}\right) + \text{const.}
$$

Setting the derivative with respect to $\boldsymbol{\mu}_{1}$ to zero and rearranging, we get:

$$
\boldsymbol{\mu}_{1}=\frac{1}{N_{1}} \sum_{n=1}^{N} t_{n} \mathbf{x}_{n}
$$

This result is the mean of input vectors $\mathbf{x}_{n}$ assigned to class $\mathcal{C}_{1}$.

- #probability #statistical-methods.maximization.mean

## Confirm and explain the corresponding maximization for $\boldsymbol{\mu}_{2}$.

By similar derivations as for $\boldsymbol{\mu}_{1}$, the result for $\boldsymbol{\mu}_{2}$ is:

$$
\boldsymbol{\mu}_{2}=\frac{1}{N_{2}} \sum_{n=1}^{N}\left(1-t_{n}\right) \mathbf{x}_{n}
$$

This result is the mean of input vectors $\mathbf{x}_{n}$ assigned to class $\mathcal{C}_{2}$.

- #probability #statistical-methods.maximization.mean

## What are the steps to find the maximum likelihood estimate for the shared covariance matrix $\boldsymbol{\Sigma}$?

To find the maximum likelihood estimation of $\boldsymbol{\Sigma}$, consider the relevant log likelihood parts:

$$
\begin{aligned}
& -\frac{1}{2} \sum_{n=1}^{N} t_{n} \ln |\boldsymbol{\Sigma}|-\frac{1}{2} \sum_{n=1}^{N} t_{n}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{1}\right)^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{1}\right) \\
& -\frac{1}{2} \sum_{n=1}^{N}\left(1-t_{n}\right) \ln |\boldsymbol{\Sigma}|-\frac{1}{2} \sum_{n=1}^{N}\left(1-t_{n}\right)\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{2}\right)^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{2}\right) \\
& =-\frac{N}{2} \ln |\boldsymbol{\Sigma}|-\frac{N}{2} \operatorname{Tr}\left\{\boldsymbol{\Sigma}^{-1} \mathbf{S}\right\}
\end{aligned}
$$

Set the derivative with respect to $\boldsymbol{\Sigma}$ equal to zero and solve for $\boldsymbol{\Sigma}$:

$$
\boldsymbol{\Sigma} = \frac{\mathbf{S}}{N}
$$

where $\mathbf{S}$ is the scatter matrix.

- #probability #statistical-methods.maximization.covariance

## What is the interpretation of $\mathbf{S}$ in the context of finding $\boldsymbol{\Sigma}$?

The scatter matrix $\mathbf{S}$ summarizes the variance-covariance relationships in the data and is defined as:

$$
\mathbf{S} = \sum_{n=1}^{N} t_{n} (\mathbf{x}_{n} - \boldsymbol{\mu}_{1})(\mathbf{x}_{n} - \boldsymbol{\mu}_{1})^{\mathrm{T}} + \sum_{n=1}^{N} (1-t_{n}) (\mathbf{x}_{n} - \boldsymbol{\mu}_{2})(\mathbf{x}_{n} - \boldsymbol{\mu}_{2})^{\mathrm{T}}
$$

Thus, $\boldsymbol{\Sigma}$ captures this overall variability, scaled by $N$.

- #statistical-methods #covariance.scatter-matrix
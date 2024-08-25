which is the mean of the observed set of data points. The maximization of (3.102) with respect to $\Sigma$ is rather more involved. The simplest approach is to ignore the symmetry constraint and show that the resulting solution is symmetric as required. Alternative derivations of this result, which impose the symmetry and positive definiteness constraints explicitly, can be found in Magnus and Neudecker (1999). The result is as expected and takes the form

$$
\boldsymbol{\Sigma}_{\mathrm{ML}}=\frac{1}{N} \sum_{n=1}^{N}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{\mathrm{ML}}\right)\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{\mathrm{ML}}\right)^{\mathrm{T}}
$$

which involves $\boldsymbol{\mu}_{\mathrm{ML}}$ because this is the result of a joint maximization with respect to $\boldsymbol{\mu}$ and $\boldsymbol{\Sigma}$. Note that the solution (3.105) for $\boldsymbol{\mu}_{\mathrm{ML}}$ does not depend on $\boldsymbol{\Sigma}_{\mathrm{ML}}$, and so we can first evaluate $\boldsymbol{\mu}_{\mathrm{ML}}$ and then use this to evaluate $\boldsymbol{\Sigma}_{\mathrm{ML}}$.

If we evaluate the expectations of the maximum likelihood solutions under the true distribution, we obtain the following results

$$
\begin{aligned}
\mathbb{E}\left[\boldsymbol{\mu}_{\mathrm{ML}}\right] & =\boldsymbol{\mu} \\
\mathbb{E}\left[\boldsymbol{\Sigma}_{\mathrm{ML}}\right] & =\frac{N-1}{N} \boldsymbol{\Sigma}
\end{aligned}
$$

We see that the expectation of the maximum likelihood estimate for the mean is equal to the true mean. However, the maximum likelihood estimate for the covariance has an expectation that is less than the true value, and hence, it is biased. We can correct this bias by defining a different estimator $\widetilde{\Sigma}$ given by

$$
\widetilde{\boldsymbol{\Sigma}}=\frac{1}{N-1} \sum_{n=1}^{N}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{\mathrm{ML}}\right)\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{\mathrm{ML}}\right)^{\mathrm{T}}
$$

Clearly from (3.106) and (3.108), the expectation of $\tilde{\Sigma}$ is equal to $\boldsymbol{\Sigma}$.

\title{
3.2.8 Sequential estimation
}

Our discussion of the maximum likelihood solution represents a batch method in which the entire training data set is considered at once. An alternative is to use sequential methods, which allow data points to be processed one at a time and then discarded. These are important for online applications and for large data when the batch processing of all data points at once is infeasible.

Consider the result (3.105) for the maximum likelihood estimator of the mean $\boldsymbol{\mu}_{\mathrm{ML}}$, which we will denote by $\boldsymbol{\mu}_{\mathrm{ML}}^{(N)}$ when it is based on $N$ observations. If we
## How is the maximum likelihood estimate for the mean $\mu_{\mathrm{ML}}$ related to the true mean $\mu$ of the Gaussian distribution?

The maximum likelihood estimate for the mean $\mu_{\mathrm{ML}}$ is an unbiased estimator of the true mean $\mu$ of the Gaussian distribution. This is expressed mathematically as $\mathbb{E}[\mu_{\mathrm{ML}}] = \mu$.

- #statistics, #estimation.theory, #maximum-likelihood

## How does the maximum likelihood estimate of variance $\sigma_{\mathrm{ML}}^2$ relate to the true variance $\sigma^2$?

The maximum likelihood estimate of the variance, $\sigma_{\mathrm{ML}}^2$, underestimates the true variance $\sigma^2$ by a factor of $\frac{N-1}{N}$. This is quantitatively described by:

$$
\mathbb{E}\left[\sigma_{\mathrm{ML}}^{2}\right] = \left(\frac{N-1}{N}\right) \sigma^{2}
$$

- #statistics, #estimation.theory, #bias

## What correction can be made to $\sigma_{\mathrm{ML}}^{2}$ to obtain an unbiased estimate of the variance?

To obtain an unbiased estimate of the variance from the biased maximum likelihood estimate $\sigma_{\mathrm{ML}}^{2}$, it can be corrected using the factor $\frac{N}{N-1}$, resulting in:

$$
\widetilde{\sigma}^{2}=\frac{N}{N-1} \sigma_{\mathrm{ML}}^{2}
$$

which simplifies to:

$$
\widetilde{\sigma}^{2}=\frac{1}{N-1} \sum_{n=1}^{N}\left(x_{n}-\mu_{\mathrm{ML}}\right)^{2}
$$

- #statistics, #variance.correction, #unbiased-estimator

## How is the maximum likelihood estimate for the variance computed from the data set?

The maximum likelihood estimate for the variance, denoted as $\sigma_{\mathrm{ML}}^2$, is calculated from the data set $\{x_n\}$ using the formula:

$$
\sigma_{\mathrm{ML}}^{2}=\frac{1}{N} \sum_{n=1}^{N}\left(x_{n}-\mu_{\mathrm{ML}}\right)^{2}
$$

where $\mu_{\mathrm{ML}}$ is the maximum likelihood estimate of the mean.

- #statistics, #maximum-likelihood, #variance-calculation

## Why does the estimator $\widehat{\sigma}^{2}$ using the true mean $\mu$ yield an unbiased estimate of the variance?

The estimator $\widehat{\sigma}^{2}$ defined as:

$$
\widehat{\sigma}^{2}=\frac{1}{N} \sum_{n=1}^{N}\left(x_{n}-\mu\right)^{2}
$$

is unbiased for the variance $\sigma^2$ because it uses the true mean $\mu$ rather than an estimate derived from the data. Mathematically, the expectation of this estimator is:

$$
\mathbb{E}\left[\widehat{\sigma}^{2}\right]=\sigma^{2}
$$

demonstrating that it accurately represents the true variance without underestimation.

- #statistics, #unbiased-estimator, #variance-calculation
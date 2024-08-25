## How does the constraint (3.153) simplify the multinomial distribution into exponential family form?
The form of the multinomial distribution under constraint (3.153) transforms as shown:

$$
\exp \left\{\sum_{k=1}^{M} x_{k} \ln \mu_{k}\right\} =\exp \left\{\sum_{k=1}^{M-1}x_{k} \ln \left(\frac{\mu_{k}}{1-\sum_{j=1}^{M-1}\mu_{j}}\right)+ \ln \left(1-\sum_{k=1}^{M-1} \mu_{k}\right)\right\}
$$

This formulation accommodates the constraint by introducing a new term that accounts for the sum of probabilities equaling 1.

- #probability.multinomial-distribution, #exponential-family, #mathematical-transformations

## How is the parameter $\eta_k$ defined in terms of $\mu_k$ in the context of a modified multinomial distribution?
In transforming the multinomial distribution to fit the exponential family format under constraint (3.153), $\eta_k$ is defined as:

$$
\eta_k = \ln \left(\frac{\mu_k}{1-\sum_{j} \mu_j}\right)
$$

This clearly delineates $\eta_k$ as the natural logarithm of the ratio of $\mu_k$ to the residual probability mass, effectively enabling the softmax function representation.

- #probability.softmax-function, #parameter-estimation, #exponential-family

## Derive the formula for $\mu_k$ using the parameter $\eta_k$.
Starting from the definition of $\eta_k$,

$$
\eta_k = \ln \left(\frac{\mu_k}{1-\sum_{j} \mu_j}\right)
$$

rearranging this gives:

$$
\mu_k = \frac{\exp(\eta_k)}{1 + \sum_j \exp(\eta_j)}
$$

This relationship represents the softmax function, which normalizes the exponentials of the input parameters to ensure that they sum to 1, suitable for probability distributions.

- #probability.softmax-function, #derivation, #exponential-family

## What is the normalized expression for the multinomial distribution in exponential family form involving $\boldsymbol{\eta}$?
The normalized expression for the multinomial distribution under the exponential family representation, with parameter vector $\boldsymbol{\eta}$, is:

$$
p(\mathbf{x} \mid \boldsymbol{\eta}) = \left(1 + \sum_{k=1}^{M-1} \exp(\eta_k)\right)^{-1} \exp(\boldsymbol{\eta}^\mathrm{T} \mathbf{x})
$$

This indicates how the function normalizes over possible outcomes using the softmax component integrated into the partition function $g(\boldsymbol{\eta})$.

- #probability.multinomial-distribution, #exponential-family-form, #probability-models

## How does the Gaussian distribution relate to the exponential family, and what is its natural parameter form under this family?
The univariate Gaussian distribution can be expressed in the exponential family form as:

$$
p(x \mid \mu, \sigma^2) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp \left\{-\frac{1}{2\sigma^2}(x-\mu)^2\right\}
$$

When rearranged yields:

$$
p(x \mid \mu, \sigma^2) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp \left\{-\frac{x^2}{2\sigma^2} + \frac{\mu x}{\sigma^2} - \frac{\mu^2}{2\sigma^2}\right\}
$$

This elicitation shows that the Gaussian distribution can be cast into the exponential family format, with $\boldsymbol{\theta} = (\frac{\mu}{\sigma^2}, -\frac{1}{2\sigma^2})$ as the natural parameters, which maintains the format $\exp(\boldsymbol{\theta}^\mathrm{T} \mathbf{T}(x) - A(\boldsymbol{\theta}))$ common to the family.

- #probability.gaussian-distribution, #exponential-family-form, #statistical-modeling
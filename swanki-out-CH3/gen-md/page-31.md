## How is the logistic sigmoid function defined in terms of $\eta$?

The logistic sigmoid function $\sigma(\eta)$ is defined as:

$$
\sigma(\eta)=\frac{1}{1+\exp(-\eta)}
$$

This function is crucial in transforming the linear combination of inputs into a probability value, bounded between 0 and 1, often used in logistic regression and neural network activation functions.

- #mathematics, #functions.sigmoid-function

## Derive the expression for $1-\sigma(\eta)$ using the logistic sigmoid function.

Given the logistic sigmoid function $\sigma(\eta)$ defined as:

$$
\sigma(\eta)=\frac{1}{1+\exp(-\eta)}
$$

The expression for $1 - \sigma(\eta)$ is derived as follows:

$$
1 - \sigma(\eta) = 1 - \frac{1}{1 + \exp(-\eta)} = \frac{1 + \exp(-\eta) - 1}{1 + \exp(-\eta)} = \frac{\exp(-\eta)}{1 + \exp(-\eta)} = \sigma(-\eta)
$$

This demonstrates the symmetric property of the sigmoid function about the origin, which is utilized in logistic regression models.

- #mathematics, #functions.sigmoid-function-derivations

## Explain the relationship between the parameters $\mu_k$ and $\eta_k$ in the context of the multinomial distribution.

In the multinomial distribution, the parameters $\mu_k$ (probabilities of different categories) are related to the parameters $\eta_k$ through the logarithmic transformation:

$$
\eta_k = \ln \mu_k
$$

This transformation ensures that the linear model parameters ($\eta_k$) are unconstrained, which helps in gradient-based optimization techniques in logistic regression. The back transformation to get probabilities ($\mu_k$) from these parameters involves the exponential function: $\mu_k = e^{\eta_k}$.

- #statistics, #distribution.multinomial-distribution

## How does the constraint $\sum_{k=1}^{M} \mu_{k}=1$ affect the independence of the parameters $\mu_k$?

The constraint $\sum_{k=1}^{M} \mu_{k}=1$ imposes a condition where Not all parameters $\mu_k$ are independent. Given $M-1$ parameters, the value of the remaining parameter is determined automatically to ensure that the sum of all $\mu_k$ equals 1. This dependency is crucial in statistical modeling and inference in multinomial settings, affecting how parameters are estimated and interpreted.

- #statistics, #distribution.constraints

## Provide a method to express the multinomial distribution in terms of $M-1$ parameters given the sum-to-one constraint.

To express the multinomial distribution with $M-1$ parameters, considering the constraint $\sum_{k=1}^{M} \mu_{k}=1$, we eliminate $\mu_M$ by expressing it as dependent on the remaining probabilities:

$$
\mu_M = 1 - \sum_{k=1}^{M-1} \mu_{k}
$$

This reduction in dimensions by one parameter avoids redundancy and is common in statistical practices like logistic regression modeling. It facilitates the parameter estimation process by reducing the degrees of freedom and ensuring the constraint is met.

- #statistics, #distribution.parameter-reduction
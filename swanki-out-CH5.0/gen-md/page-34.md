### Card 1

## Define and relate the erf function to the Gaussian distribution.

The erf function, or error function, is defined as follows

$$
\operatorname{erf}(a) = \frac{2}{\sqrt{\pi}} \int_{0}^{a} \exp\left(-\theta^{2}\right) \mathrm{d}\theta
$$

Explain how the erf function relates to the Gaussian distribution and the probit function.

The error function (erf) is primarily used to compute probabilities involving the normal distribution. It is derived from the integral of the Gaussian distribution. Specifically, it is defined as:

$$
\operatorname{erf}(a) = \frac{2}{\sqrt{\pi}} \int_{0}^{a} \exp(-\theta^2) \mathrm{d}\theta
$$

It is closely related to the cumulative distribution function (CDF) of the standard normal distribution (which is defined by the probit function $\Phi$):

$$
\Phi(a) = \frac{1}{2}\left(1 + \operatorname{erf}\left(\frac{a}{\sqrt{2}}\right)\right)
$$

- #statistics.gaussian-distribution, #functions.error-function, #probability.probit-function


### Card 2

## Define the probit function and explain its significance in the context of regression models.

The probit function $\Phi(a)$ is defined as

$$
\Phi(a) = \frac{1}{2}\left\{1+\operatorname{erf}\left(\frac{a}{\sqrt{2}}\right)\right\}
$$

How does the probit function relate to probit regression, and why is it significant compared to the logistic sigmoid function?

The probit function $\Phi(a)$ is given by:

$$
\Phi(a) = \frac{1}{2}\left\{1 + \operatorname{erf}\left(\frac{a}{\sqrt{2}}\right)\right\}
$$

Probit regression is a type of regression model where the activation function is a probit function instead of the more commonly used logistic sigmoid function. Probit regression is significant because, although it shares similarities with logistic regression, it behaves differently with respect to outliers. Specifically, the tails of the probit function decay like $\exp(-x^2)$, making it more sensitive to outliers compared to the logistic sigmoid function which decays like $\exp(-x)$.

- #statistics.probit-regression, #math.probit-function, #math.logistic-regression


### Card 3

## Discuss the impact of outliers on probit regression versus logistic regression.

Explain how the tails of the logistic sigmoid function and the probit function affect their sensitivity to outliers.

The tails of the logistic sigmoid function decay asymptotically like $\exp(-x)$, while the tails of the probit function decay like $\exp(-x^2)$. How does this difference impact the sensitivity of probit regression to outliers compared to logistic regression?

In logistic regression, the tails of the sigmoid function decay asymptotically like $\exp(-x)$. However, for the probit function, the tails decay like $\exp(-x^2)$. This difference means that probit regression tends to be more sensitive to outliers. Specifically, points that lie far from the decision boundary can significantly distort the classifier in probit regression due to the slower decay rate of $\exp(-x^2)$ compared to $\exp(-x)$.

- #statistics.outliers, #math.probit-regression, #math.logistic-regression


### Card 4

## Derive the form of the error function for a linear regression model with Gaussian noise distribution.

Given the error function for a linear regression model with Gaussian noise distribution as negative $\log$ likelihood, derive its form in terms of the parameter vector $\mathbf{w}$.

The error function in a linear regression model with Gaussian noise distribution can be written as the negative $\log$ likelihood. Define and derive its form with respect to the parameter vector $\mathbf{w}$.

For a linear regression model with Gaussian noise distribution, the error function is given by the negative log-likelihood. This can be expressed as:

$$
E(\mathbf{w}) = \frac{1}{2} \sum_{n=1}^{N} (y_n - t_n)^2
$$

where $y_n = \mathbf{w}^T \phi_n$. Taking the derivative with respect to $\mathbf{w}$:

$$
\frac{\partial E}{\partial \mathbf{w}} = \sum_{n=1}^{N} (y_n - t_n) \phi_n
$$

This results in the form where the 'error' $(y_n - t_n)$ is multiplied by the feature vector $\phi_n$.

- #statistics.linear-regression, #math.error-function, #math.gaussian-noise


### Card 5

## Explain the concept of canonical link functions in the context of generalized linear models (GLMs).

What is a canonical link function and how is it applied in the context of GLMs? Discuss the relationship of conditional distributions from the exponential family.

Define the term canonical link function and describe its application in generalized linear models (GLMs). 

A canonical link function is a specific type of link function that is used in generalized linear models (GLMs) to relate the linear predictor to the mean of the distribution function. The choice of the canonical link function is motivated by mathematical convenience and often leads to simplified computations.

For a target variable $t$ with a conditional distribution from the exponential family, the canonical link function ensures that the derivative of the log-likelihood with respect to the linear predictor $\eta$ results in a form involving the 'error' $(y_n - t_n)$ times the feature vector $\phi_n$. This can be generalized as:

$$
p(t \mid \eta, s) = \frac{1}{s} h\left(\frac{t}{s}\right) g(\eta) \exp \left\{\frac{\eta t}{s}\right\}
$$

- #statistics.glm, #math.canonical-link-function, #probability.exponential-family


### Card 6

## Conditional distribution of the target variable in the exponential family.

Consider the following form for the conditional distribution of the target variable from the exponential family:

$$
p(t \mid \eta, s) = \frac{1}{s} h\left(\frac{t}{s}\right) g(\eta) \exp \left\{\frac{\eta t}{s}\right\}
$$

Describe how this form applies to conditional distributions and how it differs from its application to input vectors.

The conditional distribution of the target variable $t$ from the exponential family can be written as:

$$
p(t \mid \eta, s) = \frac{1}{s} h\left(\frac{t}{s}\right) g(\eta) \exp \left\{\frac{\eta t}{s}\right\}
$$

In this form, conditional distributions are assumed for the target variable based on its exponential family. Here, $\eta$ represents the natural parameter, and $s$ is a scale parameter. This contrasts with its application to input vectors, where the distribution is directly applied to the features or data points. This approach is useful in GLMs where the goal is to model the relationship between predictors and the target variable.

- #statistics.exponential-family, #probability.conditional-distribution, #math.glm
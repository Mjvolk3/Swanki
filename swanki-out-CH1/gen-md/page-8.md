## Explain how linear models are used for curve fitting including the context of underlying functions and noise.

Linear models are used for curve fitting by assuming a polynomial function of the form:

$$
y(x, \mathbf{w}) = w_{0} + w_{1} x + w_{2} x^{2} + \ldots + w_{M} x^{M} = \sum_{j=0}^{M} w_{j} x^{j}
$$

In this expression:
- $y(x, \mathbf{w})$ represents the polynomial model output.
- $w_{j}$ are the polynomial coefficients.
- $M$ is the order of the polynomial.
- $x$ is the input variable raised to the various powers $j$.

Although the polynomial function $y(x, \mathbf{w})$ is non-linear in the variable $x$, it is linear in the coefficients $\mathbf{w}$. These kinds of functions are called linear models. The purpose of curve fitting in this context is to approximate underlying trends in data that might be corrupted with noise. The challenge is to generalize from a finite data set to identify the underlying function, illustrated here as $\sin (2 \pi x)$, even when data is noisy.

- #probability-theory.linear-models, #curve-fitting.polynomials, #noise-data_machine-learning

## What is the general form of a polynomial function used in linear models for curve fitting?

A general form of a polynomial function used in linear models for curve fitting is given by:

$$
y(x, \mathbf{w}) = w_{0} + w_{1} x + w_{2} x^{2} + \ldots + w_{M} x^{M} = \sum_{j=0}^{M} w_{j} x^{j}
$$

where:
- $y(x, \mathbf{w})$ represents the polynomial function.
- $\mathbf{w} = [w_{0}, w_{1}, ..., w_{M}]$ is the vector of polynomial coefficients.
- $M$ is the order of the polynomial.
- $x$ is the input variable.

These coefficients are determined by fitting the polynomial to the training data, usually by minimizing some error function that measures the disagreement between the polynomial's prediction and the observed data.

- #linear-models.polynomial, #curve-fitting.machine-learning, #error-function_minimization

## How does adding random noise to data points reflect real-world data sets in the context of the text?

Adding random noise governed by a Gaussian distribution to data points reflects real-world datasets as it captures the commonly observed property that real-world data possess an underlying regularity but individual observations are often corrupted by random noise. This noise can arise from:
- Intrinsically stochastic processes (e.g., radioactive decay).
- Variability from unobservable sources.

In machine learning, understanding these noise influences is critical for developing models that can generalize underlying trends from finite, noisy datasets.

- #data-properties.noise, #machine-learning.noise, #gaussian-distribution_randomness

## Define and explain the role of the error function in fitting polynomial coefficients for linear models.

The error function measures the misfit between the polynomial function $y(x, \mathbf{w})$ and the training data points. It is crucial in determining the values of the polynomial coefficients $\mathbf{w}$.

If we let $\{(x_{i}, t_{i})\}_{i=1}^{N}$ be our training data where $x_{i}$ is the input and $t_{i}$ is the target output, a common choice of error function is:

$$
E(\mathbf{w}) = \frac{1}{2} \sum_{i=1}^{N} \left( t_{i} - y(x_{i}, \mathbf{w}) \right)^{2}
$$

In this equation:
- $E(\mathbf{w})$ is the error function.
- $N$ is the number of training data points.
- $t_{i}$ is the target output for the $i$-th data point.
- $y(x_{i}, \mathbf{w})$ is the model prediction.

Minimizing this error function helps in finding the best-fitting polynomial coefficients.

- #error-function.polynomial-fitting, #linear-models.error, #machine-learning.coefficients

## Describe how probability theory and decision theory are applied in machine learning as mentioned in the text.

Probability theory and decision theory are applied in machine learning to handle the uncertainty in predicting values when given a finite data set:

1. **Probability Theory**: Provides a rigorous framework to express uncertainties in predictions, especially when the observed data is corrupted with noise. Probabilities allow quantification of uncertainty for given input values $\widehat{x}$ and corresponding target values $\widehat{t}$.

2. **Decision Theory**: Uses the probabilistic representations to make predictions that are optimal according to specified criteria. This includes making informed decisions based on the likelihood of various outcomes given the observed data.

Together, these theories ensure that machine learning models can generalize well from finite, noisy datasets by making probabilistically informed and optimal predictions.

- #probability-theory.machine-learning, #decision-theory.prediction, #uncertainty_handling
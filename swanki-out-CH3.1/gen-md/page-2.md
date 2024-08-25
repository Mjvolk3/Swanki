## Define the Bernoulli distribution for a binary variable with parameter $\mu$.

The Bernoulli distribution for a binary random variable $x$, which can take values 0 or 1, is defined by the parameter $\mu$. Here, $\mu$ represents the probability of $x$ being 1 (e.g., flipping heads on a coin). The probability mass function (PMF) is given by:

$$
\operatorname{Bern}(x \mid \mu) = \mu^x (1 - \mu)^{1-x}
$$

This encodes the probability of $x$ being 0 or 1, depending on $\mu$.

- #probability.distributions.bernoulli-distribution

## What is meant by the data being "independent and identically distributed" (i.i.d.)?

Data points are described as "independent and identically distributed" (i.i.d.) when each data instance in a dataset is sampled independently from the same probability distribution. This is a fundamental assumption in many statistical models for simplifying analysis by ruling out dependencies among data points and uniform data behavior through identical distribution.

- #statistics.data-analysis.iid-assumption

## Describe the general approach of parametric models in density estimation.

Parametric models in density estimation utilize a fixed form for the distribution, characterized by a set of parameters such as mean and variance in a Gaussian distribution. The main objective is to find the parameter values that best describe the data, typically by maximizing the likelihood function. This approach, however, assumes that the model's functional form well-represents the underlying data distribution, which may not always be suitable.

- #statistics.density-estimation.parametric-models

## What is the limitation of nonparametric density estimation methods mentioned in the text?

Nonparametric density estimation methods, which rely on data-driven distribution forms like histograms, nearest neighbors, and kernels, face a significant efficiency issue as they often require storing all training data. As the dataset grows, the number of parameters (or model complexity controls) increases, making these methods impractical for large datasets.

- #statistics.density-estimation.nonparametric-models

## How does deep learning bridge the gap between parametric and nonparametric approaches?

Deep learning models integrate the efficiency of parametric models with the flexibility of nonparametric methods by employing neural networks. These networks provide flexible distributions governed by a large but fixed number of parameters, addressing the efficiency shortcomings of traditional nonparametric methods without being rigidly constrained to a specific distribution form, as in standard parametric approaches.

- #machine-learning.deep-learning.hybrid-models
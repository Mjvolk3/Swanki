## Given a dataset of $N$ i.i.d. observations $\mathbf{X}=\left\{\mathbf{x}_{1}, \ldots, \mathbf{x}_{N}\right\}$ and corresponding target values $\mathbf{t}=\left\{t_{1}, \ldots, t_{N}\right\}$, what is the likelihood function?

The likelihood function is

$$
p\left(\mathbf{t} \mid \mathbf{X}, \mathbf{w}, \sigma^{2}\right) = \prod_{n=1}^{N} p\left(t_{n} \mid y\left(\mathbf{x}_{n}, \mathbf{w}\right), \sigma^{2}\right)
$$

Here, $\mathbf{w}$ represents the model parameters, $\sigma^2$ is the variance of the Gaussian noise, $\mathbf{x}_n$ are the inputs, and $t_n$ are the target values.

- #machine-learning, #probability.theory, #likelihood


## Express the error function obtained by taking the negative logarithm of the likelihood function for the dataset $\mathbf{X}=\left\{\mathbf{x}_{1}, \ldots, \mathbf{x}_{N}\right\}$ and target values $\mathbf{t}=\left\{t_{1}, \ldots, t_{N}\right\}$.

The error function is given by

$$
\frac{1}{2 \sigma^{2}} \sum_{n=1}^{N}\left\{y\left(\mathbf{x}_{n}, \mathbf{w}\right)-t_{n}\right\}^{2}+\frac{N}{2} \ln \sigma^{2}+\frac{N}{2} \ln (2 \pi)
$$

- #machine-learning, #error-function.derivation, #logarithm.application


## What is the sum-of-squares error function $E(\mathbf{w})$ used for minimizing the error associated with the model parameters $\mathbf{w}$?

The sum-of-squares error function is given by

$$
E(\mathbf{w}) = \frac{1}{2} \sum_{n=1}^{N}\left\{y\left(\mathbf{x}_{n}, \mathbf{w}\right)-t_{n}\right\}^{2}
$$

Here, $\mathbf{w}$ denotes the parameters of the model, $y(\mathbf{x}_n, \mathbf{w})$ is the model's prediction, and $t_n$ is the target value.

- #mathematics.sum-of-squares, #machine-learning.error-function, #parameter-learning


## After finding $\mathbf{w}^{\star}$, how is $\sigma^{2 \star}$ determined?

After determining $\mathbf{w}^{\star}$, $\sigma^{2 \star}$ is found by minimizing the error function $(6.25)$:

$$
\sigma^{2 \star}=\frac{1}{N} \sum_{n=1}^{N}\left\{y\left(\mathbf{x}_{n}, \mathbf{w}^{\star}\right)-t_{n}\right\}^{2}
$$

This equation provides the variance of the Gaussian noise based on the optimized model parameters $\mathbf{w}^{\star}$.

- #machine-learning, #error-function.variance, #parameter-estimation


## Consider multiple target variables assumed to be independent and conditionally distributed on $\mathbf{x}$ and $\mathbf{w}$. What is the conditional distribution of target values if all share the same noise variance $\sigma^{2}$?

The conditional distribution of the target values is given by

$$
p(\mathbf{t} \mid \mathbf{x}, \mathbf{w}) = \mathcal{N}\left(\mathbf{t} \mid \mathbf{y}(\mathbf{x}, \mathbf{w}), \sigma^{2} \mathbf{I}\right)
$$

Here, $\mathbf{y}(\mathbf{x}, \mathbf{w})$ is the model's prediction and $\mathbf{I}$ is the identity matrix.

- #statistics.conditional-distribution, #machine-learning.multiple-variables, #gaussian-noise


## Why does minimizing the error function $E(\mathbf{w})$ typically not correspond to the global maximum of the likelihood function?

Minimizing the error function $E(\mathbf{w})$ doesn't typically correspond to the global maximum of the likelihood function because the nonlinearity of the network function $y(\mathbf{x}_n, \mathbf{w})$ causes $E(\mathbf{w})$ to be non-convex.

A non-convex error function can have multiple local minima, making the search for a global optimum generally infeasible.

- #machine-learning, #optimization, #non-convexity
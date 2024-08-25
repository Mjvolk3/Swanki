## How is the maximum likelihood estimate of the variance parameter $\sigma^{2}$ expressed in terms of observed data and the parameter vector $\mathbf{w}_{\mathrm{ML}}$?
The maximum likelihood estimate (MLE) for the variance parameter $\sigma^{2}$, given the parameter vector $\mathbf{w}_{\mathrm{ML}}$, is expressed as:

$$
\sigma_{\mathrm{ML}}^{2}=\frac{1}{N} \sum_{n=1}^{N}\left\{y\left(x_{n}, \mathbf{w}_{\mathrm{ML}}\right)-t_{n}\right\}^{2}
$$

Here, $N$ is the number of observations, $x_n$ are the input values, $\mathbf{w}_{\mathrm{ML}}$ is the previously determined maximum likelihood estimate of the model parameters, $y(x_n, \mathbf{w}_{\mathrm{ML}})$ is the model prediction for the input $x_n$, and $t_n$ are the target values corresponding to each $x_n$.

- #statistics, #maximum-likelihood-estimation, #variance-estimation

## What is the predictive distribution for new values of $x$ in a probabilistic model using maximum likelihood estimates?
In a probabilistic model using maximum likelihood estimates, the predictive distribution for new values of $x$, given the parameters $\mathbf{w}_{\mathrm{ML}}$ and $\sigma_{\mathrm{ML}}^{2}$, is given by:

$$
p\left(t \mid x, \mathbf{w}_{\mathrm{ML}}, \sigma_{\mathrm{ML}}^{2}\right)=\mathcal{N}\left(t \mid y\left(x, \mathbf{w}_{\mathrm{ML}}\right), \sigma_{\mathrm{ML}}^{2}\right)
$$

This expression indicates that the predictions are distributed according to a normal distribution $\mathcal{N}$, where the mean of the distribution is the predicted value $y(x, \mathbf{w}_{\mathrm{ML}})$ and the variance is $\sigma_{\mathrm{ML}}^{2}$. This probabilistic approach provides not only an estimate of the predicted value but also an estimate of the uncertainty of this prediction.

- #predictive-distribution, #probabilistic-modeling, #normal-distribution

## How does the change of variables affect the transformation of a probability density function?
When changing variables in a probability density function from $x$ to $y$ via a transformation $x = g(y)$, the transformed density $p_y(y)$ is given by:

$$
p_{y}(y) = p_{x}(x)\left|\frac{\mathrm{d} x}{\mathrm{d} y}\right| = p_{x}(g(y))\left|\frac{\mathrm{d} g}{\mathrm{d} y}\right|
$$

This equation shows how the probability density transforms under a change of variables. The term $\left|\frac{\mathrm{d} x}{\mathrm{d} y}\right|$ or $\left|\frac{\mathrm{d} g}{\mathrm{d} y}\right|$ is the absolute value of the derivative of the transformation function $g$, reflecting the effect of scaling on the probability density due to the change in variable space. The absolute value is used to ensure a non-negative density value.

- #probability-density-functions, #transformation-of-variables, #change-of-variables

## Why is the modulus used in the transformation formula for probability densities under a change of variables?
The modulus is used in the transformation formula for probability densities to ensure that the resulting transformed density remains non-negative, regardless of the sign of the derivative:

$$
p_{y}(y) = p_{x}(x)\left|\frac{\mathrm{d} x}{\mathrm{d} y}\right| = p_{x}(g(y))\left|\frac{\mathrm{d} g}{\mathrm{d} y}\right|
$$

In this formula, if the transformation function $g$ were to have a negative derivative, the probability density $p_y(y)$ would still need to be non-negative because probabilities cannot be negative. The modulus corrects for any negative signs that might arise due to the derivative's direction of change, ensuring a positive scaling factor.

- #probability-theory, #variable-transformation, #mathematical-modulus

## What role does the transformed probability density play in the context of normalizing flows in generative modeling?
In the context of normalizing flows in generative modeling, the transformed probability density plays a crucial role by enabling complex distributions to be modeled through successive, invertible transformations. Here is how the transformation mechanism works:

$$
p_{y}(y) = p_{x}(x)\left|\frac{\mathrm{d} x}{\mathrm{d} y}\right| = p_{x}(g(y))\left|\frac{\mathrm{d} g}{\mathrm{d} y}\right|
$$

This equation allows us to map a simple, known probability density (e.g., standard normal distribution) to a more complex density reflecting the data distribution by applying a sequence of invertible transformations $g$. These transformations are designed to be differentiable as well as invertible, ensuring that the probability distributions can seamlessly flow from the simpler to the more complex configuration, hence the term "normalizing flows."

- #generative-models, #normalizing-flows, #density-transformation
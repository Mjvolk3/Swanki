## What is the main difference in convergence rate between batch gradient descent and stochastic gradient descent when using Nesterov momentum?

Nesterov momentum can improve the rate of convergence for batch gradient descent but can be less effective for stochastic gradient descent.

- #machine-learning, #optimization.nesterov-momentum


## What is the typical approach for determining the learning rate parameter in stochastic gradient descent?

In the stochastic gradient descent learning algorithm, a common approach is to start with a larger value for the learning rate parameter $\eta$ and then reduce it over time. This is often expressed as a function of the step index $\tau$:

$$
\eta = \eta(\tau)
$$

- #machine-learning, #optimization.learning-rate

  
## Write the update rule for Stochastic Gradient Descent with momentum.

The update rule for Stochastic Gradient Descent with momentum is:

$$
\Delta \mathbf{w} \leftarrow -\eta \nabla E_{n:n+B-1}(\mathbf{w}) + \mu \Delta \mathbf{w}
$$

where $\eta$ is the learning rate, $\mu$ is the momentum parameter, and $E_{n:n+B-1}(\mathbf{w})$ is the error function per mini-batch.

- #machine-learning, #optimization.gradient-descent


## How does the learning rate parameter $\eta$ affect the learning process in stochastic gradient descent?

If the learning rate parameter $\eta$ is very small, learning proceeds slowly. If $\eta$ is too large, it can lead to instability and potentially divergent oscillations. The best practice is to start with a larger $\eta$ and then reduce it over time.

- #machine-learning, #optimization.learning-rate


## {{c1::Why}} do we shuffle data if $n > N$ in the Stochastic Gradient Descent algorithm with momentum?

## Shuffling Data in SGDM

We shuffle data if $n > N$ to ensure that each epoch sees the data in a different order, preventing the model from overfitting to the sequence of data.

- #machine-learning, #optimization.gradient-descent


## What is the weight update rule in Stochastic Gradient Descent with momentum?

In Stochastic Gradient Descent with momentum, the weight update rule is:

$$
\mathbf{w} \leftarrow \mathbf{w} + \Delta \mathbf{w}
$$

where $\Delta \mathbf{w}$ is given by:

$$
\Delta \mathbf{w} \leftarrow -\eta \nabla E_{n:n+B-1}(\mathbf{w}) + \mu \Delta \mathbf{w}
$$

- #machine-learning, #optimization.weight-update
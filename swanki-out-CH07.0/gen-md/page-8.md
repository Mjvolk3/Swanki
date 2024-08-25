## What is the relationship between the mini-batch size $N$ and the error in estimating the gradient in stochastic gradient descent?

The error in computing the mean from $N$ samples is given by:

$$
\frac{\sigma}{\sqrt{N}}
$$

where $\sigma$ is the standard deviation of the distribution generating the data. Increasing the mini-batch size by a factor of 100 reduces the error only by a factor of 10, indicating diminishing returns.

- #machine-learning, #gradients, #optimization

## Why should mini-batch data points be chosen randomly in stochastic gradient descent?

Mini-batch data points should be chosen randomly to avoid correlations between successive data points which can arise from the way the data was collected (e.g., alphabetically or by date). This is handled by shuffling the data set and drawing mini-batches as successive blocks to escape local minima.

- #machine-learning, #data-preprocessing, #randomization

## What is the downside of using stochastic gradient descent with a single data point?

The gradient of the error function computed from a single data point provides a very noisy estimate of the gradient computed on the full data set. This noise can lead to inefficiencies in the convergence of the optimization process.

- #machine-learning, #gradients, #optimization

## How does hardware architecture influence the choice of mini-batch size in stochastic gradient descent?

Hardware architecture can influence the choice of mini-batch size. For example, on some hardware platforms, mini-batch sizes that are powers of 2 (e.g., 64, 128, 256) work well due to the architecture's specific optimizations and efficient execution of such sizes.

- #machine-learning, #hardware, #optimization

## What are the common distributions used for initializing weights in gradient descent, and why is the choice of $\epsilon$ important?

Weights are often initialized using either:
1. A uniform distribution in the range $[-ε, ε]$, or
2. A zero-mean Gaussian of the form $\mathcal{N}(0, ε^2)$.

The choice of $ε$ is important for effective training. Widely used approaches like He initialization help in choosing appropriate $ε$.

- #machine-learning, #initialization, #optimization

## Why is symmetry breaking important in the initialization of parameters for gradient descent?

Symmetry breaking is important because if parameters are initialized with the same value (e.g., all set to zero), their updates will be the same, leading redundant units that compute the same function. Random initialization from some distribution ensures diverse updating and breaks this symmetry.

- #machine-learning, #initialization, #symmetry-breaking
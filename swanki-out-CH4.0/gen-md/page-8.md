```markdown
## Explain the update rule in stochastic gradient descent.

The basis of stochastic gradient descent (SGD) is to update the parameter vector $\mathbf{w}$ based on each data point individually, rather than using the full dataset. After the presentation of data point $n$, the update rule is given by:

$$
\mathbf{w}^{(\tau+1)}=\mathbf{w}^{(\tau)}-\eta \nabla E_{n}
$$

where:
- $\tau$ denotes the iteration number
- $\eta$ is the learning rate
- $\nabla E_{n}$ is the gradient of the error with respect to data point $n$

In this way, the parameter vector $\mathbf{w}$ is iteratively refined towards minimizing the error function $E=\sum_{n} E_{n}$.

- #optimization, #stochastic-gradient-descent.error-function

## Describe the least-mean-squares (LMS) algorithm and its update rule for sum-of-squares error function.

For the sum-of-squares error function, the update rule for the least-mean-squares (LMS) algorithm can be expressed as:

$$
\mathbf{w}^{(\tau+1)}=\mathbf{w}^{(\tau)}+\eta\left(t_{n}-\mathbf{w}^{(\tau) \mathrm{T}} \boldsymbol{\phi}_{n}\right) \boldsymbol{\phi}_{n}
$$

where:
- $\phi_{n}=\phi\left(\mathbf{x}_{n}\right)$ represents the feature vector associated with the $n$-th data point.
- $t_{n}$ is the target value of data point $n$.
- $\eta$ is the learning rate.

This algorithm is used to iteratively adjust $\mathbf{w}$ to minimize the sum-of-squares error.

- #machine-learning, #least-mean-squares.gradient-descent

## How does regularized least squares help in controlling over-fitting?

Regularized least squares adds a regularization term to the error function, balancing between the data-fit and the model complexity:

$$
E_{D}(\mathbf{w})+\lambda E_{W}(\mathbf{w})
$$

where:
- $E_{D}(\mathbf{w})$ is the error term based on data.
- $E_{W}(\mathbf{w})$ is the regularization term.
- $\lambda$ is a coefficient controlling the trade-off.

This makes the total error function to be minimized as:

$$
\frac{1}{2} \sum_{n=1}^{N}\left\{t_{n}-\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right)\right\}^{2}+\frac{\lambda}{2} \mathbf{w}^{\mathrm{T}} \mathbf{w}
$$

Regularization shrinks the model parameter values, reducing overfitting by simplifying the model.

- #machine-learning, #regularization.over-fitting

## Write down the regularization term $E_{W}(\mathbf{w})$ for the weight vector elements and describe its role.

The regularization term $E_{W}(\mathbf{w})$ is given by:

$$
E_{W}(\mathbf{w})=\frac{1}{2} \sum_{j} w_{j}^{2}=\frac{1}{2} \mathbf{w}^{\mathrm{T}} \mathbf{w}
$$

This term penalizes large values of the weight vector elements $\mathbf{w}$, encouraging smaller parameter values and reducing the risk of overfitting by controlling model complexity.

- #regularization, #machine-learning.weight-decay

## Derive the closed-form solution of $\mathbf{w}$ for the regularized least squares problem.

Given the total error function that includes regularization:

$$
\frac{1}{2} \sum_{n=1}^{N}\left\{t_{n}-\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right)\right\}^{2}+\frac{\lambda}{2} \mathbf{w}^{\mathrm{T}} \mathbf{w}
$$

The exact minimizer can be found by setting the gradient to zero and solving for $\mathbf{w}$:

$$
\mathbf{w}=\left(\lambda \mathbf{I}+\boldsymbol{\Phi}^{\mathrm{T}} \boldsymbol{\Phi}\right)^{-1} \boldsymbol{\Phi}^{\mathrm{T}} \mathbf{t}
$$

where $\boldsymbol{\Phi}$ is the design matrix composed of feature vectors $\phi(\mathbf{x}_{n})$.

- #optimization, #regularization.closed-form

## Describe what is meant by parameter shrinkage in the context of regularization.

Parameter shrinkage refers to the effect of regularization in minimizing the surplus parameter values, effectively shrinking them towards zero. This technique:

- Reduces model complexity by penalizing large weights.
- Improves generalization by making the model simpler and reducing overfitting risks.

One example is the regularizer:

$$
E_{W}(\mathbf{w})=\frac{1}{2} \sum_{j} w_{j}^{2}=\frac{1}{2} \mathbf{w}^{\mathrm{T}} \mathbf{w}
$$

incorporated into the total error function.

- #regularization, #machine-learning.parameter-shrinkage
```
## Negative Log Likelihood for Multi-class Classification

Explain the negative log likelihood function for a multi-class classification problem using the given target variable matrix $\mathbf{T}$ and output $y_{nk}$.

The negative log likelihood function for a multi-class classification problem can be expressed as:

$$
E\left(\mathbf{w}_{1}, \ldots, \mathbf{w}_{K}\right)=-\ln p\left(\mathbf{T} \mid \mathbf{w}_{1}, \ldots, \mathbf{w}_{K}\right)
$$

Expanding it further gives:

$$
E\left(\mathbf{w}_{1}, \ldots, \mathbf{w}_{K}\right) = -\sum_{n=1}^{N} \sum_{k=1}^{K} t_{n k} \ln y_{n k}
$$

where:

- $\mathbf{T}$ is an $N \times K$ matrix of target variables.
- $y_{nk} = y_k(\boldsymbol{\phi}_n)$ is the predicted output for the $k$-th class and $n$-th data point.
- $t_{nk}$ is the target variable for the $k$-th class and $n$-th data point.

This formulation represents the cross-entropy error function commonly used for multi-class classification tasks.

- #math.statistics, #machine-learning.cross-entropy-error

## Gradient of Error Function

Derive the gradient of the error function with respect to the parameter vector $\mathbf{w}_j$.

Taking the gradient of the error function with respect to the parameter vector $\mathbf{w}_j$, we utilize the derivative properties of the softmax function:

$$
\nabla_{\mathbf{w}_{j}} E\left(\mathbf{w}_{1}, \ldots, \mathbf{w}_{K}\right) = \sum_{n=1}^{N}\left(y_{n j} - t_{n j}\right) \phi_{n}
$$

where:

- $y_{nj}$ is the predicted output for the $j$-th class and $n$-th data point.
- $t_{nj}$ is the target variable for the $j$-th class and $n$-th data point.
- $\phi_n$ is the activation of the basis function for the $n$-th data point.

This gradient is used to optimize the parameters, often through stochastic gradient descent.

- #math.optimization, #machine-learning.gradient

## Cross-entropy Error Function

What is the significance of the cross-entropy error function in multi-class classification problems?

The cross-entropy error function is significant in multi-class classification problems because it quantifies the difference between the predicted probabilities and the actual target classes. It is defined as:

$$
E\left(\mathbf{w}_{1}, \ldots, \mathbf{w}_{K}\right) = -\sum_{n=1}^{N} \sum_{k=1}^{K} t_{n k} \ln y_{n k}
$$

This function penalizes predictions that deviate from the actual target classes, making it a more suitable error function for classification tasks compared to the sum-of-squares error function, which is commonly used for regression problems.

- #machine-learning.cross-entropy-error, #classification

## Gradient for Weight $w_{ij}$

Derive the gradient of the error function with respect to the weight $w_{ij}$.

The gradient of the error function with respect to the weight $w_{ij}$, which links the basis function $\phi_{i}(\mathbf{x})$ to the output unit $t_{k}$, can be obtained from:

$$
\frac{\partial E\left(\mathbf{w}_{1}, \ldots, \mathbf{w}_{K}\right)}{\partial w_{i j}} = \sum_{n=1}^{N}\left(y_{n k} - t_{n k}\right) \phi_{i}\left(\mathbf{x}_{n}\right)
$$

This gradient takes the form of the product of the output of the basis function $\phi_{i}(\mathbf{x}_{n})$ and the error $\left(y_{n k} - t_{n k}\right)$.

- #math.optimization, #machine-learning.gradient

## Importance of Basis Function in Gradient

Explain why the basis function $\phi_{n}$ is significant in the gradient of the error function.

The basis function $\phi_{n}$ is significant in the gradient of the error function because it captures the activation at the input end of the weight link and influences how the error signal $\left(y_{n j} - t_{n j}\right)$ propagates back through the network. Specifically, the gradient is formulated as:

$$
\nabla_{\mathbf{w}_{j}} E\left(\mathbf{w}_{1}, \ldots, \mathbf{w}_{K}\right) = \sum_{n=1}^{N}\left(y_{n j} - t_{n j}\right) \phi_{n}
$$

This shows that changes in the basis function activations directly impact the gradient, thus influencing the parameter updates during optimization.

- #machine-learning.neural-networks, #optimization

## Consistency of Gradient Form

Why is the gradient of the error function with respect to parameter vectors $\mathbf{w}_j$ significant in understanding linear classification models?

The gradient of the error function with respect to parameter vectors $\mathbf{w}_j$ is significant in understanding linear classification models because it reveals a consistent form similar to other models, such as logistic regression and sum-of-squares error functions. The form:

$$
\nabla_{\mathbf{w}_{j}} E\left(\mathbf{w}_{1}, \ldots, \mathbf{w}_{K}\right) = \sum_{n=1}^{N}\left(y_{n j} - t_{n j}\right) \phi_{n}
$$

illustrates a general principle where the gradient is a product of the error term $\left(y_{n j} - t_{n j}\right)$ and the basis function activation $\phi_{n}$. This consistent form facilitates understanding and application of gradient-based optimization techniques across different models.

- #machine-learning.linear-classification, #optimization.gradient
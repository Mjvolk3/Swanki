## What is the prediction function for linear regression?

The model prediction $y(\mathbf{x}, \mathbf{w})$ for linear regression is given by:

$$
y(\mathbf{x}, \mathbf{w}) = \mathbf{w}^{\mathrm{T}} \mathbf{x} + w_0
$$

where $\mathbf{w}$ is the vector of weights, $\mathbf{x}$ is the input vector, and $w_0$ is the bias term. This predicts a continuous value in the range $(-\infty, \infty)$.

- #machine-learning, #linear-regression

## How is the model prediction modified for classification problems?

For classification problems, the linear model is modified by applying a nonlinear activation function $f(\cdot)$ to the linear combination of weights:

$$
y(\mathbf{x}, \mathbf{w}) = f\left(\mathbf{w}^{\mathrm{T}} \mathbf{x} + w_0\right)
$$

This transformation allows the model to output posterior probabilities that lie within $(0,1)$.

- #machine-learning, #classification, #activation-functions

## What is an activation function in machine learning?

In machine learning, an activation function $f(\cdot)$ is used to transform a linear combination of weights and input features:

$$
y(\mathbf{x}, \mathbf{w}) = f\left(\mathbf{w}^{\mathrm{T}} \mathbf{x} + w_0\right)
$$

The purpose of the activation function is to introduce nonlinearity, enabling the model to handle complex tasks like classification.

- #machine-learning, #activation-functions

## How can basis functions transform the input space in classification models?

In classification models, the original input vector $\mathbf{x}$ can be transformed using a vector of basis functions $\phi(\mathbf{x})$. This leads to:

$$
\mathbf{\phi}(\mathbf{x}) = \left[\phi_1(\mathbf{x}), \phi_2(\mathbf{x}), \ldots, \phi_m(\mathbf{x}) \right]^T
$$

The decision boundaries will then be linear in the feature space $\mathbf{\phi}$, corresponding to nonlinear decision boundaries in the original input space $\mathbf{x}$.

- #machine-learning, #basis-functions, #nonlinear-transformations

## What is the role of the basis function $\phi_0(\mathbf{x})$ in classification models?

In classification models, one of the basis functions $\phi_0(\mathbf{x})$ is typically set to a constant (e.g., 1) so that it acts as a bias term. The corresponding parameter $w_0$ plays the role of bias in the transformed input space:

$$
\phi_0(\mathbf{x}) = 1
$$
- #machine-learning, #basis-functions, #bias

## How do nonlinear transformations affect class overlap?

Nonlinear transformations $ \phi(\mathbf{x}) $ can alter class overlap by either increasing it or creating new overlaps. Although they cannot eliminate class overlap completely, suitable choices of nonlinearity can simplify the problem of modelling posterior probabilities. These class overlaps correspond to regions where posterior probabilities are not strictly 0 or 1.

- #machine-learning, #nonlinear-transformations, #class-overlap
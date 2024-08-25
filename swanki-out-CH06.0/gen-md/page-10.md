## How are basis functions $\phi_j(\mathbf{x})$ in multi-layer neural networks designed to be trainable?

In multi-layer neural networks, the basis functions $\phi_j(\mathbf{x})$ are chosen to have learnable parameters. These parameters, along with the coefficients $\left\{w_{j}\right\}$, are adjusted during training. This allows the whole model to be optimized by minimizing an error function using gradient-based optimization methods.

- #machine-learning, #neural-networks.trainable-basis-functions

## Explain how pre-activations $a_j^{(1)}$ are formed in a basic neural network model with two layers.

Pre-activations $a_j^{(1)}$ are formed as linear combinations of the input variables $x_1, \ldots, x_D$ in the form given by:

$$
a_{j}^{(1)}=\sum_{i=1}^{D} w_{j i}^{(1)} x_{i}+w_{j 0}^{(1)}
$$

where $j=1, \ldots, M$, $w_{j i}^{(1)}$ are the weights, and $w_{j 0}^{(1)}$ are the bias parameters.

- #machine-learning, #neural-networks.pre-activations

## How are pre-activations $a_j^{(1)}$ transformed into activations $z_j^{(1)}$ in neural networks?

Pre-activations $a_j^{(1)}$ are transformed into activations $z_j^{(1)}$ using a differentiable, nonlinear activation function $h(\cdot)$ as:

$$
z_{j}^{(1)}=h\left(a_{j}^{(1)}\right)
$$

These activations $z_j^{(1)}$ represent the outputs of the basis functions or hidden units.

- #machine-learning, #neural-networks.activation-functions

## Provide the mathematical expression used to calculate the pre-activations $a_{k}^{(2)}$ in the second layer of a neural network.

The pre-activations $a_{k}^{(2)}$ in the second layer are given by:

$$
a_{k}^{(2)}=\sum_{j=1}^{M} w_{k j}^{(2)} z_{j}^{(1)}+w_{k 0}^{(2)}
$$

where $k=1, \ldots, K$, and $K$ is the total number of outputs. Here, $w_{k j}^{(2)}$ are the weights and $w_{k 0}^{(2)}$ are the bias parameters.

- #machine-learning, #neural-networks.second-layer

## What is a key requirement for the basis functions used in neural networks and why?

A key requirement for the basis functions used in neural networks is that they must be differentiable functions of their learnable parameters. This is necessary so that gradient-based optimization methods can be applied to minimize the error function during training.

- #machine-learning, #neural-networks.basis-function-requirements

## Why can the construction of basis functions in neural networks naturally extend to hierarchical models with many layers?

The construction of basis functions in neural networks can naturally extend to hierarchical models with many layers because each basis function is a nonlinear function of a linear combination of inputs, and the coefficients in these linear combinations are learnable parameters. By recursively applying this structure, a hierarchical model, such as a deep neural network, can be formed which can capture complex patterns in data through multiple layers of nonlinear transformations.

- #machine-learning, #neural-networks.hierarchical-models
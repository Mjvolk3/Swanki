## What is the significance of sign-flip symmetries in neural networks?

The sign-flip symmetry indicates that by changing the signs of a particular group of weights (and a bias) in a neural network, the input-output mapping function represented by the network remains unchanged. This suggests the existence of multiple equivalent weight vectors that yield the same mapping function.

For $M$ hidden units, there are $2^M$ such sign-flip symmetries.

$$
\tanh(-a) = -\tanh(a)
$$


- #deep-learning, #neural-networks.symmetry

## How can weight-vector interchanges affect the input-output mapping function in a neural network with M hidden units?

Interchanging the values of all weights (and biases) leading both into and out of a particular hidden unit, with those of a different unit, leaves the input-output mapping function unchanged but corresponds to a different weight vector. Such interchanges account for $M!$ equivalent weight vectors.

- #deep-learning, #neural-networks.symmetry

## How is the overall weight-space symmetry factor for an M-hidden-unit network calculated?

The overall weight-space symmetry factor for a network with $M$ hidden units is given by:

$$
M! \cdot 2^M
$$

This factor results from combining sign-flip symmetries and weight-vector interchange symmetries.

- #deep-learning, #neural-networks.symmetry-factor

## Describe the general form of the weight-space symmetries in neural networks beyond the tanh activation function.

The weight-space symmetries apply to a wide range of activation functions, not just tanh. These symmetries occur because the input-output mapping can remain unchanged despite different equivalent weight vectors due to sign-flip and interchange symmetries. This principle holds broadly in neural networks.

- #deep-learning, #neural-networks.activation-functions

## What is the significance of weight-space symmetries in Bayesian methods for evaluating neural networks?

Weight-space symmetries play a role when Bayesian methods are used to evaluate the probability distribution over networks of different sizes. These symmetries imply that multiple weight configurations can produce the same network behavior, influencing the Bayesian assessment of model probabilities.

- #deep-learning, #bayesian-methods.neural-networks

## Explain how the two-layer network architecture can be extended to any finite number of layers in a neural network.

The two-layer network architecture can be extended to any finite number $L$ of layers, where each layer $l = 1, \ldots, L$ computes the function:

$$
\mathbf{z}^{(l)} = h^{(l)}\left(\mathbf{W}^{(l)} \mathbf{z}^{(l-1)}\right)
$$

Here, $\mathbf{z}^{(l)}$ is the activation at layer $l$, $h^{(l)}$ is the activation function, $\mathbf{W}^{(l)}$ are the weights, and $\mathbf{z}^{(l-1)}$ is the activation from the previous layer.

- #deep-learning, #neural-networks.multi-layer
## Explain the activation functions for output and hidden units in the two-layer network example.

In the two-layer network example, the output units have linear activation functions, meaning that $y_k = a_k$. On the other hand, the hidden units use a sigmoidal activation function given by:

$$
h(a) \equiv \tanh (a)
$$

The derivative of this activation function is expressed as:

$$
h^{\prime}(a) = 1 - h(a)^2
$$

- #neural-networks.activation-functions, #deep-learning


## What is the error function used for the two-layer network example in backpropagation?

The error function used for a given data point $n$ in the two-layer network example is a sum-of-squares error function:

$$
E_n = \frac{1}{2} \sum_{k=1}^{K} (y_k - t_k)^2
$$

where $y_k$ is the activation of output unit $k$, and $t_k$ is the corresponding target value.

- #neural-networks.error-functions, #backpropagation

## Describe the forward propagation steps for the two-layer network.

The forward propagation for the two-layer network is performed using the following equations:

$$
\begin{aligned}
a_j & = \sum_{i=0}^{D} w_{ji}^{(1)} x_i \\
z_j & = \tanh(a_j) \\
y_k & = \sum_{j=0}^{M} w_{kj}^{(2)} z_j
\end{aligned}
$$

where $D$ is the dimensionality of the input vector $\mathbf{x}$, and $M$ is the total number of hidden units. $x_0$ and $z_0$ are set to 1 to include bias parameters.

- #neural-networks.forward-propagation, #deep-learning

## How are the $\delta$'s for the output units calculated in backpropagation?

The $\delta$'s for the output units are calculated using the equation:

$$
\delta_k = y_k - t_k
$$

where $y_k$ is the output of unit $k$ and $t_k$ is the target value for that unit.

- #neural-networks.backpropagation, #deep-learning

## How are the $\delta$'s for the hidden units calculated in backpropagation?

The $\delta$'s for the hidden units are calculated by backpropagating the errors using:

$$
\delta_j = (1 - z_j^2) \sum_{k=1}^{K} w_{kj}^{(2)} \delta_k
$$

where $z_j$ is the activation of the hidden unit and $w_{kj}^{(2)}$ are the weights connecting hidden unit $j$ to output unit $k$.

- #neural-networks.backpropagation, #deep-learning

## Explain the utility of the derivative of the activation function $h(a) \equiv \tanh(a)$ in backpropagation.

A useful feature of the $\tanh(a)$ activation function is that its derivative can be expressed in a simple form:

$$
h^{\prime}(a) = 1 - h(a)^2
$$

This simplicity facilitates the calculation of the gradients needed for updating the weights in the backpropagation algorithm.

- #neural-networks.activation-functions, #backpropagation-utility
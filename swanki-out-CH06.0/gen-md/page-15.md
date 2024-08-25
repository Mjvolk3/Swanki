## Describe the vanishing gradients problem and mention how the softplus activation function mitigates it.

The vanishing gradients problem occurs when the gradients used in the backpropagation algorithm become very small, particularly as they are propagated to earlier layers in a deep neural network. This can severely impede training as the updates to the network weights become minimal. The softplus activation function is one choice that helps mitigate this issue, especially for large positive input values.

$$
h(a) = \ln(1 + \exp(a))
$$

- #deep-learning, #neural-networks.activation-functions

## Give the definition of the rectified linear unit (ReLU) activation function and discuss its empirical performance.

The rectified linear unit (ReLU) is an activation function defined by

$$
h(a) = \max(0, a)
$$

Empirically, ReLU is one of the best-performing activation functions and is widely used. It shows a significant advantage in terms of training efficiency over previous sigmoidal activation functions and is well-suited for low-precision implementations.

- #deep-learning, #neural-networks.activation-functions

## Define the leaky ReLU activation function and explain how it addresses issues associated with the standard ReLU.

The leaky ReLU activation function is defined as

$$
h(a) = \max(0, a) + \alpha \min(0, a)
$$

where $0<\alpha<1$. Unlike the standard ReLU, leaky ReLU has a non-zero gradient for negative input values, ensuring that there is a signal to drive training even for $a < 0$.

- #deep-learning, #neural-networks.activation-functions

## What is a potential issue with the derivative of the ReLU function, and why is it not a major concern in practice?

The derivative of the ReLU function is not defined when $a=0$. However, in practice, this can be safely ignored as it rarely impacts the performance or learning process of neural networks.

$$
h(a) = \max(0, a)
$$

- #deep-learning, #neural-networks.activation-functions, neural-networks.training-issues

## Discuss how weight-space symmetries can affect the learning process in feed-forward neural networks.

Weight-space symmetries refer to the phenomenon where multiple distinct choices for the weight vector $\mathbf{w}$ can produce the same mapping function from inputs to outputs. This can potentially create redundancy in parameter space, leading to inefficiencies during training.

$$
\text{Consider a two-layer network with $M$ hidden units and tanh activation functions.}
$$

- #deep-learning, #neural-networks.weight-space

## Explain how the introduction of ReLU has impacted the training of deep neural networks.

The introduction of ReLU has brought significant improvements in training efficiency, especially compared to sigmoidal activation functions. ReLU allows deeper networks to be trained more efficiently, is less sensitive to the random initialization of weights, and is computationally cheaper to evaluate.

$$
h(a) = \max(0, a)
$$

- #deep-learning, #neural-networks.training-efficiency
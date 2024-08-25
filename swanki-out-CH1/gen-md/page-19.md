**Card 1**

## Explain the form of the function computed by each hidden unit and each output unit in the neural network as described in the text.

The form of the function computed by each hidden unit and each output unit in the neural network is given by:

$$
z_j = \sum_i w_{ji} x_i + b_j \quad \text{(1.5)}
$$

where $z_j$ is a weighted sum of the inputs $x_i$ with weights $w_{ji}$ and bias $b_j$, followed by:

$$
a_j = f(z_j) \quad \text{(1.6)}
$$

where $f$ is a differentiable activation function. This process determines the activation $a_j$ of the unit.

- #machine-learning, #neural-networks, #activation-functions

**Card 2**

## Describe the training process of a neural network, including the initialization of parameters and the optimization technique used.

The training process of a neural network involves the following steps:

1. **Initialization of Parameters**: The parameters, which include weights and biases, are initialized using a random number generator.

2. **Optimization Technique**: Stochastic gradient descent (SGD) is typically used. This involves iteratively updating the parameters to minimize the error function.

The error function's derivatives are evaluated and used to update the parameters efficiently via a method known as error backpropagation. During backpropagation, information flows backward through the network from outputs to inputs.

- #machine-learning, #neural-networks, #gradient-descent

**Card 3**

## What is error backpropagation and how does it facilitate the training of neural networks?

Error backpropagation is a method used to update the parameters of a neural network during training. It involves the following steps:

1. **Forward Pass**: Compute the output of the network using the current set of parameters.
2. **Backward Pass**: Calculate the gradient of the error function with respect to each parameter by propagating the error backward through the network.
3. **Parameter Update**: Update the parameters using the gradient information, typically with an optimization algorithm like stochastic gradient descent (SGD).

This process allows the network to minimize the error function effectively.

- #machine-learning, #neural-networks, #backpropagation

**Card 4**

## What is the sum-of-squares error function and how is it used in the context of neural networks?

The sum-of-squares error function is used to measure the discrepancy between the actual output and the predicted output of a neural network. It is defined as:

$$
E = \frac{1}{2} \sum_{n} \| \mathbf{y}^{(n)} - \mathbf{\hat{y}}^{(n)} \|^2 \quad \text{(1.2)}
$$

where $\mathbf{y}^{(n)}$ is the actual output and $\mathbf{\hat{y}}^{(n)}$ is the predicted output for the $n$-th training example. The goal is to minimize this error function during training.

- #machine-learning, #neural-networks, #error-functions

**Card 5**

## Discuss the significance of stochastic gradient descent (SGD) in the training of neural networks as mentioned in the text.

Stochastic gradient descent (SGD) is a crucial optimization technique used in training neural networks. Its importance lies in:

1. **Efficiency**: It updates parameters using a few training examples at a time instead of the whole dataset, making it computationally efficient.
2. **Convergence**: It can help the model converge to the optimal solution by iteratively adjusting the parameters based on the gradient of the error function.
3. **Simplicity**: It is simple to implement and requires minimal computational resources compared to other optimization algorithms.

SGD plays a pivotal role in adjusting the weights and biases of a network to minimize the error function effectively.

- #machine-learning, #neural-networks, #optimization-algorithms
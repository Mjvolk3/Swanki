## What does the image illustrate in the context of neural networks?

![](https://cdn.mathpix.com/cropped/2024_05_26_5df28c9d7a64baac9eefg-1.jpg?height=308&width=491&top_left_y=215&top_left_x=1149)

%

The image illustrates the concept of backpropagation in neural networks. It shows three nodes representing units in a network, where the central unit (with activation $z_j$) connects to two other units (with activations $z_i$ and $\delta_k$, $\delta_l$) via weighted connections. The forward pass of information, indicated by black arrows, moves from the $z_i$ node through the weight $w_{ji}$, processes in the $z_j$ node, and then moves outwards through the weights $w_{kj}$, $w_{lj}$. The red arrows represent the backward propagation of errors ($\delta$'s), which are used to adjust weights during the training phase.

- neural-networks, backpropagation.illustration, machine-learning.training


## What is equation (8.10) in the context of backpropagation, and how is it derived?

![](https://cdn.mathpix.com/cropped/2024_05_26_5df28c9d7a64baac9eefg-1.jpg?height=308&width=491&top_left_y=215&top_left_x=1149)

%

Equation (8.10) in the context of backpropagation is:

$$
\frac{\partial E_{n}}{\partial w_{j i}}=\delta_{j} z_{i}
$$

This equation tells us that the derivative of the error $E_n$ with respect to the weight $w_{ji}$ is obtained by multiplying the value of $\delta$ for the unit at the output end of the weight by the value of $z$ for the unit at the input end of the weight (where $z=1$ for a bias). The derivation involves using partial derivatives $\frac{\partial a_{j}}{\partial w_{j i}}=z_{i}$ and substituting it into related expressions, confirming the form similar to that found for a simple linear model.

- neural-networks.equations, backpropagation.derivation, machine-learning.training
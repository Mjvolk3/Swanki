### Card 1

How is the derivative $\frac{\partial E_{n}}{\partial w_{j i}}$ calculated in the context of backpropagation?

![](https://cdn.mathpix.com/cropped/2024_05_26_5df28c9d7a64baac9eefg-1.jpg?height=308&width=491&top_left_y=215&top_left_x=1149)

%

The derivative $\frac{\partial E_{n}}{\partial w_{j i}}$ is calculated by multiplying the value of $\delta_{j}$ for the unit at the output end of the weight by the value of $z_{i}$ for the unit at the input end of the weight:

$$
\frac{\partial E_{n}}{\partial w_{j i}}=\delta_{j} z_{i}
$$

Note that $z=1$ for a bias.

- neural-networks.backpropagation, #machine-learning, #derivatives

### Card 2

What does the backpropagation algorithm involve in terms of error terms and forward/backward propagation?

![](https://cdn.mathpix.com/cropped/2024_05_26_5df28c9d7a64baac9eefg-1.jpg?height=308&width=491&top_left_y=215&top_left_x=1149)

%

The backpropagation algorithm involves the following:
- Forward propagation of activation through the network (black arrows in the figure).
- Backward propagation of errors (\(\delta\)'s) to compute gradients (red arrows in the figure).
- Calculation of derivatives \(\frac{\partial E_{n}}{\partial w_{j i}} = \delta_{j} z_{i}\).
- Adjustment of weights using the gradients.

- neural-networks.backpropagation, #machine-learning, #algorithm


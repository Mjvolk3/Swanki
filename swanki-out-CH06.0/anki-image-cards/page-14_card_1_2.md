## What is the mathematical definition of the hyperbolic tangent activation function, and how does it differ from the logistic sigmoid function?

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=1026&width=1497&top_left_y=200&top_left_x=150)

% 

The hyperbolic tangent activation function is defined by:

$$
\tanh (a)=\frac{e^{a}-e^{-a}}{e^{a}+e^{-a}}
$$

It differs from the logistic sigmoid function by a linear transformation of its input and output values. Specifically, the tanh function outputs values between -1 and 1 versus the sigmoid's 0 and 1.

- #machine-learning, #neural-networks.activation-functions

## Describe the "leaky ReLU" activation function and how it differs from the standard ReLU.

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=1026&width=1497&top_left_y=200&top_left_x=150)

% 

The "leaky ReLU" activation function is similar to the standard ReLU, but it allows a small, non-zero output for negative inputs. The function is typically defined by:

$$
f(x) = 
\begin{cases} 
x & \text{if } x \geq 0 \\
\alpha x & \text{if } x < 0
\end{cases}
$$

where $\alpha$ is a small slope parameter (often 0.01).

Unlike the standard ReLU which outputs 0 for all negative inputs, the leaky ReLU ensures that there is a small gradient for negative inputs, potentially mitigating the "dying ReLU" problem.

- #machine-learning, #neural-networks.activation-functions
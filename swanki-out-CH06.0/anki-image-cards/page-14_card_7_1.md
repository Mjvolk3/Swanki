## Describe the tanh activation function and its relationship to the logistic sigmoid function as shown in Figure 6.12(a).

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=439&width=491&top_left_y=721&top_left_x=1152)

%

The tanh activation function is defined by:

$$
\tanh(a) = \frac{e^a - e^{-a}}{e^a + e^{-a}}
$$

It is closely related to the logistic sigmoid function, differing by a linear transformation of its input and output values. For any network with logistic-sigmoid hidden-unit activation functions, there is an equivalent network with tanh activation functions.

- #neural-networks, #activation-functions.hyperbolic-tangent, #comparison.logistic-sigmoid

## What distinguishes the tanh function from the absolute value function in terms of neural network activation functions?

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=439&width=491&top_left_y=721&top_left_x=1152)

%

The tanh function is smooth and differentiable, defined by:

$$
\tanh(a) = \frac{e^a - e^{-a}}{e^a + e^{-a}}
$$

In contrast, the absolute value function, often depicted as V-shaped, is continuous but non-differentiable at the origin. The absolute value function is linear elsewhere, reflecting its input about the y-axis when the input is negative. 

In neural networks, smooth differentiable functions like tanh are often preferred for backpropagation, whereas the absolute value function, being non-differentiable at zero, is less commonly used as an activation function. 

- #neural-networks, #activation-functions, #mathematics.analysis
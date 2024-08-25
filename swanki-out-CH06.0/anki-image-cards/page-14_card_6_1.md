## What is the equation of the tanh activation function and what kind of behavior does it exhibit?

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=442&width=491&top_left_y=219&top_left_x=1152)

%
The tanh activation function is defined by the equation

$$
\tanh(a) = \frac{e^a - e^{-a}}{e^a + e^{-a}}
$$

The function differs from the logistic sigmoid by a linear transformation of its input and its output values. It ranges from -1 to 1 and is often used to map input values to a range between these limits.

- #neural-networks, #activation-functions, #tanh

## Describe the equational form and behavior of the softplus activation function plotted above.

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=442&width=491&top_left_y=219&top_left_x=1152)

%
The softplus activation function is given by the equation 

$$
h(a) = \ln(1 + \exp(a)).
$$

The function approaches a linear behavior for large positive input values, helping to alleviate the problem of vanishing gradients. It provides a smooth curve transition from low to high output values.

- #neural-networks, #activation-functions, #softplus
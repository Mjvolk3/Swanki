### Card 1

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=442&width=491&top_left_y=219&top_left_x=1152)

What is the definition of the $\tanh$ function, and how does it compare to the logistic sigmoid function?

%

The $\tanh$ function is defined as:

$$
\tanh (a) = \frac{e^{a} - e^{-a}}{e^{a} + e^{-a}}
$$

It differs from the logistic sigmoid function by a linear transformation of its input and its output values. Therefore, for any network with logistic-sigmoid hidden-unit activation functions, there exists an equivalent network with $\tanh$ activation functions.

- tags: #neural-networks.activation-functions, #mathematics.tanh

### Card 2

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=442&width=476&top_left_y=216&top_left_x=658)

Describe the "hard tanh" function and its graph as seen in the image.

%

The "hard tanh" function is a piecewise linear function commonly used as an activation function in neural networks. It is defined as follows:
- Output is $-1$ for inputs less than $-1$
- Output is $+1$ for inputs greater than $1$
- Linear with a slope of 1 between inputs $-1$ and 1

The graph of the "hard tanh" function demonstrates sharp transitions at input values of $-1$ and $1$, contrasting with the smoother curve of the standard $\tanh$ function.

- tags: #neural-networks.activation-functions, #mathematics.hard-tanh
## Card 1

How is the tanh activation function defined mathematically and how does it differ from the logistic sigmoid function?

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=442&width=476&top_left_y=216&top_left_x=658)

%

The tanh activation function is defined as:

$$\tanh (a)=\frac{e^{a}-e^{-a}}{e^{a}+e^{-a}}$$

It differs from the logistic sigmoid function by a linear transformation of its input and its output values. Consequently, for any network with logistic-sigmoid hidden-unit activation functions, there is an equivalent network with tanh activation functions.

- neural-networks.activation-functions, functional-analysis.hyperbolic-functions

## Card 2

Describe the characteristics and the definition of the hard tanh activation function as shown in the image.

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=442&width=476&top_left_y=216&top_left_x=658)

%

The hard tanh activation function is a piecewise linear function defined as follows:

- Outputs -1 for inputs less than -1
- Outputs +1 for inputs greater than 1
- Linear with a slope of 1 between -1 and 1

The graph depicts sharp transitions at the input values of -1 and 1, distinguishing it from the smoother, sigmoid-shaped curve of the standard tanh function.

- neural-networks.activation-functions, functional-analysis.piecewise-functions
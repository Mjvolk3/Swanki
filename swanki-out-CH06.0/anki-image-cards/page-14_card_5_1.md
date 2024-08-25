## What is the formula for the tanh activation function and how does it compare to the logistic sigmoid function?

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=440&width=481&top_left_y=723&top_left_x=658)

%

The tanh activation function is defined by:

$$
\tanh (a)=\frac{e^{a}-e^{-a}}{e^{a}+e^{-a}}
$$

It differs from the logistic sigmoid function by a linear transformation of its input and its output values. For any network with logistic-sigmoid hidden-unit activation functions, there is an equivalent network with tanh activation functions.

- #neural-networks, #activation-functions, #mathematics.tanh


## What is the leaky ReLU activation function and why is it used?

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=440&width=481&top_left_y=723&top_left_x=658)

%

The leaky ReLU (Rectified Linear Unit) activation function is given by:

$$
h(a) = \max(0, a) + \alpha \min(0, a)
$$

where \( \alpha \) is a small, positive parameter that allows for a non-zero gradient when the input \( a \) is negative. 

It is used to prevent the "dying ReLU" problem, where units never activate during training because they have a negative input. The smaller positive slope for negative inputs helps maintain the gradient flow, thus enabling better training convergence.

- #neural-networks, #activation-functions, #leaky-relu
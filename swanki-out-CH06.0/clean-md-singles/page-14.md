![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=1026&width=1497&top_left_y=200&top_left_x=150)

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=442&width=473&top_left_y=214&top_left_x=169)

(a)

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=437&width=486&top_left_y=719&top_left_x=158)

(d)

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=442&width=476&top_left_y=216&top_left_x=658)

(b)

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=440&width=481&top_left_y=723&top_left_x=658)

(e)

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=442&width=491&top_left_y=219&top_left_x=1152)

(c)

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=439&width=491&top_left_y=721&top_left_x=1152)

(f)

Figure 6.12 A variety of nonlinear activation functions.

biological neurons. A closely related function is tanh, which is defined by

$$
\tanh (a)=\frac{e^{a}-e^{-a}}{e^{a}+e^{-a}}
$$

which is plotted in Figure 6.12(a). This function differs from the logistic sigmoid by a linear transformation of its input and its output values, and so for any network

\title{
Exercise 6.4
} with logistic-sigmoid hidden-unit activation functions, there is an equivalent network with tanh activation functions. However, when training a network, these are not necessarily equivalent because for gradient-based optimization, the network weights and biases need to be initialized, and so if the activation functions are changed, then the initialization scheme must be adjusted accordingly. A 'hard' version of the tanh function (Collobert, 2004) is given by

$$
h(a)=\max (-1, \min (1, a))
$$

and is plotted in Figure 6.12(b).

A major drawback of both the logistic sigmoid and the tanh activation functions is that the gradients go to zero exponentially when the inputs have either large positive or large negative values. We will discuss this 'vanishing gradients' issue later,
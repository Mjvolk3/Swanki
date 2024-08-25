Given the detailed chunk from the paper, I'll create 6 detailed Anki cards focusing on scientific details and math equations.

---

## What is the mathematical definition of the tanh activation function?

The tanh (hyperbolic tangent) activation function is defined by

$$
\tanh(a) = \frac{e^a - e^{-a}}{e^a + e^{-a}}
$$

This function maps real values to the range $(-1, 1)$ and is commonly used in neural networks.

- #neural-networks, #activation-functions, #tanh

---

## Describe the relationship between the logistic sigmoid function and the tanh function.

The tanh function differs from the logistic sigmoid function by a linear transformation of its input and its output values. For any network with logistic-sigmoid hidden-unit activation functions, there is an equivalent network with tanh activation functions. 

Both functions are given by:

$$
\sigma(x) = \frac{1}{1 + e^{-x}} \quad \text{and} \quad \tanh(a) = \frac{e^a - e^{-a}}{e^a + e^{-a}}
$$

However, they are not necessarily equivalent when training a network because gradient-based optimization depends on the network weights and biases initialization.

- #neural-networks, #activation-functions, #sigmoid

---

## What is the 'hard' version of the tanh function?

The 'hard' version of the tanh function is given by

$$
h(a) = \max(-1, \min(1, a))
$$

This function is a piecewise linear approximation of the tanh function and is commonly used for computational efficiency.

- #neural-networks, #activation-functions, #piecewise-functions

---

## What is a major drawback of both the logistic sigmoid and the tanh activation functions?

A major drawback of both the logistic sigmoid and the tanh activation functions is the 'vanishing gradients' issue. The gradients go to zero exponentially when the inputs have either large positive or large negative values.

- #neural-networks, #activation-functions, #vanishing-gradients

---

## Why are logistic sigmoid and tanh activation functions not necessarily equivalent when training a network?

Logistic sigmoid and tanh activation functions are not necessarily equivalent when training a network because gradient-based optimization requires specific initialization of weights and biases. Changing activation functions necessitates adjustments in the initialization scheme to maintain effective training.

- #neural-networks, #activation-functions, #initialization

---

## What is the range of the tanh activation function?

The tanh activation function maps real-valued inputs to the range $(-1, 1)$:

$$
\tanh(a) = \frac{e^a - e^{-a}}{e^a + e^{-a}}
$$

This is in contrast to the logistic sigmoid function, which maps inputs to the range $(0, 1)$.

- #neural-networks, #activation-functions, #range
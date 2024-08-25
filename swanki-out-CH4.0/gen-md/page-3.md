```markdown
## Describe the linear regression model in terms of a neural network diagram. Include reference to the basis functions and parameters.

The linear regression model can be expressed as a simple neural network diagram involving a single layer of parameters. Each basis function $\phi_{j}(\mathbf{x})$ is represented by an input node, with the solid node representing the 'bias' basis function $\phi_{0}$. The function $y(\mathbf{x}, \mathbf{w})$ is represented by an output node. Each of the parameters $w_{j}$ is shown by a line connecting the corresponding basis function to the output.

#machine-learning, #linear-regression.model

## Explain why deep learning uses learned transformations instead of fixed basis functions, as practiced before deep learning.

Before deep learning, machine learning often used fixed pre-processing of input variables $\mathbf{x}$ through a set of basis functions $\left\{\phi_{j}(\mathbf{x})\right\}$, which is also known as feature extraction. The goal was to have a sufficiently powerful set of basis functions so that the learning task could be solved using a simple network model. However, handcrafting suitable basis functions was difficult for anything but the simplest applications. Deep learning avoids this by learning the required nonlinear transformations of the data directly from the data set.

#deep-learning, #basis-functions.feature-extraction

## How can the polynomial function from Chapter 1 be expressed as a linear regression model? Include the relevant equations and explanation.

The polynomial function from Chapter 1 can be expressed in the form of a linear regression model (4.3) by considering a single input variable $x$ and choosing basis functions defined by $\phi_{j}(x)=x^{j}$. In this case, the form of the model is:

$$
y(x, \mathbf{w}) = \sum_{j=0}^{M} w_j \phi_j(x) = \sum_{j=0}^{M} w_j x^j
$$

where $M$ is the degree of the polynomial and $w_j$ are the learnable parameters.

#polynomials, #linear-regression

## What are Gaussian basis functions and how are they parameterized? Provide the relevant equations.

Gaussian basis functions are defined as:

$$
\phi_{j}(x)=\exp \left\{-\frac{\left(x-\mu_{j}\right)^{2}}{2 s^{2}}\right\}
$$

In this equation, $\mu_{j}$ governs the locations of the basis functions in input space, and the parameter $s$ governs their spatial scale. These basis functions do not need a probabilistic interpretation as their normalization coefficient is unimportant since they are multiplied by learnable parameters $w_{j}$.

#gaussian-functions, #basis-functions.parameterization

## Define the sigmoidal basis function and the logistic sigmoid function. Explain their relationship with the tanh function.

The sigmoidal basis function is of the form:

$$
\phi_{j}(x)=\sigma\left(\frac{x-\mu_{j}}{s}\right)
$$

where $\sigma(a)$ is the logistic sigmoid function defined by:

$$
\sigma(a)=\frac{1}{1+\exp (-a)}
$$

The tanh function is related to the logistic sigmoid by:

$$
\tanh (a)=2 \sigma(2 a)-1
$$

This means a general linear combination of logistic sigmoid functions is equivalent to a general linear combination of tanh functions in representing the same class of input-output functions.

#sigmoidal-functions, #logistic-sigmoid.tanh

## Explain the importance of basis functions in regression models and their evolution with the advent of deep learning.

Basis functions in regression models serve to transform the input variables into a space where a linear combination of the basis functions can effectively model the target function. Traditional models relied on predefined sets of basis functions, which required domain expertise and significant effort to craft. With the advent of deep learning, the need for predefined basis functions decreased as neural networks can learn suitable non-linear transformations from data, thus automating and improving the feature extraction process.

#regression-models, #basis-functions.evolution
```
  
### Card 1

![](https://cdn.mathpix.com/cropped/2024_05_26_a31248c38a71950d5cfdg-1.jpg?height=532&width=709&top_left_y=274&top_left_x=935)

Explain the role of bias parameters in the two-layer neural network depicted in the diagram.

%

The bias parameters in the two-layer neural network model play a crucial role in adjusting the output alongside weighted inputs. They can be absorbed into the set of weight parameters by defining an additional input variable \( x_{0} \), which is clamped at \( x_{0}=1 \). Therefore, the overall network function becomes:

$$
y_{k}(\mathbf{x}, \mathbf{w})=f\left(\sum_{j=0}^{M} w_{k j}^{(2)} h\left(\sum_{i=0}^{D} w_{j i}^{(1)} x_{i}\right)\right)
$$

where \( f(\cdot) \) and \( h(\cdot) \) are non-linear functions applied element-wise for activation, \( w_{j i}^{(1)} \) are the weights for the first layer, and \( w_{k j}^{(2)} \) are the weights for the second layer.

- #neural-networks, #machine-learning.bias, #feedforward-networks

### Card 2

![](https://cdn.mathpix.com/cropped/2024_05_26_a31248c38a71950d5cfdg-1.jpg?height=532&width=709&top_left_y=274&top_left_x=935)

Describe how the input and weight parameters are organized in the described neural network model.

%

In the described neural network model, the input variables are represented as a column vector \( \mathbf{x}=\left(x_{1}, \ldots, x_{N}\right)^{\mathrm{T}} \). The weight and bias parameters are organized into matrices, allowing the network function to be expressed as:

$$
\mathbf{y}(\mathbf{x}, \mathbf{w})=f\left(\mathbf{W}^{(2)} h\left(\mathbf{W}^{(1)} \mathbf{x}\right)\right)
$$

where:

- \( \mathbf{W}^{(1)} \) is the matrix of weights connecting the input layer to the hidden layer.
- \( \mathbf{W}^{(2)} \) is the matrix of weights connecting the hidden layer to the output layer.
- \( f(\cdot) \) is the activation function applied to the output layer.
- \( h(\cdot) \) is the activation function applied to the hidden layer.

Each matrix element and vector element are operated on separately during the computation.

- #neural-networks, #machine-learning.weights, #parameter-organization
## Card 1

![](https://cdn.mathpix.com/cropped/2024_05_26_a31248c38a71950d5cfdg-1.jpg?height=532&width=709&top_left_y=274&top_left_x=935)

What do the nodes and links represent in the two-layer neural network diagram?

%

In the two-layer neural network diagram:

- Nodes represent variables:
  - Input variables \( x_0 \) to \( x_D \) (with \( x_0 \) as the bias parameter).
  - Hidden units \( z_1 \) to \( z_M \) (with \( z_0 \) as the bias parameter).
  - Output variables \( y_1 \) to \( y_K \).

- Links represent weight parameters:
  - \( w^{(1)} \) for connections between input and hidden layers.
  - \( w^{(2)} \) for connections between hidden and output layers.

- Arrows indicate the direction of information flow during forward propagation.

- Weights \( w^{(1)}_{10} \) and \( w^{(2)}_{10} \) correspond to bias weights.

- #neural-networks, #machine-learning, #parameter-representation

## Card 2

![](https://cdn.mathpix.com/cropped/2024_05_26_a31248c38a71950d5cfdg-1.jpg?height=532&width=709&top_left_y=274&top_left_x=935)

Explain how bias parameters can be integrated into weight parameters in a two-layer neural network.

%

Bias parameters can be integrated into weight parameters by defining an additional input variable \( x_0 \) with value clamped at 1. This allows the bias term to be absorbed into the weight matrix. For the first layer, the transformation is:

$$
a_j = \sum_{i=0}^{D} w_{ji}^{(1)} x_i
$$

For the second layer, the overall network function becomes:

$$
y_k(\mathbf{x}, \mathbf{w}) = f\left(\sum_{j=0}^{M} w_{kj}^{(2)} h\left(\sum_{i=0}^{D} w_{ji}^{(1)} x_i\right)\right)
$$

Using matrices, this is compactly written as:

$$
\mathbf{y}(\mathbf{x}, \mathbf{w}) = f\left(\mathbf{W}^{(2)} h\left(\mathbf{W}^{(1)} \mathbf{x}\right)\right)
$$

- #neural-networks, #machine-learning, #bias-integration
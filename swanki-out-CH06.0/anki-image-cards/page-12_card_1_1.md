## Analyze the approximation of a quadratic function using a neural network.

![](https://cdn.mathpix.com/cropped/2024_05_26_53b5c38c9dec90db1928g-1.jpg?height=401&width=491&top_left_y=222&top_left_x=624)

What do the blue dots, red curve, and dashed curves represent in the image?

%

The blue dots represent 50 data points sampled uniformly over the interval \([ -1, 1 ] \). The red curve indicates the output of the trained neural network, which approximates the parabolic shape of the quadratic function \( f(x) = x^2 \). The dashed curves, each in a different color, represent the outputs from the three hidden units with tanh activation functions within the neural network.

- #neural-networks.two-layer, #function-approximation.quadratic

## Describe the universal approximation theorem as mentioned in the associated text.

![](https://cdn.mathpix.com/cropped/2024_05_26_53b5c38c9dec90db1928g-1.jpg?height=401&width=491&top_left_y=222&top_left_x=624)

%

The universal approximation theorem states that, for a wide range of activation functions, two-layer feed-forward networks can approximate any function defined over a continuous subset of $\mathbb{R}^{D}$ to arbitrary accuracy. This theorem also holds for functions from any finite-dimensional discrete space to another, making neural networks universal approximators. However, the theorem only guarantees the existence of such a network, not that the required function can be easily found or trained.

- #neural-networks.theorems, #approximation.universal
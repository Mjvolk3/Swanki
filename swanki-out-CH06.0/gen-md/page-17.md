### Card 1

Neural networks with two layers of learnable parameters have universal approximation capabilities; however, deeper networks can represent functions more efficiently. Describe the result found by Montúfar et al. (2014) regarding the division of input space and parameter efficiency.

The result found by Montúfar et al. (2014) states that the network function divides the input space into a number of regions that is exponential in the depth of the network, but polynomial in the width of the hidden layers. To represent the same function using a two-layer network would require an exponential number of hidden units.

- #neural-networks, #deep-learning, #machine-learning.capacity

### Card 2

Define what the variables $h^{(l)}$, $\mathbf{W}^{(l)}$, $\mathbf{z}^{(0)}$, and $\mathbf{z}^{(L)}$ represent in the context of a neural network.

In the context of the neural network:

- $h^{(l)}$ denotes the activation function associated with layer $l$.
- $\mathbf{W}^{(l)}$ is the matrix of weight and bias parameters for layer $l$.
- $\mathbf{z}^{(0)} = \mathbf{x}$ represents the input vector.
- $\mathbf{z}^{(L)} = \mathbf{y}$ represents the output vector.

- #neural-networks, #deep-learning, #activation-functions

### Card 3

In the context of network architecture, clarify why the terminology of a network with layers of learnable weights is important. Given an example, which nomenclature should be used based on the paper's recommendation?

The paper recommends counting the number of layers of learnable weights for terminology. Thus, a network described sometimes as a three-layer network (counting input, hidden, and output) or sometimes as having a single-hidden-layer should be called a two-layer network, focusing on the learnable weights rather than the input layer.

- #neural-networks, #terminology, #network-architecture

### Card 4

Explain how a deep neural network facilitates object recognition in images, such as identifying a 'cat', through hierarchical representations?

In a deep neural network, early layers learn to detect low-level features such as edges. Subsequent layers combine these low-level features to form higher-level features like eyes or whiskers. These higher-level features are then combined in further layers to detect complex objects such as a cat, exemplifying a hierarchical compositional inductive bias.

- #neural-networks, #deep-learning, #image-recognition

### Card 5

What is the primary motivation for exploring deeper neural networks beyond their universal approximation capabilities?

Beyond universal approximation capabilities, a compelling reason to explore deep neural networks is that they encode a particular form of inductive bias. For example, in image recognition tasks, the architecture allows the network to detect low-level features in initial layers and combine them hierarchically to recognize complex objects, providing an efficient way to handle highly complex and nonlinear relationships.

- #neural-networks, #deep-learning, #inductive-bias

### Card 6

What does the concept of distributed representation in neural networks refer to, and how is it beneficial?

Distributed representation in neural networks refers to each unit in a hidden layer representing a 'feature' at that level of the network. This allows for a compositional benefit because features can be combined in various ways, leading to exponential gains in the number of possibilities with increasing network depth, enhancing the representation power of the network.

- #neural-networks, #distributed-representation, #feature-learning
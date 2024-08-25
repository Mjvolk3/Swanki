### Anki Card 1

**Front:**

![](https://cdn.mathpix.com/cropped/2024_05_26_53b5c38c9dec90db1928g-1.jpg?height=396&width=486&top_left_y=674&top_left_x=634)

Based on the provided graph, describe the training process and components involved in training the neural network.

% 

**Back:**

The training process depicted in the graph involves a two-layer neural network with the following characteristics:

- $N = 50$ data points (blue dots) sampled uniformly over the interval $(-1, 1)$.
- The neural network consists of three hidden units with tanh activation functions.
- The output units are linear.
- The red curve indicates the network function after training.
- The dashed curves represent the outputs of the three hidden units.

The training aimed to approximate a specific target function \(f(x)\) using the sampled data points.

- #neural-networks, #machine-learning, #activation-functions

---

### Anki Card 2

**Front:**

![](https://cdn.mathpix.com/cropped/2024_05_26_53b5c38c9dec90db1928g-1.jpg?height=396&width=486&top_left_y=674&top_left_x=634)

Explain the significance of the universal approximation theorem in the context of neural networks.

%

**Back:**

The universal approximation theorem states that two-layer feed-forward networks can approximate any function defined over a continuous subset of $\mathbb{R}^{D}$ to arbitrary accuracy, given sufficient hidden units and appropriate activation functions. This theorem, established by Funahashi (1989), Cybenko (1989), and others, implies that:

- Neural networks are capable of representing any function if the network is large enough.
- Such networks are called universal approximators.
- This theoretical result is reassuring but does not specify how to construct the network or guarantee practical training success.

The theorem is foundational in neural network research, demonstrating their potential in function approximation tasks.

- #theorems, #universal-approximation, #neural-networks
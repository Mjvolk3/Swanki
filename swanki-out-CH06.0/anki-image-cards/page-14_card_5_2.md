    
### Card 1

**Front:**

What is the definition and key characteristic of the leaky ReLU activation function shown in the graph?

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=440&width=481&top_left_y=723&top_left_x=658)

%

**Back:**

The leaky ReLU (Rectified Linear Unit) activation function is defined as:

$$
h(a) = \max(0, a) + \alpha \min(0, a)
$$

where \( \alpha \) is a small positive parameter. The key characteristic of the leaky ReLU is that it allows for a non-zero gradient when the input \( a \) is negative, which helps to prevent the dying ReLU problem during training.

- #neural-networks, #activation-functions, #leaky-relu

### Card 2

**Front:**

Describe the behavior of the leaky ReLU function for positive and negative inputs as seen in the graph.

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=440&width=481&top_left_y=723&top_left_x=658)

%

**Back:**

For positive input values \( a \), the leaky ReLU function behaves as the identity function, i.e., \( h(a) = a \). For negative input values \( a \), the function has a smaller positive slope determined by \( \alpha \), i.e., \( h(a) = \alpha a \), instead of being zero as in the standard ReLU.

- #neural-networks, #activation-functions, #behavior


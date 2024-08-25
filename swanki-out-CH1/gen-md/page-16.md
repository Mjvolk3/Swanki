### Front: 

In the context of artificial neural networks, what key mechanism allows the brain to store information and learn from experience?

### Back:

The key mechanism that allows the brain to store information and learn from experience lies in the **changes in the strengths of synapses**. Synapses are the junctions where neurons connect, and the strength of these connections can be adjusted to either stimulate or inhibit the firing of subsequent neurons. The ability to strengthen or weaken these synapses over time is fundamental to learning and memory.

- #neural-networks, #biological-inspiration, #learning-mechanisms


### Front: 

Describe the basic properties of an artificial neuron model in the context of machine learning.

### Back:
An artificial neuron model in machine learning typically includes:

1. **Linear Combination**: The neuron computes a weighted sum of its input signals from other neurons, often written as:
    $$
    z = \sum_{i=1}^n w_i x_i + b
    $$
    where $w_i$ are the weights, $x_i$ are the input signals, and $b$ is the bias term.

2. **Nonlinear Transformation**: This sum is then passed through a nonlinear activation function $f()$, such that the output of the neuron is:
    $$
    a = f(z)
    $$
    
Common examples of activation functions include the sigmoid function, hyperbolic tangent, and ReLU (Rectified Linear Unit).

- #artificial-neural-networks, #neural-models, #activation-functions


### Front: 

How many neurons and synapses does the human brain approximately contain?

### Back:

The human brain contains approximately \textbf{90 billion neurons}, each of which has on average \textbf{several thousand synapses} with other neurons, resulting in a complex network of around \textbf{100 trillion (10^{14}) synapses}.

- #neuroscience, #brain-statistics, #neural-networks


### Front: 

What is the role of non-linear functions in artificial neural networks, and why are they important?

### Back:

Non-linear functions, also known as activation functions, play a crucial role in artificial neural networks by enabling them to model complex, non-linear relationships in data. Without non-linearity, the network would only be able to represent linear transformations, irrespective of the number of layers, essentially reducing its power to that of a single-layer network, equivalent to logistic regression.

Common activation functions include:
- **Sigmoid Function**: $ \sigma(z) = \frac{1}{1 + e^{-z}} $
- **Hyperbolic Tangent**: $ \tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}} $
- **ReLU (Rectified Linear Unit)**: $ \text{ReLU}(z) = \max(0, z) $

These functions introduce density and intricacies into the training dataset, allowing for more versatile and effective learning.

- #neural-networks, #non-linear-transformation, #activation-functions


### Front: 

Explain the role of synaptic strengths in the firing of neurons.

### Back:

The strength of a synapse influences the likelihood that the firing of an input neuron will cause the output neuron to fire. This can be either excitatory or inhibitory:

1. **Excitatory Synapses**: Increase the probability that the postsynaptic neuron will fire. If the input neuron fires, a stronger synaptic connection will more likely induce firing in the output neuron.
   
2. **Inhibitory Synapses**: Decrease the probability of firing. If the input neuron fires, a stronger inhibitory connection will make it less likely for the postsynaptic neuron to fire.

The modulation of synaptic strengths is how networks of neurons store information and learn from experiences.

- #neuroscience, #synapses, #learning-mechanisms
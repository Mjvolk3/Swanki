## Representation of a multi-class linear classification model

![](https://cdn.mathpix.com/cropped/2024_05_26_4ee214bfb89bd0af3d94g-1.jpg?height=344&width=654&top_left_y=209&top_left_x=992)
%
Describe the representation of a multi-class linear classification model as shown in the image.

%
The image depicts a multi-class linear classification model as a neural network with a single layer of connections. Each basis function is represented by a node, and the solid node represents the 'bias' basis function $\phi_{0}$. Each output $y_{1}, \ldots, y_{K}$ is also represented by a node. The links between the nodes represent the corresponding weight and bias parameters.

- #machine-learning, #neural-networks.single-layer, #multi-class-classification

## Cross-entropy error function

![](https://cdn.mathpix.com/cropped/2024_05_26_4ee214bfb89bd0af3d94g-1.jpg?height=344&width=654&top_left_y=209&top_left_x=992)
%
What is the cross-entropy error function in the context of multi-class classification?

%
The cross-entropy error function for multi-class classification is given by:

$$
E\left(\mathbf{w}_{1}, \ldots, \mathbf{w}_{K}\right)=-\ln p\left(\mathbf{T} \mid \mathbf{w}_{1}, \ldots, \mathbf{w}_{K}\right)=-\sum_{n=1}^{N} \sum_{k=1}^{K} t_{n k} \ln y_{n k}
$$

where $y_{n k}=y_{k}(\boldsymbol{\phi}_{n})$, and $\mathbf{T}$ is an $N \times K$ matrix of target variables with elements $t_{n k}$.

- #machine-learning, #loss-functions.cross-entropy, #multi-class-classification
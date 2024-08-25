  
## What does Figure 5.16 represent in the context of a multi-class linear classification model?

![](https://cdn.mathpix.com/cropped/2024_05_26_4ee214bfb89bd0af3d94g-1.jpg?height=344&width=654&top_left_y=209&top_left_x=992)

%

Figure 5.16 represents a multi-class linear classification model as a neural network with a single layer of connections. Each basis function is represented by a node, with the solid node representing the 'bias' basis function $\phi_{0}$. Each output $y_{1}, \ldots, y_{N}$ is also represented by a node, and the links between the nodes represent the corresponding weight and bias parameters.

- machine-learning.neural-networks, multi-class-classification

---

## What is the cross-entropy error function for a multi-class classification problem?

![](https://cdn.mathpix.com/cropped/2024_05_26_4ee214bfb89bd0af3d94g-1.jpg?height=344&width=654&top_left_y=209&top_left_x=992)

%

The cross-entropy error function for a multi-class classification problem is given by:

$$
E\left(\mathbf{w}_{1}, \ldots, \mathbf{w}_{K}\right)=-\ln p\left(\mathbf{T} \mid \mathbf{w}_{1}, \ldots, \mathbf{w}_{K}\right)=-\sum_{n=1}^{N} \sum_{k=1}^{K} t_{n k} \ln y_{n k}
$$

where $y_{n k}$ represents the model output for input $n$ and class $k$, and $t_{n k}$ is the corresponding target variable.

- machine-learning.neural-networks, cross-entropy-error, multi-class-classification
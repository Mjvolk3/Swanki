## Card 1

![](https://cdn.mathpix.com/cropped/2024_05_26_0b66c2c41c506aebc39ag-1.jpg?height=338&width=649&top_left_y=212&top_left_x=992)

Explain the representation of a linear regression model as a neural network as shown in this image, particularly focusing on its structure and components.

%

The image depicts a linear regression model represented as a neural network with a single layer of connections. It comprises:

1. **Nodes:** Each node represents a basis function $\phi_i(x)$, where $\phi_0(x)$ is a solid node indicating the bias function.
2. **Connections:** Links between nodes symbolizing the weights $w_{ij}$ and biases for the model.
3. **Output Nodes:** Labeled $y_1(x, w), \ldots, y_K(x, w)$, representing the multiple predicted target variables.

The top layer nodes $y_1$ through $y_K$ correspond to outputs determined by the weighted sum of the basis functions $\phi_1(x)$ to $\phi_{M-1}(x)$. This network structure extends the linear regression model to scenarios with multiple output predictions.

- #machine-learning, #regression.linear, #neural-networks.single-layer

## Card 2

![](https://cdn.mathpix.com/cropped/2024_05_26_0b66c2c41c506aebc39ag-1.jpg?height=338&width=649&top_left_y=212&top_left_x=992)

Describe how the concept of basis functions and target vectors can be extended to predict multiple outputs in a linear regression model, referencing the image.

%

To predict multiple outputs $K>1$ in a linear regression model, as depicted in the image:

1. **Basis Functions:** Multiple sets of basis functions $\phi_i(x)$ are introduced for each component of the target vector $\mathbf{t}$.
2. **Target Vector:** Denoted as $\mathbf{t}=\left(t_1, \ldots, t_K\right)^{\mathrm{T}}$, containing multiple target variables.
3. **Independent Regression Problems:** Each target variable $t_k$ can be treated as a separate, independent regression problem, leveraging distinct basis functions for each.

This approach transforms the linear regression model into a structure that can handle vector targets, predicting multiple outputs via the weighted sums of the corresponding basis functions.

- #machine-learning, #regression.multiple-outputs, #neural-networks.regression
### Card 1

**Q:**

Describe the structure and the role of the bias node in the linear regression model representation as depicted in the diagram.

![](https://cdn.mathpix.com/cropped/2024_05_26_0b66c2c41c506aebc39ag-1.jpg?height=338&width=649&top_left_y=212&top_left_x=992)

%

**A:**

In the linear regression model representation, the bias node is denoted as $\phi_0(x)$ and is depicted by a solid node at the bottom of the diagram. This node is crucial as it corresponds to the bias term in a linear model, which does not depend on the input features and typically outputs a constant value of 1.

- #machine-learning, #neural-networks.linear-regression, #model-components.bias

### Card 2

**Q:**

Explain how multiple target variables are handled in a linear regression model represented as a neural network.

![](https://cdn.mathpix.com/cropped/2024_05_26_0b66c2c41c506aebc39ag-1.jpg?height=338&width=649&top_left_y=212&top_left_x=992)

%

**A:**

In the linear regression model represented as a neural network, multiple target variables are handled by having separate output nodes for each target variable. These nodes are labeled $y_1(x, w)$ to $y_K(x, w)$. Each output node corresponds to a different predicted output, determined by a distinct weighted sum of the transformed input features through the basis functions. This approach allows the model to predict multiple outputs ($K > 1$), effectively solving multiple independent regression problems simultaneously.

- #machine-learning, #neural-networks.multiple-outputs, #regression.tasks
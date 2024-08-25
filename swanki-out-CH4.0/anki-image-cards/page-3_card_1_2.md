### Anki Card 1

![](https://cdn.mathpix.com/cropped/2024_05_26_28116a89444d4b7f5a3bg-1.jpg?height=332&width=528&top_left_y=215&top_left_x=1111)

Describe the components of the linear regression model as represented by the neural network diagram.

%

The neural network diagram illustrates the linear regression model with the following components:

- **Input Nodes:** These represent the basis functions $\phi_{j}(\mathbf{x})$ where $j$ ranges from $0$ to $M-1$. Each node corresponds to one basis function.
- **Solid Node (Bias):** The solid node at the bottom left represents the bias basis function $\phi_{0}$, usually set to a constant value of 1.
- **Output Node:** The output node represents the function $y(\mathbf{x}, \mathbf{w})$.
- **Lines Connecting Nodes:** Each line connecting a basis function to the output node represents a parameter $w_{j}$, where $w_{j}$ is a weight applied to the basis function $\phi_{j}(\mathbf{x})$.

The neural network diagram serves to show how a linear combination of weighted basis functions can be used to predict a continuous target variable $y(\mathbf{x}, \mathbf{w})$. 

Tags: #machine-learning, #neural-networks, #linear-regression

---

### Anki Card 2

![](https://cdn.mathpix.com/cropped/2024_05_26_28116a89444d4b7f5a3bg-1.jpg?height=332&width=528&top_left_y=215&top_left_x=1111)

What equation does the neural network diagram represent, and what do the variables signify?

%

The neural network diagram represents the linear regression model given by the equation:

$$
y(\mathbf{x}, \mathbf{w}) = \sum_{j=0}^{M-1} w_{j} \phi_{j}(\mathbf{x})
$$

- $y(\mathbf{x}, \mathbf{w})$: The output function, which is the predicted continuous target variable.
- $w_{j}$: The parameters or weights applied to each basis function.
- $\phi_{j}(\mathbf{x})$: The basis functions derived from the input variables $\mathbf{x}$. The index $j$ ranges from $0$ to $M-1$, with $\phi_{0}$ often representing a bias term set to 1.

The diagram visually represents how the model combines these weighted basis functions to make predictions.

Tags: #machine-learning, #equations, #basis-functions
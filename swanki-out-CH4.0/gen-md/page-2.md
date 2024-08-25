### Mathematics Anki Cards

---

## Describe the basic form of the linear regression model.

The basic form of the linear regression model is defined by:

$$
y(\mathbf{x}, \mathbf{w}) = w_{0} + w_{1} x_{1} + \ldots + w_{D} x_{D}
$$

Here, $\mathbf{x}$ is a $D$-dimensional vector of input variables and $\mathbf{w}$ is a vector of parameters. Explain the significance of the linearity with respect to $\mathbf{w}$.

- #statistics.linear-regression #machine-learning.models

---

## Describe the extended linear regression model using basis functions.

The class of models can be extended by considering linear combinations of fixed nonlinear functions of the input variables:

$$
y(\mathbf{x}, \mathbf{w})=w_{0}+\sum_{j=1}^{M-1} w_{j} \phi_{j}(\mathbf{x})
$$

Here, $\phi_{j}(\mathbf{x})$ are known as basis functions. Elaborate on the effect of using nonlinear basis functions and how they differ from the initial linear terms.

- #statistics.basis-functions #machine-learning.models

---

## What is the role of the parameter $\phi_0(\mathbf{x})$?

The parameter $\phi_0(\mathbf{x})$ is defined as a dummy basis function, fixed at $\phi_0(\mathbf{x}) = 1$. It allows the equation:

$$
y(\mathbf{x}, \mathbf{w}) = \sum_{j=0}^{M-1} w_{j} \phi_{j}(\mathbf{x}) = \mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}(\mathbf{x})
$$

to include a constant term $w_0$ which acts as an offset to the data. Detail why this is important for modeling.

- #statistical-parameters.bias #machine-learning.models

---

## How does using basis functions affect the linearity of the model with respect to $\mathbf{w}$?

Despite introducing nonlinear basis functions $\phi_j(\mathbf{x})$, the model:

$$
y(\mathbf{x}, \mathbf{w})=\sum_{j=0}^{M-1} w_{j} \phi_{j}(\mathbf{x})
$$

remains linear in the parameters $\mathbf{w}$. Discuss why this characteristic is beneficial for analysis.

- #statistics.linearity #machine-learning.models

---

## How many parameters are in the extended linear regression model with basis functions?

By denoting the maximum value of the index $j$ as $M-1$, the total number of parameters in the extended model, including $w_0$, is given by $M$. Explain the significance of the number of parameters in model complexity.

- #statistics.parameter-count #machine-learning.models

---

## Explain the key limitations imposed by the linear form of the input variables $x_i$.

In a simple linear regression model:

$$
y(\mathbf{x}, \mathbf{w}) = w_{0} + w_{1} x_{1} + \ldots + w_{D} x_{D}
$$

the function is linear with respect to both the parameters $\mathbf{w}$ and the input variables $\mathbf{x}$. Discuss the limitations that this linearity on $\mathbf{x}$ imposes on the model's representation of real-world data.

- #statistics.linear-limitations #machine-learning.complexity

---


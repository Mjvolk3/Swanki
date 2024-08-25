```markdown
## Explain how the partial derivative of an activation $a_j$ with respect to weight $w_{ji}$ is expressed.

The partial derivative of an activation $a_j$ with respect to weight $w_{ji}$ is given by:

$$
\frac{\partial a_{j}}{\partial w_{j i}}=z_{i}
$$

Here, $z_i$ is the input to the weight $w_{ji}$.

- #backpropagation, #derivatives
```

```markdown
## How do we obtain the partial derivative of the error function with respect to the weight, $\partial E_n / \partial w_{ji}$?

Substituting $\partial a_{j} / \partial w_{ji} = z_i$ into the expression for $\partial E_n / \partial a_j$ and rearranging gives:

$$
\frac{\partial E_{n}}{\partial w_{j i}}=\delta_{j} z_{i}
$$

Here, $\delta_j$ is the error term for unit $j$ and $z_i$ is the input to weight $w_{ji}$.

- #backpropagation, #error-derivatives
```

```markdown
## Describe what the term $\delta_k = y_k - t_k$ represents in the context of backpropagation.

For output units, the error term $\delta_k$ is defined as:

$$
\delta_{k}=y_{k}-t_{k}
$$

where $y_k$ is the output of the unit and $t_k$ is the target value.

- #backpropagation, #output-units
```

```markdown
## How is the error term $\delta_j$ for hidden units calculated using the chain rule?

The error term $\delta_j$ for hidden units is calculated using the chain rule for partial derivatives:

$$
\delta_{j} \equiv \frac{\partial E_{n}}{\partial a_{j}}=\sum_{k} \frac{\partial E_{n}}{\partial a_{k}} \frac{\partial a_{k}}{\partial a_{j}}
$$

where the sum runs over all units $k$ to which unit $j$ sends connections.

- #backpropagation, #hidden-units
```

```markdown
## What is the backpropagation formula for the error term $\delta_j$ of a hidden unit?

Using the chain rule and definitions of $\delta$, we obtain the backpropagation formula for a hidden unit $j$:

$$
\delta_{j}=h^{\prime}\left(a_{j}\right) \sum_{k} w_{k j} \delta_{k}
$$

Here, $\delta_k$ are the error terms for units to which hidden unit $j$ connects, and $h'$ is the derivative of the activation function.

- #backpropagation, #hidden-units
```

```markdown
## In backpropagation, what does Equation (8.10) imply about calculating derivatives for weights?

Equation (8.10),

$$
\frac{\partial E_{n}}{\partial w_{j i}}=\delta_{j} z_{i}
$$

implies that the required derivative can be obtained by multiplying the error term $\delta_j$ by the input $z_i$. This simplifies the calculation and indicates that it follows the same form as a simple linear model.

- #backpropagation, #derivatives
```

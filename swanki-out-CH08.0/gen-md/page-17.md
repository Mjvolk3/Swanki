### Compute Column $j$ of the Jacobian

To compute column $j$ of the Jacobian $\mathbf{J}$, we need to set specific initial conditions. Describe these conditions.

The initial conditions are set as $\dot{x}_{j}=1$ and $\dot{x}_{i}=0$ for $i \neq j$. This can be represented in vector form as $\dot{\mathbf{x}}=\mathbf{e}_{i}$, where $\mathbf{e}_{i}$ is the $i$-th unit vector.

- #math.analysis, #differentiation.jacobian

### Full Jacobian Matrix Computation

How many forward-mode passes are required to compute the full Jacobian matrix?

To compute the full Jacobian matrix, we need $D$ forward-mode passes, where $D$ is the dimension of the input vector.

- #math.analysis, #differentiation.jacobian

### Jacobian-Vector Product

How can the product of the Jacobian $\mathbf{J}$ with a vector $\mathbf{r}$ be efficiently computed?

The product of the Jacobian with a vector $\mathbf{r}=\left(r_{1}, \ldots, r_{D}\right)^{\mathrm{T}}$ can be computed in a single forward pass by setting $\dot{\mathbf{x}}=\mathbf{r}$.

$$
\mathbf{J} \mathbf{r} = \left[\begin{array}{ccc}
\frac{\partial f_{1}}{\partial x_{1}} & \cdots & \frac{\partial f_{1}}{\partial x_{D}} \\
\vdots & \ddots & \vdots \\
\frac{\partial f_{K}}{\partial x_{1}} & \cdots & \frac{\partial f_{K}}{\partial x_{D}}
\end{array}\right]\left[\begin{array}{c}
r_{1} \\
\vdots \\
r_{D}
\end{array}\right]
$$

- #math.analysis, #differentiation.jacobian, #optimization

### Efficiency of Forward-Mode Automatic Differentiation

In what kind of networks is forward-mode automatic differentiation most efficient?

Forward-mode automatic differentiation is most efficient for networks with a few inputs and many outputs, such that $K \gg D$.

- #algorithms, #differentiation.forward-mode

### Reverse-Mode Automatic Differentiation

Define the adjoint variables $\bar{v}_{i}$ used in reverse-mode automatic differentiation.
The adjoint variables $\bar{v}_{i}$ are defined as:

$$
\bar{v}_{i} = \frac{\partial f}{\partial v_{i}}
$$

These variables can be evaluated sequentially using the chain rule.

- #algorithms, #differentiation.reverse-mode

### Sequential Evaluation of Adjoint Variables

How are the adjoint variables $\bar{v}_{i}$ evaluated in reverse-mode automatic differentiation?

The adjoint variables are evaluated sequentially starting with the output and working backwards using the chain rule of calculus:

$$
\bar{v}_{i} = \frac{\partial f}{\partial v_{i}} = \sum_{j \in \operatorname{ch}(i)} \frac{\partial f}{\partial v_{j}} \frac{\partial v_{j}}{\partial v_{i}} = \sum_{j \in \operatorname{ch}(i)} \bar{v}_{j} \frac{\partial v_{j}}{\partial v_{i}}
$$

Here, $\operatorname{ch}(i)$ denotes the children of node $i$ in the evaluation trace graph.

- #algorithms, #differentiation.chain-rule
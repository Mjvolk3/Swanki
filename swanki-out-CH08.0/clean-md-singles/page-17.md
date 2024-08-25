To compute column $j$ of the Jacobian, we need to initialize the forward pass of the tangent equations by setting $\dot{x}_{j}=1$ and $\dot{x}_{i}=0$ for $i \neq j$. We can write this in vector form as $\dot{\mathbf{x}}=\mathbf{e}_{i}$ where $\mathbf{e}_{i}$ is the $i$ th unit vector. To compute the full Jacobian matrix we need $D$ forward-mode passes. However, if we wish to evaluate the product of the Jacobian with a vector $\mathbf{r}=\left(r_{1}, \ldots, r_{D}\right)^{\mathrm{T}}$ :

$$
\mathbf{J}=\left[\begin{array}{ccc}
\frac{\partial f_{1}}{\partial x_{1}} & \cdots & \frac{\partial f_{1}}{\partial x_{D}} \\
\vdots & \ddots & \vdots \\
\frac{\partial f_{K}}{\partial x_{1}} & \cdots & \frac{\partial f_{K}}{\partial x_{D}}
\end{array}\right]\left[\begin{array}{c}
r_{1} \\
\vdots \\
r_{D}
\end{array}\right]
$$

Exercise 8.18 then this can be done in single forward pass by setting $\dot{\mathbf{x}}=\mathbf{r}$.

We see that forward-mode automatic differentiation can evaluate the full $K \times D$ Jacobian matrix of derivatives using $D$ forward passes. This is very efficient for networks with a few inputs and many outputs, such that $K \gg D$. However, we often operate in a regime where we often have just one function, namely the error function used for training, and large numbers of variables that we want to differentiate with respect to, comprising the weights and biases in the network, of which there may be millions or billions. In such situations, forward-mode automatic differentiation is extremely inefficient. We therefore turn to an alternative version of automatic differentiation based on the a backwards flow of derivative data through the evaluation trace graph.

\title{
8.2.2 Reverse-mode automatic differentiation
}

We can think of reverse-mode automatic differentiation as a generalization of the error backpropagation procedure. As with forward mode, we augment each intermediate variable $v_{i}$ with additional variables, in this case called adjoint variables, denoted $\bar{v}_{i}$. Consider again a situation with a single output function $f$ for which the adjoint variables are defined by

$$
\bar{v}_{i}=\frac{\partial f}{\partial v_{i}}
$$

These can be evaluated sequentially starting with the output and working backwards by using the chain rule of calculus:

$$
\bar{v}_{i}=\frac{\partial f}{\partial v_{i}}=\sum_{j \in \operatorname{ch}(i)} \frac{\partial f}{\partial v_{j}} \frac{\partial v_{j}}{\partial v_{i}}=\sum_{j \in \operatorname{ch}(i)} \bar{v}_{j} \frac{\partial v_{j}}{\partial v_{i}}
$$

Here $\operatorname{ch}(i)$ denotes the children of node $i$ in the evaluation trace graph, in other words the set of nodes that have arrows pointing into them from node $i$. The successive evaluation of the adjoint variables represents a flow of information backwards

Figure 8.1

Exercise 8.16 through the graph, as we saw previously.

If we again consider the specific example function given by (8.50) to (8.56), we obtain the following evaluation equations for the evaluation of the adjoint variables
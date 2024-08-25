## Jacobian Matrix for Small Perturbations

Explain the significance of the Jacobian matrix evaluating small perturbations in a neural network and write the related equation.
%
The Jacobian matrix helps determine how small changes in the input $\Delta x_i$ affect changes in the output $\Delta y_k$. This effect can be captured by the equation:

$$
\Delta y_{k} \simeq \sum_{i} \frac{\partial y_{k}}{\partial x_{i}} \Delta x_{i}
$$

Here, $\frac{\partial y_{k}}{\partial x_{i}}$ represents the partial derivative of the output $y_k$ with respect to the input $x_i$, indicating how sensitive $y_k$ is to changes in $x_i$. This relation is valid only when the changes $\left|\Delta x_{i}\right|$ are small, ensuring that the system behaves approximately linearly around the operating point.

- #neural-networks.jacobian, #error-propagation, #partial-derivatives

## Influence of Nonlinearity on Jacobian Matrix Elements

How does nonlinearity in the network mapping influence the Jacobian matrix?

%
In a trained neural network, the mapping from inputs to outputs is generally nonlinear. This nonlinearity makes the elements of the Jacobian matrix dependent on the particular input vector used, meaning they are not constants but vary with the input. Thus, the Jacobian matrix needs to be re-evaluated for each new input vector, and the relation $\Delta y_{k} = \sum_{i} \frac{\partial y_{k}}{\partial x_{i}} \Delta x_{i}$ is only valid for small perturbations of the inputs.

- #neural-networks, #nonlinearity, #jacobian-matrix

## Element of the Jacobian Matrix

Write down the expression for an element $J_{ki}$ of the Jacobian matrix using partial derivatives and weights.

%
An element $J_{k i}$ of the Jacobian matrix can be expressed as:

$$
J_{k i}=\frac{\partial y_{k}}{\partial x_{i}} = \sum_{j} w_{j i} \frac{\partial y_{k}}{\partial a_{j}}
$$

This expression is derived by factoring the change in $y_k$ with respect to $x_i$ through an intermediate layer $a_j$, where $w_{ji}$ represents the weight of connection from input $i$ to unit $j$.

- #neural-networks, #jacobian, #partial-derivatives

## Recursive Formula for Derivatives

Provide and explain the recursive backpropagation formula for the derivatives $\partial y_{k} / \partial a_{j}$ in a neural network.

%
The recursive backpropagation formula for the derivatives $\partial y_{k} / \partial a_{j}$ in a neural network is given by:

$$
\begin{aligned}
\frac{\partial y_{k}}{\partial a_{j}} & = \sum_{l} \frac{\partial y_{k}}{\partial a_{l}} \frac{\partial a_{l}}{\partial a_{j}} \\
& = h^{\prime}\left(a_{j}\right) \sum_{l} w_{l j} \frac{\partial y_{k}}{\partial a_{l}}
\end{aligned}
$$

Here, $h^{\prime}\left(a_{j}\right)$ denotes the derivative of the activation function with respect to $a_j$, and $w_{lj}$ represents the weight between units $j$ and $l$. This formula helps in propagating the derivatives backward through the network.

- #backpropagation, #recursive-formula, #neural-networks

## Initial Derivatives for Output Units

What is the initial value of the derivative $\partial y_{k} / \partial a_{l}$ for linear output units? 

Define the related variable $\delta_{kl}$.

%
For linear output units, the initial value of the derivative $\partial y_{k} / \partial a_{l}$ is given by:

$$
\frac{\partial y_{k}}{\partial a_{l}} = \delta_{k l}
$$

Here, $\delta_{k l}$ is the Kronecker delta, which equals 1 if $k = l$ and 0 otherwise. This indicates that the derivative of the output $y_k$ with respect to its corresponding activation $a_l$ is 1, and zero for all other activations.

- #neural-networks, #linear-output-units, #kronecker-delta

## Propagation Through Trained Network

Describe how errors are propagated through a network using the Jacobian matrix.

%
The errors at the outputs can be traced back to the inputs using the Jacobian matrix through the relation:

$$
\Delta y_{k} \simeq \sum_{i} \frac{\partial y_{k}}{\partial x_{i}} \Delta x_{i}
$$

In this equation, $\frac{\partial y_{k}}{\partial x_{i}}$ represents the elements of the Jacobian matrix, which captures how a small change in input $\Delta x_i$ affects the output $\Delta y_k$. By backpropagating this way, one can estimate contributions of input perturbations to output errors.

- #error-propagation, #jacobian-matrix, #neural-networks
## Define the Kronecker delta $\delta_{kl}$.

The Kronecker delta $\delta_{kl}$ are the elements of the identity matrix and are defined by

$$
\delta_{kl} = \begin{cases} 
1, & \text{if } k = l \\ 
0, & \text{otherwise} 
\end{cases}.
$$

- #linear-algebra.identity-matrix #notation.kronecker-delta


## What is the partial derivative of $y_k$ with respect to $a_l$ for an individual logistic sigmoid activation function?

For individual logistic sigmoid activation functions at each output unit, the partial derivative of $y_k$ with respect to $a_l$ is

$$
\frac{\partial y_k}{\partial a_l} = \delta_{kl}\sigma'\left(a_l\right),
$$

where $\delta_{kl}$ is the Kronecker delta and $\sigma'$ is the derivative of the sigmoid function.

- #neural-networks.activation-functions #calculus.partial-derivatives


## What is the partial derivative of $y_k$ with respect to $a_l$ for softmax outputs?

For softmax outputs, the partial derivative of $y_k$ with respect to $a_l$ is given by

$$
\frac{\partial y_k}{\partial a_l} = \delta_{kl} y_k - y_k y_l,
$$

where $\delta_{kl}$ is the Kronecker delta and $y_k$, $y_l$ are the output values.

- #neural-networks.activation-functions #calculus.partial-derivatives


## How can the Jacobian matrix be calculated numerically?

The Jacobian matrix can be calculated numerically using numerical differentiation as follows:

$$
\frac{\partial y_{k}}{\partial x_{i}} = \frac{y_{k}\left(x_i + \epsilon\right) - y_{k}\left(x_i - \epsilon\right)}{2\epsilon} + \mathcal{O}\left(\epsilon^{2}\right),
$$

where $\epsilon$ is a small perturbation value. This method involves $2D$ forward propagation passes for a network having $D$ inputs and requires $\mathcal{O}(DW)$ steps in total.

- #neural-networks.jacobian #calculus.numerical-differentiation


## How are the second derivatives of the error function with respect to the weights obtained?

The second derivatives of the error function with respect to the weights in a network can be obtained via backpropagation using

$$
\frac{\partial^2 E}{\partial w_{ji} \partial w_{lk}}.
$$

Backpropagation can be extended to evaluate second derivatives as it is used for first derivatives.

- #neural-networks.derivatives #algorithms.backpropagation


## What is the Hessian matrix in the context of neural networks?

In the context of neural networks, the Hessian matrix $\mathbf{H}$ is defined as the matrix of second derivatives of the error function $E$ with respect to the weights. Its elements are given by

$$
H_{ij} = \frac{\partial^2 E}{\partial w_i \partial w_j},
$$

where $w_i$ and $w_j$ are the weight parameters treated as elements of a single vector $\mathbf{w}$.

- #neural-networks.hessian #calculus.second-derivatives
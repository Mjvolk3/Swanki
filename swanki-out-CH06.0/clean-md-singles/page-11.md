Figure 6.9 Network diagram for a two-layer neural network. The input, hidden, and output variables are represented by nodes, and the weight parameters are represented by links between the nodes. The bias parameters are denoted by links coming from additional input and hidden variables $x_{0}$ and $z_{0}$ which are themselves denoted by solid nodes. Arrows denote the direction of information flow through the network during forward propagation.
Hidden units

![](https://cdn.mathpix.com/cropped/2024_05_26_a31248c38a71950d5cfdg-1.jpg?height=532&width=709&top_left_y=274&top_left_x=935)

function $f(\cdot)$ to give a set of network outputs $y_{k}$. A two-layer neural network can be represented in diagram form as shown in Figure 6.9.

\title{
6.2.1 Parameter matrices
}

Section 4.1.1

As we discussed in the context of linear regression models, the bias parameters in (6.7) can be absorbed into the set of weight parameters by defining an additional input variable $x_{0}$ whose value is clamped at $x_{0}=1$, so that (6.7) takes the form

$$
a_{j}=\sum_{i=0}^{D} w_{j i}^{(1)} x_{i}
$$

We can similarly absorb the second-layer biases into the second-layer weights, so that the overall network function becomes

$$
y_{k}(\mathbf{x}, \mathbf{w})=f\left(\sum_{j=0}^{M} w_{k j}^{(2)} h\left(\sum_{i=0}^{D} w_{j i}^{(1)} x_{i}\right)\right)
$$

Another notation that will prove convenient at various points in the book is to represent the inputs as a column vector $\mathbf{x}=\left(x_{1}, \ldots, x_{N}\right)^{\mathrm{T}}$ and then to gather the weight and bias parameters in (6.11) into matrices to give

$$
\mathbf{y}(\mathbf{x}, \mathbf{w})=f\left(\mathbf{W}^{(2)} h\left(\mathbf{W}^{(1)} \mathbf{x}\right)\right)
$$

where $f(\cdot)$ and $h(\cdot)$ are evaluated on each vector element separately.

\subsection*{6.2.2 Universal approximation}

The capability of a two-layer network to model a broad range of functions is illustrated in Figure 6.10. This figure also shows how individual hidden units work collaboratively to approximate the final function. The role of hidden units in a simple classification problem is illustrated in Figure 6.11.
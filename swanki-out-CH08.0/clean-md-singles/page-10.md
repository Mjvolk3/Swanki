Section 3.4

Section 3.4

\section*{Exercise 8.5}

where $\delta_{k l}$ are the elements of the identity matrix and are defined by

$$
\delta_{k l}= \begin{cases}1, & \text { if } k=l \\ 0, & \text { otherwise }\end{cases}
$$

If we have individual logistic sigmoid activation functions at each output unit, then

$$
\frac{\partial y_{k}}{\partial a_{l}}=\delta_{k l} \sigma^{\prime}\left(a_{l}\right)
$$

whereas for softmax outputs, we have

$$
\frac{\partial y_{k}}{\partial a_{l}}=\delta_{k l} y_{k}-y_{k} y_{l}
$$

We can summarize the procedure for calculating the Jacobian matrix as follows. Apply the input vector corresponding to the point in input space at which the Jacobian matrix is to be evaluated, and forward propagate in the usual way to obtain the states of all the hidden and output units in the network. Next, for each row $k$ of the Jacobian matrix, corresponding to the output unit $k$, backpropagate using the recursive relation (8.30), starting with (8.31), (8.33) or (8.34), for all the hidden units in the network. Finally, use (8.29) for the backpropagation to the inputs. The Jacobian can also be evaluated using an alternative forward propagation formalism, which can be derived in an analogous way to the backpropagation approach given here.

Again, the implementation of such algorithms can be checked using numerical differentiation in the form

$$
\frac{\partial y_{k}}{\partial x_{i}}=\frac{y_{k}\left(x_{i}+\epsilon\right)-y_{k}\left(x_{i}-\epsilon\right)}{2 \epsilon}+\mathcal{O}\left(\epsilon^{2}\right)
$$

which involves $2 D$ forward propagation passes for a network having $D$ inputs and therefore requires $\mathcal{O}(D W)$ steps in total.

\title{
8.1.6 The Hessian matrix
}

We have shown how backpropagation can be used to obtain the first derivatives of an error function with respect to the weights in the network. Backpropagation can also be used to evaluate the second derivatives of the error, which are given by

$$
\frac{\partial^{2} E}{\partial w_{j i} \partial w_{l k}}
$$

It is often convenient to consider all the weight and bias parameters as elements $w_{i}$ of a single vector, denoted $\mathbf{w}$, in which case the second derivatives form the elements $H_{i j}$ of the Hessian matrix $\mathbf{H}$ :

$$
H_{i j}=\frac{\partial^{2} E}{\partial w_{i} \partial w_{j}}
$$
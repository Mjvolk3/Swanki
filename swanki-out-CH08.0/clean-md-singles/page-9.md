Figure 8.3 Illustration of a modular deep learning architecture in which the Jacobian matrix can be used to backpropagate error signals from the outputs through to earlier modules in the system.

![](https://cdn.mathpix.com/cropped/2024_05_26_b806d19b62f773366399g-1.jpg?height=323&width=923&top_left_y=212&top_left_x=718)

associated with the inputs to be propagated through the trained network to estimate their contribution $\Delta y_{k}$ to the errors at the outputs, through the relation

$$
\Delta y_{k} \simeq \sum_{i} \frac{\partial y_{k}}{\partial x_{i}} \Delta x_{i}
$$

which assumes that the $\left|\Delta x_{i}\right|$ are small. In general, the network mapping represented by a trained neural network will be nonlinear, and so the elements of the Jacobian matrix will not be constants but will depend on the particular input vector used. Thus, (8.28) is valid only for small perturbations of the inputs, and the Jacobian itself must be re-evaluated for each new input vector.

The Jacobian matrix can be evaluated using a backpropagation procedure that is like the one derived earlier for evaluating the derivatives of an error function with respect to the weights. We start by writing the element $J_{k i}$ in the form

$$
\begin{aligned}
J_{k i}=\frac{\partial y_{k}}{\partial x_{i}} & =\sum_{j} \frac{\partial y_{k}}{\partial a_{j}} \frac{\partial a_{j}}{\partial x_{i}} \\
& =\sum_{j} w_{j i} \frac{\partial y_{k}}{\partial a_{j}}
\end{aligned}
$$

where we have made use of (8.5). The sum in (8.29) runs over all units $j$ to which the input unit $i$ sends connections (for example, over all units in the first hidden layer in the layered topology considered earlier). We now write down a recursive backpropagation formula for the derivatives $\partial y_{k} / \partial a_{j}$ :

$$
\begin{aligned}
\frac{\partial y_{k}}{\partial a_{j}} & =\sum_{l} \frac{\partial y_{k}}{\partial a_{l}} \frac{\partial a_{l}}{\partial a_{j}} \\
& =h^{\prime}\left(a_{j}\right) \sum_{l} w_{l j} \frac{\partial y_{k}}{\partial a_{l}}
\end{aligned}
$$

where the sum runs over all units $l$ to which unit $j$ sends connections (corresponding to the first index of $w_{l j}$ ). Again, we have made use of (8.5) and (8.6). This backpropagation starts at the output units, for which the required derivatives can be found directly from the functional form of the output-unit activation function. For linear output units, we have

$$
\frac{\partial y_{k}}{\partial a_{l}}=\delta_{k l}
$$
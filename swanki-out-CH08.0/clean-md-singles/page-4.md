\title{
8. BACKPROPAGATION
}

Figure 8.1 Illustration of the calculation of $\delta_{j}$ for hidden unit $j$ by backpropagation of the $\delta$ 's from those units $k$ to which unit $j$ sends connections. The black arrows denote the direction of information flow during forward propagation, and the red arrows indicate the backward propagation of error information.

![](https://cdn.mathpix.com/cropped/2024_05_26_5df28c9d7a64baac9eefg-1.jpg?height=308&width=491&top_left_y=215&top_left_x=1149)

where the $\delta$ 's are often referred to as errors for reasons we will see shortly. Using (8.5), we can write

$$
\frac{\partial a_{j}}{\partial w_{j i}}=z_{i}
$$

Substituting (8.8) and (8.9) into (8.7), we then obtain

$$
\frac{\partial E_{n}}{\partial w_{j i}}=\delta_{j} z_{i}
$$

Equation (8.10) tells us that the required derivative is obtained simply by multiplying the value of $\delta$ for the unit at the output end of the weight by the value of $z$ for the unit at the input end of the weight (where $z=1$ for a bias). Note that this takes the same form as that found for the simple linear model in (8.4). Thus, to evaluate the derivatives, we need calculate only the value of $\delta_{j}$ for each hidden and output unit in the network and then apply (8.10).

As we have seen already, for the output units, we have

$$
\delta_{k}=y_{k}-t_{k}
$$

Section 5.4.6

provided we are using the canonical link as the output-unit activation function. To evaluate the $\delta$ 's for hidden units, we again make use of the chain rule for partial derivatives:

$$
\delta_{j} \equiv \frac{\partial E_{n}}{\partial a_{j}}=\sum_{k} \frac{\partial E_{n}}{\partial a_{k}} \frac{\partial a_{k}}{\partial a_{j}}
$$

where the sum runs over all units $k$ to which unit $j$ sends connections. The arrangement of units and weights is illustrated in Figure 8.1. Note that the units labelled $k$ include other hidden units and/or output units. In writing down (8.12), we are making use of the fact that variations in $a_{j}$ give rise to variations in the error function only through variations in the variables $a_{k}$.

If we now substitute the definition of $\delta_{j}$ given by (8.8) into (8.12) and make use

Exercise 8.1 of (8.5) and (8.6), we obtain the following backpropagation formula:

$$
\delta_{j}=h^{\prime}\left(a_{j}\right) \sum_{k} w_{k j} \delta_{k}
$$

which tells us that the value of $\delta$ for a particular hidden unit can be obtained by propagating the $\delta$ 's backwards from units higher up in the network, as illustrated
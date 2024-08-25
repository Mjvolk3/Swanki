\title{
Algorithm 8.1: Backpropagation
}

Input: Input vector $\mathbf{x}_{n}$

Network parameters $\mathbf{w}$

Error function $E_{n}(\mathbf{w})$ for input $x_{n}$

Activation function $h(a)$

Output: Error function derivatives $\left\{\partial E_{n} / \partial w_{j i}\right\}$

// Forward propagation

for $j \in$ all hidden and output units do

$$
\begin{aligned}
& a_{j} \leftarrow \sum_{i} w_{j i} z_{i} / /\left\{z_{i}\right\} \text { includes inputs }\left\{x_{i}\right\} \\
& z_{j} \leftarrow h\left(a_{j}\right) / / \text { activation function }
\end{aligned}
$$

end for

// Error evaluation

for $k \in$ all output units do

$$
\delta_{k} \leftarrow \frac{\partial E_{n}}{\partial a_{k}} / / \text { compute errors }
$$

end for

// Backward propagation, in reverse order

for $j \in$ all hidden units do

$\delta_{j} \leftarrow h^{\prime}\left(a_{j}\right) \sum_{k} w_{k j} \delta_{k} / /$ recursive backward evaluation $\frac{\partial E_{n}}{\partial w_{j i}} \leftarrow \delta_{j} z_{i} / /$ evaluate derivatives

end for

return $\left\{\frac{\partial E_{n}}{\partial w_{j i}}\right\}$

in Figure 8.1. Note that the summation in (8.13) is taken over the first index on $w_{k j}$ (corresponding to backward propagation of information through the network), whereas in the forward propagation equation (8.5), it is taken over the second index. Because we already know the values of the $\delta$ 's for the output units, it follows that by recursively applying (8.13), we can evaluate the $\delta$ 's for all the hidden units in a feed-forward network, regardless of its topology. The backpropagation procedure is summarized in Algorithm 8.1.

For batch methods, the derivative of the total error $E$ can then be obtained by repeating the above steps for each data point in the training set and then summing over all data points in the batch or mini-batch:

$$
\frac{\partial E}{\partial w_{j i}}=\sum_{n} \frac{\partial E_{n}}{\partial w_{j i}}
$$
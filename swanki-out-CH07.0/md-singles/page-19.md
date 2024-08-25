Section 8.1.5

Section 8.1.5

\subsection*{7.4.2 Batch normalization}

We have seen the importance of normalizing the input data, and we can apply similar reasoning to the variables in each hidden layer of a deep network. If there is wide variation in the range of activation values in a particular hidden layer, then normalizing those values to have zero mean and unit variance should make the learning problem easier for the next layer. However, unlike normalization of the input values, which can be done once prior to the start of training, normalization of the hiddenunit values will need to be repeated during training every time the weight values are updated. This is called batch normalization (Ioffe and Szegedy, 2015).

A further motivation for batch normalization arises from the phenomena of vanishing gradients and exploding gradients, which occur when we try to train very deep neural networks. From the chain rule of calculus, the gradient of an error function \(E\) with respect to a parameter in the first layer of the network is given by

\[
\frac{\partial E}{\partial w_{i}}=\sum_{m} \cdots \sum_{l} \sum_{j} \frac{\partial z_{m}^{(1)}}{\partial w_{i}} \cdots \frac{\partial z_{j}^{(K)}}{\partial z_{l}^{(K-1)}} \frac{\partial E}{\partial z_{j}^{(K)}}
\]

where \(z_{j}^{(k)}\) denotes the activation of node \(j\) in layer \(k\), and each of the partial derivatives on the right-hand side of (7.51) represents the elements of the Jacobian matrix for that layer. The product of a large number of such terms will tend towards 0 if most of them have a magnitude \(<1\) and will tend towards \(\infty\) if most of them have a magnitude \(>1\). Consequently, as the depth of a network increases, error function gradients can tend to become either very large or very small. Batch normalization largely resolves this issue.

To see how batch normalization is defined, consider a specific layer within a multi-layer network. Each hidden unit in that layer computes a nonlinear function of its input pre-activation \(z_{i}=h\left(a_{i}\right)\), and so we have a choice of whether to normalize the pre-activation values \(a_{i}\) or the activation values \(z_{i}\). In practice, either approach may be used, and here we illustrate the procedure by normalizing the pre-activations. Because weight values are updated after each mini-batch of examples, we apply the normalization to each mini-batch. Specifically, for a mini-batch of size \(K\), we define

\[
\begin{aligned}
\mu_{i} & =\frac{1}{K} \sum_{n=1}^{K} a_{n i} \\
\sigma_{i}^{2} & =\frac{1}{K} \sum_{n=1}^{K}\left(a_{n i}-\mu_{i}\right)^{2} \\
\widehat{a}_{n i} & =\frac{a_{n i}-\mu_{i}}{\sqrt{\sigma_{i}^{2}+\delta}}
\end{aligned}
\]

where the summations over \(n=1, \ldots, K\) are taken over the elements of the minibatch. Here \(\delta\) is a small constant, introduced to avoid numerical issues in situations where \(\sigma_{i}^{2}\) is small.

By normalizing the pre-activations in a given layer of the network, we reduce the number of degrees of freedom in the parameters of that layer and hence we
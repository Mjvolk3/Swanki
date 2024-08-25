Figure 5.16 Representation of a multi-class linear classification model as a neural network having a single layer of connections. Each basis function is represented by a node, with the solid node representing the 'bias' basis function $\phi_{0}$, whereas each output $y_{1}, \ldots, y_{N}$ is also represented by a node. The links between the nodes represent the corresponding weight and bias

![](https://cdn.mathpix.com/cropped/2024_05_26_4ee214bfb89bd0af3d94g-1.jpg?height=344&width=654&top_left_y=209&top_left_x=992)
parameters.

where $y_{n k}=y_{k}\left(\boldsymbol{\phi}_{n}\right)$, and $\mathbf{T}$ is an $N \times K$ matrix of target variables with elements $t_{n k}$. Taking the negative logarithm then gives

$$
E\left(\mathbf{w}_{1}, \ldots, \mathbf{w}_{K}\right)=-\ln p\left(\mathbf{T} \mid \mathbf{w}_{1}, \ldots, \mathbf{w}_{K}\right)=-\sum_{n=1}^{N} \sum_{k=1}^{K} t_{n k} \ln y_{n k}
$$

which is known as the cross-entropy error function for the multi-class classification problem.

We now take the gradient of the error function with respect to one of the param-

Exercise 5.22

Chapter 7

Section 5.4.6 eter vectors $\mathbf{w}_{j}$. Making use of the result (5.78) for the derivatives of the softmax function, we obtain

$$
\nabla_{\mathbf{w}_{j}} E\left(\mathbf{w}_{1}, \ldots, \mathbf{w}_{K}\right)=\sum_{n=1}^{N}\left(y_{n j}-t_{n j}\right) \phi_{n}
$$

where we have made use of $\sum_{k} t_{n k}=1$. Again, we could optimize the parameters through stochastic gradient descent.

Once again, we see the same form arising for the gradient as was found for the sum-of-squares error function with the linear model and for the cross-entropy error with the logistic regression model, namely the product of the error $\left(y_{n j}-t_{n j}\right)$ times the basis function activation $\phi_{n}$. These are examples of a more general result that we will explore later.

Linear classification models can be represented as single-layer neural networks as shown in Figure 5.16. If we consider the derivative of the error function with respect to a weight $w_{i k}$, which links basis function $\phi_{i}(\mathbf{x})$ to output unit $t_{k}$, we have from $(5.81)$

$$
\frac{\partial E\left(\mathbf{w}_{1}, \ldots, \mathbf{w}_{K}\right)}{\partial w_{i j}}=\sum_{n=1}^{N}\left(y_{n k}-t_{n k}\right) \phi_{i}\left(\mathbf{x}_{n}\right)
$$

Comparing this with Figure 5.16, we see that, for each data point $n$ this gradient takes the form of the output of the basis function at the input end of the weight link with the 'error' $\left(y_{n k}-t_{n k}\right)$ at the output end.
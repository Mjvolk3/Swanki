Figure 4.4 Representation of a linear regression model as a neural network having a single layer of connections. Each basis function is represented by a node, with the solid node representing the 'bias' basis function \(\phi_{0}\). Likewise each output \(y_{1}, \ldots, y_{K}\) is represented by a node. The links between the nodes represent the corresponding weight and bias

![](https://cdn.mathpix.com/cropped/2024_05_26_0b66c2c41c506aebc39ag-1.jpg?height=338&width=649&top_left_y=212&top_left_x=992)
parameters.

\title{
4.1.7 Multiple outputs
}

So far, we have considered situations with a single target variable \(t\). In some applications, we may wish to predict \(K>1\) target variables, which we denote collectively by the target vector \(\mathbf{t}=\left(t_{1}, \ldots, t_{K}\right)^{\mathrm{T}}\). This could be done by introducing a different set of basis functions for each component of \(t\), leading to multiple, independent regression problems. However, a more common approach is to use the same set of basis functions to model all of the components the target vector so that

\[
\mathbf{y}(\mathbf{x}, \mathbf{w})=\mathbf{W}^{\mathrm{T}} \boldsymbol{\phi}(\mathbf{x})
\]

where \(\mathbf{y}\) is a \(K\)-dimensional column vector, \(\mathbf{W}\) is an \(M \times K\) matrix of parameters, and \(\phi(\mathbf{x})\) is an \(M\)-dimensional column vector with elements \(\phi_{j}(\mathbf{x})\) with \(\phi_{0}(\mathbf{x})=1\) as before. Again, this can be represented as a neural network having a single layer of parameters, as shown in Figure 4.4.

Suppose we take the conditional distribution of the target vector to be an isotropic Gaussian of the form

\[
p\left(\mathbf{t} \mid \mathbf{x}, \mathbf{W}, \sigma^{2}\right)=\mathcal{N}\left(\mathbf{t} \mid \mathbf{W}^{\mathrm{T}} \boldsymbol{\phi}(\mathbf{x}), \sigma^{2} \mathbf{I}\right)
\]

If we have a set of observations \(\mathbf{t}_{1}, \ldots, \mathbf{t}_{N}\), we can combine these into a matrix \(\mathbf{T}\) of size \(N \times K\) such that the \(n\)th row is given by \(\mathbf{t}_{n}^{\mathrm{T}}\). Similarly, we can combine the input vectors \(\mathbf{x}_{1}, \ldots, \mathbf{x}_{N}\) into a matrix \(\mathbf{X}\). The log likelihood function is then given by

\[
\begin{aligned}
\ln p\left(\mathbf{T} \mid \mathbf{X}, \mathbf{W}, \sigma^{2}\right) & =\sum_{n=1}^{N} \ln \mathcal{N}\left(\mathbf{t}_{n} \mid \mathbf{W}^{\mathrm{T}} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right), \sigma^{2} \mathbf{I}\right) \\
& =-\frac{N K}{2} \ln \left(2 \pi \sigma^{2}\right)-\frac{1}{2 \sigma^{2}} \sum_{n=1}^{N}\left\|\mathbf{t}_{n}-\mathbf{W}^{\mathrm{T}} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right)\right\|^{2}
\end{aligned}
\]

As before, we can maximize this function with respect to \(\mathbf{W}\), giving

\[
\mathbf{W}_{\mathrm{ML}}=\left(\boldsymbol{\Phi}^{\mathrm{T}} \boldsymbol{\Phi}\right)^{-1} \boldsymbol{\Phi}^{\mathrm{T}} \mathbf{T}
\]

where we have combined the input feature vectors \(\phi\left(\mathbf{x}_{1}\right), \ldots, \phi\left(\mathbf{x}_{N}\right)\) into a matrix \(\boldsymbol{\Phi}\). If we examine this result for each target variable \(t_{k}\), we have

\[
\mathbf{w}_{k}=\left(\boldsymbol{\Phi}^{\mathrm{T}} \boldsymbol{\Phi}\right)^{-1} \boldsymbol{\Phi}^{\mathrm{T}} \mathbf{t}_{k}=\boldsymbol{\Phi}^{\dagger} \mathbf{t}_{k}
\]
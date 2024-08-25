\section*{Chapter 7}

Section 1.2

\section*{Exercise 4.6}

made before all the data points are seen.

We can obtain a sequential learning algorithm by applying the technique of stochastic gradient descent, also known as sequential gradient descent, as follows. If the error function comprises a sum over data points \(E=\sum_{n} E_{n}\), then after presentation of data point \(n\), the stochastic gradient descent algorithm updates the parameter vector \(\mathbf{w}\) using

\[
\mathbf{w}^{(\tau+1)}=\mathbf{w}^{(\tau)}-\eta \nabla E_{n}
\]

where \(\tau\) denotes the iteration number, and \(\eta\) is a suitably chosen learning rate parameter. The value of \(\mathbf{w}\) is initialized to some starting vector \(\mathbf{w}^{(0)}\). For the sum-ofsquares error function (4.11), this gives

\[
\mathbf{w}^{(\tau+1)}=\mathbf{w}^{(\tau)}+\eta\left(t_{n}-\mathbf{w}^{(\tau) \mathrm{T}} \boldsymbol{\phi}_{n}\right) \boldsymbol{\phi}_{n}
\]

where \(\phi_{n}=\phi\left(\mathbf{x}_{n}\right)\). This is known as the least-mean-squares or the LMS algorithm.

\title{
4.1.6 Regularized least squares
}

We have previously introduced the idea of adding a regularization term to an error function to control over-fitting, so that the total error function to be minimized takes the form

\[
E_{D}(\mathbf{w})+\lambda E_{W}(\mathbf{w})
\]

where \(\lambda\) is the regularization coefficient that controls the relative importance of the data-dependent error \(E_{D}(\mathbf{w})\) and the regularization term \(E_{W}(\mathbf{w})\). One of the simplest forms of regularizer is given by the sum of the squares of the weight vector elements:

\[
E_{W}(\mathbf{w})=\frac{1}{2} \sum_{j} w_{j}^{2}=\frac{1}{2} \mathbf{w}^{\mathrm{T}} \mathbf{w}
\]

If we also consider the sum-of-squares error function given by

\[
E_{D}(\mathbf{w})=\frac{1}{2} \sum_{n=1}^{N}\left\{t_{n}-\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right)\right\}^{2}
\]

then the total error function becomes

\[
\frac{1}{2} \sum_{n=1}^{N}\left\{t_{n}-\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right)\right\}^{2}+\frac{\lambda}{2} \mathbf{w}^{\mathrm{T}} \mathbf{w}
\]

In statistics, this regularizer provides an example of a parameter shrinkage method because it shrinks parameter values towards zero. It has the advantage that the error function remains a quadratic function of \(\mathbf{w}\), and so its exact minimizer can be found in closed form. Specifically, setting the gradient of (4.26) with respect to w to zero and solving for \(\mathrm{w}\) as before, we obtain

\[
\mathbf{w}=\left(\lambda \mathbf{I}+\boldsymbol{\Phi}^{\mathrm{T}} \boldsymbol{\Phi}\right)^{-1} \boldsymbol{\Phi}^{\mathrm{T}} \mathbf{t} .
\]

This represents a simple extension of the least-squares solution (4.14).
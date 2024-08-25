\section*{Exercise 5.18}

Exercise 5.19

Section 4.1.3

Chapter 7
We now use maximum likelihood to determine the parameters of the logistic regression model. To do this, we will make use of the derivative of the logistic sigmoid function, which can conveniently be expressed in terms of the sigmoid function itself:

$$
\frac{\mathrm{d} \sigma}{\mathrm{d} a}=\sigma(1-\sigma)
$$

For a data set $\left\{\boldsymbol{\phi}_{n}, t_{n}\right\}$, where $\boldsymbol{\phi}_{n}=\boldsymbol{\phi}\left(\mathbf{x}_{n}\right)$ and $t_{n} \in\{0,1\}$, with $n=1, \ldots, N$, the likelihood function can be written

$$
p(\mathbf{t} \mid \mathbf{w})=\prod_{n=1}^{N} y_{n}^{t_{n}}\left\{1-y_{n}\right\}^{1-t_{n}}
$$

where $\mathbf{t}=\left(t_{1}, \ldots, t_{N}\right)^{\mathrm{T}}$ and $y_{n}=p\left(\mathcal{C}_{1} \mid \boldsymbol{\phi}_{n}\right)$. As usual, we can define an error function by taking the negative logarithm of the likelihood, which gives the crossentropy error function:

$$
E(\mathbf{w})=-\ln p(\mathbf{t} \mid \mathbf{w})=-\sum_{n=1}^{N}\left\{t_{n} \ln y_{n}+\left(1-t_{n}\right) \ln \left(1-y_{n}\right)\right\}
$$

where $y_{n}=\sigma\left(a_{n}\right)$ and $a_{n}=\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}_{n}$. Taking the gradient of the error function with respect to $\mathbf{w}$, we obtain

$$
\nabla E(\mathbf{w})=\sum_{n=1}^{N}\left(y_{n}-t_{n}\right) \phi_{n}
$$

where we have made use of (5.72). We see that the factor involving the derivative of the logistic sigmoid has cancelled, leading to a simplified form for the gradient of the log likelihood. In particular, the contribution to the gradient from data point $n$ is given by the 'error' $y_{n}-t_{n}$ between the target value and the prediction of the model times the basis function vector $\phi_{n}$. Furthermore, comparison with (4.12) shows that this takes precisely the same form as the gradient of the sum-of-squares error function for the linear regression model.

The maximum likelihood solution corresponds to $\nabla E(\mathbf{w})=0$. However, from (5.75) we see that this no longer corresponds to a set of linear equations, due to the nonlinearity in $y(\cdot)$, and so this equation does not have a closed-form solution. One approach to finding a maximum likelihood solution would be to use stochastic gradient descent, in which $\nabla E_{n}$ is the $n$th term on the right-hand side of (5.75). Stochastic gradient descent will be the principal approach to training the highly nonlinear neural networks discussed in later chapters. However, the maximum likelihood equation is only 'slightly' nonlinear, and in fact the error function (5.74), in which the model is defined by (5.71), is a convex function of the parameters, which allows the error function to be minimized using a simple algorithm called iterative reweighted least squares or IRLS (Bishop, 2006). However, this does not easily generalize to more complex models such as deep neural networks.
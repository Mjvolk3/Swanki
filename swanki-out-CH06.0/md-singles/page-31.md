unit pre-activations denoted by \(a_{k}^{\pi}\) that determine the mixing coefficients \(\pi_{k}(\mathbf{x}), K\) outputs denoted by \(a_{k}^{\sigma}\) that determine the Gaussian standard deviations \(\sigma_{k}(\mathbf{x})\), and \(K \times L\) outputs denoted by \(a_{k j}^{\mu}\) that determine the components \(\mu_{k j}(\mathbf{x})\) of the Gaussian means \(\boldsymbol{\mu}_{k}(\mathbf{x})\). The total number of network outputs is given by \((L+2) K\), unlike the usual \(L\) outputs for a network that simply predicts the conditional means of the target variables.

The mixing coefficients must satisfy the constraints

\[
\sum_{k=1}^{K} \pi_{k}(\mathbf{x})=1, \quad 0 \leqslant \pi_{k}(\mathbf{x}) \leqslant 1
\]

which can be achieved using a set of softmax outputs:

\[
\pi_{k}(\mathbf{x})=\frac{\exp \left(a_{k}^{\pi}\right)}{\sum_{l=1}^{K} \exp \left(a_{l}^{\pi}\right)}
\]

Similarly, the variances must satisfy \(\sigma_{k}^{2}(\mathbf{x}) \geqslant 0\) and so can be represented in terms of the exponentials of the corresponding network pre-activations using

\[
\sigma_{k}(\mathbf{x})=\exp \left(a_{k}^{\sigma}\right)
\]

Finally, because the means \(\boldsymbol{\mu}_{k}(\mathrm{x})\) have real components, they can be represented directly by the network outputs:

\[
\mu_{k j}(\mathbf{x})=a_{k j}^{\mu}
\]

in which the output-unit activation functions are given by the identity \(f(a)=a\).

The learnable parameters of the mixture density network comprise the vector \(\mathbf{w}\) of weights and biases in the neural network, which can be set by maximum likelihood or equivalently by minimizing an error function defined to be the negative logarithm of the likelihood. For independent data, this error function takes the form

\[
E(\mathbf{w})=-\sum_{n=1}^{N} \ln \left\{\sum_{k=1}^{K} \pi_{k}\left(\mathbf{x}_{n}, \mathbf{w}\right) \mathcal{N}\left(\mathbf{t}_{n} \mid \boldsymbol{\mu}_{k}\left(\mathbf{x}_{n}, \mathbf{w}\right), \sigma_{k}^{2}\left(\mathbf{x}_{n}, \mathbf{w}\right)\right)\right\}
\]

where we have made the dependencies on \(\mathbf{w}\) explicit.

\title{
6.5.3 Gradient optimization
}

To minimize the error function, we need to calculate the derivatives of the error \(E(\mathbf{w})\) with respect to the components of \(\mathbf{w}\). We will see later how to compute these derivatives automatically. It is instructive, however, to derive suitable expressions for the derivatives of the error with respect to the output-unit pre-activations explicitly as this highlights the probabilistic interpretation of these quantities. Because the error function (6.43) is composed of a sum of terms, one for each training data point, we can consider the derivatives for a particular input vector \(\mathbf{x}_{n}\) with associated target vector \(\mathbf{t}_{n}\). The derivatives of the total error \(E\) are obtained by summing over all
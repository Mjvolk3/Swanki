Chapter 7

\section*{Exercise 6.17}

Exercise 6.18

Exercise 6.19

Exercise 6.20 data points, or the individual gradients for each data point can be used directly in gradient-based optimization algorithms.

It is convenient to introduce the following variables:

\[
\gamma_{n k}=\gamma_{k}\left(\mathbf{t}_{n} \mid \mathbf{x}_{n}\right)=\frac{\pi_{k} \mathcal{N}_{n k}}{\sum_{l=1}^{K} \pi_{l} \mathcal{N}_{n l}}
\]

where \(\mathcal{N}_{n k}\) denotes \(\mathcal{N}\left(\mathbf{t}_{n} \mid \boldsymbol{\mu}_{k}\left(\mathbf{x}_{n}\right), \sigma_{k}^{2}\left(\mathbf{x}_{n}\right)\right)\). These quantities have a natural interpretation as posterior probabilities for the components of the mixture in which the mixing coefficients \(\pi_{k}(\mathbf{x})\) are viewed as \(\mathbf{x}\)-dependent prior probabilities.

The derivatives of the error function with respect to the network output preactivations governing the mixing coefficients are given by

\[
\frac{\partial E_{n}}{\partial a_{k}^{\pi}}=\pi_{k}-\gamma_{n k}
\]

Similarly, the derivatives with respect to the output pre-activations controlling the component means are given by

\[
\frac{\partial E_{n}}{\partial a_{k l}^{\mu}}=\gamma_{n k}\left\{\frac{\mu_{k l}-t_{n l}}{\sigma_{k}^{2}}\right\}
\]

Finally, the derivatives with respect to the output pre-activations controlling the component variances are given by

\[
\frac{\partial E_{n}}{\partial a_{k}^{\sigma}}=\gamma_{n k}\left\{L-\frac{\left\|\mathbf{t}_{n}-\boldsymbol{\mu}_{k}\right\|^{2}}{\sigma_{k}^{2}}\right\}
\]

\subsection*{6.5.4 Predictive distribution}

We illustrate the use of a mixture density network by returning to the toy example of an inverse problem shown in Figure 6.17. Plots of the mixing coefficients \(\pi_{k}(x)\), the means \(\mu_{k}(x)\), and the conditional density contours corresponding to \(p(t \mid x)\), are shown in Figure 6.19. The outputs of the neural network, and hence the parameters in the mixture model, are necessarily continuous single-valued functions of the input variables. However, we see from Figure 6.19(c) that the model is able to produce a conditional density that is unimodal for some values of \(x\) and trimodal for other values by modulating the amplitudes of the mixing components \(\pi_{k}(\mathbf{x})\).

Once a mixture density network has been trained, it can predict the conditional density function of the target data for any given value of the input vector. This conditional density represents a complete description of the generator of the data, so far as the problem of predicting the value of the output vector is concerned. From this density function, we can calculate more specific quantities that may be of interest in different applications. One of the simplest of these is the mean, corresponding to the conditional average of the target data, and is given by

\[
\mathbb{E}[\mathbf{t} \mid \mathbf{x}]=\int \mathbf{t} p(\mathbf{t} \mid \mathbf{x}) \mathrm{d} \mathbf{t}=\sum_{k=1}^{K} \pi_{k}(\mathbf{x}) \boldsymbol{\mu}_{k}(\mathbf{x})
\]
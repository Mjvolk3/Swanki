Using the same line of argument as led to the derivation of the result (3.172), we see that the conditional mean of $t$, which we denote by $y$, is given by

$$
y \equiv \mathbb{E}[t \mid \eta]=-s \frac{d}{d \eta} \ln g(\eta)
$$

Thus, $y$ and $\eta$ must related, and we denote this relation through $\eta=\psi(y)$.

Following Nelder and Wedderburn (1972), we define a generalized linear model to be one for which $y$ is a nonlinear function of a linear combination of the input (or feature) variables so that

$$
y=f\left(\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}\right)
$$

where $f(\cdot)$ is known as the activation function in the machine learning literature, and $f^{-1}(\cdot)$ is known as the link function in statistics.

Now consider the log likelihood function for this model, which, as a function of $\eta$, is given by

$$
\ln p(\mathbf{t} \mid \eta, s)=\sum_{n=1}^{N} \ln p\left(t_{n} \mid \eta, s\right)=\sum_{n=1}^{N}\left\{\ln g\left(\eta_{n}\right)+\frac{\eta_{n} t_{n}}{s}\right\}+\text { const }
$$

where we are assuming that all observations share a common scale parameter (which corresponds to the noise variance for a Gaussian distribution, for instance) and so $s$ is independent of $n$. The derivative of the log likelihood with respect to the model parameters $\mathbf{w}$ is then given by

$$
\begin{aligned}
\nabla_{\mathbf{w}} \ln p(\mathbf{t} \mid \eta, s) & =\sum_{n=1}^{N}\left\{\frac{\mathrm{d}}{\mathrm{d} \eta_{n}} \ln g\left(\eta_{n}\right)+\frac{t_{n}}{s}\right\} \frac{\mathrm{d} \eta_{n}}{\mathrm{~d} y_{n}} \frac{\mathrm{d} y_{n}}{\mathrm{~d} a_{n}} \nabla_{\mathbf{w}} a_{n} \\
& =\sum_{n=1}^{N} \frac{1}{s}\left\{t_{n}-y_{n}\right\} \psi^{\prime}\left(y_{n}\right) f^{\prime}\left(a_{n}\right) \phi_{n}
\end{aligned}
$$

where $a_{n}=\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}_{n}$, and we have used $y_{n}=f\left(a_{n}\right)$ together with the result (5.90) for $\mathbb{E}[t \mid \eta]$. We now see that there is a considerable simplification if we choose a particular form for the link function $f^{-1}(y)$ given by

$$
f^{-1}(y)=\psi(y)
$$

which gives $f(\psi(y))=y$ and hence $f^{\prime}(\psi) \psi^{\prime}(y)=1$. Also, because $a=f^{-1}(y)$, we have $a=\psi$ and hence $f^{\prime}(a) \psi^{\prime}(y)=1$. In this case, the gradient of the error function reduces to

$$
\nabla \ln E(\mathbf{w})=\frac{1}{s} \sum_{n=1}^{N}\left\{y_{n}-t_{n}\right\} \boldsymbol{\phi}_{n}
$$

We have seen that there is a natural pairing between the choice of error function and the choice of output-unit activation function. Although we have derived this result in the context of single-layer network models, the same considerations apply to deep neural networks discussed in later chapters.
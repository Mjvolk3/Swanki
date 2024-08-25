Making use of the constraint (3.153), the multinomial distribution in this representation then becomes

$$
\begin{aligned}
& \exp \left\{\sum_{k=1}^{M} x_{k} \ln \mu_{k}\right\} \\
& =\exp \left\{\sum_{k=1}^{M-1} x_{k} \ln \mu_{k}+\left(1-\sum_{k=1}^{M-1} x_{k}\right) \ln \left(1-\sum_{k=1}^{M-1} \mu_{k}\right)\right\} \\
& =\exp \left\{\sum_{k=1}^{M-1} x_{k} \ln \left(\frac{\mu_{k}}{1-\sum_{j=1}^{M-1} \mu_{j}}\right)+\ln \left(1-\sum_{k=1}^{M-1} \mu_{k}\right)\right\}
\end{aligned}
$$

We now identify

$$
\ln \left(\frac{\mu_{k}}{1-\sum_{j} \mu_{j}}\right)=\eta_{k}
$$

which we can solve for $\mu_{k}$ by first summing both sides over $k$ and then rearranging and back-substituting to give

$$
\mu_{k}=\frac{\exp \left(\eta_{k}\right)}{1+\sum_{j} \exp \left(\eta_{j}\right)}
$$

This is called the softmax function or the normalized exponential. In this representation, the multinomial distribution therefore takes the form

$$
p(\mathbf{x} \mid \boldsymbol{\eta})=\left(1+\sum_{k=1}^{M-1} \exp \left(\eta_{k}\right)\right)^{-1} \exp \left(\boldsymbol{\eta}^{\mathrm{T}} \mathbf{x}\right)
$$

This is the standard form of the exponential family, with parameter vector $\boldsymbol{\eta}=$ $\left(\eta_{1}, \ldots, \eta_{M-1}\right)^{\mathrm{T}}$ in which

$$
\begin{aligned}
\mathbf{u}(\mathbf{x}) & =\mathbf{x} \\
h(\mathbf{x}) & =1 \\
g(\boldsymbol{\eta}) & =\left(1+\sum_{k=1}^{M-1} \exp \left(\eta_{k}\right)\right)^{-1}
\end{aligned}
$$

Finally, let us consider the Gaussian distribution. For the univariate Gaussian, we have

$$
\begin{aligned}
p\left(x \mid \mu, \sigma^{2}\right) & =\frac{1}{\left(2 \pi \sigma^{2}\right)^{1 / 2}} \exp \left\{-\frac{1}{2 \sigma^{2}}(x-\mu)^{2}\right\} \\
& =\frac{1}{\left(2 \pi \sigma^{2}\right)^{1 / 2}} \exp \left\{-\frac{1}{2 \sigma^{2}} x^{2}+\frac{\mu}{\sigma^{2}} x-\frac{1}{2 \sigma^{2}} \mu^{2}\right\}
\end{aligned}
$$

which, after some simple rearranging, can be cast in the standard exponential family form (3.138) with
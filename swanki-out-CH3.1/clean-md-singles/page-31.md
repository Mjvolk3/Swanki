which we can solve for $\mu$ to give $\mu=\sigma(\eta)$, where

$$
\sigma(\eta)=\frac{1}{1+\exp (-\eta)}
$$

is called the logistic sigmoid function. Thus, we can write the Bernoulli distribution using the standard representation (3.138) in the form

$$
p(x \mid \eta)=\sigma(-\eta) \exp (\eta x)
$$

where we have used $1-\sigma(\eta)=\sigma(-\eta)$, which is easily proved from (3.143). Comparison with (3.138) shows that

$$
\begin{aligned}
u(x) & =x \\
h(x) & =1 \\
g(\eta) & =\sigma(-\eta)
\end{aligned}
$$

Next consider the multinomial distribution which, for a single observation $\mathbf{x}$, takes the form

$$
p(\mathbf{x} \mid \boldsymbol{\mu})=\prod_{k=1}^{M} \mu_{k}^{x_{k}}=\exp \left\{\sum_{k=1}^{M} x_{k} \ln \mu_{k}\right\}
$$

where $\mathbf{x}=\left(x_{1}, \ldots, x_{M}\right)^{\mathrm{T}}$. Again, we can write this in the standard representation (3.138) so that

$$
p(\mathbf{x} \mid \boldsymbol{\eta})=\exp \left(\boldsymbol{\eta}^{\mathrm{T}} \mathbf{x}\right)
$$

where $\eta_{k}=\ln \mu_{k}$, and we have defined $\boldsymbol{\eta}=\left(\eta_{1}, \ldots, \eta_{M}\right)^{\mathrm{T}}$. Again, comparing with (3.138) we have

$$
\begin{aligned}
\mathbf{u}(\mathbf{x}) & =\mathbf{x} \\
h(\mathbf{x}) & =1 \\
g(\boldsymbol{\eta}) & =1
\end{aligned}
$$

Note that the parameters $\eta_{k}$ are not independent because the parameters $\mu_{k}$ are subject to the constraint

$$
\sum_{k=1}^{M} \mu_{k}=1
$$

so that, given any $M-1$ of the parameters $\mu_{k}$, the value of the remaining parameter is fixed. In some circumstances, it will be convenient to remove this constraint by expressing the distribution in terms of only $M-1$ parameters. This can be achieved by using the relationship (3.153) to eliminate $\mu_{M}$ by expressing it in terms of the remaining $\left\{\mu_{k}\right\}$ where $k=1, \ldots, M-1$, thereby leaving $M-1$ parameters. Note that these remaining parameters are still subject to the constraints

$$
0 \leqslant \mu_{k} \leqslant 1, \quad \sum_{k=1}^{M-1} \mu_{k} \leqslant 1
$$
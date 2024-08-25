correspond to the state where \(x_{3}=1\), then \(\mathbf{x}\) will be represented by

\[
\mathbf{x}=(0,0,1,0,0,0)^{\mathrm{T}}
\]

Note that such vectors satisfy \(\sum_{k=1}^{K} x_{k}=1\). If we denote the probability of \(x_{k}=1\) by the parameter \(\mu_{k}\), then the distribution of \(\mathbf{x}\) is given by

\[
p(\mathbf{x} \mid \boldsymbol{\mu})=\prod_{k=1}^{K} \mu_{k}^{x_{k}}
\]

where \(\boldsymbol{\mu}=\left(\mu_{1}, \ldots, \mu_{K}\right)^{\mathrm{T}}\), and the parameters \(\mu_{k}\) are constrained to satisfy \(\mu_{k} \geqslant 0\) and \(\sum_{k} \mu_{k}=1\), because they represent probabilities. The distribution (3.14) can be regarded as a generalization of the Bernoulli distribution to more than two outcomes. It is easily seen that the distribution is normalized:

\[
\sum_{\mathbf{x}} p(\mathbf{x} \mid \boldsymbol{\mu})=\sum_{k=1}^{K} \mu_{k}=1
\]

and that

\[
\mathbb{E}[\mathbf{x} \mid \boldsymbol{\mu}]=\sum_{\mathbf{x}} p(\mathbf{x} \mid \boldsymbol{\mu}) \mathbf{x}=\boldsymbol{\mu}
\]

Now consider a data set \(\mathcal{D}\) of \(N\) independent observations \(\mathbf{x}_{1}, \ldots, \mathbf{x}_{N}\). The corresponding likelihood function takes the form

\[
p(\mathcal{D} \mid \boldsymbol{\mu})=\prod_{n=1}^{N} \prod_{k=1}^{K} \mu_{k}^{x_{n k}}=\prod_{k=1}^{K} \mu_{k}^{\left(\sum_{n} x_{n k}\right)}=\prod_{k=1}^{K} \mu_{k}^{m_{k}}
\]

where we see that the likelihood function depends on the \(N\) data points only through the \(K\) quantities:

\[
m_{k}=\sum_{n=1}^{N} x_{n k}
\]

Section 3.4

Appendix \(C\)

which represent the number of observations of \(x_{k}=1\). These are called the sufficient statistics for this distribution. Note that the variables \(m_{k}\) are subject to the constraint

\[
\sum_{k=1}^{K} m_{k}=N
\]

To find the maximum likelihood solution for \(\boldsymbol{\mu}\), we need to maximize \(\ln p(\mathcal{D} \mid \boldsymbol{\mu})\) with respect to \(\mu_{k}\) taking account of the constraint (3.15) that the \(\mu_{k}\) must sum to one. This can be achieved using a Lagrange multiplier \(\lambda\) and maximizing

\[
\sum_{k=1}^{K} m_{k} \ln \mu_{k}+\lambda\left(\sum_{k=1}^{K} \mu_{k}-1\right)
\]
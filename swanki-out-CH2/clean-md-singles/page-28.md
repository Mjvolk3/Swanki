$p\left(x_{i}\right) \Delta$. This gives a discrete distribution for which the entropy takes the form

$$
\mathrm{H}_{\Delta}=-\sum_{i} p\left(x_{i}\right) \Delta \ln \left(p\left(x_{i}\right) \Delta\right)=-\sum_{i} p\left(x_{i}\right) \Delta \ln p\left(x_{i}\right)-\ln \Delta
$$

where we have used $\sum_{i} p\left(x_{i}\right) \Delta=1$, which follows from (2.89) and (2.25). We now omit the second term $-\ln \Delta$ on the right-hand side of (2.90), since it is independent of $p(x)$, and then consider the limit $\Delta \rightarrow 0$. The first term on the right-hand side of (2.90) will approach the integral of $p(x) \ln p(x)$ in this limit so that

$$
\lim _{\Delta \rightarrow 0}\left\{-\sum_{i} p\left(x_{i}\right) \Delta \ln p\left(x_{i}\right)\right\}=-\int p(x) \ln p(x) \mathrm{d} x
$$

where the quantity on the right-hand side is called the differential entropy. We see that the discrete and continuous forms of the entropy differ by a quantity $\ln \Delta$, which diverges in the limit $\Delta \rightarrow 0$. This reflects that specifying a continuous variable very precisely requires a large number of bits. For a density defined over multiple continuous variables, denoted collectively by the vector $\mathbf{x}$, the differential entropy is given by

$$
\mathrm{H}[\mathbf{x}]=-\int p(\mathbf{x}) \ln p(\mathbf{x}) \mathrm{d} \mathbf{x}
$$

\title{
2.5.4 Maximum entropy
}

We saw for discrete distributions that the maximum entropy configuration corresponds to a uniform distribution of probabilities across the possible states of the variable. Let us now consider the corresponding result for a continuous variable. If this maximum is to be well defined, it will be necessary to constrain the first and second moments of $p(x)$ and to preserve the normalization constraint. We therefore maximize the differential entropy with the three constraints:

$$
\begin{aligned}
\int_{-\infty}^{\infty} p(x) \mathrm{d} x & =1 \\
\int_{-\infty}^{\infty} x p(x) \mathrm{d} x & =\mu \\
\int_{-\infty}^{\infty}(x-\mu)^{2} p(x) \mathrm{d} x & =\sigma^{2}
\end{aligned}
$$

The constrained maximization can be performed using Lagrange multipliers so that we maximize the following functional with respect to $p(x)$ :

$$
\begin{aligned}
& -\int_{-\infty}^{\infty} p(x) \ln p(x) \mathrm{d} x+\lambda_{1}\left(\int_{-\infty}^{\infty} p(x) \mathrm{d} x-1\right) \\
& \quad+\lambda_{2}\left(\int_{-\infty}^{\infty} x p(x) \mathrm{d} x-\mu\right)+\lambda_{3}\left(\int_{-\infty}^{\infty}(x-\mu)^{2} p(x) \mathrm{d} x-\sigma^{2}\right)
\end{aligned}
$$
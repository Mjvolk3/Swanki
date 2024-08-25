which satisfies $P^{\prime}(x)=p(x)$, as shown in Figure 2.6.

If we have several continuous variables $x_{1}, \ldots, x_{D}$, denoted collectively by the vector $\mathbf{x}$, then we can define a joint probability density $p(\mathbf{x})=p\left(x_{1}, \ldots, x_{D}\right)$ such that the probability of $\mathbf{x}$ falling in an infinitesimal volume $\delta \mathbf{x}$ containing the point $\mathbf{x}$ is given by $p(\mathbf{x}) \delta \mathbf{x}$. This multivariate probability density must satisfy

$$
\begin{aligned}
p(\mathbf{x}) & \geqslant 0 \\
\int p(\mathbf{x}) \mathrm{d} \mathbf{x} & =1
\end{aligned}
$$

in which the integral is taken over the whole of $\mathbf{x}$ space. More generally, we can also consider joint probability distributions over a combination of discrete and continuous variables.

The sum and product rules of probability, as well as Bayes' theorem, also apply to probability densities as well as to combinations of discrete and continuous variables. If $\mathbf{x}$ and $\mathbf{y}$ are two real variables, then the sum and product rules take the form

$$
\begin{array}{lc}
\text { sum rule } & p(\mathbf{x})=\int p(\mathbf{x}, \mathbf{y}) \mathrm{d} \mathbf{y} \\
\text { product rule } & p(\mathbf{x}, \mathbf{y})=p(\mathbf{y} \mid \mathbf{x}) p(\mathbf{x})
\end{array}
$$

Similarly, Bayes' theorem can be written in the form

$$
p(\mathbf{y} \mid \mathbf{x})=\frac{p(\mathbf{x} \mid \mathbf{y}) p(\mathbf{y})}{p(\mathbf{x})}
$$

where the denominator is given by

$$
p(\mathbf{x})=\int p(\mathbf{x} \mid \mathbf{y}) p(\mathbf{y}) \mathrm{d} \mathbf{y}
$$

A formal justification of the sum and product rules for continuous variables requires a branch of mathematics called measure theory (Feller, 1966) and lies outside the scope of this book. Its validity can be seen informally, however, by dividing each real variable into intervals of width $\Delta$ and considering the discrete probability distribution over these intervals. Taking the limit $\Delta \rightarrow 0$ then turns sums into integrals and gives the desired result.

\title{
2.2.1 Example distributions
}

There are many forms of probability density that are in widespread use and that are important both in their own right and as building blocks for more complex probabilistic models. The simplest form would be one in which $p(x)$ is a constant, independent of $x$, but this cannot be normalized because the integral in (2.28) will be divergent. Distributions that cannot be normalized are called improper. We can, however, have the uniform distribution that is constant over a finite region, say $(c, d)$, and zero elsewhere, in which case (2.28) implies

$$
p(x)=1 /(d-c), \quad x \in(c, d)
$$
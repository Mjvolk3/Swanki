Appendix $B$

Exercise 2.24

Exercise 2.25

Using the calculus of variations, we set the derivative of this functional to zero giving

$$
p(x)=\exp \left\{-1+\lambda_{1}+\lambda_{2} x+\lambda_{3}(x-\mu)^{2}\right\}
$$

The Lagrange multipliers can be found by back-substitution of this result into the three constraint equations, leading finally to the result:

$$
p(x)=\frac{1}{\left(2 \pi \sigma^{2}\right)^{1 / 2}} \exp \left\{-\frac{(x-\mu)^{2}}{2 \sigma^{2}}\right\}
$$

and so the distribution that maximizes the differential entropy is the Gaussian. Note that we did not constrain the distribution to be non-negative when we maximized the entropy. However, because the resulting distribution is indeed non-negative, we see with hindsight that such a constraint is not necessary.

If we evaluate the differential entropy of the Gaussian, we obtain

$$
\mathrm{H}[x]=\frac{1}{2}\left\{1+\ln \left(2 \pi \sigma^{2}\right)\right\}
$$

Thus, we see again that the entropy increases as the distribution becomes broader, i.e., as $\sigma^{2}$ increases. This result also shows that the differential entropy, unlike the discrete entropy, can be negative, because $\mathrm{H}(x)<0$ in (2.99) for $\sigma^{2}<1 /(2 \pi e)$.

\title{
2.5.5 Kullback-Leibler divergence
}

So far in this section, we have introduced a number of concepts from information theory, including the key notion of entropy. We now start to relate these ideas to machine learning. Consider some unknown distribution $p(\mathbf{x})$, and suppose that we have modelled this using an approximating distribution $q(\mathbf{x})$. If we use $q(\mathbf{x})$ to construct a coding scheme for transmitting values of $\mathrm{x}$ to a receiver, then the average additional amount of information (in nats) required to specify the value of $\mathrm{x}$ (assuming we choose an efficient coding scheme) as a result of using $q(\mathbf{x})$ instead of the true distribution $p(\mathbf{x})$ is given by

$$
\begin{aligned}
\mathrm{KL}(p \| q) & =-\int p(\mathbf{x}) \ln q(\mathbf{x}) \mathrm{d} \mathbf{x}-\left(-\int p(\mathbf{x}) \ln p(\mathbf{x}) \mathrm{d} \mathbf{x}\right) \\
& =-\int p(\mathbf{x}) \ln \left\{\frac{q(\mathbf{x})}{p(\mathbf{x})}\right\} \mathrm{d} \mathbf{x}
\end{aligned}
$$

This is known as the relative entropy or Kullback-Leibler divergence, or KL divergence (Kullback and Leibler, 1951), between the distributions $p(\mathbf{x})$ and $q(\mathbf{x})$. Note that it is not a symmetrical quantity, that is to say $\operatorname{KL}(p \| q) \not \equiv \operatorname{KL}(q \| p)$.

We now show that the Kullback-Leibler divergence satisfies $\operatorname{KL}(p \| q) \geqslant 0$ with equality if, and only if, $p(\mathbf{x})=q(\mathbf{x})$. To do this we first introduce the concept of convex functions. A function $f(x)$ is said to be convex if it has the property that every chord lies on or above the function, as shown in Figure 2.15.

Any value of $x$ in the interval from $x=a$ to $x=b$ can be written in the form $\lambda a+(1-\lambda) b$ where $0 \leqslant \lambda \leqslant 1$. The corresponding point on the chord
Figure 2.7 Plots of a uniform distribution over the range $(-1,1)$, shown in red, the exponential distribution with $\lambda=1$, shown in blue, and a Laplace distribution with $\mu=1$ and $\gamma=1$, shown in green.

![](https://cdn.mathpix.com/cropped/2024_05_10_1078b436a401e29e2f93g-1.jpg?height=500&width=703&top_left_y=219&top_left_x=955)

Another simple form of density is the exponential distribution given by

$$
p(x \mid \lambda)=\lambda \exp (-\lambda x), \quad x \geqslant 0
$$

A variant of the exponential distribution, known as the Laplace distribution, allows the peak to be moved to a location $\mu$ and is given by

$$
p(x \mid \mu, \gamma)=\frac{1}{2 \gamma} \exp \left(-\frac{|x-\mu|}{\gamma}\right)
$$

The constant, exponential, and Laplace distributions are illustrated in Figure 2.7.

Another important distribution is the Dirac delta function, which is written

$$
p(x \mid \mu)=\delta(x-\mu)
$$

This is defined to be zero everywhere except at $x=\mu$ and to have the property of integrating to unity according to (2.28). Informally, we can think of this as an infinitely narrow and infinitely tall spike located at $x=\mu$ with the property of having unit area. Finally, if we have a finite set of observations of $x$ given by $\mathcal{D}=\left\{x_{1}, \ldots, x_{N}\right\}$ then we can use the delta function to construct the empirical distribution given by

$$
p(x \mid \mathcal{D})=\frac{1}{N} \sum_{n=1}^{N} \delta\left(x-x_{n}\right)
$$

which consists of a Dirac delta function centred on each of the data points. The probability density defined by (2.37) integrates to one as required.

\title{
2.2.2 Expectations and covariances
}

One of the most important operations involving probabilities is that of finding weighted averages of functions. The weighted average of some function $f(x)$ under a probability distribution $p(x)$ is called the expectation of $f(x)$ and will be denoted by $\mathbb{E}[f]$. For a discrete distribution, it is given by summing over all possible values of $x$ in the form

$$
\mathbb{E}[f]=\sum_{x} p(x) f(x)
$$
where the average is weighted by the relative probabilities of the different values of $x$. For continuous variables, expectations are expressed in terms of an integration with respect to the corresponding probability density:

$$
\mathbb{E}[f]=\int p(x) f(x) \mathrm{d} x
$$

In either case, if we are given a finite number $N$ of points drawn from the probability distribution or probability density, then the expectation can be approximated as a Exercise 2.7 finite sum over these points:

$$
\mathbb{E}[f] \simeq \frac{1}{N} \sum_{n=1}^{N} f\left(x_{n}\right)
$$

The approximation in (2.40) becomes exact in the limit $N \rightarrow \infty$.

Sometimes we will be considering expectations of functions of several variables, in which case we can use a subscript to indicate which variable is being averaged over, so that for instance

$$
\mathbb{E}_{x}[f(x, y)]
$$

denotes the average of the function $f(x, y)$ with respect to the distribution of $x$. Note that $\mathbb{E}_{x}[f(x, y)]$ will be a function of $y$.

We can also consider a conditional expectation with respect to a conditional distribution, so that

$$
\mathbb{E}_{x}[f \mid y]=\sum_{x} p(x \mid y) f(x)
$$

which is also a function of $y$. For continuous variables, the conditional expectation takes the form

$$
\mathbb{E}_{x}[f \mid y]=\int p(x \mid y) f(x) \mathrm{d} x
$$

The variance of $f(x)$ is defined by

$$
\operatorname{var}[f]=\mathbb{E}\left[(f(x)-\mathbb{E}[f(x)])^{2}\right]
$$

and provides a measure of how much $f(x)$ varies around its mean value $\mathbb{E}[f(x)]$. Expanding out the square, we see that the variance can also be written in terms of the expectations of $f(x)$ and $f(x)^{2}$ :

$$
\operatorname{var}[f]=\mathbb{E}\left[f(x)^{2}\right]-\mathbb{E}[f(x)]^{2}
$$

In particular, we can consider the variance of the variable $x$ itself, which is given by

$$
\operatorname{var}[x]=\mathbb{E}\left[x^{2}\right]-\mathbb{E}[x]^{2}
$$

For two random variables $x$ and $y$, the covariance measures the extent to which the two variables vary together and is defined by

$$
\begin{aligned}
\operatorname{cov}[x, y] & =\mathbb{E}_{x, y}[\{x-\mathbb{E}[x]\}\{y-\mathbb{E}[y]\}] \\
& =\mathbb{E}_{x, y}[x y]-\mathbb{E}[x] \mathbb{E}[y]
\end{aligned}
$$
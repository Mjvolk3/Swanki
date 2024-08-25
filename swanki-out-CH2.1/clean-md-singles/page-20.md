We can also use maximum likelihood to determine the variance parameter $\sigma^{2}$.

Exercise 2.18 Maximizing (2.66) with respect to $\sigma^{2}$ gives

$$
\sigma_{\mathrm{ML}}^{2}=\frac{1}{N} \sum_{n=1}^{N}\left\{y\left(x_{n}, \mathbf{w}_{\mathrm{ML}}\right)-t_{n}\right\}^{2}
$$

Note that we can first determine the parameter vector $\mathbf{w}_{\mathrm{ML}}$ governing the mean, and subsequently use this to find the variance $\sigma_{\mathrm{ML}}^{2}$ as was the case for the simple Gaussian distribution.

Having determined the parameters $\mathbf{w}$ and $\sigma^{2}$, we can now make predictions for new values of $x$. Because we now have a probabilistic model, these are expressed in terms of the predictive distribution that gives the probability distribution over $t$, rather than simply a point estimate, and is obtained by substituting the maximum likelihood parameters into (2.64) to give

$$
p\left(t \mid x, \mathbf{w}_{\mathrm{ML}}, \sigma_{\mathrm{ML}}^{2}\right)=\mathcal{N}\left(t \mid y\left(x, \mathbf{w}_{\mathrm{ML}}\right), \sigma_{\mathrm{ML}}^{2}\right)
$$

\title{
2.4. Transformation of Densities
}

\section*{Chapter 18}

We turn now to a discussion of how a probability density transforms under a nonlinear change of variable. This property will play a crucial role when we discuss a class of generative models called normalizing flows. It also highlights that a probability density has a different behaviour than a simple function under such transformations.

Consider a single variable $x$ and suppose we make a change of variables $x=$ $g(y)$, then a function $f(x)$ becomes a new function $\widetilde{f}(y)$ defined by

$$
\widetilde{f}(y)=f(g(y))
$$

Now consider a probability density $p_{x}(x)$, and again change variables using $x=$ $g(y)$, giving rise to a density $p_{y}(y)$ with respect to the new variable $y$, where the suffixes denote that $p_{x}(x)$ and $p_{y}(y)$ are different densities. Observations falling in the range $(x, x+\delta x)$ will, for small values of $\delta x$, be transformed into the range $(y, y+\delta y)$, where $x=g(y)$, and $p_{x}(x) \delta x \simeq p_{y}(y) \delta y$. Hence, if we take the limit $\delta x \rightarrow 0$, we obtain

$$
\begin{aligned}
p_{y}(y) & =p_{x}(x)\left|\frac{\mathrm{d} x}{\mathrm{~d} y}\right| \\
& =p_{x}(g(y))\left|\frac{\mathrm{d} g}{\mathrm{~d} y}\right|
\end{aligned}
$$

Here the modulus $|\cdot|$ arises because the derivative $\mathrm{d} y / \mathrm{d} x$ could be negative, whereas the density is scaled by the ratio of lengths, which is always positive.
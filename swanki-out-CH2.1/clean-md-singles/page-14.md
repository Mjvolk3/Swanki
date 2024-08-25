Figure 2.8 Plot of a Gaussian distribution for a single continuous variable $x$ showing the mean $\mu$ and the standard deviation $\sigma$.

![](https://cdn.mathpix.com/cropped/2024_05_10_0b3cce270cab6a31625fg-1.jpg?height=555&width=770&top_left_y=216&top_left_x=890)

Exercise $2.9 \quad$ If $x$ and $y$ are independent, then their covariance equals zero.

For two vectors $\mathbf{x}$ and $\mathbf{y}$, their covariance is a matrix given by

$$
\begin{aligned}
\operatorname{cov}[\mathbf{x}, \mathbf{y}] & =\mathbb{E}_{\mathbf{x}, \mathbf{y}}\left[\{\mathbf{x}-\mathbb{E}[\mathbf{x}]\}\left\{\mathbf{y}^{\mathrm{T}}-\mathbb{E}\left[\mathbf{y}^{\mathrm{T}}\right]\right\}\right] \\
& =\mathbb{E}_{\mathbf{x}, \mathbf{y}}\left[\mathbf{x} \mathbf{y}^{\mathrm{T}}\right]-\mathbb{E}[\mathbf{x}] \mathbb{E}\left[\mathbf{y}^{\mathrm{T}}\right]
\end{aligned}
$$

If we consider the covariance of the components of a vector $\mathbf{x}$ with each other, then we use a slightly simpler notation $\operatorname{cov}[\mathbf{x}] \equiv \operatorname{cov}[\mathbf{x}, \mathbf{x}]$.

\title{
2.3. The Gaussian Distribution
}

One of the most important probability distributions for continuous variables is called the normal or Gaussian distribution, and we will make extensive use of this distribution throughout the rest of the book. For a single real-valued variable $x$, the Gaussian distribution is defined by

$$
\mathcal{N}\left(x \mid \mu, \sigma^{2}\right)=\frac{1}{\left(2 \pi \sigma^{2}\right)^{1 / 2}} \exp \left\{-\frac{1}{2 \sigma^{2}}(x-\mu)^{2}\right\}
$$

which represents a probability density over $x$ governed by two parameters: $\mu$, called the mean, and $\sigma^{2}$, called the variance. The square root of the variance, given by $\sigma$, is called the standard deviation, and the reciprocal of the variance, written as $\beta=1 / \sigma^{2}$, is called the precision. We will see the motivation for this terminology shortly. Figure 2.8 shows a plot of the Gaussian distribution. Although the form of the Gaussian distribution might seem arbitrary, we will see later that it arises

Section 2.5 .4 naturally from the concept of maximum entropy and from the perspective of the Section 3.2

From (2.49) we see that the Gaussian distribution satisfies

$$
\mathcal{N}\left(x \mid \mu, \sigma^{2}\right)>0
$$
Figure 2.9 Illustration of the likelihood function for the Gaussian distribution shown by the red curve. Here the grey points denote a data set of values $\left\{x_{n}\right\}$, and the likelihood function (2.55) is given by the product of the corresponding values of $p(x)$ denoted by the blue points. Maximizing the likelihood involves adjusting the mean and variance of the Gaussian so as to maximize this product.

![](https://cdn.mathpix.com/cropped/2024_05_10_21eb94606b794741a6f9g-1.jpg?height=471&width=689&top_left_y=219&top_left_x=957)

set $\mathbf{x}$ is i.i.d., we can therefore write the probability of the data set, given $\mu$ and $\sigma^{2}$, in the form

$$
p\left(\mathbf{x} \mid \mu, \sigma^{2}\right)=\prod_{n=1}^{N} \mathcal{N}\left(x_{n} \mid \mu, \sigma^{2}\right)
$$

When viewed as a function of $\mu$ and $\sigma^{2}$, this is called the likelihood function for the Gaussian and is interpreted diagrammatically in Figure 2.9.

One common approach for determining the parameters in a probability distribution using an observed data set, known as maximum likelihood, is to find the parameter values that maximize the likelihood function. This might appear to be a strange criterion because, from our foregoing discussion of probability theory, it would seem more natural to maximize the probability of the parameters given the data, not the probability of the data given the parameters. In fact, these two criteria are related.

To start with, however, we will determine values for the unknown parameters $\mu$ and $\sigma^{2}$ in the Gaussian by maximizing the likelihood function (2.55). In practice, it is more convenient to maximize the $\log$ of the likelihood function. Because the logarithm is a monotonically increasing function of its argument, maximizing the $\log$ of a function is equivalent to maximizing the function itself. Taking the $\log$ not only simplifies the subsequent mathematical analysis, but it also helps numerically because the product of a large number of small probabilities can easily underflow the numerical precision of the computer, and this is resolved by computing the sum of the $\log$ probabilities instead. From (2.49) and (2.55), the log likelihood function can be written in the form

$$
\ln p\left(\mathbf{x} \mid \mu, \sigma^{2}\right)=-\frac{1}{2 \sigma^{2}} \sum_{n=1}^{N}\left(x_{n}-\mu\right)^{2}-\frac{N}{2} \ln \sigma^{2}-\frac{N}{2} \ln (2 \pi)
$$

Maximizing (2.56) with respect to $\mu$, we obtain the maximum likelihood solution Exercise $2.15 \quad$ given by

$$
\mu_{\mathrm{ML}}=\frac{1}{N} \sum_{n=1}^{N} x_{n}
$$
![](https://cdn.mathpix.com/cropped/2024_05_10_10ceec4bdaa45dd5506eg-1.jpg?height=1248&width=1238&top_left_y=216&top_left_x=412

ChatGPT figure/image summary: The image shows a colorful abstract background with the number "2" prominently displayed in the center and the word "Probabilities" below it. This appears to be the title page or heading for a chapter or section in a book or document that deals with the topic of probabilities, likely in the context of mathematics or statistics. The design is meant to be visually engaging while signifying the start of a new section focused on the concept of probabilities.)

In almost every application of machine learning we have to deal with uncertainty. For example, a system that classifies images of skin lesions as benign or malignant can never in practice achieve perfect accuracy. We can distinguish between two kinds of uncertainty. The first is epistemic uncertainty (derived from the Greek word episteme meaning knowledge), sometimes called systematic uncertainty. It arises because we only get to see data sets of finite size. As we observe more data, for instance more examples of benign and malignant skin lesion images, we are better able to predict the class of a new example. However, even with an infinitely large data set, we would still not be able to achieve perfect accuracy due to the second kind of uncertainty known as aleatoric uncertainty, also called intrinsic or stochastic uncertainty, or sometimes simply called noise. Generally speaking, the noise arises because we are able to observe only partial information about the world, and therefore, one way to reduce this source of uncertainty is to gather different kinds of data. This is illustrated

Figure 2.6 The concept of probability for discrete variables can be extended to that of a probability density $p(x)$ over a continuous variable $x$ and is such that the probability of $x$ lying in the interval $(x, x+\delta x)$ is given by $p(x) \delta x$ for $\delta x \rightarrow 0$. The probability density can be expressed as the derivative of a cumulative distribution function $P(x)$.

![](https://cdn.mathpix.com/cropped/2024_05_10_46157df5e120ef4bbe80g-1.jpg?height=545&width=767&top_left_y=216&top_left_x=891

ChatGPT figure/image summary: The image displays a graph illustrating two curves representing different mathematical functions related to probability. The horizontal axis is labeled as "x", and there are two curves plotted:

1. A blue curve that fluctuates across the graph labeled as "p(x)" which represents a probability density function (pdf). It shows how the probability density varies with the variable x. This curve is not uniform, indicating that the probability density changes across different values of x.

2. A red curve labeled as "P(x)" which represents a cumulative distribution function (CDF). It is a monotonically increasing function that represents the probability that the random variable X will take a value less than or equal to x.

Also, there's a shaded vertical strip labeled as "δx" which is illustrating an infinitesimally small interval around a particular value of x. The probability that the random variable falls within this interval can be approximated by the area under the blue curve (p(x)) over that interval, indicated by the product "p(x) δx" as δx approaches zero. This graphical representation ties into the explanation of probability density functions and cumulative distribution functions described in the text.)

\title{
2.2. Probability Densities
}

As well as considering probabilities defined over discrete sets of values, we also wish to consider probabilities with respect to continuous variables. For instance, we might wish to predict what dose of drug to give to a patient. Since there will be uncertainty in this prediction, we want to quantify this uncertainty and again we can make use of probabilities. However, we cannot simply apply the concepts of probability discussed so far directly, since the probability of observing a specific value for a continuous variable, to infinite precision, will effectively be zero. Instead, we need to introduce the concept of a probability density. Here we will limit ourselves to a relatively informal discussion.

We define the probability density $p(x)$ over a continuous variable $x$ to be such that the probability of $x$ falling in the interval $(x, x+\delta x)$ is given by $p(x) \delta x$ for $\delta x \rightarrow 0$. This is illustrated in Figure 2.6. The probability that $x$ will lie in an interval $(a, b)$ is then given by

$$
p(x \in(a, b))=\int_{a}^{b} p(x) \mathrm{d} x
$$

Because probabilities are non-negative, and because the value of $x$ must lie somewhere on the real axis, the probability density $p(x)$ must satisfy the two conditions

$$
\begin{array}{r}
p(x) \geqslant 0 \\
\int_{-\infty}^{\infty} p(x) \mathrm{d} x=1
\end{array}
$$

The probability that $x$ lies in the interval $(-\infty, z)$ is given by the cumulative distribution function defined by

$$
P(z)=\int_{-\infty}^{z} p(x) \mathrm{d} x
$$

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

Figure 2.7 Plots of a uniform distribution over the range $(-1,1)$, shown in red, the exponential distribution with $\lambda=1$, shown in blue, and a Laplace distribution with $\mu=1$ and $\gamma=1$, shown in green.

![](https://cdn.mathpix.com/cropped/2024_05_10_1078b436a401e29e2f93g-1.jpg?height=500&width=703&top_left_y=219&top_left_x=955

ChatGPT figure/image summary: The image is a graph showing three probability density functions plotted against a variable \( x \). Each function is represented by a different color:

1. The red plot represents a uniform distribution over the range \((-1, 1)\). It is constant within this interval and zero elsewhere. The height is such that the area under the curve within the interval adds up to 1, indicating a properly normalized probability distribution.

2. The blue plot represents an exponential distribution with parameter \(\lambda = 1\). The graph shows a positive exponential decrease starting from the y-axis and decaying as \( x \) increases. It starts at \( x = 0 \) and continues towards positive infinity.

3. The green plot represents a Laplace distribution with parameters \(\mu = 1\) and \(\gamma = 1\). It features a peak at the value of \( x \) corresponding to the mean \(\mu\), and the graph is symmetric on both sides of this peak, showing exponential decay towards both directions from \(\mu\).

The x-axis is labeled with \( x \), and the y-axis is labeled with \( p(x) \), indicating probability density. This graph is a visual representation of the probability densities described in the text preceding this figure, demonstrating different functional forms of simple probability distributions.)

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

Figure 2.8 Plot of a Gaussian distribution for a single continuous variable $x$ showing the mean $\mu$ and the standard deviation $\sigma$.

![](https://cdn.mathpix.com/cropped/2024_05_10_0b3cce270cab6a31625fg-1.jpg?height=555&width=770&top_left_y=216&top_left_x=890

ChatGPT figure/image summary: The image shows a plot of the Gaussian (normal) distribution for a single continuous variable \( x \). This function is illustrated with a bell-shaped curve that is symmetrical around the mean \( \mu \). The graph is labeled with \( \mathcal{N}(x|\mu,\sigma^2) \) on the y-axis, indicating that this is the probability density of \( x \). The x-axis represents the variable \( x \), with a point marked as \( \mu \), identifying the mean of the distribution. There is also a horizontal two-headed arrow spanning the width labeled as \( 2\sigma \), which indicates that this length represents two standard deviations from the mean (one to the left and one to the right), illustrating the region where approximately 95% of the values lie if the data is normally distributed.)

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

Exercise 2.12

Exercise 2.13

Exercise 2.14
Also, it is straightforward to show that the Gaussian is normalized, so that

$$
\int_{-\infty}^{\infty} \mathcal{N}\left(x \mid \mu, \sigma^{2}\right) \mathrm{d} x=1
$$

Thus, (2.49) satisfies the two requirements for a valid probability density.

\subsection*{2.3.1 Mean and variance}

We can readily find expectations of functions of $x$ under the Gaussian distribution. In particular, the average value of $x$ is given by

$$
\mathbb{E}[x]=\int_{-\infty}^{\infty} \mathcal{N}\left(x \mid \mu, \sigma^{2}\right) x \mathrm{~d} x=\mu
$$

Because the parameter $\mu$ represents the average value of $x$ under the distribution, it is referred to as the mean. The integral in (2.52) is known as the first-order moment of the distribution because it is the expectation of $x$ raised to the power one. We can similarly evaluate the second-order moment given by

$$
\mathbb{E}\left[x^{2}\right]=\int_{-\infty}^{\infty} \mathcal{N}\left(x \mid \mu, \sigma^{2}\right) x^{2} \mathrm{~d} x=\mu^{2}+\sigma^{2}
$$

From (2.52) and (2.53), it follows that the variance of $x$ is given by

$$
\operatorname{var}[x]=\mathbb{E}\left[x^{2}\right]-\mathbb{E}[x]^{2}=\sigma^{2}
$$

and hence $\sigma^{2}$ is referred to as the variance parameter. The maximum of a distribution is known as its mode. For a Gaussian, the mode coincides with the mean.

\subsection*{2.3.2 Likelihood function}

Suppose that we have a data set of observations represented as a row vector $\mathbf{x}=\left(x_{1}, \ldots, x_{N}\right)$, representing $N$ observations of the scalar variable $x$. Note that we are using the typeface $\mathbf{x}$ to distinguish this from a single observation of a $D$ dimensional vector-valued variable, which we represent by a column vector $\mathbf{x}=$ $\left(x_{1}, \ldots, x_{D}\right)^{\mathrm{T}}$. We will suppose that the observations are drawn independently from a Gaussian distribution whose mean $\mu$ and variance $\sigma^{2}$ are unknown, and we would like to determine these parameters from the data set. The problem of estimating a distribution, given a finite set of observations, is known as density estimation. It should be emphasized that the problem of density estimation is fundamentally illposed, because there are infinitely many probability distributions that could have given rise to the observed finite data set. Indeed, any distribution $p(\mathbf{x})$ that is nonzero at each of the data points $\mathbf{x}_{1}, \ldots, \mathbf{x}_{N}$ is a potential candidate. Here we constrain the space of distributions to be Gaussians, which leads to a well-defined solution.

Data points that are drawn independently from the same distribution are said to be independent and identically distributed, which is often abbreviated to i.i.d. or IID. We have seen that the joint probability of two independent events is given by the product of the marginal probabilities for each event separately. Because our data

Figure 2.9 Illustration of the likelihood function for the Gaussian distribution shown by the red curve. Here the grey points denote a data set of values $\left\{x_{n}\right\}$, and the likelihood function (2.55) is given by the product of the corresponding values of $p(x)$ denoted by the blue points. Maximizing the likelihood involves adjusting the mean and variance of the Gaussian so as to maximize this product.

![](https://cdn.mathpix.com/cropped/2024_05_10_21eb94606b794741a6f9g-1.jpg?height=471&width=689&top_left_y=219&top_left_x=957

ChatGPT figure/image summary: In the image, you see a graphical representation of the likelihood function for a Gaussian (normal) distribution, depicted by the red curve. The grey points along the horizontal axis represent a dataset of values \(\{x_n\}\), and the blue points on the curve directly above these grey points show the corresponding values of the probability density function \(p(x)\) for the Gaussian distribution with parameters \(\mu\) and \(\sigma^2\). The green vertical lines connect the dataset points (grey) with their respective probability density function values (blue). The notation \(N(x_n | \mu, \sigma^2)\) indicates that the blue points are obtained from the Gaussian density function with mean \(\mu\) and variance \(\sigma^2\) evaluated at points \(x_n\). Maximizing the likelihood function involves adjusting the mean \(\mu\) and variance \(\sigma^2\) of the Gaussian distribution so that the product of the probabilities corresponding to the observed data points is maximized.)

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

which is the sample mean, i.e., the mean of the observed values $\left\{x_{n}\right\}$. Similarly, maximizing (2.56) with respect to $\sigma^{2}$, we obtain the maximum likelihood solution for the variance in the form

$$
\sigma_{\mathrm{ML}}^{2}=\frac{1}{N} \sum_{n=1}^{N}\left(x_{n}-\mu_{\mathrm{ML}}\right)^{2}
$$

which is the sample variance measured with respect to the sample mean $\mu_{\mathrm{ML}}$. Note that we are performing a joint maximization of (2.56) with respect to $\mu$ and $\sigma^{2}$, but for a Gaussian distribution, the solution for $\mu$ decouples from that for $\sigma^{2}$ so that we can first evaluate (2.57) and then subsequently use this result to evaluate (2.58).

\title{
2.3.3 Bias of maximum likelihood
}

The technique of maximum likelihood is widely used in deep learning and forms the foundation for most machine learning algorithms. However, it has some limitations, which we can illustrate using a univariate Gaussian.

We first note that the maximum likelihood solutions $\mu_{\mathrm{ML}}$ and $\sigma_{\mathrm{ML}}^{2}$ are functions of the data set values $x_{1}, \ldots, x_{N}$. Suppose that each of these values has been generated independently from a Gaussian distribution whose true parameters are $\mu$ and $\sigma^{2}$. Now consider the expectations of $\mu_{\mathrm{ML}}$ and $\sigma_{\mathrm{ML}}^{2}$ with respect to these data set values. It is straightforward to show that

$$
\begin{aligned}
\mathbb{E}\left[\mu_{\mathrm{ML}}\right] & =\mu \\
\mathbb{E}\left[\sigma_{\mathrm{ML}}^{2}\right] & =\left(\frac{N-1}{N}\right) \sigma^{2}
\end{aligned}
$$

We see that, when averaged over data sets of a given size, the maximum likelihood solution for the mean will equal the true mean. However, the maximum likelihood estimate of the variance will underestimate the true variance by a factor $(N-1) / N$. This is an example of a phenomenon called bias in which the estimator of a random quantity is systematically different from the true value. The intuition behind this result is given by Figure 2.10.

Note that bias arises because the variance is measured relative to the maximum likelihood estimate of the mean, which itself is tuned to the data. Suppose instead we had access to the true mean $\mu$ and we used this to determine the variance using the estimator

Exercise 2.17

$$
\widehat{\sigma}^{2}=\frac{1}{N} \sum_{n=1}^{N}\left(x_{n}-\mu\right)^{2}
$$

Then we find that

$$
\mathbb{E}\left[\widehat{\sigma}^{2}\right]=\sigma^{2}
$$

which is unbiased. Of course, we do not have access to the true mean but only to the observed data values. From the result (2.60) it follows that for a Gaussian distribution, the following estimate for the variance parameter is unbiased:

$$
\widetilde{\sigma}^{2}=\frac{N}{N-1} \sigma_{\mathrm{ML}}^{2}=\frac{1}{N-1} \sum_{n=1}^{N}\left(x_{n}-\mu_{\mathrm{ML}}\right)^{2}
$$


![](https://cdn.mathpix.com/cropped/2024_05_10_b1d2b75d968ee60f6ba8g-1.jpg?height=316&width=1492&top_left_y=210&top_left_x=154

ChatGPT figure/image summary: The image shows three separate graphs, each representing a different dataset consisting of two data points (indicated by the green dots). For each graph, there are two Gaussian distributions depicted: the true Gaussian distribution (in red) and the Gaussian distribution obtained by maximum likelihood fitting to the observed data points (in blue).

The vertical dashed lines indicate the true mean (µ) of the data-generating process. The red curves represent the true Gaussian distribution centered at this mean with variance σ² (although the variance itself is not explicitly shown in the image). The blue curves represent the maximum likelihood estimate of the Gaussian distribution based on the limited data points provided by the green dots. The peaks of the blue curves correspond to the sample mean (µ_ML) of the respective datasets. It's clear that the blue curves have smaller variances than the red one, which reflects the underestimation of the variance by the maximum likelihood estimator, a concept explained in the provided text.

This image illustrates the concept of bias in the context of maximum likelihood estimation, specifically how using the maximum likelihood estimator for the mean does not introduce bias (as the expectation of the mean matches the true mean), but using it for the variance underestimates the true variance of the distribution. It provides a visual representation of the bias concept described in the section titled "2.3.3 Bias of maximum likelihood" in the context of a univariate Gaussian distribution.)

Figure 2.10 Illustration of how bias arises when using maximum likelihood to determine the mean and variance of a Gaussian. The red curves show the true Gaussian distribution from which data is generated, and the three blue curves show the Gaussian distributions obtained by fitting to three data sets, each consisting of two data points shown in green, using the maximum likelihood results (2.57) and (2.58). Averaged across the three data sets, the mean is correct, but the variance is systematically underestimated because it is measured relative to the sample mean and not relative to the true mean.

Section 2.6.3

Section 1.2
Correcting for the bias of maximum likelihood in complex models such as neural networks is not so easy, however.

Note that the bias of the maximum likelihood solution becomes less significant as the number $N$ of data points increases. In the limit $N \rightarrow \infty$ the maximum likelihood solution for the variance equals the true variance of the distribution that generated the data. In the case of the Gaussian, for anything other than small $N$, this bias will not prove to be a serious problem. However, throughout this book we will be interested in complex models with many parameters, for which the bias problems associated with maximum likelihood will be much more severe. In fact, the issue of bias in maximum likelihood is closely related to the problem of over-fitting.

\subsection*{2.3.4 Linear regression}

We have seen how the problem of linear regression can be expressed in terms of error minimization. Here we return to this example and view it from a probabilistic perspective, thereby gaining some insights into error functions and regularization.

The goal in the regression problem is to be able to make predictions for the target variable $t$ given some new value of the input variable $x$ by using a set of training data comprising $N$ input values $\mathbf{x}=\left(x_{1}, \ldots, x_{N}\right)$ and their corresponding target values $\mathbf{t}=\left(t_{1}, \ldots, t_{N}\right)$. We can express our uncertainty over the value of the target variable using a probability distribution. For this purpose, we will assume that, given the value of $x$, the corresponding value of $t$ has a Gaussian distribution with a mean equal to the value $y(x, \mathbf{w})$ of the polynomial curve given by (1.1), where $\mathbf{w}$ are the polynomial coefficients, and a variance $\sigma^{2}$. Thus, we have

$$
p\left(t \mid x, \mathbf{w}, \sigma^{2}\right)=\mathcal{N}\left(t \mid y(x, \mathbf{w}), \sigma^{2}\right)
$$

This is illustrated schematically in Figure 2.11.

We now use the training data $\{\mathbf{x}, \mathbf{t}\}$ to determine the values of the unknown parameters $\mathbf{w}$ and $\sigma^{2}$ by maximum likelihood. If the data is assumed to be drawn

Figure 2.11 Schematic illustration of a Gaussian conditional distribution for $t$ given $x$, defined by (2.64), in which the mean is given by the polynomial function $y(x, \mathbf{w})$, and the variance is given by the parameter $\sigma^{2}$.

![](https://cdn.mathpix.com/cropped/2024_05_10_0e32f455ec8070cf8fccg-1.jpg?height=681&width=694&top_left_y=221&top_left_x=955

ChatGPT figure/image summary: The image shows a plot of a mathematical function and data points, which is related to the topic of regression analysis, a statistical process for estimating the relationships among variables. The red curve represents a true function, denoted as \( y(x, w) \), which is a mathematical model to fit the data points. The blue dots are data points that are generated by adding Gaussian noise to the true function \( y(x, w) \), simulating observed data in an experiment or a study.

The blue curve represents a Gaussian distribution centered on the vertical line at \( x_0 \), indicating the distribution of the target variable \( t \) given the input variable \( x \), shown as \( p(t | x_0, w, \sigma^2) \). This curve reflects the probability distribution for the outcome variable \( t \) for a given \( x \) value (in this case \( x_0 \)), where \( \sigma^2 \) denotes the variance of the Gaussian distribution. Hence, the image demonstrates the concept of conditional probability distribution in a regression context, where the goal is to predict the target variable \( t \) given a new input \( x \) based on a learned model.)

independently from the distribution (2.64), then the likelihood function is given by

$$
p\left(\mathbf{t} \mid \mathbf{x}, \mathbf{w}, \sigma^{2}\right)=\prod_{n=1}^{N} \mathcal{N}\left(t_{n} \mid y\left(x_{n}, \mathbf{w}\right), \sigma^{2}\right)
$$

As we did for the simple Gaussian distribution earlier, it is convenient to maximize the logarithm of the likelihood function. Substituting for the Gaussian distribution, given by (2.49), we obtain the log likelihood function in the form

$$
\ln p\left(\mathbf{t} \mid \mathbf{x}, \mathbf{w}, \sigma^{2}\right)=-\frac{1}{2 \sigma^{2}} \sum_{n=1}^{N}\left\{y\left(x_{n}, \mathbf{w}\right)-t_{n}\right\}^{2}-\frac{N}{2} \ln \sigma^{2}-\frac{N}{2} \ln (2 \pi)
$$

Consider first the evaluation of the maximum likelihood solution for the polynomial coefficients, which will be denoted by $\mathbf{w}_{\mathrm{ML}}$. These are determined by maximizing (2.66) with respect to w. For this purpose, we can omit the last two terms on the right-hand side of (2.66) because they do not depend on w. Also, note that scaling the $\log$ likelihood by a positive constant coefficient does not alter the location of the maximum with respect to $\mathbf{w}$, and so we can replace the coefficient $1 / 2 \sigma^{2}$ with $1 / 2$. Finally, instead of maximizing the log likelihood, we can equivalently minimize the negative $\log$ likelihood. We therefore see that maximizing the likelihood is equivalent, so far as determining $\mathbf{w}$ is concerned, to minimizing the sum-of-squares error function defined by

$$
E(\mathbf{w})=\frac{1}{2} \sum_{n=1}^{N}\left\{y\left(x_{n}, \mathbf{w}\right)-t_{n}\right\}^{2}
$$

Thus, the sum-of-squares error function has arisen as a consequence of maximizing the likelihood under the assumption of a Gaussian noise distribution.

![](https://cdn.mathpix.com/cropped/2024_05_10_9d5d7b4dd8479033db17g-1.jpg?height=520&width=694&top_left_y=219&top_left_x=151

ChatGPT figure/image summary: The image is a three-dimensional plot of a surface. The axes are labeled \( x1 \), \( x2 \), and \( y \), and they form a right-handed coordinate system. The surface itself is a two-dimensional wave-like pattern, which appears to be a mathematical graph possibly representing a function of two variables, such as \( y = \sin(2\pi x1) \sin(2\pi x2) \), as described in the text. The surface has a sinusoidal pattern along both the \( x1 \) and \( x2 \) axes, with peaks and troughs that repeat regularly in both directions. This type of plot could be used to visualize functions in two variables for analysis or to provide visual insight into multivariable data in mathematics or engineering contexts.)

(a)

![](https://cdn.mathpix.com/cropped/2024_05_10_9d5d7b4dd8479033db17g-1.jpg?height=407&width=406&top_left_y=329&top_left_x=852

ChatGPT figure/image summary: This image appears to correspond to Figure 2.1(b) based on the description you provided. It shows a plot of 100 data points where the horizontal axis represents the variable \( x_1 \), and the vertical axis is labeled "y," which likely signifies the measured output or target variable. In this scenario, \( x_2 \) is unobserved, and as a result, the plot shows high levels of noise in the data due to the lack of information about \( x_2 \). This visualization reflects a two-dimensional regression problem reduced to one dimension due to the unobserved variable, which leads to a greater spread in the data points along the vertical axis.)

(b)

![](https://cdn.mathpix.com/cropped/2024_05_10_9d5d7b4dd8479033db17g-1.jpg?height=410&width=359&top_left_y=330&top_left_x=1242

ChatGPT figure/image summary: The image you've provided shows a scatter plot graph with a collection of data points presented in red. The points appear to be distributed in a nonlinear pattern, resembling part of a curve or circular shape, plotted against an x-axis labeled as \( x_1 \). This plotting scheme suggests that we may be looking at a graphical representation of a data set with one dimension observable (represented on the x-axis), while other dimensions or variables that might affect the distribution are not visualized. This image exemplifies the appearance of data when viewed in a reduced dimension, which can often obscure underlying relationships.

This image corresponds to the descriptive text associating it with Figure 2.1(b). According to the text, the plot represents 100 data points where a second variable, \( x_2 \), is unobserved, reflecting high levels of noise in the data. This unobserved variable is a key factor in the scenario described, which affects the spread and distribution of the data points in such a way that, without this dimension, the data looks highly dispersed and noisy. This would be an example of how missing information about certain variables can have a pronounced impact on the apparent structure, or lack thereof, in a data set.)

(c)

Figure 2.1 An extension of the simple sine curve regression problem to two dimensions. (a) A plot of the function $y\left(x_{1}, x_{2}\right)=\sin \left(2 \pi x_{1}\right) \sin \left(2 \pi x_{2}\right)$. Data is generated by selecting values for $x_{1}$ and $x_{2}$, computing the corresponding value of $y\left(x_{1}, x_{2}\right)$, and then adding Gaussian noise. (b) Plot of 100 data points in which $x_{2}$ is unobserved showing high levels of noise. (c) Plot of 100 data points in which $x_{2}$ is fixed to the value $x_{2}=\frac{\pi}{2}$, simulating the effect of being able to measure $x_{2}$ as well as $x_{1}$, showing much lower levels of noise.

Section 1.2

Section 2.1

Section 5.2 using an extension of the sine curve example to two dimensions in Figure 2.1.

As a practical example of this, a biopsy sample of the skin lesion is much more informative than the image alone and might greatly improve the accuracy with which we can determine if a new lesion is malignant. Given both the image and the biopsy data, the intrinsic uncertainty might be very small, and by collecting a large training data set, we may be able to reduce the systematic uncertainty to a low level and thereby make predictions of the class of the lesion with high accuracy.

Both kinds of uncertainty can be handled using the framework of probability theory, which provides a consistent paradigm for the quantification and manipulation of uncertainty and therefore forms one of the central foundations for machine learning. We will see that probabilities are governed by two simple formulae known as the sum rule and the product rule. When coupled with decision theory, these rules allow us, at least in principle, to make optimal predictions given all the information available to us, even though that information may be incomplete or ambiguous.

The concept of probability is often introduced in terms of frequencies of repeatable events. Consider, for example, the bent coin shown in Figure 2.2, and suppose that the shape of the coin is such that if it is flipped a large number of times, it lands concave side up $60 \%$ of the time, and therefore lands convex side up $40 \%$ of the time. We say that the probability of landing concave side up is $60 \%$ or 0.6 . Strictly, the probability is defined in the limit of an infinite number of 'trials' or coin flips in this case. Because the coin must land either concave side up or convex side up, these probabilities add to $100 \%$ or 1.0. This definition of probability in terms of the frequency of repeatable events is the basis for the frequentist view of statistics.

Now suppose that, although we know that the probability that the coin will land concave side up is 0.6 , we are not allowed to look at the coin itself and we do not

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

This procedure for transforming densities can be very powerful. Any density $p(y)$ can be obtained from a fixed density $q(x)$ that is everywhere non-zero by making a nonlinear change of variable $y=f(x)$ in which $f(x)$ is a monotonic function so that $0 \leqslant f^{\prime}(x)<\infty$.

One consequence of the transformation property (2.71) is that the concept of the maximum of a probability density is dependent on the choice of variable. Suppose $f(x)$ has a mode (i.e., a maximum) at $\widehat{x}$ so that $f^{\prime}(\widehat{x})=0$. The corresponding mode of $\widetilde{f}(y)$ will occur for a value $\widehat{y}$ obtained by differentiating both sides of (2.70) with respect to $y$ :

$$
\tilde{f}^{\prime}(\widehat{y})=f^{\prime}(g(\widehat{y})) g^{\prime}(\widehat{y})=0
$$

Assuming $g^{\prime}(\widehat{y}) \neq 0$ at the mode, then $f^{\prime}(g(\widehat{y}))=0$. However, we know that $f^{\prime}(\widehat{x})=0$, and so we see that the locations of the mode expressed in terms of each of the variables $x$ and $y$ are related by $\widehat{x}=g(\widehat{y})$, as one would expect. Thus, finding a mode with respect to the variable $x$ is equivalent to first transforming to the variable $y$, then finding a mode with respect to $y$, and then transforming back to $x$.

Now consider the behaviour of a probability density $p_{x}(x)$ under the change of variables $x=g(y)$, where the density with respect to the new variable is $p_{y}(y)$ and is given by (2.71). To deal with the modulus in (2.71) we can write $g^{\prime}(y)=s\left|g^{\prime}(y)\right|$ where $s \in\{-1,+1\}$. Then $(2.71)$ can be written as

$$
p_{y}(y)=p_{x}(g(y)) s g^{\prime}(y)
$$

where we have used $1 / s=s$. Differentiating both sides with respect to $y$ then gives

$$
p_{y}^{\prime}(y)=s p_{x}^{\prime}(g(y))\left\{g^{\prime}(y)\right\}^{2}+s p_{x}(g(y)) g^{\prime \prime}(y)
$$

Due to the presence of the second term on the right-hand side of (2.73), the relationship $\widehat{x}=g(\widehat{y})$ no longer holds. Thus, the value of $x$ obtained by maximizing $p_{x}(x)$ will not be the value obtained by transforming to $p_{y}(y)$ then maximizing with respect to $y$ and then transforming back to $x$. This causes modes of densities to be dependent on the choice of variables. However, for a linear transformation, the second term on the right-hand side of (2.73) vanishes, and so in this case the location of the maximum transforms according to $\widehat{x}=g(\widehat{y})$.

This effect can be illustrated with a simple example, as shown in Figure 2.12. We begin by considering a Gaussian distribution $p_{x}(x)$ over $x$ shown by the red curve in Figure 2.12. Next we draw a sample of $N=50,000$ points from this distribution and plot a histogram of their values, which as expected agrees with the distribution $p_{x}(x)$. Now consider a nonlinear change of variables from $x$ to $y$ given by

$$
x=g(y)=\ln (y)-\ln (1-y)+5
$$

The inverse of this function is given by

$$
y=g^{-1}(x)=\frac{1}{1+\exp (-x+5)}
$$

which is a logistic sigmoid function and is shown in Figure 2.12 by the blue curve.

Figure 2.12 Example of the transformation of the mode of a density under a nonlinear change of variables, illustrating the different behaviour compared to a simple function.

![](https://cdn.mathpix.com/cropped/2024_05_10_99e0ce50ade2d8f270a1g-1.jpg?height=498&width=721&top_left_y=220&top_left_x=939

ChatGPT figure/image summary: The image illustrates a mathematical concept related to the transformation of probability distributions. On the right side of the image, there is a red curve, representing a Gaussian distribution \( p_x(x) \) as a function of the variable \( x \). Below this curve, there is a histogram in blue that represents a sample of data points drawn from this Gaussian distribution.

On the left side, there is a blue curve labeled \( g^{-1}(x) \), which represents the transformation from \( x \) to \( y \) using a logistic sigmoid function, which is the inverse of the function given by \( x = g(y) = \ln(y) - \ln(1-y) + 5 \).

Additionally, there is a green curve on the left side that represents the Gaussian distribution \( p_x(x) \) transformed as a function of \( y \) through the function \( g^{-1} \), labeled as \( p_x(g(y)) \).

Finally, there's a magenta curve, also on the left side, which represents the actual transformed density \( p_y(y) \) over \( y \), according to the transformation property mentioned in the contextual information. This differs from the green curve as it takes into account the change of variables' effect on the density, leading to a different location for the mode (the peak of the density).

This figure aims to display the difference between simply transforming the Gaussian distribution as a function of \( x \) and the actual transformation of the density over \( y \) which includes the Jacobian determinant factor, resulting in the shift of the mode as visualized by the magenta curve. The shaded areas under the curves likely correspond to the probability mass, and hatched regions might serve to emphasize the differences between the histograms and the actual distributions after transformation.)

If we simply transform $p_{x}(x)$ as a function of $x$ we obtain the green curve $p_{x}(g(y))$ shown in Figure 2.12, and we see that the mode of the density $p_{x}(x)$ is transformed via the sigmoid function to the mode of this curve. However, the density over $y$ transforms instead according to (2.71) and is shown by the magenta curve on the left side of the diagram. Note that this has its mode shifted relative to the mode of the green curve.

To confirm this result, we take our sample of 50,000 values of $x$, evaluate the corresponding values of $y$ using (2.75), and then plot a histogram of their values. We see that this histogram matches the magenta curve in Figure 2.12 and not the green curve.

\title{
2.4.1 Multivariate distributions
}

We can extend the result (2.71) to densities defined over multiple variables. Consider a density $p(\mathbf{x})$ over a $D$-dimensional variable $\mathbf{x}=\left(x_{1}, \ldots, x_{D}\right)^{\mathrm{T}}$, and suppose we transform to a new variable $\mathbf{y}=\left(y_{1}, \ldots, y_{D}\right)^{\mathrm{T}}$ where $\mathbf{x}=\mathbf{g}(\mathbf{y})$. Here we will limit ourselves to the case where $\mathbf{x}$ and $\mathbf{y}$ have the same dimensionality. The transformed density is then given by the generalization of (2.71) in the form

$$
p_{\mathbf{y}}(\mathbf{y})=p_{\mathbf{x}}(\mathbf{x})|\operatorname{det} \mathbf{J}|
$$

where $\mathbf{J}$ is the Jacobian matrix whose elements are given by the partial derivatives $J_{i j}=\partial g_{i} / \partial y_{j}$, so that

$$
\mathbf{J}=\left[\begin{array}{ccc}
\frac{\partial g_{1}}{\partial y_{1}} & \cdots & \frac{\partial g_{1}}{\partial y_{D}} \\
\vdots & \ddots & \vdots \\
\frac{\partial g_{D}}{\partial y_{1}} & \cdots & \frac{\partial g_{D}}{\partial y_{D}}
\end{array}\right]
$$

Intuitively, we can view the change of variables as expanding some regions of space and contracting others, with an infinitesimal region $\Delta \mathrm{x}$ around a point $\mathrm{x}$ being transformed to a region $\Delta \mathbf{y}$ around the point $\mathbf{y}=\mathbf{g}(\mathbf{x})$. The absolute value of the determinant of the Jacobian represents the ratio of these volumes and is the same factor

![](https://cdn.mathpix.com/cropped/2024_05_10_effe402d88fd8f278266g-1.jpg?height=894&width=1394&top_left_y=227&top_left_x=209

ChatGPT figure/image summary: The image shows a three-part comparison illustrating the effect of a nonlinear transformation on a two-dimensional probability distribution. In the top row, we have three different representations:

- On the left side, there is a grid representing the initial coordinate system with the axes labeled \(x_1\) and \(x_2\). This is the space where the original distribution is defined.
- In the middle, there is a heat map of a Gaussian distribution, where the intensity of the color corresponds to the probability density. The distribution is centered and exhibits a radial symmetry, indicating higher density towards the center.
- On the right side, there is a scatter plot of red points, which are samples drawn from the Gaussian distribution shown in the middle figure. These points are densely concentrated near the center of the plot, consistent with the high probability density of the Gaussian distribution.

In the bottom row, the same three types of representation showcase the transformed variables:

- On the left side, there is a grid now representing the transformed coordinate system with axes labeled \(y_1\) and \(y_2\). The grid lines are distorted, indicating that a nonlinear transformation has been applied.
- In the middle, there is another heat map, now showing the transformed distribution, which has become more complex and multimodal as a result of the nonlinear transformation.
- On the right side, there is another scatter plot of red points, representing the same samples from the top right figure but now plotted in the transformed coordinate space. The scatter plot shows that the points are spread out and assume a more complex structure corresponding to the transformed distribution's heat map.

The general impression from this figure is to demonstrate how the nonlinear change of variables distorts the initial Gaussian distribution and how the corresponding samples are dispersed according to this transformation. The precise mathematical transformation applied to the coordinates is not explained in this image alone but would be detailed in the body of the text accompanying this figure.)

$x_{1}$
![](https://cdn.mathpix.com/cropped/2024_05_10_effe402d88fd8f278266g-1.jpg?height=760&width=398&top_left_y=288&top_left_x=226

ChatGPT figure/image summary: The image depicts a visual illustration of how a two-dimensional grid transformation occurs. It demonstrates the effect of a nonlinear variable change on the grid lines that represent the probability distribution in two dimensions. 

In the upper part of the image, you see a regularly spaced grid pattern in a space designated by \(x_1\) and \(x_2\). This can be understood as the original coordinate system where the variables are uniformly spaced and follow a standard Cartesian grid.

Below the arrow, the grid has been transformed into a new space, designated by \(y_1\) and \(y_2\). The effect of the transformation is seen as a distortion of the grid lines, which now appear as curved and varying in spacing. This grid deformation visually represents the change of variables from \(x\) space to \(y\) space following a nonlinear transformation.

This diagram is likely illustrating the conceptual change of variables in a probability distribution, analogous to the transformation described in the text you provided. It visually explains how a simple, regular distribution over \(x_1\) and \(x_2\) would look quite different when transformed into the \(y\) coordinate system due to the nonlinear relationship between the two. The distortion of the grid lines suggests that the transformation has expanded certain regions and contracted others, which would impact the density of the distribution and the position of its mode, consistent with the nonlinear change of variables concept described earlier.)

$y_{1}$ $x_{1}$

$y_{1}$ $y_{1}$

Figure 2.13 Illustration of the effect of a change of variables on a probability distribution in two dimensions. The left column shows the transforming of the variables whereas the middle and right columns show the corresponding effects on a Gaussian distribution and on samples from that distribution, respectively.

that arises when changing variables within an integral. The formula (2.77) follows from the fact that the probability mass in region $\Delta \mathrm{x}$ is the same as the probability mass in $\Delta \mathbf{y}$. Once again, we take the modulus to ensure that the density is nonnegative.

We can illustrate this by applying a change of variables to a Gaussian distribution in two dimensions, as shown in the top row in Figure 2.13. Here the transformation Exercise 2.20 from $\mathbf{x}$ to $\mathbf{y}$ is given by

$$
\begin{aligned}
& y_{1}=x_{1}+\tanh \left(5 x_{1}\right) \\
& y_{2}=x_{2}+\tanh \left(5 x_{2}\right)+\frac{x_{1}^{3}}{3}
\end{aligned}
$$

Also shown on the bottom row are samples from a Gaussian distribution in $\mathrm{x}$-space along with the corresponding transformed samples in $\mathbf{y}$-space.

\title{
2.5. Information Theory
}

Probability theory forms the basis for another important framework called information theory, which quantifies the information present in a data set and which plays an important role in machine learning. Here we give a brief introduction to some of the key elements of information theory that we will need later in the book, including the important concept of entropy in its various forms. For a more comprehensive introduction to information theory, with connections to machine learning, see MacKay (2003).

\subsection*{2.5.1 Entropy}

We begin by considering a discrete random variable $x$ and we ask how much information is received when we observe a specific value for this variable. The amount of information can be viewed as the 'degree of surprise' on learning the value of $x$. If we are told that a highly improbable event has just occurred, we will have received more information than if we were told that some very likely event has just occurred, and if we knew that the event was certain to happen, we would receive no information. Our measure of information content will therefore depend on the probability distribution $p(x)$, and so we look for a quantity $h(x)$ that is a monotonic function of the probability $p(x)$ and that expresses the information content. The form of $h(\cdot)$ can be found by noting that if we have two events $x$ and $y$ that are unrelated, then the information gained from observing both of them should be the sum of the information gained from each of them separately, so that $h(x, y)=h(x)+h(y)$. Two unrelated events are statistically independent and so $p(x, y)=p(x) p(y)$. From these two relationships, it is easily shown that $h(x)$ must be given by the logarithm

Exercise 2.21 of $p(x)$ and so we have

$$
h(x)=-\log _{2} p(x)
$$

where the negative sign ensures that information is positive or zero. Note that low probability events $x$ correspond to high information content. The choice of base for the logarithm is arbitrary, and for the moment we will adopt the convention prevalent in information theory of using logarithms to the base of 2 . In this case, as we will see shortly, the units of $h(x)$ are bits ('binary digits').

Now suppose that a sender wishes to transmit the value of a random variable to a receiver. The average amount of information that they transmit in the process is obtained by taking the expectation of (2.80) with respect to the distribution $p(x)$ and is given by

$$
\mathrm{H}[x]=-\sum_{x} p(x) \log _{2} p(x)
$$

This important quantity is called the entropy of the random variable $x$. Note that $\lim _{\epsilon \rightarrow 0}(\epsilon \ln \epsilon)=0$ and so we will take $p(x) \ln p(x)=0$ whenever we encounter a value for $x$ such that $p(x)=0$.

So far, we have given a rather heuristic motivation for the definition of information (2.80) and the corresponding entropy (2.81). We now show that these definitions

indeed possess useful properties. Consider a random variable $x$ having eight possible states, each of which is equally likely. To communicate the value of $x$ to a receiver, we would need to transmit a message of length 3 bits. Notice that the entropy of this variable is given by

$$
\mathrm{H}[x]=-8 \times \frac{1}{8} \log _{2} \frac{1}{8}=3 \text { bits. }
$$

Now consider an example (Cover and Thomas, 1991) of a variable having eight possible states $\{a, b, c, d, e, f, g, h\}$ for which the respective probabilities are given by $\left(\frac{1}{2}, \frac{1}{4}, \frac{1}{8}, \frac{1}{16}, \frac{1}{64}, \frac{1}{64}, \frac{1}{64}, \frac{1}{64}\right)$. The entropy in this case is given by

$$
\mathrm{H}[x]=-\frac{1}{2} \log _{2} \frac{1}{2}-\frac{1}{4} \log _{2} \frac{1}{4}-\frac{1}{8} \log _{2} \frac{1}{8}-\frac{1}{16} \log _{2} \frac{1}{16}-\frac{4}{64} \log _{2} \frac{1}{64}=2 \text { bits. }
$$

We see that the nonuniform distribution has a smaller entropy than the uniform one, and we will gain some insight into this shortly when we discuss the interpretation of entropy in terms of disorder. For the moment, let us consider how we would transmit the identity of the variable's state to a receiver. We could do this, as before, using a 3-bit number. However, we can take advantage of the nonuniform distribution by using shorter codes for the more probable events, at the expense of longer codes for the less probable events, in the hope of getting a shorter average code length. This can be done by representing the states $\{a, b, c, d, e, f, g, h\}$ using, for instance, the following set of code strings: $0,10,110,1110,111100,111101,111110$, and 111111. The average length of the code that has to be transmitted is then

average code length $=\frac{1}{2} \times 1+\frac{1}{4} \times 2+\frac{1}{8} \times 3+\frac{1}{16} \times 4+4 \times \frac{1}{64} \times 6=2$ bits,

which again is the same as the entropy of the random variable. Note that shorter code strings cannot be used because it must be possible to disambiguate a concatenation of such strings into its component parts. For instance, 11001110 decodes uniquely into the state sequence $c, a, d$. This relation between entropy and shortest coding length is a general one. The noiseless coding theorem (Shannon, 1948) states that the entropy is a lower bound on the number of bits needed to transmit the state of a random variable.

From now on, we will switch to the use of natural logarithms in defining entropy, as this will provide a more convenient link with ideas elsewhere in this book. In this case, the entropy is measured in units of nats (from 'natural logarithm') instead of bits, which differ simply by a factor of $\ln 2$.

\title{
2.5.2 Physics perspective
}

We have introduced the concept of entropy in terms of the average amount of information needed to specify the state of a random variable. In fact, the concept of entropy has much earlier origins in physics where it was introduced in the context of equilibrium thermodynamics and later given a deeper interpretation as a measure of disorder through developments in statistical mechanics. We can understand this alternative view of entropy by considering a set of $N$ identical objects that are to be divided amongst a set of bins, such that there are $n_{i}$ objects in the $i$ th bin. Consider

the number of different ways of allocating the objects to the bins. There are $N$ ways to choose the first object, $(N-1)$ ways to choose the second object, and so on, leading to a total of $N$ ! ways to allocate all $N$ objects to the bins, where $N$ ! (pronounced ' $N$ factorial') denotes the product $N \times(N-1) \times \cdots \times 2 \times 1$. However, we do not wish to distinguish between rearrangements of objects within each bin. In the $i$ th bin there are $n_{i}$ ! ways of reordering the objects, and so the total number of ways of allocating the $N$ objects to the bins is given by

$$
W=\frac{N!}{\prod_{i} n_{i}!}
$$

which is called the multiplicity. The entropy is then defined as the logarithm of the multiplicity scaled by a constant factor $1 / N$ so that

$$
\mathrm{H}=\frac{1}{N} \ln W=\frac{1}{N} \ln N!-\frac{1}{N} \sum_{i} \ln n_{i}!
$$

We now consider the limit $N \rightarrow \infty$, in which the fractions $n_{i} / N$ are held fixed, and apply Stirling's approximation:

$$
\ln N!\simeq N \ln N-N
$$

which gives

$$
\mathrm{H}=-\lim _{N \rightarrow \infty} \sum_{i}\left(\frac{n_{i}}{N}\right) \ln \left(\frac{n_{i}}{N}\right)=-\sum_{i} p_{i} \ln p_{i}
$$

where we have used $\sum_{i} n_{i}=N$. Here $p_{i}=\lim _{N \rightarrow \infty}\left(n_{i} / N\right)$ is the probability of an object being assigned to the $i$ th bin. In physics terminology, the specific allocation of objects into bins is called a microstate, and the overall distribution of occupation numbers, expressed through the ratios $n_{i} / N$, is called a macrostate. The multiplicity $W$, which expresses the number of microstates in a given macrostate, is also known as the weight of the macrostate.

We can interpret the bins as the states $x_{i}$ of a discrete random variable $X$, where $p\left(X=x_{i}\right)=p_{i}$. The entropy of the random variable $X$ is then

$$
\mathrm{H}[p]=-\sum_{i} p\left(x_{i}\right) \ln p\left(x_{i}\right)
$$

Distributions $p\left(x_{i}\right)$ that are sharply peaked around a few values will have a relatively low entropy, whereas those that are spread more evenly across many values will have higher entropy, as illustrated in Figure 2.14.

Because $0 \leqslant p_{i} \leqslant 1$, the entropy is non-negative, and it will equal its minimum value of 0 when one of the $p_{i}=1$ and all other $p_{j \neq i}=0$. The maximum entropy Appendix $C$ configuration can be found by maximizing $\mathrm{H}$ using a Lagrange multiplier to enforce the normalization constraint on the probabilities. Thus, we maximize

$$
\widetilde{\mathrm{H}}=-\sum_{i} p\left(x_{i}\right) \ln p\left(x_{i}\right)+\lambda\left(\sum_{i} p\left(x_{i}\right)-1\right)
$$


![](https://cdn.mathpix.com/cropped/2024_05_10_86a2845941e286ae4e26g-1.jpg?height=648&width=1510&top_left_y=272&top_left_x=134

ChatGPT figure/image summary: The image shows two histograms representing two different probability distributions over 30 bins. Each histogram visualizes the probability distribution of a discrete random variable by depicting the relative frequencies of the variable falling within each bin. The left histogram is more concentrated around fewer bins with a peak at one particular bin, indicating a distribution with a lower degree of spread, and it has an associated entropy (H) of 1.77. The right histogram appears more spread out across many bins, suggesting a more uniform distribution of probabilities, and has a higher entropy value of 3.09. The histograms serve to illustrate that distributions that are more evenly spread across a wide range of values will have higher entropy, supporting the text's explanation of entropy as a measure of the spread or uncertainty in a probability distribution.)

Figure 2.14 Histograms of two probability distributions over 30 bins illustrating the higher value of the entropy $\mathrm{H}$ for the broader distribution. The largest entropy would arise from a uniform distribution which would give $\mathrm{H}=-\ln (1 / 30)=3.40$.

Exercise 2.22 Exercise 2.23 from which we find that all of the $p\left(x_{i}\right)$ are equal and are given by $p\left(x_{i}\right)=1 / M$ where $M$ is the total number of states $x_{i}$. The corresponding value of the entropy is then $\mathrm{H}=\ln M$. This result can also be derived from Jensen's inequality (to be discussed shortly). To verify that the stationary point is indeed a maximum, we can evaluate the second derivative of the entropy, which gives

$$
\frac{\partial \widetilde{\mathrm{H}}}{\partial p\left(x_{i}\right) \partial p\left(x_{j}\right)}=-I_{i j} \frac{1}{p_{i}}
$$

where $I_{i j}$ are the elements of the identity matrix. We see that these values are all negative and, hence, the stationary point is indeed a maximum.

\subsection*{2.5.3 Differential entropy}

We can extend the definition of entropy to include distributions $p(x)$ over continuous variables $x$ as follows. First divide $x$ into bins of width $\Delta$. Then, assuming that $p(x)$ is continuous, the mean value theorem (Weisstein, 1999) tells us that, for each such bin, there must exist a value $x_{i}$ in the range $i \Delta \leqslant x_{i} \leqslant(i+1) \Delta$ such that

$$
\int_{i \Delta}^{(i+1) \Delta} p(x) \mathrm{d} x=p\left(x_{i}\right) \Delta
$$

We can now quantize the continuous variable $x$ by assigning any value $x$ to the value $x_{i}$ whenever $x$ falls in the $i$ th bin. The probability of observing the value $x_{i}$ is then

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

Figure 2.2 Probability can be viewed either as a frequency associated with a repeatable event or as a quantification of uncertainty. A bent coin can be used to illustrate the difference, as discussed in the text.

![](https://cdn.mathpix.com/cropped/2024_05_10_1ff7c1baa6bdceecd13ag-1.jpg?height=244&width=354&top_left_y=222&top_left_x=917

ChatGPT figure/image summary: The image is of a bent coin. It appears to be a regular coin that has been physically distorted to no longer be flat, which might affect its dynamics when flipped. The context provided discusses the use of probability to understand uncertain outcomes and uses the bent coin to illustrate the difference between probability as a frequency of events and probability as a quantification of uncertainty — a perspective that is central to Bayesian probability. The coin in the image serves as a visual aid for these conceptual discussions in the paper.)

$60 \%$

![](https://cdn.mathpix.com/cropped/2024_05_10_1ff7c1baa6bdceecd13ag-1.jpg?height=239&width=342&top_left_y=230&top_left_x=1302

ChatGPT figure/image summary: The image depicts a bent or deformed coin. The coin appears to have a convex curvature, and the sides are not visible in this perspective, so it's unclear which side represents heads and which represents tails. The context provided suggests that this image is used to illustrate the concept of probability, both in terms of frequency of repeatable events and in the Bayesian sense as a quantification of uncertainty. The text discusses how one might approach betting on the outcome of a coin flip with such a bent coin, noting that without further information, one might assume a 50% probability for heads or tails, highlighting the use of probability to manage uncertainty in situations that are not repeatable events.)

$40 \%$

know which side is heads and which is tails. If asked to take a bet on whether the coin will land heads or tails when flipped, then symmetry suggests that our bet should be based on the assumption that the probability of seeing heads is 0.5 , and indeed a more careful analysis shows that, in the absence of any additional information, this is indeed the rational choice. Here we are using probabilities in a more general sense than simply the frequency of events. Whether the convex side of the coin is heads or tails is not itself a repeatable event, it is simply unknown. The use of probability as a

Section 2.6 quantification of uncertainty is the Bayesian perspective and is more general in that it includes frequentist probability as a special case. We can learn about which side of the coin is heads if we are given results from a sequence of coin flips by making Exercise 2.40 use of Bayesian reasoning. The more results we observe, the lower our uncertainty as to which side of the coin is which.

Having introduced the concept of probability informally, we turn now to a more detailed exploration of probabilities and discuss how to use them quantitatively. Concepts developed in the remainder of this chapter will form a core foundation for many of the topics discussed throughout the book.

\title{
2.1. The Rules of Probability
}

In this section we will derive two simple rules that govern the behaviour of probabilities. However, in spite of their apparent simplicity, these rules will prove to be very powerful and widely applicable. We will motivate the rules of probability by first introducing a simple example.

\subsection*{2.1.1 A medical screening example}

Consider the problem of screening a population in order to provide early detection of cancer, and let us suppose that $1 \%$ of the population actually have cancer. Ideally our test for cancer would give a positive result for anyone who has cancer and a negative result for anyone who does not. However, tests are not perfect, so we will suppose that when the test is given to people who are free of cancer, $3 \%$ of them will test positive. These are known as false positives. Similarly, when the test is given to people who do have cancer, $10 \%$ of them will test negative. These are called false negatives. The various error rates are illustrated in Figure 2.3.

Given this information, we might ask the following questions: (1) 'If we screen the population, what is the probability that someone will test positive?', (2) 'If some-

Figure 2.15 A convex function $f(x)$ is one for which every chord (shown in blue) lies on or above the function (shown in red).

![](https://cdn.mathpix.com/cropped/2024_05_10_0551caecedc5cc817095g-1.jpg?height=555&width=653&top_left_y=216&top_left_x=1007

ChatGPT figure/image summary: The image illustrates a graph that is being used to describe the property of a convex function. The graph has two axes, an x-axis labeled "x" and a y-axis that is not labeled but is implied to measure the function value "f(x)." On the graph, there is a curve representing the function f(x), which is shown in red. The curve has a convex shape, meaning it curves upwards.

Additionally, there are two vertical dashed lines in green that intersect the x-axis at points labeled "a" and "b," respectively. These points correspond to values where the curve is defined and are used to form a "chord," which is a straight line in blue connecting the points on the curve directly above "a" and "b." The chord represents a linear interpolation between these two points on the function.

The property of convexity is highlighted by the fact that the blue chord always lies above or on the red convex curve between the points "a" and "b." This characteristic is key to identifying a function as convex, as described in the provided text. Additionally, there is a point "x" between "a" and "b" on the x-axis, which helps show that for any point on the function between "a" and "b," the value of the function is always below the line segment (or chord) that connects the values of the function at "a" and "b." 

The illustration serves as a visual aid in understanding the definition and properties of convex functions, a concept discussed in the text excerpt from the paper. Convex functions are a fundamental concept in mathematics and are particularly important in the field of optimization.)

is given by $\lambda f(a)+(1-\lambda) f(b)$, and the corresponding value of the function is $f(\lambda a+(1-\lambda) b)$. Convexity then implies

$$
f(\lambda a+(1-\lambda) b) \leqslant \lambda f(a)+(1-\lambda) f(b)
$$

This is equivalent to the requirement that the second derivative of the function be

Exercise 2.32 everywhere positive. Examples of convex functions are $x \ln x$ (for $x>0$ ) and $x^{2}$. A function is called strictly convex if the equality is satisfied only for $\lambda=0$ and $\lambda=1$. If a function has the opposite property, namely that every chord lies on or below the function, it is called concave, with a corresponding definition for strictly concave. If a function $f(x)$ is convex, then $-f(x)$ will be concave.

Exercise 2.33

Using the technique of proof by induction, we can show from (2.101) that a convex function $f(x)$ satisfies

$$
f\left(\sum_{i=1}^{M} \lambda_{i} x_{i}\right) \leqslant \sum_{i=1}^{M} \lambda_{i} f\left(x_{i}\right)
$$

where $\lambda_{i} \geqslant 0$ and $\sum_{i} \lambda_{i}=1$, for any set of points $\left\{x_{i}\right\}$. The result (2.102) is known as Jensen's inequality. If we interpret the $\lambda_{i}$ as the probability distribution over a discrete variable $x$ taking the values $\left\{x_{i}\right\}$, then (2.102) can be written

$$
f(\mathbb{E}[x]) \leqslant \mathbb{E}[f(x)]
$$

where $\mathbb{E}[\cdot]$ denotes the expectation. For continuous variables, Jensen's inequality takes the form

$$
f\left(\int \mathbf{x} p(\mathbf{x}) \mathrm{d} \mathbf{x}\right) \leqslant \int f(\mathbf{x}) p(\mathbf{x}) \mathrm{d} \mathbf{x}
$$

We can apply Jensen's inequality in the form (2.104) to the Kullback-Leibler divergence (2.100) to give

$$
\mathrm{KL}(p \| q)=-\int p(\mathbf{x}) \ln \left\{\frac{q(\mathbf{x})}{p(\mathbf{x})}\right\} \mathrm{d} \mathbf{x} \geqslant-\ln \int q(\mathbf{x}) \mathrm{d} \mathbf{x}=0
$$

where we have used $-\ln x$ is a convex function, together with the normalization condition $\int q(\mathbf{x}) \mathrm{d} \mathbf{x}=1$. In fact, $-\ln x$ is a strictly convex function, so the equality will hold if, and only if, $q(\mathbf{x})=p(\mathbf{x})$ for all $\mathbf{x}$. Thus, we can interpret the KullbackLeibler divergence as a measure of the dissimilarity of the two distributions $p(\mathbf{x})$ and $q(\mathbf{x})$.

We see that there is an intimate relationship between data compression and density estimation (i.e., the problem of modelling an unknown probability distribution) because the most efficient compression is achieved when we know the true distribution. If we use a distribution that is different from the true one, then we must necessarily have a less efficient coding, and on average the additional information that must be transmitted is (at least) equal to the Kullback-Leibler divergence between the two distributions.

Suppose that data is being generated from an unknown distribution $p(\mathbf{x})$ that we wish to model. We can try to approximate this distribution using some parametric distribution $q(\mathbf{x} \mid \boldsymbol{\theta})$, governed by a set of adjustable parameters $\boldsymbol{\theta}$. One way to determine $\boldsymbol{\theta}$ is to minimize the Kullback-Leibler divergence between $p(\mathbf{x})$ and $q(\mathbf{x} \mid \boldsymbol{\theta})$ with respect to $\boldsymbol{\theta}$. We cannot do this directly because we do not know $p(\mathbf{x})$. Suppose, however, that we have observed a finite set of training points $\mathbf{x}_{n}$, for $n=1, \ldots, N$, drawn from $p(\mathbf{x})$. Then the expectation with respect to $p(\mathbf{x})$ can be approximated by a finite sum over these points, using (2.40), so that

$$
\mathrm{KL}(p \| q) \simeq \frac{1}{N} \sum_{n=1}^{N}\left\{-\ln q\left(\mathbf{x}_{n} \mid \boldsymbol{\theta}\right)+\ln p\left(\mathbf{x}_{n}\right)\right\}
$$

The second term on the right-hand side of (2.106) is independent of $\boldsymbol{\theta}$, and the first term is the negative log likelihood function for $\boldsymbol{\theta}$ under the distribution $q(\mathbf{x} \mid \boldsymbol{\theta})$ evaluated using the training set. Thus, we see that minimizing this Kullback-Leibler divergence is equivalent to maximizing the log likelihood function.

\title{
2.5.6 Conditional entropy
}

Now consider the joint distribution between two sets of variables $\mathbf{x}$ and $\mathbf{y}$ given by $p(\mathbf{x}, \mathbf{y})$ from which we draw pairs of values of $\mathbf{x}$ and $\mathbf{y}$. If a value of $\mathbf{x}$ is already known, then the additional information needed to specify the corresponding value of $\mathbf{y}$ is given by $-\ln p(\mathbf{y} \mid \mathbf{x})$. Thus the average additional information needed to specify y can be written as

$$
\mathrm{H}[\mathbf{y} \mid \mathbf{x}]=-\iint p(\mathbf{y}, \mathbf{x}) \ln p(\mathbf{y} \mid \mathbf{x}) \mathrm{d} \mathbf{y} \mathrm{d} \mathbf{x}
$$

which is called the conditional entropy of $\mathbf{y}$ given $\mathbf{x}$. It is easily seen, using the product rule, that the conditional entropy satisfies the relation:

$$
\mathrm{H}[\mathbf{x}, \mathbf{y}]=\mathrm{H}[\mathbf{y} \mid \mathbf{x}]+\mathrm{H}[\mathbf{x}]
$$

where $\mathrm{H}[\mathbf{x}, \mathbf{y}]$ is the differential entropy of $p(\mathbf{x}, \mathbf{y})$ and $\mathrm{H}[\mathbf{x}]$ is the differential entropy of the marginal distribution $p(\mathbf{x})$. Thus, the information needed to describe $\mathbf{x}$ and $\mathbf{y}$ is given by the sum of the information needed to describe $\mathbf{x}$ alone plus the additional information required to specify $\mathbf{y}$ given $\mathbf{x}$.

\title{
2.5.7 Mutual information
}

When two variables $\mathbf{x}$ and $\mathbf{y}$ are independent, their joint distribution will factorize into the product of their marginals $p(\mathbf{x}, \mathbf{y})=p(\mathbf{x}) p(\mathbf{y})$. If the variables are not independent, we can gain some idea of whether they are 'close' to being independent by considering the Kullback-Leibler divergence between the joint distribution and the product of the marginals, given by

$$
\begin{aligned}
\mathrm{I}[\mathbf{x}, \mathbf{y}] & \equiv \mathrm{KL}(p(\mathbf{x}, \mathbf{y}) \| p(\mathbf{x}) p(\mathbf{y})) \\
& =-\iint p(\mathbf{x}, \mathbf{y}) \ln \left(\frac{p(\mathbf{x}) p(\mathbf{y})}{p(\mathbf{x}, \mathbf{y})}\right) \mathrm{d} \mathbf{x} \mathrm{d} \mathbf{y}
\end{aligned}
$$

which is called the mutual information between the variables $\mathbf{x}$ and $\mathbf{y}$. From the properties of the Kullback-Leibler divergence, we see that $I[\mathbf{x}, \mathbf{y}] \geqslant 0$ with equality if, and only if, $\mathbf{x}$ and $\mathbf{y}$ are independent. Using the sum and product rules of probability, we see that the mutual information is related to the conditional entropy

Exercise 2.38 through

$$
\mathrm{I}[\mathbf{x}, \mathbf{y}]=\mathrm{H}[\mathbf{x}]-\mathrm{H}[\mathbf{x} \mid \mathbf{y}]=\mathrm{H}[\mathbf{y}]-\mathrm{H}[\mathbf{y} \mid \mathbf{x}]
$$

Thus, the mutual information represents the reduction in the uncertainty about $\mathrm{x}$ by virtue of being told the value of $\mathbf{y}$ (or vice versa). From a Bayesian perspective, we can view $p(\mathbf{x})$ as the prior distribution for $\mathbf{x}$ and $p(\mathbf{x} \mid \mathbf{y})$ as the posterior distribution after we have observed new data $\mathbf{y}$. The mutual information therefore represents the reduction in uncertainty about $\mathbf{x}$ as a consequence of the new observation $\mathbf{y}$.

\subsection*{2.6. Bayesian Probabilities}

When we considered the bent coin in Figure 2.2, we introduced the concept of probability in terms of the frequencies of random, repeatable events, such as the probability of the coin landing concave side up. We will refer to this as the classical or frequentist interpretation of probability. We also introduced the more general Bayesian view, in which probabilities provide a quantification of uncertainty. In this case, our uncertainty is whether the concave side of the coin is heads or tails.

The use of probability to represent uncertainty is not an ad hoc choice but is inevitable if we are to respect common sense while making rational and coherent inferences. For example, Cox (1946) showed that if numerical values are used to represent degrees of belief, then a simple set of axioms encoding common sense properties of such beliefs leads uniquely to a set of rules for manipulating degrees of belief that are equivalent to the sum and product rules of probability. It is therefore natural to refer to these quantities as (Bayesian) probabilities.

For the bent coin we assumed, in the absence of further information, that the probability of the concave side of the coin being heads is 0.5 . Now suppose we are told the results of flipping the coin a few times. Intuitively, it seems that this should provide us with some information as to whether the concave side is heads. For instance, suppose we see many more flips that land tails than land heads. Given

Exercise 2.40

Section 3.1.2

Section 1.2 that the coin is more likely to land concave side up, this provides evidence to suggest that the concave side is more likely to be tails. In fact, this intuition is correct, and furthermore, we can quantify this using the rules of probability. Bayes' theorem now acquires a new significance, because it allows us to convert the prior probability for the concave side being heads into a posterior probability by incorporating the data provided by the coin flips. Moreover, this process is iterative, meaning the posterior probability becomes the prior for incorporating data from further coin flips.

One aspect of the Bayesian viewpoint is that the inclusion of prior knowledge arises naturally. Suppose, for instance, that a fair-looking coin is tossed three times and lands heads each time. The maximum likelihood estimate of the probability of landing heads would give 1, implying that all future tosses will land heads! By contrast, a Bayesian approach with any reasonable prior will lead to a less extreme conclusion.

\subsection*{2.6.1 Model parameters}

The Bayesian perspective provides valuable insights into several aspects of machine learning, and we can illustrate these using the sine curve regression example. Here we denote the training data set by $\mathcal{D}$. We have already seen in the context of linear regression that the parameters can be chosen using maximum likelihood, in which $\mathbf{w}$ is set to the value that maximizes the likelihood function $p(\mathcal{D} \mid \mathbf{w})$. This corresponds to choosing the value of $\mathbf{w}$ for which the probability of the observed data set is maximized. In the machine learning literature, the negative log of the likelihood function is called an error function. Because the negative logarithm is a monotonically decreasing function, maximizing the likelihood is equivalent to minimizing the error. This leads to a specific choice of parameter values, denoted $\mathbf{w}_{\mathrm{ML}}$, which are then used to make predictions for new data.

We have seen that different choices of training data set, for example containing different numbers of data points, give rise to different solutions for $\mathbf{w}_{\mathrm{ML}}$. From a Bayesian perspective, we can also use the machinery of probability theory to describe this uncertainty in the model parameters. We can capture our assumptions about $\mathbf{w}$, before observing the data, in the form of a prior probability distribution $p(\mathbf{w})$. The effect of the observed data $\mathcal{D}$ is expressed through the likelihood function $p(\mathcal{D} \mid \mathbf{w})$, and Bayes' theorem now takes the form

$$
p(\mathbf{w} \mid \mathcal{D})=\frac{p(\mathcal{D} \mid \mathbf{w}) p(\mathbf{w})}{p(\mathcal{D})}
$$

which allows us to evaluate the uncertainty in w after we have observed $\mathcal{D}$ in the form of the posterior probability $p(\mathbf{w} \mid \mathcal{D})$.

It is important to emphasize that the quantity $p(\mathcal{D} \mid \mathbf{w})$ is called the likelihood function when it is viewed as a function of the parameter vector $\mathbf{w}$, and it expresses how probable the observed data set is for different values of w. Note that the likelihood $p(\mathcal{D} \mid \mathbf{w})$ is not a probability distribution over $\mathbf{w}$, and its integral with respect to $\mathbf{w}$ does not (necessarily) equal one.

Given this definition of likelihood, we can state Bayes' theorem in words:

Section 1.2.5

Exercise 2.41 where all of these quantities are viewed as functions of $\mathbf{w}$. The denominator in (2.111) is the normalization constant, which ensures that the posterior distribution on the left-hand side is a valid probability density and integrates to one. Indeed, by integrating both sides of (2.111) with respect to $\mathrm{w}$, we can express the denominator in Bayes' theorem in terms of the prior distribution and the likelihood function:

$$
p(\mathcal{D})=\int p(\mathcal{D} \mid \mathbf{w}) p(\mathbf{w}) \mathrm{d} \mathbf{w}
$$

In both the Bayesian and frequentist paradigms, the likelihood function $p(\mathcal{D} \mid \mathbf{w})$ plays a central role. However, the manner in which it is used is fundamentally different in the two approaches. In a frequentist setting, $\mathbf{w}$ is considered to be a fixed parameter, whose value is determined by some form of 'estimator', and error bars on this estimate are determined (conceptually, at least) by considering the distribution of possible data sets $\mathcal{D}$. By contrast, from the Bayesian viewpoint there is only a single data set $\mathcal{D}$ (namely the one that is actually observed), and the uncertainty in the parameters is expressed through a probability distribution over $\mathbf{w}$.

\subsection*{2.6.2 Regularization}

We can use this Bayesian perspective to gain insight into the technique of regularization that was used in the sine curve regression example to reduce over-fitting. Instead of choosing the model parameters by maximizing the likelihood function with respect to $\mathrm{w}$, we can maximize the posterior probability (2.111). This technique is called the maximum a posteriori estimate, or simply MAP estimate. Equivalently, we can minimize the negative $\log$ of the posterior probability. Taking negative logs of both sides of (2.111), we have

$$
-\ln p(\mathbf{w} \mid \mathcal{D})=-\ln p(\mathcal{D} \mid \mathbf{w})-\ln p(\mathbf{w})+\ln p(\mathcal{D})
$$

The first term on the right-hand side of (2.114) is the usual log likelihood. The third term can be omitted since it does not depend on $\mathbf{w}$. The second term takes the form of a function of $\mathbf{w}$, which is added to the log likelihood, and we can recognize this as a form of regularization. To make this more explicit, suppose we choose the prior distribution $p(\mathbf{w})$ to be the product of independent zero-mean Gaussian distributions for each of the elements of $\mathbf{w}$ such that each has the same variance $s^{2}$ so that

$$
p(\mathbf{w} \mid s)=\prod_{i=0}^{M} \mathcal{N}\left(w_{i} \mid 0, s^{2}\right)=\prod_{i=0}^{M}\left(\frac{1}{2 \pi s^{2}}\right)^{1 / 2} \exp \left\{-\frac{w_{i}^{2}}{2 s^{2}}\right\}
$$

Substituting into (2.114), we obtain

$$
-\ln p(\mathbf{w} \mid \mathcal{D})=-\ln p(\mathcal{D} \mid \mathbf{w})+\frac{1}{2 s^{2}} \sum_{i=0}^{M} w_{i}^{2}+\text { const. }
$$

If we consider the particular case of the linear regression model whose log likelihood is given by (2.66), then we find that maximizing the posterior distribution is equivalent to minimizing the function

$$
E(\mathbf{w})=\frac{1}{2 \sigma^{2}} \sum_{n=1}^{N}\left\{y\left(x_{n}, \mathbf{w}\right)-t_{n}\right\}^{2}+\frac{1}{2 s^{2}} \mathbf{w}^{\mathrm{T}} \mathbf{w}
$$

We see that this takes the form of the regularized sum-of-squares error function encountered earlier in the form (1.4).

\title{
2.6.3 Bayesian machine learning
}

The Bayesian perspective has allowed us to motivate the use of regularization and to derive a specific form for the regularization term. However, the use of Bayes' theorem alone does not constitute a truly Bayesian treatment of machine learning since it is still finding a single solution for $\mathbf{w}$ and does not therefore take account of uncertainty in the value of $\mathbf{w}$. Suppose we have a training data set $\mathcal{D}$ and our goal is to predict some target variable $t$ given a new input value $x$. We are therefore interested in the distribution of $t$ given both $x$ and $\mathcal{D}$. From the sum and product rules of probability, we have

$$
p(t \mid x, \mathcal{D})=\int p(t \mid x, \mathbf{w}) p(\mathbf{w} \mid \mathcal{D}) \mathrm{d} \mathbf{w}
$$

We see that the prediction is obtained by taking a weighted average $p(t \mid x, \mathbf{w})$ over all possible values of $\mathbf{w}$ in which the weighting function is given by the posterior probability distribution $p(\mathbf{w} \mid \mathcal{D})$. The key difference that distinguishes Bayesian methods is this integration over the space of parameters. By contrast, conventional frequentist methods use point estimates for parameters obtained by optimizing a loss function such as a regularized sum-of-squares.

This fully Bayesian treatment of machine learning offers some powerful in-

Section 1.2

Section 9.6 sights. For example, the problem of over-fitting, encountered earlier in the context of polynomial regression, is an example of a pathology arising from the use of maximum likelihood, and does not arise when we marginalize over parameters using the Bayesian approach. Similarly, we may have multiple potential models that we could use to solve a given problem, such as polynomials of different orders in the regression example. A maximum likelihood approach simply picks the model that gives the highest probability of the data, but this favours ever more complex models, leading to over-fitting. A fully Bayesian treatment involves averaging over all possible models, with the contribution of each model weighted by its posterior probability. Moreover, this probability is typically highest for models of intermediate complexity. Very simple models (such as polynomials of low order) have low probability as they are unable to fit the data well, whereas very complex models (such as polynomials of very high order) also have low probability because the Bayesian integration over parameters automatically and elegantly penalizes complexity. For a comprehensive overview of Bayesian methods applied to machine learning, including neural networks, see Bishop (2006).

Unfortunately, there is a major drawback with the Bayesian framework, and this is apparent in (2.118), which involves integrating over the space of parameters. Modern deep learning models can have millions or billions of parameters and even simple approximations to such integrals are typically infeasible. In fact, given a

limited compute budget and an ample source of training data, it will often be better to apply maximum likelihood techniques, generally augmented with one or more forms of regularization, to a large neural network rather than apply a Bayesian treatment to a much smaller model.

\title{
Exercises
}

2.1 ( $\star$ ) In the cancer screening example, we used a prior probability of cancer of $p(C=$ $1)=0.01$. In reality, the prevalence of cancer is generally very much lower. Consider a situation in which $p(C=1)=0.001$, and recompute the probability of having cancer given a positive test $p(C=1 \mid T=1)$. Intuitively, the result can appear surprising to many people since the test seems to have high accuracy and yet a positive test still leads to a low probability of having cancer.

2.2 ( $\star$ ) Deterministic numbers satisfy the property of transitivity, so that if $x>y$ and $y>z$ then it follows that $x>z$. When we go to random numbers, however, this property need no longer apply. Figure 2.16 shows a set of four cubical dice that have been arranged in a cyclic order. Show that each of the four dice has a $2 / 3$ probability of rolling a higher number than the previous die in the cycle. Such dice are known as non-transitive dice, and the specific examples shown here are called Efron dice.

Figure 2.16 An example of non-transitive cubical dice, in which each die has been 'flattened' to reveal the numbers on each of the faces. The dice have been arranged in a cycle, such that each die has a $2 / 3$ probability of rolling a higher number than the previous die in the cycle.

![](https://cdn.mathpix.com/cropped/2024_05_10_94469b00ff35a4fb5aa3g-1.jpg?height=503&width=457&top_left_y=1080&top_left_x=1071

ChatGPT figure/image summary: This image shows a set of four differently colored cubical dice, each with numbers on their faces. The die colors are orange, red, blue, and green, and they are arranged in a circular order with arrows between them indicating a cycle. Each die has a unique distribution of numbers:

- The orange die has the numbers 3, 3, 3, 3, 3, and 3.
- The red die has 2, 2, 2, 6, 6, and 6.
- The blue die has 4, 4, 4, 0, 0, and 0.
- The green die has 5, 5, 5, 1, 1, and 1.

The circular arrangement suggests that each die is meant to be "competing" against the next one in the cycle (orange against red, red against blue, blue against green, and green against orange). The numbers are assigned in such a way that each die has a 2/3 probability of rolling a higher number than the preceding die in the cycle, illustrating the concept of non-transitive dice as referred to in Exercise 2.2 of the paper. This property is known as non-transitivity because it contradicts the transitive property of conventional dice, where if die A typically rolls higher than die B, and die B typically rolls higher than die C, then die A should also typically roll higher than die C, which is not the case with these dice.)

2.3 (*) Consider a variable $y$ given by the sum of two independent random variables $\mathbf{y}=\mathbf{u}+\mathbf{v}$ where $\mathbf{u} \sim p_{\mathbf{u}}(\mathbf{u})$ and $\mathbf{v} \sim p_{\mathbf{v}}(\mathbf{v})$. Show that the distribution $p_{\mathbf{y}}(\mathbf{y})$ is given by

$$
p(\mathbf{y})=\int p_{\mathbf{u}}(\mathbf{u}) p_{\mathbf{v}}(\mathbf{y}-\mathbf{u}) \mathrm{d} \mathbf{u}
$$

This is known as the convolution of $p_{\mathbf{u}}(\mathbf{u})$ and $p_{\mathbf{v}}(\mathbf{v})$.

$2.4(\star \star)$ Verify that the uniform distribution (2.33) is correctly normalized, and find expressions for its mean and variance.

$2.5(\star \star)$ Verify that the exponential distribution (2.34) and the Laplace distribution (2.35) are correctly normalized.

Figure 2.3 Illustration of the accuracy of a cancer test. Out of every hundred people taking the test who do not have cancer, shown on the left, on average three will test positive. For those who have cancer, shown on the right, out of every hundred people taking the test, on average 90 will test positive.

![](https://cdn.mathpix.com/cropped/2024_05_10_103c75cae03fc6403b87g-1.jpg?height=564&width=745&top_left_y=216&top_left_x=912

ChatGPT figure/image summary: The image depicts an illustration representing the accuracy of a cancer test. On the left side labeled "No Cancer," there are many blue figures to represent individuals who do not have cancer, with a few red figures interspersed among them to represent false positives in the test -- individuals who tested positive but do not have cancer. On the right side labeled "Cancer," there are red figures representing individuals who have cancer, most of which represent true positives -- correctly identified cases of cancer by the test. The purpose of the illustration is to visually convey the concept of the accuracy of the cancer test, highlighting how many individuals are correctly identified as having or not having cancer and pointing out the occurrence of false-positive test results.)

one receives a positive test result, what is the probability that they actually have cancer?'. We could answer such questions by working through the cancer screening case in detail. Instead, however, we will pause our discussion of this specific example and first derive the general rules of probability, known as the sum rule of probability and the product rule. We will then illustrate the use of these rules by answering our two questions.

\title{
2.1.2 The sum and product rules
}

To derive the rules of probability, consider the slightly more general example shown in Figure 2.4 involving two variables $X$ and $Y$. In our cancer example, $X$ could represent the presence or absence of cancer, and $Y$ could be a variable denoting the outcome of the test. Because the values of these variables can vary from one person to another in a way that is generally unknown, they are called random variables or stochastic variables. We will suppose that $X$ can take any of the values $x_{i}$ where $i=1, \ldots, L$ and that $Y$ can take the values $y_{j}$ where $j=1, \ldots, M$. Consider a total of $N$ trials in which we sample both of the variables $X$ and $Y$, and let the number of such trials in which $X=x_{i}$ and $Y=y_{j}$ be $n_{i j}$. Also, let the number of trials in which $X$ takes the value $x_{i}$ (irrespective of the value that $Y$ takes) be denoted by $c_{i}$, and similarly let the number of trials in which $Y$ takes the value $y_{j}$ be denoted by $r_{j}$.

The probability that $X$ will take the value $x_{i}$ and $Y$ will take the value $y_{j}$ is written $p\left(X=x_{i}, Y=y_{j}\right)$ and is called the joint probability of $X=x_{i}$ and $Y=y_{j}$. It is given by the number of points falling in the cell $i, j$ as a fraction of the total number of points, and hence

$$
p\left(X=x_{i}, Y=y_{j}\right)=\frac{n_{i j}}{N}
$$

Here we are implicitly considering the limit $N \rightarrow \infty$. Similarly, the probability that $X$ takes the value $x_{i}$ irrespective of the value of $Y$ is written as $p\left(X=x_{i}\right)$ and is

Figure 2.4 We can derive the sum and product rules of probability by considering a random variable $X$, which takes the values $\left\{x_{i}\right\}$ where $i=1, \ldots, L$, and a second random variable $Y$, which takes the values $\left\{y_{j}\right\}$ where $j=$ $1, \ldots, M$. In this illustration, we have $L=5$ and $M=3$. If we consider the total number $N$ of instances of these variables, then we denote the number of instances where $X=x_{i}$ and $Y=y_{j}$ by $n_{i j}$, which is the number of instances in the corresponding cell of the array. The number of instances in column $i$, corresponding to $X=x_{i}$, is denoted by $c_{i}$, and the number of instances in row $j$, corresponding to $Y=y_{j}$, is denoted by $r_{j}$.

![](https://cdn.mathpix.com/cropped/2024_05_10_0ac15dbddb7cf99e2d43g-1.jpg?height=361&width=539&top_left_y=215&top_left_x=1113

ChatGPT figure/image summary: The image illustrates the concept of a two-dimensional probability distribution table, corresponding to Figure 2.4 in the provided text. In the context of the probability rules being discussed:

- There are two random variables, \(X\) and \(Y\), which take on \(L\) and \(M\) different values respectively.
- The grid represents the joint occurrences of the values of these two random variables across \(N\) trials. Each cell in the grid corresponds to a particular combination of \(X=x_i\) and \(Y=y_j\), with the number of occurrences denoted as \(n_{ij}\).
- The terms \(c_i\) at the top of the columns represent the total number of occurrences where the random variable \(X\) takes on the value \(x_i\) across all \(N\) instances, regardless of the value of \(Y\).
- The terms \(r_j\) on the right represent the number of occurrences where the random variable \(Y\) takes on the value \(y_j\), again regardless of the value of \(X\).

This illustration would be used to explain how to derive the sum and product rules of probability, eventually leading to a discussion of Bayes' theorem as described in the provided text. The sum rule allows one to find the probability of a single random variable by summing over the probabilities of the joint occurrences of that random variable with all possible values of the other variable. The product rule relates the conditional probability of one variable given the other to the joint probability of both variables and the marginal probability of one variable.)

given by the fraction of the total number of points that fall in column $i$, so that

$$
p\left(X=x_{i}\right)=\frac{c_{i}}{N}
$$

Since $\sum_{i} c_{i}=N$, we see that

$$
\sum_{i=1}^{L} p\left(X=x_{i}\right)=1
$$

and, hence, the probabilities sum to one as required. Because the number of instances in column $i$ in Figure 2.4 is just the sum of the number of instances in each cell of that column, we have $c_{i}=\sum_{j} n_{i j}$ and therefore, from (2.1) and (2.2), we have

$$
p\left(X=x_{i}\right)=\sum_{j=1}^{M} p\left(X=x_{i}, Y=y_{j}\right)
$$

which is the sum rule of probability. Note that $p\left(X=x_{i}\right)$ is sometimes called the marginal probability and is obtained by marginalizing, or summing out, the other variables (in this case $Y$ ).

If we consider only those instances for which $X=x_{i}$, then the fraction of such instances for which $Y=y_{j}$ is written $p\left(Y=y_{j} \mid X=x_{i}\right)$ and is called the conditional probability of $Y=y_{j}$ given $X=x_{i}$. It is obtained by finding the fraction of those points in column $i$ that fall in cell $i, j$ and, hence, is given by

$$
p\left(Y=y_{j} \mid X=x_{i}\right)=\frac{n_{i j}}{c_{i}}
$$

Summing both sides over $j$ and using $\sum_{j} n_{i j}=c_{i}$, we obtain

$$
\sum_{j=1}^{M} p\left(Y=y_{j} \mid X=x_{i}\right)=1
$$

showing that the conditional probabilities are correctly normalized. From (2.1), (2.2), and (2.5), we can then derive the following relationship:

$$
\begin{aligned}
p\left(X=x_{i}, Y=y_{j}\right) & =\frac{n_{i j}}{N}=\frac{n_{i j}}{c_{i}} \cdot \frac{c_{i}}{N} \\
& =p\left(Y=y_{j} \mid X=x_{i}\right) p\left(X=x_{i}\right)
\end{aligned}
$$

which is the product rule of probability.

So far, we have been quite careful to make a distinction between a random variable, such as $X$, and the values that the random variable can take, for example $x_{i}$. Thus, the probability that $X$ takes the value $x_{i}$ is denoted $p\left(X=x_{i}\right)$. Although this helps to avoid ambiguity, it leads to a rather cumbersome notation, and in many cases there will be no need for such pedantry. Instead, we may simply write $p(X)$ to denote a distribution over the random variable $X$, or $p\left(x_{i}\right)$ to denote the distribution evaluated for the particular value $x_{i}$, provided that the interpretation is clear from the context.

With this more compact notation, we can write the two fundamental rules of probability theory in the following form:

$$
\begin{array}{cc}
\text { sum rule } & p(X)=\sum_{Y} p(X, Y) \\
\text { product rule } & p(X, Y)=p(Y \mid X) p(X)
\end{array}
$$

Here $p(X, Y)$ is a joint probability and is verbalized as 'the probability of $X$ and $Y^{\prime}$. Similarly, the quantity $p(Y \mid X)$ is a conditional probability and is verbalized as 'the probability of $Y$ given $X$ '. Finally, the quantity $p(X)$ is a marginal probability and is simply 'the probability of $X$ '. These two simple rules form the basis for all of the probabilistic machinery that we will use throughout this book.

\title{
2.1.3 Bayes' theorem
}

From the product rule, together with the symmetry property $p(X, Y)=p(Y, X)$, we immediately obtain the following relationship between conditional probabilities:

$$
p(Y \mid X)=\frac{p(X \mid Y) p(Y)}{p(X)}
$$

which is called Bayes' theorem and which plays an important role in machine learning. Note how Bayes' theorem relates the conditional distribution $p(Y \mid X)$ on the left-hand side of the equation, to the 'reversed' conditional distribution $p(X \mid Y)$ on the right-hand side. Using the sum rule, the denominator in Bayes' theorem can be expressed in terms of the quantities appearing in the numerator:

$$
p(X)=\sum_{Y} p(X \mid Y) p(Y)
$$

Thus, we can view the denominator in Bayes' theorem as being the normalization constant required to ensure that the sum over the conditional probability distribution on the left-hand side of (2.10) over all values of $Y$ equals one.


![](https://cdn.mathpix.com/cropped/2024_05_10_755c14c4a9b1412fbd69g-1.jpg?height=1056&width=1490&top_left_y=260&top_left_x=134

ChatGPT figure/image summary: The image provided is a graphical representation of a joint probability distribution and the related marginal and conditional distributions for two random variables, X and Y. 

In the top left quadrant of the image, we see a scatter plot showing the joint distribution p(X, Y), with 60 data points distributed across nine columns (representing the possible values of X) and two rows (representing the two possible values of Y). Each data point is illustrated as a blue dot, and the graph is divided by red grid lines that separate the different values of X and Y.

In the top right quadrant, there is a bar graph representing the marginal probability distribution of Y, denoted as p(Y). The length of each bar corresponds to the fraction of points in the top left graph for each value of Y. There are two bars indicating the distribution for Y=1 and Y=2.

In the bottom left quadrant, we see another bar graph showing the marginal probability distribution of X, denoted as p(X). This histogram estimates the distribution for the variable X independently of Y, giving us the overall likelihood of each X value regardless of Y.

Finally, in the bottom right quadrant, the image shows a bar graph for the conditional distribution p(X|Y=1), which depicts the likelihood of various X values given that Y=1. This histogram is derived from considering only the bottom row from the scatter plot in the top left graph where Y=1 and ignoring the data points where Y=2.)

Figure 2.5 An illustration of a distribution over two variables, $X$, which takes nine possible values, and $Y$, which takes two possible values. The top left figure shows a sample of 60 points drawn from a joint probability distribution over these variables. The remaining figures show histogram estimates of the marginal distributions $p(X)$ and $p(Y)$, as well as the conditional distribution $p(X \mid Y=1)$ corresponding to the bottom row in the top left figure.

In Figure 2.5, we show a simple example involving a joint distribution over two

Section 3.5.1 variables to illustrate the concept of marginal and conditional distributions. Here a finite sample of $N=60$ data points has been drawn from the joint distribution and is shown in the top left. In the top right is a histogram of the fractions of data points having each of the two values of $Y$. From the definition of probability, these fractions would equal the corresponding probabilities $p(Y)$ in the limit when the sample size $N \rightarrow \infty$. We can view the histogram as a simple way to model a probability distribution given only a finite number of points drawn from that distribution. The remaining two plots in Figure 2.5 show the corresponding histogram estimates of $p(X)$ and $p(X \mid Y=1)$.

\title{
2.1.4 Medical screening revisited
}

Let us now return to our cancer screening example and apply the sum and product rules of probability to answer our two questions. For clarity, when working through this example, we will once again be explicit about distinguishing between the random variables and their instantiations. We will denote the presence or absence of cancer by the variable $C$, which can take two values: $C=0$ corresponds to 'no cancer' and $C=1$ corresponds to 'cancer'. We have assumed that one person in a hundred in the population has cancer, and so we have

$$
\begin{aligned}
& p(C=1)=1 / 100 \\
& p(C=0)=99 / 100
\end{aligned}
$$

respectively. Note that these satisfy $p(C=0)+p(C=1)=1$.

Now let us introduce a second random variable $T$ representing the outcome of a screening test, where $T=1$ denotes a positive result, indicative of cancer, and $T=0$ a negative result, indicative of the absence of cancer. As illustrated in Figure 2.3, we know that for those who have cancer the probability of a positive test result is $90 \%$, while for those who do not have cancer the probability of a positive test result is $3 \%$. We can therefore write out all four conditional probabilities:

$$
\begin{aligned}
p(T=1 \mid C=1) & =90 / 100 \\
p(T=0 \mid C=1) & =10 / 100 \\
p(T=1 \mid C=0) & =3 / 100 \\
p(T=0 \mid C=0) & =97 / 100
\end{aligned}
$$

Again, note that these probabilities are normalized so that

$$
p(T=1 \mid C=1)+p(T=0 \mid C=1)=1
$$

and similarly

$$
p(T=1 \mid C=0)+p(T=0 \mid C=0)=1
$$

We can now use the sum and product rules of probability to answer our first question and evaluate the overall probability that someone who is tested at random will have a positive test result:

$$
\begin{aligned}
p(T=1) & =p(T=1 \mid C=0) p(C=0)+p(T=1 \mid C=1) p(C=1) \\
& =\frac{3}{100} \times \frac{99}{100}+\frac{90}{100} \times \frac{1}{100}=\frac{387}{10,000}=0.0387
\end{aligned}
$$

We see that if a person is tested at random there is a roughly $4 \%$ chance that the test will be positive even though there is a $1 \%$ chance that they actually have cancer. From this it follows, using the sum rule, that $p(T=0)=1-387 / 10,000=$ $9613 / 10,000=0.9613$ and, hence, there is a roughly $96 \%$ chance that the do not have cancer.

Now consider our second question, which is the one that is of particular interest to a person being screened: if a test is positive, what is the probability that the person

has cancer? This requires that we evaluate the probability of cancer conditional on the outcome of the test, whereas the probabilities in (2.14) to (2.17) give the probability distribution over the test outcome conditioned on whether the person has cancer. We can solve the problem of reversing the conditional probability by using Bayes' theorem (2.10) to give

$$
\begin{aligned}
p(C=1 \mid T=1) & =\frac{p(T=1 \mid C=1) p(C=1)}{p(T=1)} \\
& =\frac{90}{100} \times \frac{1}{100} \times \frac{10,000}{387}=\frac{90}{387} \simeq 0.23
\end{aligned}
$$

so that if a person is tested at random and the test is positive, there is a $23 \%$ probability that they actually have cancer. From the sum rule, it then follows that $p(C=$ $0 \mid T=1)=1-90 / 387=297 / 387 \simeq 0.77$, which is a $77 \%$ chance that they do not have cancer.

\title{
2.1.5 Prior and posterior probabilities
}

We can use the cancer screening example to provide an important interpretation of Bayes' theorem as follows. If we had been asked whether someone is likely to have cancer, before they have received a test, then the most complete information we have available is provided by the probability $p(C)$. We call this the prior probability because it is the probability available before we observe the result of the test. Once we are told that this person has received a positive test, we can then use Bayes' theorem to compute the probability $p(C \mid T)$, which we will call the posterior probability because it is the probability obtained after we have observed the test result $T$.

In this example, the prior probability of having cancer is $1 \%$. However, once we have observed that the test result is positive, we find that the posterior probability of cancer is now $23 \%$, which is a substantially higher probability of cancer, as we would intuitively expect. We note, however, that a person with a positive test still has only a $23 \%$ change of actually having cancer, even though the test appears, from Figure 2.3 to be reasonably 'accurate'. This conclusion seems counter-intuitive to many people. The reason has to do with the low prior probability of having cancer. Although the test provides strong evidence of cancer, this has to be combined with the prior probability using Bayes' theorem to arrive at the correct posterior probability.

\subsection*{2.1.6 Independent variables}

Finally, if the joint distribution of two variables factorizes into the product of the marginals, so that $p(X, Y)=p(X) p(Y)$, then $X$ and $Y$ are said to be independent. An example of independent events would be the successive flips of a coin. From the product rule, we see that $p(Y \mid X)=p(Y)$, and so the conditional distribution of $Y$ given $X$ is indeed independent of the value of $X$. In our cancer screening example, if the probability of a positive test is independent of whether the person has cancer, then $p(T \mid C)=p(T)$, which means that from Bayes' theorem (2.10) we have $p(C \mid T)=p(C)$, and therefore probability of cancer is not changed by observing the test outcome. Of course, such a test would be useless because the outcome of the test tells us nothing about whether the person has cancer.


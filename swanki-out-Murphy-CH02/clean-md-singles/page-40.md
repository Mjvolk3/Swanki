![](https://cdn.mathpix.com/cropped/2024_06_13_4a0eadb9c3250516aa8dg-1.jpg?height=441&width=518&top_left_y=208&top_left_x=404)

(a)

![](https://cdn.mathpix.com/cropped/2024_06_13_4a0eadb9c3250516aa8dg-1.jpg?height=441&width=517&top_left_y=208&top_left_x=1119)

(b)

Figure 2.23: The central limit theorem in pictures. We plot a histogram of $\hat{\mu}_{N}^{s}=\frac{1}{N_{\mathcal{D}}} \sum_{n=1}^{N_{\mathcal{D}}} x_{n s}$, where $x_{n s} \sim \operatorname{Beta}(1,5)$, for $s=1: 10000$. As $N_{\mathcal{D}} \rightarrow \infty$, the distribution tends towards a Gaussian. (a) $N=1$. (b) $N=5$. Adapted from Figure 2.6 of [Bis06]. Generated by centralLimitDemo.ipynb.

Hence the distribution of the quantity

$$
Z_{N_{\mathcal{D}}} \triangleq \frac{S_{N_{\mathcal{D}}}-N_{\mathcal{D}} \mu}{\sigma \sqrt{N_{\mathcal{D}}}}=\frac{\bar{X}-\mu}{\sigma / \sqrt{N_{\mathcal{D}}}}
$$

converges to the standard normal, where $\bar{X}=S_{N} / N$ is the sample mean. This is called the central limit theorem. See e.g., [Jay03, p222] or [Ric95, p169] for a proof.

In Figure 2.23 we give an example in which we compute the sample mean of rv's drawn from a beta distribution. We see that the sampling distribution of this mean rapidly converges to a Gaussian distribution.

\title{
2.8.7 Monte Carlo approximation
}

Suppose $\boldsymbol{x}$ is a random variable, and $\boldsymbol{y}=f(\boldsymbol{x})$ is some function of $\boldsymbol{x}$. It is often difficult to compute the induced distribution $p(\boldsymbol{y})$ analytically. One simple but powerful alternative is to draw a large number of samples from the $\boldsymbol{x}$ 's distribution, and then to use these samples (instead of the distribution) to approximate $p(\boldsymbol{y})$.

For example, suppose $x \sim \operatorname{Unif}(-1,1)$ and $y=f(x)=x^{2}$. We can approximate $p(y)$ by drawing many samples from $p(x)$ (using a uniform random number generator), squaring them, and computing the resulting empirical distribution, which is given by

$$
p_{S}(y) \triangleq \frac{1}{N_{s}} \sum_{s=1}^{N_{s}} \delta\left(y-y_{s}\right)
$$

This is just an equally weighted "sum of spikes", each centered on one of the samples (see Section 2.7.6). By using enough samples, we can approximate $p(y)$ rather well. See Figure 2.24 for an illustration.

This approach is called a Monte Carlo approximation to the distribution. (The term "Monte Carlo" comes from the name of a famous gambling casino in Monaco.) Monte Carlo techniques were
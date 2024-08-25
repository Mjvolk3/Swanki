```markdown
## What will be the probability distribution of the sum of two dice rolls, $y=x_{1}+x_{2}$, where $x_{i} \sim \operatorname{Unif}(\{1,2, \ldots, 6\})$?

When summing two uniformly distributed dice rolls, the distribution of the sum 'y' is computed as follows:

$$
\begin{aligned}
& p(y=2)=p\left(x_{1}=1\right) p\left(x_{2}=1\right)=\frac{1}{6} \cdot \frac{1}{6}=\frac{1}{36} \\
& p(y=3)=p\left(x_{1}=1\right) p\left(x_{2}=2\right)+p\left(x_{1}=2\right) p\left(x_{2}=1\right)=\frac{1}{6} \cdot \frac{1}{6}+\frac{1}{6} \cdot \frac{1}{6}=\frac{2}{36}
\end{aligned}
$$

Continuing in this way, we find $p(y=4)=3/36, p(y=5)=4/36, p(y=6)=5/36, p(y=7)=6/36$, $p(y=8)=5/36, p(y=9)=4/36, p(y=10)=3/36, p(y=11)=2/36$ and $p(y=12)=1/36$. 

- #probability, #random-variables, #distributions

## Given that $x_{1} \sim \mathcal{N}\left(\boldsymbol{\mu}_{1}, \sigma_{1}^{2}\right)$ and $x_{2} \sim \mathcal{N}\left(\boldsymbol{\mu}_{2}, \sigma_{2}^{2}\right)$, what is $p(y)$ where $y = x_{1} + x_{2}$?

When two independent Gaussian random variables are summed, their resultant distribution is also Gaussian:

$$
p(y)=\mathcal{N}\left(y \mid \boldsymbol{\mu}_{1}+\boldsymbol{\mu}_{2}, \sigma_{1}^{2}+\sigma_{2}^{2}\right)
$$

This result shows the convolution of two Gaussian distributions.

- #statistics, #convolution, #distributions

## What is an example of a probability density function (pdf) of the sum of two continuous random variables?

An example of the pdf of the sum of two continuous random variables, each following a Gaussian distribution, can be represented as:

$$
p(y)=\mathcal{N}\left(y \mid \boldsymbol{\mu}_{1}+\boldsymbol{\mu}_{2}, \sigma_{1}^{2}+\sigma_{2}^{2}\right)
$$

- #statistics, #pdf, #gaussian

## Considering $N_{\mathcal{D}}$ iid random variables with mean $\mu$ and variance $\sigma^{2}$, what can we say about the distribution of their sum $S_{N_{\mathcal{D}}}=\sum_{n=1}^{N_{\mathcal{D}}} X_{n}$ as $N_{\mathcal{D}}$ increases?

As $N_{\mathcal{D}}$ increases, the distribution of the sum approaches:

$$
p\left(S_{N_{\mathcal{D}}}=u\right)=\frac{1}{\sqrt{2 \pi N_{\mathcal{D}} \sigma^{2}}} \exp \left(-\frac{\left(u-N_{\mathcal{D}} \mu\right)^{2}}{2 N_{\mathcal{D}} \sigma^{2}}\right)
$$

This result is a consequence of the Central Limit Theorem.

- #central-limit-theorem, #statistics, #distributions

## How do you calculate $p(y=3)$ where $y=x_{1}+x_{2}$ and $x_{i} \sim \operatorname{Unif}(\{1,2, \ldots, 6\})$?

To calculate $p(y=3)$:
$$
p(y=3)=p\left(x_{1}=1\right) p\left(x_{2}=2\right)+p\left(x_{1}=2\right) p\left(x_{2}=1\right)=\frac{1}{6} \cdot \frac{1}{6}+\frac{1}{6} \cdot \frac{1}{6}=\frac{2}{36}
$$

- #probability, #computation, #dice-rolls

## What does the Central Limit Theorem state regarding the distribution of the sum of a large number of iid random variables?

The Central Limit Theorem states that the sum of a large number of iid random variables with mean $\mu$ and variance $\sigma^2$ will be approximately normally distributed regardless of the original distribution of the variables. 

$$
p\left(S_{N_{\mathcal{D}}}=u\right)=\frac{1}{\sqrt{2 \pi N_{\mathcal{D}} \sigma^{2}}} \exp \left(-\frac{\left(u-N_{\mathcal{D}} \mu\right)^{2}}{2 N_{\mathcal{D}} \sigma^{2}}\right)
$$

- #central-limit-theorem, #iid, #probability
```
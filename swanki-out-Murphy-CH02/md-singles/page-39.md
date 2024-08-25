![](https://cdn.mathpix.com/cropped/2024_06_13_3b03ebbae3c95d0ddb56g-1.jpg?height=393&width=518&top_left_y=196&top_left_x=751)

Figure 2.22: Distribution of the sum of two dice rolls, i.e., \(p(y)\) where \(y=x_{1}+x_{2}\) and \(x_{i} \sim \operatorname{Unif}(\{1,2, \ldots, 6\})\). From https://en.wikipedia.org/wiki/Probability_distribution. Used with kind permission of Wikipedia author Tim Stellmach.

over \(\{1,2, \ldots, 6\}\). Let \(y=x_{1}+x_{2}\) be the sum of the dice. We have

\[
\begin{aligned}
& p(y=2)=p\left(x_{1}=1\right) p\left(x_{2}=1\right)=\frac{1}{6} \frac{1}{6}=\frac{1}{36} \\
& p(y=3)=p\left(x_{1}=1\right) p\left(x_{2}=2\right)+p\left(x_{1}=2\right) p\left(x_{2}=1\right)=\frac{1}{6} \frac{1}{6}+\frac{1}{6} \frac{1}{6}=\frac{2}{36}
\end{aligned}
\]

Continuing in this way, we find \(p(y=4)=3 / 36, p(y=5)=4 / 36, p(y=6)=5 / 36, p(y=7)=6 / 36\), \(p(y=8)=5 / 36, p(y=9)=4 / 36, p(y=10)=3 / 36, p(y=11)=2 / 36\) and \(p(y=12)=1 / 36\). See Figure 2.22 for a plot. We see that the distribution looks like a Gaussian; we explain the reasons for this in Section 2.8.6.

We can also compute the pdf of the sum of two continuous rv's. For example, in the case of Gaussians, where \(x_{1} \sim \mathcal{N}\left(\boldsymbol{\mu}_{1}, \sigma_{1}^{2}\right)\) and \(x_{2} \sim \mathcal{N}\left(\boldsymbol{\mu}_{2}, \sigma_{2}^{2}\right)\), one can show (Exercise 2.4) that if \(y=x_{1}+x_{2}\) then

\[
p(y)=\mathcal{N}\left(x_{1} \mid \boldsymbol{\mu}_{1}, \sigma_{1}^{2}\right) \otimes \mathcal{N}\left(x_{2} \mid \boldsymbol{\mu}_{2}, \sigma_{2}^{2}\right)=\mathcal{N}\left(y \mid \boldsymbol{\mu}_{1}+\boldsymbol{\mu}_{2}, \sigma_{1}^{2}+\sigma_{2}^{2}\right)
\]

Hence the convolution of two Gaussians is a Gaussian.

\title{
2.8.6 Central limit theorem
}

Now consider \(N_{\mathcal{D}}\) random variables with pdf's (not necessarily Gaussian) \(p_{n}(x)\), each with mean \(\mu\) and variance \(\sigma^{2}\). We assume each variable is independent and identically distributed or iid for short, which means \(X_{n} \sim p(X)\) are independent samples from the same distribution. Let \(S_{N_{\mathcal{D}}}=\sum_{n=1}^{N_{\mathcal{D}}} X_{n}\) be the sum of the rv's. One can show that, as \(N\) increases, the distribution of this sum approaches

\[
p\left(S_{N_{\mathcal{D}}}=u\right)=\frac{1}{\sqrt{2 \pi N_{\mathcal{D}} \sigma^{2}}} \exp \left(-\frac{\left(u-N_{\mathcal{D}} \mu\right)^{2}}{2 N_{\mathcal{D}} \sigma^{2}}\right)
\]

Author: Kevin P. Murphy. (C) MIT Press. CC-BY-NC-ND license
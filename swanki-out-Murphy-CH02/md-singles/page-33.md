![](https://cdn.mathpix.com/cropped/2024_06_13_aee57e93246230d45dbeg-1.jpg?height=592&width=1237&top_left_y=189&top_left_x=402)

Figure 2.18: Illustration of the (a) empirical pdf and (b) empirical cdf derived from a set of \(N=5\) samples. From https: //bit. ly/3hFgi0e. Used with kind permission of Mauro Escudero.

- Chi-squared distribution. This is defined by

\[
\chi_{\nu}^{2}(x) \triangleq \mathrm{Ga}\left(x \mid \text { shape }=\frac{\nu}{2}, \text { rate }=\frac{1}{2}\right)
\]

where \(\nu\) is called the degrees of freedom. This is the distribution of the sum of squared Gaussian random variables. More precisely, if \(Z_{i} \sim \mathcal{N}(0,1)\), and \(S=\sum_{i=1}^{\nu} Z_{i}^{2}\), then \(S \sim \chi_{\nu}^{2}\).

- The inverse Gamma distribution is defined as follows:

\[
\operatorname{IG}(x \mid \text { shape }=a, \text { scale }=b) \triangleq \frac{b^{a}}{\Gamma(a)} x^{-(a+1)} e^{-b / x}
\]

The distribution has these properties

\[
\text { mean }=\frac{b}{a-1}, \text { mode }=\frac{b}{a+1}, \text { var }=\frac{b^{2}}{(a-1)^{2}(a-2)}
\]

The mean only exists if \(a>1\). The variance only exists if \(a>2\). Note: if \(X \sim \mathrm{Ga}\) (shape \(=\) \(a\), rate \(=b\) ), then \(1 / X \sim \operatorname{IG}\) (shape \(=a\), scale \(=b\) ). (Note that \(b\) plays two different roles in this case.)

\title{
2.7.6 Empirical distribution
}

Suppose we have a set of \(N\) samples \(\mathcal{D}=\left\{x^{(1)}, \ldots, x^{(N)}\right\}\), derived from a distribution \(p(X)\), where \(X \in \mathbb{R}\). We can approximate the pdf using a set of delta functions (Section 2.6.5) or "spikes", centered on these samples:

\[
\hat{p}_{N}(x)=\frac{1}{N} \sum_{n=1}^{N} \delta_{x^{(n)}}(x)
\]

Author: Kevin P. Murphy. (C) MIT Press. CC-BY-NC-ND license
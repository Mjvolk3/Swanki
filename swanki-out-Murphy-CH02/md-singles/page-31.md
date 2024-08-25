The half Cauchy distribution is a version of the Cauchy (with \(\mu=0\) ) that is "folded over" on itself, so all its probability density is on the positive reals. Thus it has the form

\[
\mathcal{C}_{+}(x \mid \gamma) \triangleq \frac{2}{\pi \gamma}\left[1+\left(\frac{x}{\gamma}\right)^{2}\right]^{-1}
\]

This is useful in Bayesian modeling, where we want to use a distribution over positive reals with heavy tails, but finite density at the origin.

\title{
2.7.3 Laplace distribution
}

Another distribution with heavy tails is the Laplace distribution \({ }^{10}\), also known as the double sided exponential distribution. This has the following pdf:

\[
\operatorname{Laplace}(y \mid \mu, b) \triangleq \frac{1}{2 b} \exp \left(-\frac{|y-\mu|}{b}\right)
\]

See Figure 2.15 for a plot. Here \(\mu\) is a location parameter and \(b>0\) is a scale parameter. This distribution has the following properties:

\[
\text { mean }=\mu, \text { mode }=\mu, \text { var }=2 b^{2}
\]

In Section 11.6.1, we discuss how to use the Laplace distribution for robust linear regression, and in Section 11.4, we discuss how to use the Laplace distribution for sparse linear regression.

\subsection*{2.7.4 Beta distribution}

The beta distribution has support over the interval \([0,1]\) and is defined as follows:

\[
\operatorname{Beta}(x \mid a, b)=\frac{1}{B(a, b)} x^{a-1}(1-x)^{b-1}
\]

where \(B(a, b)\) is the beta function, defined by

\[
B(a, b) \triangleq \frac{\Gamma(a) \Gamma(b)}{\Gamma(a+b)}
\]

where \(\Gamma(a)\) is the Gamma function defined by

\[
\Gamma(a) \triangleq \int_{0}^{\infty} x^{a-1} e^{-x} d x
\]

See Figure 2.17a for plots of some beta distributions.

We require \(a, b>0\) to ensure the distribution is integrable (i.e., to ensure \(B(a, b)\) exists). If \(a=b=1\), we get the uniform distribution. If \(a\) and \(b\) are both less than 1 , we get a bimodal distribution with "spikes" at 0 and 1 ; if \(a\) and \(b\) are both greater than 1 , the distribution is unimodal.

For later reference, we note that the distribution has the following properties (Exercise 2.8):

\[
\text { mean }=\frac{a}{a+b}, \text { mode }=\frac{a-1}{a+b-2}, \text { var }=\frac{a b}{(a+b)^{2}(a+b+1)}
\]
\footnotetext{
10. Pierre-Simon Laplace (1749-1827) was a French mathematician, who played a key role in creating the field of Bayesian statistics.

Author: Kevin P. Murphy. (C) MIT Press. CC-BY-NC-ND license
}
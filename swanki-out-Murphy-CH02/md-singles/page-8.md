We can write this assumption as a graph \(X-Z-Y\), which captures the intuition that all the dependencies between \(X\) and \(Y\) are mediated via \(Z\). By using larger graphs, we can define complex joint distributions; these are known as graphical models, and are discussed in Section 3.6.

\title{
2.2.5 Moments of a distribution
}

In this section, we describe various summary statistics that can be derived from a probability distribution (either a pdf or pmf).

\subsection*{2.2.5.1 Mean of a distribution}

The most familiar property of a distribution is its mean, or expected value, often denoted by \(\mu\). For continuous rv's, the mean is defined as follows:

\[
\mathbb{E}[X] \triangleq \int_{\mathcal{X}} x p(x) d x
\]

If the integral is not finite, the mean is not defined; we will see some examples of this later.

For discrete rv's, the mean is defined as follows:

\[
\mathbb{E}[X] \triangleq \sum_{x \in \mathcal{X}} x p(x)
\]

However, this is only meaningful if the values of \(x\) are ordered in some way (e.g., if they represent integer counts).

Since the mean is a linear operator, we have

\[
\mathbb{E}[a X+b]=a \mathbb{E}[X]+b
\]

This is called the linearity of expectation.

For a set of \(n\) random variables, one can show that the expectation of their sum is as follows:

\[
\mathbb{E}\left[\sum_{i=1}^{n} X_{i}\right]=\sum_{i=1}^{n} \mathbb{E}\left[X_{i}\right]
\]

If they are independent, the expectation of their product is given by

\[
\mathbb{E}\left[\prod_{i=1}^{n} X_{i}\right]=\prod_{i=1}^{n} \mathbb{E}\left[X_{i}\right]
\]

\subsection*{2.2.5.2 Variance of a distribution}

The variance is a measure of the "spread" of a distribution, often denoted by \(\sigma^{2}\). This is defined as follows:

\[
\begin{aligned}
\mathbb{V}[X] & \triangleq \mathbb{E}\left[(X-\mu)^{2}\right]=\int(x-\mu)^{2} p(x) d x \\
& =\int x^{2} p(x) d x+\mu^{2} \int p(x) d x-2 \mu \int x p(x) d x=\mathbb{E}\left[X^{2}\right]-\mu^{2}
\end{aligned}
\]
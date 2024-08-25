\title{
2.2.2.3 Quantiles
}

If the cdf \(P\) is strictly monotonically increasing, it has an inverse, called the inverse cdf, or percent point function (ppf), or quantile function.

If \(P\) is the cdf of \(X\), then \(P^{-1}(q)\) is the value \(x_{q}\) such that \(\operatorname{Pr}\left(X \leq x_{q}\right)=q\); this is called the \(q^{\prime}\) th quantile of \(P\). The value \(P^{-1}(0.5)\) is the median of the distribution, with half of the probability mass on the left, and half on the right. The values \(P^{-1}(0.25)\) and \(P^{-1}(0.75)\) are the lower and upper quartiles.

For example, let \(\Phi\) be the cdf of the Gaussian distribution \(\mathcal{N}(0,1)\), and \(\Phi^{-1}\) be the inverse cdf. Then points to the left of \(\Phi^{-1}(\alpha / 2)\) contain \(\alpha / 2\) of the probability mass, as illustrated in Figure 2.2b. By symmetry, points to the right of \(\Phi^{-1}(1-\alpha / 2)\) also contain \(\alpha / 2\) of the mass. Hence the central interval \(\left(\Phi^{-1}(\alpha / 2), \Phi^{-1}(1-\alpha / 2)\right)\) contains \(1-\alpha\) of the mass. If we set \(\alpha=0.05\), the central \(95 \%\) interval is covered by the range

\[
\left(\Phi^{-1}(0.025), \Phi^{-1}(0.975)\right)=(-1.96,1.96)
\]

If the distribution is \(\mathcal{N}\left(\mu, \sigma^{2}\right)\), then the \(95 \%\) interval becomes \((\mu-1.96 \sigma, \mu+1.96 \sigma)\). This is often approximated by writing \(\mu \pm 2 \sigma\).

\subsection*{2.2.3 Sets of related random variables}

In this section, we discuss distributions over sets of related random variables.

Suppose, to start, that we have two random variables, \(X\) and \(Y\). We can define the joint distribution of two random variables using \(p(x, y)=p(X=x, Y=y)\) for all possible values of \(X\) and \(Y\). If both variables have finite cardinality, we can represent the joint distribution as a \(2 \mathrm{~d}\) table, all of whose entries sum to one. For example, consider the following example with two binary variables:

\[
\begin{array}{l|ll}
p(X, Y) & Y=0 & Y=1 \\
\hline X=0 & 0.2 & 0.3 \\
X=1 & 0.3 & 0.2
\end{array}
\]

If two variables are independent, we can represent the joint as the product of the two marginals. If both variables have finite cardinality, we can factorize the \(2 \mathrm{~d}\) joint table into a product of two \(1 \mathrm{~d}\) vectors, as shown in Figure 2.3.

Given a joint distribution, we define the marginal distribution of an rv as follows:

\[
p(X=x)=\sum_{y} p(X=x, Y=y)
\]

where we are summing over all possible states of \(Y\). This is sometimes called the sum rule or the rule of total probability. We define \(p(Y=y)\) similarly. For example, from the above \(2 \mathrm{~d}\) table, we see \(p(X=0)=0.2+0.3=0.5\) and \(p(Y=0)=0.2+0.3=0.5\). (The term "marginal" comes from the accounting practice of writing the sums of rows and columns on the side, or margin, of a table.)

We define the conditional distribution of an rv using

\[
p(Y=y \mid X=x)=\frac{p(X=x, Y=y)}{p(X=x)}
\]

We can rearrange this equation to get

\[
p(x, y)=p(x) p(y \mid x)
\]

Draft of "Probabilistic Machine Learning: An Introduction". August 8, 2022
from which we derive the useful result

\[
\mathbb{E}\left[X^{2}\right]=\sigma^{2}+\mu^{2}
\]

The standard deviation is defined as

\[
\operatorname{std}[X] \triangleq \sqrt{\mathbb{V}[X]}=\sigma
\]

This is useful since it has the same units as \(X\) itself.

The variance of a shifted and scaled version of a random variable is given by

\[
\mathbb{V}[a X+b]=a^{2} \mathbb{V}[X]
\]

If we have a set of \(n\) independent random variables, the variance of their sum is given by the sum of their variances:

\[
\mathbb{V}\left[\sum_{i=1}^{n} X_{i}\right]=\sum_{i=1}^{n} \mathbb{V}\left[X_{i}\right]
\]

The variance of their product can also be derived, as follows:

\[
\begin{aligned}
\mathbb{V}\left[\prod_{i=1}^{n} X_{i}\right] & =\mathbb{E}\left[\left(\prod_{i} X_{i}\right)^{2}\right]-\left(\mathbb{E}\left[\prod_{i} X_{i}\right]\right)^{2} \\
& =\mathbb{E}\left[\prod_{i} X_{i}^{2}\right]-\left(\prod_{i} \mathbb{E}\left[X_{i}\right]\right)^{2} \\
& =\prod_{i} \mathbb{E}\left[X_{i}^{2}\right]-\prod_{i}\left(\mathbb{E}\left[X_{i}\right]\right)^{2} \\
& =\prod_{i}\left(\mathbb{V}\left[X_{i}\right]+\left(\mathbb{E}\left[X_{i}\right]\right)^{2}\right)-\prod_{i}\left(\mathbb{E}\left[X_{i}\right]\right)^{2} \\
& =\prod_{i}\left(\sigma_{i}^{2}+\mu_{i}^{2}\right)-\prod_{i} \mu_{i}^{2}
\end{aligned}
\]

\title{
2.2.5.3 Mode of a distribution
}

The mode of a distribution is the value with the highest probability mass or probability density:

\[
\boldsymbol{x}^{*}=\underset{\boldsymbol{x}}{\operatorname{argmax}} p(\boldsymbol{x})
\]

If the distribution is multimodal, this may not be unique, as illustrated in Figure 2.4. Furthermore, even if there is a unique mode, this point may not be a good summary of the distribution.

\subsection*{2.2.5.4 Conditional moments}

When we have two or more dependent random variables, we can compute the moments of one given knowledge of the other. For example, the law of iterated expectations, also called the law of total expectation, tells us that

\[
\mathbb{E}[X]=\mathbb{E}_{Y}[\mathbb{E}[X \mid Y]]
\]

Author: Kevin P. Murphy. (C) MIT Press. CC-BY-NC-ND license
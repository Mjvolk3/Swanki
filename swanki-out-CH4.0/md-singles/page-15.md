Because this quantity will be dependent on the particular data set \(\mathcal{D}\), we take its average over the ensemble of data sets. If we add and subtract the quantity \(\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]\) inside the braces, and then expand, we obtain

\[
\begin{aligned}
& \left\{f(\mathbf{x} ; \mathcal{D})-\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]+\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]-h(\mathbf{x})\right\}^{2} \\
& =\left\{f(\mathbf{x} ; \mathcal{D})-\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]\right\}^{2}+\left\{\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]-h(\mathbf{x})\right\}^{2} \\
& +2\left\{f(\mathbf{x} ; \mathcal{D})-\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]\right\}\left\{\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]-h(\mathbf{x})\right\}
\end{aligned}
\]

We now take the expectation of this expression with respect to \(\mathcal{D}\) and note that the final term will vanish, giving

\[
\begin{aligned}
& \mathbb{E}_{\mathcal{D}}\left[\{f(\mathbf{x} ; \mathcal{D})-h(\mathbf{x})\}^{2}\right] \\
& =\underbrace{\left\{\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]-h(\mathbf{x})\right\}^{2}}_{(\text {bias })^{2}}+\underbrace{\mathbb{E}_{\mathcal{D}}\left[\left\{f(\mathbf{x} ; \mathcal{D})-\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]\right\}^{2}\right]}_{\text {variance }}
\end{aligned}
\]

We see that the expected squared difference between \(f(\mathbf{x} ; \mathcal{D})\) and the regression function \(h(\mathbf{x})\) can be expressed as the sum of two terms. The first term, called the squared bias, represents the extent to which the average prediction over all data sets differs from the desired regression function. The second term, called the variance, measures the extent to which the solutions for individual data sets vary around their average, and hence, this measures the extent to which the function \(f(\mathbf{x} ; \mathcal{D})\) is sensitive to the particular choice of data set. We will provide some intuition to support these definitions shortly when we consider a simple example.

So far, we have considered a single input value \(\mathrm{x}\). If we substitute this expansion back into (4.42), we obtain the following decomposition of the expected squared loss:

\[
\text { expected loss }=(\text { bias })^{2}+\text { variance }+ \text { noise }
\]

where

\[
\begin{aligned}
(\text { bias })^{2} & =\int\left\{\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]-h(\mathbf{x})\right\}^{2} p(\mathbf{x}) \mathrm{d} \mathbf{x} \\
\text { variance } & =\int \mathbb{E}_{\mathcal{D}}\left[\left\{f(\mathbf{x} ; \mathcal{D})-\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]\right\}^{2}\right] p(\mathbf{x}) \mathrm{d} \mathbf{x} \\
\text { noise } & =\iint\{h(\mathbf{x})-t\}^{2} p(\mathbf{x}, t) \mathrm{d} \mathbf{x} \mathrm{d} t
\end{aligned}
\]

and the bias and variance terms now refer to integrated quantities.

Our goal is to minimize the expected loss, which we have decomposed into the sum of a (squared) bias, a variance, and a constant noise term. As we will see, there is a trade-off between bias and variance, with very flexible models having low bias and high variance, and relatively rigid models having high bias and low variance. The model with the optimal predictive capability is the one that leads to the best balance between bias and variance. This is illustrated by considering the sinusoidal data set introduced earlier. Here we independently generate 100 data sets, each containing
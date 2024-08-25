Section 6.1.1

Chapter 1

Section 3.1.2 \(M\) bins, then the total number of bins will be \(M^{D}\). This exponential scaling with \(D\) is an example of the curse of dimensionality. In a space of high dimensionality, the quantity of data needed to provide meaningful estimates of the local probability density would be prohibitive.

The histogram approach to density estimation does, however, teach us two important lessons. First, to estimate the probability density at a particular location, we should consider the data points that lie within some local neighbourhood of that point. Note that the concept of locality requires that we assume some form of distance measure, and here we have been assuming Euclidean distance. For histograms, this neighbourhood property was defined by the bins, and there is a natural 'smoothing' parameter describing the spatial extent of the local region, in this case the bin width. Second, to obtain good results, the value of the smoothing parameter should be neither too large nor too small. This is reminiscent of the choice of model complexity in polynomial regression where the degree \(M\) of the polynomial, or alternatively the value \(\lambda\) of the regularization parameter, was optimal for some intermediate value, neither too large nor too small. Armed with these insights, we turn now to a discussion of two widely used nonparametric techniques for density estimation, kernel estimators and nearest neighbours, which have better scaling with dimensionality than the simple histogram model.

\subsection*{3.5.2 Kernel densities}

Let us suppose that observations are being drawn from some unknown probability density \(p(\mathbf{x})\) in some \(D\)-dimensional space, which we will take to be Euclidean, and we wish to estimate the value of \(p(\mathbf{x})\). From our earlier discussion of locality, let us consider some small region \(\mathcal{R}\) containing \(\mathbf{x}\). The probability mass associated with this region is given by

\[
P=\int_{\mathcal{R}} p(\mathbf{x}) \mathrm{d} \mathbf{x}
\]

Now suppose that we have collected a data set comprising \(N\) observations drawn from \(p(\mathbf{x})\). Because each data point has a probability \(P\) of falling within \(\mathcal{R}\), the total number \(K\) of points that lie inside \(\mathcal{R}\) will be distributed according to the binomial distribution:

\[
\operatorname{Bin}(K \mid N, P)=\frac{N!}{K!(N-K)!} P^{K}(1-P)^{N-K}
\]

Using (3.11), we see that the mean fraction of points falling inside the region is \(\mathbb{E}[K / N]=P\), and similarly using (3.12), we see that the variance around this mean is \(\operatorname{var}[K / N]=P(1-P) / N\). For large \(N\), this distribution will be sharply peaked around the mean and so

\[
K \simeq N P
\]

If, however, we also assume that the region \(\mathcal{R}\) is sufficiently small so that the probability density \(p(\mathbf{x})\) is roughly constant over the region, then we have

\[
P \simeq p(\mathbf{x}) V
\]
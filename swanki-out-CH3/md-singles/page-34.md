Now consider a set of independent identically distributed data denoted by \(\mathbf{X}=\) \(\left\{\mathbf{x}_{1}, \ldots, \mathbf{x}_{n}\right\}\), for which the likelihood function is given by

\[
p(\mathbf{X} \mid \boldsymbol{\eta})=\left(\prod_{n=1}^{N} h\left(\mathbf{x}_{n}\right)\right) g(\boldsymbol{\eta})^{N} \exp \left\{\boldsymbol{\eta}^{\mathrm{T}} \sum_{n=1}^{N} \mathbf{u}\left(\mathbf{x}_{n}\right)\right\}
\]

Setting the gradient of \(\ln p(\mathbf{X} \mid \boldsymbol{\eta})\) with respect to \(\boldsymbol{\eta}\) to zero, we get the following condition to be satisfied by the maximum likelihood estimator \(\boldsymbol{\eta}_{\mathrm{ML}}\) :

\[
-\nabla \ln g\left(\boldsymbol{\eta}_{\mathrm{ML}}\right)=\frac{1}{N} \sum_{n=1}^{N} \mathbf{u}\left(\mathbf{x}_{n}\right)
\]

which can in principle be solved to obtain \(\boldsymbol{\eta}_{\mathrm{ML}}\). We see that the solution for the maximum likelihood estimator depends on the data only through \(\sum_{n} \mathbf{u}\left(\mathbf{x}_{n}\right)\), which is therefore called the sufficient statistic of the distribution (3.138). We do not need to store the entire data set itself but only the value of the sufficient statistic. For the Bernoulli distribution, for example, the function \(\mathbf{u}(x)\) is given just by \(x\) and so we need only keep the sum of the data points \(\left\{x_{n}\right\}\), whereas for the Gaussian \(\mathbf{u}(x)=\left(x, x^{2}\right)^{\mathrm{T}}\), and so we should keep both the sum of \(\left\{x_{n}\right\}\) and the sum of \(\left\{x_{n}^{2}\right\}\).

If we consider the limit \(N \rightarrow \infty\), then the right-hand side of (3.174) becomes \(\mathbb{E}[\mathbf{u}(\mathbf{x})]\), and so by comparing with (3.172) we see that in this limit, \(\boldsymbol{\eta}_{\mathrm{ML}}\) will equal the true value \(\boldsymbol{\eta}\).

\title{
3.5. Nonparametric Methods
}

Throughout this chapter, we have focused on the use of probability distributions having specific functional forms governed by a small number of parameters whose values are to be determined from a data set. This is called the parametric approach to density modelling. An important limitation of this approach is that the chosen density might be a poor model of the distribution that generates the data, which can result in poor predictive performance. For instance, if the process that generates the data is multimodal, then this aspect of the distribution can never be captured by a Gaussian, which is necessarily unimodal. In this final section, we consider some nonparametric approaches to density estimation that make few assumptions about the form of the distribution.

\subsection*{3.5.1 Histograms}

Let us start with a discussion of histogram methods for density estimation, which we have already encountered in the context of marginal and conditional distributions in Figure 2.5 and in the context of the central limit theorem in Figure 3.2. Here we explore the properties of histogram density models in more detail, focusing on cases with a single continuous variable \(x\). Standard histograms simply partition \(x\) into distinct bins of width \(\Delta_{i}\) and then count the number \(n_{i}\) of observations of \(x\) falling
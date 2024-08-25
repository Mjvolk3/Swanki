form (4.8), the conditional mean will be simply

\[
\mathbb{E}[t \mid \mathbf{x}]=\int t p(t \mid \mathbf{x}) \mathrm{d} t=y(\mathbf{x}, \mathbf{w})
\]

The use of calculus of variations to derive (4.37) implies that we are optimizing over all possible functions \(f(\mathbf{x})\). Although any parametric model that we can implement in practice is limited in the range of functions that it can represent, the framework of deep neural networks, discussed extensively in later chapters, provides a highly flexible class of functions that, for many practical purposes, can approximate any desired function to high accuracy.

We can derive this result in a slightly different way, which will also shed light on the nature of the regression problem. Armed with the knowledge that the optimal solution is the conditional expectation, we can expand the square term as follows

\[
\begin{aligned}
& \{f(\mathbf{x})-t\}^{2}=\{f(\mathbf{x})-\mathbb{E}[t \mid \mathbf{x}]+\mathbb{E}[t \mid \mathbf{x}]-t\}^{2} \\
& =\{f(\mathbf{x})-\mathbb{E}[t \mid \mathbf{x}]\}^{2}+2\{f(\mathbf{x})-\mathbb{E}[t \mid \mathbf{x}]\}\{\mathbb{E}[t \mid \mathbf{x}]-t\}+\{\mathbb{E}[t \mid \mathbf{x}]-t\}^{2}
\end{aligned}
\]

where, to keep the notation uncluttered, we use \(\mathbb{E}[t \mid \mathbf{x}]\) to denote \(\mathbb{E}_{t}[t \mid \mathbf{x}]\). Substituting into the loss function (4.35) and performing the integral over \(t\), we see that the crossterm vanishes and we obtain an expression for the loss function in the form

\[
\mathbb{E}[L]=\int\{f(\mathbf{x})-\mathbb{E}[t \mid \mathbf{x}]\}^{2} p(\mathbf{x}) \mathrm{d} \mathbf{x}+\int \operatorname{var}[t \mid \mathbf{x}] p(\mathbf{x}) \mathrm{d} \mathbf{x}
\]

The function \(f(\mathbf{x})\) we seek to determine appears only in the first term, which will be minimized when \(f(\mathbf{x})\) is equal to \(\mathbb{E}[t \mid \mathbf{x}]\), in which case this term will vanish. This is simply the result that we derived previously, and shows that the optimal least-squares predictor is given by the conditional mean. The second term is the variance of the distribution of \(t\), averaged over \(\mathbf{x}\), and represents the intrinsic variability of the target data and can be regarded as noise. Because it is independent of \(f(\mathbf{x})\), it represents the irreducible minimum value of the loss function.

The squared loss is not the only possible choice of loss function for regression. Here we consider briefly one simple generalization of the squared loss, called the Minkowski loss, whose expectation is given by

\[
\mathbb{E}\left[L_{q}\right]=\iint|f(\mathbf{x})-t|^{q} p(\mathbf{x}, t) \mathrm{d} \mathbf{x} \mathrm{d} t
\]

which reduces to the expected squared loss for \(q=2\). The function \(|f-t|^{q}\) is plotted against \(f-t\) for various values of \(q\) in Figure 4.6. The minimum of \(\mathbb{E}\left[L_{q}\right]\) is given by the conditional mean for \(q=2\), the conditional median for \(q=1\), and the conditional mode for \(q \rightarrow 0\).

Note that the Gaussian noise assumption implies that the conditional distribution of \(t\) given \(\mathbf{x}\) is unimodal, which may be inappropriate for some applications. In this case a squared loss can lead to very poor results and we need to develop more sophisticated approaches. For example, we can extend this model by using mixtures
Figure 4.5 The regression function \(f^{\star}(x)\), which minimizes the expected squared loss, is given by the mean of the conditional distribution \(p(t \mid x)\).

![](https://cdn.mathpix.com/cropped/2024_05_26_194577429b12ff8ccc6dg-1.jpg?height=539&width=708&top_left_y=219&top_left_x=938)

given by

\[
\mathbb{E}[L]=\iint L(t, f(\mathbf{x})) p(\mathbf{x}, t) \mathrm{d} \mathbf{x} \mathrm{d} t
\]

where we are averaging over the distribution of both input and target variables, weighted by their joint distribution \(p(\mathbf{x}, t)\). A common choice of loss function in regression problems is the squared loss given by \(L(t, f(\mathbf{x}))=\{f(\mathbf{x})-t\}^{2}\). In this case, the expected loss can be written

\[
\mathbb{E}[L]=\iint\{f(\mathbf{x})-t\}^{2} p(\mathbf{x}, t) \mathrm{d} \mathbf{x} \mathrm{d} t
\]

It is important not to confuse the squared-loss function with the sum-of-squares error function introduced earlier. The error function is used to set the parameters during training in order to determine the conditional probability distribution \(p(t \mid \mathbf{x})\), whereas the loss function governs how the conditional distribution is used to arrive at a predictive function \(f(\mathbf{x})\) specifying a prediction for each value of \(\mathbf{x}\).

Our goal is to choose \(f(\mathbf{x})\) so as to minimize \(\mathbb{E}[L]\). If we assume a completely

\section*{Appendix \(B\)} flexible function \(f(\mathbf{x})\), we can do this formally using the calculus of variations to give

\[
\frac{\delta \mathbb{E}[L]}{\delta f(\mathbf{x})}=2 \int\{f(\mathbf{x})-t\} p(\mathbf{x}, t) \mathrm{d} t=0
\]

Solving for \(f(\mathbf{x})\) and using the sum and product rules of probability, we obtain

\[
f^{\star}(\mathbf{x})=\frac{1}{p(\mathbf{x})} \int t p(\mathbf{x}, t) \mathrm{d} t=\int t p(t \mid \mathbf{x}) \mathrm{d} t=\mathbb{E}_{t}[t \mid \mathbf{x}]
\]

which is the conditional average of \(t\) conditioned on \(\mathrm{x}\) and is known as the regression function. This result is illustrated in Figure 4.5. It can readily be extended to multiple target variables represented by the vector \(\mathbf{t}\), in which case the optimal solution is the conditional average \(\mathbf{f}^{\star}(\mathbf{x})=\mathbb{E}_{t}[\mathbf{t} \mid \mathbf{x}]\). For a Gaussian conditional distribution of the
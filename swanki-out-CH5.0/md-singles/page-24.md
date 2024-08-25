![](https://cdn.mathpix.com/cropped/2024_05_26_bb6ce2823310d4cb97d4g-1.jpg?height=643&width=701&top_left_y=211&top_left_x=150)

\(x_{1}\)

![](https://cdn.mathpix.com/cropped/2024_05_26_bb6ce2823310d4cb97d4g-1.jpg?height=643&width=679&top_left_y=211&top_left_x=970)

\(x_{1}\)

Figure 5.14 The left-hand plot shows the class-conditional densities for three classes each having a Gaussian distribution, coloured red, green, and blue, in which the red and blue classes have the same covariance matrix. The right-hand plot shows the corresponding posterior probabilities, in which each point on the image is coloured using proportions of red, blue, and green ink corresponding to the posterior probabilities for the respective three classes. The decision boundaries are also shown. Notice that the boundary between the red and blue classes, which have the same covariance matrix, is linear, whereas those between the other pairs of classes are quadratic.

the prior class probabilities \(p\left(\mathcal{C}_{k}\right)\), using maximum likelihood. This requires a data set comprising observations of \(\mathbf{x}\) along with their corresponding class labels.

First, suppose we have two classes, each having a Gaussian class-conditional density with a shared covariance matrix, and suppose we have a data set \(\left\{\mathbf{x}_{n}, t_{n}\right\}\) where \(n=1, \ldots, N\). Here \(t_{n}=1\) denotes class \(\mathcal{C}_{1}\) and \(t_{n}=0\) denotes class \(\mathcal{C}_{2}\). We denote the prior class probability \(p\left(\mathcal{C}_{1}\right)=\pi\), so that \(p\left(\mathcal{C}_{2}\right)=1-\pi\). For a data point \(\mathbf{x}_{n}\) from class \(\mathcal{C}_{1}\), we have \(t_{n}=1\) and hence

\[
p\left(\mathbf{x}_{n}, \mathcal{C}_{1}\right)=p\left(\mathcal{C}_{1}\right) p\left(\mathbf{x}_{n} \mid \mathcal{C}_{1}\right)=\pi \mathcal{N}\left(\mathbf{x}_{n} \mid \boldsymbol{\mu}_{1}, \boldsymbol{\Sigma}\right)
\]

Similarly for class \(\mathcal{C}_{2}\), we have \(t_{n}=0\) and hence

\[
p\left(\mathbf{x}_{n}, \mathcal{C}_{2}\right)=p\left(\mathcal{C}_{2}\right) p\left(\mathbf{x}_{n} \mid \mathcal{C}_{2}\right)=(1-\pi) \mathcal{N}\left(\mathbf{x}_{n} \mid \boldsymbol{\mu}_{2}, \boldsymbol{\Sigma}\right)
\]

Thus, the likelihood function is given by

\[
p\left(\mathbf{t}, \mathbf{X} \mid \pi, \boldsymbol{\mu}_{1}, \boldsymbol{\mu}_{2}, \boldsymbol{\Sigma}\right)=\prod_{n=1}^{N}\left[\pi \mathcal{N}\left(\mathbf{x}_{n} \mid \boldsymbol{\mu}_{1}, \boldsymbol{\Sigma}\right)\right]^{t_{n}}\left[(1-\pi) \mathcal{N}\left(\mathbf{x}_{n} \mid \boldsymbol{\mu}_{2}, \boldsymbol{\Sigma}\right)\right]^{1-t_{n}}
\]

where \(\mathbf{t}=\left(t_{1}, \ldots, t_{N}\right)^{\mathrm{T}}\). As usual, it is convenient to maximize the log of the likelihood function. Consider first the maximization with respect to \(\pi\). The terms in

![](https://cdn.mathpix.com/cropped/2024_05_26_48954a2b928492e90315g-1.jpg?height=498&width=1492&top_left_y=227&top_left_x=153)

Figure 5.13 The left-hand plot shows the class-conditional densities for two classes, denoted red and blue. On the right is the corresponding posterior probability \(p\left(\mathcal{C}_{1} \mid \mathbf{x}\right)\), which is given by a logistic sigmoid of a linear function of \(\mathbf{x}\). The surface in the right-hand plot is coloured using a proportion of red ink given by \(p\left(\mathcal{C}_{1} \mid \mathbf{x}\right)\) and a proportion of blue ink given by \(p\left(\mathcal{C}_{2} \mid \mathbf{x}\right)=1-p\left(\mathcal{C}_{1} \mid \mathbf{x}\right)\).

are constant and so will be given by linear functions of \(\mathbf{x}\), and therefore the decision boundaries are linear in input space. The prior probabilities \(p\left(\mathcal{C}_{k}\right)\) enter only through the bias parameter \(w_{0}\), so that changes in the priors have the effect of making parallel shifts of the decision boundary and more generally of the parallel contours of constant posterior probability.

For the general case of \(K\) classes, the posterior probabilities are given by (5.45) where, from (5.46) and (5.47), we have

\[
a_{k}(\mathbf{x})=\mathbf{w}_{k}^{\mathrm{T}} \mathbf{x}+w_{k 0}
\]

in which we have defined

\[
\begin{aligned}
\mathbf{w}_{k} & =\boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}_{k} \\
w_{k 0} & =-\frac{1}{2} \boldsymbol{\mu}_{k}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}_{k}+\ln p\left(\mathcal{C}_{k}\right)
\end{aligned}
\]

We see that the \(a_{k}(\mathbf{x})\) are again linear functions of \(\mathbf{x}\) as a consequence of the cancellation of the quadratic terms due to the shared covariances. The resulting decision boundaries, corresponding to the minimum misclassification rate, will occur when two of the posterior probabilities (the two largest) are equal, and so will be defined by linear functions of \(\mathbf{x}\). Thus, we again have a generalized linear model.

If we relax the assumption of a shared covariance matrix and allow each classconditional density \(p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)\) to have its own covariance matrix \(\boldsymbol{\Sigma}_{k}\), then the earlier cancellations will no longer occur, and we will obtain quadratic functions of \(\mathbf{x}\), giving rise to a quadratic discriminant. The linear and quadratic decision boundaries are illustrated in Figure 5.14.

\title{
5.3.2 Maximum likelihood solution
}

Once we have specified a parametric functional form for the class-conditional densities \(p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)\), we can then determine the values of the parameters, together with
Section 4.1.3

Exercise 5.1 except element \(t_{j}\), which takes the value 1 . For instance, if we have \(K=5\) classes, then a data point from class 2 would be given the target vector

\[
\mathbf{t}=(0,1,0,0,0)^{\mathrm{T}}
\]

Again, we can interpret the value of \(t_{k}\) as the probability that the class is \(\mathcal{C}_{k}\) in which the probabilities take only the values 0 and 1 .

\subsection*{5.1.4 Least squares for classification}

With linear regression models, the minimization of a sum-of-squares error function leads to a simple closed-form solution for the parameter values. It is therefore tempting to see if we can apply the same least-squares formalism to classification problems. Consider a general classification problem with \(K\) classes and a 1 -of- \(K\) binary coding scheme for the target vector \(t\). One justification for using least squares in such a context is that it approximates the conditional expectation \(\mathbb{E}[\mathbf{t} \mid \mathbf{x}]\) of the target values given the input vector. For a binary coding scheme, this conditional expectation is given by the vector of posterior class probabilities. Unfortunately, these probabilities are typically approximated rather poorly, and indeed the approximations can have values outside the range \((0,1)\). However, it is instructional to explore these simple models and to understand how these limitations arise.

Each class \(\mathcal{C}_{k}\) is described by its own linear model so that

\[
y_{k}(\mathbf{x})=\mathbf{w}_{k}^{\mathrm{T}} \mathbf{x}+w_{k 0}
\]

where \(k=1, \ldots, K\). We can conveniently group these together using vector notation so that

\[
\mathbf{y}(\mathbf{x})=\widetilde{\mathbf{W}}^{\mathrm{T}} \widetilde{\mathbf{x}}
\]

where \(\widetilde{\mathbf{W}}\) is a matrix whose \(k\) th column comprises the \((D+1)\)-dimensional vector \(\widetilde{\mathbf{w}}_{k}=\left(w_{k 0}, \mathbf{w}_{k}^{\mathrm{T}}\right)^{\mathrm{T}}\) and \(\widetilde{\mathbf{x}}\) is the corresponding augmented input vector \(\left(1, \mathbf{x}^{\mathrm{T}}\right)^{\mathrm{T}}\) with a dummy input \(x_{0}=1\). A new input \(\mathbf{x}\) is then assigned to the class for which the output \(y_{k}=\widetilde{\mathbf{w}}_{k}^{\mathrm{T}} \widetilde{\mathbf{x}}\) is largest.

We now determine the parameter matrix \(\widetilde{\mathbf{W}}\) by minimizing a sum-of-squares error function. Consider a training data set \(\left\{\mathbf{x}_{n}, \mathbf{t}_{n}\right\}\) where \(n=1, \ldots, N\), and define a matrix \(\mathbf{T}\) whose \(n\)th row is the vector \(\mathbf{t}_{n}^{\mathrm{T}}\), together with a matrix \(\widetilde{\mathbf{X}}\) whose \(n\)th row is \(\widetilde{\mathbf{x}}_{n}^{\mathrm{T}}\). The sum-of-squares error function can then be written as

\[
E_{D}(\widetilde{\mathbf{W}})=\frac{1}{2} \operatorname{Tr}\left\{(\widetilde{\mathbf{X}} \widetilde{\mathbf{W}}-\mathbf{T})^{\mathrm{T}}(\widetilde{\mathbf{X}} \widetilde{\mathbf{W}}-\mathbf{T})\right\}
\]

Setting the derivative with respect to \(\widetilde{\mathbf{W}}\) to zero and rearranging, we obtain the solution for \(\widetilde{\mathbf{W}}\) in the form

\[
\widetilde{\mathbf{W}}=\left(\widetilde{\mathbf{X}}^{\mathrm{T}} \widetilde{\mathbf{X}}\right)^{-1} \widetilde{\mathbf{X}}^{\mathrm{T}} \mathbf{T}=\widetilde{\mathbf{X}}^{\dagger} \mathbf{T}
\]

Section 4.1.3

where \(\widetilde{\mathbf{X}}^{\dagger}\) is the pseudo-inverse of the matrix \(\widetilde{\mathbf{X}}\). We then obtain the discriminant
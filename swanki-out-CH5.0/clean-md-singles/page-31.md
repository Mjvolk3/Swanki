Exercise 5.20

Chapter 9

Section 5.3

Exercise 5.21
Note that maximum likelihood can exhibit severe over-fitting for data sets that are linearly separable. This arises because the maximum likelihood solution occurs when the hyperplane corresponding to $\sigma=0.5$, equivalent to $\mathrm{w}^{\mathrm{T}} \phi=0$, separates the two classes and the magnitude of $\mathbf{w}$ goes to infinity. In this case, the logistic sigmoid function becomes infinitely steep in feature space, corresponding to a Heaviside step function, so that every training point from each class $k$ is assigned a posterior probability $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)=1$. Furthermore, there is typically a continuum of such solutions because any separating hyperplane will give rise to the same posterior probabilities at the training data points. Maximum likelihood provides no way to favour one such solution over another, and which solution is found in practice will depend on the choice of optimization algorithm and on the parameter initialization. Note that the problem will arise even if the number of data points is large compared with the number of parameters in the model, so long as the training data set is linearly separable. The singularity can be avoided by adding a regularization term to the error function.

\subsection*{5.4.4 Multi-class logistic regression}

In our discussion of generative models for multi-class classification, we have seen that, for a large class of distributions from the exponential family, the posterior probabilities are given by a softmax transformation of linear functions of the feature variables, so that

$$
p\left(\mathcal{C}_{k} \mid \boldsymbol{\phi}\right)=y_{k}(\boldsymbol{\phi})=\frac{\exp \left(a_{k}\right)}{\sum_{j} \exp \left(a_{j}\right)}
$$

where the pre-activations $a_{k}$ are given by

$$
a_{k}=\mathbf{w}_{k}^{\mathrm{T}} \boldsymbol{\phi}
$$

There we used maximum likelihood to determine separately the class-conditional densities and the class priors and then found the corresponding posterior probabilities using Bayes' theorem, thereby implicitly determining the parameters $\left\{\mathbf{w}_{k}\right\}$. Here we consider the use of maximum likelihood to determine the parameters $\left\{\mathbf{w}_{k}\right\}$ of this model directly. To do this, we will require the derivatives of $y_{k}$ with respect to all the pre-activations $a_{j}$. These are given by

$$
\frac{\partial y_{k}}{\partial a_{j}}=y_{k}\left(I_{k j}-y_{j}\right)
$$

where $I_{k j}$ are the elements of the identity matrix.

Next we write down the likelihood function. This is most easily done using the 1 -of- $K$ coding scheme in which the target vector $\mathbf{t}_{n}$ for a feature vector $\phi_{n}$ belonging to class $\mathcal{C}_{k}$ is a binary vector with all elements zero except for element $k$, which equals one. The likelihood function is then given by

$$
p\left(\mathbf{T} \mid \mathbf{w}_{1}, \ldots, \mathbf{w}_{K}\right)=\prod_{n=1}^{N} \prod_{k=1}^{K} p\left(\mathcal{C}_{k} \mid \boldsymbol{\phi}_{n}\right)^{t_{n k}}=\prod_{n=1}^{N} \prod_{k=1}^{K} y_{n k}^{t_{n k}}
$$
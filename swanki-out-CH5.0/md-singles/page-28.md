\title{
5.4.1 Activation functions
}

Chapter 4

Section 5.2

Section 6.1
In linear regression, the model prediction \(y(\mathbf{x}, \mathbf{w})\) is given by a linear function of the parameters

\[
y(\mathbf{x}, \mathbf{w})=\mathbf{w}^{\mathrm{T}} \mathbf{x}+w_{0}
\]

which gives a continuous-valued output in the range \((-\infty, \infty)\). For classification problems, however, we wish to predict discrete class labels, or more generally posterior probabilities that lie in the range \((0,1)\). To achieve this, we consider a generalization of this model in which we transform the linear function of \(\mathbf{w}\) and \(w_{0}\) using a nonlinear function \(f(\cdot)\) so that

\[
y(\mathbf{x}, \mathbf{w})=f\left(\mathbf{w}^{\mathrm{T}} \mathbf{w}+w+0\right)
\]

In the machine learning literature, \(f(\cdot)\) is known as an activation function, whereas its inverse is called a link function in the statistics literature. The decision surfaces correspond to \(y(\mathbf{x})=\) constant, so that \(\mathbf{w}^{\mathrm{T}} \mathbf{x}=\) constant, and hence the decision surfaces are linear functions of \(\mathbf{x}\), even if the function \(f(\cdot)\) is nonlinear. For this reason, the class of models described by (5.70) are called generalized linear models (McCullagh and Nelder, 1989). However, in contrast to the models used for regression, they are no longer linear in the parameters due to the nonlinear function \(f(\cdot)\). This will lead to more complex analytical and computational properties than for linear regression models. Nevertheless, these models are still relatively simple compared to the much more flexible nonlinear models that will be studied in subsequent chapters.

\subsection*{5.4.2 Fixed basis functions}

So far in this chapter, we have considered classification models that work directly with the original input vector \(\mathbf{x}\). However, all the algorithms are equally applicable if we first make a fixed nonlinear transformation of the inputs using a vector of basis functions \(\phi(\mathbf{x})\). The resulting decision boundaries will be linear in the feature space \(\phi\), and these correspond to nonlinear decision boundaries in the original \(\mathbf{x}\) space, as illustrated in Figure 5.15. Classes that are linearly separable in the feature space \(\phi(\mathrm{x})\) need not be linearly separable in the original observation space \(\mathrm{x}\).

Note that as in our discussion of linear models for regression, one of the basis functions is typically set to a constant, say \(\phi_{0}(\mathbf{x})=1\), so that the corresponding parameter \(w_{0}\) plays the role of a bias.

For many problems of practical interest, there is significant overlap in \(\mathrm{x}\)-space between the class-conditional densities \(p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)\). This corresponds to posterior probabilities \(p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)\), which, for at least some values of \(\mathbf{x}\), are not 0 or 1 . In such cases, the optimal solution is obtained by modelling the posterior probabilities accurately and then applying standard decision theory. Note that nonlinear transformations \(\phi(\mathbf{x})\) cannot remove such a class overlap, although they can increase the level of overlap or create an overlap where none existed in the original observation space. However, suitable choices of nonlinearity can make the process of modelling the posterior probabilities easier. However, such fixed basis function models have important limitations, and these will be resolved in later chapters by allowing the basis functions themselves to adapt to the data.
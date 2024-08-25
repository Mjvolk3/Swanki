
![](https://cdn.mathpix.com/cropped/2024_05_26_f271bce35f2c91024ce0g-1.jpg?height=740&width=1514&top_left_y=221&top_left_x=110)

Figure 5.15 Illustration of the role of nonlinear basis functions in linear classification models. The left-hand plot shows the original input space $\left(x_{1}, x_{2}\right)$ together with data points from two classes labelled red and blue. Two 'Gaussian' basis functions $\phi_{1}(\mathbf{x})$ and $\phi_{2}(\mathbf{x})$ are defined in this space with centres shown by the green crosses and with contours shown by the green circles. The right-hand plot shows the corresponding feature space $\left(\phi_{1}, \phi_{2}\right)$ together with the linear decision boundary obtained given by a logistic regression model of the form discussed in Section 5.4.3. This corresponds to a nonlinear decision boundary in the original input space, shown by the black curve in the left-hand plot.

\title{
5.4.3 Logistic regression
}

We first consider the problem of two-class classification. In our discussion of generative approaches in Section 5.3, we saw that under rather general assumptions, the posterior probability of class $\mathcal{C}_{1}$ can be written as a logistic sigmoid acting on a linear function of the feature vector $\phi$ so that

$$
p\left(\mathcal{C}_{1} \mid \boldsymbol{\phi}\right)=y(\boldsymbol{\phi})=\sigma\left(\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}\right)
$$

with $p\left(\mathcal{C}_{2} \mid \phi\right)=1-p\left(\mathcal{C}_{1} \mid \phi\right)$. Here $\sigma(\cdot)$ is the logistic sigmoid function defined by (5.42). In the terminology of statistics, this model is known as logistic regression, although it should be emphasized that this is a model for classification rather than for continuous variable.

For an $M$-dimensional feature space $\phi$, this model has $M$ adjustable parameters. By contrast, if we had fitted Gaussian class-conditional densities using maximum likelihood, we would have used $2 M$ parameters for the means and $M(M+1) / 2$ parameters for the (shared) covariance matrix. Together with the class prior $p\left(\mathcal{C}_{1}\right)$, this gives a total of $M(M+5) / 2+1$ parameters, which grows quadratically with $M$, in contrast to the linear dependence on $M$ of the number of parameters in logistic regression. For large values of $M$, there is a clear advantage in working with the logistic regression model directly.
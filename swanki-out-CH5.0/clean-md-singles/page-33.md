Figure 5.17 Schematic example of a probability density $p(\theta)$ shown by the blue curve, given in this example by a mixture of two Gaussians, along with its cumulative distribution function $f(a)$, shown by the red curve. Note that the value of the blue curve at any point, such as that indicated by the vertical green line, corresponds to the slope of the red curve at the same point. Conversely, the value of the red curve at this point corresponds to the area under the blue curve indicated by the shaded green region. In the stochastic threshold model, the class label takes the value $t=1$ if the value of $a=\mathbf{w}^{\mathrm{T}} \phi$ exceeds a threshold, otherwise it takes the value $t=0$. This is equivalent to an activation function given by the cumulative distribution function $f(a)$.

![](https://cdn.mathpix.com/cropped/2024_05_26_5640d2959c04ab9cdc5eg-1.jpg?height=503&width=654&top_left_y=230&top_left_x=948)

\title{
5.4.5 Probit regression
}

We have seen that, for a broad range of class-conditional distributions described by the exponential family, the resulting posterior class probabilities are given by a logistic (or softmax) transformation acting on a linear function of the feature variables. However, not all choices of class-conditional density give rise to such a simple form for the posterior probabilities, which suggests that it might be worth exploring other types of discriminative probabilistic model. Consider the two-class case, again remaining within the framework of generalized linear models, so that

$$
p(t=1 \mid a)=f(a)
$$

where $a=\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}$, and $f(\cdot)$ is the activation function.

One way to motivate an alternative choice for the link function is to consider a noisy threshold model, as follows. For each input $\phi_{n}$, we evaluate $a_{n}=\mathbf{w}^{\mathrm{T}} \phi_{n}$ and then we set the target value according to

$$
\begin{cases}t_{n}=1, & \text { if } a_{n} \geqslant \theta \\ t_{n}=0, & \text { otherwise }\end{cases}
$$

If the value of $\theta$ is drawn from a probability density $p(\theta)$, then the corresponding activation function will be given by the cumulative distribution function

$$
f(a)=\int_{-\infty}^{a} p(\theta) \mathrm{d} \theta
$$

as illustrated in Figure 5.17.

As a specific example, suppose that the density $p(\theta)$ is given by a zero-mean, unit-variance Gaussian. The corresponding cumulative distribution function is given by

$$
\Phi(a)=\int_{-\infty}^{a} \mathcal{N}(\theta \mid 0,1) \mathrm{d} \theta
$$
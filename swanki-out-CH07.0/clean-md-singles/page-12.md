![](https://cdn.mathpix.com/cropped/2024_05_26_3303158b4fe79cdfa9ebg-1.jpg?height=452&width=1055&top_left_y=214&top_left_x=506)

$\mathbf{w}$

Figure 7.4 With a fixed learning rate parameter, gradient descent down a surface with low curvature leads to successively smaller steps corresponding to linear convergence. In such a situation, the effect of a momentum term is like an increase in the effective learning rate parameter.

where $\lambda_{\min }$ is the smallest eigenvalue. If the ratio $\lambda_{\min } / \lambda_{\max }$ (whose reciprocal is known as the condition number of the Hessian) is very small, corresponding to highly elongated elliptical error contours as in Figure 7.3, then progress towards the minimum will be extremely slow.

\title{
7.3.1 Momentum
}

One simple technique for dealing with the problem of widely differing eigenvalues is to add a momentum term to the gradient descent formula. This effectively adds inertia to the motion through weight space and smooths out the oscillations depicted in Figure 7.3. The modified gradient descent formula is given by

$$
\Delta \mathbf{w}^{(\tau-1)}=-\eta \nabla E\left(\mathbf{w}^{(\tau-1)}\right)+\mu \Delta \mathbf{w}^{(\tau-2)}
$$

where $\mu$ is called the momentum parameter. The weight vector is then updated using $(7.15)$.

To understand the effect of the momentum term, consider first the motion through a region of weight space for which the error surface has relatively low curvature, as indicated in Figure 7.4. If we make the approximation that the gradient is unchanging, then we can apply (7.31) iteratively to a long series of weight updates, and then sum the resulting arithmetic series to give

$$
\begin{aligned}
\Delta \mathbf{w} & =-\eta \nabla E\left\{1+\mu+\mu^{2}+\ldots\right\} \\
& =-\frac{\eta}{1-\mu} \nabla E
\end{aligned}
$$

and we see that the result of the momentum term is to increase the effective learning rate from $\eta$ to $\eta /(1-\mu)$.

By contrast, in a region of high curvature in which gradient descent is oscillatory, as indicated in Figure 7.5, successive contributions from the momentum term will
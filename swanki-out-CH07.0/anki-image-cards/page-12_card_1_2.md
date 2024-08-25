## Card 1

![](https://cdn.mathpix.com/cropped/2024_05_26_3303158b4fe79cdfa9ebg-1.jpg?height=452&width=1055&top_left_y=214&top_left_x=506)

What is the impact of adding a momentum term to the gradient descent algorithm according to the image?

%

The impact of adding a momentum term to the gradient descent algorithm is that it can enable a more rapid descent towards the minimum of the error function by effectively increasing the size of the steps and smoothing out their trajectory. This is particularly beneficial when navigating a valley-like shape of the error surface, as it accelerates the optimization process compared to the standard gradient descent which takes smaller, less directed steps.

- #optimization, #machine-learning.gradient-descent, #training-parameters.momentum

---

## Card 2

![](https://cdn.mathpix.com/cropped/2024_05_26_3303158b4fe79cdfa9ebg-1.jpg?height=452&width=1055&top_left_y=214&top_left_x=506)

Explain the effect of low curvature on gradient descent with a fixed learning rate.

%

With a fixed learning rate parameter, gradient descent down a surface with low curvature leads to successively smaller steps, which correspond to linear convergence. This is because the low curvature results in elongated elliptical error contours, making progress towards the minimum extremely slow. The ratio $\lambda_{\min} / \lambda_{\max}$, where $\lambda_{\min}$ is the smallest eigenvalue, indicates how elongated these contours are. A very small ratio (high condition number of the Hessian) exacerbates this effect.

- #optimization, #machine-learning.gradient-descent, #training-parameters.learning-rate
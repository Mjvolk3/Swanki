## How does the value of the regularization parameter $\lambda$ affect the polynomial fit to the data set as shown in Figure 1.9?

![](https://cdn.mathpix.com/cropped/2024_05_18_e829ee8c78472bc3e50eg-1.jpg?height=448&width=1510&top_left_y=208&top_left_x=148)

%

The value of the regularization parameter $\lambda$ significantly impacts the polynomial fit. In Figure 1.9, for $\ln \lambda = -18$ (left plot), the polynomial fit closely follows the data points, indicating effective suppression of overfitting. For $\ln \lambda = 0$ (right plot), the fit shows larger deviations and indicates underfitting due to excessive regularization. The regularization parameter $\lambda$ thus balances the trade-off between overfitting and underfitting.

- #machine-learning, #regularization, #polynomial-fitting

---

## What is the effect of $\lambda = 0$ in the regularized error function for polynomial fitting as per the given image and text?

![](https://cdn.mathpix.com/cropped/2024_05_18_e829ee8c78472bc3e50eg-1.jpg?height=448&width=1510&top_left_y=208&top_left_x=148)

%

When $\lambda = 0$ in the regularized error function for polynomial fitting, the regularization term is completely removed, leading to an unregularized fit that may result in overfitting. This scenario is represented by $\ln \lambda = -\infty$, as shown in figure context. Without regularization, the model fits the noise of the data set more closely, potentially harming its generalization to new data.

$$
\widetilde{E}(\mathbf{w})=\frac{1}{2} \sum_{n=1}^{N}\left\{y\left(x_{n}, \mathbf{w}\right)-t_{n}\right\}^{2}+\frac{\lambda}{2}\|\mathbf{w}\|^{2}
$$

- #machine-learning, #error-function, #polynomial-fitting
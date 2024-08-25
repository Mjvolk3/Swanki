## How do nonlinear basis functions affect linear classification models?

![](https://cdn.mathpix.com/cropped/2024_05_26_f271bce35f2c91024ce0g-1.jpg?height=740&width=1514&top_left_y=221&top_left_x=110)

%

Nonlinear basis functions transform the original input space $\left(x_{1}, x_{2}\right)$ into a feature space $\left(\phi_{1}, \phi_{2}\right)$. In this transformed space, data points from different classes become more separable, allowing for a linear decision boundary, which in logistic regression, leads to a nonlinear decision boundary in the original input space.

- #machine-learning, #classification, #nonlinear-basis-functions

---

## Explain the transformation depicted in Figure 5.15 involving Gaussian basis functions and logistic regression.

![](https://cdn.mathpix.com/cropped/2024_05_26_f271bce35f2c91024ce0g-1.jpg?height=740&width=1514&top_left_y=221&top_left_x=110)

%

The transformation involves applying Gaussian basis functions $\phi_{1}(\mathbf{x})$ and $\phi_{2}(\mathbf{x})$, centered at the green crosses in the input space $\left(x_{1}, x_{2}\right)$. This results in a feature space $\left(\phi_{1}, \phi_{2}\right)$, where logistic regression creates a linear decision boundary, translating into a nonlinear decision boundary in the original input space, as visualized by the separating black curve.

- #machine-learning, #logistic-regression, #basis-function-transformations
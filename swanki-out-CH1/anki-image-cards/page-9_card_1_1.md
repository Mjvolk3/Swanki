## What does Figure 1.5 illustrate in the context of machine learning and polynomial regression?

![](https://cdn.mathpix.com/cropped/2024_05_18_17918633c30415faad8eg-1.jpg?height=599&width=772&top_left_y=223&top_left_x=877)

%

Figure 1.5 illustrates a curve fitting problem in the context of machine learning and polynomial regression. The graph has the horizontal axis representing the input variable $x$ and the vertical axis representing the target variable $t$. Blue points indicate the training data, and a red continuous curve represents the polynomial function $y(x, \mathbf{w})$, which has been fitted to the training data. Green arrows extend vertically from each blue point to the red curve, indicating the displacements (errors) between the actual target values ($t_n$) and the predictions ($y(x_n, \mathbf{w})$). The aim is to adjust the coefficients $\mathbf{w}$ to minimize these displacements.

- #machine-learning, #polynomial-regression, #error-function

## How is the sum-of-squares error function mathematically expressed, and what does it represent?

![](https://cdn.mathpix.com/cropped/2024_05_18_17918633c30415faad8eg-1.jpg?height=599&width=772&top_left_y=223&top_left_x=877)

%

The sum-of-squares error function $E(\mathbf{w})$ is mathematically expressed as:

$$
E(\mathbf{w})=\frac{1}{2} \sum_{n=1}^{N} \left\{y\left(x_{n}, \mathbf{w}\right)-t_{n}\right\}^{2}
$$

It represents the sum of the squares of the displacements of each data point from the fitted function $y(x, \mathbf{w})$, indicated by the green arrows in the figure. This function measures the difference between the predicted values $y\left(x_{n}, \mathbf{w}\right)$ and the actual target values $t_{n}$ for each data point $x_{n}$. The factor of $\frac{1}{2}$ is included for mathematical convenience in derivative calculations.

- #machine-learning, #error-function, #sum-of-squares
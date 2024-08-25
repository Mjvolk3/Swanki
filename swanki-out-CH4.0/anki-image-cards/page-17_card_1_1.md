### Card 1

**How does the regularization parameter $\lambda$ affect the bias and variance in regression models?**

![](https://cdn.mathpix.com/cropped/2024_05_26_d7ac92f7ef61188399a4g-1.jpg?height=1486&width=1518&top_left_y=302&top_left_x=144)

%

In regression models:

- **Large $\lambda$ (e.g., $\ln \lambda = 3$)**: Results in low variance but high bias. The model fits are similar but deviate from the actual function.
- **Moderate $\lambda$ (e.g., $\ln \lambda = 1$)**: Strikes a balance between variance and bias. The model fits show moderate variability and better approximation of the actual function.
- **Small $\lambda$ (e.g., $\ln \lambda = -3$)**: Leads to low bias but high variance. The model fits closely follow the actual function but exhibit substantial differences between each fit, indicating overfitting.

- #statistics.regression, #machine-learning.regularization, #model-complexity.bias-variance

### Card 2

**What does the average fit indicate in the context of model complexity and regularization in regression models?**

![](https://cdn.mathpix.com/cropped/2024_05_26_d7ac92f7ef61188399a4g-1.jpg?height=1486&width=1518&top_left_y=302&top_left_x=144)

%

The average fit (red curve in the right plots) represents the mean response of the model across multiple data sets. Its closeness to the original sinusoidal function (green curve) indicates the overall performance of the model:

- For **large $\lambda$** (top row), the average fit diverges significantly from the sinusoidal function, indicating high bias.
- For **moderate $\lambda$** (middle row), the average fit approximates the sinusoidal function more closely, balancing bias and variance.
- For **small $\lambda$** (bottom row), the average fit follows the sinusoidal function closely, indicating low bias but higher variance and potential overfitting to noise.

- #statistics.regression, #machine-learning.model-performance, #regularization.average-fit
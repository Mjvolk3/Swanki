    
### Card 1

**Linear Regression with Homoskedastic Error Variance**

![](https://cdn.mathpix.com/cropped/2024_06_13_7978c08eaaee0a4861dag-1.jpg?height=331&width=449&top_left_y=240&top_left_x=429)

Explain the concept demonstrated by the following regression model.

% 

The image demonstrates linear regression with homoskedastic error variance, meaning the variance of the prediction errors is constant across all levels of the independent variable $x$. The solid red line represents the mean function $\mu(x) = b + wx$. The parallel green lines depict the predictive interval, typically $\mu(x) \pm 2\sigma$, indicating the variability or uncertainty in the prediction due to the Gaussian noise with fixed variance $\sigma^2$. This interval suggests that approximately 95% of the observed data falls within the interval, assuming normally distributed errors.

- #machine-learning.regression, #statistics.gaussian-distribution, #data-analysis.homoscedasticity

---

### Card 2

**Conditional Density Model for Regression**

![](https://cdn.mathpix.com/cropped/2024_06_13_7978c08eaaee0a4861dag-1.jpg?height=329&width=434&top_left_y=241&top_left_x=1143)

What is the form of the conditional density model used for regression? Define the predicted mean and variance in terms of input variables.

%

The conditional density model used for regression is:

$$
p(y \mid \boldsymbol{x} ; \boldsymbol{\theta}) = \mathcal{N}\left(y \mid f_{\mu}(\boldsymbol{x} ; \boldsymbol{\theta}), f_{\sigma}(\boldsymbol{x} ; \boldsymbol{\theta})^{2}\right)
$$

Here:

- $f_{\mu}(\boldsymbol{x} ; \boldsymbol{\theta}) \in \mathbb{R}$ predicts the mean of the distribution,
- $f_{\sigma}(\boldsymbol{x} ; \boldsymbol{\theta})^{2} \in \mathbb{R}_{+}$ predicts the variance which can be input-dependent.

This model allows the parameters of the Gaussian to be functions of the input variables, thus accommodating heteroscedasticity or varying variances depending on the input $ \boldsymbol{x}$.

- #machine-learning.regression, #statistics.conditional-density, #data-analysis.heteroscedasticity
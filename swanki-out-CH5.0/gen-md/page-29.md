```markdown
## Describe the role of nonlinear basis functions in linear classification models as illustrated in Figure 5.15.

The role of nonlinear basis functions in linear classification models is to transform the original input space $(x_1, x_2)$ into a feature space $(\phi_1, \phi_2)$ where a linear decision boundary can be applied. For instance:

- Left-hand plot: The original input space $(x_1, x_2)$ with red and blue data points and two 'Gaussian' basis functions $\phi_1(\mathbf{x})$ and $\phi_2(\mathbf{x})$ with green centres and contours.
- Right-hand plot: The feature space $(\phi_1, \phi_2)$ with a linear decision boundary obtained by a logistic regression model.

This approach results in a nonlinear decision boundary in the original input space.

- #machine-learning, #nonlinear-basis-functions, #classification-models

## What is the posterior probability of class $\mathcal{C}_{1}$ in logistic regression?

The posterior probability of class $\mathcal{C}_{1}$ in logistic regression can be expressed as:

$$
p(\mathcal{C}_1 | \boldsymbol{\phi}) = y(\boldsymbol{\phi}) = \sigma(\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi})
$$

where $\sigma(\cdot)$ is the logistic sigmoid function, $\mathbf{w}$ is the weight vector, and $\boldsymbol{\phi}$ is the feature vector.

- #statistics, #logistic-regression, #posterior-probability

## Define the logistic sigmoid function used in logistic regression.

The logistic sigmoid function $\sigma(z)$, often used in logistic regression, is defined by:

$$
\sigma(z) = \frac{1}{1 + e^{-z}}
$$

This function maps real-valued numbers into the interval (0, 1), making it suitable for binary classification tasks.

- #statistics, #logistic-regression, #sigmoid-function

## Compare the number of parameters in a logistic regression model to a model fitting Gaussian class-conditional densities.

For an $M$-dimensional feature space $\phi$:

- **Logistic Regression**: Requires $M$ adjustable parameters.
- **Gaussian Class-Conditional Densities**:
  - $2M$ parameters for means.
  - $M(M+1)/2$ parameters for covariance matrix.
  - Together with the class prior $p(\mathcal{C}_1)$, a total of $M(M+5)/2 + 1$ parameters.
  
Logistic regression has a linear dependence on $M$, while Gaussian models grow quadratically with $M$. Thus, logistic regression is more scalable for large $M$.

- #statistics, #logistic-regression, #gaussian-densities

## What simplifies the number of parameters needed in logistic regression compared to Gaussian class-conditional densities?

The logistic regression model reduces the number of parameters by focusing on the linear dependence of the feature vector $\boldsymbol{\phi}$ via the weight vector $\mathbf{w}$. Instead of individually parameterizing class-conditional densities, logistic regression necessitates just $M$ adjustable parameters for an $M$-dimensional feature space $\phi$.

- #statistics, #logistic-regression, #parameter-efficiency

## Why is logistic regression advantageous for a high-dimensional feature space?

Logistic regression is advantageous for a high-dimensional feature space because it scales linearly with the number of dimensions $M$, requiring only $M$ parameters. In contrast, fitting Gaussian class-conditional densities would require $M(M+5)/2 + 1$ parameters, growing quadratically with $M$ and becoming computationally infeasible for large $M$.

- #statistics, #logistic-regression, #high-dimensional-data
```
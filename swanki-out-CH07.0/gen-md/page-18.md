## Describe the purpose of data normalization in the context of gradient descent training.

Data normalization is important in gradient descent training because it helps to ensure that input variables span similar ranges. Without normalization, different input variables can have vastly different ranges, which can cause the training process to be inefficient or even problematic. This is due to the error surface having very different curvatures along different axes, making optimization harder.

- .machine-learning, .data-preprocessing, .gradient-descent

---

## Provide the formulas for calculating the mean $\mu_i$ and variance $\sigma_i^2$ for data normalization.

The mean and variance for a continuous input variable \( x \) can be calculated using the following formulas:

$$
\begin{aligned}
& \mu_{i} = \frac{1}{N} \sum_{n=1}^{N} x_{n i} \\
& \sigma_{i}^{2} = \frac{1}{N} \sum_{n=1}^{N} \left( x_{n i} - \mu_{i} \right)^{2}
\end{aligned}
$$

- .statistical-concepts, .mean-variance, .data-normalization

---

## Explain how input values are re-scaled during data normalization, and provide the formula used.

After calculating the mean and variance, input values are re-scaled to have zero mean and unit variance using the following formula:

$$
\widetilde{x}_{n i} = \frac{x_{n i} - \mu_{i}}{\sigma_{i}}
$$

This transformation ensures that all input values have the same scale, which helps in the gradient descent optimization process.

- .data-preprocessing, .normalization, .gradient-descent

---

## What must be ensured when pre-processing development, validation, or test data in data normalization?

When pre-processing development, validation, or test data, it is crucial to use the same values of $\mu_i$ and $\sigma_i$ that were used for the training data. This ensures that all inputs are scaled consistently and that the model performs correctly on these additional data sets.

- .machine-learning, .data-preprocessing, .consistency

---

## Calculate the mean $\mu_i$ and variance $\sigma_i^2$ if the input data $x_{ni}$ consists of the values 1, 2, 3, 4, and 5.

First, calculate the mean $\mu_i$:

$$
\mu_i = \frac{1}{5} \sum_{n=1}^{5} x_{n i} = \frac{1}{5} (1 + 2 + 3 + 4 + 5) = \frac{15}{5} = 3
$$

Next, calculate the variance $\sigma_i^2$:

$$
\sigma_i^2 = \frac{1}{5} \sum_{n=1}^{5} (x_{n i} - \mu_i)^2 = \frac{1}{5} ((1-3)^2 + (2-3)^2 + (3-3)^2 + (4-3)^2 + (5-3)^2) = \frac{1}{5} (4 + 1 + 0 + 1 + 4) = \frac{10}{5} = 2
$$

- .statistics, .mean-variance, .calculations

---

## Normalize the data values 1, 2, 3, 4, and 5 using the mean and variance calculated previously.

Use the mean $ \mu_i = 3 $ and variance $ \sigma_i^2 = 2 $, thus the standard deviation $ \sigma_i = \sqrt{2} $. The normalized values are:

$$
\begin{aligned}
&\widetilde{x}_{1} = \frac{1 - 3}{\sqrt{2}} = \frac{-2}{\sqrt{2}} = -\sqrt{2} \\
&\widetilde{x}_{2} = \frac{2 - 3}{\sqrt{2}} = \frac{-1}{\sqrt{2}} = -\frac{1}{\sqrt{2}} \\
&\widetilde{x}_{3} = \frac{3 - 3}{\sqrt{2}} = 0 \\
&\widetilde{x}_{4} = \frac{4 - 3}{\sqrt{2}} = \frac{1}{\sqrt{2}} \\
&\widetilde{x}_{5} = \frac{5 - 3}{\sqrt{2}} = \frac{2}{\sqrt{2}} = \sqrt{2}
\end{aligned}
$$

- .statistics, .data-preprocessing, .normalization
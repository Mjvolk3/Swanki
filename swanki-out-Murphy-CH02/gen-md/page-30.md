## Discuss the effect of outliers on fitting Gaussian, Student, and Laplace distributions as illustrated in the paper.

The provided figure demonstrates how outliers impact Gaussian, Student, and Laplace distributions. Specifically:

- (a) Without outliers, the Gaussian and Student distributions are nearly indistinguishable.
- (b) With outliers, the Gaussian distribution is significantly affected, while the Student and Laplace distributions show greater robustness.

$$\text { mean }=\mu, \text { mode }=\mu, \operatorname{var}=\frac{\nu \sigma^{2}}{(\nu-2)}$$

- #statistics, #outliers.impact

## Explain why the Student distribution is more robust to outliers compared to the Gaussian distribution.

The Student distribution is more robust to outliers because its probability density function (pdf) decays as a polynomial function of the squared distance from the center. In contrast, the Gaussian distribution's pdf decays exponentially. This slower decay means more probability mass in the tails, making the Student distribution less sensitive to outliers.

$$\text { mean }=\mu, \text { mode }=\mu, \operatorname{var}=\frac{\nu \sigma^{2}}{(\nu-2)}$$

- #statistics, #robustness.student-distribution

## Describe the conditions under which the variance of the Student distribution is defined and explain its robustness properties.

The variance of the Student distribution is defined only if $\nu > 2$. The distribution is robust to outliers due to its heavy tails, which decay polynomially rather than exponentially. For $\nu \gg 5$, the Student distribution approximates a Gaussian distribution and loses its robustness properties.

$$\operatorname{var}=\frac{\nu \sigma^{2}}{(\nu-2)}$$

- #statistics, #variance.student-distribution

## What happens to the Student distribution as the degrees of freedom (\nu) increases significantly (e.g., \nu \gg 5)?

As the degrees of freedom $\nu$ increase significantly (e.g., $\nu \gg 5$), the Student distribution rapidly approaches a Gaussian distribution and loses its robustness properties against outliers. This is because the heavy tails become less pronounced, making it behave more like a Gaussian distribution.

- #statistics, #degrees.of-freedom.effect

## Define the Cauchy distribution and explain its key characteristics.

The Cauchy distribution, also known as the Lorentz distribution, is defined by:

$$
\mathcal{C}(x \mid \mu, \gamma)=\frac{1}{\gamma \pi}\left[1+\left(\frac{x-\mu}{\gamma}\right)^{2}\right]^{-1}
$$

Key characteristics include:

- Very heavy tails compared to a Gaussian distribution.
- The integral that defines the mean does not converge, highlighting its extremely heavy tails.
- $95\%$ of values from a standard Cauchy distribution lie between -12.7 and 12.7, compared to -1.96 and 1.96 for a standard normal distribution.

- #probability.distribution, #cauchy-distribution

## What happens to the Student distribution when $\nu = 1$?

When $\nu = 1$, the Student distribution is known as the Cauchy or Lorentz distribution. It possesses extremely heavy tails, much heavier than those of a Gaussian distribution. This characteristic highlights its robustness to outliers and the fact that it lacks a defined mean.

$$
\mathcal{C}(x \mid \mu, \gamma)=\frac{1}{\gamma \pi}\left[1+\left(\frac{x-\mu}{\gamma}\right)^{2}\right]^{-1}
$$

- #statistics, #cauchy-distribution.
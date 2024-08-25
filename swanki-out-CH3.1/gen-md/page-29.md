## In the Maximum Likelihood estimation, how is the estimate of \(\theta_0^{\text{ML}}\) represented and derived in terms of sine and cosine functions?
\(\theta_{0}^{\mathrm{ML}}=\tan ^{-1}\left\{\frac{\sum_{n} \sin \theta_{n}}{\sum_{n} \cos \theta_{n}}\right\}\)

The estimate \(\theta_0^{\text{ML}}\) is effectively computed as the argument of an inverse tangent function, which balances the sum of sine and cosine components of observations. This arises geometrically from projecting observations \(\theta_n\) onto a two-dimensional Cartesian space, and evaluating their collective direction, acknowledging statistical central tendency.

- #statistics, #maximum-likelihood-estimation

## What is the relationship between \(I_0^\prime(m)\) and \(I_1(m)\) as utilized in approach (3.131) and why is it applicable in the context of optimizing \(m\)?
\(I_{0}^{\prime}(m) = I_{1}(m)\)

This relationship is crucial for solving the maximization of the likelihood equation (3.131) regarding parameter \(m\). By Abramowitz and Stegun’s reference, the derivative of the zeroth-order modified Bessel function of the first kind, \(I_0\), equals the first-order function, \(I_1\). This derivative relation is necessary to express the derivative of the likelihood in terms of known Bessel functions, facilitating analytic optimization.

- #mathematics, #bessel-functions, #function-relationships

## Define the function \( A(m) \) as used in the analysis of von Mises distribution within the paper.
$$
A(m)=\frac{I_{1}(m)}{I_{0}(m)}
$$

This defines \( A(m) \) as the ratio of the first-order modified Bessel function of the first kind to the zeroth order. The function gauges the concentration of angles around the mean direction in a von Mises distribution, providing an analytical tool to assess the spread of periodic data around a central value.

- #statistics, #data-analysis, #von-mises-distribution

## Demonstrate how \( A\(m_{\text{ML}}\) \) is expressed using trigonometric identity in terms of \(\theta_{0}^{\text{ML}}\) and sine, cosine sums.
$$
A\left(m_{\mathrm{ML}}\right)=\left(\frac{1}{N} \sum_{n=1}^{N} \cos \theta_{n}\right) \cos \theta_{0}^{\mathrm{ML}}+\left(\frac{1}{N} \sum_{n=1}^{N} \sin \theta_{n}\right) \sin \theta_{0}^{\mathrm{ML}}
$$

This expression of \( A(m_{\text{ML}}) \) incorporates the mean cosine and sine of the sample observations, multiplied respectively by the cosine and sine of the estimated parameter \( \theta_0^{\text{ML}} \). This represents a weighted average or resultant vector length in circular statistics, factoring in the mean direction.

- #trigonometry, #statistical-analysis, #circular-statistics

## Discuss multimodality handling in von Mises distributions within the context of the discussed paper.
One limitation of the von Mises distribution is that it is unimodal, which restricts its versatility in modelling data with multiple peaks or modes. To overcome this, the paper suggests forming mixtures of von Mises distributions. This approach provides a more flexible framework for modelling periodic variables, accommodating multimodality through the superposition of multiple von Mises distributions.

- #distributions, #periodic-data-analysis, #multimodality
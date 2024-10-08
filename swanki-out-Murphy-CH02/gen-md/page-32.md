## Describe the gamma distribution and its parameters.

The gamma distribution is a flexible distribution for positive real valued random variables, $x>0$. It is defined in terms of two parameters, called the shape $a>0$ and the rate $b>0$:

$$
\operatorname{Ga}(x \mid \text { shape }=a, \text { rate }=b) \triangleq \frac{b^{a}}{\Gamma(a)} x^{a-1} e^{-x b}
$$

- #gamma-distribution, #probability-distributions

## What is an alternative parameterization of the gamma distribution?

Sometimes the gamma distribution is parameterized in terms of the shape $a$ and the scale $s=1 / b$:

$$
\operatorname{Ga}(x \mid \text { shape }=a, \text { scale }=s) \triangleq \frac{1}{s^{a} \Gamma(a)} x^{a-1} e^{-x / s}
$$

- #gamma-distribution, #probability-distributions

## What are the mean, mode, and variance of the gamma distribution?

For the gamma distribution, we have the following properties:

$$
\text { mean }=\frac{a}{b}, \text { mode }=\frac{a-1}{b}, \text { var }=\frac{a}{b^{2}}
$$

Where $a$ is the shape and $b$ is the rate.

- #gamma-distribution, #probability-distributions

## How is the exponential distribution related to the gamma distribution?

The exponential distribution is a special case of the gamma distribution:

$$
\operatorname{Expon}(x \mid \lambda) \triangleq \operatorname{Ga}(x \mid \text { shape }=1, \text { rate }=\lambda)
$$

This distribution describes the times between events in a Poisson process, which occur continuously and independently at a constant average rate $\lambda$.

- #exponential-distribution, #gamma-distribution, #poisson-process

## How does the mode of a gamma distribution change with the parameter $a$ (shape)?

For a gamma distribution,

- If $a \leq 1$, the mode is at $0$.
- If $a > 1$, the mode is at $\frac{a-1}{b}$.

Generated by:

$$
\operatorname{Ga}(x \mid \text { shape }=a, \text { rate }=b) = \frac{b^{a}}{\Gamma(a)} x^{a-1} e^{-x b}
$$

- #gamma-distribution, #probability-distributions

## What happens to the gamma distribution as the rate $b$ increases?

As the rate $b$ increases, the horizontal scale of the gamma distribution is reduced, thus squeezing everything leftwards and upwards. This effect can be illustrated by plotting different gamma distributions with varying rates $b$.

- #gamma-distribution, #probability-distributions
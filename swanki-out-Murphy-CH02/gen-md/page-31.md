```markdown
## Explain the pdf of the half Cauchy distribution and when it is used. Why is it considered suitable for Bayesian modeling of distributions over positive reals with heavy tails?

The probability density function (pdf) of the half Cauchy distribution is given by:

$$
\mathcal{C}_{+}(x \mid \gamma) \triangleq \frac{2}{\pi \gamma}\left[1+\left(\frac{x}{\gamma}\right)^{2}\right]^{-1}
$$

This distribution is useful in Bayesian modeling when a distribution over positive reals with heavy tails is needed but finite density at the origin.

- #bayesian-modeling, #half-cauchy-distribution, #heavy-tails

## Write out the pdf and the properties (mean, mode, variance) of the Laplace distribution.

The probability density function (pdf) of the Laplace distribution is:

$$
\operatorname{Laplace}(y \mid \mu, b) \triangleq \frac{1}{2b} \exp\left( -\frac{|y - \mu|}{b} \right)
$$

The properties of the Laplace distribution are:
$$
\text { mean } = \mu, \quad \text { mode } = \mu, \quad \text { var } = 2b^2
$$

- #laplace-distribution, #probability, #properties

## Define the beta distribution and express the beta function $B(a, b)$ in terms of the gamma function $\Gamma$.

The beta distribution is defined as follows:

$$
\operatorname{Beta}(x \mid a, b)=\frac{1}{B(a, b)} x^{a-1}(1-x)^{b-1}
$$

The beta function $B(a, b)$ is given by:

$$
B(a, b) \triangleq \frac{\Gamma(a) \Gamma(b)}{\Gamma(a+b)}
$$

- #beta-distribution, #gamma-function, #beta-function

## What are the mean, mode, and variance of the beta distribution in terms of parameters $a$ and $b$?

For the beta distribution, the mean, mode, and variance are given by:

$$
\text { mean } = \frac{a}{a+b}, \quad \text { mode } = \frac{a-1}{a+b-2}, \quad \text { var } = \frac{a b}{(a+b)^2(a+b+1)}
$$

- #beta-distribution, #moments, #parameterization

## Discuss the conditions under which the beta distribution becomes uniform or bimodal.

When $a = b = 1$, the beta distribution becomes uniform. If $a$ and $b$ are both less than 1, the distribution is bimodal with "spikes" at $0$ and $1$.

$$
\operatorname{Beta}(x \mid 1, 1) = 1 \quad \text{(Uniform distribution)}
$$

If $a, b < 1$, $\operatorname{Beta}(x \mid a, b)$ is bimodal.

- #beta-distribution, #uniform-distribution, #bimodal-distribution

## Explain the concept of the Gamma function $\Gamma(a)$ and write down its integral representation.

The Gamma function $\Gamma(a)$ is defined by the integral:

$$
\Gamma(a) \triangleq \int_{0}^{\infty} x^{a-1} e^{-x} \, dx
$$

It generalizes the factorial function to real and complex numbers.

- #gamma-function, #integration, #special-functions
```
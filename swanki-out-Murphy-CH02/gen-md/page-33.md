Below are six Anki cards that address key points from the provided paper chunk, making use of both LaTeX for mathematical expressions and detailed explanations.

---

## What is the definition of the Chi-squared distribution?

The Chi-squared distribution is defined as:

$$
\chi_{\nu}^{2}(x) \triangleq \mathrm{Ga}\left(x \mid \text { shape }=\frac{\nu}{2}, \text { rate }=\frac{1}{2}\right)
$$

where $\nu$ is the degrees of freedom. 

- #statistics, #probability-distribution.chi-squared

---

## How is the Chi-squared distribution related to Gaussian random variables?

If $Z_{i} \sim \mathcal{N}(0,1)$ and $S=\sum_{i=1}^{\nu} Z_{i}^{2}$, then $S \sim \chi_{\nu}^{2}$.

In words, the Chi-squared distribution is the distribution of the sum of squared Gaussian random variables.

- #statistics, #probability-distribution.chi-squared

---

## Define the inverse Gamma distribution.

The inverse Gamma distribution is defined as follows:

$$
\operatorname{IG}(x \mid \text { shape }=a, \text { scale }=b) \triangleq \frac{b^{a}}{\Gamma(a)} x^{-(a+1)} e^{-b / x}
$$

- #statistics, #probability-distribution.inverse-gamma

---

## What are the properties of the inverse Gamma distribution?

The inverse Gamma distribution has the following properties:

$$
\text { mean }=\frac{b}{a-1}, \text { mode }=\frac{b}{a+1}, \text { var }=\frac{b^{2}}{(a-1)^{2}(a-2)}
$$

The mean exists if $a>1$ and the variance exists if $a>2$.

- #statistics, #probability-distribution.inverse-gamma

---

## What is the empirical pdf $\hat{p}_{N}(x)$ and how is it approximated?

For a set of $N$ samples $\mathcal{D}=\left\{x^{(1)}, \ldots, x^{(N)}\right\}$ from a distribution $p(X)$, the empirical pdf is approximated by a set of delta functions (or "spikes") centered on these samples:

$$
\hat{p}_{N}(x)=\frac{1}{N} \sum_{n=1}^{N} \delta_{x^{(n)}}(x)
$$

- #statistics, #empirical-distributions.pdf

---

## Explain how the empirical CDF can be derived from the empirical pdf.

The empirical CDF (cumulative distribution function) can be derived by integrating the empirical pdf $\hat{p}_{N}(x)$. Given $N$ samples, the empirical CDF is a step function that increases by $\frac{1}{N}$ at each sample point $x^{(n)}$.

$$
\hat{F}_{N}(x)=\int_{-\infty}^{x} \hat{p}_{N}(t) \, dt
$$

- #statistics, #empirical-distributions.cdf

---

These cards cover definitions, relationships between distributions, and the process of constructing empirical distributions, as discussed in the provided chunk of the paper.
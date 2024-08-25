```markdown
## What does the delta function distribution satisfy?

The delta function distribution satisfies the sifting property:

$$
\int_{-\infty}^{\infty} f(y) \delta(x-y) dy = f(x)
$$

- #statistics, #integrals.delta-function
```

```markdown
## Write the pdf of the Student's $t$-distribution and define its parameters.

The pdf of the Student's $t$-distribution is given by:

$$
\mathcal{T}\left(y \mid \mu, \sigma^{2}, \nu\right) \propto \left[1 + \frac{1}{\nu}\left(\frac{y - \mu}{\sigma}\right)^{2}\right]^{-\left(\frac{\nu + 1}{2}\right)}
$$

Where:
- $\mu$ is the mean,
- $\sigma > 0$ is the scale parameter,
- $\nu > 0$ is called the degrees of freedom.

- #statistics, #probability.student-t
```

```markdown
## Explain the sensitivity of the Gaussian distribution to outliers and an alternative distribution.

The Gaussian distribution is quite sensitive to outliers. A robust alternative to the Gaussian distribution is the Student's $t$-distribution, which has heavier tails and is less influenced by outliers.

- #statistics, #probability.robust-alternatives
```

```markdown
## What happens to the Student's $t$-distribution as $\nu$ increases?

As the degrees of freedom $\nu$ increase, the Student's $t$-distribution behaves more like a Gaussian distribution.

- #statistics, #probability.student-t
```

```markdown
## What property do the pdfs of the Laplace and Student distributions share? How do they differ?

Both the Laplace and Student distributions are unimodal. However, the Laplace distribution is log-concave for any parameter value, whereas the Student distribution is not log-concave for any parameter value.

- #statistics, #distributions, unimodality
```

```markdown
## What is the relation between the Cauchy distribution and the Student's $t$-distribution?

When $\nu = 1$, the Student's $t$-distribution becomes the Cauchy distribution, which does not have a well-defined mean and variance.

- #statistics, #probability, cauchy-distribution
```
## What is the form of the Gaussian basis functions and can you derive its structure?

A Gaussian basis function is typically expressed in the form:

$$
\phi_j(x) = \exp\left(-\frac{(x-\mu_j)^2}{2s^2}\right)
$$

where $\mu_j$ and $s$ are parameters that control the center and width of the basis function, respectively. To derive the structure, we start with the general form of a Gaussian function centered at $\mu_j$:

$$
\mathcal{N}(x|\mu_j, s^2) = \frac{1}{\sqrt{2\pi s^2}} \exp\left(-\frac{(x-\mu_j)^2}{2s^2}\right)
$$

However, since we are dealing with basis functions, we can ignore the normalizing factor because it is typically accounted for elsewhere in the model. Thus, we obtain the simplified form:

$$
\phi_j(x) = \exp\left(-\frac{(x-\mu_j)^2}{2s^2}\right)
$$

where $\phi_j(x)$ represents the value of the $j$-th basis function evaluated at input $x$.

- #mathematics.basis-functions, #statistics.gaussian

## What are the sigmoidal basis functions and their general equation as mentioned in the document?

The general form of a sigmoidal basis function is defined as follows:

$$\phi_j(x) = \frac{1}{1 + \exp(-a(x - \mu_j))}$$

Where $a$ and $\mu_j$ are parameters. $\mu_j$ controls the position of the sigmoid along the x-axis and $a$ controls the slope of the sigmoid.

- #mathematics.basis-functions, #statistics.sigmoidal-functions

## Interpret the basis function expansion mentioned in the document in the context of Fourier basis.

A Fourier basis function leads to an expansion in sinusoidal functions, typically represented as:

$$
\psi_k(x) = \cos(kx) \quad \text{and} \quad \psi_k(x) = \sin(kx)
$$

where $k$ denotes the frequency of the sinusoid. Each basis function represents a specific frequency and has infinite spatial extent. Fourier basis functions are particularly useful in signal processing due to their ability to represent periodic components.

- #mathematics.basis-functions, #signal-processing.fourier

## Explain the assumption of the target variable $t$ with the additive Gaussian noise model in the context of this chapter.

The target variable $t$ is given by a function $y(\mathbf{x}, \mathbf{w})$ with additive Gaussian noise $\epsilon$. This can be expressed as:

$$
t = y(\mathbf{x}, \mathbf{w}) + \epsilon
$$

where $\epsilon$ is a zero-mean Gaussian random variable with variance $\sigma^{2}$. Therefore, the probability density function for $t$ given $\mathbf{x}$, $\mathbf{w}$, and $\sigma^{2}$ is:

$$
p(t| \mathbf{x}, \mathbf{w}, \sigma^{2}) = \mathcal{N}(t| y(\mathbf{x}, \mathbf{w}), \sigma^{2})
$$

This Gaussian noise model underlies many fitting and estimation techniques, such as the least-squares approach.

- #statistics.likelihood, #mathematics.gaussian

## Why are wavelets significant in terms of basis functions as discussed in Section 4.1.7?

Wavelets are significant in basis functions because they are localized in both space and frequency. This dual localization makes them extremely useful in signal processing applications where inputs often reside on a regular lattice (e.g., time series, images). The orthogonality of wavelets simplifies their application and analysis:

Wavelets possess the following properties:
- Localized in both time (or space) and frequency.
- Mutually orthogonal.
- Useful for analyzing and representing data with localized features.

This dual peaking property allows for efficient representation and analysis of signals that have localized changes, such as sudden spikes or edges.

- #mathematics.basis-functions, #signal-processing.wavelets

## Describe the relationship between the least-squares approach and maximum likelihood estimation as given in the provided document.

In the document, the least-squares approach and maximum likelihood estimation are related under the assumption of Gaussian noise. Minimizing the sum-of-squares error function is equivalent to maximizing the likelihood of the observed data under a Gaussian noise model.

The error function can be represented as:

$$
E(\mathbf{w}) = \sum_{n=1}^{N} (t_n - y(\mathbf{x}_n, \mathbf{w}))^2
$$

Assuming $t = y(\mathbf{x}, \mathbf{w}) + \epsilon$, where $\epsilon \sim \mathcal{N}(0, \sigma^2)$, the likelihood function $p(\mathbf{t}|\mathbf{X}, \mathbf{w}, \sigma^2)$ is Gaussian:

$$
p(\mathbf{t}|\mathbf{X}, \mathbf{w}, \sigma^2) = \prod_{n=1}^{N} \mathcal{N}(t_n | y(\mathbf{x}_n, \mathbf{w}), \sigma^2)
$$

Maximizing this likelihood function corresponds to minimizing the negative log-likelihood, which is proportional to the sum-of-squares error function.

- #statistics.least-squares, #statistics.maximum-likelihood
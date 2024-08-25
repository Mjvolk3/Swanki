## How is the von Mises distribution derived from conditioning a 2D Gaussian on the unit circle?

The von Mises distribution can be derived from a two-dimensional Gaussian distribution by conditioning on the unit circle. Consider a 2D Gaussian with mean vector $\boldsymbol{\mu} = (\mu_1, \mu_2)$ and covariance matrix $\boldsymbol{\Sigma} = \sigma^2 \mathbf{I}$, with density function:

$$
p(x_1, x_2) = \frac{1}{2\pi\sigma^2} \exp \left\{-\frac{(x_1-\mu_1)^2 + (x_2-\mu_2)^2}{2\sigma^2}\right\}
$$

By mapping this distribution onto the unit circle and performing a coordinate transformation to polar coordinates, we limit our analysis to the angular component, $\theta$, leading to a periodic but initially unnormalized distribution dependent only on $\theta$.

- #statistics, #distributions.von-mises, #math.transformation

## How do we convert Cartesian to polar coordinates in the context of deriving the von Mises distribution?

To analyze the distribution along the unit circle, we convert the Cartesian coordinates $(x_1, x_2)$ and the mean vector $\boldsymbol{\mu} = (\mu_1, \mu_2)$ into polar coordinates:
$$
x_1 = r \cos \theta, \quad x_2 = r \sin \theta
$$
and
$$
\mu_1 = r_0 \cos \theta_0, \quad \mu_2 = r_0 \sin \theta_0
$$
This transformation is crucial for substituting into the Gaussian distribution's exponent and focusing on the circular dependency by conditioning on $r = 1$.

- #math.coordinates, #math.transformation.polar-coordinates, #statistics.distributions

## What simplifications occur when substituting polar coordinates into the Gaussian distribution's exponent?

Upon substituting polar transformations into the Gaussian function and conditioning on $r=1$, we focus on the exponent term which transforms as follows:

$$
-\frac{1}{2 \sigma^2}\left\{(1-r_0 \cos(\theta - \theta_0))^2 + (1-r_0 \sin(\theta - \theta_0))^2\right\}
$$

Using trigonometric identities, this simplifies to:
$$
\frac{r_0}{\sigma^2} \cos (\theta - \theta_0) + \text {const}
$$
where 'const' includes terms independent of $\theta$. This highlights the impact of the angular difference $(\theta - \theta_0)$ on distribution shape.

- #math.simplification, #statistics.derivation, #math.trigonometry

## How is the parameter $m$ defined in the context of the von Mises distribution and what significance does it have?

In the derivation of the von Mises distribution, the parameter $m$ is defined as:
$$
m = \frac{r_0}{\sigma^2}
$$
It represents the concentration parameter of the distribution, indicating how tightly the distribution is concentrated around the mean direction $\theta_0$. Larger values of $m$ imply greater concentration (or lower dispersion) around the mean direction.

- #statistics.distributions.von-mises, #math.parameters, #statistics.concentration

## Derive the final expression for the von Mises distribution from the simplified Gaussian exponent considering the unit circle conditioning.

Upon transforming and simplifying the Gaussian's exponent, considering the unit circle ($r=1$), we find the distribution dependent only on $\theta$:
$$
p(\theta \mid \theta_0, m) = \frac{1}{2\pi I_0(m)} \exp \left\{m \cos (\theta - \theta_0)\right\}
$$
$I_0(m)$, the modified Bessel function of the first kind and order zero, serves as the normalizing constant. This expression illustrates the von Mises distribution for circular data, characterized by mean direction $\theta_0$ and concentration parameter $m$.

- #math.final-expression, #statistics.distributions.von-mises, #statistics.normalization
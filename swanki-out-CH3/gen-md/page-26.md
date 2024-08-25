## How are the Cartesian coordinates of the sample mean represented in terms of the average radius $\bar{r}$ and angle $\bar{\theta}$?

Given the coordinates of the individual observations $\mathbf{x}_n = (\cos \theta_n, \sin \theta_n)$ on a unit circle, the Cartesian coordinates of the sample mean can be written as $\overline{\mathbf{x}} = (\bar{r} \cos \bar{\theta}, \bar{r} \sin \bar{\theta})$.

%
This representation facilitates understanding how circular or periodic data behave in a Cartesian coordinate system, commonly used when dealing with averages of vectors positioned on a unit circle.

- #statistics, #data-representation.unit-circle

## How are the Cartesian components $\bar{x}_1$ and $\bar{x}_2$ of the sample mean calculated from individual observations?

The Cartesian components of the sample mean are computed as follows:
$$
\bar{x}_1 = \bar{r} \cos \bar{\theta} = \frac{1}{N} \sum_{n=1}^{N} \cos \theta_n, \quad \bar{x}_2 = \bar{r} \sin \bar{\theta} = \frac{1}{N} \sum_{n=1}^{N} \sin \theta_n
$$

%
This calculation shows the decomposition of the mean vector into its x and y components, which is crucial for further computational and analytical tasks involving mean orientation or central tendency in circular statistics.

- #statistics, #data-representation.vector-components

## How can $\bar{\theta}$ be derived from the sinusoidal components of the vectors?

To find the average angle $\bar{\theta}$ from vectors on a unit circle, one takes the ratio of their y-component sum to their x-component sum and applies the arctangent function:
$$
\bar{\theta} = \tan^{-1}\left(\frac{\sum_{n} \sin \theta_n}{\sum_{n} \cos \theta_n}\right)
$$

%
This result crucially uses the trigonometric identity for tangent, which relates the sine and cosine functions, providing a practical method to compute the central angle from component averages.

- #trigonometry, #data-analysis.mean-estimation

## What are the required properties of a periodic probability density function $p(\theta)$?

A periodic probability density function $p(\theta)$, important in circular statistics, must satisfy three key conditions:
$$
\begin{aligned}
p(\theta) & \geqslant 0 \\
\int_{0}^{2 \pi} p(\theta) \mathrm{d} \theta & =1 \\
p(\theta+2 \pi) & =p(\theta)
\end{aligned}
$$

%
These conditions ensure non-negativity, normalization (integrating to one over a cycle), and periodicity, which are crucial for valid probability distributions on circular or angular domains. These properties ensure that the function behaves consistently when it repeats every $2\pi$ radians.

- #probability, #distributions.periodic-functions

## How does the Gaussian distribution adapt to satisfy the conditions of a periodic function?

To adapt a Gaussian distribution to meet the periodic constraints necessary for circular data analysis, one can consider a Gaussian over two variables $x_1$ and $x_2$ and ensure it satisfies the properties:
$$
\begin{aligned}
p(\theta) & \geqslant 0 \\
\int_{0}^{2 \pi} p(\theta) \mathrm{d} \theta & =1 \\
p(\theta+2 \pi) & =p(\theta)
\end{aligned}
$$

%
This adaptation involves ensuring the distribution is non-negative, integrates to one over a $2\pi$ interval, and repeats its behavior every $2\pi$. By doing so, Gaussian distributions can be utilized in circular statistics, commonly used for data that inherently wrap around a circle, such as angles or time-of-day.

- #probability, #gaussian-distribution.periodic-adaptation
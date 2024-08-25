## How does the von Mises distribution arise from conditioning a 2D Gaussian on the unit circle based on the provided explanation and illustration in Figure 3.10?

![](https://cdn.mathpix.com/cropped/2024_05_13_a727111505627aa0270dg-1.jpg?height=386&width=422&top_left_y=217&top_left_x=1225)

%

The von Mises distribution can be derived by starting with a two-dimensional Gaussian distribution given by

$$
p\left(x_{1}, x_{2}\right)=\frac{1}{2 \pi \sigma^{2}} \exp \left\{-\frac{\left(x_{1}-\mu_{1}\right)^{2}+\left(x_{2}-\mu_{2}\right)^{2}}{2 \sigma^{2}}\right\}
$$

where $\mu_1$ and $\mu_2$ are the mean coordinates and $\sigma^2$ is the variance for both dimensions. When this Gaussian is conditioned on the unit circle (i.e., $x_1$ and $x_2$ satisfy $x_1^2 + x_2^2 = 1$), the result is a distribution that is periodic along the circumference of the circle. This periodic distribution is not normalized and needs adjustment to meet the requirements of a probability distribution, leading to the von Mises distribution form under appropriate transformation and normalization processes.

- #probability-distributions, #von-mises-distribution, #gaussian-distribution

## What is the transformation from Cartesian to polar coordinates used to adjust a 2D Gaussian distribution into the von Mises format, as explained while considering axes in Figure 3.10?

![](https://cdn.mathpix.com/cropped/2024_05_13_a727111505627aa0270dg-1.jpg?height=386&width=422&top_left_y=217&top_left_x=1225)

%

In transitioning from a Gaussian distribution in Cartesian coordinates $(x_1, x_2)$ to a polar representation, we use:

$$
x_{1}=r \cos \theta, \quad x_{2}=r \sin \theta
$$

Applying this for a unit circle ($r=1$), the distribution becomes a function of $\theta$ only. The new form of the distribution along $\theta$ becomes periodic because it repeats values across the circle after every $2\pi$ radians, leading to the von Mises distribution after normalization. This transformation uniquely maps values on the Cartesian grid constrained by $x_1^2 + x_2^2 = 1$ onto a single circular path, making $\theta$ the only variable of concern, which thereby simplifies to a one-dimensional angular distribution exhibiting characteristics of circular statistics.

- #coordinate-transformation, #cartesian-polar-conversion, #circular-statistics
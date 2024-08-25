![](https://cdn.mathpix.com/cropped/2024_05_10_effe402d88fd8f278266g-1.jpg?height=894&width=1394&top_left_y=227&top_left_x=209)

$x_{1}$
![](https://cdn.mathpix.com/cropped/2024_05_10_effe402d88fd8f278266g-1.jpg?height=760&width=398&top_left_y=288&top_left_x=226)

$y_{1}$ $x_{1}$

$y_{1}$ $y_{1}$

Figure 2.13 Illustration of the effect of a change of variables on a probability distribution in two dimensions. The left column shows the transforming of the variables whereas the middle and right columns show the corresponding effects on a Gaussian distribution and on samples from that distribution, respectively.

that arises when changing variables within an integral. The formula (2.77) follows from the fact that the probability mass in region $\Delta \mathrm{x}$ is the same as the probability mass in $\Delta \mathbf{y}$. Once again, we take the modulus to ensure that the density is nonnegative.

We can illustrate this by applying a change of variables to a Gaussian distribution in two dimensions, as shown in the top row in Figure 2.13. Here the transformation Exercise 2.20 from $\mathbf{x}$ to $\mathbf{y}$ is given by

$$
\begin{aligned}
& y_{1}=x_{1}+\tanh \left(5 x_{1}\right) \\
& y_{2}=x_{2}+\tanh \left(5 x_{2}\right)+\frac{x_{1}^{3}}{3}
\end{aligned}
$$

Also shown on the bottom row are samples from a Gaussian distribution in $\mathrm{x}$-space along with the corresponding transformed samples in $\mathbf{y}$-space.
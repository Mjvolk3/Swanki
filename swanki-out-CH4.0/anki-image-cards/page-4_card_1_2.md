### Card 1

**Q: Describe the Gaussian basis functions as shown in the middle plot of the image.**

![](https://cdn.mathpix.com/cropped/2024_05_26_e13468588350511df9e7g-1.jpg?height=438&width=1486&top_left_y=234&top_left_x=134)

%

The center plot displays Gaussian basis functions, described by the equation:
$$
\phi_j(x) = \exp \left\{-\frac{(x-\mu_j)^2}{2s^2}\right\},
$$
where \( \mu_j \) represents the mean (or center) and \( s \) the scale (standard deviation). Each curve resembles a bell-shaped distribution, with different curves centered at different \( \mu_j \) values.

- #machine-learning, #regression, #functions.gaussian

---

### Card 2

**Q: Explain the sigmoidal basis functions depicted on the right plot of the image.**

![](https://cdn.mathpix.com/cropped/2024_05_26_e13468588350511df9e7g-1.jpg?height=438&width=1486&top_left_y=234&top_left_x=134)

%

The sigmoidal basis functions, shown on the right plot, are given by:
$$
\phi_j(x) = \sigma\left(\frac{x-\mu_j}{s}\right), \quad \text{where} \quad \sigma(a) = \frac{1}{1+\exp(-a)},
$$
with \( \mu_j \) indicating the position and \( s \) the scale. These functions exhibit an "S"-shaped curve, transitioning smoothly from 0 to 1, and each curve is horizontally shifted based on different \( \mu_j \) values.

- #machine-learning, #regression, #functions.sigmoidal
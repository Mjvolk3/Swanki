## Describe the three types of basis functions depicted in Figure 4.2.

![](https://cdn.mathpix.com/cropped/2024_05_26_e13468588350511df9e7g-1.jpg?height=438&width=1486&top_left_y=234&top_left_x=134)

%

Figure 4.2 illustrates three different types of basis functions used in linear regression models or simple neural networks:

1. **Polynomial Basis Functions (left):** These functions represent various polynomial equations. They are of the form \( \phi_j(x) = x^j \), where \( j \) varies. The curves range from linear to higher-order polynomials.
   
2. **Gaussian Basis Functions (center):** These are Gaussian functions, typically described by \( \phi_j(x) = \exp \left\{-\frac{(x-\mu_j)^2}{2s^2}\right\} \). Each curve represents a bell-shaped Gaussian distribution centered at different \( x \) values.
   
3. **Sigmoidal Basis Functions (right):** These functions take the form \( \phi_j(x) = \sigma\left(\frac{x-\mu_j}{s}\right) \), where \( \sigma(a) = \frac{1}{1+\exp(-a)} \). The curves are S-shaped sigmoid functions, shifted along the x-axis for different \( \mu_j \) values.

- #mathematics.basis-functions, #linear-regression, #neural-networks

## What is the form of the Gaussian basis function depicted in the center of Figure 4.2?

![](https://cdn.mathpix.com/cropped/2024_05_26_e13468588350511df9e7g-1.jpg?height=438&width=1486&top_left_y=234&top_left_x=134)

%

The Gaussian basis function depicted in the center of Figure 4.2 is typically expressed as:

$$
\phi_j(x) = \exp \left\{-\frac{(x-\mu_j)^2}{2s^2}\right\}
$$

where \( \mu_j \) indicates the central location of the Gaussian function and \( s \) represents the scale of the function.

- #mathematics.gaussian-functions, #regression-models, #basis-functions
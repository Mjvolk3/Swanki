## What does the blue curve in the image represent in the context of Gaussian conditional distribution?

![](https://cdn.mathpix.com/cropped/2024_05_10_0e32f455ec8070cf8fccg-1.jpg?height=681&width=694&top_left_y=221&top_left_x=955)

%

The blue curve represents a Gaussian distribution centered on the vertical line at \( x_0 \), showing the distribution of the target variable \( t \) given the input variable \( x \), denoted as \( p(t | x_0, w, \sigma^2) \). This indicates the probability distribution for the outcome variable \( t \) for a specific \( x \) value \( x_0 \), where \( \sigma^2 \) denotes the variance of the Gaussian distribution. The curve is essential in understanding the conditional probability distribution used in regression analysis to predict the target variable \( t \) based on a given input \( x \) and learned model parameters.

- #statistics, #gaussian-distribution, #regression-analysis

## How is the maximum likelihood solution for the polynomial coefficients \(\mathbf{w}_{\mathrm{ML}}\) determined from the log likelihood function?

![](https://cdn.mathpix.com/cropped/2024_05_10_0e32f455ec8070cf8fccg-1.jpg?height=681&width=694&top_left_y=221&top_left_x=955)

%

To find the maximum likelihood solution for the polynomial coefficients \(\mathbf{w}_{\mathrm{ML}}\), one must maximize the logarithm of the likelihood function, particularly focusing on equation

$$
\ln p\left(\mathbf{t} \mid \mathbf{x}, \mathbf{w}, \sigma^{2}\right) = -\frac{1}{2 \sigma^{2}} \sum_{n=1}^{N}\left\{y\left(x_{n}, \mathbf{w}\right)-t_{n}\right\}^{2} - \frac{N}{2} \ln \sigma^{2} - \frac{N}{2} \ln (2 \pi)
$$

In the maximization process, the terms \(-\frac{N}{2} \ln \sigma^{2}\) and \(-\frac{N}{2} \ln (2 \pi)\) are constants with respect to \( \mathbf{w} \) and hence can be omitted. The focus then shifts to minimizing

$$
\sum_{n=1}^{N}\left\{y\left(x_{n}, \mathbf{w}\right)-t_{n}\right\}^{2}
$$

which essentially is a form of the least squares problem. Thus, \(\mathbf{w}_{\mathrm{ML}}\) is obtained by finding the set of \( \mathbf{w} \) that minimizes the squared error between the predicted values and the actual target values.

- #machine-learning, #maximum-likelihood-estimation, #optimization
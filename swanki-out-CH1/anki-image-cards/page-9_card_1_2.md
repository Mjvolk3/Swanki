### Card 1

![](https://cdn.mathpix.com/cropped/2024_05_18_17918633c30415faad8eg-1.jpg?height=599&width=772&top_left_y=223&top_left_x=877)

What is the formula for the error function depicted in Figure 1.5, and what is its geometrical interpretation?

%

The error function depicted in Figure 1.5 is given by:

$$
E(\mathbf{w}) = \frac{1}{2} \sum_{n=1}^{N} \left\{ y(x_n, \mathbf{w}) - t_n \right\}^2
$$

The geometrical interpretation of this error function is that it is the sum of the squares of the vertical displacements (shown by the green arrows) between the predicted values $y(x_n, \mathbf{w})$ and the actual target values $t_n$ for each data point $x_n$. This would be zero if the function $y(x, \mathbf{w})$ passed exactly through each training data point.

- #machine-learning, #polynomial-regression, #error-function

### Card 2

![](https://cdn.mathpix.com/cropped/2024_05_18_17918633c30415faad8eg-1.jpg?height=599&width=772&top_left_y=223&top_left_x=877)

%
Explain the significance of the factor \( \frac{1}{2} \) in the error function formula.

%

The factor \( \frac{1}{2} \) in the error function formula 

$$
E(\mathbf{w}) = \frac{1}{2} \sum_{n=1}^{N} \left\{ y(x_n, \mathbf{w}) - t_n \right\}^2 
$$

is included for convenience, particularly to simplify the gradient computation. By including this factor, when taking the derivative of the error function with respect to the parameters $\mathbf{w}$, the 2 that appears from differentiating the square term will cancel out the $\frac{1}{2}$ factor, making the resulting expression simpler.

- #machine-learning, #polynomial-regression, #gradient-descent
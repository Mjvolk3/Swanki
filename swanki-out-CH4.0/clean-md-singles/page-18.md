Figure 4.8 Plot of squared bias and variance, together with their sum, corresponding to the results shown in Figure 4.7. Also shown is the average test set error for a test data set size of 1,000 points. The minimum value of (bias) ${ }^{2}+$ variance occurs around $\ln \lambda=0.43$, which is close to the value that gives the minimum error on the test data.

![](https://cdn.mathpix.com/cropped/2024_05_26_a42f38fa62538bcdd4efg-1.jpg?height=544&width=901&top_left_y=214&top_left_x=756)

\title{
Exercises
}

4.1 ( $\star$ ) Consider the sum-of-squares error function given by (1.2) in which the function $y(x, \mathbf{w})$ is given by the polynomial (1.1). Show that the coefficients $\mathbf{w}=\left\{w_{i}\right\}$ that minimize this error function are given by the solution to the following set of linear equations:

$$
\sum_{j=0}^{M} A_{i j} w_{j}=T_{i}
$$

where

$$
A_{i j}=\sum_{n=1}^{N}\left(x_{n}\right)^{i+j}
$$

Here a suffix $i$ or $j$ denotes the index of a component, whereas $(x)^{i}$ denotes $x$ raised to the power of $i$.

4.2 ( $\star$ ) Write down the set of coupled linear equations, analogous to (4.53), satisfied by the coefficients $w_{i}$ that minimize the regularized sum-of-squares error function given by $(1.4)$.

4.3 ( $\star$ ) Show that the tanh function defined by

$$
\tanh (a)=\frac{e^{a}-e^{-a}}{e^{a}+e^{-a}}
$$

and the logistic sigmoid function defined by (4.6) are related by

$$
\tanh (a)=2 \sigma(2 a)-1
$$

Hence, show that a general linear combination of logistic sigmoid functions of the form

$$
y(x, \mathbf{w})=w_{0}+\sum_{j=1}^{M} w_{j} \sigma\left(\frac{x-\mu_{j}}{s}\right)
$$
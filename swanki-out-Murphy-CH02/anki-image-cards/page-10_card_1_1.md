## Understanding the Gaussian Mixture

![](https://cdn.mathpix.com/cropped/2024_06_13_398d6182f58c2c67baf7g-1.jpg?height=329&width=498&top_left_y=239&top_left_x=751)

What does Figure 2.4 illustrate in the context of probability distributions?

%

Figure 2.4 illustrates a mixture of two one-dimensional (1D) Gaussians, given by the equation:

$$
p(x)=0.5 \mathcal{N}(x \mid 0,0.5)+0.5 \mathcal{N}(x \mid 2,0.5)
$$

The graph shows two peaks corresponding to the means (0 and 2) of the Gaussian components, each with a variance of 0.5. The equal mixing coefficients of 0.5 indicate an equal contribution from both components.

- #statistics, #probability-distributions, #gaussian-mixture

## Inner Expectation Property in Probability

![](https://cdn.mathpix.com/cropped/2024_06_13_398d6182f58c2c67baf7g-1.jpg?height=329&width=498&top_left_y=239&top_left_x=751)

What is the property involving the double expectation of a discrete random variable $X$ given another random variable $Y$?

%

The property states that for discrete random variables $X$ and $Y$, the expectation of the conditional expectation of $X$ given $Y$ equals the overall expectation of $X$. This can be expressed as:

$$
\mathbb{E}[ \mathbb{E}[X \mid Y] ] = \mathbb{E}[X]
$$

The proof involves the following steps:

$$
\begin{aligned}
\mathbb{E}_{Y}[\mathbb{E}[X \mid Y]] & =\mathbb{E}_{Y}\left[\sum_{x} x p(X=x \mid Y)\right] \\
& =\sum_{y}\left[\sum_{x} x p(X=x \mid Y=y)\right] p(Y=y)=\sum_{x, y} x p(X=x, Y=y)=\mathbb{E}[X]
\end{aligned}
$$

- #statistics, #expectation, #probability-theory
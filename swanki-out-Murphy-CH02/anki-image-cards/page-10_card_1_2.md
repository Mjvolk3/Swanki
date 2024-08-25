## What does the graph in Figure 2.4 illustrate about the mixture of two 1D Gaussians?

![](https://cdn.mathpix.com/cropped/2024_06_13_398d6182f58c2c67baf7g-1.jpg?height=329&width=498&top_left_y=239&top_left_x=751)

%

The graph in Figure 2.4 illustrates the probability density function (PDF) of a mixture of two one-dimensional Gaussians, represented by the equation:

$$
p(x) = 0.5 \mathcal{N}(x \mid 0, 0.5) + 0.5 \mathcal{N}(x \mid 2, 0.5)
$$

This mixture consists of two Gaussian components with means at 0 and 2, both having a variance of 0.5. The equal mixing coefficients of 0.5 indicate that each component contributes equally to the overall mixture, resulting in a bimodal distribution with two peaks.

- #probability, #statics.bimodal-distributions

---

## Prove that $\mathbb{E}_{Y}[\mathbb{E}[X \mid Y]] = \mathbb{E}[X]$ for discrete random variables $X$ and $Y$.

![](https://cdn.mathpix.com/cropped/2024_06_13_398d6182f58c2c67baf7g-1.jpg?height=329&width=498&top_left_y=239&top_left_x=751)

%

To prove that $\mathbb{E}_{Y}[\mathbb{E}[X \mid Y]] = \mathbb{E}[X]$ for discrete random variables $X$ and $Y$, follow these steps:

1. Start with the law of total expectation:
   $$
   \mathbb{E}_{Y}[\mathbb{E}[X \mid Y]] = \mathbb{E}_{Y}\left[\sum_{x} x p(X=x \mid Y)\right]
   $$

2. Transform the inner expectation:
   $$
   \mathbb{E}_{Y}\left[\sum_{x} x p(X=x \mid Y)\right] = \sum_{y}\left[\sum_{x} x p(X=x \mid Y=y)\right] p(Y=y)
   $$

3. Combine the sums:
   $$
   \sum_{y}\left[\sum_{x} x p(X=x \mid Y=y)\right] p(Y=y) = \sum_{x, y} x p(X=x, Y=y)
   $$

4. Recognize the joint probability $p(X=x, Y=y)$:
   $$
   \sum_{x, y} x p(X=x, Y=y) = \mathbb{E}[X]
   $$

Therefore,
$$
\mathbb{E}_{Y}[\mathbb{E}[X \mid Y]] = \mathbb{E}[X]
$$

- #mathematics.expectation, #probability.law-of-total-expectation
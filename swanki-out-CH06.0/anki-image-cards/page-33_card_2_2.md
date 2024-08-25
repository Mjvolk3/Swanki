## Front of Card 1

![](https://cdn.mathpix.com/cropped/2024_05_26_6a9b15d90f257837d782g-1.jpg?height=425&width=415&top_left_y=234&top_left_x=679)

What do the color-coded curves in plot (b) represent in the context of a mixture density network?

%
The color-coded curves in plot (b) represent the means $\boldsymbol{\mu}_{k}(x)$ for each mixture component $k$, using the same color-coding as the mixing coefficients $\pi_{k}(x)$.

- mixture-density-networks, means, visualization

## Front of Card 2

![](https://cdn.mathpix.com/cropped/2024_05_26_6a9b15d90f257837d782g-1.jpg?height=425&width=415&top_left_y=234&top_left_x=679)

How is the variance of the density function about the conditional average evaluated in this mixture density network?

%
The variance of the density function about the conditional average is evaluated using the formula:

$$
\begin{aligned}
s^{2}(\mathbf{x}) & =\mathbb{E}\left[\|\mathbf{t}-\mathbb{E}[\mathbf{t} \mid \mathbf{x}]\|^{2} \mid \mathbf{x}\right] \\
& =\sum_{k=1}^{K} \pi_{k}(\mathbf{x})\left\{\sigma_{k}^{2}(\mathbf{x})+\left\|\boldsymbol{\mu}_{k}(\mathbf{x})-\sum_{l=1}^{K} \pi_{l}(\mathbf{x}) \boldsymbol{\mu}_{l}(\mathbf{x})\right\|^{2}\right\}.
\end{aligned}
$$

- mixture-density-networks, variance, conditional-average
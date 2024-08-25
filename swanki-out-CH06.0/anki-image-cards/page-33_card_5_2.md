### Anki Card 1

**Q: What does the plot in figure (d) of the provided image illustrate in the context of a mixture density network?**

![](https://cdn.mathpix.com/cropped/2024_05_26_6a9b15d90f257837d782g-1.jpg?height=432&width=418&top_left_y=761&top_left_x=1183)

%

The plot in figure (d) illustrates the approximate conditional mode of the conditional density in a mixture density network. The red points represent the mean of the most probable component (with the largest mixing coefficient) for each value of $\mathbf{x}$. This depicts how the network can predict and represent complex multimodal density functions, beyond just the conditional mean.

- #machine-learning, #neural-networks, #mixture-density-network

### Anki Card 2

**Q: How is the variance of the density function about the conditional average evaluated mathematically in the context of a mixture density network?**

![](https://cdn.mathpix.com/cropped/2024_05_26_6a9b15d90f257837d782g-1.jpg?height=432&width=418&top_left_y=761&top_left_x=1183)

%

The variance of the density function about the conditional average in a mixture density network is evaluated as follows:

$$
\begin{aligned}
s^{2}(\mathbf{x}) & =\mathbb{E}\left[\|\mathbf{t}-\mathbb{E}[\mathbf{t} \mid \mathbf{x}]\|^{2} \mid \mathbf{x}\right] \\
& =\sum_{k=1}^{K} \pi_{k}(\mathbf{x})\left\{\sigma_{k}^{2}(\mathbf{x})+\left\|\boldsymbol{\mu}_{k}(\mathbf{x})-\sum_{l=1}^{K} \pi_{l}(\mathbf{x}) \boldsymbol{\mu}_{l}(\mathbf{x})\right\|^{2}\right\}
\end{aligned}
$$

Here, $\pi_{k}(\mathbf{x})$ represents the mixing coefficients, $\sigma_{k}(\mathbf{x})$ are the variances, and $\boldsymbol{\mu}_{k}(\mathbf{x})$ are the means of the components.

- #machine-learning, #statistical-modeling, #variance
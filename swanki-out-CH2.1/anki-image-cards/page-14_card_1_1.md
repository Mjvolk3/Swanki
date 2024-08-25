## Given the plot of the Gaussian distribution for a variable $x$ shown, what equation corresponds to this distribution and how are $\mu$ and $\sigma$ represented graphically?

![](https://cdn.mathpix.com/cropped/2024_05_10_0b3cce270cab6a31625fg-1.jpg?height=555&width=770&top_left_y=216&top_left_x=890)

% 

The equation represented by the plot is $\mathcal{N}(x|\mu,\sigma^2)$ which indicates the Gaussian (normal) distribution with mean $\mu$ and variance $\sigma^2$. In the graph, $\mu$ is shown as the peak of the bell-shaped curve and $\sigma$ is represented graphically by the horizontal arrow on either side of $\mu$, each part of the arrow extending $\sigma$ units. This two-headed arrow of total length $2\sigma$ represents two standard deviations from the mean, covering roughly 95% of the data distribution if the data follows this Gaussian distribution.

- #statistics, #gaussian-distribution, #plot-interpretation

## Considering two independent variables, derive the relationship of their covariance as a matrix. What simplification occurs for a single vector?

![](https://cdn.mathpix.com/cropped/2024_05_10_0b3cce270cab6a31625fg-1.jpg?height=555&width=770&top_left_y=216&top_left_x=890)

%

For two independent vectors $\mathbf{x}$ and $\mathbf{y}$, we understand independence as their covariance being zero, therefore:

$$
\operatorname{cov}[\mathbf{x}, \mathbf{y}] = \mathbb{E}[\mathbf{x} \mathbf{y}^\mathrm{T}] - \mathbb{E}[\mathbf{x}] \mathbb{E}[\mathbf{y}^\mathrm{T}]
$$

Since they are independent, $\mathbb{E}[\mathbf{x} \mathbf{y}^\mathrm{T}]$ simplifies to $\mathbb{E}[\mathbf{x}] \mathbb{E}[\mathbf{y}^\mathrm{T}]$, rendering the covariance matrix equal to zero.

For a single vector $\mathbf{x}$, the covariance matrix with itself simplifies, denoted as $\operatorname{cov}[\mathbf{x}] \equiv \operatorname{cov}[\mathbf{x}, \mathbf{x}]$, fundamentally focusing on variance calculations within the vector components.

- #covariance, #matrix-derivation, #statistical-independence
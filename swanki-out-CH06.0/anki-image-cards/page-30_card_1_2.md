### Anki Card 1

**Q: Explain the purpose of a mixture density network and how it models the conditional probability density \(p(\mathbf{t} \mid \mathbf{x})\).**

![](https://cdn.mathpix.com/cropped/2024_05_26_fdc10e06182b216dcb8fg-1.jpg?height=442&width=952&top_left_y=221&top_left_x=696)

%

A mixture density network uses a parametric mixture model for the distribution of \(\mathbf{t}\) whose parameters are determined by the outputs of a neural network taking \(\mathbf{x}\) as its input. It models the conditional probability density \(p(\mathbf{t} \mid \mathbf{x})\) as follows:

$$
p(\mathbf{t} \mid \mathbf{x}) = \sum_{k=1}^{K} \pi_{k}(\mathbf{x}) \mathcal{N}\left(\mathbf{t} \mid \boldsymbol{\mu}_{k}(\mathbf{x}), \sigma_{k}^{2}(\mathbf{x})\right)
$$

Here:
- \(\pi_k(\mathbf{x})\) are the mixing coefficients,
- \(\mathcal{N}\left(\mathbf{t} \mid \boldsymbol{\mu}_{k}(\mathbf{x}), \sigma_{k}^{2}(\mathbf{x})\right)\) are Gaussian components whose parameters (\(\boldsymbol{\mu}_k(\mathbf{x})\), \(\sigma_k^{2}(\mathbf{x})\)) depend on \(\mathbf{x}\).

This model is capable of approximating arbitrary conditional distributions.

- #machine-learning, #neural-networks, #mixture-density-network

### Anki Card 2

**Q: Describe the components and structure of the illustrated mixture density network used to predict \( p(t|x) \).**

![](https://cdn.mathpix.com/cropped/2024_05_26_fdc10e06182b216dcb8fg-1.jpg?height=442&width=952&top_left_y=221&top_left_x=696)

%

The mixture density network illustrated can be broken down as follows:

- **Neurons/Nodes:** Represented by blue circles.
- **Input Layer:** At the bottom, nodes \( x_1 \) to \( x_D \), where \( D \) is the dimensionality of the input vector \(\mathbf{x}\).
- **Output Layer:** At the top, nodes \( θ_1 \) to \( θ_K \) correspond to network outputs determining parameters of mixture model components and mixing coefficients.

On the right side, the graph shows:

- **Horizontal Axis:** Represents \( t \).
- **Blue Curves:** Depict individual Gaussian components each with its own mean and variance as output by the neural network.
- **Red Curve:** Summarized mixture distribution, summing all individual components weighted by \(\pi_k(x)\).

This configuration allows for the modeling of a wide range of complex probability distributions of \( t \).

- #machine-learning, #neural-networks, #mixture-density-network
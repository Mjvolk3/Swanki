```markdown
## Describe the weight vector update in mini-batch stochastic gradient descent.

The weight vector is updated using the gradient of the error function over a mini-batch in mini-batch stochastic gradient descent.

$$
\mathbf{w} \leftarrow \mathbf{w} - \eta \nabla E_{n: n+B-1}(\mathbf{w})
$$

- #machine-learning, #optimization.gradient-descent

---

## What is the role of ReLU activation function in the transformation within layer $l$?

The ReLU (Rectified Linear Unit) activation function ensures that any negative inputs are zeroed out while positive inputs remain unchanged.

$$
z_{i}^{(l)} = \operatorname{ReLU}(a_{i}^{(l)})
$$

- #machine-learning, #activation-functions.relu

---

## What are the initial conditions for weights when using a Gaussian distribution in the context of Algorithm 7.2?

The weights are initialized using a Gaussian distribution with mean $0$ and variance $\epsilon^2$.

$$
\mathcal{N}(0, \epsilon^2)
$$

- #machine-learning, .weight-initialization.gaussian

---

## Calculate the variance of the unit outputs $z_i$ in layer $l$ when using a ReLU activation function with Gaussian initialization.

The variance of the unit outputs in layer $l$ is:

$$
\operatorname{var}[z_i^{(l)}] = \frac{M}{2} \epsilon^2 \lambda^2
$$

where $M$ is the number of units sending connections, $\epsilon^2$ is the variance of the Gaussian initialization, and $\lambda^2$ is the variance of the outputs in the previous layer.

- #machine-learning, #activation-functions.relu, .variance.calculation

---

## Explain the importance of ensuring the variance of pre-activations does not decay to zero or grow significantly across layers.

To maintain stable training, the variance of pre-activations should be consistent across layers; otherwise, gradients may vanish or explode, leading to training instability.

$$
\operatorname{var}[z_i^{(l)}] = \frac{M}{2} \epsilon^2 \lambda^2
$$

- #machine-learning, .variance.stability

---

## Derive the expected value of pre-activations $a_i$ in layer $l$ when initialized with a Gaussian distribution.

Given:

$$
a_{i}^{(l)} = \sum_{j=1}^{M} w_{i j} z_{j}^{(l-1)}
$$

The expected value is:

$$
\mathbb{E}[a_i^{(l)}] = 0
$$

since weights $w_{ij}$ are initialized with $\mathcal{N}(0, \epsilon^2)$ and $z_{j}^{(l-1)}$ has zero mean.

- #machine-learning, #weight-initialization.expected-value
```
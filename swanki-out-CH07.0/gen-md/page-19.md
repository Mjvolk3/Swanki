```markdown
## Explain the motivation for using batch normalization in training deep neural networks.

Batch normalization addresses the vanishing and exploding gradient problems, which arise during training very deep neural networks. This problem can be understood through the gradient of an error function $E$ with respect to a parameter in the first layer of the network:

$$
\frac{\partial E}{\partial w_{i}}=\sum_{m} \cdots \sum_{l} \sum_{j} \frac{\partial z_{m}^{(1)}}{\partial w_{i}} \cdots \frac{\partial z_{j}^{(K)}}{\partial z_{l}^{(K-1)}} \frac{\partial E}{\partial z_{j}^{(K)}}
$$

where $z_{j}^{(k)}$ denotes the activation of node $j$ in layer $k$. Batch normalization helps to stabilize this gradient and improve learning.

- #machine-learning, #deep-learning.batch-normalization, #gradient-problems
```

```markdown
## Describe the procedure of normalizing pre-activations in batch normalization.

In batch normalization, pre-activations $a_i$ are normalized. For a mini-batch of size $K$, the procedure involves:

$$
\begin{aligned}
\mu_{i} & =\frac{1}{K} \sum_{n=1}^{K} a_{n i} \\
\sigma_{i}^{2} & =\frac{1}{K} \sum_{n=1}^{K}\left(a_{n i}-\mu_{i}\right)^{2} \\
\widehat{a}_{n i} & =\frac{a_{n i}-\mu_{i}}{\sqrt{\sigma_{i}^{2}+\delta}}
\end{aligned}
$$

where $\mu_i$ is the mean, $\sigma_i^2$ is the variance, and $\delta$ is a small constant to avoid division by zero.

- #machine-learning, #deep-learning.batch-normalization, #statistical-methods
```

```markdown
## What happens to the gradient of an error function when the activation values in a hidden layer vary widely, and how does batch normalization address this?

When activation values in a hidden layer vary widely, the product of the Jacobian terms tends to zero if most have magnitude $<1$ or to infinity if most have magnitude $>1$. This leads to vanishing or exploding gradients:

$$
\frac{\partial E}{\partial w_{i}}=\sum_{m} \cdots \sum_{l} \sum_{j} \frac{\partial z_{m}^{(1)}}{\partial w_{i}} \cdots \frac{\partial z_{j}^{(K)}}{\partial z_{l}^{(K-1)}} \frac{\partial E}{\partial z_{j}^{(K)}}
$$

Batch normalization addresses this by normalizing activation values to have zero mean and unit variance, stabilizing the gradient.

- #machine-learning, #deep-learning.batch-normalization, #gradient-problems
```

```markdown
## Define the terms $\mu_i$, $\sigma_i^2$, and $\widehat{a}_{n i}$ in the context of batch normalization.

In batch normalization, for a mini-batch of size $K$, the terms are defined as follows:

$$
\begin{aligned}
\mu_{i} & = \frac{1}{K} \sum_{n=1}^{K} a_{n i} \quad \text{(mean)} \\
\sigma_{i}^{2} & = \frac{1}{K} \sum_{n=1}^{K} \left(a_{n i} - \mu_{i}\right)^{2} \quad \text{(variance)} \\
\widehat{a}_{n i} & = \frac{a_{n i} - \mu_{i}}{\sqrt{\sigma_{i}^{2} + \delta}} \quad \text{(normalized activation)}
\end{aligned}
$$

where $a_{n i}$ is the pre-activation value and $\delta$ is a small constant.

- #machine-learning, #deep-learning.batch-normalization, #statistical-methods
```

```markdown
## In batch normalization, how often must the normalization of hidden unit values be repeated during training?

Unlike normalization of the input values, which can be done once prior to the start of training, normalization of the hidden unit values must be repeated during training every time the weight values are updated. This is to ensure that the values are always appropriately scaled during the entire training process.

- #machine-learning, #deep-learning.batch-normalization, #training-methods
```

```markdown
## Why is a small constant $\delta$ included in the denominator of the normalized activation equation in batch normalization?

The small constant $\delta$ in the equation

$$
\widehat{a}_{n i} = \frac{a_{n i} - \mu_{i}}{\sqrt{\sigma_{i}^{2} + \delta}}
$$

is included to avoid numerical issues in situations where the variance $\sigma_{i}^{2}$ is very small, thereby preventing division by zero or extremely large values.

- #machine-learning, #deep-learning.batch-normalization, #numerical-stability
```
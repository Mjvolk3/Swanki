```markdown
## What is the normalized probability expression $p_c$ in the softmax distribution?

The normalized probability $p_c$ in the softmax distribution is given by:

$$
p_{c} = \frac{e^{a_{c}}}{Z(\boldsymbol{a})}
$$

where

$$
Z(\boldsymbol{a}) = \sum_{c^{\prime}=1}^{C} e^{a_{c^{\prime}}}
$$

In this context, $\boldsymbol{a} = f(\boldsymbol{x} ; \boldsymbol{\theta})$ are the logits.

- #machine-learning, #softmax-distribution, #normalization

## What is the purpose of the log-sum-exp (LSE) trick?

The log-sum-exp (LSE) trick is used to avoid numerical problems when computing the partition function $Z$, especially with large or small logits. The LSE trick is expressed as:

$$
\log \sum_{c=1}^{C} \exp \left(a_{c}\right) = m+\log \sum_{c=1}^{C} \exp \left(a_{c}-m\right)
$$

where $m = \max_{c} a_{c}$ ensures that the largest value exponentiated will be zero.

- #machine-learning, #log-sum-exp, #numerical-stability

## How is the LSE function implemented?

The LSE function is defined as:

$$
\operatorname{lse}(\boldsymbol{a}) \triangleq \log \sum_{c=1}^{C} \exp \left(a_{c}\right)
$$

This transformation helps maintain numerical stability by reducing the chance of overflow or underflow.

- #machine-learning, #log-sum-exp, #function-implementation

## How do we compute probabilities from logits using the LSE trick?

Using the LSE trick, probabilities from logits can be computed as:

$$
p(y=c \mid \boldsymbol{x}) = \exp \left(a_{c} - \operatorname{lse}(\boldsymbol{a})\right)
$$

This methodology ensures numerical stability while converting logits to probabilities.

- #machine-learning, #logits, #probability-computation

## What is the cross-entropy loss formula $\mathcal{L}$ for one example in binary classification?

The cross-entropy loss $\mathcal{L}$ for one example in binary classification is given by:

$$
\mathcal{L} = - \left[\mathbb{I}(y=0) \log p_{0} + \mathbb{I}(y=1) \log p_{1} \right]
$$

where $\mathbb{I}$ is the indicator function.

- #machine-learning, #cross-entropy-loss, #binary-classification

## How can the log probabilities $\log p_1$ and $\log p_0$ be expressed in terms of logits for numerical stability?

The log probabilities $\log p_1$ and $\log p_0$ in terms of logits can be written as:

$$
\begin{aligned}
& \log p_{1} = \log \left(\frac{1}{1 + \exp(-a)}\right) = -\operatorname{lse}([0, -a]) \\
& \log p_{0} = -\operatorname{lse}([0, a])
\end{aligned}
$$

- #machine-learning, #logits, #log-probabilities
```
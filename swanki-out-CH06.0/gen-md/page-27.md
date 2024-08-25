```anki
## If we have $K$ separate binary classifications to perform with a network having $K$ outputs, what function represents the conditional distribution of the targets?

The conditional distribution of the targets is given by:

$$
p(\mathbf{t} \mid \mathbf{x}, \mathbf{w})=\prod_{k=1}^{K} y_{k}(\mathbf{x}, \mathbf{w})^{t_{k}}\left[1-y_{k}(\mathbf{x}, \mathbf{w})\right]^{1-t_{k}}
$$

Here:
- $p(\mathbf{t} \mid \mathbf{x}, \mathbf{w})$ is the conditional probability of the target vector $\mathbf{t}$ given input vector $\mathbf{x}$ and weights $\mathbf{w}$.
- $y_{k}(\mathbf{x}, \mathbf{w})$ is the output of the $k^{th}$ neuron with logistic-sigmoid activation for input $\mathbf{x}$.
- $t_{k} \in\{0,1\}$ is the binary class label associated with the $k^{th}$ output.

- #neural-networks, #probability, #binary-classification
```

```anki
## What is the error function derived from the negative logarithm of the likelihood function for $K$ binary classifications?

The error function is:

$$
E(\mathbf{w})=-\sum_{n=1}^{N} \sum_{k=1}^{K}\left\{t_{n k} \ln y_{n k}+\left(1-t_{n k}\right) \ln \left(1-y_{n k}\right)\right\}
$$

Here:
- $E(\mathbf{w})$ is the error function.
- $y_{n k}$ denotes $y_{k}\left(\mathbf{x}_{n}, \mathbf{w}\right)$, the output of the $k^{th}$ neuron for the $n^{th}$ input.
- $t_{n k}$ is the binary class label for the $k^{th}$ output and $n^{th}$ input.

- #neural-networks, #error-function, #binary-classification
```

```anki
## Explain the softmax function used in multiclass classification and how it relates to the output-unit activation.

The softmax function is defined as:

$$
y_{k}(\mathbf{x}, \mathbf{w})=\frac{\exp \left(a_{k}(\mathbf{x}, \mathbf{w})\right)}{\sum_{j} \exp \left(a_{j}(\mathbf{x}, \mathbf{w})\right)}
$$

Here:
- $y_{k}(\mathbf{x}, \mathbf{w})$ is the probability of class $k$ given input $\mathbf{x}$ and weights $\mathbf{w}$.
- $a_{k}(\mathbf{x}, \mathbf{w})$ is the pre-activation of the $k^{th}$ unit.
- The softmax function ensures that the probabilities sum to 1 and each $y_{k}$ lies between 0 and 1.

The softmax function is used to convert the pre-activation values into probabilities for multiclass classification.

- #neural-networks, #multiclass-classification, #softmax
```

```anki
## What is the error function in multiclass classification given the network outputs and binary target variables with 1-of-$K$ coding scheme?

The error function for multiclass classification is:

$$
E(\mathbf{w})=-\sum_{n=1}^{N} \sum_{k=1}^{K} t_{k n} \ln y_{k}\left(\mathbf{x}_{n}, \mathbf{w}\right)
$$

Here:
- $E(\mathbf{w})$ is the error function.
- $t_{k n}$ is a binary variable indicating whether the $n^{th}$ input belongs to the $k^{th}$ class.
- $y_{k}\left(\mathbf{x}_{n}, \mathbf{w}\right)$ is the output probability for class $k$ given input $\mathbf{x}_{n}$.

- #neural-networks, #error-function, #multiclass-classification
```

```anki
## When dealing with a flipped value $t$ in Exercise 6.15, what can be set in advance or treated as a hyperparameter to be inferred from data? 

In Exercise 6.15, the value of $\epsilon$ can be set in advance or treated as a hyperparameter to be inferred from the data.

Here:
- $\epsilon$ represents the noise parameter related to the probability of flipping the target value $t$.
- Setting $\epsilon$ involves prior knowledge or experience.
- Treating $\epsilon$ as a hyperparameter allows its value to be optimized based on the data.

- #probability, #hyperparameters, #classification
```

```anki
## Explain the degeneracy issue with the softmax function and how it can be resolved.

The degeneracy issue with the softmax function arises because the $y_{k}(\mathbf{x}, \mathbf{w})$ are unchanged if a constant is added to all of the $a_{k}(\mathbf{x}, \mathbf{w})$. This causes the error function to be constant for some directions in weight space.

To resolve this degeneracy, an appropriate regularization term can be added to the error function, which penalizes large weights and discourages this invariance.

- #neural-networks, #softmax, #regularization
```
## What is the relationship between the likelihood function and the sum-of-squares error function in the context of minimizing with respect to weights?

The task of maximizing the likelihood function with respect to the weights is equivalent to minimizing the sum-of-squares error function:

$$
E(\mathbf{w})=\frac{1}{2} \sum_{n=1}^{N}\left\|\mathbf{y}\left(\mathbf{x}_{n}, \mathbf{w}\right)-\mathbf{t}_{n}\right\|^{2}
$$

This result is derived by following the same argument as for a single target variable. 

- #probability, #optimization.sum-of-squares-error

---

## How is the noise variance defined in the context of sum-of-squares error minimization?

The noise variance $\sigma^2$ in the context of minimizing the sum-of-squares error function is:

$$
\sigma^{2 \star}=\frac{1}{N K} \sum_{n=1}^{N}\left\|\mathbf{y}\left(\mathbf{x}_{n}, \mathbf{w}^{\star}\right)-\mathbf{t}_{n}\right\|^{2}
$$

Where $K$ is the dimensionality of the target variable $ \mathbf{t} $.

- #statistics, #probability.noise-variance

---

## Show the relationship between the error function’s gradient and the output-unit activation function in regression.

In regression, the network can be viewed as having an identity output activation function, making $y_{k}=a_{k}$. The gradient of the sum-of-squares error function is:

$$
\frac{\partial E}{\partial a_{k}}=y_{k}-t_{k}
$$

This implies that the gradient of the error with respect to the activation $a_{k}$ is simply the error between the output $y_{k}$ and the target $t_{k}$.

- #machine-learning, #regression.gradient

---

## Describe the error function for binary classification using a logistic sigmoid activation function.

For a binary classification problem where $t = 1$ denotes class $\mathcal{C}_{1}$ and $t = 0$ denotes class $\mathcal{C}_{2}$, the error function (cross-entropy error) is given by:

$$
E(\mathbf{w})=-\sum_{n=1}^{N}\left\{t_{n} \ln y_{n}+\left(1-t_{n}\right) \ln \left(1-y_{n}\right)\right\}
$$

Here, $y_{n}$ denotes $y\left(\mathbf{x}_{n}, \mathbf{w}\right)$.

- #machine-learning, #classification.binary-classification
    
---

## What is the form of the conditional distribution of targets given inputs in binary classification?

The conditional distribution of targets $t$ given inputs $\mathbf{x}$ in binary classification, assuming a logistic sigmoid activation function, is a Bernoulli distribution of the form:

$$
p(t \mid \mathbf{x}, \mathbf{w})=y(\mathbf{x}, \mathbf{w})^{t}\{1-y(\mathbf{x}, \mathbf{w})\}^{1-t}
$$

Here, $y(\mathbf{x}, \mathbf{w})$ represents the conditional probability $p(\mathcal{C}_{1} | \mathbf{x})$.

- #probability, #classification.bernoulli-distribution

---

## How can the cross-entropy error function improve classification problems compared to the sum-of-squares error function?

Using the cross-entropy error function instead of the sum-of-squares for a classification problem leads to faster training and improved generalization as found by Simard, Steinkraus, and Platt (2003).

$$
E(\mathbf{w})=-\sum_{n=1}^{N}\left\{t_{n} \ln y_{n}+\left(1-t_{n}\right) \ln \left(1-y_{n}\right)\right\}
$$

The cross-entropy error better aligns with the probabilistic interpretation of classification problems.

- #machine-learning, #optimization.cross-entropy
## What transformation does the softmax function perform over its inputs?

The softmax function maps $\mathbb{R}^{C}$ to $[0, 1]^{C}$, ensuring that $0 \leq \operatorname{softmax}(\boldsymbol{a})_{c} \leq 1$ and $\sum_{c=1}^{C} \operatorname{softmax}(\boldsymbol{a})_{c} = 1$.

- #machine-learning, #logistic-regression, #softmax-function

## How does the softmax function behave as the temperature $T$ approaches zero?

The softmax function behaves as follows when the temperature $T$ approaches zero:

$$
\operatorname{softmax}(\boldsymbol{a} / T)_{c} = \begin{cases}1.0 & \text { if } c=\operatorname{argmax}_{c^{\prime}} a_{c^{\prime}} \\ 0.0 & \text { otherwise }\end{cases}
$$

As $T \rightarrow 0$, the distribution concentrates most of its probability mass in the most probable state (winner takes all).

- #machine-learning, #softmax-function, #temperature

## What is the final model for multiclass logistic regression using a linear predictor?

The final model for multiclass logistic regression using a linear predictor $f(\boldsymbol{x}; \boldsymbol{\theta}) = \mathbf{W} \boldsymbol{x} + \boldsymbol{b}$ becomes:

$$
p(y \mid \boldsymbol{x}; \boldsymbol{\theta}) = \operatorname{Cat}(y \mid \operatorname{softmax}(\mathbf{W} \boldsymbol{x}+\boldsymbol{b}))
$$

- #machine-learning, #logistic-regression, #multiclass

## How can the probability $p(y=c \mid \boldsymbol{x}; \boldsymbol{\theta})$ for multinomial logistic regression be written in terms of logits $\boldsymbol{a}$?

For multinomial logistic regression, the probability can be written as:

$$
p(y=c \mid \boldsymbol{x}; \boldsymbol{\theta}) = \frac{e^{a_{c}}}{\sum_{c^{\prime}=1}^{C} e^{a_{c^{\prime}}}}
$$

where $\boldsymbol{a} = \mathbf{W} \boldsymbol{x} + \boldsymbol{b}$.

- #machine-learning, #logistic-regression, #multinomial

## Under what condition does multinomial logistic regression reduce to binary logistic regression?

Multinomial logistic regression reduces to binary logistic regression if there are only two classes ($C = 2$). The softmax function for two classes simplifies as follows:

$$
\operatorname{softmax}(\boldsymbol{a})_{0} = \frac{e^{a_{0}}}{e^{a_{0}} + e^{a_{1}}} = \frac{1}{1 + e^{a_{1} - a_{0}}} = \sigma(a_{0} - a_{1})
$$

Thus, we can train the model to predict $a = a_{1} - a_{0}$.

- #machine-learning, #logistic-regression, #binary

## Why is a model using two weight vectors $\boldsymbol{w}_{0}$ and $\boldsymbol{w}_{1}$ considered over-parameterized in binary logistic regression?

Using two weight vectors $\boldsymbol{w}_{0}$ and $\boldsymbol{w}_{1}$ in binary logistic regression is considered over-parameterized because:

$$
\sigma(a_{0} - a_{1})
$$

can be learned using just a single weight vector $\boldsymbol{w}$. The use of two weight vectors (one per class) can lead to redundant parameters, which may hurt interpretability, even though the predictions will remain the same.

- #machine-learning, #logistic-regression, #over-parameterization
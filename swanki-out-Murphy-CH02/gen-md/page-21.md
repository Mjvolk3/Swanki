## Discuss the formula for the probability in logistic regression.

The formula for the probability in logistic regression is:

$$
p(y=1 \mid \boldsymbol{x} ; \boldsymbol{\theta})=\sigma\left(\boldsymbol{w}^{\top} \boldsymbol{x}+b\right)=\frac{1}{1+e^{-\left(\boldsymbol{w}^{\top} \boldsymbol{x}+b\right)}}
$$

## What do the variables $\boldsymbol{w}$, $\boldsymbol{x}$, and $b$ represent in logistic regression?

The variable $\boldsymbol{w}$ represents the weight vector, $\boldsymbol{x}$ is the feature vector, and $b$ is the bias term. These parameters are used to compute the linear combination $\boldsymbol{w}^{\top} \boldsymbol{x}+b$, which is then passed through the sigmoid function $\sigma(z) = \frac{1}{1+e^{-z}}$ to produce the probability.

- #math, #logistic-regression.variables-interpretation

## What is the significance of the decision boundary in logistic regression?

The decision boundary in logistic regression is the value $x^{*}$ where the probability $p(y=1 \mid x=x^{*}, \boldsymbol{\theta})$ equals 0.5. In the given example from the iris dataset, $x^{*} \approx 1.7$. This boundary helps in making classification decisions.

- #math, #logistic-regression.decision-boundary

## Explain why linear regression is inappropriate for binary classification problems.

Linear regression yields probabilities that can exceed 1 or drop below 0 as the feature values move far enough in either direction, which is inappropriate for binary classification. Logistic regression addresses this by ensuring the probabilities stay between 0 and 1 through the sigmoid function.

- #math, #regression.linear-vs-logistic

## Define the categorical distribution and provide its equation.

The categorical distribution is a discrete probability distribution for a finite set of labels $y \in\{1, \ldots, C\}$.

$$
\operatorname{Cat}(y \mid \boldsymbol{\theta}) \triangleq \prod_{c=1}^{C} \theta_{c}^{\mathbb{I}(y=c)}
$$

This means $p(y=c \mid \boldsymbol{\theta})=\theta_{c}$, where the parameters are constrained by $0 \leq \theta_{c} \leq 1$ and $\sum_{c=1}^{C} \theta_{c}=1$.

- #probability, #distributions.categorical

## How can we represent the categorical distribution using a one-hot vector?

We can represent the categorical distribution using a one-hot vector $\boldsymbol{y}$, where $y_{c}$ denotes the presence of class $c$ (1 if present, 0 otherwise).

$$
\operatorname{Cat}(\boldsymbol{y} \mid \boldsymbol{\theta}) \triangleq \prod_{c=1}^{C} \theta_{c}^{y_{c}}
$$

This helps in encoding class labels for easier mathematical manipulation.

- #probability, #distributions.one-hot-encoding 

## What is the relationship between the categorical distribution and multinomial distribution?

The categorical distribution is a special case of the multinomial distribution. Suppose we observe $N$ categorical trials $y_{n} \sim \operatorname{Cat}(\cdot \mid \boldsymbol{\theta})$ for $n=1:N$, it leads to the vector $\boldsymbol{y}$ which counts the occurrences of each class.

$$
\operatorname{Cat}(\boldsymbol{y} \mid \boldsymbol{\theta}) \triangleq \prod_{c=1}^{C} \theta_{c}^{y_{c}} \text{ for one trial}
$$

- #probability, #distributions.categorical-vs-multinomial
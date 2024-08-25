```markdown
## What is the chain rule of probability for $D$ variables?

To find the joint distribution of $D$ variables using the chain rule of probability, we extend the product rule:

$$
p\left(\boldsymbol{x}_{1: D}\right)=p\left(x_{1}\right) p\left(x_{2} \mid x_{1}\right) p\left(x_{3} \mid x_{1}, x_{2}\right) p\left(x_{4} \mid x_{1}, x_{2}, x_{3}\right) \ldots p\left(x_{D} \mid \boldsymbol{x}_{1: D-1}\right)
$$

The chain rule of probability allows us to construct high dimensional joint distributions from a set of conditional distributions. Each term in the product represents a conditional probability of a variable given the preceding ones. 


- #probability, #chain-rule
```
```markdown
## How many parameters are needed to define the joint distribution of two discrete random variables, $X$ and $Y$, under the assumption of independence?

For two discrete random variables, $X$ with 6 states and $Y$ with 5 states, assuming independence simplifies the parameter estimation:

$$p(x, y) = p(x) p(y)$$

A general joint distribution would need $(6 \times 5) - 1 = 29$ parameters due to the sum-to-one constraint. With independence, we only need $(6-1) + (5-1) = 9$ parameters.

This significant reduction in parameters is due to the assumption that $X$ and $Y$ do not influence each other.

- #probability,  #independence
```
```markdown
## What does it mean for two variables $X$ and $Y$ to be unconditionally or marginally independent?

Two variables $X$ and $Y$ are unconditionally or marginally independent (denoted $X \perp Y$) if the joint probability can be written as a product of their marginals:

$$X \perp Y \Longleftrightarrow p(X, Y) = p(X) p(Y)$$

This means the occurrence of $X$ does not affect the occurrence of $Y$ and vice versa.

- #probability, #independence
```
```markdown
## What defines mutual independence among a set of variables $X_{1}, \ldots, X_{n}$?

A set of variables $X_{1}, \ldots, X_{n}$ is considered mutually independent if the joint probability can be decomposed into the product of the individual marginals for all subsets $\left\{X_{1}, \ldots, X_{m}\right\} \subseteq \left\{X_{1}, \ldots, X_{n}\right\}$:

$$
p\left(X_{1}, \ldots, X_{m}\right) = \prod_{i=1}^{m} p\left(X_{i}\right)
$$

For example, if $X_{1}, X_{2}, X_{3}$ are mutually independent, then:

$$
p\left(X_{1}, X_{2}, X_{3}\right) = p\left(X_{1}\right) p\left(X_{2}\right) p\left(X_{3}\right),
$$
$$
p\left(X_{1}, X_{2}\right) = p\left(X_{1}\right) p\left(X_{2}\right),
$$
$$
p\left(X_{2}, X_{3}\right) = p\left(X_{2}\right) p\left(X_{3}\right),
$$
$$
p\left(X_{1}, X_{3}\right) = p\left(X_{1}\right) p\left(X_{3}\right)
$$

Each condition ensures that every subset of the variables is independent of the others.

- #probability, #mutual-independence
```
```markdown
## How is conditional independence defined between variables $X$ and $Y$ given $Z$?

Conditional independence between $X$ and $Y$ given $Z$ (denoted $X \perp Y \mid Z$) means that the conditional joint probability can be factored into the product of the conditional marginals:

$$X \perp Y \mid Z \Longleftrightarrow p(X, Y \mid Z) = p(X \mid Z) p(Y \mid Z)$$

This states that $X$ and $Y$ are independent given that $Z$ is known.

- #probability, #conditional-independence
```
```markdown
## Explain with an example how unconditional independence is rare and how conditional independence is more practical.

Unconditional independence is rare in practice because most variables can influence each other. However, this influence is often indirect and mediated via other variables. 

For instance, suppose $X$ and $Y$ represent two health conditions that are both influenced by a third variable $Z$ (such as age). Although $X$ and $Y$ are not unconditionally independent, knowing $Z$ might render them conditionally independent:

$$X \perp Y \mid Z \Rightarrow p(X, Y \mid Z) = p(X \mid Z) p(Y \mid Z)$$

This conditional independence is more useful and practical in analyzing real-world scenarios where direct influence is mediated by other factors.

- #probability, #conditional-independence
```
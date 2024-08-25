```markdown
## What is the empirical distribution $\hat{P}_{N}(x)$ for a dataset $\mathcal{D}$ with $N$ samples?

The empirical distribution of the dataset $\mathcal{D}$ is defined as:

$$
\hat{P}_{N}(x)=\frac{1}{N} \sum_{n=1}^{N} \mathbb{I}\left(x^{(n)} \leq x\right)=\frac{1}{N} \sum_{n=1}^{N} u_{x^{(n)}}(x)
$$

where $u_{y}(x)$ is a step function at $y$.

- #probability, #empirical-distribution
---
## Give the definition of the step function $u_{y}(x)$.

The step function $u_{y}(x)$ is defined by:

$$
u_{y}(x)= \begin{cases}1 & \text { if } x \geq y \\ 0 & \text { if } x < y\end{cases}
$$

- #probability, #step-function
---
## What is the pmf of $Y$, $p_{y}(y)$, if $X$ is a discrete random variable and $\boldsymbol{y}=f(\boldsymbol{x})$ is a deterministic transformation?

If $X$ is a discrete random variable and $\boldsymbol{y}=f(\boldsymbol{x})$ is a deterministic transformation, the pmf for $Y$ is:

$$
p_{y}(y)=\sum_{x: f(x)=y} p_{x}(x)
$$

- #probability, #random-variables.transformation
---
## If $f(X)=1$ if $X$ is even and $f(X)=0$ otherwise, and $p_{x}(X)$ is uniform on the set $\{1, \ldots, 10\}$, what is $p_{y}(1)$?

Given $f(X)=1$ if $X$ is even and $f(X)=0$ otherwise, and $p_{x}(X)$ is uniform on the set $\{1, \ldots, 10\}$, then:

$$
p_{y}(1)=\sum_{x \in \{2,4,6,8,10\}} p_{x}(x)=0.5
$$

- #probability, #random-variables.transformation
---
## How is the cdf of a continuous random variable $Y=p(\boldsymbol{y})$ derived from $X$?

For a continuous random variable $X$ and $Y=f(\boldsymbol{x})$ as a deterministic transformation, the cdf of $Y$ is:

$$
P_{y}(y) \triangleq \operatorname{Pr}(Y \leq y)=\operatorname{Pr}(f(X) \leq y)=\operatorname{Pr}(X \in \{x \mid f(x) \leq y\})
$$

- #probability, #cdf.transformation
---
## How can we derive the pdf of a continuous random variable $y$ if the transformation function $f$ is invertible?

If the transformation function $f$ is invertible, the pdf of $y$ can be derived by differentiating the cdf:

$$
p_{y}(y) = \frac{d}{dy} P_{y}(y) 
$$

- #probability, #pdf.transformation
```
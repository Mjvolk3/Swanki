This is called the empirical distribution of the dataset $\mathcal{D}$. An example of this, with $N=5$, is shown in Figure 2.18(a).

The corresponding cdf is given by

$$
\hat{P}_{N}(x)=\frac{1}{N} \sum_{n=1}^{N} \mathbb{I}\left(x^{(n)} \leq x\right)=\frac{1}{N} \sum_{n=1}^{N} u_{x^{(n)}}(x)
$$

where $u_{y}(x)$ is a step function at $y$ defined by

$$
u_{y}(x)= \begin{cases}1 & \text { if } x \geq y \\ 0 & \text { if } x<y\end{cases}
$$

This can be visualized as a "stair case", as in Figure 2.18(b), where the jumps of height $1 / N$ occur at every sample.

\title{
2.8 Transformations of random variables *
}

Suppose $\boldsymbol{x} \sim p()$ is some random variable, and $\boldsymbol{y}=f(\boldsymbol{x})$ is some deterministic transformation of it. In this section, we discuss how to compute $p(\boldsymbol{y})$.

\subsection*{2.8.1 Discrete case}

If $X$ is a discrete rv, we can derive the pmf for $Y$ by simply summing up the probability mass for all the $x$ 's such that $f(x)=y$ :

$$
p_{y}(y)=\sum_{x: f(x)=y} p_{x}(x)
$$

For example, if $f(X)=1$ if $X$ is even and $f(X)=0$ otherwise, and $p_{x}(X)$ is uniform on the set $\{1, \ldots, 10\}$, then $p_{y}(1)=\sum_{x \in\{2,4,6,8,10\}} p_{x}(x)=0.5$, and hence $p_{y}(0)=0.5$ also. Note that in this example, $f$ is a many-to-one function.

\subsection*{2.8.2 Continuous case}

If $X$ is continuous, we cannot use Equation (2.150) since $p_{x}(x)$ is a density, not a pmf, and we cannot sum up densities. Instead, we work with cdf's, as follows:

$$
P_{y}(y) \triangleq \operatorname{Pr}(Y \leq y)=\operatorname{Pr}(f(X) \leq y)=\operatorname{Pr}(X \in\{x \mid f(x) \leq y\})
$$

If $f$ is invertible, we can derive the pdf of $y$ by differentiating the cdf, as we show below. If $f$ is not invertible, we can use numerical integration, or a Monte Carlo approximation.

\subsection*{2.8.3 Invertible transformations (bijections)}

In this section, we consider the case of monotonic and hence invertible functions. (Note a function is invertible iff it is a bijector). With this assumption, there is a simple formula for the pdf of $y$, as we will see. (This can be generalized to invertible, but non-monotonic, functions, but we ignore this case.)

Draft of "Probabilistic Machine Learning: An Introduction". August 8, 2022
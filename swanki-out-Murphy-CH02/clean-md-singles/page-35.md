![](https://cdn.mathpix.com/cropped/2024_06_13_9144c552ba5b89e1e6c1g-1.jpg?height=390&width=426&top_left_y=198&top_left_x=450)

(a)

![](https://cdn.mathpix.com/cropped/2024_06_13_9144c552ba5b89e1e6c1g-1.jpg?height=266&width=431&top_left_y=321&top_left_x=1157)

(b)

Figure 2.19: (a) Mapping a uniform pdf through the function $f(x)=2 x+1$. (b) Illustration of how two nearby points, $x$ and $x+d x$, get mapped under $f$. If $\frac{d y}{d x}>0$, the function is locally increasing, but if $\frac{d y}{d x}<0$, the function is locally decreasing. From [Jan18]. Used with kind permission of Eric Jang.

\title{
2.8.3.1 Change of variables: scalar case
}

We start with an example. Suppose $x \sim \operatorname{Unif}(0,1)$, and $y=f(x)=2 x+1$. This function stretches and shifts the probability distribution, as shown in Figure 2.19(a). Now let us zoom in on a point $x$ and another point that is infinitesimally close, namely $x+d x$. We see this interval gets mapped to $(y, y+d y)$. The probability mass in these intervals must be the same, hence $p(x) d x=p(y) d y$, and so $p(y)=p(x) d x / d y$. However, since it does not matter (in terms of probability preservation) whether $d x / d y>0$ or $d x / d y<0$, we get

$$
p_{y}(y)=p_{x}(x)\left|\frac{d x}{d y}\right|
$$

Now consider the general case for any $p_{x}(x)$ and any monotonic function $f: \mathbb{R} \rightarrow \mathbb{R}$. Let $g=f^{-1}$, so $y=f(x)$ and $x=g(y)$. If we assume that $f: \mathbb{R} \rightarrow \mathbb{R}$ is monotonically increasing we get

$$
P_{y}(y)=\operatorname{Pr}(f(X) \leq y)=\operatorname{Pr}\left(X \leq f^{-1}(y)\right)=P_{x}\left(f^{-1}(y)\right)=P_{x}(g(y))
$$

Taking derivatives we get

$$
p_{y}(y) \triangleq \frac{d}{d y} P_{y}(y)=\frac{d}{d y} P_{x}(x)=\frac{d x}{d y} \frac{d}{d x} P_{x}(x)=\frac{d x}{d y} p_{x}(x)
$$

We can derive a similar expression (but with opposite signs) for the case where $f$ is monotonically decreasing. To handle the general case we take the absolute value to get

$$
p_{y}(y)=p_{x}(g(y))\left|\frac{d}{d y} g(y)\right|
$$

This is called change of variables formula.

\subsection*{2.8.3.2 Change of variables: multivariate case}

We can extend the previous results to multivariate distributions as follows. Let $\boldsymbol{f}$ be an invertible function that maps $\mathbb{R}^{n}$ to $\mathbb{R}^{n}$, with inverse $\boldsymbol{g}$. Suppose we want to compute the pdf of $\boldsymbol{y}=\boldsymbol{f}(\boldsymbol{x})$. By

Author: Kevin P. Murphy. (C) MIT Press. CC-BY-NC-ND license
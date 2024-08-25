![](https://cdn.mathpix.com/cropped/2024_06_13_647790ec99d4643bfdd1g-1.jpg?height=380&width=510&top_left_y=198&top_left_x=755)

Figure 2.3: Computing $p(x, y)=p(x) p(y)$, where $X \perp Y$. Here $X$ and $Y$ are discrete random variables; $X$ has 6 possible states (values) and $Y$ has 5 possible states. A general joint distribution on two such variables would require $(6 \times 5)-1=29$ parameters to define it (we subtract 1 because of the sum-to-one constraint). By assuming (unconditional) independence, we only need $(6-1)+(5-1)=9$ parameters to define $p(x, y)$.

This is called the product rule.

By extending the product rule to $D$ variables, we get the chain rule of probability:

$$
p\left(\boldsymbol{x}_{1: D}\right)=p\left(x_{1}\right) p\left(x_{2} \mid x_{1}\right) p\left(x_{3} \mid x_{1}, x_{2}\right) p\left(x_{4} \mid x_{1}, x_{2}, x_{3}\right) \ldots p\left(x_{D} \mid \boldsymbol{x}_{1: D-1}\right)
$$

This provides a way to create a high dimensional joint distribution from a set of conditional distributions. We discuss this in more detail in Section 3.6.

\title{
2.2.4 Independence and conditional independence
}

We say $X$ and $Y$ are unconditionally independent or marginally independent, denoted $X \perp Y$, if we can represent the joint as the product of the two marginals (see Figure 2.3), i.e.,

$$
X \perp Y \Longleftrightarrow p(X, Y)=p(X) p(Y)
$$

In general, we say a set of variables $X_{1}, \ldots, X_{n}$ is (mutually) independent if the joint can be written as a product of marginals for all subsets $\left\{X_{1}, \ldots, X_{m}\right\} \subseteq\left\{X_{1}, \ldots, X_{n}\right\}$ : i.e.,

$$
p\left(X_{1}, \ldots, X_{m}\right)=\prod_{i=1}^{m} p\left(X_{i}\right)
$$

For example, we say $X_{1}, X_{2}, X_{3}$ are mutually independent if the following conditions hold: $p\left(X_{1}, X_{2}, X_{3}\right)=$ $p\left(X_{1}\right) p\left(X_{2}\right) p\left(X_{3}\right), p\left(X_{1}, X_{2}\right)=p\left(X_{1}\right) p\left(X_{2}\right), p\left(X_{2}, X_{3}\right)=p\left(X_{2}\right) p\left(X_{3}\right)$, and $p\left(X_{1}, X_{3}\right)=p\left(X_{1}\right) p\left(X_{3}\right) .{ }^{2}$

Unfortunately, unconditional independence is rare, because most variables can influence most other variables. However, usually this influence is mediated via other variables rather than being direct. We therefore say $X$ and $Y$ are conditionally independent (CI) given $Z$ iff the conditional joint can be written as a product of conditional marginals:

$$
X \perp Y \mid Z \Longleftrightarrow p(X, Y \mid Z)=p(X \mid Z) p(Y \mid Z)
$$

2. For further discussion, see https://github.com/probml/pml-book/issues/353\#issuecomment-1120327442.

Author: Kevin P. Murphy. (C) MIT Press. CC-BY-NC-ND license
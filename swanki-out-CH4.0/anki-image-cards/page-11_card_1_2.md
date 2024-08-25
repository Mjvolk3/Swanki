## What is represented by the regression function $f^{\star}(x)$ in the given graph?

![](https://cdn.mathpix.com/cropped/2024_05_26_194577429b12ff8ccc6dg-1.jpg?height=539&width=708&top_left_y=219&top_left_x=938)

%

The regression function $f^{\star}(x)$ represents the mean of the conditional distribution $p(t \mid x)$. It minimizes the expected squared loss in regression problems.

- #machine-learning, #regression

---

## How is the expected loss $\mathbb{E}[L]$ calculated for the squared loss function $L(t, f(\mathbf{x}))=\{f(\mathbf{x})-t\}^{2}$?

![](https://cdn.mathpix.com/cropped/2024_05_26_194577429b12ff8ccc6dg-1.jpg?height=539&width=708&top_left_y=219&top_left_x=938)

%

The expected loss $\mathbb{E}[L]$ is calculated as:

$$
\mathbb{E}[L]=\iint\{f(\mathbf{x})-t\}^{2} p(\mathbf{x}, t) \mathrm{d} \mathbf{x} \mathrm{d} t
$$

where we integrate over the joint distribution $p(\mathbf{x}, t)$ of the input $\mathbf{x}$ and the target variable $t$.

- #machine-learning, #regression, #expected-value
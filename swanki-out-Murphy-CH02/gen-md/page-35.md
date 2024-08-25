## What happens when mapping a uniform pdf through the function $f(x) = 2x + 1$?

When mapping a uniform pdf through the function $f(x) = 2x + 1$, the probability density function $p_y(y)$ is transformed using the change of variables formula.

Given:
$$
x \sim \operatorname{Unif}(0,1) \quad \text{and} \quad y = f(x) = 2x + 1,
$$
we use the change of variables formula:
$$
p_{y}(y) = p_{x}(x) \left| \frac{dx}{dy} \right|.
$$

Here, $\frac{dx}{dy} = \frac{1}{\frac{dy}{dx}} = \frac{1}{2}$, so the resulting pdf is:
$$
p_{y}(y) = \frac{1}{2}.
$$

- #probability, #distribution-transformations
  
## How do two nearby points $(x, x+dx)$ get mapped under the function $f$ if $\frac{dy}{dx}>0$ versus $\frac{dy}{dx}<0$?

When two nearby points $(x, x+dx)$ get mapped under the function $f(x)=2x+1$:
- If $\frac{dy}{dx} > 0$, the function is locally increasing.
- If $\frac{dy}{dx} < 0$, the function is locally decreasing.

The scaled probability density is the same in both cases since we consider the absolute value.

Given:
$$
p(x) \, dx = p(y) \, dy,
$$
we deduce:
$$
p_{y}(y) = p_{x}(x) \left| \frac{dx}{dy} \right|.
$$

- #calculus, #mapping-transformations, #probability-density

## Derive the probability distribution transformation from $p_x(x)$ to $p_y(y)$ for a monotonic function $f: \mathbb{R} \to \mathbb{R}$.

For a monotonic function $f: \mathbb{R} \rightarrow \mathbb{R}$, the probability distribution transformation from $p_x(x)$ to $p_y(y)$ is:
Given $x = g(y) = f^{-1}(y)$, the cumulative distribution functions satisfy:
$$
P_{y}(y) = \operatorname{Pr}(f(X) \leq y) = \operatorname{Pr}\left(X \leq f^{-1}(y)\right) = P_{x}(g(y)).
$$

Taking derivatives:
$$
p_{y}(y) = \frac{d}{dy} P_{y}(y) = \frac{d}{dy} P_{x}(g(y)) = \frac{dx}{dy} p_{x}(x).
$$

Finally, using the absolute value for general cases:
$$
p_{y}(y) = p_{x}(g(y)) \left| \frac{d}{dy} g(y) \right|.
$$

- #probability, #calculus, #transformations

## For the multivariate case, what is the change of variables formula for pdfs?

In the multivariate case, suppose $\mathbf{y} = \mathbf{f}(\mathbf{x})$ and $\mathbf{f}$ is an invertible function mapping $\mathbb{R}^n$ to $\mathbb{R}^n$, with inverse $\mathbf{g}$. The pdf transformation is:
$$
p_{\mathbf{y}}(\mathbf{y}) = p_{\mathbf{x}}(\mathbf{g}(\mathbf{y})) \left| \det \left( \frac{\partial \mathbf{g}}{\partial \mathbf{y}} \right) \right|,
$$

where $\frac{\partial \mathbf{g}}{\partial \mathbf{y}}$ denotes the Jacobian matrix of $\mathbf{g}$.

- #multivariate-probability, #jacobian, #change-of-variables

## What happens when the function $f$ is monotonically decreasing in the context of transforming probability distributions?

If the function $f$ is monotonically decreasing, the cumulative distribution relationship changes sign. For a decreasing function $f(x)$:
$$
P_{y}(y) = \operatorname{Pr}(f(X) \leq y) = \operatorname{Pr}(X \geq f^{-1}(y)) = 1 - P_{x}(f^{-1}(y)).
$$

Taking derivatives with respect to $y$:
$$
p_{y}(y) = -\frac{d x}{d y} p_{x}(x).
$$

In this case, we still use the absolute value in the final formula:
$$
p_{y}(y) = p_{x}(g(y)) \left| \frac{d}{dy} g(y) \right|.
$$

- ##calculus, #probability-distributions, #monotonic-functions

## Translate the example where $x \sim \operatorname{Unif}(0,1)$ and $y=f(x)=2x+1$ to the derived general change of variables formula.

Given that $x \sim \operatorname{Unif}(0,1)$ and $y = f(x) = 2x + 1$, deriving the general change of variables formula involves the following steps:
1. Calculate:
$$
\frac{dx}{dy} = \frac{1}{2}.
$$

2. Apply the change of variables formula:
$$
p_{y}(y) = p_{x}(g(y)) \left| \frac{d}{dy} g(y) \right|,
$$

where $g(y) = f^{-1}(y) = \frac{y-1}{2}$.

Hence:
$$
p_y(y) = \frac{1}{2} \quad \text{for} \quad y \in [1,3].
$$

- ##probability, #distribution-transformations
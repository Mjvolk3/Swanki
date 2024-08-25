## Using the gradient descent formula (7.16) and orthonormality relation (7.9), what expression do we obtain for the change in $\alpha_i$ at each step of the gradient descent algorithm?

Using the gradient descent formula and orthonormality relation, the expression for the change in $\alpha_i$ at each step is:

$$
\Delta \alpha_{i}=-\eta \lambda_{i} \alpha_{i}
$$

where:
- $\Delta \alpha_{i}$ is the change in coefficient $\alpha_{i}$.
- $\eta$ is the learning rate.
- $\lambda_{i}$ is the eigenvalue associated with the direction $u_{i}$.
- $\alpha_{i}$ is the coefficient at the current step, representing the distance to the minimum along the direction $u_{i}$.

- #gradient-descent, #eigenvalues, #optimization

## If we start with an initial $\alpha_i^{(0)}$, how will $\alpha_i$ evolve after $T$ steps in gradient descent?

After $T$ steps, $\alpha_i$ will evolve according to the formula:

$$
\alpha_{i}^{(T)}=\left(1-\eta \lambda_{i}\right)^{T} \alpha_{i}^{(0)}
$$

This shows that $\alpha_i$ decreases exponentially over iterations with a factor $(1 - \eta \lambda_i)$. 

- #gradient-descent, #eigenvalues, #convergence-rate

## Combining equations (7.24) and (7.25) with the gradient descent formula (7.16), derive the expression for the update in $\alpha_i$.

The combined equations give us:

$$
\Delta \alpha_{i}=-\eta \lambda_{i} \alpha_{i}
$$

From this, it follows that the new value $\alpha_i^{\text{new}}$ is:

$$
\alpha_{i}^{\text {new }}=\left(1-\eta \lambda_{i}\right) \alpha_{i}^{\text {old }}
$$

- #gradient-descent, #optimization, #eigenvalues

## What condition must hold to ensure that the limit $T \rightarrow \infty$ leads to $\alpha_i = 0$?

The condition that must hold is:

$$
\left|1-\eta \lambda_{i}\right|<1
$$

This ensures that $\alpha_i$ will converge to 0 as $T$ approaches infinity.

- #gradient-descent, #convergence, #optimization

## Explain how $\eta$ affects the speed of convergence in gradient descent and the limit on its value.

The factor $(1 - \eta \lambda_i)$ determines the speed of convergence. Increasing $\eta$ makes this factor smaller, thus improving convergence. However, the value of $\eta$ must be less than $2 / \lambda_{\max}$ to ensure $\left|1-\eta \lambda_{i}\right|<1$ and prevent divergence.

- #convergence-rate, #learning-rate, #optimization

## Why does the smallest eigenvalue dominate the rate of convergence when $\eta$ is set to its largest permissible value?

When $\eta$ is set to its largest allowable value, the convergence rate is governed by:

$$
\left(1-\frac{2 \lambda_{\min }}{\lambda_{\max }}\right)
$$

Because this factor is determined by the smallest eigenvalue $\lambda_{\min}$, it slows down the convergence along the direction associated with $\lambda_{\min}$.

- #eigenvalues, #convergence-rate, #gradient-descent
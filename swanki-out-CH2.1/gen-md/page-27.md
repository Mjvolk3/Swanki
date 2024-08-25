## Define the entropy $\mathrm{H}$ for a discrete distribution of probabilities.

The entropy, $\mathrm{H}$, for a discrete distribution where the probabilities of distinct states $x_i$ are given by $p(x_i)$ is defined as:
$$
\mathrm{H} = -\sum_i p(x_i) \ln(p(x_i))
$$
This formula quantifies the amount of uncertainty or randomness in the distribution.

- #information-theory.entropy, #probability.discrete-distributions

## Explain why a uniform distribution maximizes entropy using the concept of entropy $\mathrm{H}$.

A uniform distribution maximizes entropy because in such a distribution, every outcome $x_i$ has equal probability, $p(x_i) = \frac{1}{M}$ for $M$ total outcomes. The entropy for a uniform distribution is then given by:
$$
\mathrm{H} = -\sum_{i=1}^M \frac{1}{M} \ln\left(\frac{1}{M}\right) = \ln(M)
$$
Since entropy measures uncertainty and a uniform distribution provides no preference among outcomes, it maximizes uncertainty.

- #information-theory.entropy-maximization, #probability.uniform-distribution

## Derive the expression for the second derivative of entropy $\mathrm{H}$ with respect to $p(x_i)$ and discuss its implications.

To verify that the entropy function attains a maximum, we consider its second derivative:
$$
\frac{\partial^2 \mathrm{H}}{\partial p(x_i) \partial p(x_j)} = -I_{ij} \frac{1}{p_i}
$$
where $I_{ij}$ is the Kronecker delta (which is 1 if $i=j$ and 0 otherwise). This shows all diagonal elements are negative (since $p_i>0$), ensuring the entropy function is concave, indicating a maximum at the stationary point.

- #calculus.derivatives, #information-theory.entropy-analysis

## Explain how the concept of differential entropy extends to continuous distributions.

Differential entropy extends the concept of entropy to continuous distributions by considering a variable $x$ divided into bins of width $\Delta$. Assuming $p(x)$ is continuous and using the mean value theorem:
$$
\int_{i \Delta}^{(i+1) \Delta} p(x) \mathrm{d} x = p(x_i) \Delta
$$
represents the probability of $x$ falling within the $i$-th bin, approximated by $p(x_i)$ times the bin width. This allows for approximating entropy in continuous domains.

- #information-theory.differential-entropy, #calculus.integration

## Utilize the identity matrix in the context of the second derivative of entropy.

In the expression for the second derivative of entropy for a discrete distribution, the identity matrix $I_{ij}$ plays a crucial role by ensuring that the mixture of partial derivatives only contributes along the diagonal where $i=j$:
$$
\frac{\partial^2 \mathrm{H}}{\partial p(x_i) \partial p(x_j)} = -I_{ij} \frac{1}{p_i}
$$
This implies that off-diagonal elements (where $i \neq j$) do not contribute to the curvature of the entropy function, focusing all impact on individual probabilities $p_i$.

- #linear-algebra.identity-matrix, #calculus.second-derivative
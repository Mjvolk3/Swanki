## Derive the expression for the estimated density at a point $\mathbf{x}$ using the kernel density estimator method described in the paper.

To estimate the density at a point $\mathbf{x}$ using the kernel density estimator, we employ a kernel function $k(\mathbf{u})$ and a scaling factor $h$. The kernel function used is defined as:

$$
k(\mathbf{u})=\left\{\begin{array}{ll}
1, & \left|u_{i}\right| \leqslant 1 / 2, \\
0, & \text{otherwise }
\end{array}\right., \quad i=1, \ldots, D
$$

The kernel density estimator for a point $\mathbf{x}$ is derived by substituting the count of points within a hypercube centered at $\mathbf{x}$ into the density estimate formula:

$$
K=\sum_{n=1}^{N} k\left(\frac{\mathbf{x}-\mathbf{x}_{n}}{h}\right)
$$

Substituting $K$ and the volume of the hypercube $V=h^D$ into the density formula given by:

$$
p(\mathbf{x})=\frac{K}{N V}
$$

yields

$$
p(\mathbf{x})=\frac{1}{N} \sum_{n=1}^{N} \frac{1}{h^{D}} k\left(\frac{\mathbf{x}-\mathbf{x}_{n}}{h}\right)
$$

This equation estimates the density at $\mathbf{x}$ considering the number of points falling within a hypercube of side $h$ centered at $\mathbf{x}$, scaling by the volume of the hypercube and the total number of data points $N$.

- #statistics.density-estimation, #machine-learning.kernel-method, #mathematics.equation-derivation

## Explain the conditions under which the kernel density estimator converges to the true probability density.

The kernel density estimator converges to the true probability density as the number of data points $N$ approaches infinity, under specific conditions on the parameters $V$ (volume of the region $\mathcal{R}$) and $K$ (number of points in $\mathcal{R}$). According to Duda and Hart (1973), these conditions are:

1. The volume $V$ should shrink with increasing $N$.
2. The number $K$ should grow with $N$.
3. The rates of shrinkage of $V$ and growth of $K$ should be appropriate to ensure that the binomial distribution is sharply peaked.

These conditions ensure both sufficient granularity in the local region around each point (due to shrinking $V$) and statistical reliability (due to increasing $K$). Consequently, as $N \rightarrow \infty$, the estimator becomes increasingly accurate, theoretically converging to the true density.

- #statistics.asymptotic-behavior, #machine-learning.theory, #mathematics.probability-limits

## Define the function $k(\mathbf{u})$ used in the kernel method and its role in density estimation.

In the kernel method of density estimation, the function $k(\mathbf{u})$ acts as the kernel, specifically a Parzen window. The function is defined as:
$$
k(\mathbf{u})=\left\{\begin{array}{ll}
1, & \left|u_{i}\right| \leqslant 1 / 2, \\
0, & \text{otherwise }
\end{array}, \quad i=1, \ldots, D\right.
$$

This function identifies whether a given point $\mathbf{x}_n$ (after adjustment by $\mathbf{x}$ and scaling by $h$) falls inside a unit hypercube centered on the origin. Its role in density estimation is critical as it determines the inclusion of a data point into the count $K$ that is used to estimate the density at $\mathbf{x}$. The form of $k(\mathbf{u})$ creates a hypercube of side $h$ around $\mathbf{x}$, and $K$ is computed by summing over the transformed data points.

- #machine-learning.kernel-method, #mathematics.functions, #statistics.density-estimation

## Discuss the contradictory assumptions underlying the initial density estimation formula $p(\mathbf{x}) = \frac{K}{N V}$ and their implications.

The given density estimation formula,
$$
p(\mathbf{x}) = \frac{K}{N V}
$$
relies on two contradictory assumptions:

1. The region $\mathcal{R}$ is small enough that the density within it is nearly constant (suggesting a very localized estimation).
2. $\mathcal{R}$ is large enough relative to the density to ensure a sufficient count $K$ of data points within it for the binomial distribution to be sharply peaked (ensuring statistical reliability).

These assumptions are contradictory because increasing the size of $\mathcal{R}$ to satisfy the second condition may violate the first condition. The balance between these conditions impacts the estimator’s bias and variance, essentially dictating the estimator’s effectiveness and reliability in practical scenarios. Careful tuning of $V$ and $K$ becomes essential to derive a useful density estimate.

- #statistics.biases, #machine-learning.assumptions, #mathematics.statistical-conditions

## Compare and contrast the $K$-nearest-neighbour and kernel approaches to density estimation as discussed in the paper.

The paper outlines two approaches to employ the density estimate $p(\mathbf{x}) = \frac{K}{N V}$: the $K$-nearest-neighbour and kernel methods.

- **$K$-Nearest-Neighbour Approach**: This method fixes the number of nearest data points $K$ and determines the volume $V$ based on how dispersed these $K$ points are around the query point $\mathbf{x}$. It directly relates $V$ to the distance to the $K$-th nearest point, naturally adapting to the data density.

- **Kernel Approach**: It fixes the volume $V$ (e.g., using a hypercube with sides of length $h$) and computes $K$ by counting how many data points fall within this predefined volume. This approach applies a uniform volume across all query points, which might be suboptimal in areas of varying data density.

Both methods converge to the true density as $N \rightarrow \infty$, assuming appropriate changes in $K$ and $V$. However, their performance can differ significantly depending on data distribution, with the $K$-nearest-neighbour potentially adapting better to local data characteristics.

- #machine-learning.density-estimation, #statistics.method-comparison, #mathematics.convergence-properties
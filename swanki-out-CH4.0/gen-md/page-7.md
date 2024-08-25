### Card 1

## What is the least-squares regression function and how is it geometrically interpreted in the context of the given $N$-dimensional space?

The least-squares regression function is obtained by finding the orthogonal projection of the data vector $\mathbf{t}$ onto the subspace spanned by the basis functions $\phi_{j}(\mathbf{x})$. Geometrically, this means that the solution $\mathbf{y}$ lies in the $M$-dimensional subspace that is closest to $\mathbf{t}$. The sum-of-squares error $E(\mathbf{w})$ is minimized by this projection, and this can be expressed as:

$$
E(\mathbf{w}) = \frac{1}{2} ||\mathbf{t} - \boldsymbol{\Phi} \mathbf{w}||^2
$$

where $\boldsymbol{\Phi}$ is the design matrix formed by basis functions evaluated at data points.


- #machine-learning, #linear-regression, #least-squares

### Card 2

## How can numerical difficulties arise in solving the normal equations directly when using least-squares solutions, and how can these difficulties be mitigated?

Numerical difficulties can arise when $\boldsymbol{\Phi}^{\mathrm{T}} \boldsymbol{\Phi}$ is close to singular, especially if two or more basis vectors $\varphi_{j}$ are co-linear, resulting in parameter values with large magnitudes. Such issues can be mitigated using Singular Value Decomposition (SVD) to address near degeneracies. The addition of a regularization term ensures the matrix remains non-singular in the presence of these degeneracies.

$$
\text{Regularized least-squares solution: } (\boldsymbol{\Phi}^{\mathrm{T}} \boldsymbol{\Phi} + \lambda \mathbf{I})\mathbf{w} = \boldsymbol{\Phi}^{\mathrm{T}} \mathbf{t}
$$

- #machine-learning, #linear-regression, #numerical-methods

### Card 3

## What defines the vector $\mathbf{y}$ in the context of least-squares regression from the given paper chunk?

The vector $\mathbf{y}$ in the context of least-squares regression is defined as an $N$-dimensional vector whose $n$th element is given by $y\left(\mathbf{x}_{n}, \mathbf{w}\right)$, where $n=1, \ldots, N$. Because $\mathbf{y}$ is an arbitrary linear combination of the vectors $\varphi_{j}$, it can reside anywhere in the $M$-dimensional subspace spanned by the basis functions $\phi_{j}\left(\mathbf{x}_{n}\right)$.

$$
\mathbf{y} = \boldsymbol{\Phi} \mathbf{w}
$$

- #machine-learning, #linear-regression, #basis-functions

### Card 4

## Explain the orthogonal projection concept in the context of least-squares solution.

In the least-squares solution, the orthogonal projection of the data vector $\mathbf{t}$ onto the subspace spanned by the basis functions $\phi_{j}(\mathbf{x})$ signifies that the solution $\mathbf{y}$ lies within the subspace and is closest to $\mathbf{t}$. This minimizes the sum-of-squares error, which is associated with the squared Euclidean distance between $\mathbf{y}$ and $\mathbf{t}$.

$$
\mathbf{y} = \boldsymbol{\Phi} \mathbf{w}_{\mathrm{ML}}
$$

- #machine-learning, #linear-regression, #projection

### Card 5

## Describe the advantage of sequential learning methods over batch methods in the context of large datasets.

Sequential learning methods, also known as online algorithms, process data points one at a time and update model parameters after each presentation. This is advantageous over batch methods, which require processing the entire training set at once, making sequential methods more computationally efficient for large datasets and suitable for real-time applications where data arrives continuously.

- #machine-learning, #sequential-learning, #online-learning

### Card 6

## What role does the $M$-dimensional subspace $\mathcal{S}$ play in the least-squares solution and how is it derived?

The $M$-dimensional subspace $\mathcal{S}$ is spanned by the $M$ basis vectors $\phi_{j}\left(\mathbf{x}_{n}\right)$, which form the columns of the design matrix $\boldsymbol{\Phi}$. The least-squares solution involves finding $\mathbf{w}$ such that the vector $\mathbf{y} = \boldsymbol{\Phi} \mathbf{w}$ lies in this subspace and minimizes the distance to the data vector $\mathbf{t}$.

$$
\mathcal{S} = \text{span}\{\varphi_{1}, \varphi_{2}, \ldots, \varphi_{M}\}
$$

- #machine-learning, #linear-regression, #subspaces
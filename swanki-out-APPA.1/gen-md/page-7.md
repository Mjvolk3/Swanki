## Given the matrix $\mathbf{A}$, what is the formula to represent it in terms of its eigenvalues $\lambda_i$ and corresponding eigenvectors $\mathbf{u}_i$? How can you represent the inverse of $\mathbf{A}$ in a similar form?

\[
\begin{aligned}
\mathbf{A} & =\sum_{i=1}^{M} \lambda_{i} \mathbf{u}_{i} \mathbf{u}_{i}^{\mathrm{T}} \\
\mathbf{A}^{-1} & =\sum_{i=1}^{M} \frac{1}{\lambda_{i}} \mathbf{u}_{i} \mathbf{u}_{i}^{\mathrm{T}}
\end{aligned}
\]

In these equations, $\mathbf{A}$ is described in terms of summation over its eigenvalues $\lambda_i$ and the outer product of its eigenvectors $\mathbf{u}_i$. The inverse of $\mathbf{A}$ follows a similar structure but inversely weights each term by $\frac{1}{\lambda_i}$. 

- #matrix-theory, #eigenvalues, #eigenvectors


## What is the result when you take the determinant of matrix $\mathbf{A}$, expressed as $\mathbf{A} = \sum_{i=1}^{M} \lambda_{i} \mathbf{u}_{i} \mathbf{u}_{i}^{\mathrm{T}}$?

$$
|\mathbf{A}|=\prod_{i=1}^{M} \lambda_{i}
$$

Taking the determinant of matrix $\mathbf{A}$ reveals that it is the product of its eigenvalues, $\lambda_i$. This stems from the property of determinants in eigen-decomposition.

- #determinants, #matrix-theory


## Explain how to obtain the trace of the matrix $\mathbf{A}$ using its eigenvalues $\lambda_i$.

$$
\operatorname{Tr}(\mathbf{A})=\sum_{i=1}^{M} \lambda_{i}
$$

The trace of matrix $\mathbf{A}$ is the sum of its eigenvalues. This outcome comes from the cyclic property of the trace operator and the fact that $\mathbf{U}^{\mathrm{T}} \mathbf{U}=\mathbf{I}$ where $\mathbf{U}$ is the matrix of eigenvectors.

- #trace-operator, #matrix-theory


## What defines a matrix $\mathbf{A}$ as positive definite, and how is this related to its eigenvalues $\lambda_i$?

A matrix $\mathbf{A}$ is said to be positive definite, denoted by $\mathbf{A} \succ 0$, if $\mathbf{w}^{\mathrm{T}} \mathbf{A w}>0$ for all non-zero values of vector $\mathbf{w}$. This is equivalently ensured if all eigenvalues $\lambda_i$ are greater than zero.

Positive definiteness of a matrix ensures that all its eigenvalues are positive, ensuring $\mathbf{A}\mathbf{w}$ does not invert the direction of $\mathbf{w}$ for any non-zero $\mathbf{w}$. An arbitrary vector $\mathbf{w}$ can be expressed as a linear combination of eigenvectors.

- #positive-definiteness, #eigenvalues

## What does it mean for a matrix to be positive semidefinite and how is it different from being positive definite?

A matrix is said to be positive semidefinite if $\mathbf{w}^{\mathrm{T}} \mathbf{A} \mathbf{w} \geqslant 0$ for all vectors $\mathbf{w}$, denoted $\mathbf{A} \succeq 0$, and this is equivalent to all eigenvalues $\lambda_i$ being nonnegative.

A positive semidefinite matrix allows zero eigenvalues while a positive definite matrix does not. The matrix retains some properties (like not inverting the direction of $\mathbf{w}$), but may map some vectors to zero (if they are eigenvectors corresponding to zero eigenvalues).

- #positive-semi-definiteness, #eigenvalues

## What is the condition number of a matrix and how is it calculated using its eigenvalues?

The condition number $\mathrm{CN}$ of a matrix is given by

$$
\mathrm{CN}=\left(\frac{\lambda_{\max }}{\lambda_{\min }}\right)^{1 / 2}
$$

where $\lambda_{\max }$ is the largest eigenvalue and $\lambda_{\min }$ is the smallest eigenvalue. 

The condition number indicates how sensitive the matrix is to small changes; larger values suggest greater sensitivity or ill-conditioning.

- #condition-number, #matrix-stability
## Differentiate the product of two matrices with respect to a variable \( x \).

Using the product rule of derivatives, express the differentiation of the product of two matrices \( \mathbf{A} \) and \( \mathbf{B} \) with respect to a variable \( x \).

$$
\frac{\partial}{\partial x}(\mathbf{A B}) = \frac{\partial \mathbf{A}}{\partial x} \mathbf{B} + \mathbf{A} \frac{\partial \mathbf{B}}{\partial x}
$$

- #calculus, #linear-algebra.matrix-differentiation


## Differentiate the inverse of a matrix with respect to a variable \( x \).

How do you express the differentiation of the inverse of a matrix \( \mathbf{A} \) with respect to a variable \( x \)?

$$
\frac{\partial}{\partial x}\left(\mathbf{A}^{-1}\right)=-\mathbf{A}^{-1} \frac{\partial \mathbf{A}}{\partial x} \mathbf{A}^{-1} 
$$

- #calculus, #linear-algebra.matrix-differentiation


## Prove $\frac{\partial}{\partial x}\left(\mathbf{A}^{-1}\right)=-\mathbf{A}^{-1} \frac{\partial \mathbf{A}}{\partial x} \mathbf{A}^{-1}$.

Given $\mathbf{A}^{-1} \mathbf{A}=\mathbf{I}$, differentiate this equation and show that the derivative of the inverse of a matrix can be expressed as $\frac{\partial}{\partial x}\left(\mathbf{A}^{-1}\right)=-\mathbf{A}^{-1} \frac{\partial \mathbf{A}}{\partial x} \mathbf{A}^{-1}$.

%
Differentiating $\mathbf{A}^{-1} \mathbf{A}=\mathbf{I}$ with respect to \( x \):

$$
\frac{\partial}{\partial x}(\mathbf{A}^{-1} \mathbf{A}) = \frac{\partial \mathbf{A}^{-1}}{\partial x}\mathbf{A} + \mathbf{A}^{-1} \frac{\partial \mathbf{A}}{\partial x} = 0
$$

We then isolate $\frac{\partial \mathbf{A}^{-1}}{\partial x}$:

$$
\frac{\partial \mathbf{A}^{-1}}{\partial x} \mathbf{A} = - \mathbf{A}^{-1} \frac{\partial \mathbf{A}}{\partial x}
$$

Finally, right-multiplying both sides by $\mathbf{A}^{-1}$, we get:

$$
\frac{\partial \mathbf{A}^{-1}}{\partial x} = - \mathbf{A}^{-1} \frac{\partial \mathbf{A}}{\partial x} \mathbf{A}^{-1}
$$

- #calculus, #linear-algebra.matrix-differentiation


## Trace of a product differentiation with respect to a matrix element.

If we choose $x$ to be one of the elements of $\mathbf{A}$, how can we express the differentiation of the trace of product $\mathbf{A B}$ with respect to $A_{ij}$?

$$
\frac{\partial}{\partial A_{i j}} \operatorname{Tr}(\mathbf{A B}) = B_{j i} 
$$

- #calculus, #linear-algebra.matrix-differentiation


## Properties of the trace differentiation with respect to a matrix.

What are the properties of differentiating the trace of certain matrix expressions with respect to a matrix \( \mathbf{A} \)?

$$
\begin{aligned}
\frac{\partial}{\partial \mathbf{A}} \operatorname{Tr}\left(\mathbf{A}^{\mathrm{T}} \mathbf{B}\right) & =\mathbf{B} \\
\frac{\partial}{\partial \mathbf{A}} \operatorname{Tr}(\mathbf{A}) & =\mathbf{I} \\
\frac{\partial}{\partial \mathbf{A}} \operatorname{Tr}\left(\mathbf{A B} \mathbf{A}^{\mathrm{T}}\right) & =\mathbf{A}\left(\mathbf{B} + \mathbf{B}^{\mathrm{T}}\right)
\end{aligned}
$$

- #calculus, #linear-algebra.traces


## Eigenvector equation for a square matrix.

For a square matrix $\mathbf{A}$ of size $M \times M$, what is the eigenvector equation?

$$
\mathbf{A} \mathbf{u}_{i} = \lambda_{i} \mathbf{u}_{i} 
$$

where \( \mathbf{u}_{i} \) is the eigenvector and \( \lambda_{i} \) is the corresponding eigenvalue.

- #linear-algebra, #eigenvectors.matrix-equation
If there is a total of $W$ weights and biases in the network, then $\mathbf{w}$ and $\mathbf{b}$ have length $W$ and $\mathbf{H}$ has dimensionality $W \times W$. From (7.3), the corresponding local approximation to the gradient is given by

$$
\nabla E(\mathbf{w})=\mathbf{b}+\mathbf{H}(\mathbf{w}-\widehat{\mathbf{w}})
$$

For points $\mathbf{w}$ that are sufficiently close to $\widehat{\mathbf{w}}$, these expressions will give reasonable approximations for the error and its gradient.

Consider the particular case of a local quadratic approximation around a point $\mathbf{w}^{\star}$ that is a minimum of the error function. In this case there is no linear term, because $\nabla E=0$ at $\mathbf{w}^{\star}$, and $(7.3)$ becomes

$$
E(\mathbf{w})=E\left(\mathbf{w}^{\star}\right)+\frac{1}{2}\left(\mathbf{w}-\mathbf{w}^{\star}\right)^{\mathrm{T}} \mathbf{H}\left(\mathbf{w}-\mathbf{w}^{\star}\right)
$$

where the Hessian $\mathbf{H}$ is evaluated at $\mathbf{w}^{\star}$. To interpret this geometrically, consider the eigenvalue equation for the Hessian matrix:

$$
\mathbf{H} \mathbf{u}_{i}=\lambda_{i} \mathbf{u}_{i}
$$

\section*{Appendix A}

\section*{Appendix $A$}

Exercise 7.1 where the eigenvectors $\mathbf{u}_{i}$ form a complete orthonormal set so that

$$
\mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{j}=\delta_{i j}
$$

We now expand $\left(\mathbf{w}-\mathbf{w}^{\star}\right)$ as a linear combination of the eigenvectors in the form

$$
\mathbf{w}-\mathbf{w}^{\star}=\sum_{i} \alpha_{i} \mathbf{u}_{i}
$$

This can be regarded as a transformation of the coordinate system in which the origin is translated to the point $\mathbf{w}^{\star}$ and the axes are rotated to align with the eigenvectors through the orthogonal matrix whose columns are $\left\{\mathbf{u}_{1}, \ldots, \mathbf{u}_{W}\right\}$. By substituting (7.10) into (7.7) and using (7.8) and (7.9), the error function can be written in the form

$$
E(\mathbf{w})=E\left(\mathbf{w}^{\star}\right)+\frac{1}{2} \sum_{i} \lambda_{i} \alpha_{i}^{2}
$$

Suppose we set all $\alpha_{i}=0$ for $i \neq j$ and then vary $\alpha_{j}$, corresponding to moving $\mathbf{w}$ away from $\mathbf{w}^{\star}$ in the direction of $\mathbf{u}_{j}$. We see from (7.11) that the error function will increase if the corresponding eigenvalue $\lambda_{j}$ is positive and will decrease if it is negative. If all eigenvalues are positive then $\mathbf{w}^{\star}$ corresponds to a local minimum of the error function, whereas if they are all negative then $\mathbf{w}^{\star}$ corresponds to a local maximum. If we have a mix of positive and negative eigenvalues then $\mathbf{w}^{\star}$ represents a saddle point.

A matrix $\mathbf{H}$ is said to be positive definite if, and only if,

$$
\mathbf{v}^{\mathrm{T}} \mathbf{H} \mathbf{v}>0, \quad \text { for all } \mathbf{v}
$$
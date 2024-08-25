can be written as

$$
\nabla E=\sum_{i} \alpha_{i} \lambda_{i} \mathbf{u}_{i}
$$

Again using (7.10) we can express the change in the weight vector in terms of corresponding changes in the coefficients $\left\{\alpha_{i}\right\}$ :

$$
\Delta \mathbf{w}=\sum_{i} \Delta \alpha_{i} \mathbf{u}_{i}
$$

Combining (7.24) with (7.25) and the gradient descent formula (7.16) and using the orthonormality relation (7.9) for the eigenvectors of the Hessian, we obtain the following expression for the change in $\alpha_{i}$ at each step of the gradient descent algorithm:

$$
\Delta \alpha_{i}=-\eta \lambda_{i} \alpha_{i}
$$

Exercise 7.10 from which it follows that

$$
\alpha_{i}^{\text {new }}=\left(1-\eta \lambda_{i}\right) \alpha_{i}^{\text {old }}
$$

where 'old' and 'new' denote values before and after a weight update. Using the orthonormality relation (7.9) for the eigenvectors together with (7.10), we have

$$
\mathbf{u}_{i}^{\mathrm{T}}\left(\mathbf{w}-\mathbf{w}^{\star}\right)=\alpha_{i}
$$

and so $\alpha_{i}$ can be interpreted as the distance to the minimum along the direction $\mathbf{u}_{i}$. From (7.27) we see that these distances evolve independently such that, at each step, the distance along the direction of $\mathbf{u}_{i}$ is multiplied by a factor $\left(1-\eta \lambda_{i}\right)$. After a total of $T$ steps we have

$$
\alpha_{i}^{(T)}=\left(1-\eta \lambda_{i}\right)^{T} \alpha_{i}^{(0)}
$$

It follows that, provided $\left|1-\eta \lambda_{i}\right|<1$, the limit $T \rightarrow \infty$ leads to $\alpha_{i}=0$, which from (7.28) shows that $\mathbf{w}=\mathbf{w}^{\star}$ and so the weight vector has reached the minimum of the error.

Note that (7.29) demonstrates that gradient descent leads to linear convergence in the neighbourhood of a minimum. Also, convergence to the stationary point requires that all the $\lambda_{i}$ be positive, which in turn implies that the stationary point is indeed a minimum. By making $\eta$ larger we can make the factor $\left(1-\eta \lambda_{i}\right)$ smaller and hence improve the speed of convergence. There is a limit to how large $\eta$ can be made, however. We can permit $\left(1-\eta \lambda_{i}\right)$ to go negative (which gives oscillating values of $\alpha_{i}$ ), but we must ensure that $\left|1-\eta \lambda_{i}\right|<1$ otherwise the $\alpha_{i}$ values will diverge. This limits the value of $\eta$ to $\eta<2 / \lambda_{\max }$ where $\lambda_{\max }$ is the largest of the eigenvalues. The rate of convergence, however, is dominated by the smallest eigenvalue, so with $\eta$ set to its largest permitted value, the convergence along the direction corresponding to the smallest eigenvalue (the long axis of the ellipse in Figure 7.3) will be governed by

$$
\left(1-\frac{2 \lambda_{\min }}{\lambda_{\max }}\right)
$$
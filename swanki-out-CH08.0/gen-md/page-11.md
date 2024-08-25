# Card 1

## Describe the Hessian matrix in the context of neural networks and its computational implications.

The Hessian matrix is a second-order derivative matrix of the error surface often used in nonlinear optimization algorithms for training neural networks. If a network has $W$ parameters (weights and biases), the Hessian matrix will have the dimensions $W \times W$. The computational effort needed to evaluate the Hessian matrix scales like $\mathcal{O}(W^2)$ for each data point.

- #machine-learning, #optimization.hessian-matrix

---

# Card 2

## Explain why saving the full Hessian matrix in large-scale neural networks is impractical and discuss an approximate method.

Since neural networks may contain millions or even billions of parameters, it is impractical to save the full Hessian matrix due to its $\mathcal{O}(W^2)$ storage requirement and even more demanding $\mathcal{O}(W^3)$ computational effort to evaluate its inverse. One approximation method involves evaluating only the diagonal elements of the Hessian while setting off-diagonal elements to zero. 

- #machine-learning, #optimization.approximation

---

# Card 3

## In the context of neural networks, describe the outer product approximation method for the Hessian matrix.

Consider a regression application using a sum-of-squares error function:
$$
E=\frac{1}{2} \sum_{n=1}^{N}\left(y_{n}-t_{n}\right)^{2}
$$
The Hessian matrix can be expressed as:
$$
\mathbf{H}=\sum_{n=1}^{N} \nabla y_{n}\left(\nabla y_{n}\right)^{\mathrm{T}}+\sum_{n=1}^{N}\left(y_{n}-t_{n}\right) \nabla \nabla y_{n}
$$
If $y_n$ is very close to $t_n$, the second term will be small and can often be neglected.

- #machine-learning, #optimization.outer-product-approx

---

# Card 4

## Derive the Hessian matrix for the given sum-of-squares error function in neural networks.

Given the error function:
$$
E=\frac{1}{2} \sum_{n=1}^{N}\left(y_{n}-t_{n}\right)^{2}
$$
The Hessian matrix $\mathbf{H}$ is:
$$
\mathbf{H}=\nabla \nabla E=\sum_{n=1}^{N} \nabla y_{n}\left(\nabla y_{n}\right)^{\mathrm{T}}+\sum_{n=1}^{N}\left(y_{n}-t_{n}\right) \nabla \nabla y_{n}
$$

- #math, #machine-learning.hessian-matrix

---

# Card 5

## Why is the product of the Hessian matrix with a vector often used, and what is its computational complexity?

In neural networks, sometimes only the product ${ }^{\mathrm{T}} \mathbf{H}$ of the Hessian with a vector $\mathbf{v}$ is needed rather than the entire matrix. This product can be calculated efficiently in $\mathcal{O}(W)$ steps using an extended backpropagation method (Møller, 1993; Pearlmutter, 1994).

- #machine-learning, #optimization.vector-product

---

# Card 6

## Discuss a situation in neural networks where neglecting certain terms in the Hessian can be justified.

Consider a sum-of-squares error function:
$$
E=\frac{1}{2} \sum_{n=1}^{N}\left(y_{n}-t_{n}\right)^{2}
$$
If the network's outputs $y_n$ are very close to the target values $t_n$, the term $\sum_{n=1}^{N}\left(y_{n}-t_{n}\right) \nabla \nabla y_{n}$ in the Hessian matrix can be neglected. This simplification is based on the fact that this term will be small for well-trained networks.

- #machine-learning, #optimization.hessian-approx
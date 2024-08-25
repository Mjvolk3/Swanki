Below are six flashcards created from the given text using the specified format:

---

## Derivatives with respect to weights.

What are the derivatives of the error function $E_n$ with respect to the first-layer and second-layer weights?

$$
\frac{\partial E_{n}}{\partial w_{j i}^{(1)}}=\delta_{j} x_{i}, \quad \frac{\partial E_{n}}{\partial w_{k j}^{(2)}}=\delta_{k} z_{j}
$$

The derivatives with respect to the first-layer weights ($w_{ji}^{(1)}$) and second-layer weights ($w_{kj}^{(2)}$) are given by:

$$
\frac{\partial E_{n}}{\partial w_{j i}^{(1)}} = \delta_{j} x_{i}
$$

where $\delta_j$ is the error term for neuron $j$ in the first layer, and $x_i$ is the input to that neuron.

For the second-layer weights:

$$
\frac{\partial E_{n}}{\partial w_{k j}^{(2)}} = \delta_{k} z_{j}
$$

where $\delta_k$ is the error term for neuron $k$ in the second layer, and $z_j$ is the activation output from neuron $j$ in the first layer.

- #neural-networks, #error-function.derivatives

---

## Computational complexity of error function evaluation.

What is the computational complexity of evaluating the error function in a neural network with $W$ weights?

The computational complexity of evaluating the error function $E_n$ for a given input data point in a neural network is $\mathcal{O}(W)$ for sufficiently large $W$.

The complexity is due to:

1. Each term in the sum requires one multiplication and one addition.
2. The evaluation of activation functions contributes a small overhead.

Thus, the overall computational cost is dominated by the number of weights, which is $\mathcal{O}(W)$.

- #neural-networks, #computational-complexity.error-function
  
---

## Finite differences for derivatives.

Explain how finite differences can be used to approximate the derivatives of the error function $E_n$. What is the general expression?

Finite differences can be used to approximate the derivatives of the error function $E_n$ by perturbing each weight $w_{ji}$ in turn. The general expression is:

$$
\frac{\partial E_{n}}{\partial w_{j i}}=\frac{E_{n}\left(w_{j i}+\epsilon\right)-E_{n}\left(w_{j i}\right)}{\epsilon}+\mathcal{O}(\epsilon)
$$

where $\epsilon$ is a small perturbation.

- #numerical-differentiation, #error-function.finite-differences

---

## Accuracy improvement in finite differences.

How can the accuracy of finite differences be improved? What is the improved expression?

The accuracy of finite differences can be improved by using symmetrical central differences, which are given by:

$$
\frac{\partial E_{n}}{\partial w_{j i}}=\frac{E_{n}\left(w_{j i}+\epsilon\right)-E_{n}\left(w_{j i}-\epsilon\right)}{2 \epsilon}+\mathcal{O}\left(\epsilon^{2}\right)
$$

The $\mathcal{O}(\epsilon)$ corrections cancel out using this method.

- #numerical-differentiation, #error-function.central-differences

---

## Numerical differentiation computational cost.

What is the computational cost of numerical differentiation compared to backpropagation in terms of $W$?

The computational cost of numerical differentiation is $\mathcal{O}(W^2)$, compared to $\mathcal{O}(W)$ for backpropagation.

In numerical differentiation:

- Each forward propagation requires $\mathcal{O}(W)$ steps.
- There are $W$ weights, each of which must be perturbed individually.

Thus, the overall cost is $\mathcal{O}(W^2)$.

- #numerical-differentiation, #computational-complexity

---

## Central differences in error computation.

Why are central differences more accurate than finite differences for computing numerical derivatives?

Central differences are more accurate than finite differences because the $\mathcal{O}(\epsilon)$ corrections cancel out. 

Using symmetrical central differences:

$$
\frac{\partial E_{n}}{\partial w_{j i}}=\frac{E_{n}\left(w_{j i}+\epsilon\right)-E_{n}\left(w_{j i}-\epsilon\right)}{2 \epsilon}+\mathcal{O}\left(\epsilon^{2}\right)
$$

In this method, the residual corrections are $\mathcal{O}\left(\epsilon^{2}\right)$, making it a higher-order and more accurate approximation compared to the standard finite differences approach.

- #numerical-differentiation, #error-function.central-differences

---

These cards encapsulate essential concepts and details from the given text chunk, emphasizing scientific nuances and mathematical equations as requested.
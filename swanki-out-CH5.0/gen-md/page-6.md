Here are six Anki-style cards focusing on the scientific and mathematical concepts found in Section 4.1.3.

---

## What is the target vector for a data point from class 2 if \( K=5 \) classes using a 1-of-K binary coding scheme?

The target vector is:

$$
\mathbf{t}=(0,1,0,0,0)^{\mathrm{T}}
$$

The element $t_{j}$, corresponding to the class label, takes the value 1, while all other elements are 0.

- #classification, #coding-scheme.one-of-k

---

## Explain the least squares approach for classification and its key limitation.

Least squares for classification aims to approximate the conditional expectation $\mathbb{E}[\mathbf{t} \mid \mathbf{x}]$. Specifically, for a general classification problem with $K$ classes and a 1-of-K binary coding scheme, the least squares method attempts to minimize a sum-of-squares error function.

**Key Limitation:** The approximations of the posterior class probabilities can have values outside the range $(0,1)$, leading to poor probabilistic interpretations.

- #classification, #least-squares.limitation

---

## Write the equation for the linear model associated with class $\mathcal{C}_{k}$.

The linear model for class $\mathcal{C}_{k}$ is:

$$
y_{k}(\mathbf{x})=\mathbf{w}_{k}^{\mathrm{T}} \mathbf{x} + w_{k 0}
$$

where $k=1, \ldots, K$.

- #classification, #linear-model.class

---

## What is the sum-of-squares error function for the classification problem?

The sum-of-squares error function is given by:

$$
E_{D}(\widetilde{\mathbf{W}}) = \frac{1}{2} \operatorname{Tr}\left\{ (\widetilde{\mathbf{X}} \widetilde{\mathbf{W}} - \mathbf{T})^{\mathrm{T}} (\widetilde{\mathbf{X}} \widetilde{\mathbf{W}} - \mathbf{T}) \right\}
$$

where $\widetilde{\mathbf{W}}$ is the parameter matrix, $\widetilde{\mathbf{X}}$ is the matrix of augmented input vectors, and $\mathbf{T}$ is the matrix of target vectors.

- #classification, #error-function.sum-of-squares

---

## Derive the closed-form solution for the parameter matrix $\widetilde{\mathbf{W}}$ in least squares classification.

Setting the derivative of the error function with respect to $\widetilde{\mathbf{W}}$ to zero and rearranging, we get:

$$
\widetilde{\mathbf{W}} = \left( \widetilde{\mathbf{X}}^{\mathrm{T}} \widetilde{\mathbf{X}} \right)^{-1} \widetilde{\mathbf{X}}^{\mathrm{T}} \mathbf{T}
$$

Alternatively,

$$
\widetilde{\mathbf{W}} = \widetilde{\mathbf{X}}^{\dagger} \mathbf{T}
$$

where $\widetilde{\mathbf{X}}^{\dagger}$ is the pseudo-inverse of $\widetilde{\mathbf{X}}$.

- #classification, #parameter-solution.closed-form

---

## Explain the notation and components in the equation \(\mathbf{y}(\mathbf{x}) = \widetilde{\mathbf{W}}^{\mathrm{T}} \widetilde{\mathbf{x}}\).

- $\mathbf{y}(\mathbf{x})$: Vector of outputs for each class $\mathcal{C}_k$.
- $\widetilde{\mathbf{W}}$: Matrix whose $k$-th column is the augmented weight vector $\widetilde{\mathbf{w}_k}$.
- $\widetilde{\mathbf{x}}$: Augmented input vector $\left(1, \mathbf{x}^{\mathrm{T}}\right)^{\mathrm{T}}$ with a dummy input $x_0 = 1$.

This equation groups individual linear models into a vector form, facilitating easier computation and evaluation.

- #classification, #vector-notation.augmented
### Card 1

## Why is using gradient information advantageous in training neural networks?

Using gradient information is advantageous because it significantly reduces the computational effort required to find the minimum of the error function. Each evaluation of the gradient $\nabla E$ brings $W$ pieces of information, where $W$ is the number of learnable parameters. Therefore, we might hope to find the minimum in $\mathcal{O}(W)$ gradient evaluations. Each evaluation takes $\mathcal{O}(W)$ steps, so the minimum can be found in $\mathcal{O}(W^2)$ steps, which is more efficient compared to $\mathcal{O}(W^3)$ steps required without using gradient information.

- #machine-learning, #neural-networks.training, #gradients.complexity

---

### Card 2

## What is the relation between the quadratic approximation error surface and the number of parameters $W$ in a neural network?

The error surface in the quadratic approximation to the error function is specified by the quantities $\mathbf{b}$ and $\mathbf{H}$, which contain a total of $\frac{W(W+3)}{2}$ independent elements because the matrix $\mathbf{H}$ is symmetric. The minimum location depends on $\mathcal{O}(W^2)$ parameters. Without gradient information, $\mathcal{O}(W^2)$ function evaluations, each requiring $\mathcal{O}(W)$ steps, are needed. Hence, the computational effort is $\mathcal{O}(W^3)$.

- #machine-learning, #neural-networks.parameters, #error-surface.quadratic-approximation

---

### Card 3

## Explain the iterative update step in batch gradient descent for a neural network.

In batch gradient descent, the weight update at iteration $\tau$ is given by
$$\mathbf{w}^{(\tau)} = \mathbf{w}^{(\tau-1)} - \eta \nabla E \left(\mathbf{w}^{(\tau-1)}\right)$$
where $\eta$ is the learning rate. After each update, the gradient is re-evaluated for the new weight vector $\mathbf{w}^{(\tau+1)}$, and the process is repeated. The weight vector is moved in the direction of the greatest rate of decrease of the error function.

- #machine-learning, #neural-networks.training, #gradient-descent.batch

---

### Card 4

## How does the computational effort of finding the minimum error differ between using gradient information and not using it?

Without gradient information, the computational effort to find the minimum error of the function is $\mathcal{O}(W^3)$. Using gradient information, the computational effort is reduced to $\mathcal{O}(W^2)$. This is primarily because each gradient evaluation brings $W$ pieces of information and takes $\mathcal{O}(W)$ steps, leading to more efficient minimization.

- #machine-learning, #neural-networks.computational-effort, #gradients.efficiency

---

### Card 5

## Define the term "learning rate" in the context of gradient descent.

The learning rate, denoted as $\eta$, is a parameter in gradient descent methods that determines the size of the step taken in the direction of the negative gradient of the error function. It affects the magnitude of updates to the weight vector $\mathbf{w}$ in each iteration according to the equation
$$\mathbf{w}^{(\tau)} = \mathbf{w}^{(\tau-1)} - \eta \nabla E \left(\mathbf{w}^{(\tau-1)}\right)$$

- #machine-learning, #neural-networks.training, #learning-rate

---

### Card 6

## What is the main drawback of batch gradient descent?

Batch gradient descent can become extremely inefficient when dealing with very large data sets because each error function or gradient evaluation requires processing the entire training set. This drawback is significant in the context of deep learning, where large datasets are common.

- #machine-learning, #neural-networks.training, #gradient-descent.batch-inefficiency
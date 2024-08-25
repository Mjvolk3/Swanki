Here are 6 Anki cards based on the provided chunk from the paper on Adam optimization:

---

## What is the main purpose of Adam optimization algorithm in training machine learning models?

The purpose of Adam optimization is to update the weights of a neural network during training by minimizing the error function for mini-batches of data points.

- #machine-learning, #optimization.adam, #training

---

## What are the key parameters used in Adam optimization?

The key parameters used in Adam optimization include:

- Training set of data points indexed by $n \in \{1, \ldots, N\}$
- Batch size $B$
- Error function per mini-batch $E_{n: n+B-1}(\mathbf{w})$
- Learning rate $\eta$
- Decay parameters $\beta_1$ and $\beta_2$
- Stabilization parameter $\delta$

- #machine-learning, #optimization.adam, #parameters

---

## What is the bias correction formula used for the first moment estimate in Adam optimization?

The bias correction formula for the first moment estimate is:

$$
\widehat{\mathbf{s}} = \frac{\mathbf{s}}{1 - \beta_{1}^{\tau}}
$$

Where $\widehat{\mathbf{s}}$ is the bias-corrected estimate, $\beta_1$ is the decay parameter for the first moment, and $\tau$ is the time step.

- #machine-learning, #optimization.adam, #formulas

---

## Explain the role of $\mathbf{r}$ in Adam Optimization algorithm.

In Adam optimization, $\mathbf{r}$ stores an exponentially decaying average of past squared gradients:

$$
\mathbf{r} \leftarrow \beta_{2} \mathbf{r} + \left(1 - \beta_{2}\right) \mathbf{g} \odot \mathbf{g}
$$

Here, $\mathbf{g}$ is the gradient, $\odot$ denotes element-wise multiplication, and $\beta_{2}$ is the decay parameter.

- #machine-learning, #optimization.adam, #gradients

---

## How is the weight vector $\mathbf{w}$ updated in the Adam optimization algorithm?

The weight vector $\mathbf{w}$ is updated as follows:

$$
\Delta \mathbf{w} \leftarrow -\eta \frac{\widehat{\mathbf{s}}}{\sqrt{\widehat{\mathbf{r}}} + \delta}
$$

$$
\mathbf{w} \leftarrow \mathbf{w} + \Delta \mathbf{w}
$$

Where $\eta$ is the learning rate, $\widehat{\mathbf{s}}$ and $\widehat{\mathbf{r}}$ are the bias-corrected first and second moment estimates, respectively, $\delta$ is the stabilization parameter.

- #machine-learning, #optimization.adam, #weight-update

---

## When does the Adam optimization algorithm shuffle the training data?

The algorithm shuffles the training data when $n+B$ exceeds $N$:

$$
\text{if } n + B > N \text{ then shuffle data} 
$$

This ensures the training process is not biased by the order of data points.

- #machine-learning, #optimization.adam, #training-data

---
### Card 1

## What is depicted by the ellipses in Figure 7.3 and what problem can occur with gradient descent in this scenario?

The ellipses in Figure 7.3 depict an error surface $E$ that has the form of a long valley with substantially different curvatures along different directions. In this scenario, the local negative gradient vector $-\nabla E$ does not point towards the minimum of the error function for most points in weight space. This can cause successive steps of gradient descent to oscillate across the valley, leading to very slow progress along the valley towards the minimum.

- #machine-learning, #optimization.gradient-descent, #error-function

---

### Card 2

## What is the impact of the curvature variation in the error surface on the gradient descent process?

When the curvature of $E$ varies significantly with direction, creating a 'valley', the local gradient vector for batch gradient descent, which is perpendicular to the local contour, does not point directly towards the minimum. This causes oscillations across the valley, making progress slow and inefficient. 

- #machine-learning, #optimization.gradient-descent, #curvature

---

### Card 3

## Why do the vectors $\mathbf{u}_{1}$ and $\mathbf{u}_{2}$ play a significant role in the context of gradient descent as illustrated in Figure 7.3?

The vectors $\mathbf{u}_{1}$ and $\mathbf{u}_{2}$ are the eigenvectors of the Hessian matrix. They indicate the directions of principal curvature of the error function. Understanding the eigenvectors helps in visualizing how gradient descent could oscillate and slow down when there are significantly different curvatures along different directions.

- #machine-learning, #optimization.gradient-descent, #eigenvectors

---

### Card 4

## How can the scale $\epsilon$ of the initialization distribution be determined for a neural network unit with M inputs, and what is the importance of this scale?

The scale $\epsilon$ of the initialization distribution for a neural network unit with $M$ inputs can be calculated as:

$$
\epsilon=\sqrt{\frac{2}{M}}
$$

This scale ensures that the initial weights are appropriately small, which can be crucial for training neural networks, especially to ensure most pre-activations are initially active during learning.

- #machine-learning, #neural-networks.initialization, #hyperparameters

---

### Card 5

## Why are bias parameters typically set to small positive values in neural network initialization, and how does this help with ReLU units?

Bias parameters are typically set to small positive values to ensure that most pre-activations are initially active during learning. This is particularly helpful with ReLU units because it ensures that the pre-activations are positive, providing a non-zero gradient to drive learning.

- #machine-learning, #neural-networks.initialization, #bias-parameters

---

### Card 6

## Explain the relationship between the learning rate $\eta$ and the efficiency of the gradient descent process depicted in Figure 7.3.

In the scenario depicted in Figure 7.3, the learning rate $\eta$ influences the step size of the gradient descent process. Although a higher $\eta$ might intuitively seem to lead to faster convergence, it can cause oscillations that become divergent if $\eta$ is too large. As a result, $\eta$ must be kept sufficiently small to avoid divergent oscillations, causing the gradient descent to take many small steps and be very inefficient.

- #machine-learning, #optimization.gradient-descent, #learning-rate
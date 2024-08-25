## What is the effect of a momentum term on the effective value of the learning rate parameter in oscillatory situations in gradient descent?

When successive steps of gradient descent are oscillatory, a momentum term has little influence on the effective value of the learning rate parameter $\eta$. The momentum term tends to cancel out the oscillations and thus the effective learning rate remains close to $\eta$.

$$
\text{Effective Learning Rate} \approx \eta
$$

- #optimization, #gradient-descent.oscillations

---

## What is the typical value of the momentum parameter $\mu$ in practice, and what range should it fall within?

The momentum parameter $\mu$ typically used in practice is 0.9. According to Equation 7.33, $\mu$ should lie within the range:

$$
0 \leq \mu \leq 1
$$

- #optimization, #gradient-descent.momentum

---

## How does the inclusion of momentum term affect the convergence in gradient descent?

The inclusion of a momentum term in gradient descent can lead to faster convergence towards the minimum by mitigating divergent oscillations. This is achieved because the momentum term effectively guides the progress along the valley of the error function more rapidly compared to unmodified gradient descent.

$$
\text{Error Function Valley Progress} \uparrow
$$

- #optimization, #gradient-descent.momentum

---

## Summarize the difference between conventional stochastic gradient descent with momentum and Nesterov momentum.

In conventional stochastic gradient descent with momentum:
1. Compute the gradient at the current position.
2. Take a step amplified by adding previous step's momentum.

In Nesterov momentum:
1. Compute a step based on the previous momentum.
2. Calculate the gradient at this new step taken with the calculated momentum.

- #optimization, #gradient-descent.nesterov-momentum

---

## What is the schematic effect of adding a momentum term to the gradient descent algorithm, according to Figure 7.6?

Adding a momentum term to the gradient descent algorithm results in a more rapid progress along the valley of the error function, as shown in Figure 7.6. This contrasts with the unmodified gradient descent, which has slower progress along the same path.

$$
\text{Gradient Descent with Momentum} \gg \text{Unmodified Gradient Descent}
$$

- #optimization, #gradient-descent.momentum-illustration

---

## Define the update rule for gradient descent with momentum.

The update rule for gradient descent with momentum can be defined as:

$$
v_t = \mu v_{t-1} + \eta \nabla J(\theta)
$$

$$
\theta = \theta - v_t
$$

where:
- $v_t$ is the velocity
- $\mu$ is the momentum parameter (typically 0.9)
- $\eta$ is the learning rate
- $\nabla J(\theta)$ is the gradient at $\theta$

- #optimization, #gradient-descent.momentum-update-rule
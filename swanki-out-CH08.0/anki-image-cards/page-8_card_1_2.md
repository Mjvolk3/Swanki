### Card 1

**Front:**

![](https://cdn.mathpix.com/cropped/2024_05_26_076a5354f07695d4c0c6g-1.jpg?height=811&width=940&top_left_y=217&top_left_x=717)
%
How does the error in numerical gradient computation behave for central differences as the step size $\epsilon$ decreases?

**Back:**

For the central differences method, the error is much smaller compared to finite differences, and it exhibits a quadratic relationship with the step size, $\mathcal{O}(\epsilon^2)$. This means that as $\epsilon$ decreases, the error initially decreases rapidly and forms a slope of 2 on a log-log plot, before numerical round-off errors begin to dominate.

- #numerical-optimization, #gradient-computation, #scientific-computation

### Card 2

**Front:**

![](https://cdn.mathpix.com/cropped/2024_05_26_076a5354f07695d4c0c6g-1.jpg?height=811&width=940&top_left_y=217&top_left_x=717)
%
What happens to the error in the finite differences method when the step size $\epsilon$ becomes very small?

**Back:**

In the finite differences method, as the step size $\epsilon$ becomes very small, the error initially decreases linearly on a log-log scale. However, once it reaches the limit of numerical round-off errors, further reduction in $\epsilon$ leads to increased noise and an overall increase in error. This shows that there is an optimal step size that minimizes error before round-off errors dominate.

- #numerical-optimization, #gradient-computation, #finite-differences
## Evaluate the image and associated text to create an Anki card

![](https://cdn.mathpix.com/cropped/2024_05_26_076a5354f07695d4c0c6g-1.jpg?height=811&width=940&top_left_y=217&top_left_x=717)

% 

Based on the image and associated text, what is the main advantage of using central differences over finite differences for numerical gradient computation?

%

The main advantage of using central differences over finite differences, as depicted in the image, is that central differences result in a much smaller error overall. Specifically, the error associated with central differences behaves according to the order of $\mathcal{O}(\epsilon^2)$, demonstrating a quadratic relationship between the error and the step size, as opposed to the linear error in finite differences. This makes central differences a more accurate method, especially when the step size becomes very small. 

- #numerical-methods, #gradient-computation, #central-differences

## Evaluate the image and associated text to create an Anki card

![](https://cdn.mathpix.com/cropped/2024_05_26_076a5354f07695d4c0c6g-1.jpg?height=811&width=940&top_left_y=217&top_left_x=717)

%

Explain the relationship between the step size $\epsilon$ and numerical round-off errors in the context of finite differences for gradient computation.

%

In the context of finite differences for gradient computation, as the step size $\epsilon$ decreases, the error in the numerical computation initially decreases linearly on a logarithmic scale. However, at some point, the evaluated gradient reaches the limit of numerical round-off, leading to a noisy line where the error actually increases with decreasing $\epsilon$. This phenomenon implies that too small of a step size can degrade the accuracy of the gradient computation due to numerical round-off errors.

- #numerical-methods, #finite-differences, #round-off-errors
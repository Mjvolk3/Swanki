## Effect of Momentum on Gradient Descent

![](https://cdn.mathpix.com/cropped/2024_05_26_26df87b0396463dc47e2g-1.jpg?height=679&width=689&top_left_y=217&top_left_x=955)

Explain the influence of the momentum term on the effective learning rate parameter in the gradient descent algorithm when the successive steps are oscillatory.

%
When successive steps of gradient descent are oscillatory, a momentum term has little influence on the effective value of the learning rate parameter $\eta$. The momentum term tends to cancel out, leading to an effective learning rate that is close to the original $\eta$. Thus, while momentum can accelerate convergence towards the minimum, it also introduces an additional parameter $\mu$ that needs to be fine-tuned.

- machine-learning, optimization.gradient-descent, algorithms.gradient-descent

## Visual Representation of Gradient Descent with Momentum

![](https://cdn.mathpix.com/cropped/2024_05_26_26df87b0396463dc47e2g-1.jpg?height=679&width=689&top_left_y=217&top_left_x=955)

Describe the schematic illustration provided in the image and its relevance to the gradient descent algorithm with momentum.

%
The image provides a schematic illustration of weight updates in an optimization problem as part of an explanation of the gradient descent algorithm with momentum. It shows an abstract error surface, a red downward-facing parabola, and weight update vectors ($\Delta \mathbf{w}^{(1)}$, $\Delta \mathbf{w}^{(2)}$, $\Delta \mathbf{w}^{(3)}$) represented by black arrows. These vectors indicate the direction and magnitude of weight adjustments at each iteration. This type of diagram is used to visually explain how gradient descent with momentum navigates the error landscape to minimize the error function and find an optimal set of parameters.

- machine-learning, optimization, algorithms.gradient-descent
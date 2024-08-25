## How does Nesterov momentum differ from conventional momentum in stochastic gradient descent?

![](https://cdn.mathpix.com/cropped/2024_05_26_26df87b0396463dc47e2g-1.jpg?height=287&width=640&top_left_y=1703&top_left_x=989)

%

In conventional stochastic gradient descent with momentum, the gradient is first computed at the current location, and then a step is taken which is amplified by adding momentum from the previous step. With Nesterov momentum, a step is first computed based on the previous momentum, and then the gradient is calculated.

- #machine-learning.optimization, #nesterov-momentum, #gradient-descent 


## What effect does adding a momentum term have on the gradient descent algorithm, as illustrated in Figure 7.6?

![](https://cdn.mathpix.com/cropped/2024_05_26_26df87b0396463dc47e2g-1.jpg?height=287&width=640&top_left_y=1703&top_left_x=989)

%

Adding a momentum term to the gradient descent algorithm results in more rapid progress along the valley of the error function, showing smoother transitions without oscillating back and forth. This effect is due to the smoothing capabilities of the momentum term in dealing with the problem of differing eigenvalues in the optimization process.

- #machine-learning.optimization, #momentum, #gradient-descent
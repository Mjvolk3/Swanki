## Explain the class-conditional densities and posterior probabilities shown in Figure 5.14.

![](https://cdn.mathpix.com/cropped/2024_05_26_bb6ce2823310d4cb97d4g-1.jpg?height=643&width=701&top_left_y=211&top_left_x=150)

%

Figure 5.14 depicts the class-conditional densities and posterior probabilities for three classes, each following a Gaussian distribution (red, green, and blue). The key points are:

- **Left Plot**: Shows the class-conditional densities with contours representing areas of equal probability density.
  - **Red and Blue Classes**: Identical covariance matrices resulting in linear decision boundary.
  - **Green Class**: Different covariance matrix, leading to quadratic decision boundaries against red and blue classes.
  
- **Right Plot**: Displays posterior probabilities, where each point is colored based on the proportion of posterior probabilities for the three classes. The decision boundaries are explicit, demonstrating linearity between red and blue, and quadratic boundaries for the other class pairs.

- #machine-learning, #classification, #bayesian-theory


## What determines the shape of the decision boundaries among different classes in Figure 5.14?

![](https://cdn.mathpix.com/cropped/2024_05_26_bb6ce2823310d4cb97d4g-1.jpg?height=643&width=701&top_left_y=211&top_left_x=150)

%

In Figure 5.14, the shape of the decision boundaries between different classes is determined by the covariance matrices of the Gaussian distributions:

- **Red and Blue Classes**: Shared covariance matrix, resulting in a linear decision boundary.
- **Other Class Pairs (Red-Green, Blue-Green)**: Different covariance matrices, leading to quadratic decision boundaries.

- #machine-learning, #classification, #decision-boundaries
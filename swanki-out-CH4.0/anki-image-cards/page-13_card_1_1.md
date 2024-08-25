### Card 1

#### Front

![](https://cdn.mathpix.com/cropped/2024_05_26_39f071919089f32e7ef4g-1.jpg?height=1096&width=1512&top_left_y=209&top_left_x=148)

Explain how the Minkowski loss function \( L_q = |f - t|^q \) changes with different values of \( q \) as illustrated in the provided plots.

% 

#### Back

The Minkowski loss function \( L_q = |f - t|^q \) changes as follows for different values of \( q \):

- **\( q = 0.3 \):** The function forms a steep well around \( f - t = 0 \) and flattens out quickly as \( f - t \) moves away from zero.
- **\( q = 1 \):** Represents the absolute loss (linear case) forming a V shape. The gradient remains constant with the distance between prediction \( f \) and target \( t \).
- **\( q = 2 \):** Corresponds to the standard squared loss function, represented as a symmetrical parabola about \( f - t = 0 \), indicating quadratically increasing penalty with deviations from the target.
- **\( q = 10 \):** Results in a very steep and narrow well around \( f - t = 0 \), suggesting an extremely high penalty for even small deviations.

These variations illustrate how different values of \( q \) affect the loss function's sensitivity to errors and its robustness to outliers in regression models.

- #machine-learning.loss-functions, #regression.minkowski-loss, #error-sensitivity

### Card 2

#### Front

![](https://cdn.mathpix.com/cropped/2024_05_26_39f071919089f32e7ef4g-1.jpg?height=1096&width=1512&top_left_y=209&top_left_x=148)

What does the bottom-left plot correspond to in the Minkowski loss functions and what is its characteristic shape?

% 

#### Back

The bottom-left plot corresponds to \( q = 2 \) in the Minkowski loss functions, representing the standard squared loss function. This function is characterized by a symmetrical parabola centered at \( f - t = 0 \), indicating that the penalty for errors increases quadratically as the predictions deviate from the target values.

- #machine-learning.loss-functions, #regression.squared-loss, #error-sensitivity
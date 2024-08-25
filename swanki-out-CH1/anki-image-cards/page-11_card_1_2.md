### How does the root-mean-square error (RMS) vary with the complexity parameter \( M \) on the training and test sets?

![](https://cdn.mathpix.com/cropped/2024_05_18_9b0445fe9c08724522fdg-1.jpg?height=428&width=879&top_left_y=216&top_left_x=779)

%

In Figure 1.7, small values of \( M \) result in large RMS errors for the test set due to underfitting, as the polynomials are too inflexible to capture the function's oscillations. Increasing \( M \) within the range \( 3 \leqslant M \leqslant 8 \) reduces the errors and provides a better representation of the generating function $\sin (2 \pi x)$. However, too large \( M \) values increase the test set error again, indicative of overfitting.

- #machine-learning, #model-complexity, #error-analysis


### Why do small values of \( M \) result in large test set errors in the context of fitting polynomials to data?

![](https://cdn.mathpix.com/cropped/2024_05_18_9b0445fe9c08724522fdg-1.jpg?height=428&width=879&top_left_y=216&top_left_x=779)

%

Small values of \( M \), shown in Figure 1.7, yield large test set errors because the corresponding polynomials are not flexible enough to capture the oscillations of the target function $\sin (2 \pi x)$. This leads to significant underfitting, where the model fails to represent the underlying data pattern accurately.

- #machine-learning, #underfitting, #model-complexity
## How does the root-mean-square error (\(E_{RMS}\)) vary with \(\ln \lambda\) for an \(M=9\) polynomial as shown in Figure 1.10?

![](https://cdn.mathpix.com/cropped/2024_05_18_990fac6c15f219991e40g-1.jpg?height=440&width=884&top_left_y=212&top_left_x=779)

%
The root-mean-square error (\(E_{RMS}\)) decreases initially with \(\ln \lambda\) but then increases, exhibiting a U-shaped behavior for both the training and test curves. The training error (\(E_{RMS}\)) is initially high, decreases to a minimum, and then increases again. The test error follows a similar pattern but intersects the training error at a certain \(\ln \lambda\), indicating the point where the model begins to overfit the data. 

- #machine-learning, #model-selection.hyperparameters, #error-metrics

---

## Why can't the value of the hyperparameter \(\lambda\) be determined by jointly minimizing the error function with respect to \(\mathbf{w}\) and \(\lambda\)?

![](https://cdn.mathpix.com/cropped/2024_05_18_990fac6c15f219991e40g-1.jpg?height=440&width=884&top_left_y=212&top_left_x=779)

%
Jointly minimizing the error function with respect to \(\mathbf{w}\) and \(\lambda\) leads to \(\lambda \rightarrow 0\), resulting in an over-fitted model with small or zero training error. This is undesirable as it fails to generalize well to new, unseen data. Hence, determining the value of hyperparameters must be done through a different process to avoid overfitting.

- #machine-learning, #model-selection.hyperparameters, #overfitting

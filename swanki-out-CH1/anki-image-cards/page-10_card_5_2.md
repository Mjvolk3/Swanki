## How is the concept of overfitting illustrated in the provided image?

![](https://cdn.mathpix.com/cropped/2024_05_18_a0676cf8759377514923g-1.jpg?height=432&width=693&top_left_y=734&top_left_x=953)

%

The concept of overfitting is illustrated by a high-degree polynomial function (red curve) of order $M = 9$ fitted to the data points (blue dots). The function passes exactly through each data point, resulting in $E(\mathbf{w}^{\star}) = 0$, but it oscillates wildly, giving a poor representation of the underlying function $\sin(2 \pi x)$ (green curve). This overfitting occurs because the model is too complex for the true underlying pattern, leading to poor generalization on new data.

- #machine-learning, #overfitting, #polynomial-regression

## What does the green curve represent in the plot, and why is it important?

![](https://cdn.mathpix.com/cropped/2024_05_18_a0676cf8759377514923g-1.jpg?height=432&width=693&top_left_y=734&top_left_x=953)

%

The green curve represents the original function $\sin(2 \pi x)$ that generated the data. It is important because it highlights the true underlying pattern that should be captured by a fitting model. The contrasted red polynomial curve illustrates overfitting, where the model adheres too closely to the noise in the training data, rather than capturing the true underlying function.

- #machine-learning, #overfitting, #ground-truth
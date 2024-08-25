### Anki Card 1

![](https://cdn.mathpix.com/cropped/2024_05_18_a0676cf8759377514923g-1.jpg?height=432&width=693&top_left_y=734&top_left_x=953)

%

**What phenomenon is demonstrated by the plot of a high-degree polynomial fitted to data points, as shown in the image?**

This plot demonstrates the phenomenon of overfitting in machine learning. The high-degree polynomial (red curve) passes through every data point but oscillates wildly, failing to generalize well to the underlying function $\sin(2 \pi x)$ (green curve).

- #machine-learning, #overfitting, #polynomial-regression

### Anki Card 2

![](https://cdn.mathpix.com/cropped/2024_05_18_a0676cf8759377514923g-1.jpg?height=432&width=693&top_left_y=734&top_left_x=953)

%

**Explain why the high-degree polynomial fitted to the data points provides a poor representation of the underlying function.**

The high-degree polynomial exactly passes through each data point, resulting in an error function value of $E(\mathbf{w}^{\star}) = 0$. However, it oscillates wildly between the points, failing to capture the smooth nature of the underlying function $\sin(2 \pi x)$. This overfitting results in a poor representation and generalization of the underlying function.

- #machine-learning, #overfitting, #polynomial-regression
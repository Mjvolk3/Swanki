## Polynomial curve fitting for various polynomial orders (M)

![](https://cdn.mathpix.com/cropped/2024_05_18_a0676cf8759377514923g-1.jpg?height=977&width=1512&top_left_y=203&top_left_x=148)

What does the bottom-right plot (\(M = 9\)) illustrate in the context of overfitting?

%

The bottom-right plot with \(M = 9\) illustrates overfitting. Although the ninth-order polynomial fits all the data points exactly, it oscillates wildly, indicating that it is capturing noise rather than the underlying function \(\sin(2 \pi x)\). This poor generalization to unseen data is characteristic of overfitting.

- #machine-learning, #modeling.overfitting, #polynomial-regression

## Polynomial curve fitting for various polynomial orders (M)

![](https://cdn.mathpix.com/cropped/2024_05_18_a0676cf8759377514923g-1.jpg?height=977&width=1512&top_left_y=203&top_left_x=148)

Describe the general trend observed as the polynomial order \(M\) increases in the plots.

%

As the polynomial order \(M\) increases, the fitted polynomial curves start to follow the data points more closely. Initially, a lower-order polynomial (\(M=0\) and \(M=1\)) provides a simple, smooth approximation but may underfit the data. Increasing \(M\) improves fit quality, with \(M=3\) fitting well. However, an extremely high-order polynomial (\(M=9\)) results in overfitting, where the curve fits the training data perfectly but captures the noise, leading to poor generalization.

- #machine-learning, #modeling, #polynomial-regression
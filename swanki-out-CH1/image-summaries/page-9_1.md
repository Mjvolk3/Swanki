ChatGPT figure/image summary: The image is a graph illustrating a curve fitting problem in the context of machine learning and polynomial regression. It shows a two-dimensional plot where the horizontal axis represents the input variable \( x \), and the vertical axis represents the target variable \( t \).

There are blue points on the graph that signify the training data. Each blue point has a specific position on the horizontal \( x \) axis and a corresponding target value on the vertical \( t \) axis.

A red continuous curve represents the polynomial function \( y(x, \mathbf{w}) \), which has been fitted to the training data. This curve is the result of using a polynomial function to model the underlying trend in the training data.

Green arrows extend vertically from each of the blue points down to the red curve. These green arrows indicate the displacements between the actual target values (\( t_n \)) from the training data and the predictions made by the fitted polynomial (\( y(x_n, \mathbf{w}) \)). The length of an arrow represents the extent to which the model's prediction deviates from the actual data point.

The purpose of the illustration is to visually represent the concept of an error function -- in this case, a sum-of-squares error function -- which measures the difference between the prediction and the actual data points. The goal in curve fitting is to adjust the coefficients of the polynomial (\( \mathbf{w} \)) to minimize the sum of the squares of these errors.
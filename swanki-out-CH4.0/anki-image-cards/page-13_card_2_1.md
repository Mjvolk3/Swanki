## What does the graph in the image illustrate?

![](https://cdn.mathpix.com/cropped/2024_05_26_39f071919089f32e7ef4g-1.jpg?height=504&width=691&top_left_y=217&top_left_x=153)

%
The graph illustrates the plot of the quantity $L_{q} = |f - t|^{q}$ for $q = 0.3$. The horizontal axis represents $f - t$ (the difference between the predicted value $f$ and the target value $t$), and the vertical axis represents $|f - t|^{0.3}$. The curve has a V-like shape, characteristic of graphs of absolute value functions raised to a power less than 1, indicating that as $|f - t|$ increases, the value of $|f - t|^{0.3}$ increases at a slower rate due to the exponent being less than 1. This graph shows the effect of different values of $q$ in the Minkowski loss function on the loss curve, where a lower value of $q$ makes the loss function less sensitive to outliers compared to the squared loss (i.e., $q = 2$).

- #mathematics, #loss-functions, #regression

## How does the value of $q$ in the Minkowski loss function affect the sensitivity to outliers?

![](https://cdn.mathpix.com/cropped/2024_05_26_39f071919089f32e7ef4g-1.jpg?height=504&width=691&top_left_y=217&top_left_x=153)

%

A lower value of $q$ in the Minkowski loss function ($L_{q} = |f - t|^{q}$) makes the loss function less sensitive to outliers. For example, when $q = 0.3$, the increase in loss value $|f - t|^{0.3}$ for large errors $|f - t|$ is slower compared to the quadratic loss function where $q = 2$. Hence, for regression tasks, using lower values of $q$ can reduce the impact of outliers on the model's performance.

- #mathematics, #loss-functions, #outliers
## What is the Root-Mean-Square (RMS) error and how is it related to predicting values for new data observations?

$$
\mathrm{RMS} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} \left( t_i - y(x_i, \mathbf{w}) \right)^2}
$$

The RMS error measures the difference between predicted values $y(x_i, \mathbf{w})$ and actual values $t_i$ over $N$ data points, giving an indication of predictive accuracy.

- #statistical-learning, #error-metrics.root-mean-square

## What observation can we make about $M$ values between 3 and 8 from the provided research?

For values of $M$ in the range $3 \leqslant M \leqslant 8$, the test set error is minimized, indicating these polynomial models capture the underlying function $\sin(2\pi x)$ well.

- #statistical-learning, #model-selection.optimal-M

## For a polynomial of order $M=9$, why does the training set error go to zero, yet the test set error becomes very large?

The polynomial for $M=9$ can perfectly fit the 10 training data points due to having 10 degrees of freedom $\{w_0, w_1, \ldots, w_9\}$. However, this results in overfitting: the model captures the noise in the training data, leading to poor generalization and hence a large test set error.

$$
\mathbf{w} = \{w_0, w_1, \ldots, w_9\}
$$

- #overfitting, #model-complexity.high-degree-polynomials

## Why does a higher-order polynomial potentially perform worse than a lower-order polynomial even though it encompasses all lower-order polynomials?

Although a polynomial of higher order, such as $M=9$, can express more complex relationships and include all lower-order polynomials, it tends to overfit the data, thereby capturing random noise and leading to large oscillations that worsen test set errors.

- #overfitting, #model-complexity.high-order-polynomials

## How does the behavior of the learned model change as the size of the data set is varied?

As the size of the data set increases, the overfitting problem becomes less severe for a given model complexity. This indicates that larger data sets help stabilize the model, reducing its tendency to fit random noise.

$$
\text{Overfitting} \rightarrow \text{Less severe with larger data sets}
$$

- #statistical-learning, #data-quantity.effect
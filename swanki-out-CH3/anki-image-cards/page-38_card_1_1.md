## How does setting the smoothing parameter \( h \) too small affect the kernel density estimation as demonstrated in Figure 3.14?

![](https://cdn.mathpix.com/cropped/2024_05_13_394aafe250f00e0713c1g-1.jpg?height=181&width=628&top_left_y=244&top_left_x=956)

%

Setting \( h \) too small results in a very noisy density model, as shown by the densely oscillating blue line in the top panel of Figure 3.14. This reveals an overfitting issue where the model becomes highly sensitive to local data variations, failing to capture the smoother underlying distribution accurately, represented by the green curve.

- #statistics.kernel-density-estimate, #data-analysis.smoothing-parameter, #machine-learning.overfitting

## Derive the kernel density estimation formula given the Gaussian kernel function.

![](https://cdn.mathpix.com/cropped/2024_05_13_394aafe250f00e0713c1g-1.jpg?height=210&width=630&top_left_y=552&top_left_x=955)

%

The kernel density estimation formula using a Gaussian kernel function is expressed as:

$$
p(\mathbf{x})=\frac{1}{N} \sum_{n=1}^{N} \frac{1}{\left(2 \pi h^{2}\right)^{D / 2}} \exp \left\{-\frac{\left\|\mathbf{x}-\mathbf{x}_{n}\right\|^{2}}{2 h^{2}}\right\}
$$

Here, \( N \) is the number of data points, \( h \) is the bandwidth (smoothing parameter), and \( D \) is the dimensionality of the data. The Gaussian kernel places a Gaussian distribution over each data point \( \mathbf{x}_n \), and the contributions from all points are summed and normalized, ensuring the total area under the density estimate is 1.

- #statistics.kernel-density-estimate, #mathematics.gaussian-kernel, #data-analysis.formula-derivation
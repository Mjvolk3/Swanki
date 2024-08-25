## What are the logistic sigmoid function and the scaled probit function, and how are they related in the given plot?

![](https://cdn.mathpix.com/cropped/2024_05_26_ecc13ea52b1adcd44cf9g-1.jpg?height=498&width=726&top_left_y=230&top_left_x=917)

%

The logistic sigmoid function $\sigma(a)$ is defined as:

$$
\sigma(a) = \frac{1}{1 + \exp(-a)}
$$

The scaled probit function $\Phi(\lambda a)$, with the scaling factor $\lambda^2 = \pi / 8$, is chosen so that the derivatives of both curves are equal for $a = 0$. 

The plot shows:
- The logistic sigmoid function (red solid curve)
- The scaled probit function (blue dashed curve)

The scaling factor ensures that the two curves have the same derivative at $a = 0$.

- #mathematics, #functions.sigmoid, #classification.probit

## How is the probability \( p(\mathcal{C}_1 \mid \mathbf{x}) \) related to the logistic sigmoid function?

![](https://cdn.mathpix.com/cropped/2024_05_26_ecc13ea52b1adcd44cf9g-1.jpg?height=498&width=726&top_left_y=230&top_left_x=917)

%

The probability \( p(\mathcal{C}_1 \mid \mathbf{x}) \) can be written as:

$$
p(\mathcal{C}_1 \mid \mathbf{x}) = \frac{p(\mathbf{x} \mid \mathcal{C}_1) p(\mathcal{C}_1)}{p(\mathbf{x} \mid \mathcal{C}_1) p(\mathcal{C}_1) + p(\mathbf{x} \mid \mathcal{C}_2) p(\mathcal{C}_2)}
$$

This expression simplifies to:

$$
p(\mathcal{C}_1 \mid \mathbf{x}) = \frac{1}{1 + \exp(-a)} = \sigma(a)
$$

where 

$$
a = \ln \left(\frac{p(\mathbf{x} \mid \mathcal{C}_1) p(\mathcal{C}_1)}{p(\mathbf{x} \mid \mathcal{C}_2) p(\mathcal{C}_2)}\right)
$$

and $\sigma(a)$ is the logistic sigmoid function.

- #mathematics, #functions.sigmoid, #classification.probability
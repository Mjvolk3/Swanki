### Card 1

![](https://cdn.mathpix.com/cropped/2024_05_26_ecc13ea52b1adcd44cf9g-1.jpg?height=498&width=726&top_left_y=230&top_left_x=917)

What is the definition of the logistic sigmoid function $\sigma(a)$ and how is it used in classification?

%

The logistic sigmoid function $\sigma(a)$ is defined as:

$$
\sigma(a)=\frac{1}{1+\exp(-a)}
$$

It is used to map any real-valued input $a$ into a value between 0 and 1, which represents a probability. This function is particularly useful in binary classification algorithms, as it outputs the probability of the input belonging to a particular class.

- #mathematics.functions, #machine-learning.classification, #sigmoid_function

---

### Card 2

![](https://cdn.mathpix.com/cropped/2024_05_26_ecc13ea52b1adcd44cf9g-1.jpg?height=498&width=726&top_left_y=230&top_left_x=917)

Explain the relationship between the logistic sigmoid function $\sigma(a)$ and the scaled probit function $\Phi(\lambda a)$ in the context of Figure 5.12.

%

In Figure 5.12, the logistic sigmoid function $\sigma(a)$, shown as the solid red curve, and the scaled probit function $\Phi(\lambda a)$, shown as the dashed blue curve, are compared. The scaling factor $\lambda^2 = \frac{\pi}{8}$ ensures that the derivatives of both functions are equal at $a = 0$. Both functions map real-valued inputs into a range between 0 and 1, useful for representing probabilities in classification tasks, with $\sigma(a)$ defined by:

$$
\sigma(a) = \frac{1}{1 + \exp(-a)}
$$

and $\Phi(a)$ as the cumulative distribution function of a standard normal distribution.

- #mathematics.functions, #machine-learning.classification, #probit_function
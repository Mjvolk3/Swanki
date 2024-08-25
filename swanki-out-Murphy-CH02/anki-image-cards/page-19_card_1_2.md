## What is the sigmoid (logistic) function and what are some of its key properties?

![](https://cdn.mathpix.com/cropped/2024_06_13_5e8463dfe213d57710b3g-1.jpg?height=510&width=1248&top_left_y=222&top_left_x=381)

% 

The sigmoid (logistic) function $\sigma(a)$ is defined as:

$$
\sigma(a) = \left(1 + e^{-a} \right)^{-1}
$$

Some key properties include:

$$
\begin{aligned}
\sigma(x) & \triangleq \frac{1}{1+e^{-x}} = \frac{e^{x}}{1+e^{x}} \\
\frac{d}{d x} \sigma(x) & = \sigma(x)(1-\sigma(x)) \\
1-\sigma(x) & = \sigma(-x) \\
\sigma^{-1}(p) & = \log \left(\frac{p}{1-p}\right) \triangleq \operatorname{logit}(p) \\
\sigma_{+}(x) & \triangleq \log \left(1+e^{x}\right) \triangleq \operatorname{softplus}(x) \\
\frac{d}{d x} \sigma_{+}(x) & = \sigma(x)
\end{aligned}
$$

- #mathematics.sigmoid-function, #machine-learning.activation-functions, #calculus.derivatives

---

## Describe the Heaviside function and its typical use in modeling.

![](https://cdn.mathpix.com/cropped/2024_06_13_5e8463dfe213d57710b3g-1.jpg?height=510&width=1248&top_left_y=222&top_left_x=381)

%

The Heaviside function $\mathbb{I}(a > 0)$, also known as the unit step function, is defined as:

$$
\mathbb{I}(a > 0) =
\begin{cases} 
0 & \text{if } a \leq 0, \\
1 & \text{if } a > 0.
\end{cases}
$$

This function is commonly used to model situations where there is a switch from one state to another at a certain threshold.

- #mathematics.heaviside-function, #modeling.step-functions, #applications.physical-systems
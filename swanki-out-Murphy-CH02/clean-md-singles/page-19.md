![](https://cdn.mathpix.com/cropped/2024_06_13_5e8463dfe213d57710b3g-1.jpg?height=510&width=1248&top_left_y=222&top_left_x=381)

Figure 2.10: (a) The sigmoid (logistic) function $\sigma(a)=\left(1+e^{-a}\right)^{-1}$. (b) The Heaviside function $\mathbb{I}(a>0)$. Generated by activation_fun_plot.ipynb.

$$
\begin{aligned}
\sigma(x) & \triangleq \frac{1}{1+e^{-x}}=\frac{e^{x}}{1+e^{x}} \\
\frac{d}{d x} \sigma(x) & =\sigma(x)(1-\sigma(x)) \\
1-\sigma(x) & =\sigma(-x) \\
\sigma^{-1}(p) & =\log \left(\frac{p}{1-p}\right) \triangleq \operatorname{logit}(p) \\
\sigma_{+}(x) & \triangleq \log \left(1+e^{x}\right) \triangleq \operatorname{softplus}(x) \\
\frac{d}{d x} \sigma_{+}(x) & =\sigma(x)
\end{aligned}
$$

Table 2.3: Some useful properties of the sigmoid (logistic) and related functions. Note that the logit function is the inverse of the sigmoid function, and has a domain of $[0,1]$.

where $f(\boldsymbol{x} ; \boldsymbol{\theta})$ is some function that predicts the mean parameter of the output distribution. We will consider many different kinds of function $f$ in Part II-Part IV.

To avoid the requirement that $0 \leq f(\boldsymbol{x} ; \boldsymbol{\theta}) \leq 1$, we can let $f$ be an unconstrained function, and use the following model:

$$
p(y \mid \boldsymbol{x}, \boldsymbol{\theta})=\operatorname{Ber}(y \mid \sigma(f(\boldsymbol{x} ; \boldsymbol{\theta})))
$$

Here $\sigma()$ is the sigmoid or logistic function, defined as follows:

$$
\sigma(a) \triangleq \frac{1}{1+e^{-a}}
$$

where $a=f(\boldsymbol{x} ; \boldsymbol{\theta})$. The term "sigmoid" means S-shaped: see Figure 2.10a for a plot. We see that it Author: Kevin P. Murphy. (C) MIT Press. CC-BY-NC-ND license
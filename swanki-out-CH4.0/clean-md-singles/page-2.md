\title{
4.1. Linear Regression
}

The goal of regression is to predict the value of one or more continuous target variables $t$ given the value of a $D$-dimensional vector $\mathbf{x}$ of input variables. Typically we are given a training data set comprising $N$ observations $\left\{\mathbf{x}_{n}\right\}$, where $n=1, \ldots, N$, together with corresponding target values $\left\{t_{n}\right\}$, and the goal is to predict the value of $t$ for a new value of $\mathbf{x}$. To do this, we formulate a function $y(\mathbf{x}, \mathbf{w})$ whose values for new inputs $\mathbf{x}$ constitute the predictions for the corresponding values of $t$, and where $\mathrm{w}$ represents a vector of parameters that can be learned from the training data.

The simplest model for regression is one that involves a linear combination of the input variables:

$$
y(\mathbf{x}, \mathbf{w})=w_{0}+w_{1} x_{1}+\ldots+w_{D} x_{D}
$$

where $\mathbf{x}=\left(x_{1}, \ldots, x_{D}\right)^{\mathrm{T}}$. The term linear regression sometimes refers specifically to this form of model. The key property of this model is that it is a linear function of the parameters $w_{0}, \ldots, w_{D}$. It is also, however, a linear function of the input variables $x_{i}$, and this imposes significant limitations on the model.

\subsection*{4.1.1 Basis functions}

We can extend the class of models defined by (4.1) by considering linear combinations of fixed nonlinear functions of the input variables, of the form

$$
y(\mathbf{x}, \mathbf{w})=w_{0}+\sum_{j=1}^{M-1} w_{j} \phi_{j}(\mathbf{x})
$$

where $\phi_{j}(\mathrm{x})$ are known as basis functions. By denoting the maximum value of the index $j$ by $M-1$, the total number of parameters in this model will be $M$.

The parameter $w_{0}$ allows for any fixed offset in the data and is sometimes called

Section 4.3

Section 6.1 a bias parameter (not to be confused with bias in a statistical sense). It is often convenient to define an additional dummy basis function $\phi_{0}(\mathbf{x})$ whose value is fixed at $\phi_{0}(\mathbf{x})=1$ so that $(4.2)$ becomes

$$
y(\mathbf{x}, \mathbf{w})=\sum_{j=0}^{M-1} w_{j} \phi_{j}(\mathbf{x})=\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}(\mathbf{x})
$$

where $\mathbf{w}=\left(w_{0}, \ldots, w_{M-1}\right)^{\mathrm{T}}$ and $\boldsymbol{\phi}=\left(\phi_{0}, \ldots, \phi_{M-1}\right)^{\mathrm{T}}$. We can represent the model (4.3) using a neural network diagram, as shown in Figure 4.1.

By using nonlinear basis functions, we allow the function $y(\mathbf{x}, \mathbf{w})$ to be a nonlinear function of the input vector $\mathbf{x}$. Functions of the form (4.2) are called linear models, however, because they are linear in $\mathbf{w}$. It is this linearity in the parameters that will greatly simplify the analysis of this class of models. However, it also leads to some significant limitations.
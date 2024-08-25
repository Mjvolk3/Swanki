## Appendix B of the paper discusses the calculus of variations. What is a functional?

A functional $F[y]$ is an operator that takes a function $y(x)$ and returns a scalar value $F$. 

For example, the entropy $\mathrm{H}[x]$ for a continuous variable $x$ is a functional since it returns the entropy value of $x$ under a given probability density function $p(x)$.

- #calculus-of-variations, #functionals

## Define $$y(x+\epsilon)$$ in terms of its expansion.

Given the function $y(x)$, when we make a small change $\epsilon$ to the variable $x$, we can expand $y(x)$ as:

$$
y(x+\epsilon)=y(x)+\frac{\mathrm{d} y}{\mathrm{~d} x} \epsilon+\mathcal{O}\left(\epsilon^{2}\right)
$$

Here, $\mathcal{O}\left(\epsilon^{2}\right)$ represents higher-order terms that become negligible as $\epsilon \rightarrow 0$.

- #calculus, #function-expansion

## How do functional derivatives in the calculus of variations analogously arise compared to partial derivatives?

Functional derivatives arise in the context of variations of a functional $F[y]$, similar to how partial derivatives arise in functions of several variables.

For a function $y\left(x_{1}, \ldots, x_{D}\right)$, we have:

$$
y\left(x_{1}+\epsilon_{1}, \ldots, x_{D}+\epsilon_{D}\right)=y\left(x_{1}, \ldots, x_{D}\right)+\sum_{i=1}^{D} \frac{\partial y}{\partial x_{i}} \epsilon_{i}+\mathcal{O}\left(\epsilon^{2}\right)
$$

For a functional $F[y]$, we consider a small change $\epsilon \eta(x)$ to the function $y(x)$ to define its variation.

- #calculus-of-variations, #functional-derivatives

## How would one evaluate a conventional derivative $\frac{\mathrm{d} y}{\mathrm{~d} x}$ using an expansion method without ordinary calculus' rules?

One could evaluate $\frac{\mathrm{d} y}{\mathrm{~d} x}$ by making a small change $\epsilon$ to $x$ and expanding $y(x+\epsilon)$ as follows:

$$
y(x+\epsilon)=y(x)+\frac{\mathrm{d} y}{\mathrm{~d} x} \epsilon+\mathcal{O}\left(\epsilon^{2}\right)
$$

Finally, take the limit as $\epsilon \rightarrow 0$ to isolate the term involving $\frac{\mathrm{d} y}{\mathrm{~d} x}$.

- #calculus, #derivatives

## What is the main goal in the calculus of variations?

In the calculus of variations, the primary objective is to find a function $y(x)$ that maximizes or minimizes a functional $F[y]$. 

This is analogous to finding the value of $x$ that maximizes or minimizes a function $y(x)$ in conventional calculus.

- #calculus-of-variations, #optimization

## How is the concept of a functional useful in machine learning?

In machine learning, a functional can represent various objectives, such as the entropy functional $\mathrm{H}[x]$. For a continuous variable $x$ with a probability density function $p(x)$, the entropy functional $\mathrm{H}[p]$ returns the entropy of $x$ under the given density.

Thus, functional forms are critical for defining objectives and constraints in optimization problems in machine learning.

- #machine-learning, #entropy, #functionals
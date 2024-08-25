\title{
Appendix C. Lagrange Multipliers
}

Lagrange multipliers, also sometimes called undetermined multipliers, are used to find the stationary points of a function of several variables subject to one or more constraints.

Consider the problem of finding the maximum of a function $f\left(x_{1}, x_{2}\right)$ subject to a constraint relating $x_{1}$ and $x_{2}$, which we write in the form

$$
g\left(x_{1}, x_{2}\right)=0
$$

One approach would be to solve the constraint equation (C.1) and thus express $x_{2}$ as a function of $x_{1}$ in the form $x_{2}=h\left(x_{1}\right)$. This can then be substituted into $f\left(x_{1}, x_{2}\right)$ to give a function of $x_{1}$ alone of the form $f\left(x_{1}, h\left(x_{1}\right)\right)$. The maximum with respect to $x_{1}$ could then be found by differentiation in the usual way, to give the stationary value $x_{1}^{\star}$, with the corresponding value of $x_{2}$ given by $x_{2}^{\star}=h\left(x_{1}^{\star}\right)$.

One problem with this approach is that it may be difficult to find an analytic solution of the constraint equation that allows $x_{2}$ to be expressed as an explicit function of $x_{1}$. Also, this approach treats $x_{1}$ and $x_{2}$ differently and so spoils the natural symmetry between these variables.

A more elegant, and often simpler, approach introduces a parameter $\lambda$ called a Lagrange multiplier. We shall motivate this technique from a geometrical perspective. Consider a $D$-dimensional variable $\mathbf{x}$ with components $x_{1}, \ldots, x_{D}$. The constraint equation $g(\mathbf{x})=0$ then represents a $(D-1)$-dimensional surface in $\mathbf{x}$-space as indicated in Figure C.1.

First note that at any point on the constraint surface, the gradient $\nabla g(\mathbf{x})$ of the constraint function is orthogonal to the surface. To see this, consider a point $\mathbf{x}$ that lies on the constraint surface along with a nearby point $\mathbf{x}+\boldsymbol{\epsilon}$ that also lies on the surface. If we make a Taylor expansion around $\mathbf{x}$, we have

$$
g(\mathbf{x}+\boldsymbol{\epsilon}) \simeq g(\mathbf{x})+\boldsymbol{\epsilon}^{\mathrm{T}} \nabla g(\mathbf{x})
$$

Because both $\mathbf{x}$ and $\mathbf{x}+\boldsymbol{\epsilon}$ lie on the constraint surface, we have $g(\mathbf{x})=g(\mathbf{x}+\boldsymbol{\epsilon})$ and hence $\boldsymbol{\epsilon}^{\mathrm{T}} \nabla g(\mathbf{x}) \simeq 0$. In the limit $\|\boldsymbol{\epsilon}\| \rightarrow 0$, we have $\boldsymbol{\epsilon}^{\mathrm{T}} \nabla g(\mathbf{x})=0$, and because $\boldsymbol{\epsilon}$ is
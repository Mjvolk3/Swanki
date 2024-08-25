the problem of maximizing $f(\mathbf{x})$ subject to $g(\mathbf{x}) \geqslant 0$ is obtained by optimizing the Lagrange function (C.4) with respect to $\mathrm{x}$ and $\lambda$ subject to the conditions

$$
\begin{aligned}
g(\mathbf{x}) & \geqslant 0 \\
\lambda & \geqslant 0 \\
\lambda g(\mathbf{x}) & =0
\end{aligned}
$$

These are known as the Karush-Kuhn-Tucker (KKT) conditions (Karush, 1939; Kuhn and Tucker, 1951).

Note that if we wish to minimize (rather than maximize) the function $f(\mathbf{x})$ subject to an inequality constraint $g(\mathbf{x}) \geqslant 0$, then we minimize the Lagrangian function $L(\mathbf{x}, \lambda)=f(\mathbf{x})-\lambda g(\mathbf{x})$ with respect to $\mathbf{x}$, again subject to $\lambda \geqslant 0$.

Finally, it is straightforward to extend the technique of Lagrange multipliers to cases with multiple equality and inequality constraints. Suppose we wish to maximize $f(\mathbf{x})$ subject to $g_{j}(\mathbf{x})=0$ for $j=1, \ldots, J$, and $h_{k}(\mathbf{x}) \geqslant 0$ for $k=1, \ldots, K$. We then introduce Lagrange multipliers $\left\{\lambda_{j}\right\}$ and $\left\{\mu_{k}\right\}$, and then optimize the Lagrangian function given by

$$
L\left(\mathbf{x},\left\{\lambda_{j}\right\},\left\{\mu_{k}\right\}\right)=f(\mathbf{x})+\sum_{j=1}^{J} \lambda_{j} g_{j}(\mathbf{x})+\sum_{k=1}^{K} \mu_{k} h_{k}(\mathbf{x})
$$

subject to $\mu_{k} \geqslant 0$ and $\mu_{k} h_{k}(\mathbf{x})=0$ for $k=1, \ldots, K$. Extensions to constrained functional derivatives are similarly straightforward. For a more detailed discussion of the technique of Lagrange multipliers, see Nocedal and Wright (1999).
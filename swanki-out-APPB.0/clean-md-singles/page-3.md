from which we can read off the functional derivative by comparison with (B.3). Requiring that the functional derivative vanishes then gives

$$
\frac{\partial G}{\partial y}-\frac{\mathrm{d}}{\mathrm{d} x}\left(\frac{\partial G}{\partial y^{\prime}}\right)=0
$$

which are known as the Euler-Lagrange equations. For example, if

$$
G=y(x)^{2}+\left(y^{\prime}(x)\right)^{2}
$$

then the Euler-Lagrange equations take the form

$$
y(x)-\frac{\mathrm{d}^{2} y}{\mathrm{~d} x^{2}}=0
$$

This second-order differential equation can be solved for $y(x)$ by making use of the boundary conditions on $y(x)$.

Often, we consider functionals defined by integrals whose integrands take the form $G(y, x)$ and that do not depend on the derivatives of $y(x)$. In this case, stationarity simply requires that $\partial G / \partial y(x)=0$ for all values of $x$.

If we are optimizing a functional with respect to a probability distribution, then we need to maintain the normalization constraint on the probabilities. This is often most conveniently done using a Lagrange multiplier, which then allows an unconstrained optimization to be performed.

The extension of the above results to a multi-dimensional variable $\mathrm{x}$ is straightforward. For a more comprehensive discussion of the calculus of variations, see Sagan (1969).
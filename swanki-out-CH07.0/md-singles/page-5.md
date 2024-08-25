Figure 7.2 In the neighbourhood of a minimum \(\mathrm{w}^{\star}\), the error function can be approximated by a quadratic. Contours of constant error are then ellipses whose axes are aligned with the eigenvectors \(\mathbf{u}_{i}\) of the Hessian matrix, with lengths that are inversely proportional to the square roots of the corresponding eigenvectors

![](https://cdn.mathpix.com/cropped/2024_05_26_2a651def79b1bf34dbe2g-1.jpg?height=451&width=767&top_left_y=219&top_left_x=877)

Because the eigenvectors \(\left\{\mathbf{u}_{i}\right\}\) form a complete set, an arbitrary vector \(\mathbf{v}\) can be written in the form

\[
\mathbf{v}=\sum_{i} c_{i} \mathbf{u}_{i}
\]

From (7.8) and (7.9), we then have

\[
\mathbf{v}^{\mathrm{T}} \mathbf{H} \mathbf{v}=\sum_{i} c_{i}^{2} \lambda_{i}
\]

Exercise 7.2 and so \(\mathbf{H}\) will be positive definite if, and only if, all its eigenvalues are positive. Thus, a necessary and sufficient condition for \(\mathbf{w}^{\star}\) to be a local minimum is that the gradient of the error function should vanish at \(\mathbf{w}^{\star}\) and the Hessian matrix evaluated Exercise \(7.3 \quad\) at \(\mathbf{w}^{\star}\) should be positive definite. In the new coordinate system, whose basis vectors are given by the eigenvectors \(\left\{\mathbf{u}_{i}\right\}\), the contours of constant \(E(\mathbf{w})\) are axis-aligned Exercise \(7.6 \quad\) ellipses centred on the origin, as illustrated in Figure 7.2.

\title{
7.2. Gradient Descent Optimization
}

There is little hope of finding an analytical solution to the equation \(\nabla E(\mathbf{w})=0\) for an error function as complex as one defined by a neural network, and so we resort to iterative numerical procedures. The optimization of continuous nonlinear functions is a widely studied problem, and there exists an extensive literature on how to solve it efficiently. Most techniques involve choosing some initial value \(\mathbf{w}^{(0)}\) for the weight vector and then moving through weight space in a succession of steps of the form

\[
\mathbf{w}^{(\tau)}=\mathbf{w}^{(\tau-1)}+\Delta \mathbf{w}^{(\tau-1)}
\]

where \(\tau\) labels the iteration step. Different algorithms involve different choices for the weight vector update \(\Delta \mathbf{w}^{(\tau)}\).

Because of the complex shape of the error surface for all but the simplest neural networks, the solution found will depend, among other things, on the particular choice of initial parameter values \(\mathbf{w}^{(0)}\). To find a sufficiently good solution, it may
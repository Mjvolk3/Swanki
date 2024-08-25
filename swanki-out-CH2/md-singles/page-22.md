Figure 2.12 Example of the transformation of the mode of a density under a nonlinear change of variables, illustrating the different behaviour compared to a simple function.

![](https://cdn.mathpix.com/cropped/2024_05_10_99e0ce50ade2d8f270a1g-1.jpg?height=498&width=721&top_left_y=220&top_left_x=939)

If we simply transform \(p_{x}(x)\) as a function of \(x\) we obtain the green curve \(p_{x}(g(y))\) shown in Figure 2.12, and we see that the mode of the density \(p_{x}(x)\) is transformed via the sigmoid function to the mode of this curve. However, the density over \(y\) transforms instead according to (2.71) and is shown by the magenta curve on the left side of the diagram. Note that this has its mode shifted relative to the mode of the green curve.

To confirm this result, we take our sample of 50,000 values of \(x\), evaluate the corresponding values of \(y\) using (2.75), and then plot a histogram of their values. We see that this histogram matches the magenta curve in Figure 2.12 and not the green curve.

\title{
2.4.1 Multivariate distributions
}

We can extend the result (2.71) to densities defined over multiple variables. Consider a density \(p(\mathbf{x})\) over a \(D\)-dimensional variable \(\mathbf{x}=\left(x_{1}, \ldots, x_{D}\right)^{\mathrm{T}}\), and suppose we transform to a new variable \(\mathbf{y}=\left(y_{1}, \ldots, y_{D}\right)^{\mathrm{T}}\) where \(\mathbf{x}=\mathbf{g}(\mathbf{y})\). Here we will limit ourselves to the case where \(\mathbf{x}\) and \(\mathbf{y}\) have the same dimensionality. The transformed density is then given by the generalization of (2.71) in the form

\[
p_{\mathbf{y}}(\mathbf{y})=p_{\mathbf{x}}(\mathbf{x})|\operatorname{det} \mathbf{J}|
\]

where \(\mathbf{J}\) is the Jacobian matrix whose elements are given by the partial derivatives \(J_{i j}=\partial g_{i} / \partial y_{j}\), so that

\[
\mathbf{J}=\left[\begin{array}{ccc}
\frac{\partial g_{1}}{\partial y_{1}} & \cdots & \frac{\partial g_{1}}{\partial y_{D}} \\
\vdots & \ddots & \vdots \\
\frac{\partial g_{D}}{\partial y_{1}} & \cdots & \frac{\partial g_{D}}{\partial y_{D}}
\end{array}\right]
\]

Intuitively, we can view the change of variables as expanding some regions of space and contracting others, with an infinitesimal region \(\Delta \mathrm{x}\) around a point \(\mathrm{x}\) being transformed to a region \(\Delta \mathbf{y}\) around the point \(\mathbf{y}=\mathbf{g}(\mathbf{x})\). The absolute value of the determinant of the Jacobian represents the ratio of these volumes and is the same factor
Figure 5.1 Illustration of the geometry of a linear discriminant function in two dimensions. The decision surface, shown in red, is perpendicular to \(\mathbf{w}\), and its displacement from the origin is controlled by the bias parameter \(w_{0}\). Also, the signed orthogonal distance of a general point \(\mathrm{x}\) from the decision surface is given by \(y(\mathbf{x}) /\|\mathbf{w}\|\).

![](https://cdn.mathpix.com/cropped/2024_05_26_54f3776e893a83ecd076g-1.jpg?height=698&width=898&top_left_y=215&top_left_x=760)

the \(D\)-dimensional input space. Consider two points \(\mathbf{x}_{\mathrm{A}}\) and \(\mathbf{x}_{\mathrm{B}}\) both of which lie on the decision surface. Because \(y\left(\mathbf{x}_{\mathrm{A}}\right)=y\left(\mathbf{x}_{\mathrm{B}}\right)=0\), we have \(\mathbf{w}^{\mathrm{T}}\left(\mathbf{x}_{\mathrm{A}}-\mathbf{x}_{\mathrm{B}}\right)=0\) and hence the vector \(\mathbf{w}\) is orthogonal to every vector lying within the decision surface, and so \(\mathrm{w}\) determines the orientation of the decision surface. Similarly, if \(\mathrm{x}\) is a point on the decision surface, then \(y(\mathrm{x})=0\), and so the normal distance from the origin to the decision surface is given by

\[
\frac{\mathbf{w}^{\mathrm{T}} \mathbf{x}}{\|\mathbf{w}\|}=-\frac{w_{0}}{\|\mathbf{w}\|}
\]

We therefore see that the bias parameter \(w_{0}\) determines the location of the decision surface. These properties are illustrated for the case of \(D=2\) in Figure 5.1.

Furthermore, note that the value of \(y(\mathbf{x})\) gives a signed measure of the perpendicular distance \(r\) of the point \(\mathbf{x}\) from the decision surface. To see this, consider an arbitrary point \(\mathbf{x}\) and let \(\mathbf{x}_{\perp}\) be its orthogonal projection onto the decision surface, so that

\[
\mathbf{x}=\mathbf{x}_{\perp}+r \frac{\mathbf{w}}{\|\mathbf{w}\|}
\]

Multiplying both sides of this result by \(\mathbf{w}^{\mathrm{T}}\) and adding \(w_{0}\), and making use of \(y(\mathbf{x})=\) \(\mathbf{w}^{\mathrm{T}} \mathbf{x}+w_{0}\) and \(y\left(\mathbf{x}_{\perp}\right)=\mathbf{w}^{\mathrm{T}} \mathbf{x}_{\perp}+w_{0}=0\), we have

\[
r=\frac{y(\mathbf{x})}{\|\mathbf{w}\|}
\]

This result is illustrated in Figure 5.1.

Section 4.1.1

As with linear regression models, it is sometimes convenient to use a more compact notation in which we introduce an additional dummy 'input' value \(x_{0}=1\) and then define \(\widetilde{\mathbf{w}}=\left(w_{0}, \mathbf{w}\right)\) and \(\widetilde{\mathbf{x}}=\left(x_{0}, \mathbf{x}\right)\) so that

\[
y(\mathbf{x})=\widetilde{\mathbf{w}}^{\mathrm{T}} \widetilde{\mathbf{x}}
\]
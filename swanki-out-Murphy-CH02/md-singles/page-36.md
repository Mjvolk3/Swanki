
![](https://cdn.mathpix.com/cropped/2024_06_13_a723e795abd87511cc8bg-1.jpg?height=390&width=938&top_left_y=198&top_left_x=548)

Figure 2.20: Illustration of an affine transformation applied to a unit square, \(f(\boldsymbol{x})=\mathbf{A} \boldsymbol{x}+\boldsymbol{b}\). (a) Here \(\mathbf{A}=\mathbf{I}\). (b) Here \(\boldsymbol{b}=\mathbf{0}\). From [Jan18]. Used with kind permission of Eric Jang.

analogy with the scalar case, we have

\[
p_{y}(\boldsymbol{y})=p_{x}(\boldsymbol{g}(\boldsymbol{y}))\left|\operatorname{det}\left[\mathbf{J}_{g}(\boldsymbol{y})\right]\right|
\]

where \(\mathbf{J}_{g}=\frac{d \boldsymbol{g}(\boldsymbol{y})}{d \boldsymbol{y}^{\top}}\) is the Jacobian of \(\boldsymbol{g}\), and \(|\operatorname{det} \mathbf{J}(\boldsymbol{y})|\) is the absolute value of the determinant of \(\mathbf{J}\) evaluated at \(\boldsymbol{y}\). (See Section 7.8.5 for a discussion of Jacobians.) In Exercise 3.6 you will use this formula to derive the normalization constant for a multivariate Gaussian.

Figure 2.20 illustrates this result in \(2 \mathrm{~d}\), for the case where \(f(\boldsymbol{x})=\mathbf{A} \boldsymbol{x}+\boldsymbol{b}\), where \(\mathbf{A}=\left(\begin{array}{ll}a & c \\ b & d\end{array}\right)\). We see that the area of the unit square changes by a factor of \(\operatorname{det}(\mathbf{A})=a d-b c\), which is the area of the parallelogram.

As another example, consider transforming a density from Cartesian coordinates \(\boldsymbol{x}=\left(x_{1}, x_{2}\right)\) to polar coordinates \(\boldsymbol{y}=\boldsymbol{f}\left(x_{1}, x_{2}\right)\), so \(\boldsymbol{g}(r, \theta)=(r \cos \theta, r \sin \theta)\). Then

\[
\begin{aligned}
\mathbf{J}_{g} & =\left(\begin{array}{ll}
\frac{\partial x_{1}}{\partial x_{2}} & \frac{\partial x_{1}}{\partial \theta_{2}} \\
\frac{\partial x_{2}}{\partial r} & \frac{\partial x_{2}}{\partial \theta}
\end{array}\right)=\left(\begin{array}{cc}
\cos \theta & -r \sin \theta \\
\sin \theta & r \cos \theta
\end{array}\right) \\
\left|\operatorname{det}\left(\mathbf{J}_{g}\right)\right| & =\left|r \cos ^{2} \theta+r \sin ^{2} \theta\right|=|r|
\end{aligned}
\]

Hence

\[
p_{r, \theta}(r, \theta)=p_{x_{1}, x_{2}}(r \cos \theta, r \sin \theta) r
\]

To see this geometrically, notice that the area of the shaded patch in Figure 2.21 is given by

\[
\operatorname{Pr}(r \leq R \leq r+d r, \theta \leq \Theta \leq \theta+d \theta)=p_{r, \theta}(r, \theta) d r d \theta
\]

In the limit, this is equal to the density at the center of the patch times the size of the patch, which is given by \(r d r d \theta\). Hence

\[
p_{r, \theta}(r, \theta) d r d \theta=p_{x_{1}, x_{2}}(r \cos \theta, r \sin \theta) r d r d \theta
\]
![](https://cdn.mathpix.com/cropped/2024_05_13_cf325eae3c87c1cb9850g-1.jpg?height=715&width=1341&top_left_y=209&top_left_x=248)

![](https://cdn.mathpix.com/cropped/2024_05_13_cf325eae3c87c1cb9850g-1.jpg?height=640&width=630&top_left_y=217&top_left_x=252)

(a)

![](https://cdn.mathpix.com/cropped/2024_05_13_cf325eae3c87c1cb9850g-1.jpg?height=642&width=594&top_left_y=214&top_left_x=973)

(b)

Figure 3.5 (a) Contours of a Gaussian distribution \(p\left(x_{a}, x_{b}\right)\) over two variables. (b) The marginal distribution \(p\left(x_{a}\right)\) (blue curve) and the conditional distribution \(p\left(x_{a} \mid x_{b}\right)\) for \(x_{b}=0.7\) (red curve).

where \(\boldsymbol{\mu}, \mathbf{A}\), and \(\mathbf{b}\) are parameters governing the means, and \(\boldsymbol{\Lambda}\) and \(\mathbf{L}\) are precision matrices. If \(\mathbf{x}\) has dimensionality \(M\) and \(\mathbf{y}\) has dimensionality \(D\), then the matrix \(\mathbf{A}\) has size \(D \times M\).

First we find an expression for the joint distribution over \(\mathbf{x}\) and \(\mathbf{y}\). To do this, we define

\[
\mathrm{z}=\binom{\mathrm{x}}{\mathrm{y}}
\]

and then consider the log of the joint distribution:

\[
\begin{aligned}
\ln p(\mathbf{z})= & \ln p(\mathbf{x})+\ln p(\mathbf{y} \mid \mathbf{x}) \\
= & -\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^{\mathrm{T}} \boldsymbol{\Lambda}(\mathbf{x}-\boldsymbol{\mu}) \\
& -\frac{1}{2}(\mathbf{y}-\mathbf{A} \mathbf{x}-\mathbf{b})^{\mathrm{T}} \mathbf{L}(\mathbf{y}-\mathbf{A} \mathbf{x}-\mathbf{b})+\text { const }
\end{aligned}
\]

where 'const' denotes terms independent of \(\mathbf{x}\) and \(\mathbf{y}\). As before, we see that this is a quadratic function of the components of \(\mathbf{z}\), and hence, \(p(\mathbf{z})\) is Gaussian distribution. To find the precision of this Gaussian, we consider the second-order terms in (3.86), which can be written as

\[
\begin{aligned}
& -\frac{1}{2} \mathbf{x}^{\mathrm{T}}\left(\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm{T}} \mathbf{L} \mathbf{A}\right) \mathbf{x}-\frac{1}{2} \mathbf{y}^{\mathrm{T}} \mathbf{L} \mathbf{y}+\frac{1}{2} \mathbf{y}^{\mathrm{T}} \mathbf{L} \mathbf{A} \mathbf{x}+\frac{1}{2} \mathbf{x}^{\mathrm{T}} \mathbf{A}^{\mathrm{T}} \mathbf{L} \mathbf{y} \\
& \quad=-\frac{1}{2}\binom{\mathbf{x}}{\mathbf{y}}^{\mathrm{T}}\left(\begin{array}{cc}
\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm{T}} \mathbf{L} \mathbf{A} & -\mathbf{A}^{\mathrm{T}} \mathbf{L} \\
-\mathbf{L} \mathbf{A} & \mathbf{L}
\end{array}\right)\binom{\mathbf{x}}{\mathbf{y}}=-\frac{1}{2} \mathbf{z}^{\mathrm{T}} \mathbf{R} \mathbf{z}
\end{aligned}
\]

and so the Gaussian distribution over \(\mathbf{z}\) has precision (inverse covariance) matrix
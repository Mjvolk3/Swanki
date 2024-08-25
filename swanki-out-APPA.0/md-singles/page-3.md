and that the determinant of a diagonal matrix is given by the product of the elements on the leading diagonal. Thus, for a \(2 \times 2\) matrix, the determinant takes the form

\[
|\mathbf{A}|=\left|\begin{array}{ll}
a_{11} & a_{12} \\
a_{21} & a_{22}
\end{array}\right|=a_{11} a_{22}-a_{12} a_{21}
\]

The determinant of a product of two matrices is given by

\[
|\mathbf{A B}|=|\mathbf{A} \| \mathbf{B}|
\]

as can be shown from (A.10). Also, the determinant of an inverse matrix is given by

\[
\left|\mathbf{A}^{-1}\right|=\frac{1}{|\mathbf{A}|}
\]

which can be shown by taking the determinant of (A.2) and applying (A.12).

If \(\mathbf{A}\) and \(\mathbf{B}\) are matrices of size \(N \times M\), then

\[
\left|\mathbf{I}_{N}+\mathbf{A} \mathbf{B}^{\mathrm{T}}\right|=\left|\mathbf{I}_{M}+\mathbf{A}^{\mathrm{T}} \mathbf{B}\right| .
\]

A useful special case is

\[
\left|\mathbf{I}_{N}+\mathbf{a b}^{\mathrm{T}}\right|=1+\mathbf{a}^{\mathrm{T}} \mathbf{b}
\]

where \(\mathbf{a}\) and \(\mathbf{b}\) are \(N\)-dimensional column vectors.

\title{
A.3. Matrix Derivatives
}

Sometimes we need to consider derivatives of vectors and matrices with respect to scalars. The derivative of a vector a with respect to a scalar \(x\) is a vector whose components are given by

\[
\left(\frac{\partial \mathbf{a}}{\partial x}\right)_{i}=\frac{\partial a_{i}}{\partial x}
\]

with an analogous definition for the derivative of a matrix. Derivatives with respect to vectors and matrices can also be defined, for instance

\[
\left(\frac{\partial x}{\partial \mathbf{a}}\right)_{i}=\frac{\partial x}{\partial a_{i}}
\]

and similarly

\[
\left(\frac{\partial \mathbf{a}}{\partial \mathbf{b}}\right)_{i j}=\frac{\partial a_{i}}{\partial b_{j}}
\]

The following is easily proven by writing out the components:

\[
\frac{\partial}{\partial \mathbf{x}}\left(\mathbf{x}^{\mathrm{T}} \mathbf{a}\right)=\frac{\partial}{\partial \mathbf{x}}\left(\mathbf{a}^{\mathrm{T}} \mathbf{x}\right)=\mathbf{a}
\]
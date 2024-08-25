\title{
A. LINEAR ALGEBRA
}

Similarly

$$
\frac{\partial}{\partial x}(\mathbf{A B})=\frac{\partial \mathbf{A}}{\partial x} \mathbf{B}+\mathbf{A} \frac{\partial \mathbf{B}}{\partial x}
$$

The derivative of the inverse of a matrix can be expressed as

$$
\frac{\partial}{\partial x}\left(\mathbf{A}^{-1}\right)=-\mathbf{A}^{-1} \frac{\partial \mathbf{A}}{\partial x} \mathbf{A}^{-1}
$$

as can be shown by differentiating the equation $\mathbf{A}^{-1} \mathbf{A}=\mathbf{I}$ using (A.20) and then right-multiplying by $\mathbf{A}^{-1}$. Also

$$
\frac{\partial}{\partial x} \ln |\mathbf{A}|=\operatorname{Tr}\left(\mathbf{A}^{-1} \frac{\partial \mathbf{A}}{\partial x}\right)
$$

which we shall prove later. If we choose $x$ to be one of the elements of $\mathbf{A}$, we have

$$
\frac{\partial}{\partial A_{i j}} \operatorname{Tr}(\mathbf{A B})=B_{j i}
$$

as can be seen by writing out the matrices using index notation. We can write this result more compactly in the form

$$
\frac{\partial}{\partial \mathbf{A}} \operatorname{Tr}(\mathbf{A B})=\mathbf{B}^{\mathrm{T}}
$$

With this notation, we have the following properties:

$$
\begin{aligned}
\frac{\partial}{\partial \mathbf{A}} \operatorname{Tr}\left(\mathbf{A}^{\mathrm{T}} \mathbf{B}\right) & =\mathbf{B} \\
\frac{\partial}{\partial \mathbf{A}} \operatorname{Tr}(\mathbf{A}) & =\mathbf{I} \\
\frac{\partial}{\partial \mathbf{A}} \operatorname{Tr}\left(\mathbf{A B} \mathbf{A}^{\mathrm{T}}\right) & =\mathbf{A}\left(\mathbf{B}+\mathbf{B}^{\mathrm{T}}\right)
\end{aligned}
$$

which can again be proven by writing out the matrix indices. We also have

$$
\frac{\partial}{\partial \mathbf{A}} \ln |\mathbf{A}|=\left(\mathbf{A}^{-1}\right)^{\mathrm{T}}
$$

which follows from (A.22) and (A.24).

\section*{A.4. Eigenvectors}

For a square matrix $\mathbf{A}$ of size $M \times M$, the eigenvector equation is defined by

$$
\mathbf{A} \mathbf{u}_{i}=\lambda_{i} \mathbf{u}_{i}
$$
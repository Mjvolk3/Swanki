which is easily proven by taking the transpose of (A.2) and applying (A.1).

A useful identity involving matrix inverses is the following:

$$
\left(\mathbf{P}^{-1}+\mathbf{B}^{\mathrm{T}} \mathbf{R}^{-1} \mathbf{B}\right)^{-1} \mathbf{B}^{\mathrm{T}} \mathbf{R}^{-1}=\mathbf{P B}^{\mathrm{T}}\left(\mathbf{B} \mathbf{P} \mathbf{B}^{\mathrm{T}}+\mathbf{R}\right)^{-1}
$$

which is easily verified by right-multiplying both sides by $\left(\mathbf{B P B}^{\mathrm{T}}+\mathbf{R}\right)$. Suppose that $\mathbf{P}$ has dimensionality $N \times N$ and that $\mathbf{R}$ has dimensionality $M \times M$, so that $\mathbf{B}$ is $M \times N$. Then if $M \ll N$, it will be much cheaper to evaluate the right-hand side of (A.5) than the left-hand side. A special case that sometimes arises is

$$
(\mathbf{I}+\mathbf{A B})^{-1} \mathbf{A}=\mathbf{A}(\mathbf{I}+\mathbf{B A})^{-1}
$$

Another useful identity involving inverses is the following:

$$
\left(\mathbf{A}+\mathbf{B D}^{-1} \mathbf{C}\right)^{-1}=\mathbf{A}^{-1}-\mathbf{A}^{-1} \mathbf{B}\left(\mathbf{D}+\mathbf{C A}^{-1} \mathbf{B}\right)^{-1} \mathbf{C A}^{-1}
$$

which is known as the Woodbury identity. It can be verified by multiplying both sides by $\left(\mathbf{A}+\mathbf{B D}^{-1} \mathbf{C}\right)$. This is useful, for instance, when $\mathbf{A}$ is large and diagonal and hence easy to invert, and when $\mathbf{B}$ has many rows but few columns (and conversely for $\mathbf{C}$ ), so that the right-hand side is much cheaper to evaluate than the left-hand side.

A set of vectors $\left\{\mathbf{a}_{1}, \ldots, \mathbf{a}_{N}\right\}$ is said to be linearly independent if the relation $\sum_{n} \alpha_{n} \mathbf{a}_{n}=0$ holds only if all $\alpha_{n}=0$. This implies that none of the vectors can be expressed as a linear combination of the remainder. The rank of a matrix is the maximum number of linearly independent rows (or equivalently the maximum number of linearly independent columns).

\title{
A.2. Traces and Determinants
}

Square matrices have traces and determinants. The trace $\operatorname{Tr}(\mathbf{A})$ of a matrix $\mathbf{A}$ is defined as the sum of the elements on the leading diagonal. By writing out the indices, we see that

$$
\operatorname{Tr}(\mathbf{A B})=\operatorname{Tr}(\mathbf{B A})
$$

By applying this formula multiple times to the product of three matrices, we see that

$$
\operatorname{Tr}(\mathbf{A B C})=\operatorname{Tr}(\mathbf{C A B})=\operatorname{Tr}(\mathbf{B C A})
$$

which is known as the cyclic property of the trace operator. It clearly extends to the product of any number of matrices. The determinant $|\mathbf{A}|$ of an $N \times N$ matrix $\mathbf{A}$ is defined by

$$
|\mathbf{A}|=\sum( \pm 1) A_{1 i_{1}} A_{2 i_{2}} \cdots A_{N i_{N}}
$$

in which the sum is taken over all products consisting of precisely one element from each row and one element from each column, with a coefficient +1 or -1 according to whether the permutation $i_{1} i_{2} \ldots i_{N}$ is even or odd, respectively. Note that $|\mathbf{I}|=1$,
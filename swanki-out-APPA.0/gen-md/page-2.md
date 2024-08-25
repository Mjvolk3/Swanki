### Card 1

A useful identity involving matrix inverses is the following:
$$
\left(\mathbf{P}^{-1}+\mathbf{B}^{\mathrm{T}} \mathbf{R}^{-1} \mathbf{B}\right)^{-1} \mathbf{B}^{\mathrm{T}} \mathbf{R}^{-1}=\mathbf{P B}^{\mathrm{T}}\left(\mathbf{B} \mathbf{P} \mathbf{B}^{\mathrm{T}}+\mathbf{R}\right)^{-1}
$$

Verify this identity by right-multiplying both sides by $\left(\mathbf{B P B}^{\mathrm{T}}+\mathbf{R}\right)$.

$$
\left(\mathbf{P}^{-1}+\mathbf{B}^{\mathrm{T}} \mathbf{R}^{-1} \mathbf{B}\right)^{-1} \mathbf{B}^{\mathrm{T}} \mathbf{R}^{-1} = \mathbf{P B}^{\mathrm{T}} \left(\mathbf{B P B}^{\mathrm{T}}+\mathbf{R}\right)^{-1}
$$

By right-multiplying both sides by $\left(\mathbf{B P B}^{\mathrm{T}}+\mathbf{R}\right)$, we obtain:
$$
\left( \left(\mathbf{P}^{-1}+\mathbf{B}^{\mathrm{T}} \mathbf{R}^{-1} \mathbf{B}\right)^{-1} \mathbf{B}^{\mathrm{T}} \mathbf{R}^{-1} \right) \left(\mathbf{B P B}^{\mathrm{T}}+\mathbf{R}\right) = \mathbf{P B}^{\mathrm{T}} \left(\mathbf{B P B}^{\mathrm{T}}+\mathbf{R} \right) \left(\mathbf{B P B}^{\mathrm{T}}+\mathbf{R}\right)^{-1}
$$

Simplifying both sides, we get:
$$
\mathbf{P B}^{\mathrm{T}} = \mathbf{P B}^{\mathrm{T}}
$$
This verifies the identity. 

- #linear-algebra, #matrix-theory

### Card 2

In the context of matrix determinants, what is the trace of a matrix $\mathbf{A}$ and how is it defined?

The trace $\operatorname{Tr}(\mathbf{A})$ of a matrix $\mathbf{A}$ is defined as the sum of the elements on the leading diagonal:
$$
\operatorname{Tr}(\mathbf{A}) = \sum_{i} A_{ii}
$$

- #linear-algebra, #matrix-theory

### Card 3

Using the cyclic property of the trace operator, show that $\operatorname{Tr}(\mathbf{A B C}) = \operatorname{Tr}(\mathbf{B C A})$.

The trace of the product of matrices $\mathbf{A}$, $\mathbf{B}$, and $\mathbf{C}$ has the following cyclic property:
$$
\operatorname{Tr}(\mathbf{A B C}) = \operatorname{Tr}(\mathbf{B C A}) = \operatorname{Tr}(\mathbf{C A B})
$$

This can be shown using the definition of the trace:
$$
\operatorname{Tr}(\mathbf{A B C}) = \sum_{i} (\mathbf{A B C})_{ii} = \sum_{i} \sum_{j} \sum_{k} A_{ij} B_{jk} C_{ki}
$$
By rearranging the summation indices, we see that:
$$
\operatorname{Tr}(\mathbf{A B C}) = \sum_{j} \sum_{k} \sum_{i} B_{jk} C_{ki} A_{ij} = \operatorname{Tr}(\mathbf{B C A})
$$

- #linear-algebra, #matrix-theory

### Card 4

What is the Woodbury identity for matrix inversion, and why is it useful?

The Woodbury identity for matrix inversion is given by:
$$
\left(\mathbf{A}+\mathbf{B D}^{-1} \mathbf{C}\right)^{-1}=\mathbf{A}^{-1}-\mathbf{A}^{-1} \mathbf{B}\left(\mathbf{D}+\mathbf{C A}^{-1} \mathbf{B}\right)^{-1} \mathbf{C A}^{-1}
$$

This is useful when $\mathbf{A}$ is large and diagonal (hence easy to invert) and $\mathbf{B}$ has many rows but few columns (and conversely for $\mathbf{C}$). It makes the inverse significantly cheaper to compute.

- #linear-algebra, #matrix-theory

### Card 5

Given the relation $\sum_{n} \alpha_{n} \mathbf{a}_{n}=0$, what is the condition for the set of vectors $\left\{\mathbf{a}_{1}, \ldots, \mathbf{a}_{N}\right\}$ to be linearly independent?

A set of vectors $\left\{\mathbf{a}_{1}, \ldots, \mathbf{a}_{N}\right\}$ is linearly independent if:
$$
\sum_{n} \alpha_{n} \mathbf{a}_{n}=0 \Rightarrow \alpha_{n}=0 \, \forall \, n
$$

This implies that none of the vectors can be expressed as a linear combination of the other vectors.

- #linear-algebra, #vector-theory

### Card 6

What is the determinant $|\mathbf{A}|$ of an $N \times N$ matrix $\mathbf{A}$, and what does it mean for the permutation $i_{1} i_{2} \ldots i_{N}$ to be even or odd?

The determinant $|\mathbf{A}|$ of an $N \times N$ matrix $\mathbf{A}$ is defined by:
$$
|\mathbf{A}| = \sum( \pm 1) A_{1 i_{1}} A_{2 i_{2}} \cdots A_{N i_{N}}
$$

The sum is taken over all products consisting of precisely one element from each row and one element from each column, with a coefficient +1 or -1 according to whether the permutation $i_{1} i_{2} \ldots i_{N}$ is even or odd, respectively.

An even permutation has an even number of inversions (where an inversion is a pair where a larger number precedes a smaller one). An odd permutation has an odd number of inversions.

- #linear-algebra, #matrix-theory
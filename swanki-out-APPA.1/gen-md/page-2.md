## Matrix inverse identity involving $ \mathbf{P}, \mathbf{B}, \mathbf{R}$

Describe the useful matrix identity involving $ \mathbf{P}, \mathbf{B}, \mathbf{R}$ and its verification process.

The identity is given by:

$$
\left(\mathbf{P}^{-1}+\mathbf{B}^{\mathrm{T}} \mathbf{R}^{-1} \mathbf{B}\right)^{-1} \mathbf{B}^{\mathrm{T}} \mathbf{R}^{-1}=\mathbf{P B}^{\mathrm{T}}\left(\mathbf{B} \mathbf{P} \mathbf{B}^{\mathrm{T}}+\mathbf{R}\right)^{-1}
$$

To verify, right-multiply both sides by $\left(\mathbf{B P B}^{\mathrm{T}}+\mathbf{R}\right)$.

- #linear-algebra, #matrix-identities

---

## The Woodbury identity

State and explain the Woodbury identity, including the context in which it is useful.

The Woodbury identity is given by:

$$
\left(\mathbf{A}+\mathbf{B D}^{-1} \mathbf{C}\right)^{-1}=\mathbf{A}^{-1}-\mathbf{A}^{-1} \mathbf{B}\left(\mathbf{D}+\mathbf{C A}^{-1} \mathbf{B}\right)^{-1} \mathbf{C A}^{-1}
$$

This identity is particularly useful when $\mathbf{A}$ is large and diagonal (and hence easy to invert), and when $\mathbf{B}$ has many rows but few columns (and conversely for $\mathbf{C}$).

- #linear-algebra, #matrix-identities.woodbury-identity

---

## Linear independence definition

Define linear independence for a set of vectors $\{ \mathbf{a}_{1}, \ldots, \mathbf{a}_{N} \}$.

A set of vectors $\{ \mathbf{a}_{1}, \ldots, \mathbf{a}_{N} \}$ is said to be linearly independent if the relation $\sum_{n} \alpha_{n} \mathbf{a}_{n}=0$ holds only if all $\alpha_{n}=0$. This implies that none of the vectors can be expressed as a linear combination of the remainder.

- #linear-algebra, #vector-spaces.linear-independence

---

## Matrix rank explanation

Explain the rank of a matrix.

The rank of a matrix is the maximum number of linearly independent rows (or equivalently the maximum number of linearly independent columns).

- #linear-algebra, #matrix-properties.rank

---

## Trace operator's cyclic property

Explain the cyclic property of the trace operator for matrices $\mathbf{A}, \mathbf{B}, \mathbf{C}$.

The cyclic property of the trace operator is given by:

$$
\operatorname{Tr}(\mathbf{A B C})=\operatorname{Tr}(\mathbf{C A B})=\operatorname{Tr}(\mathbf{B C A})
$$

This property extends to the product of any number of matrices.

- #linear-algebra, #matrix-properties.trace

---

## Determinant definition for an $N \times N$ matrix

Define the determinant $|\mathbf{A}|$ of an $N \times N$ matrix $\mathbf{A}$.

The determinant $|\mathbf{A}|$ is defined by:

$$
|\mathbf{A}|=\sum( \pm 1) A_{1 i_{1}} A_{2 i_{2}} \cdots A_{N i_{N}}
$$

where the sum is taken over all products consisting of precisely one element from each row and one element from each column, with a coefficient +1 or -1 according to whether the permutation $i_{1} i_{2} \ldots i_{N}$ is even or odd, respectively.

- #linear-algebra, #matrix-properties.determinant
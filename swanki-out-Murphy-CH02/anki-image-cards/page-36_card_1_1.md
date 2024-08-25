## What is the effect of an affine transformation on a unit square as shown in the image?

![](https://cdn.mathpix.com/cropped/2024_06_13_a723e795abd87511cc8bg-1.jpg?height=390&width=938&top_left_y=198&top_left_x=548)

%

The affine transformation is illustrated in two parts. On the left, the transformation only involves a translation where the original unit square is shifted to form a new square without scaling (represented as a blue square). On the right, the transformation includes scaling and possibly rotation, forming a parallelogram. This affine transformation can be expressed as $f(\boldsymbol{x}) = \mathbf{A} \boldsymbol{x} + \boldsymbol{b}$, where $f(\boldsymbol{x})$ is the transformed vector, $\mathbf{A}$ is the transformation matrix, and $\boldsymbol{b}$ is the translation vector. The area of the parallelogram is given by the determinant of the transformation matrix $\mathbf{A}$, specifically $ad - bc$.

- #mathematics, #linear-algebra.affine-transformation, #multivariate-distributions

## How is the area of the transformed shape determined in an affine transformation?

![](https://cdn.mathpix.com/cropped/2024_06_13_a723e795abd87511cc8bg-1.jpg?height=390&width=938&top_left_y=198&top_left_x=548)

%

The area of the transformed shape in an affine transformation is given by the determinant of the transformation matrix $\mathbf{A}$. For a 2x2 matrix $\mathbf{A}$, represented as:

$$
\mathbf{A} = 
\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}
$$

the area of the parallelogram formed by the affine transformation is determined by $| \det(\mathbf{A}) | = | ad - bc |$. This value represents the scaling factor of the area due to the transformation.

- #mathematics, #linear-algebra.determinant, #multivariate-distributions
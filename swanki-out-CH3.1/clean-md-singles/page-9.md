Figure 3.3 The red curve shows the elliptical surface of constant probability density for a Gaussian in a two-dimensional space $\mathrm{x}=$ $\left(x_{1}, x_{2}\right)$ on which the density is $\exp (-1 / 2)$ of its value at $\mathbf{x}=$ $\mu$. The axes of the ellipse are defined by the eigenvectors $\mathbf{u}_{i}$ of the covariance matrix, with corresponding eigenvalues $\lambda_{i}$.

![](https://cdn.mathpix.com/cropped/2024_05_13_1c6f5d15308081306a07g-1.jpg?height=564&width=787&top_left_y=216&top_left_x=857)

which case the distribution is singular and is confined to a subspace of lower dimensionality. If all the eigenvalues are non-negative, then the covariance matrix is said to be positive semidefinite.

Now consider the form of the Gaussian distribution in the new coordinate system defined by the $y_{i}$. In going from the $\mathbf{x}$ to the $\mathbf{y}$ coordinate system, we have a Jacobian matrix $\mathbf{J}$ with elements given by

$$
J_{i j}=\frac{\partial x_{i}}{\partial y_{j}}=U_{j i}
$$

where $U_{j i}$ are the elements of the matrix $\mathbf{U}^{\mathrm{T}}$. Using the orthonormality property of the matrix $\mathbf{U}$, we see that the square of the determinant of the Jacobian matrix is

$$
|\mathbf{J}|^{2}=\left|\mathbf{U}^{\mathrm{T}}\right|^{2}=\left|\mathbf{U}^{\mathrm{T}}\right||\mathbf{U}|=\left|\mathbf{U}^{\mathrm{T}} \mathbf{U}\right|=|\mathbf{I}|=1
$$

and, hence, $|\mathbf{J}|=1$. Also, the determinant $|\boldsymbol{\Sigma}|$ of the covariance matrix can be written as the product of its eigenvalues, and hence

$$
|\boldsymbol{\Sigma}|^{1 / 2}=\prod_{j=1}^{D} \lambda_{j}^{1 / 2}
$$

Thus, in the $y_{j}$ coordinate system, the Gaussian distribution takes the form

$$
p(\mathbf{y})=p(\mathbf{x})|\mathbf{J}|=\prod_{j=1}^{D} \frac{1}{\left(2 \pi \lambda_{j}\right)^{1 / 2}} \exp \left\{-\frac{y_{j}^{2}}{2 \lambda_{j}}\right\}
$$

which is the product of $D$ independent univariate Gaussian distributions. The eigenvectors therefore define a new set of shifted and rotated coordinates with respect to which the joint probability distribution factorizes into a product of independent distributions. The integral of the distribution in the $\mathbf{y}$ coordinate system is then

$$
\int p(\mathbf{y}) \mathrm{d} \mathbf{y}=\prod_{j=1}^{D} \int_{-\infty}^{\infty} \frac{1}{\left(2 \pi \lambda_{j}\right)^{1 / 2}} \exp \left\{-\frac{y_{j}^{2}}{2 \lambda_{j}}\right\} \mathrm{d} y_{j}=1
$$
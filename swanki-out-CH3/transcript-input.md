![](https://cdn.mathpix.com/cropped/2024_05_13_20a9d15d747590c3e3e1g-1.jpg?height=1248&width=1226&top_left_y=216&top_left_x=423

ChatGPT figure/image summary: The image displays a title "3 Standard Distributions" against an abstract background composed of multi-colored, soft-focus, light patterns. This is likely the chapter heading or section title from a textbook or publication that discusses statistical distributions, particularly focusing on standard or commonly used probability distributions within the field of statistics or data science. The formatting suggests it is part of a digital document, possibly an ebook or a PDF of a textbook.)

In this chapter we discuss some specific examples of probability distributions and their properties. As well as being of interest in their own right, these distributions can form building blocks for more complex models and will be used extensively throughout the book.

One role for the distributions discussed in this chapter is to model the probability distribution $p(\mathbf{x})$ of a random variable $\mathbf{x}$, given a finite set $\mathbf{x}_{1}, \ldots, \mathbf{x}_{N}$ of observations. This problem is known as density estimation. It should be emphasized that the problem of density estimation is fundamentally ill-posed, because there are infinitely many probability distributions that could have given rise to the observed finite data set. Indeed, any distribution $p(\mathbf{x})$ that is non-zero at each of the data points $\mathbf{x}_{1}, \ldots, \mathbf{x}_{N}$ is a potential candidate. The issue of choosing an appropriate distribution relates to the problem of model selection, which has already been encountered Section 1.2 in the context of polynomial curve fitting and which is a central issue in machine

\title{
3. STANDARD DISTRIBUTIONS
}

where we have used the result (2.51) for the normalization of the univariate Gaussian. This confirms that the multivariate Gaussian (3.26) is indeed normalized.

\subsection*{3.2.2 Moments}

We now look at the moments of the Gaussian distribution and thereby provide an interpretation of the parameters $\boldsymbol{\mu}$ and $\boldsymbol{\Sigma}$. The expectation of $\mathbf{x}$ under the Gaussian distribution is given by

$$
\begin{aligned}
\mathbb{E}[\mathbf{x}] & =\frac{1}{(2 \pi)^{D / 2}} \frac{1}{|\boldsymbol{\Sigma}|^{1 / 2}} \int \exp \left\{-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})\right\} \mathbf{x} \mathrm{d} \mathbf{x} \\
& =\frac{1}{(2 \pi)^{D / 2}} \frac{1}{|\boldsymbol{\Sigma}|^{1 / 2}} \int \exp \left\{-\frac{1}{2} \mathbf{z}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \mathbf{z}\right\}(\mathbf{z}+\boldsymbol{\mu}) \mathrm{d} \mathbf{z}
\end{aligned}
$$

where we have changed variables using $\mathbf{z}=\mathbf{x}-\boldsymbol{\mu}$. Note that the exponent is an even function of the components of $\mathbf{z}$, and because the integrals over these are taken over the range $(-\infty, \infty)$, the term in $\mathbf{z}$ in the factor $(\mathbf{z}+\boldsymbol{\mu})$ will vanish by symmetry. Thus,

$$
\mathbb{E}[\mathbf{x}]=\boldsymbol{\mu}
$$

and so we refer to $\boldsymbol{\mu}$ as the mean of the Gaussian distribution.

We now consider second-order moments of the Gaussian. In the univariate case, we considered the second-order moment given by $\mathbb{E}\left[x^{2}\right]$. For the multivariate Gaussian, there are $D^{2}$ second-order moments given by $\mathbb{E}\left[x_{i} x_{j}\right]$, which we can group together to form the matrix $\mathbb{E}\left[\mathbf{x x}^{\mathrm{T}}\right]$. This matrix can be written as

$$
\begin{aligned}
\mathbb{E}\left[\mathbf{x} \mathbf{x}^{\mathrm{T}}\right] & =\frac{1}{(2 \pi)^{D / 2}} \frac{1}{|\boldsymbol{\Sigma}|^{1 / 2}} \int \exp \left\{-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})\right\} \mathbf{x x}^{\mathrm{T}} \mathrm{d} \mathbf{x} \\
& =\frac{1}{(2 \pi)^{D / 2}} \frac{1}{|\boldsymbol{\Sigma}|^{1 / 2}} \int \exp \left\{-\frac{1}{2} \mathbf{z}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \mathbf{z}\right\}(\mathbf{z}+\boldsymbol{\mu})(\mathbf{z}+\boldsymbol{\mu})^{\mathrm{T}} \mathrm{d} \mathbf{z}
\end{aligned}
$$

where again we have changed variables using $\mathbf{z}=\mathrm{x}-\boldsymbol{\mu}$. Note that the cross-terms involving $\boldsymbol{\mu} \mathbf{z}^{\mathrm{T}}$ and $\boldsymbol{\mu}^{\mathrm{T}} \mathbf{z}$ will again vanish by symmetry. The term $\boldsymbol{\mu} \boldsymbol{\mu}^{\mathrm{T}}$ is constant and can be taken outside the integral, which itself is unity because the Gaussian distribution is normalized. Consider the term involving $\mathbf{z z}^{\mathrm{T}}$. Again, we can make use of the eigenvector expansion of the covariance matrix given by (3.28), together with the completeness of the set of eigenvectors, to write

$$
\mathbf{z}=\sum_{j=1}^{D} y_{j} \mathbf{u}_{j}
$$

where $y_{j}=\mathbf{u}_{j}^{\mathrm{T}} \mathbf{z}$, which gives

$$
\begin{aligned}
& \frac{1}{(2 \pi)^{D / 2}} \frac{1}{|\boldsymbol{\Sigma}|^{1 / 2}} \int \exp \left\{-\frac{1}{2} \mathbf{z}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \mathbf{z}\right\} \mathbf{z z}^{\mathrm{T}} \mathrm{d} \mathbf{z} \\
& =\frac{1}{(2 \pi)^{D / 2}} \frac{1}{|\boldsymbol{\Sigma}|^{1 / 2}} \sum_{i=1}^{D} \sum_{j=1}^{D} \mathbf{u}_{i} \mathbf{u}_{j}^{\mathrm{T}} \int \exp \left\{-\sum_{k=1}^{D} \frac{y_{k}^{2}}{2 \lambda_{k}}\right\} y_{i} y_{j} \mathrm{~d} \mathbf{y} \\
& =\sum_{i=1}^{D} \mathbf{u}_{i} \mathbf{u}_{i}^{\mathrm{T}} \lambda_{i}=\boldsymbol{\Sigma}
\end{aligned}
$$

where we have made use of the eigenvector equation (3.28), together with the fact that the integral on the middle line vanishes by symmetry unless $i=j$. In the final line we have made use of the results (2.53) and (3.38), together with (3.31). Thus, we have

$$
\mathbb{E}\left[\mathbf{x x}^{\mathrm{T}}\right]=\boldsymbol{\mu} \boldsymbol{\mu}^{\mathrm{T}}+\boldsymbol{\Sigma}
$$

When defining the variance for a single random variable, we subtracted the mean before taking the second moment. Similarly, in the multivariate case it is again convenient to subtract off the mean, giving rise to the covariance of a random vector $\mathrm{x}$ defined by

$$
\operatorname{cov}[\mathbf{x}]=\mathbb{E}\left[(\mathbf{x}-\mathbb{E}[\mathbf{x}])(\mathbf{x}-\mathbb{E}[\mathbf{x}])^{\mathrm{T}}\right]
$$

For the specific case of a Gaussian distribution, we can make use of $\mathbb{E}[\mathbf{x}]=\boldsymbol{\mu}$, together with the result (3.46), to give

$$
\operatorname{cov}[\mathbf{x}]=\mathbf{\Sigma}
$$

Because the parameter matrix $\boldsymbol{\Sigma}$ governs the covariance of $\mathbf{x}$ under the Gaussian distribution, it is called the covariance matrix.

\title{
3.2.3 Limitations
}

Although the Gaussian distribution (3.26) is often used as a simple density model, it suffers from some significant limitations. Consider the number of free parameters in the distribution. A general symmetric covariance matrix $\boldsymbol{\Sigma}$ will have $D(D+1) / 2$ independent parameters, and there are another $D$ independent parameters in $\boldsymbol{\mu}$, giving $D(D+3) / 2$ parameters in total. For large $D$, the total number of parameters therefore grows quadratically with $D$, and the computational task of manipulating and inverting the large matrices can become prohibitive. One way to address this problem is to use restricted forms of the covariance matrix. If we consider covariance matrices that are diagonal, so that $\boldsymbol{\Sigma}=\operatorname{diag}\left(\sigma_{i}^{2}\right)$, we then have a total of $2 D$ independent parameters in the density model. The corresponding contours of constant density are given by axis-aligned ellipsoids. We could further restrict the covariance matrix to be proportional to the identity matrix, $\boldsymbol{\Sigma}=\sigma^{2} \mathbf{I}$, known as an isotropic covariance, giving $D+1$ independent parameters in the model together with spherical surfaces of constant density. The three possibilities of general, diagonal, and isotropic covariance matrices are illustrated in Figure 3.4. Unfortunately,

Figure 3.4 Contours of constant probability density for a Gaussian distribution in two dimensions in which the covariance matrix is (a) of general form, (b) diagonal, in which case the elliptical contours are aligned with the coordinate axes, and (c) proportional to the identity matrix, in which case the contours are concentric circles.

![](https://cdn.mathpix.com/cropped/2024_05_13_21e07f2f44c90a145f10g-1.jpg?height=317&width=359&top_left_y=215&top_left_x=680

ChatGPT figure/image summary: The image shows a two-dimensional graph with coordinates \( x_1 \) and \( x_2 \). On this graph, there are concentric elliptical contours that represent levels of constant probability density for a 2D Gaussian distribution. The ellipses are centered around a point which is the mean of the distribution, and the orientation and shape of the ellipses correspond to the covariance structure of the distribution. This particular graph represents a Gaussian distribution with a general form of the covariance matrix, where the principal axes of the ellipses are not aligned with the coordinate axes. This indicates that there is some correlation between \( x_1 \) and \( x_2 \) in the distribution.)

(a)

![](https://cdn.mathpix.com/cropped/2024_05_13_21e07f2f44c90a145f10g-1.jpg?height=323&width=340&top_left_y=217&top_left_x=1012

ChatGPT figure/image summary: The image provided is likely to be the one referred to in the paper's context as part (c), which is described as showing the contours of constant probability density for a Gaussian distribution in two dimensions where the covariance matrix is proportional to the identity matrix. As a result, the contours are concentric circles. The description indicates that the Gaussian distribution in this case is isotropic, meaning that it is the same in all directions, and the probability density does not depend on the direction, only on the distance from the mean. 

In the image, you would see a series of concentric circles centered on a point that represents the mean (μ) of the distribution. The variance (σ^2) would be the same in every direction from this mean, which is why the contours form circles rather than ellipses. Each circle represents a contour where the probability density of the Gaussian distribution is constant. As you move outward from the center, each successive circle typically corresponds to a lower probability density.)

(b)

![](https://cdn.mathpix.com/cropped/2024_05_13_21e07f2f44c90a145f10g-1.jpg?height=315&width=303&top_left_y=214&top_left_x=1338

ChatGPT figure/image summary: The image depicts a graphical representation of a two-dimensional Gaussian distribution with isotropic covariance. This is visualized through the contours of constant probability density, which are shown as concentric circles centered around the mean of the distribution. An isotropic covariance matrix means that the variances in all directions are equal, resulting in these circular contours as opposed to elliptical ones that would be seen with an anisotropic (direction-dependent) covariance. The density is highest at the center and decreases as one moves away from the center, reflecting the characteristics of a Gaussian distribution. This matches the description for Figure 3.4(c) as mentioned in the provided contextual information.)

(c)
Section 3.2.9

Chapter 16 whereas such approaches limit the number of degrees of freedom in the distribution and make inversion of the covariance matrix a much faster operation, they also greatly restrict the form of the probability density and limit its ability to capture interesting correlations in the data.

A further limitation of the Gaussian distribution is that it is intrinsically unimodal (i.e., has a single maximum) and so is unable to provide a good approximation to multimodal distributions. Thus, the Gaussian distribution can be both too flexible, in the sense of having too many parameters, and too limited in the range of distributions that it can adequately represent. We will see later that the introduction of latent variables, also called hidden variables or unobserved variables, allows both of these problems to be addressed. In particular, a rich family of multimodal distributions is obtained by introducing discrete latent variables leading to mixtures of Gaussians. Similarly, the introduction of continuous latent variables leads to models in which the number of free parameters can be controlled independently of the dimensionality $D$ of the data space while still allowing the model to capture the dominant correlations in the data set.

\subsection*{3.2.4 Conditional distribution}

An important property of a multivariate Gaussian distribution is that if two sets of variables are jointly Gaussian, then the conditional distribution of one set conditioned on the other is again Gaussian. Similarly, the marginal distribution of either set is also Gaussian.

First, consider the case of conditional distributions. Suppose that $\mathbf{x}$ is a $D$ dimensional vector with Gaussian distribution $\mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}, \boldsymbol{\Sigma})$ and that we partition $\mathrm{x}$ into two disjoint subsets $\mathbf{x}_{a}$ and $\mathbf{x}_{b}$. Without loss of generality, we can take $\mathbf{x}_{a}$ to form the first $M$ components of $\mathbf{x}$, with $\mathbf{x}_{b}$ comprising the remaining $D-M$ components, so that

$$
\mathbf{x}=\binom{\mathbf{x}_{a}}{\mathbf{x}_{b}}
$$

We also define corresponding partitions of the mean vector $\boldsymbol{\mu}$ given by

$$
\boldsymbol{\mu}=\binom{\boldsymbol{\mu}_{a}}{\boldsymbol{\mu}_{b}}
$$

and of the covariance matrix $\Sigma$ given by

$$
\boldsymbol{\Sigma}=\left(\begin{array}{ll}
\boldsymbol{\Sigma}_{a a} & \boldsymbol{\Sigma}_{a b} \\
\boldsymbol{\Sigma}_{b a} & \boldsymbol{\Sigma}_{b b}
\end{array}\right)
$$

Note that the symmetry $\boldsymbol{\Sigma}^{\mathrm{T}}=\boldsymbol{\Sigma}$ of the covariance matrix implies that $\boldsymbol{\Sigma}_{a a}$ and $\boldsymbol{\Sigma}_{b b}$ are symmetric and that $\boldsymbol{\Sigma}_{b a}=\boldsymbol{\Sigma}_{a b}^{\mathrm{T}}$.

In many situations, it will be convenient to work with the inverse of the covariance matrix:

$$
\mathbf{\Lambda} \equiv \boldsymbol{\Sigma}^{-1}
$$

which is known as the precision matrix. In fact, we will see that some properties of Gaussian distributions are most naturally expressed in terms of the covariance, whereas others take a simpler form when viewed in terms of the precision. We therefore also introduce the partitioned form of the precision matrix:

$$
\boldsymbol{\Lambda}=\left(\begin{array}{ll}
\boldsymbol{\Lambda}_{a a} & \boldsymbol{\Lambda}_{a b} \\
\boldsymbol{\Lambda}_{b a} & \boldsymbol{\Lambda}_{b b}
\end{array}\right)
$$

corresponding to the partitioning (3.49) of the vector $\mathrm{x}$. Because the inverse of a symmetric matrix is also symmetric, we see that $\boldsymbol{\Lambda}_{a a}$ and $\boldsymbol{\Lambda}_{b b}$ are symmetric and that $\boldsymbol{\Lambda}_{b a}=\boldsymbol{\Lambda}_{a b}^{\mathrm{T}}$. It should be stressed at this point that, for instance, $\boldsymbol{\Lambda}_{a a}$ is not simply given by the inverse of $\boldsymbol{\Sigma}_{a a}$. In fact, we will shortly examine the relation between the inverse of a partitioned matrix and the inverses of its partitions.

We begin by finding an expression for the conditional distribution $p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right)$. From the product rule of probability, we see that this conditional distribution can be evaluated from the joint distribution $p(\mathbf{x})=p\left(\mathbf{x}_{a}, \mathbf{x}_{b}\right)$ simply by fixing $\mathbf{x}_{b}$ to the observed value and normalizing the resulting expression to obtain a valid probability distribution over $\mathbf{x}_{a}$. Instead of performing this normalization explicitly, we can obtain the solution more efficiently by considering the quadratic form in the exponent of the Gaussian distribution given by (3.27) and then reinstating the normalization coefficient at the end of the calculation. If we make use of the partitioning (3.49), (3.50), and (3.53), we obtain

$$
\begin{aligned}
& -\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})= \\
& \quad-\frac{1}{2}\left(\mathbf{x}_{a}-\boldsymbol{\mu}_{a}\right)^{\mathrm{T}} \boldsymbol{\Lambda}_{a a}\left(\mathbf{x}_{a}-\boldsymbol{\mu}_{a}\right)-\frac{1}{2}\left(\mathbf{x}_{a}-\boldsymbol{\mu}_{a}\right)^{\mathrm{T}} \boldsymbol{\Lambda}_{a b}\left(\mathbf{x}_{b}-\boldsymbol{\mu}_{b}\right) \\
& \quad-\frac{1}{2}\left(\mathbf{x}_{b}-\boldsymbol{\mu}_{b}\right)^{\mathrm{T}} \boldsymbol{\Lambda}_{b a}\left(\mathbf{x}_{a}-\boldsymbol{\mu}_{a}\right)-\frac{1}{2}\left(\mathbf{x}_{b}-\boldsymbol{\mu}_{b}\right)^{\mathrm{T}} \boldsymbol{\Lambda}_{b b}\left(\mathbf{x}_{b}-\boldsymbol{\mu}_{b}\right) .
\end{aligned}
$$

We see that as a function of $\mathbf{x}_{a}$, this is again a quadratic form, and hence, the corresponding conditional distribution $p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right)$ will be Gaussian. Because this distribution is completely characterized by its mean and its covariance, our goal will be to identify expressions for the mean and covariance of $p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right)$ by inspection of (3.54).

This is an example of a rather common operation associated with Gaussian distributions, sometimes called 'completing the square', in which we are given a

quadratic form defining the exponent terms in a Gaussian distribution and we need to determine the corresponding mean and covariance. Such problems can be solved straightforwardly by noting that the exponent in a general Gaussian distribution $\mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}, \boldsymbol{\Sigma})$ can be written as

$$
-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})=-\frac{1}{2} \mathbf{x}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \mathbf{x}+\mathbf{x}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}+\text { const }
$$

where 'const' denotes terms that are independent of $\mathbf{x}$, We have also made use of the symmetry of $\Sigma$. Thus, if we take our general quadratic form and express it in the form given by the right-hand side of (3.55), then we can immediately equate the matrix of coefficients entering the second-order term in $\mathrm{x}$ to the inverse covariance matrix $\boldsymbol{\Sigma}^{-1}$ and the coefficient of the linear term in $\mathrm{x}$ to $\boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}$, from which we can obtain $\boldsymbol{\mu}$.

Now let us apply this procedure to the conditional Gaussian distribution $p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right)$ for which the quadratic form in the exponent is given by (3.54). We will denote the mean and covariance of this distribution by $\boldsymbol{\mu}_{a \mid b}$ and $\boldsymbol{\Sigma}_{a \mid b}$, respectively. Consider the functional dependence of (3.54) on $\mathbf{x}_{a}$ in which $\mathbf{x}_{b}$ is regarded as a constant. If we pick out all terms that are second order in $\mathbf{x}_{a}$, we have

$$
-\frac{1}{2} \mathbf{x}_{a}^{\mathrm{T}} \boldsymbol{\Lambda}_{a a} \mathbf{x}_{a}
$$

from which we can immediately conclude that the covariance (inverse precision) of $p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right)$ is given by

$$
\boldsymbol{\Sigma}_{a \mid b}=\boldsymbol{\Lambda}_{a a}^{-1}
$$

Now consider all the terms in (3.54) that are linear in $\mathbf{x}_{a}$ :

$$
\mathbf{x}_{a}^{\mathrm{T}}\left\{\boldsymbol{\Lambda}_{a a} \boldsymbol{\mu}_{a}-\boldsymbol{\Lambda}_{a b}\left(\mathbf{x}_{b}-\boldsymbol{\mu}_{b}\right)\right\}
$$

where we have used $\boldsymbol{\Lambda}_{b a}^{\mathrm{T}}=\boldsymbol{\Lambda}_{a b}$. From our discussion of the general form (3.55), the coefficient of $\mathbf{x}_{a}$ in this expression must equal $\boldsymbol{\Sigma}_{a \mid b}^{-1} \boldsymbol{\mu}_{a \mid b}$ and, hence,

$$
\begin{aligned}
\boldsymbol{\mu}_{a \mid b} & =\boldsymbol{\Sigma}_{a \mid b}\left\{\boldsymbol{\Lambda}_{a a} \boldsymbol{\mu}_{a}-\boldsymbol{\Lambda}_{a b}\left(\mathbf{x}_{b}-\boldsymbol{\mu}_{b}\right)\right\} \\
& =\boldsymbol{\mu}_{a}-\boldsymbol{\Lambda}_{a a}^{-1} \boldsymbol{\Lambda}_{a b}\left(\mathbf{x}_{b}-\boldsymbol{\mu}_{b}\right)
\end{aligned}
$$

where we have made use of (3.57).

The results (3.57) and (3.59) are expressed in terms of the partitioned precision matrix of the original joint distribution $p\left(\mathbf{x}_{a}, \mathbf{x}_{b}\right)$. We can also express these results in terms of the corresponding partitioned covariance matrix. To do this, we make use of the following identity for the inverse of a partitioned matrix:

$$
\left(\begin{array}{ll}
\mathbf{A} & \mathbf{B} \\
\mathbf{C} & \mathbf{D}
\end{array}\right)^{-1}=\left(\begin{array}{cc}
\mathbf{M} & -\mathbf{M B D}^{-1} \\
-\mathbf{D}^{-1} \mathbf{C M} & \mathbf{D}^{-1}+\mathbf{D}^{-1} \mathbf{C M B D}^{-1}
\end{array}\right)
$$

where we have defined

$$
\mathbf{M}=\left(\mathbf{A}-\mathbf{B D}^{-1} \mathbf{C}\right)^{-1}
$$

The quantity $\mathbf{M}^{-1}$ is known as the Schur complement of the matrix on the left-hand side of (3.60) with respect to the submatrix D. Using the definition

$$
\left(\begin{array}{ll}
\boldsymbol{\Sigma}_{a a} & \boldsymbol{\Sigma}_{a b} \\
\boldsymbol{\Sigma}_{b a} & \boldsymbol{\Sigma}_{b b}
\end{array}\right)^{-1}=\left(\begin{array}{ll}
\boldsymbol{\Lambda}_{a a} & \boldsymbol{\Lambda}_{a b} \\
\boldsymbol{\Lambda}_{b a} & \boldsymbol{\Lambda}_{b b}
\end{array}\right)
$$

and making use of (3.60), we have

$$
\begin{aligned}
\boldsymbol{\Lambda}_{a a} & =\left(\boldsymbol{\Sigma}_{a a}-\boldsymbol{\Sigma}_{a b} \boldsymbol{\Sigma}_{b b}^{-1} \boldsymbol{\Sigma}_{b a}\right)^{-1} \\
\boldsymbol{\Lambda}_{a b} & =-\left(\boldsymbol{\Sigma}_{a a}-\boldsymbol{\Sigma}_{a b} \boldsymbol{\Sigma}_{b b}^{-1} \boldsymbol{\Sigma}_{b a}\right)^{-1} \boldsymbol{\Sigma}_{a b} \boldsymbol{\Sigma}_{b b}^{-1}
\end{aligned}
$$

From these we obtain the following expressions for the mean and covariance of the conditional distribution $p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right)$ :

$$
\begin{aligned}
\boldsymbol{\mu}_{a \mid b} & =\boldsymbol{\mu}_{a}+\boldsymbol{\Sigma}_{a b} \boldsymbol{\Sigma}_{b b}^{-1}\left(\mathbf{x}_{b}-\boldsymbol{\mu}_{b}\right) \\
\boldsymbol{\Sigma}_{a \mid b} & =\boldsymbol{\Sigma}_{a a}-\boldsymbol{\Sigma}_{a b} \boldsymbol{\Sigma}_{b b}^{-1} \boldsymbol{\Sigma}_{b a}
\end{aligned}
$$

Comparing (3.57) and (3.66), we see that the conditional distribution $p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right)$ takes a simpler form when expressed in terms of the partitioned precision matrix than when it is expressed in terms of the partitioned covariance matrix. Note that the mean of the conditional distribution $p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right)$, given by (3.65), is a linear function of $\mathbf{x}_{b}$ and that the covariance, given by (3.66), is independent of $\mathbf{x}_{b}$. This represents an example of a linear-Gaussian model.

\title{
3.2.5 Marginal distribution
}

We have seen that if a joint distribution $p\left(\mathbf{x}_{a}, \mathbf{x}_{b}\right)$ is Gaussian, then the conditional distribution $p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right)$ will again be Gaussian. Now we turn to a discussion of the marginal distribution given by

$$
p\left(\mathbf{x}_{a}\right)=\int p\left(\mathbf{x}_{a}, \mathbf{x}_{b}\right) \mathrm{d} \mathbf{x}_{b}
$$

which, as we will see, is also Gaussian. Once again, our strategy for calculating this distribution will be to focus on the quadratic form in the exponent of the joint distribution and thereby to identify the mean and covariance of the marginal distribution $p\left(\mathbf{x}_{a}\right)$.

The quadratic form for the joint distribution can be expressed, using the partitioned precision matrix, in the form (3.54). Our goal is to integrate out $\mathbf{x}_{b}$, which is most easily achieved by first considering the terms involving $\mathbf{x}_{b}$ and then completing the square to facilitate the integration. Picking out just those terms that involve $\mathbf{x}_{b}$, we have

$$
-\frac{1}{2} \mathbf{x}_{b}^{\mathrm{T}} \boldsymbol{\Lambda}_{b b} \mathbf{x}_{b}+\mathbf{x}_{b}^{T} \mathbf{m}=-\frac{1}{2}\left(\mathbf{x}_{b}-\boldsymbol{\Lambda}_{b b}^{-1} \mathbf{m}\right)^{\mathrm{T}} \boldsymbol{\Lambda}_{b b}\left(\mathbf{x}_{b}-\boldsymbol{\Lambda}_{b b}^{-1} \mathbf{m}\right)+\frac{1}{2} \mathbf{m}^{\mathrm{T}} \boldsymbol{\Lambda}_{b b}^{-1} \mathbf{m}
$$

where we have defined

$$
\mathbf{m}=\boldsymbol{\Lambda}_{b b} \boldsymbol{\mu}_{b}-\boldsymbol{\Lambda}_{b a}\left(\mathbf{x}_{a}-\boldsymbol{\mu}_{a}\right)
$$

We see that the dependence on $\mathbf{x}_{b}$ has been cast into the standard quadratic form of a Gaussian distribution corresponding to the first term on the right-hand side of (3.68) plus a term that does not depend on $\mathbf{x}_{b}$ (but that does depend on $\mathbf{x}_{a}$ ). Thus, when we take the exponential of this quadratic form, we see that the integration over $\mathbf{x}_{b}$ required by (3.67) will take the form

$$
\int \exp \left\{-\frac{1}{2}\left(\mathbf{x}_{b}-\boldsymbol{\Lambda}_{b b}^{-1} \mathbf{m}\right)^{\mathrm{T}} \boldsymbol{\Lambda}_{b b}\left(\mathbf{x}_{b}-\boldsymbol{\Lambda}_{b b}^{-1} \mathbf{m}\right)\right\} \mathrm{d} \mathbf{x}_{b}
$$

This integration is easily performed by noting that it is the integral over an unnormalized Gaussian, and so the result will be the reciprocal of the normalization coefficient. We know from the form of the normalized Gaussian given by (3.26) that this coefficient is independent of the mean and depends only on the determinant of the covariance matrix. Thus, by completing the square with respect to $\mathbf{x}_{b}$, we can integrate out $\mathbf{x}_{b}$ so that the only term remaining from the contributions on the left-hand side of (3.68) that depends on $\mathbf{x}_{a}$ is the last term on the right-hand side of (3.68) in which $\mathbf{m}$ is given by (3.69). Combining this term with the remaining terms from (3.54) that depend on $\mathbf{x}_{a}$, we obtain

$$
\begin{aligned}
& \frac{1}{2}\left[\boldsymbol{\Lambda}_{b b} \boldsymbol{\mu}_{b}-\boldsymbol{\Lambda}_{b a}\left(\mathbf{x}_{a}-\boldsymbol{\mu}_{a}\right)\right]^{\mathrm{T}} \boldsymbol{\Lambda}_{b b}^{-1}\left[\boldsymbol{\Lambda}_{b b} \boldsymbol{\mu}_{b}-\boldsymbol{\Lambda}_{b a}\left(\mathbf{x}_{a}-\boldsymbol{\mu}_{a}\right)\right] \\
&-\frac{1}{2} \mathbf{x}_{a}^{\mathrm{T}} \boldsymbol{\Lambda}_{a a} \mathbf{x}_{a}+\mathbf{x}_{a}^{\mathrm{T}}\left(\boldsymbol{\Lambda}_{a a} \boldsymbol{\mu}_{a}+\boldsymbol{\Lambda}_{a b} \boldsymbol{\mu}_{b}\right)+\text { const } \\
&=-\frac{1}{2} \mathbf{x}_{a}^{\mathrm{T}}\left(\boldsymbol{\Lambda}_{a a}-\boldsymbol{\Lambda}_{a b} \boldsymbol{\Lambda}_{b b}^{-1} \boldsymbol{\Lambda}_{b a}\right) \mathbf{x}_{a} \\
&+\mathbf{x}_{a}^{\mathrm{T}}\left(\boldsymbol{\Lambda}_{a a}-\boldsymbol{\Lambda}_{a b} \boldsymbol{\Lambda}_{b b}^{-1} \boldsymbol{\Lambda}_{b a}\right) \boldsymbol{\mu}_{a}+\text { const }
\end{aligned}
$$

where 'const' denotes quantities independent of $\mathbf{x}_{a}$. Again, by comparison with (3.55), we see that the covariance of the marginal distribution $p\left(\mathbf{x}_{a}\right)$ is given by

$$
\boldsymbol{\Sigma}_{a}=\left(\boldsymbol{\Lambda}_{a a}-\boldsymbol{\Lambda}_{a b} \boldsymbol{\Lambda}_{b b}^{-1} \boldsymbol{\Lambda}_{b a}\right)^{-1}
$$

Similarly, the mean is given by

$$
\boldsymbol{\Sigma}_{a}\left(\boldsymbol{\Lambda}_{a a}-\boldsymbol{\Lambda}_{a b} \boldsymbol{\Lambda}_{b b}^{-1} \boldsymbol{\Lambda}_{b a}\right) \boldsymbol{\mu}_{a}=\boldsymbol{\mu}_{a}
$$

where we have used (3.72). The covariance (3.72) is expressed in terms of the partitioned precision matrix given by (3.53). We can rewrite this in terms of the corresponding partitioning of the covariance matrix given by (3.51), as we did for the conditional distribution. These partitioned matrices are related by

$$
\left(\begin{array}{ll}
\boldsymbol{\Lambda}_{a a} & \boldsymbol{\Lambda}_{a b} \\
\boldsymbol{\Lambda}_{b a} & \boldsymbol{\Lambda}_{b b}
\end{array}\right)^{-1}=\left(\begin{array}{ll}
\boldsymbol{\Sigma}_{a a} & \boldsymbol{\Sigma}_{a b} \\
\boldsymbol{\Sigma}_{b a} & \boldsymbol{\Sigma}_{b b}
\end{array}\right)
$$

Making use of (3.60), we then have

$$
\left(\boldsymbol{\Lambda}_{a a}-\boldsymbol{\Lambda}_{a b} \boldsymbol{\Lambda}_{b b}^{-1} \boldsymbol{\Lambda}_{b a}\right)^{-1}=\boldsymbol{\Sigma}_{a a}
$$

Thus, we obtain the intuitively satisfying result that the marginal distribution $p\left(\mathbf{x}_{a}\right)$ has mean and covariance given by

$$
\begin{aligned}
\mathbb{E}\left[\mathbf{x}_{a}\right] & =\boldsymbol{\mu}_{a} \\
\operatorname{cov}\left[\mathbf{x}_{a}\right] & =\boldsymbol{\Sigma}_{a a}
\end{aligned}
$$

We see that for a marginal distribution, the mean and covariance are most simply expressed in terms of the partitioned covariance matrix, in contrast to the conditional distribution for which the partitioned precision matrix gives rise to simpler expressions.

Our results for the marginal and conditional distributions of a partitioned Gaussian can be summarized as follows. Given a joint Gaussian distribution $\mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}, \boldsymbol{\Sigma})$ with $\boldsymbol{\Lambda} \equiv \boldsymbol{\Sigma}^{-1}$ and the following partitions

$$
\begin{aligned}
\mathbf{x}=\binom{\mathbf{x}_{a}}{\mathbf{x}_{b}}, & \boldsymbol{\mu}=\binom{\boldsymbol{\mu}_{a}}{\boldsymbol{\mu}_{b}} \\
\boldsymbol{\Sigma}=\left(\begin{array}{ll}
\boldsymbol{\Sigma}_{a a} & \boldsymbol{\Sigma}_{a b} \\
\boldsymbol{\Sigma}_{b a} & \boldsymbol{\Sigma}_{b b}
\end{array}\right), & \boldsymbol{\Lambda}=\left(\begin{array}{ll}
\boldsymbol{\Lambda}_{a a} & \boldsymbol{\Lambda}_{a b} \\
\boldsymbol{\Lambda}_{b a} & \boldsymbol{\Lambda}_{b b}
\end{array}\right)
\end{aligned}
$$

then the conditional distribution is given by

$$
\begin{aligned}
p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right) & =\mathcal{N}\left(\mathbf{x} \mid \boldsymbol{\mu}_{a \mid b}, \boldsymbol{\Lambda}_{a a}^{-1}\right) \\
\boldsymbol{\mu}_{a \mid b} & =\boldsymbol{\mu}_{a}-\boldsymbol{\Lambda}_{a a}^{-1} \boldsymbol{\Lambda}_{a b}\left(\mathbf{x}_{b}-\boldsymbol{\mu}_{b}\right)
\end{aligned}
$$

and the marginal distribution is given by

$$
p\left(\mathbf{x}_{a}\right)=\mathcal{N}\left(\mathbf{x}_{a} \mid \boldsymbol{\mu}_{a}, \boldsymbol{\Sigma}_{a a}\right)
$$

We illustrate the idea of conditional and marginal distributions associated with a multivariate Gaussian using an example involving two variables in Figure 3.5.

\title{
3.2.6 Bayes' theorem
}

In Sections 3.2.4 and 3.2.5 we considered a Gaussian $p(\mathbf{x})$ in which we partitioned the vector $\mathbf{x}$ into two subvectors $\mathbf{x}=\left(\mathbf{x}_{a}, \mathbf{x}_{b}\right)$ and then found expressions for the conditional distribution $p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right)$ and the marginal distribution $p\left(\mathbf{x}_{a}\right)$. We noted that the mean of the conditional distribution $p\left(\mathbf{x}_{a} \mid \mathbf{x}_{b}\right)$ was a linear function of $\mathbf{x}_{b}$. Here we will suppose that we are given a Gaussian marginal distribution $p(\mathbf{x})$ and a Gaussian conditional distribution $p(\mathbf{y} \mid \mathbf{x})$ in which $p(\mathbf{y} \mid \mathbf{x})$ has a mean that is a linear function of $\mathbf{x}$ and a covariance that is independent of $\mathbf{x}$. This is an example of a linear-Gaussian model (Roweis and Ghahramani, 1999). We wish to find the marginal distribution $p(\mathbf{y})$ and the conditional distribution $p(\mathbf{x} \mid \mathbf{y})$. This is a structure that arises in several types of generative model and it will prove convenient to derive the general results here.

We will take the marginal and conditional distributions to be

$$
\begin{aligned}
p(\mathbf{x}) & =\mathcal{N}\left(\mathbf{x} \mid \boldsymbol{\mu}, \boldsymbol{\Lambda}^{-1}\right) \\
p(\mathbf{y} \mid \mathbf{x}) & =\mathcal{N}\left(\mathbf{y} \mid \mathbf{A} \mathbf{x}+\mathbf{b}, \mathbf{L}^{-1}\right)
\end{aligned}
$$

![](https://cdn.mathpix.com/cropped/2024_05_13_cf325eae3c87c1cb9850g-1.jpg?height=715&width=1341&top_left_y=209&top_left_x=248

ChatGPT figure/image summary: The images provided are graphical representations illustrating concepts from the paper related to multivariate Gaussian distributions and their marginal and conditional distributions. Here's a breakdown of what each image depicts:

- Image (a) shows contours of a bivariate (two-dimensional) Gaussian distribution for the variables \( x_a \) and \( x_b \). The contours represent points of equal probability density, and the distribution is centered where the contours are most closely spaced. The red line at \( x_b = 0.7 \) indicates a specific value of \( x_b \) for which the conditional distribution \( p(x_a | x_b = 0.7) \) is derived.

- Image (b) compares two probability distribution curves plotted against \( x_a \). The blue curve represents the marginal distribution \( p(x_a) \), showing the distribution of \( x_a \) without considering \( x_b \). The red curve represents the conditional distribution \( p(x_a | x_b = 0.7) \), which is the distribution of \( x_a \) given that \( x_b \) is fixed at a value of 0.7. The peak of the red curve is shifted relative to the blue curve, and its spread (variance) might be different, reflecting the conditional information imposed by \( x_b \).

The figures essentially visualize the concepts discussed in the paper, showcasing how the joint Gaussian distribution factors into marginal and conditional distributions based on the variables' covariances and means.)

![](https://cdn.mathpix.com/cropped/2024_05_13_cf325eae3c87c1cb9850g-1.jpg?height=640&width=630&top_left_y=217&top_left_x=252

ChatGPT figure/image summary: The image is a two-dimensional plot showing contours of a bivariate Gaussian distribution \( p(x_a, x_b) \) with respect to two variables \( x_a \) and \( x_b \). These contours represent regions of constant probability density. The horizontal axis is labeled \( x_a \) and ranges from 0 to 1, while the vertical axis is labeled \( x_b \) and also ranges from 0 to 1.

There is a red horizontal line on the plot at \( x_b = 0.7 \), indicating a specific value of \( x_b \) where the conditional distribution \( p(x_a | x_b) \) might be evaluated. The concentration of the contour lines towards the center indicates the area of highest probability density, and as one moves outward from the center, the probability density decreases, as suggested by the spacing of the contour lines. The labels on the axes, contour lines, and the red line are clearly laid out to illustrate this statistical concept.)

(a)

![](https://cdn.mathpix.com/cropped/2024_05_13_cf325eae3c87c1cb9850g-1.jpg?height=642&width=594&top_left_y=214&top_left_x=973

ChatGPT figure/image summary: Based on the provided context, the image shows two probability density functions (PDFs) plotted as curves. The blue curve represents the marginal distribution of a random variable \( x_a \), denoted as \( p(x_a) \). The red curve represents the conditional probability distribution \( p(x_a | x_b = 0.7) \), which means it is the distribution of random variable \( x_a \) given that another random variable \( x_b \) has a value of 0.7.

The curves are plotted against the values of \( x_a \) on the horizontal axis, while the vertical axis shows the probability densities. The area under each curve would integrate to 1 since these are probability distributions. The blue curve, representing the marginal distribution, appears to be broader and flatter, suggesting a larger variance compared to the red curve. The red curve, representing the conditional distribution, is narrower and has a peak that suggests a higher probability density for certain values of \( x_a \), indicating a smaller variance and more certainty about \( x_a \) when \( x_b \) is known to be 0.7. The specific mathematical forms of these distributions would depend on the parameters of the Gaussian distributions they are derived from, as detailed in the surrounding text.)

(b)

Figure 3.5 (a) Contours of a Gaussian distribution $p\left(x_{a}, x_{b}\right)$ over two variables. (b) The marginal distribution $p\left(x_{a}\right)$ (blue curve) and the conditional distribution $p\left(x_{a} \mid x_{b}\right)$ for $x_{b}=0.7$ (red curve).

where $\boldsymbol{\mu}, \mathbf{A}$, and $\mathbf{b}$ are parameters governing the means, and $\boldsymbol{\Lambda}$ and $\mathbf{L}$ are precision matrices. If $\mathbf{x}$ has dimensionality $M$ and $\mathbf{y}$ has dimensionality $D$, then the matrix $\mathbf{A}$ has size $D \times M$.

First we find an expression for the joint distribution over $\mathbf{x}$ and $\mathbf{y}$. To do this, we define

$$
\mathrm{z}=\binom{\mathrm{x}}{\mathrm{y}}
$$

and then consider the log of the joint distribution:

$$
\begin{aligned}
\ln p(\mathbf{z})= & \ln p(\mathbf{x})+\ln p(\mathbf{y} \mid \mathbf{x}) \\
= & -\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^{\mathrm{T}} \boldsymbol{\Lambda}(\mathbf{x}-\boldsymbol{\mu}) \\
& -\frac{1}{2}(\mathbf{y}-\mathbf{A} \mathbf{x}-\mathbf{b})^{\mathrm{T}} \mathbf{L}(\mathbf{y}-\mathbf{A} \mathbf{x}-\mathbf{b})+\text { const }
\end{aligned}
$$

where 'const' denotes terms independent of $\mathbf{x}$ and $\mathbf{y}$. As before, we see that this is a quadratic function of the components of $\mathbf{z}$, and hence, $p(\mathbf{z})$ is Gaussian distribution. To find the precision of this Gaussian, we consider the second-order terms in (3.86), which can be written as

$$
\begin{aligned}
& -\frac{1}{2} \mathbf{x}^{\mathrm{T}}\left(\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm{T}} \mathbf{L} \mathbf{A}\right) \mathbf{x}-\frac{1}{2} \mathbf{y}^{\mathrm{T}} \mathbf{L} \mathbf{y}+\frac{1}{2} \mathbf{y}^{\mathrm{T}} \mathbf{L} \mathbf{A} \mathbf{x}+\frac{1}{2} \mathbf{x}^{\mathrm{T}} \mathbf{A}^{\mathrm{T}} \mathbf{L} \mathbf{y} \\
& \quad=-\frac{1}{2}\binom{\mathbf{x}}{\mathbf{y}}^{\mathrm{T}}\left(\begin{array}{cc}
\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm{T}} \mathbf{L} \mathbf{A} & -\mathbf{A}^{\mathrm{T}} \mathbf{L} \\
-\mathbf{L} \mathbf{A} & \mathbf{L}
\end{array}\right)\binom{\mathbf{x}}{\mathbf{y}}=-\frac{1}{2} \mathbf{z}^{\mathrm{T}} \mathbf{R} \mathbf{z}
\end{aligned}
$$

and so the Gaussian distribution over $\mathbf{z}$ has precision (inverse covariance) matrix

given by

$$
\mathbf{R}=\left(\begin{array}{cc}
\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm{T}} \mathbf{L} \mathbf{A} & -\mathbf{A}^{\mathrm{T}} \mathbf{L} \\
-\mathbf{L} \mathbf{A} & \mathbf{L}
\end{array}\right)
$$

\section*{Exercise 3.23}

Exercise 3.24

Section 3.2

Section 3.2

The covariance matrix is found by taking the inverse of the precision, which can be done using the matrix inversion formula (3.60) to give

$$
\operatorname{cov}[\mathbf{z}]=\mathbf{R}^{-1}=\left(\begin{array}{cc}
\boldsymbol{\Lambda}^{-1} & \boldsymbol{\Lambda}^{-1} \mathbf{A}^{\mathrm{T}} \\
\mathbf{A} \boldsymbol{\Lambda}^{-1} & \mathbf{L}^{-1}+\mathbf{A} \boldsymbol{\Lambda}^{-1} \mathbf{A}^{\mathrm{T}}
\end{array}\right)
$$

Similarly, we can find the mean of the Gaussian distribution over z by identifying the linear terms in (3.86), which are given by

$$
\mathbf{x}^{\mathrm{T}} \boldsymbol{\Lambda} \boldsymbol{\mu}-\mathbf{x}^{\mathrm{T}} \mathbf{A}^{\mathrm{T}} \mathbf{L} \mathbf{b}+\mathbf{y}^{\mathrm{T}} \mathbf{L} \mathbf{b}=\binom{\mathbf{x}}{\mathbf{y}}^{\mathrm{T}}\binom{\boldsymbol{\Lambda} \boldsymbol{\mu}-\mathbf{A}^{\mathrm{T}} \mathbf{L} \mathbf{b}}{\mathbf{L} \mathbf{b}}
$$

Using our earlier result (3.55) obtained by completing the square over the quadratic form of a multivariate Gaussian, we find that the mean of $\mathbf{z}$ is given by

$$
\mathbb{E}[\mathbf{z}]=\mathbf{R}^{-1}\binom{\boldsymbol{\Lambda} \boldsymbol{\mu}-\mathbf{A}^{\mathrm{T}} \mathbf{L} \mathbf{b}}{\mathbf{L b}}
$$

Making use of (3.89), we then obtain

$$
\mathbb{E}[\mathbf{z}]=\binom{\boldsymbol{\mu}}{\mathbf{A} \boldsymbol{\mu}+\mathbf{b}}
$$

Next we find an expression for the marginal distribution $p(\mathbf{y})$ in which we have marginalized over $\mathbf{x}$. Recall that the marginal distribution over a subset of the components of a Gaussian random vector takes a particularly simple form when expressed in terms of the partitioned covariance matrix. Specifically, its mean and covariance are given by (3.76) and (3.77), respectively. Making use of (3.89) and (3.92), we see that the mean and covariance of the marginal distribution $p(\mathbf{y})$ are given by

$$
\begin{aligned}
\mathbb{E}[\mathbf{y}] & =\mathbf{A} \boldsymbol{\mu}+\mathbf{b} \\
\operatorname{cov}[\mathbf{y}] & =\mathbf{L}^{-1}+\mathbf{A} \mathbf{\Lambda}^{-1} \mathbf{A}^{\mathrm{T}}
\end{aligned}
$$

A special case of this result is when $\mathbf{A}=\mathbf{I}$, in which case the marginal distribution reduces to the convolution of two Gaussians, for which we see that the mean of the convolution is the sum of the means of the two Gaussians and the covariance of the convolution is the sum of their covariances.

Finally, we seek an expression for the conditional $p(\mathbf{x} \mid \mathbf{y})$. Recall that the results for the conditional distribution are most easily expressed in terms of the partitioned precision matrix, using (3.57) and (3.59). Applying these results to (3.89) and (3.92), we see that the conditional distribution $p(\mathbf{x} \mid \mathbf{y})$ has mean and covariance given by

$$
\begin{aligned}
\mathbb{E}[\mathbf{x} \mid \mathbf{y}] & =\left(\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm{T}} \mathbf{L} \mathbf{A}\right)^{-1}\left\{\mathbf{A}^{\mathrm{T}} \mathbf{L}(\mathbf{y}-\mathbf{b})+\boldsymbol{\Lambda} \boldsymbol{\mu}\right\} \\
\operatorname{cov}[\mathbf{x} \mid \mathbf{y}] & =\left(\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm{T}} \mathbf{L} \mathbf{A}\right)^{-1}
\end{aligned}
$$

learning.

We begin by considering distributions for discrete variables before exploring the Gaussian distribution for continuous variables. These are specific examples of parametric distributions, so called because they are governed by a relatively small number of adjustable parameters, such as the mean and variance of a Gaussian. To apply such models to the problem of density estimation, we need a procedure for determining suitable values for the parameters, given an observed data set, and our main focus will be on maximizing the likelihood function. In this chapter, we will assume that the data observations are independent and identically distributed (i.i.d.), whereas in future chapters we will explore more complex scenarios involving structured data where this assumption no longer holds.

One limitation of the parametric approach is that it assumes a specific functional form for the distribution, which may turn out to be inappropriate for a particular application. An alternative approach is given by nonparametric density estimation methods in which the form of the distribution typically depends on the size of the data set. Such models still contain parameters, but these control the model complexity rather than the form of the distribution. We end this chapter by briefly considering three nonparametric methods based respectively on histograms, nearest neighbours, and kernels. A major limitation of nonparametric techniques such as these is that they involve storing all the training data. In other words, the number of parameters grows with the size of the data set, so that the method become very inefficient for large data sets. Deep learning combines the efficiency of parametric models with the generality of nonparametric methods by considering flexible distributions based on neural networks having a large, but fixed, number of parameters.

\title{
3.1. Discrete Variables
}

We begin by considering simple distributions for discrete variables, starting with binary variables and then moving on to multi-state variables.

\subsection*{3.1.1 Bernoulli distribution}

Consider a single binary random variable $x \in\{0,1\}$. For example, $x$ might describe the outcome of flipping a coin, with $x=1$ representing 'heads' and $x=0$ representing 'tails'. If this were a damaged coin, such as the one shown in Figure 2.2, the probability of landing heads is not necessarily the same as that of landing tails. The probability of $x=1$ will be denoted by the parameter $\mu$ so that

$$
p(x=1 \mid \mu)=\mu
$$

where $0 \leqslant \mu \leqslant 1$, from which it follows that $p(x=0 \mid \mu)=1-\mu$. The probability distribution over $x$ can therefore be written in the form

$$
\operatorname{Bern}(x \mid \mu)=\mu^{x}(1-\mu)^{1-x}
$$

Exercise 3.1

which is known as the Bernoulli distribution. It is easily verified that this distribution

The evaluation of this conditional distribution can be seen as an example of Bayes' theorem, in which we interpret $p(\mathbf{x})$ as a prior distribution over $\mathbf{x}$. If the variable $\mathbf{y}$ is observed, then the conditional distribution $p(\mathbf{x} \mid \mathbf{y})$ represents the corresponding posterior distribution over $\mathrm{x}$. Having found the marginal and conditional distributions, we have effectively expressed the joint distribution $p(\mathbf{z})=p(\mathbf{x}) p(\mathbf{y} \mid \mathbf{x})$ in the form $p(\mathbf{x} \mid \mathbf{y}) p(\mathbf{y})$.

These results can be summarized as follows. Given a marginal Gaussian distribution for $\mathrm{x}$ and a conditional Gaussian distribution for $\mathrm{y}$ given $\mathrm{x}$ in the form

$$
\begin{aligned}
p(\mathbf{x}) & =\mathcal{N}\left(\mathbf{x} \mid \boldsymbol{\mu}, \boldsymbol{\Lambda}^{-1}\right) \\
p(\mathbf{y} \mid \mathbf{x}) & =\mathcal{N}\left(\mathbf{y} \mid \mathbf{A} \mathbf{x}+\mathbf{b}, \mathbf{L}^{-1}\right)
\end{aligned}
$$

then the marginal distribution of $\mathbf{y}$ and the conditional distribution of $\mathbf{x}$ given $\mathbf{y}$ are given by

$$
\begin{aligned}
p(\mathbf{y}) & =\mathcal{N}\left(\mathbf{y} \mid \mathbf{A} \boldsymbol{\mu}+\mathbf{b}, \mathbf{L}^{-1}+\mathbf{A} \boldsymbol{\Lambda}^{-1} \mathbf{A}^{\mathrm{T}}\right) \\
p(\mathbf{x} \mid \mathbf{y}) & =\mathcal{N}\left(\mathbf{x} \mid \boldsymbol{\Sigma}\left\{\mathbf{A}^{\mathrm{T}} \mathbf{L}(\mathbf{y}-\mathbf{b})+\boldsymbol{\Lambda} \boldsymbol{\mu}\right\}, \boldsymbol{\Sigma}\right)
\end{aligned}
$$

where

$$
\boldsymbol{\Sigma}=\left(\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm{T}} \mathbf{L} \mathbf{A}\right)^{-1}
$$

\title{
3.2.7 Maximum likelihood
}

Given a data set $\mathbf{X}=\left(\mathbf{x}_{1}, \ldots, \mathbf{x}_{N}\right)^{\mathrm{T}}$ in which the observations $\left\{\mathbf{x}_{n}\right\}$ are assumed to be drawn independently from a multivariate Gaussian distribution, we can estimate the parameters of the distribution by maximum likelihood. The log likelihood function is given by

$$
\ln p(\mathbf{X} \mid \boldsymbol{\mu}, \boldsymbol{\Sigma})=-\frac{N D}{2} \ln (2 \pi)-\frac{N}{2} \ln |\boldsymbol{\Sigma}|-\frac{1}{2} \sum_{n=1}^{N}\left(\mathbf{x}_{n}-\boldsymbol{\mu}\right)^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}\left(\mathbf{x}_{n}-\boldsymbol{\mu}\right)
$$

By simple rearrangement, we see that the likelihood function depends on the data set only through the two quantities

$$
\sum_{n=1}^{N} \mathbf{x}_{n}, \quad \sum_{n=1}^{N} \mathbf{x}_{n} \mathbf{x}_{n}^{\mathrm{T}}
$$

These are known as the sufficient statistics for the Gaussian distribution. Using (A.19), the derivative of the $\log$ likelihood with respect to $\boldsymbol{\mu}$ is given by

$$
\frac{\partial}{\partial \boldsymbol{\mu}} \ln p(\mathbf{X} \mid \boldsymbol{\mu}, \boldsymbol{\Sigma})=\sum_{n=1}^{N} \boldsymbol{\Sigma}^{-1}\left(\mathbf{x}_{n}-\boldsymbol{\mu}\right)
$$

and setting this derivative to zero, we obtain the solution for the maximum likelihood estimate of the mean:

$$
\boldsymbol{\mu}_{\mathrm{ML}}=\frac{1}{N} \sum_{n=1}^{N} \mathbf{x}_{n}
$$

which is the mean of the observed set of data points. The maximization of (3.102) with respect to $\Sigma$ is rather more involved. The simplest approach is to ignore the symmetry constraint and show that the resulting solution is symmetric as required. Alternative derivations of this result, which impose the symmetry and positive definiteness constraints explicitly, can be found in Magnus and Neudecker (1999). The result is as expected and takes the form

$$
\boldsymbol{\Sigma}_{\mathrm{ML}}=\frac{1}{N} \sum_{n=1}^{N}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{\mathrm{ML}}\right)\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{\mathrm{ML}}\right)^{\mathrm{T}}
$$

which involves $\boldsymbol{\mu}_{\mathrm{ML}}$ because this is the result of a joint maximization with respect to $\boldsymbol{\mu}$ and $\boldsymbol{\Sigma}$. Note that the solution (3.105) for $\boldsymbol{\mu}_{\mathrm{ML}}$ does not depend on $\boldsymbol{\Sigma}_{\mathrm{ML}}$, and so we can first evaluate $\boldsymbol{\mu}_{\mathrm{ML}}$ and then use this to evaluate $\boldsymbol{\Sigma}_{\mathrm{ML}}$.

If we evaluate the expectations of the maximum likelihood solutions under the true distribution, we obtain the following results

$$
\begin{aligned}
\mathbb{E}\left[\boldsymbol{\mu}_{\mathrm{ML}}\right] & =\boldsymbol{\mu} \\
\mathbb{E}\left[\boldsymbol{\Sigma}_{\mathrm{ML}}\right] & =\frac{N-1}{N} \boldsymbol{\Sigma}
\end{aligned}
$$

We see that the expectation of the maximum likelihood estimate for the mean is equal to the true mean. However, the maximum likelihood estimate for the covariance has an expectation that is less than the true value, and hence, it is biased. We can correct this bias by defining a different estimator $\widetilde{\Sigma}$ given by

$$
\widetilde{\boldsymbol{\Sigma}}=\frac{1}{N-1} \sum_{n=1}^{N}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{\mathrm{ML}}\right)\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{\mathrm{ML}}\right)^{\mathrm{T}}
$$

Clearly from (3.106) and (3.108), the expectation of $\tilde{\Sigma}$ is equal to $\boldsymbol{\Sigma}$.

\title{
3.2.8 Sequential estimation
}

Our discussion of the maximum likelihood solution represents a batch method in which the entire training data set is considered at once. An alternative is to use sequential methods, which allow data points to be processed one at a time and then discarded. These are important for online applications and for large data when the batch processing of all data points at once is infeasible.

Consider the result (3.105) for the maximum likelihood estimator of the mean $\boldsymbol{\mu}_{\mathrm{ML}}$, which we will denote by $\boldsymbol{\mu}_{\mathrm{ML}}^{(N)}$ when it is based on $N$ observations. If we

Figure 3.6 Plots of the Old Faithful data in which the red curves are contours of constant probability density. (a) A single Gaussian distribution which has been fitted to the data using maximum likelihood. Note that this distribution fails to capture the two clumps in the data and indeed places much of its probability mass in the central region between the clumps where the data are relatively sparse. (b) The distribution given by a linear combination of two Gaussians, also fitted by maximum likelihood, which gives a better representation of the data.

![](https://cdn.mathpix.com/cropped/2024_05_13_03b536ff7a8b51c2a0c5g-1.jpg?height=506&width=503&top_left_y=216&top_left_x=640

ChatGPT figure/image summary: The image displays a scatter plot overlaid with contour lines representing constant probability density. The data points in the scatter plot are shown as blue dots. The contour lines appear to represent the probability density of a single Gaussian distribution fitted to the data; however, this Gaussian model does not seem to capture the structure of the data effectively. The red contours indicate areas of high likelihood under the Gaussian model, and their elliptical shapes suggest the orientation and spread (covariance) of the inferred Gaussian distribution.

The axis labels are not clearly visible, but based on the context provided, the horizontal axis likely represents the duration of the Old Faithful geyser eruptions in minutes, and the vertical axis probably denotes the time in minutes to the next eruption.

This figure illustrates the limitations of using a single Gaussian distribution to model complex, multimodal distributions such as the one observed with the Old Faithful geyser data. The data exhibit two clumps, suggesting that a mixture of two Gaussians might be a better fit for capturing the underlying structure—a conclusion reached and illustrated in a different part of the paper, which is not shown here.)

(a)

![](https://cdn.mathpix.com/cropped/2024_05_13_03b536ff7a8b51c2a0c5g-1.jpg?height=506&width=508&top_left_y=216&top_left_x=1131

ChatGPT figure/image summary: The image appears to be a scatter plot along with overlaid contour lines. The scatter plot shows a collection of individual data points, highlighted as blue dots, and is likely representing some two-dimensional data. The contour lines, shown in shades of red and blue, indicate regions of constant probability density. There are two clearly distinct clusters of data points, with each cluster being encompassed by its own set of contour lines.

The contours suggest that a statistical model has been fitted to the data, particularly a mixture of two Gaussian distributions. This is based on the Gaussian probability density function's characteristically elliptical contours. Each cluster has its own set of concentric ellipses, with the density decreasing as the ellipses expand outward.

This kind of visual representation is commonly used in statistical data analysis to demonstrate how well a certain model, in this case a mixture of Gaussians, fits the observed data. The model appears to capture the two main clusters in the data effectively, with the contour lines representing areas of higher probability density within each cluster.)

(b)

dissect out the contribution from the final data point $\mathbf{x}_{N}$, we obtain

$$
\begin{aligned}
\boldsymbol{\mu}_{\mathrm{ML}}^{(N)} & =\frac{1}{N} \sum_{n=1}^{N} \mathbf{x}_{n} \\
& =\frac{1}{N} \mathbf{x}_{N}+\frac{1}{N} \sum_{n=1}^{N-1} \mathbf{x}_{n} \\
& =\frac{1}{N} \mathbf{x}_{N}+\frac{N-1}{N} \boldsymbol{\mu}_{\mathrm{ML}}^{(N-1)} \\
& =\boldsymbol{\mu}_{\mathrm{ML}}^{(N-1)}+\frac{1}{N}\left(\mathbf{x}_{N}-\boldsymbol{\mu}_{\mathrm{ML}}^{(N-1)}\right)
\end{aligned}
$$

This result has a nice interpretation, as follows. After observing $N-1$ data points, we estimate $\boldsymbol{\mu}$ by $\boldsymbol{\mu}_{\mathrm{ML}}^{(N-1)}$. We now observe data point $\mathbf{x}_{N}$, and we obtain our revised estimate $\boldsymbol{\mu}_{\mathrm{ML}}^{(N)}$ by moving the old estimate a small amount, proportional to $1 / N$, in the direction of the 'error signal' $\left(\mathbf{x}_{N}-\boldsymbol{\mu}_{\mathrm{ML}}^{(N-1)}\right)$. Note that, as $N$ increases, so the contributions from successive data points get smaller.

\title{
3.2.9 Mixtures of Gaussians
}

Although the Gaussian distribution has some important analytical properties, it suffers from significant limitations when used to model modelling real data sets. Consider the example shown in Figure 3.6(a). This is known as the 'Old Faithful' data set, and comprises 272 measurements of the eruption of the Old Faithful geyser in Yellowstone National Park in the USA. Each measurement gives the duration of the eruption in minutes (horizontal axis) and the time in minutes to the next eruption (vertical axis). We see that the data set forms two dominant clumps, and that a simple Gaussian distribution is unable to capture this structure.

We might expect that a superposition of two Gaussian distributions would be able to do a much better job of representing the structure in this data set, and indeed

Figure 3.7 Example of a Gaussian mixture distribution in one dimension showing three Gaussians (each scaled by a coefficient) in blue and their sum in red.

![](https://cdn.mathpix.com/cropped/2024_05_13_7914fb982b6a4f2206b4g-1.jpg?height=416&width=606&top_left_y=217&top_left_x=1055

ChatGPT figure/image summary: This image displays a Gaussian mixture distribution in one dimension. There are three individual Gaussian distributions shown in blue, each characterized by their own mean and spread. The red curve represents the overall mixture distribution which is the sum of the blue Gaussian distributions. The horizontal axis, labeled 't', can be interpreted as the variable for which the distribution is defined, while the vertical axis, labeled 'p(t|x)', represents the probability density. Each blue curve depicts one component of the mixture model with its respective peak and width, while the overall red curve reflects the combined effect of the three components, resulting in a more complex probability density function that captures the contribution from each individual component in the mixture.)

this proves to be the case, as can be seen from Figure 3.6(b). Such superpositions, formed by taking linear combinations of more basic distributions such as Gaussians, can be formulated as probabilistic models known as mixture distributions. In this section we will consider Gaussians to illustrate the framework of mixture models. More generally, mixture models can comprise linear combinations of other distributions, for example mixtures of Bernoulli distributions for binary variables. In Figure 3.7 we see that a linear combination of Gaussians can give rise to very complex densities. By using a sufficient number of Gaussians and by adjusting their means and covariances as well as the coefficients in the linear combination, almost any continuous distribution can be approximated to arbitrary accuracy.

We therefore consider a superposition of $K$ Gaussian densities of the form

$$
p(\mathbf{x})=\sum_{k=1}^{K} \pi_{k} \mathcal{N}\left(\mathbf{x} \mid \boldsymbol{\mu}_{k}, \boldsymbol{\Sigma}_{k}\right)
$$

which is called a mixture of Gaussians. Each Gaussian density $\mathcal{N}\left(\mathbf{x} \mid \boldsymbol{\mu}_{k}, \boldsymbol{\Sigma}_{k}\right)$ is called a component of the mixture and has its own mean $\boldsymbol{\mu}_{k}$ and covariance $\boldsymbol{\Sigma}_{k}$. Contour and surface plots for a Gaussian mixture in two dimensions having three components are shown in Figure 3.8.

The parameters $\pi_{k}$ in (3.111) are called mixing coefficients. If we integrate both sides of (3.111) with respect to $\mathbf{x}$, and note that both $p(\mathbf{x})$ and the individual Gaussian components are normalized, we obtain

$$
\sum_{k=1}^{K} \pi_{k}=1
$$

Also, given that $\mathcal{N}\left(\mathbf{x} \mid \boldsymbol{\mu}_{k}, \boldsymbol{\Sigma}_{k}\right) \geqslant 0$, a sufficient condition for the requirement $p(\mathbf{x}) \geqslant$ 0 is that $\pi_{k} \geqslant 0$ for all $k$. Combining this with the condition (3.112), we obtain

$$
0 \leqslant \pi_{k} \leqslant 1
$$

We can therefore see that the mixing coefficients satisfy the requirements to be probabilities, and we will show that this probabilistic interpretation of mixture distributions is very powerful.

![](https://cdn.mathpix.com/cropped/2024_05_13_bbb54caf8784589780acg-1.jpg?height=510&width=518&top_left_y=214&top_left_x=110

ChatGPT figure/image summary: The image shows a two-dimensional plane with contour plots representing three different Gaussian distributions, overlaid on top of each other. Each set of concentric rings represents the contours of constant density for one Gaussian component. The contours are colored differently for each Gaussian component: one in red, another in blue, and the third in green. The mixing coefficients, which are the probabilities associated with each Gaussian component, are indicated on the image with the symbols "π1 = 0.5", "π2 = 0.3", and "π3 = 0.2" next to the corresponding contour plots. The location of the highest density for each Gaussian is marked with a small circle (•) at the center of the concentric rings, where the contours are closest together. This visualization helps to illustrate the concept of a Gaussian mixture model where multiple Gaussian probability distributions are combined to form a more complex distribution.)

(a)

![](https://cdn.mathpix.com/cropped/2024_05_13_bbb54caf8784589780acg-1.jpg?height=452&width=510&top_left_y=214&top_left_x=624

ChatGPT figure/image summary: This image shows a two-dimensional space with contours plotted to represent a probability density function, \( p(\mathbf{x}) \). The contours are in a shape that suggests that the density function is composed of multiple modes or peaks, which are likely formed by the mixture of several Gaussian distributions. The highest density areas, representing the higher probability regions, are where the contour lines are closest together. This pattern exemplifies how a Gaussian mixture distribution can lead to complex, multi-modal density patterns in a two-dimensional space.)

$x_{1}$

(b)

![](https://cdn.mathpix.com/cropped/2024_05_13_bbb54caf8784589780acg-1.jpg?height=427&width=435&top_left_y=292&top_left_x=1148

ChatGPT figure/image summary: The image provided is a three-dimensional surface plot of a mixture distribution consisting of three Gaussian components. The axes are likely representing two different variables, perhaps \( x_1 \) and \( x_2 \) as part of the two-dimensional space being considered. The surface plot is showing various peaks where each peak corresponds to one of the Gaussians in the mixture. The height of the plot at any point represents the value of the probability density function of the mixture distribution at that point, with the peaks indicating regions of higher probability.)

(c)

Figure 3.8 Illustration of a mixture of three Gaussians in a two-dimensional space. (a) Contours of constant density for each of the mixture components, in which the three components are denoted red, blue, and green, and the values of the mixing coefficients are shown below each component. (b) Contours of the marginal probability density $p(\mathbf{x})$ of the mixture distribution. (c) A surface plot of the distribution $p(\mathbf{x})$.

From the sum and product rules of probability, the marginal density can be written as

$$
p(\mathbf{x})=\sum_{k=1}^{K} p(k) p(\mathbf{x} \mid k)
$$

which is equivalent to (3.111) in which we can view $\pi_{k}=p(k)$ as the prior probability of picking the $k$ th component, and the density $\mathcal{N}\left(\mathbf{x} \mid \boldsymbol{\mu}_{k}, \boldsymbol{\Sigma}_{k}\right)=p(\mathbf{x} \mid k)$ as the probability of $\mathrm{x}$ conditioned on $k$. As we will see in later chapters, an important role is played by the corresponding posterior probabilities $p(k \mid \mathbf{x})$, which are also known as responsibilities. From Bayes' theorem, these are given by

$$
\begin{aligned}
\gamma_{k}(\mathbf{x}) & \equiv p(k \mid \mathbf{x}) \\
& =\frac{p(k) p(\mathbf{x} \mid k)}{\sum_{l} p(l) p(\mathbf{x} \mid l)} \\
& =\frac{\pi_{k} \mathcal{N}\left(\mathbf{x} \mid \boldsymbol{\mu}_{k}, \boldsymbol{\Sigma}_{k}\right)}{\sum_{l} \pi_{l} \mathcal{N}\left(\mathbf{x} \mid \boldsymbol{\mu}_{l}, \boldsymbol{\Sigma}_{l}\right)}
\end{aligned}
$$

The form of the Gaussian mixture distribution is governed by the parameters $\pi$, $\boldsymbol{\mu}$, and $\boldsymbol{\Sigma}$, where we have used the notation $\boldsymbol{\pi} \equiv\left\{\pi_{1}, \ldots, \pi_{K}\right\}, \boldsymbol{\mu} \equiv\left\{\boldsymbol{\mu}_{1}, \ldots, \boldsymbol{\mu}_{K}\right\}$, and $\boldsymbol{\Sigma} \equiv\left\{\boldsymbol{\Sigma}_{1}, \ldots \boldsymbol{\Sigma}_{K}\right\}$. One way to set the values of these parameters is to use maximum likelihood. From (3.111), the log of the likelihood function is given by

$$
\ln p(\mathbf{X} \mid \boldsymbol{\pi}, \boldsymbol{\mu}, \boldsymbol{\Sigma})=\sum_{n=1}^{N} \ln \left\{\sum_{k=1}^{K} \pi_{k} \mathcal{N}\left(\mathbf{x}_{n} \mid \boldsymbol{\mu}_{k}, \boldsymbol{\Sigma}_{k}\right)\right\}
$$

where $\mathbf{X}=\left\{\mathbf{x}_{1}, \ldots, \mathbf{x}_{N}\right\}$. We immediately see that the situation is now much more complex than with a single Gaussian, due to the summation over $k$ inside the log-

arithm. As a result, the maximum likelihood solution for the parameters no longer has a closed-form analytical solution. One approach for maximizing the likelihood function is to use iterative numerical optimization techniques. Alternatively, we can employ a powerful framework called expectation maximization, which has wide applicability to a variety of different deep generative models.

\title{
3.3. Periodic Variables
}

Although Gaussian distributions are of great practical significance, both in their own right and as building blocks for more complex probabilistic models, there are situations in which they are inappropriate as density models for continuous variables. One important case, which arises in practical applications, is that of periodic variables.

An example of a periodic variable is the wind direction at a particular geographical location. We might, for instance, measure the wind direction at multiple locations and wish to summarize this data using a parametric distribution. Another example is calendar time, where we may be interested in modelling quantities that are believed to be periodic over 24 hours or over an annual cycle. Such quantities can conveniently be represented using an angular (polar) coordinate $0 \leqslant \theta<2 \pi$.

We might be tempted to treat periodic variables by choosing some direction as the origin and then applying a conventional distribution such as the Gaussian. Such an approach, however, would give results that were strongly dependent on the arbitrary choice of origin. Suppose, for instance, that we have two observations at $\theta_{1}=1^{\circ}$ and $\theta_{2}=359^{\circ}$, and we model them using a standard univariate Gaussian distribution. If we place the origin at $0^{\circ}$, then the sample mean of this data set will be $180^{\circ}$ with standard deviation $179^{\circ}$, whereas if we place the origin at $180^{\circ}$, then the mean will be $0^{\circ}$ and the standard deviation will be $1^{\circ}$. We clearly need to develop a special approach for periodic variables.

\subsection*{3.3.1 Von Mises distribution}

Let us consider the problem of evaluating the mean of a set of observations $\mathcal{D}=\left\{\theta_{1}, \ldots, \theta_{N}\right\}$ of a periodic variable $\theta$ where $\theta$ is measured in radians. We have already seen that the simple average $\left(\theta_{1}+\cdots+\theta_{N}\right) / N$ will be strongly coordinate dependent. To find an invariant measure of the mean, note that the observations can be viewed as points on the unit circle and can therefore be described instead by two-dimensional unit vectors $\mathbf{x}_{1}, \ldots, \mathbf{x}_{N}$ where $\left\|\mathbf{x}_{n}\right\|=1$ for $n=1, \ldots, N$, as illustrated in Figure 3.9. We can average the vectors $\left\{\mathbf{x}_{n}\right\}$ instead to give

$$
\overline{\mathbf{x}}=\frac{1}{N} \sum_{n=1}^{N} \mathbf{x}_{n}
$$

and then find the corresponding angle $\bar{\theta}$ of this average. Clearly, this definition will ensure that the location of the mean is independent of the origin of the angular coordinate. Note that $\overline{\mathbf{x}}$ will typically lie inside the unit circle. The Cartesian coordinates

Figure 3.9 Illustration of the representation of values $\theta_{n}$ of a periodic variable as twodimensional vectors $\mathbf{x}_{n}$ living on the unit circle. Also shown is the average $\bar{x}$ of those vectors.

![](https://cdn.mathpix.com/cropped/2024_05_13_b304b92298c168b494aag-1.jpg?height=623&width=648&top_left_y=216&top_left_x=995

ChatGPT figure/image summary: The image illustrates a unit circle with a few points represented on its circumference, symbolizing values of a periodic variable as two-dimensional vectors. These vectors are marked as \( x_1, x_2, x_3, \) and \( x_4 \) and are positioned at various angles around the circle. The average of these vectors is represented by a vector \( \bar{x} \) inside the circle, pointing towards the circumference but not reaching it, indicating that the average vector \( \bar{x} \) generally lies within the unit circle. This depiction aligns with the text, which describes a process for calculating the mean of observations of a periodic variable that avoids the problems associated with coordinate dependence, which arise when using standard linear averages for circular data. This is important when dealing with angles or time of day to ensure that the measure of central tendency is meaningful and consistent irrespective of where the angular origin is placed.)

of the observations are given by $\mathbf{x}_{n}=\left(\cos \theta_{n}, \sin \theta_{n}\right)$, and we can write the Cartesian coordinates of the sample mean in the form $\overline{\mathbf{x}}=(\bar{r} \cos \bar{\theta}, \bar{r} \sin \bar{\theta})$. Substituting into (3.117) and equating the $x_{1}$ and $x_{2}$ components then gives

$$
\bar{x}_{1}=\bar{r} \cos \bar{\theta}=\frac{1}{N} \sum_{n=1}^{N} \cos \theta_{n}, \quad \bar{x}_{2}=\bar{r} \sin \bar{\theta}=\frac{1}{N} \sum_{n=1}^{N} \sin \theta_{n}
$$

Taking the ratio, and using the identity $\tan \theta=\sin \theta / \cos \theta$, we can solve for $\bar{\theta}$ to give

$$
\bar{\theta}=\tan ^{-1}\left\{\frac{\sum_{n} \sin \theta_{n}}{\sum_{n} \cos \theta_{n}}\right\}
$$

Shortly, we will see how this result arises naturally as a maximum likelihood estimator.

First, we need to define a periodic generalization of the Gaussian called the von Mises distribution. Here we will limit our attention to univariate distributions, although analogous periodic distributions can also be found over hyperspheres of arbitrary dimension (Mardia and Jupp, 2000).

By convention, we will consider distributions $p(\theta)$ that have period $2 \pi$. Any probability density $p(\theta)$ defined over $\theta$ must not only be non-negative and integrate to one, but it must also be periodic. Thus, $p(\theta)$ must satisfy the three conditions:

$$
\begin{aligned}
p(\theta) & \geqslant 0 \\
\int_{0}^{2 \pi} p(\theta) \mathrm{d} \theta & =1 \\
p(\theta+2 \pi) & =p(\theta)
\end{aligned}
$$

From (3.122), it follows that $p(\theta+M 2 \pi)=p(\theta)$ for any integer $M$.

We can easily obtain a Gaussian-like distribution that satisfies these three properties as follows. Consider a Gaussian distribution over two variables $\mathbf{x}=\left(x_{1}, x_{2}\right)$

Figure 3.10 The von Mises distribution can be derived by considering a two-dimensional Gaussian of the form (3.123), whose density contours are shown in blue, and conditioning on the unit circle shown in red.

![](https://cdn.mathpix.com/cropped/2024_05_13_a727111505627aa0270dg-1.jpg?height=386&width=422&top_left_y=217&top_left_x=1225

ChatGPT figure/image summary: The image provided is an illustration that accompanies a mathematical discussion on the von Mises distribution in the context of periodic variables and their representations on a circle. This figure is intended to demonstrate how a two-dimensional Gaussian distribution can be converted into a periodic distribution by taking the value of the distribution along a circle of fixed radius (in this case, the unit circle).

In the image, you can see:
- A Cartesian coordinate system with axes \( x_1 \) and \( x_2 \).
- A red circle with radius \( r = 1 \), representing the unit circle upon which the periodic variable lies.
- Blue concentric level curves, which are the density contours of a two-dimensional Gaussian distribution centered at some point in the plane. These contours are equidistant from each other, indicating a constant increase in the value of the probability density function \( p(\mathbf{x}) \) from the outermost to the innermost curve.

This visual is meant to show the relationship between a standard Gaussian distribution over Cartesian coordinates and its adaptation to a circular or periodic domain, leading to the von Mises distribution when conditioned on the unit circle.)

having mean $\boldsymbol{\mu}=\left(\mu_{1}, \mu_{2}\right)$ and a covariance matrix $\boldsymbol{\Sigma}=\sigma^{2} \mathbf{I}$ where $\mathbf{I}$ is the $2 \times 2$ identity matrix, so that

$$
p\left(x_{1}, x_{2}\right)=\frac{1}{2 \pi \sigma^{2}} \exp \left\{-\frac{\left(x_{1}-\mu_{1}\right)^{2}+\left(x_{2}-\mu_{2}\right)^{2}}{2 \sigma^{2}}\right\}
$$

The contours of constant $p(\mathbf{x})$ are circles, as illustrated in Figure 3.10.

Now suppose we consider the value of this distribution along a circle of fixed radius. Then by construction, this distribution will be periodic, although it will not be normalized. We can determine the form of this distribution by transforming from Cartesian coordinates $\left(x_{1}, x_{2}\right)$ to polar coordinates $(r, \theta)$ so that

$$
x_{1}=r \cos \theta, \quad x_{2}=r \sin \theta .
$$

We also map the mean $\boldsymbol{\mu}$ into polar coordinates by writing

$$
\mu_{1}=r_{0} \cos \theta_{0}, \quad \mu_{2}=r_{0} \sin \theta_{0}
$$

Next we substitute these transformations into the two-dimensional Gaussian distribution (3.123), and then condition on the unit circle $r=1$, noting that we are interested only in the dependence on $\theta$. Focusing on the exponent in the Gaussian distribution we have

$$
\begin{aligned}
& -\frac{1}{2 \sigma^{2}}\left\{\left(r \cos \theta-r_{0} \cos \theta_{0}\right)^{2}+\left(r \sin \theta-r_{0} \sin \theta_{0}\right)^{2}\right\} \\
& \quad=-\frac{1}{2 \sigma^{2}}\left\{1+r_{0}^{2}-2 r_{0} \cos \theta \cos \theta_{0}-2 r_{0} \sin \theta \sin \theta_{0}\right\} \\
& \quad=\frac{r_{0}}{\sigma^{2}} \cos \left(\theta-\theta_{0}\right)+\text { const }
\end{aligned}
$$

where 'const' denotes terms independent of $\theta$. We have made use of the following trigonometrical identities:

$$
\begin{aligned}
\cos ^{2} A+\sin ^{2} A & =1 \\
\cos A \cos B+\sin A \sin B & =\cos (A-B)
\end{aligned}
$$

If we now define $m=r_{0} / \sigma^{2}$, we obtain our final expression for the distribution of $p(\theta)$ along the unit circle $r=1$ in the form

$$
p\left(\theta \mid \theta_{0}, m\right)=\frac{1}{2 \pi I_{0}(m)} \exp \left\{m \cos \left(\theta-\theta_{0}\right)\right\}
$$


![](https://cdn.mathpix.com/cropped/2024_05_13_d2a86a8e5b0b3cfb4473g-1.jpg?height=586&width=1354&top_left_y=232&top_left_x=192

ChatGPT figure/image summary: The image presents two graphs representing the von Mises distribution for two different sets of parameter values. On the left side, there is a Cartesian plot where the horizontal axis likely represents the angle θ (ranging from 0 to 2π or from -π to π, though the axis is not explicitly labeled) and the vertical axis represents the probability density. The plot includes two curves corresponding to two different von Mises distributions:

- A red curve for the distribution with parameters m = 5, θ₀ = π/4.
- A blue curve for the distribution with parameters m = 1, θ₀ = 3π/4.

The red curve is narrower and has a higher peak, indicating a higher concentration parameter m, and suggests more certainty about the mean direction θ₀. Conversely, the blue curve is broader and flatter, indicating a lower concentration and hence more dispersion around the mean direction.

On the right side, there are polar plots corresponding to the same von Mises distributions. The horizontal line in the middle of the polar plot likely represents 0 radians (or 0 degrees), and the plot ranges from 0 to 2π in the clockwise direction. In polar coordinates, the angular variable θ is represented as the angle from the positive horizontal axis, and the radius indicates the probability density for that angle. The red curve (m = 5, θ₀ = π/4) is shown as a sharply defined bump indicating a direction around π/4 where the density is highest. The blue curve (m = 1, θ₀ = 3π/4) is more spread out, matching the same characteristics shown on the Cartesian plot.

These plots serve to visualize how the von Mises distribution, which is a probability distribution on the circle, changes with different values of the parameters m (concentration) and θ₀ (mean direction).)

Figure 3.11 The von Mises distribution plotted for two different parameter values, shown as a Cartesian plot on the left and as the corresponding polar plot on the right.

which is called the von Mises distribution or the circular normal. Here the parameter $\theta_{0}$ corresponds to the mean of the distribution, whereas $m$, which is known as the concentration parameter, is analogous to the inverse variance (i.e. the precision) for the Gaussian. The normalization coefficient in (3.129) is expressed in terms of $I_{0}(m)$, which is the zeroth-order modified Bessel function of the first kind (Abramowitz and Stegun, 1965) and is defined by

$$
I_{0}(m)=\frac{1}{2 \pi} \int_{0}^{2 \pi} \exp \{m \cos \theta\} \mathrm{d} \theta
$$

\title{
Exercise 3.31
}

For large $m$, the distribution becomes approximately Gaussian. The von Mises distribution is plotted in Figure 3.11, and the function $I_{0}(m)$ is plotted in Figure 3.12.

Now consider the maximum likelihood estimators for the parameters $\theta_{0}$ and $m$ for the von Mises distribution. The log likelihood function is given by

$$
\ln p\left(\mathcal{D} \mid \theta_{0}, m\right)=-N \ln (2 \pi)-N \ln I_{0}(m)+m \sum_{n=1}^{N} \cos \left(\theta_{n}-\theta_{0}\right)
$$

Setting the derivative with respect to $\theta_{0}$ equal to zero gives

$$
\sum_{n=1}^{N} \sin \left(\theta_{n}-\theta_{0}\right)=0
$$

To solve for $\theta_{0}$, we make use of the trigonometric identity

$$
\sin (A-B)=\cos B \sin A-\cos A \sin B
$$

Exercise $3.32 \quad$ from which we obtain


![](https://cdn.mathpix.com/cropped/2024_05_13_895fbab03e81bab56181g-1.jpg?height=512&width=1492&top_left_y=232&top_left_x=128

ChatGPT figure/image summary: The image displays two graphs side by side. On the left graph, a red curve represents the Bessel function \( I_0(m) \) plotted against \( m \) on the horizontal axis and \( I_0(m) \) on the vertical axis. The curve starts near the origin and rises steeply as \( m \) increases, indicating that \( I_0(m) \) grows rapidly with \( m \).

On the right graph, a red curve depicts the function \( A(m) \), which is plotted against \( m \) on the horizontal axis and \( A(m) \) on the vertical axis. The graph shows that \( A(m) \) starts at 0 when \( m \) is 0 and asymptotically approaches 1 as \( m \) increases, suggesting that \( A(m) \) saturates to a value of 1 for large \( m \).

Both graphs share a similar range for \( m \) on their respective horizontal axes, starting at 0 and extending to 10. Vertical axis scales are different due to the different nature of the functions plotted. The left graph's vertical axis reaches beyond 3000 to accommodate the rapid growth of the Bessel function, while the right graph's vertical axis goes up to 1 to display the saturation behavior of \( A(m) \).)

Figure 3.12 Plot of the Bessel function $I_{0}(m)$ defined by (3.130), together with the function $A(m)$ defined by $(3.136)$

$$
\theta_{0}^{\mathrm{ML}}=\tan ^{-1}\left\{\frac{\sum_{n} \sin \theta_{n}}{\sum_{n} \cos \theta_{n}}\right\}
$$

which we recognize as the result (3.119) obtained earlier for the mean of the observations viewed in a two-dimensional Cartesian space.

Similarly, maximizing (3.131) with respect to $m$ and making use of $I_{0}^{\prime}(m)=$ $I_{1}(m)$ (Abramowitz and Stegun, 1965), we have

$$
A\left(m_{\mathrm{ML}}\right)=\frac{1}{N} \sum_{n=1}^{N} \cos \left(\theta_{n}-\theta_{0}^{\mathrm{ML}}\right)
$$

where we have substituted for the maximum likelihood solution for $\theta_{0}^{\mathrm{ML}}$ (recalling that we are performing a joint optimization over $\theta$ and $m$ ), and we have defined

$$
A(m)=\frac{I_{1}(m)}{I_{0}(m)}
$$

The function $A(m)$ is plotted in Figure 3.12. Making use of the trigonometric identity (3.128), we can write (3.135) in the form

$$
A\left(m_{\mathrm{ML}}\right)=\left(\frac{1}{N} \sum_{n=1}^{N} \cos \theta_{n}\right) \cos \theta_{0}^{\mathrm{ML}}+\left(\frac{1}{N} \sum_{n=1}^{N} \sin \theta_{n}\right) \sin \theta_{0}^{\mathrm{ML}}
$$

The right-hand side of (3.137) is easily evaluated, and the function $A(m)$ can be inverted numerically. One limitation of the von Mises distribution is that it is unimodal. By forming mixtures of von Mises distributions, we obtain a flexible framework for modelling periodic variables that can handle multimodality.

For completeness, we mention briefly some alternative techniques for constructing periodic distributions. The simplest approach is to use a histogram of observations in which the angular coordinate is divided into fixed bins. This has the virtue of

is normalized and that it has mean and variance given by

$$
\begin{aligned}
\mathbb{E}[x] & =\mu \\
\operatorname{var}[x] & =\mu(1-\mu)
\end{aligned}
$$

Now suppose we have a data set $\mathcal{D}=\left\{x_{1}, \ldots, x_{N}\right\}$ of observed values of $x$. We can construct the likelihood function, which is a function of $\mu$, on the assumption that the observations are drawn independently from $p(x \mid \mu)$, so that

$$
p(\mathcal{D} \mid \mu)=\prod_{n=1}^{N} p\left(x_{n} \mid \mu\right)=\prod_{n=1}^{N} \mu^{x_{n}}(1-\mu)^{1-x_{n}}
$$

We can estimate a value for $\mu$ by maximizing the likelihood function or equivalently by maximizing the logarithm of the likelihood, since the log is a monotonic function. The log likelihood function of the Bernoulli distribution is given by

$$
\ln p(\mathcal{D} \mid \mu)=\sum_{n=1}^{N} \ln p\left(x_{n} \mid \mu\right)=\sum_{n=1}^{N}\left\{x_{n} \ln \mu+\left(1-x_{n}\right) \ln (1-\mu)\right\}
$$

At this point, note that the log likelihood function depends on the $N$ observations $x_{n}$ only through their sum $\sum_{n} x_{n}$. This sum provides an example of a sufficient statistic for the data under this distribution. If we set the derivative of $\ln p(\mathcal{D} \mid \mu)$ with respect to $\mu$ equal to zero, we obtain the maximum likelihood estimator:

$$
\mu_{\mathrm{ML}}=\frac{1}{N} \sum_{n=1}^{N} x_{n}
$$

which is also known as the sample mean. Denoting the number of observations of $x=1$ (heads) within this data set by $m$, we can write (3.7) in the form

$$
\mu_{\mathrm{ML}}=\frac{m}{N}
$$

so that the probability of landing heads is given, in this maximum likelihood framework, by the fraction of observations of heads in the data set.

\title{
3.1.2 Binomial distribution
}

We can also work out the distribution for the binary variable $x$ of the number $m$ of observations of $x=1$, given that the data set has size $N$. This is called the binomial distribution, and from (3.5) we see that it is proportional to $\mu^{m}(1-\mu)^{N-m}$. To obtain the normalization coefficient, note that out of $N$ coin flips, we have to add up all of the possible ways of obtaining $m$ heads, so that the binomial distribution can be written as

$$
\operatorname{Bin}(m \mid N, \mu)=\binom{N}{m} \mu^{m}(1-\mu)^{N-m}
$$

simplicity and flexibility but also suffers from significant limitations, as we will see

Section 3.5 when we discuss histogram methods in more detail later. Another approach starts, like the von Mises distribution, from a Gaussian distribution over a Euclidean space but now marginalizes onto the unit circle rather than conditioning (Mardia and Jupp, 2000). However, this leads to more complex forms of distribution and will not be discussed further. Finally, any valid distribution over the real axis (such as a Gaussian) can be turned into a periodic distribution by mapping successive intervals of width $2 \pi$ onto the periodic variable $(0,2 \pi)$, which corresponds to 'wrapping' the real axis around the unit circle. Again, the resulting distribution is more complex to handle than the von Mises distribution.

\title{
3.4. The Exponential Family
}

The probability distributions that we have studied so far in this chapter (with the exception of mixture models) are specific examples of a broad class of distributions called the exponential family (Duda and Hart, 1973; Bernardo and Smith, 1994). Members of the exponential family have many important properties in common, and it is illuminating to discuss these properties in some generality.

The exponential family of distributions over $\mathrm{x}$, given parameters $\boldsymbol{\eta}$, is defined to be the set of distributions of the form

$$
p(\mathbf{x} \mid \boldsymbol{\eta})=h(\mathbf{x}) g(\boldsymbol{\eta}) \exp \left\{\boldsymbol{\eta}^{\mathrm{T}} \mathbf{u}(\mathbf{x})\right\}
$$

where $\mathrm{x}$ may be scalar or vector and may be discrete or continuous. Here $\boldsymbol{\eta}$ are called the natural parameters of the distribution, and $\mathbf{u}(\mathbf{x})$ is some function of $\mathbf{x}$. The function $g(\boldsymbol{\eta})$ can be interpreted as the coefficient that ensures that the distribution is normalized, and therefore, it satisfies

$$
g(\boldsymbol{\eta}) \int h(\mathbf{x}) \exp \left\{\boldsymbol{\eta}^{\mathrm{T}} \mathbf{u}(\mathbf{x})\right\} \mathrm{d} \mathbf{x}=1
$$

where the integration is replaced by summation if $\mathrm{x}$ is a discrete variable.

We begin by taking some examples of the distributions introduced earlier in the chapter and showing that they are indeed members of the exponential family. Consider first the Bernoulli distribution:

$$
p(x \mid \mu)=\operatorname{Bern}(x \mid \mu)=\mu^{x}(1-\mu)^{1-x}
$$

Expressing the right-hand side as the exponential of the logarithm, we have

$$
\begin{aligned}
p(x \mid \mu) & =\exp \{x \ln \mu+(1-x) \ln (1-\mu)\} \\
& =(1-\mu) \exp \left\{\ln \left(\frac{\mu}{1-\mu}\right) x\right\}
\end{aligned}
$$

Comparison with (3.138) allows us to identify

$$
\eta=\ln \left(\frac{\mu}{1-\mu}\right)
$$

which we can solve for $\mu$ to give $\mu=\sigma(\eta)$, where

$$
\sigma(\eta)=\frac{1}{1+\exp (-\eta)}
$$

is called the logistic sigmoid function. Thus, we can write the Bernoulli distribution using the standard representation (3.138) in the form

$$
p(x \mid \eta)=\sigma(-\eta) \exp (\eta x)
$$

where we have used $1-\sigma(\eta)=\sigma(-\eta)$, which is easily proved from (3.143). Comparison with (3.138) shows that

$$
\begin{aligned}
u(x) & =x \\
h(x) & =1 \\
g(\eta) & =\sigma(-\eta)
\end{aligned}
$$

Next consider the multinomial distribution which, for a single observation $\mathbf{x}$, takes the form

$$
p(\mathbf{x} \mid \boldsymbol{\mu})=\prod_{k=1}^{M} \mu_{k}^{x_{k}}=\exp \left\{\sum_{k=1}^{M} x_{k} \ln \mu_{k}\right\}
$$

where $\mathbf{x}=\left(x_{1}, \ldots, x_{M}\right)^{\mathrm{T}}$. Again, we can write this in the standard representation (3.138) so that

$$
p(\mathbf{x} \mid \boldsymbol{\eta})=\exp \left(\boldsymbol{\eta}^{\mathrm{T}} \mathbf{x}\right)
$$

where $\eta_{k}=\ln \mu_{k}$, and we have defined $\boldsymbol{\eta}=\left(\eta_{1}, \ldots, \eta_{M}\right)^{\mathrm{T}}$. Again, comparing with (3.138) we have

$$
\begin{aligned}
\mathbf{u}(\mathbf{x}) & =\mathbf{x} \\
h(\mathbf{x}) & =1 \\
g(\boldsymbol{\eta}) & =1
\end{aligned}
$$

Note that the parameters $\eta_{k}$ are not independent because the parameters $\mu_{k}$ are subject to the constraint

$$
\sum_{k=1}^{M} \mu_{k}=1
$$

so that, given any $M-1$ of the parameters $\mu_{k}$, the value of the remaining parameter is fixed. In some circumstances, it will be convenient to remove this constraint by expressing the distribution in terms of only $M-1$ parameters. This can be achieved by using the relationship (3.153) to eliminate $\mu_{M}$ by expressing it in terms of the remaining $\left\{\mu_{k}\right\}$ where $k=1, \ldots, M-1$, thereby leaving $M-1$ parameters. Note that these remaining parameters are still subject to the constraints

$$
0 \leqslant \mu_{k} \leqslant 1, \quad \sum_{k=1}^{M-1} \mu_{k} \leqslant 1
$$

Making use of the constraint (3.153), the multinomial distribution in this representation then becomes

$$
\begin{aligned}
& \exp \left\{\sum_{k=1}^{M} x_{k} \ln \mu_{k}\right\} \\
& =\exp \left\{\sum_{k=1}^{M-1} x_{k} \ln \mu_{k}+\left(1-\sum_{k=1}^{M-1} x_{k}\right) \ln \left(1-\sum_{k=1}^{M-1} \mu_{k}\right)\right\} \\
& =\exp \left\{\sum_{k=1}^{M-1} x_{k} \ln \left(\frac{\mu_{k}}{1-\sum_{j=1}^{M-1} \mu_{j}}\right)+\ln \left(1-\sum_{k=1}^{M-1} \mu_{k}\right)\right\}
\end{aligned}
$$

We now identify

$$
\ln \left(\frac{\mu_{k}}{1-\sum_{j} \mu_{j}}\right)=\eta_{k}
$$

which we can solve for $\mu_{k}$ by first summing both sides over $k$ and then rearranging and back-substituting to give

$$
\mu_{k}=\frac{\exp \left(\eta_{k}\right)}{1+\sum_{j} \exp \left(\eta_{j}\right)}
$$

This is called the softmax function or the normalized exponential. In this representation, the multinomial distribution therefore takes the form

$$
p(\mathbf{x} \mid \boldsymbol{\eta})=\left(1+\sum_{k=1}^{M-1} \exp \left(\eta_{k}\right)\right)^{-1} \exp \left(\boldsymbol{\eta}^{\mathrm{T}} \mathbf{x}\right)
$$

This is the standard form of the exponential family, with parameter vector $\boldsymbol{\eta}=$ $\left(\eta_{1}, \ldots, \eta_{M-1}\right)^{\mathrm{T}}$ in which

$$
\begin{aligned}
\mathbf{u}(\mathbf{x}) & =\mathbf{x} \\
h(\mathbf{x}) & =1 \\
g(\boldsymbol{\eta}) & =\left(1+\sum_{k=1}^{M-1} \exp \left(\eta_{k}\right)\right)^{-1}
\end{aligned}
$$

Finally, let us consider the Gaussian distribution. For the univariate Gaussian, we have

$$
\begin{aligned}
p\left(x \mid \mu, \sigma^{2}\right) & =\frac{1}{\left(2 \pi \sigma^{2}\right)^{1 / 2}} \exp \left\{-\frac{1}{2 \sigma^{2}}(x-\mu)^{2}\right\} \\
& =\frac{1}{\left(2 \pi \sigma^{2}\right)^{1 / 2}} \exp \left\{-\frac{1}{2 \sigma^{2}} x^{2}+\frac{\mu}{\sigma^{2}} x-\frac{1}{2 \sigma^{2}} \mu^{2}\right\}
\end{aligned}
$$

which, after some simple rearranging, can be cast in the standard exponential family form (3.138) with

$$
\begin{aligned}
\boldsymbol{\eta} & =\binom{\mu / \sigma^{2}}{-1 / 2 \sigma^{2}} \\
\mathbf{u}(x) & =\binom{x}{x^{2}} \\
h(\mathbf{x}) & =(2 \pi)^{-1 / 2} \\
g(\boldsymbol{\eta}) & =\left(-2 \eta_{2}\right)^{1 / 2} \exp \left(\frac{\eta_{1}^{2}}{4 \eta_{2}}\right)
\end{aligned}
$$

Finally, we shall sometimes make use of a restricted form of (3.138) in which we choose $\mathbf{u}(\mathrm{x})=\mathrm{x}$. However, this can be somewhat generalized by noting that if $f(\mathbf{x})$ is a normalized density then

$$
\frac{1}{s} f\left(\frac{1}{s} \mathbf{x}\right)
$$

is also a normalized density, where $s>0$ is a scale parameter. Combining these, we arrive at a restricted set of exponential family class-conditional densities of the form

$$
p\left(\mathbf{x} \mid \boldsymbol{\lambda}_{k}, s\right)=\frac{1}{s} h\left(\frac{1}{s} \mathbf{x}\right) g\left(\boldsymbol{\lambda}_{k}\right) \exp \left\{\frac{1}{s} \boldsymbol{\lambda}_{k}^{\mathrm{T}} \mathbf{x}\right\}
$$

Note that we are allowing each class to have its own parameter vector $\boldsymbol{\lambda}_{k}$ but we are assuming that the classes share the same scale parameter $s$.

\title{
3.4.1 Sufficient statistics
}

Let us now consider the problem of estimating the parameter vector $\boldsymbol{\eta}$ in the general exponential family distribution (3.138) using the technique of maximum likelihood. Taking the gradient of both sides of (3.139) with respect to $\boldsymbol{\eta}$, we have

$$
\begin{aligned}
& \nabla g(\boldsymbol{\eta}) \int h(\mathbf{x}) \exp \left\{\boldsymbol{\eta}^{\mathrm{T}} \mathbf{u}(\mathbf{x})\right\} \mathrm{d} \mathbf{x} \\
& \quad+g(\boldsymbol{\eta}) \int h(\mathbf{x}) \exp \left\{\boldsymbol{\eta}^{\mathrm{T}} \mathbf{u}(\mathbf{x})\right\} \mathbf{u}(\mathbf{x}) \mathrm{d} \mathbf{x}=0
\end{aligned}
$$

Rearranging and making use again of (3.139) then gives

$$
-\frac{1}{g(\boldsymbol{\eta})} \nabla g(\boldsymbol{\eta})=g(\boldsymbol{\eta}) \int h(\mathbf{x}) \exp \left\{\boldsymbol{\eta}^{\mathrm{T}} \mathbf{u}(\mathbf{x})\right\} \mathbf{u}(\mathbf{x}) \mathrm{d} \mathbf{x}=\mathbb{E}[\mathbf{u}(\mathbf{x})]
$$

We therefore obtain the result

$$
-\nabla \ln g(\boldsymbol{\eta})=\mathbb{E}[\mathbf{u}(\mathbf{x})]
$$

Note that the covariance of $\mathbf{u}(\mathbf{x})$ can be expressed in terms of the second derivatives of $g(\boldsymbol{\eta})$, and similarly for higher-order moments. Thus, provided we can normalize a distribution from the exponential family, we can always find its moments by simple differentiation.

Now consider a set of independent identically distributed data denoted by $\mathbf{X}=$ $\left\{\mathbf{x}_{1}, \ldots, \mathbf{x}_{n}\right\}$, for which the likelihood function is given by

$$
p(\mathbf{X} \mid \boldsymbol{\eta})=\left(\prod_{n=1}^{N} h\left(\mathbf{x}_{n}\right)\right) g(\boldsymbol{\eta})^{N} \exp \left\{\boldsymbol{\eta}^{\mathrm{T}} \sum_{n=1}^{N} \mathbf{u}\left(\mathbf{x}_{n}\right)\right\}
$$

Setting the gradient of $\ln p(\mathbf{X} \mid \boldsymbol{\eta})$ with respect to $\boldsymbol{\eta}$ to zero, we get the following condition to be satisfied by the maximum likelihood estimator $\boldsymbol{\eta}_{\mathrm{ML}}$ :

$$
-\nabla \ln g\left(\boldsymbol{\eta}_{\mathrm{ML}}\right)=\frac{1}{N} \sum_{n=1}^{N} \mathbf{u}\left(\mathbf{x}_{n}\right)
$$

which can in principle be solved to obtain $\boldsymbol{\eta}_{\mathrm{ML}}$. We see that the solution for the maximum likelihood estimator depends on the data only through $\sum_{n} \mathbf{u}\left(\mathbf{x}_{n}\right)$, which is therefore called the sufficient statistic of the distribution (3.138). We do not need to store the entire data set itself but only the value of the sufficient statistic. For the Bernoulli distribution, for example, the function $\mathbf{u}(x)$ is given just by $x$ and so we need only keep the sum of the data points $\left\{x_{n}\right\}$, whereas for the Gaussian $\mathbf{u}(x)=\left(x, x^{2}\right)^{\mathrm{T}}$, and so we should keep both the sum of $\left\{x_{n}\right\}$ and the sum of $\left\{x_{n}^{2}\right\}$.

If we consider the limit $N \rightarrow \infty$, then the right-hand side of (3.174) becomes $\mathbb{E}[\mathbf{u}(\mathbf{x})]$, and so by comparing with (3.172) we see that in this limit, $\boldsymbol{\eta}_{\mathrm{ML}}$ will equal the true value $\boldsymbol{\eta}$.

\title{
3.5. Nonparametric Methods
}

Throughout this chapter, we have focused on the use of probability distributions having specific functional forms governed by a small number of parameters whose values are to be determined from a data set. This is called the parametric approach to density modelling. An important limitation of this approach is that the chosen density might be a poor model of the distribution that generates the data, which can result in poor predictive performance. For instance, if the process that generates the data is multimodal, then this aspect of the distribution can never be captured by a Gaussian, which is necessarily unimodal. In this final section, we consider some nonparametric approaches to density estimation that make few assumptions about the form of the distribution.

\subsection*{3.5.1 Histograms}

Let us start with a discussion of histogram methods for density estimation, which we have already encountered in the context of marginal and conditional distributions in Figure 2.5 and in the context of the central limit theorem in Figure 3.2. Here we explore the properties of histogram density models in more detail, focusing on cases with a single continuous variable $x$. Standard histograms simply partition $x$ into distinct bins of width $\Delta_{i}$ and then count the number $n_{i}$ of observations of $x$ falling

Figure 3.13 An illustration of the histogram approach to density estimation, in which a data set of 50 data points is generated from the distribution shown by the green curve. Histogram density estimates, based on (3.175) with a common bin width $\Delta$, are shown for various values of $\Delta$.

![](https://cdn.mathpix.com/cropped/2024_05_13_1386240291c0269943e6g-1.jpg?height=513&width=628&top_left_y=244&top_left_x=956

ChatGPT figure/image summary: The image shows three histograms, each representing density estimates of a data set consisting of 50 data points that were generated from a distribution depicted by the background green curve (which appears to be a mixture of two Gaussians). The histograms are illustrating different levels of granularity based on varying bin widths, Delta (Δ), for the density estimation.

The top histogram uses a bin width of Δ = 0.04, resulting in a very spiked representation that exhibits more variance and captures very fine details of the data, potentially including noise or fluctuations that are not representative of the underlying distribution.

The middle histogram employs a bin width of Δ = 0.08. This histogram is smoother than the one above, capturing a more balanced representation of the underlying distribution while providing some detail of its structure.

The bottom histogram utilizes a bin width of Δ = 0.25, which oversimplifies the underlying distribution, smoothing out important details such as the bimodal peaks, and not effectively representing the true distribution.

Each histogram demonstrates the effect of choosing different bin widths on the estimated probability density function, highlighting the necessity of selecting an optimal bin width to accurately model the true underlying distribution without introducing too much noise or oversmoothing the features.)

in bin $i$. To turn this count into a normalized probability density, we simply divide by the total number $N$ of observations and by the width $\Delta_{i}$ of the bins to obtain probability values for each bin:

$$
p_{i}=\frac{n_{i}}{N \Delta_{i}}
$$

for which it is easily seen that $\int p(x) \mathrm{d} x=1$. This gives a model for the density $p(x)$ that is constant over the width of each bin. Often the bins are chosen to have the same width $\Delta_{i}=\Delta$.

In Figure 3.13, we show an example of histogram density estimation. Here the data is drawn from the distribution corresponding to the green curve, which is formed from a mixture of two Gaussians. Also shown are three examples of histogram density estimates corresponding to three different choices for the bin width $\Delta$. We see that when $\Delta$ is very small (top figure), the resulting density model is very spiky, with a lot of structure that is not present in the underlying distribution that generated the data set. Conversely, if $\Delta$ is too large (bottom figure) then the result is a model that is too smooth and consequently fails to capture the bimodal property of the green curve. The best results are obtained for some intermediate value of $\Delta$ (middle figure). In principle, a histogram density model is also dependent on the choice of edge location for the bins, though this is typically much less significant than the bin width $\Delta$.

Note that the histogram method has the property (unlike the methods to be discussed shortly) that, once the histogram has been computed, the data set itself can be discarded, which can be advantageous if the data set is large. Also, the histogram approach is easily applied if the data points arrive sequentially.

In practice, the histogram technique can be useful for obtaining a quick visualization of data in one or two dimensions but is unsuited to most density estimation applications. One obvious problem is that the estimated density has discontinuities that are due to the bin edges rather than any property of the underlying distribution that generated the data. A major limitation of the histogram approach is its scaling with dimensionality. If we divide each variable in a $D$-dimensional space into

Section 6.1.1

Chapter 1

Section 3.1.2 $M$ bins, then the total number of bins will be $M^{D}$. This exponential scaling with $D$ is an example of the curse of dimensionality. In a space of high dimensionality, the quantity of data needed to provide meaningful estimates of the local probability density would be prohibitive.

The histogram approach to density estimation does, however, teach us two important lessons. First, to estimate the probability density at a particular location, we should consider the data points that lie within some local neighbourhood of that point. Note that the concept of locality requires that we assume some form of distance measure, and here we have been assuming Euclidean distance. For histograms, this neighbourhood property was defined by the bins, and there is a natural 'smoothing' parameter describing the spatial extent of the local region, in this case the bin width. Second, to obtain good results, the value of the smoothing parameter should be neither too large nor too small. This is reminiscent of the choice of model complexity in polynomial regression where the degree $M$ of the polynomial, or alternatively the value $\lambda$ of the regularization parameter, was optimal for some intermediate value, neither too large nor too small. Armed with these insights, we turn now to a discussion of two widely used nonparametric techniques for density estimation, kernel estimators and nearest neighbours, which have better scaling with dimensionality than the simple histogram model.

\subsection*{3.5.2 Kernel densities}

Let us suppose that observations are being drawn from some unknown probability density $p(\mathbf{x})$ in some $D$-dimensional space, which we will take to be Euclidean, and we wish to estimate the value of $p(\mathbf{x})$. From our earlier discussion of locality, let us consider some small region $\mathcal{R}$ containing $\mathbf{x}$. The probability mass associated with this region is given by

$$
P=\int_{\mathcal{R}} p(\mathbf{x}) \mathrm{d} \mathbf{x}
$$

Now suppose that we have collected a data set comprising $N$ observations drawn from $p(\mathbf{x})$. Because each data point has a probability $P$ of falling within $\mathcal{R}$, the total number $K$ of points that lie inside $\mathcal{R}$ will be distributed according to the binomial distribution:

$$
\operatorname{Bin}(K \mid N, P)=\frac{N!}{K!(N-K)!} P^{K}(1-P)^{N-K}
$$

Using (3.11), we see that the mean fraction of points falling inside the region is $\mathbb{E}[K / N]=P$, and similarly using (3.12), we see that the variance around this mean is $\operatorname{var}[K / N]=P(1-P) / N$. For large $N$, this distribution will be sharply peaked around the mean and so

$$
K \simeq N P
$$

If, however, we also assume that the region $\mathcal{R}$ is sufficiently small so that the probability density $p(\mathbf{x})$ is roughly constant over the region, then we have

$$
P \simeq p(\mathbf{x}) V
$$

where $V$ is the volume of $\mathcal{R}$. Combining (3.178) and (3.179), we obtain our density estimate in the form

$$
p(\mathbf{x})=\frac{K}{N V}
$$

Note that the validity of (3.180) depends on two contradictory assumptions, namely that the region $\mathcal{R}$ is sufficiently small that the density is approximately constant over the region and yet sufficiently large (in relation to the value of that density) that the number $K$ of points falling inside the region is sufficient for the binomial distribution to be sharply peaked.

We can exploit the result (3.180) in two different ways. Either we can fix $K$ and determine the value of $V$ from the data, which gives rise to the $K$-nearest-neighbour technique discussed shortly, or we can fix $V$ and determine $K$ from the data, giving rise to the kernel approach. It can be shown that both the $K$-nearest-neighbour density estimator and the kernel density estimator converge to the true probability density in the limit $N \rightarrow \infty$ provided that $V$ shrinks with $N$ and that $K$ grows with $N$, at an appropriate rate (Duda and Hart, 1973).

We begin by discussing the kernel method in detail. To start with we take the region $\mathcal{R}$ to be a small hypercube centred on the point $\mathrm{x}$ at which we wish to determine the probability density. To count the number $K$ of points falling within this region, it is convenient to define the following function:

$$
k(\mathbf{u})=\left\{\begin{array}{ll}
1, & \left|u_{i}\right| \leqslant 1 / 2, \\
0, & \text { otherwise }
\end{array} \quad i=1, \ldots, D\right.
$$

which represents a unit cube centred on the origin. The function $k(\mathbf{u})$ is an example of a kernel function, and in this context, it is also called a Parzen window. From (3.181), the quantity $k\left(\left(\mathbf{x}-\mathbf{x}_{n}\right) / h\right)$ will be 1 if the data point $\mathbf{x}_{n}$ lies inside a cube of side $h$ centred on $\mathbf{x}$, and zero otherwise. The total number of data points lying inside this cube will therefore be

$$
K=\sum_{n=1}^{N} k\left(\frac{\mathbf{x}-\mathbf{x}_{n}}{h}\right)
$$

Substituting this expression into (3.180) then gives the following result for the estimated density at $\mathbf{x}$ :

$$
p(\mathbf{x})=\frac{1}{N} \sum_{n=1}^{N} \frac{1}{h^{D}} k\left(\frac{\mathbf{x}-\mathbf{x}_{n}}{h}\right)
$$

where we have used $V=h^{D}$ for the volume of a hypercube of side $h$ in $D$ dimensions. Using the symmetry of the function $k(\mathbf{u})$, we can now reinterpret this equation, not as a single cube centred on $\mathrm{x}$ but as the sum over $N$ cubes centred on the $N$ data points $\mathbf{x}_{n}$.

As it stands, the kernel density estimator (3.183) will suffer from one of the same problems that the histogram method suffered from, namely the presence of artificial discontinuities, in this case at the boundaries of the cubes. We can obtain a smoother

Figure 3.14 Illustration of the kernel density model (3.184) applied to the same data set used to demonstrate the histogram approach in Figure 3.13. We see that $h$ acts as a smoothing parameter and that if it is set too small (top panel), the result is a very noisy density model, whereas if it is set too large (bottom panel), then the bimodal nature of the underlying distribution from which the data is generated (shown by the green curve) is washed out. The best density model is obtained for some intermediate value of $h$

![](https://cdn.mathpix.com/cropped/2024_05_13_394aafe250f00e0713c1g-1.jpg?height=181&width=628&top_left_y=244&top_left_x=956

ChatGPT figure/image summary: The image is a graph representing a kernel density estimate of a data set, with a very small smoothing parameter \( h = 0.005 \). The horizontal axis likely represents some variable across its domain, possibly the data points in the set, while the vertical axis represents the estimated density values for that variable.

The graph displays a noisy blue line that oscillates significantly, indicating the density estimate at various points across the variable's domain. The small value of \( h \) has led to a high sensitivity to local variations in the data, and as a result, the density estimate appears to be overfitting the data, capturing too much noise and not reflecting a smooth underlying distribution.

Also shown on the chart is a smooth green curve, which likely represents the true or underlying distribution from which the data points were sampled. The discrepancy between the green curve and the noisy blue line illustrates the paper's point: when \( h \) is set very small, the resulting density model can be very noisy and does not smoothly capture the true properties of the underlying distribution.

The context provided suggests that the figure should serve as a visual example of what happens when the smoothing parameter \( h \) in kernel density estimation is set too small, leading to a result that is not ideal for representing the true density of the data.)


![](https://cdn.mathpix.com/cropped/2024_05_13_394aafe250f00e0713c1g-1.jpg?height=210&width=630&top_left_y=552&top_left_x=955

ChatGPT figure/image summary: The image depicts a graph that apparently corresponds to the illustration of kernel density estimation described in the extracted text, specifically aligned with Figure 3.14 in the given context. This graph represents the application of a kernel density model to a data set. Based on the information provided, the graph shows the result of applying a kernel density model with a particular smoothing parameter h, which is set to a value of 0.2 in this instance.

In the graph, there appear to be two curves: one representing the kernel density estimate (likely the blue curve) and the other representing the true density (likely the green curve) from which the data set was generated. The description mentions that if h is set too small, the density estimate will be very noisy, while a large h could oversmooth the data and wash out important features such as bimodality. Therefore, the image likely illustrates the effect of setting the smoothing parameter h to a small value (0.2), leading to a density model that captures more fluctuations in the data.

The x-axis seems to represent some standardized variable or measurement, while the y-axis indicates the estimated density or frequency of the data points. The blue curve might be the estimated density that has higher variance due to a small h, reflecting every fluctuation in the data points, while the green curve probably shows the true underlying distribution which exhibits a smoother, bimodal nature.)
(middle panel).

density model if we choose a smoother kernel function, and a common choice is the Gaussian, which gives rise to the following kernel density model:

$$
p(\mathbf{x})=\frac{1}{N} \sum_{n=1}^{N} \frac{1}{\left(2 \pi h^{2}\right)^{D / 2}} \exp \left\{-\frac{\left\|\mathbf{x}-\mathbf{x}_{n}\right\|^{2}}{2 h^{2}}\right\}
$$

where $h$ represents the standard deviation of the Gaussian components. Thus, our density model is obtained by placing a Gaussian over each data point, adding up the contributions over the whole data set, and then dividing by $N$ so that the density is correctly normalized. In Figure 3.14, we apply the model (3.184) to the data set used earlier to demonstrate the histogram technique. We see that, as expected, the parameter $h$ plays the role of a smoothing parameter, and there is a trade-off between sensitivity to noise at small $h$ and over-smoothing at large $h$. Again, the optimization of $h$ is a problem in model complexity, analogous to the choice of bin width in histogram density estimation or the degree of the polynomial used in curve fitting.

We can choose any other kernel function $k(\mathbf{u})$ in (3.183) subject to the conditions

$$
\begin{aligned}
k(\mathbf{u}) & \geqslant 0 \\
\int k(\mathbf{u}) \mathrm{d} \mathbf{u} & =1
\end{aligned}
$$

which ensure that the resulting probability distribution is non-negative everywhere and integrates to one. The class of density model given by (3.183) is called a kernel density estimator or Parzen estimator. It has a great merit that there is no computation involved in the 'training' phase because this simply requires the training set to be stored. However, this is also one of its great weaknesses because the computational cost of evaluating the density grows linearly with the size of the data set.

Figure 3.15 Illustration of $K$-nearestneighbour density estimation using the same data set as in Figures 3.14 and 3.13. We see that the parameter $K$ governs the degree of smoothing, so that a small value of $K$ leads to a very noisy density model (top panel), whereas a large value (bottom panel) smooths out the bimodal nature of the true distribution (shown by the green curve) from which the data set was generated

![](https://cdn.mathpix.com/cropped/2024_05_13_6ed6c0d1a6c56c334c29g-1.jpg?height=511&width=628&top_left_y=245&top_left_x=956

ChatGPT figure/image summary: The image provided is a set of three line graphs, each plotted within the same range of what appears to be 0 to 1 on the x-axis, and 0 to 5 on the y-axis. Each graph includes a noisy blue line and a smooth green curve. The three graphs represent different values of a parameter $K$: at the top $K=1$, in the middle $K=5$, and at the bottom $K=30$. The noisy blue lines suggest the output of some estimation or density function applied to a dataset, while the smooth green curve seems to represent the actual or underlying distribution from which the data was generated.

The graphs illustrate how changing the parameter $K$ affects the estimation of the data distribution. In the top graph where $K=1$, the estimation is very noisy and oscillates rapidly, indicating a high sensitivity to the data points. As $K$ increases to 5 in the middle graph, there's a noticeable decrease in noise and a better approximation of the green curve, though some noise and irregularities still persist. Finally, in the bottom graph with $K=30$, the estimation is much smoother and closely follows the shape of the green curve, implying a good balance between noise reduction and retaining the bimodal features of the underlying distribution. This sequence suggests that an intermediate value of $K$ provides a favorable trade-off between the sensitivity to noise and the ability to capture the true structure of the data distribution.)

\title{
3.5.3 Nearest-neighbours
}

One of the difficulties with the kernel approach to density estimation is that the parameter $h$ governing the kernel width is fixed for all kernels. In regions of high data density, a large value of $h$ may lead to over-smoothing and a washing out of structure that might otherwise be extracted from the data. However, reducing $h$ may lead to noisy estimates elsewhere in the data space where the density is smaller. Thus, the optimal choice for $h$ may be dependent on the location within the data space. This issue is addressed by nearest-neighbour methods for density estimation.

We therefore return to our general result (3.180) for local density estimation, and instead of fixing $V$ and determining the value of $K$ from the data, we consider a fixed value of $K$ and use the data to find an appropriate value for $V$. To do this, we consider a small sphere centred on the point $\mathrm{x}$ at which we wish to estimate the density $p(\mathbf{x})$, and we allow the radius of the sphere to grow until it contains precisely $K$ data points. The estimate of the density $p(\mathbf{x})$ is then given by (3.180) with $V$ set to the volume of the resulting sphere. This technique is known as $K$ nearest neighbours and is illustrated in Figure 3.15 for various choices of the parameter $K$ using the same data set as used in Figures 3.13 and 3.14. We see that the value of $K$ now governs the degree of smoothing and that again there is an optimum choice for $K$ that is neither too large nor too small. Note that the model produced by $K$ nearest neighbours is not a true density model because the integral over all space diverges.

We close this chapter by showing how the $K$-nearest-neighbour technique for density estimation can be extended to the problem of classification. To do this, we apply the $K$-nearest-neighbour density estimation technique to each class separately and then make use of Bayes' theorem. Let us suppose that we have a data set comprising $N_{k}$ points in class $\mathcal{C}_{k}$ with $N$ points in total, so that $\sum_{k} N_{k}=N$. If we wish to classify a new point $\mathbf{x}$, we draw a sphere centred on $\mathbf{x}$ containing precisely $K$ points irrespective of their class. Suppose this sphere has volume $V$ and contains $K_{k}$ points from class $\mathcal{C}_{k}$. Then (3.180) provides an estimate of the density associated

Figure 3.1 Histogram plot of the binomial distribution (3.9) as a function of $m$ for $N=10$ and $\mu=0.25$.

![](https://cdn.mathpix.com/cropped/2024_05_13_f10b60699ae8e7fdd3dcg-1.jpg?height=513&width=732&top_left_y=232&top_left_x=911

ChatGPT figure/image summary: The image shows a histogram plot of the binomial distribution as a function of \( m \). It represents the probability distribution for \( m \), where \( m \) is the number of successes in \( N=10 \) trials, with the probability of success in each trial being \( \mu=0.25 \). The histogram bars correspond to different values of \( m \), which range from 0 to 10, and the height of each bar represents the probability of observing that number of successes within the 10 trials, under the binomial distribution assumptions.

The histogram provides a visual interpretation of the binomial distribution, showing that for this particular setting, lower and higher values of \( m \) are less likely than the values closer to the mean, which is \( N\mu = 10 \times 0.25 = 2.5 \). However, the bars suggest that the most likely number of successes \( m \) is slightly higher than 2.5, likely around 3, due to the discrete nature of the distribution. The plot is a typical representation that one might find in a textbook discussing probability and statistics, particularly the binomial distribution and its properties.)

where

$$
\binom{N}{m} \equiv \frac{N!}{(N-m)!m!}
$$

Exercise 3.3

Exercise 2.10

is the number of ways of choosing $m$ objects out of a total of $N$ identical objects without replacement. Figure 3.1 shows a plot of the binomial distribution for $N=10$ and $\mu=0.25$.

The mean and variance of the binomial distribution can be found by using the results that, for independent events, the mean of the sum is the sum of the means and the variance of the sum is the sum of the variances. Because $m=x_{1}+\ldots+x_{N}$ and because for each observation the mean and variance are given by (3.3) and (3.4), respectively, we have

$$
\begin{aligned}
\mathbb{E}[m] & \equiv \sum_{m=0}^{N} m \operatorname{Bin}(m \mid N, \mu)=N \mu \\
\operatorname{var}[m] & \equiv \sum_{m=0}^{N}(m-\mathbb{E}[m])^{2} \operatorname{Bin}(m \mid N, \mu)=N \mu(1-\mu)
\end{aligned}
$$

Exercise 3.4 These results can also be proved directly by using calculus.

\title{
3.1.3 Multinomial distribution
}

Binary variables can be used to describe quantities that can take one of two possible values. Often, however, we encounter discrete variables that can take on one of $K$ possible mutually exclusive states. Although there are various alternative ways to express such variables, we will see shortly that a particularly convenient representation is the 1-of- $K$ scheme, sometimes called 'one-hot encoding', in which the variable is represented by a $K$-dimensional vector $\mathrm{x}$ in which one of the elements $x_{k}$ equals 1 and all remaining elements equal 0 . So, for instance, if we have a variable that can take $K=6$ states and a particular observation of the variable happens to

Figure 3.16 (a) In the $K$-nearestneighbour classifier, a new point, shown by the black diamond, is classified according to the majority class membership of the $K$ closest training data points, in this case $K=$ 3. (b) In the nearest-neighbour ( $K=1$ ) approach to classification, the resulting decision boundary is composed of hyperplanes that form perpendicular bisectors of pairs of points from different classes.

![](https://cdn.mathpix.com/cropped/2024_05_13_8f53b2b39e722c44ef82g-1.jpg?height=491&width=515&top_left_y=214&top_left_x=622

ChatGPT figure/image summary: The image provided shows a 2-dimensional scatter plot with two distinct classes of points: one represented by red dots and the other by blue dots. A black diamond symbol, presumably representing a new data point, is also present in the plot. The green lines drawn from the black diamond suggest that this point's classification is determined by measuring its proximity to the nearest neighbouring points from the two classes. This is a visual representation of a k-nearest neighbour classifier, where in this example \( K \) seems to be 3, meaning that the classification of the black diamond point is influenced by the 3 closest points from the existing classes. The axes are labeled \( x_1 \) and \( x_2 \), indicating the two dimensions of the feature space for the data points shown.)

(a)

![](https://cdn.mathpix.com/cropped/2024_05_13_8f53b2b39e722c44ef82g-1.jpg?height=504&width=515&top_left_y=212&top_left_x=1130

ChatGPT figure/image summary: The provided image graphs the decision boundary of a classification problem in a two-dimensional feature space labeled \( x_1 \) and \( x_2 \). Red and blue dots represent data points from two different classes in the feature space. A green line represents the decision boundary determined by a nearest-neighbour classification algorithm (likely for \( K=1 \), as the boundary is nonlinear and appears to be adapting closely to the individual data points).

This decision boundary is used to classify new data points based on their proximity to existing points from the training dataset. If a new point falls on one side of the green line, it would be classified into one class (say, the blue class), and if it falls on the other side, it would be classified into the red class. The decision boundary visually represents how the nearest-neighbour algorithm distinguishes between the two classes based on the closest training examples.)

(b)

with each class:

$$
p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)=\frac{K_{k}}{N_{k} V}
$$

Similarly, the unconditional density is given by

$$
p(\mathbf{x})=\frac{K}{N V}
$$

and the class priors are given by

$$
p\left(\mathcal{C}_{k}\right)=\frac{N_{k}}{N}
$$

We can now combine (3.187), (3.188), and (3.189) using Bayes' theorem to obtain the posterior probability of class membership:

$$
p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)=\frac{p\left(\mathbf{x} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right)}{p(\mathbf{x})}=\frac{K_{k}}{K}
$$

We can minimize the probability of misclassification by assigning the test point $\mathrm{x}$ to the class having the largest posterior probability, corresponding to the largest value of $K_{k} / K$. Thus, to classify a new point, we identify the $K$ nearest points from the training data set and then assign the new point to the class having the largest number of representatives amongst this set. Ties can be broken at random. The particular case of $K=1$ is called the nearest-neighbour rule, because a test point is simply assigned to the same class as the nearest point from the training set. These concepts are illustrated in Figure 3.16.

An interesting property of the nearest-neighbour $(K=1)$ classifier is that, in the limit $N \rightarrow \infty$, the error rate is never more than twice the minimum achievable error rate of an optimal classifier, i.e., one that uses the true class distributions (Cover and Hart, 1967) .

As discussed so far, both the $K$-nearest-neighbour method and the kernel density estimator require the entire training data set to be stored, leading to expensive

computation if the data set is large. This effect can be offset, at the expense of some additional one-off computation, by constructing tree-based search structures to allow (approximate) near neighbours to be found efficiently without doing an exhaustive search of the data set. Nevertheless, these nonparametric methods are still severely limited. On the other hand, we have seen that simple parametric models are very restricted in terms of the forms of distribution that they can represent. We therefore need to find density models that are very flexible and yet for which the complexity of the models can be controlled independently of the size of the training set, and this can be achieved using deep neural networks.

\title{
Exercises
}

3.1 (*) Verify that the Bernoulli distribution (3.2) satisfies the following properties:

$$
\begin{aligned}
\sum_{x=0}^{1} p(x \mid \mu) & =1 \\
\mathbb{E}[x] & =\mu \\
\operatorname{var}[x] & =\mu(1-\mu)
\end{aligned}
$$

Show that the entropy $\mathrm{H}[x]$ of a Bernoulli-distributed random binary variable $x$ is given by

$$
\mathrm{H}[x]=-\mu \ln \mu-(1-\mu) \ln (1-\mu)
$$

$3.2(\star \star)$ The form of the Bernoulli distribution given by (3.2) is not symmetric between the two values of $x$. In some situations, it will be more convenient to use an equivalent formulation for which $x \in\{-1,1\}$, in which case the distribution can be written

$$
p(x \mid \mu)=\left(\frac{1-\mu}{2}\right)^{(1-x) / 2}\left(\frac{1+\mu}{2}\right)^{(1+x) / 2}
$$

where $\mu \in[-1,1]$. Show that the distribution (3.195) is normalized, and evaluate its mean, variance, and entropy.

$3.3(\star \star)$ In this exercise, we prove that the binomial distribution (3.9) is normalized. First, use the definition (3.10) of the number of combinations of $m$ identical objects chosen from a total of $N$ to show that

$$
\binom{N}{m}+\binom{N}{m-1}=\binom{N+1}{m}
$$

Use this result to prove by induction the following result:

$$
(1+x)^{N}=\sum_{m=0}^{N}\binom{N}{m} x^{m}
$$

correspond to the state where $x_{3}=1$, then $\mathbf{x}$ will be represented by

$$
\mathbf{x}=(0,0,1,0,0,0)^{\mathrm{T}}
$$

Note that such vectors satisfy $\sum_{k=1}^{K} x_{k}=1$. If we denote the probability of $x_{k}=1$ by the parameter $\mu_{k}$, then the distribution of $\mathbf{x}$ is given by

$$
p(\mathbf{x} \mid \boldsymbol{\mu})=\prod_{k=1}^{K} \mu_{k}^{x_{k}}
$$

where $\boldsymbol{\mu}=\left(\mu_{1}, \ldots, \mu_{K}\right)^{\mathrm{T}}$, and the parameters $\mu_{k}$ are constrained to satisfy $\mu_{k} \geqslant 0$ and $\sum_{k} \mu_{k}=1$, because they represent probabilities. The distribution (3.14) can be regarded as a generalization of the Bernoulli distribution to more than two outcomes. It is easily seen that the distribution is normalized:

$$
\sum_{\mathbf{x}} p(\mathbf{x} \mid \boldsymbol{\mu})=\sum_{k=1}^{K} \mu_{k}=1
$$

and that

$$
\mathbb{E}[\mathbf{x} \mid \boldsymbol{\mu}]=\sum_{\mathbf{x}} p(\mathbf{x} \mid \boldsymbol{\mu}) \mathbf{x}=\boldsymbol{\mu}
$$

Now consider a data set $\mathcal{D}$ of $N$ independent observations $\mathbf{x}_{1}, \ldots, \mathbf{x}_{N}$. The corresponding likelihood function takes the form

$$
p(\mathcal{D} \mid \boldsymbol{\mu})=\prod_{n=1}^{N} \prod_{k=1}^{K} \mu_{k}^{x_{n k}}=\prod_{k=1}^{K} \mu_{k}^{\left(\sum_{n} x_{n k}\right)}=\prod_{k=1}^{K} \mu_{k}^{m_{k}}
$$

where we see that the likelihood function depends on the $N$ data points only through the $K$ quantities:

$$
m_{k}=\sum_{n=1}^{N} x_{n k}
$$

Section 3.4

Appendix $C$

which represent the number of observations of $x_{k}=1$. These are called the sufficient statistics for this distribution. Note that the variables $m_{k}$ are subject to the constraint

$$
\sum_{k=1}^{K} m_{k}=N
$$

To find the maximum likelihood solution for $\boldsymbol{\mu}$, we need to maximize $\ln p(\mathcal{D} \mid \boldsymbol{\mu})$ with respect to $\mu_{k}$ taking account of the constraint (3.15) that the $\mu_{k}$ must sum to one. This can be achieved using a Lagrange multiplier $\lambda$ and maximizing

$$
\sum_{k=1}^{K} m_{k} \ln \mu_{k}+\lambda\left(\sum_{k=1}^{K} \mu_{k}-1\right)
$$

Setting the derivative of (3.20) with respect to $\mu_{k}$ to zero, we obtain

$$
\mu_{k}=-m_{k} / \lambda
$$

We can solve for the Lagrange multiplier $\lambda$ by substituting (3.21) into the constraint $\sum_{k} \mu_{k}=1$ to give $\lambda=-N$. Thus, we obtain the maximum likelihood solution for $\mu_{k}$ in the form

$$
\mu_{k}^{\mathrm{ML}}=\frac{m_{k}}{N}
$$

which is the fraction of the $N$ observations for which $x_{k}=1$.

We can also consider the joint distribution of the quantities $m_{1}, \ldots, m_{K}$, conditioned on the parameter vector $\boldsymbol{\mu}$ and on the total number $N$ of observations. From (3.17), this takes the form

$$
\operatorname{Mult}\left(m_{1}, m_{2}, \ldots, m_{K} \mid \boldsymbol{\mu}, N\right)=\binom{N}{m_{1} m_{2} \ldots m_{K}} \prod_{k=1}^{K} \mu_{k}^{m_{k}}
$$

which is known as the multinomial distribution. The normalization coefficient is the number of ways of partitioning $N$ objects into $K$ groups of size $m_{1}, \ldots, m_{K}$ and is given by

$$
\binom{N}{m_{1} m_{2} \ldots m_{K}}=\frac{N!}{m_{1}!m_{2}!\ldots m_{K}!}
$$

Note that two-state quantities can be represented either as binary variables and modelled using the binomial distribution (3.9) or as 1 -of-2 variables and modelled using the distribution (3.14) with $K=2$.

\title{
3.2. The Multivariate Gaussian
}

Section 2.3

Section 2.5
The Gaussian, also known as the normal distribution, is a widely used model for the distribution of continuous variables. We have already seen that for of a single variable $x$, the Gaussian distribution can be written in the form

$$
\mathcal{N}\left(x \mid \mu, \sigma^{2}\right)=\frac{1}{\left(2 \pi \sigma^{2}\right)^{1 / 2}} \exp \left\{-\frac{1}{2 \sigma^{2}}(x-\mu)^{2}\right\}
$$

where $\mu$ is the mean and $\sigma^{2}$ is the variance. For a $D$-dimensional vector $\mathbf{x}$, the multivariate Gaussian distribution takes the form

$$
\mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}, \boldsymbol{\Sigma})=\frac{1}{(2 \pi)^{D / 2}} \frac{1}{|\boldsymbol{\Sigma}|^{1 / 2}} \exp \left\{-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})\right\}
$$

where $\boldsymbol{\mu}$ is the $D$-dimensional mean vector, $\boldsymbol{\Sigma}$ is the $D \times D$ covariance matrix, and det $\boldsymbol{\Sigma}$ denotes the determinant of $\boldsymbol{\Sigma}$.

The Gaussian distribution arises in many different contexts and can be motivated from a variety of different perspectives. For example, we have already seen that for


![](https://cdn.mathpix.com/cropped/2024_05_13_e8ee62e6cbb6e54a3380g-1.jpg?height=324&width=970&top_left_y=226&top_left_x=133

ChatGPT figure/image summary: The image contains two side-by-side histogram plots. Both histograms display the distribution of values within the range of 0 to 1 on the x-axis. On the y-axis, there are numerical values possibly indicating the frequency or probability density of the observations within each bin of the histogram.

The histogram on the left is labeled "N = 1" and shows a uniform distribution, with each bin having an equally tall bar, indicating that there is an equal frequency of the variable's occurrence in each interval.

The histogram on the right is labeled "N = 2" and shows a distribution that is beginning to take on a bell-shaped form, suggesting that observations are more likely to occur around the central values and less likely towards the extremes of 0 and 1.

The context provided describes that as the number "N" of uniformly distributed variables increases, the distribution of their mean tends towards a Gaussian distribution. This illustrates a demonstration of the Central Limit Theorem, where the mean of a large number of uniformly distributed variables will approach a normal (Gaussian) distribution, even if the original variables themselves are not normally distributed. The histograms in the image likely represent an early stage of this phenomenon, with "N = 1" not showing a Gaussian shape and "N = 2" displaying a more pronounced central peak.)

![](https://cdn.mathpix.com/cropped/2024_05_13_e8ee62e6cbb6e54a3380g-1.jpg?height=310&width=455&top_left_y=236&top_left_x=1167

ChatGPT figure/image summary: The image appears to be a histogram plot representing the distribution of the mean of \( N \) uniformly distributed numbers. The value of \( N \) is indicated as 10, suggesting that the histogram plot is showing the distribution resulting from the mean of 10 uniformly distributed random variables over the interval [0,1]. The x-axis likely represents the mean value, with the interval ranging from 0 to 1, while the y-axis represents the frequency of each bin. The histogram bars are colored blue, and the overall shape might resemble a Gaussian distribution to some extent, although with such a small value of \( N \), the distribution should not be expected to be perfectly Gaussian. The histogram is a visual representation used to illustrate the concepts discussed in the text, likely related to the central limit theorem or sampling of random variables.)

Figure 3.2 Histogram plots of the mean of $N$ uniformly distributed numbers for various values of $N$. We observe that as $N$ increases, the distribution tends towards a Gaussian.

Exercise 3.8

Appendix $A$

Exercise 3.11 a single real variable, the distribution that maximizes the entropy is the Gaussian. This property applies also to the multivariate Gaussian.

Another situation in which the Gaussian distribution arises is when we consider the sum of multiple random variables. The central limit theorem tells us that, subject to certain mild conditions, the sum of a set of random variables, which is of course itself a random variable, has a distribution that becomes increasingly Gaussian as the number of terms in the sum increases (Walker, 1969). We can illustrate this by considering $N$ variables $x_{1}, \ldots, x_{N}$ each of which has a uniform distribution over the interval $[0,1]$ and then considering the distribution of the mean $\left(x_{1}+\cdots+x_{N}\right) / N$. For large $N$, this distribution tends to a Gaussian, as illustrated in Figure 3.2. In practice, the convergence to a Gaussian as $N$ increases can be very rapid. One consequence of this result is that the binomial distribution (3.9), which is a distribution over $m$ defined by the sum of $N$ observations of the random binary variable $x$, will tend to a Gaussian as $N \rightarrow \infty$ (see Figure 3.1 for $N=10$ ).

The Gaussian distribution has many important analytical properties, and we will consider several of these in detail. As a result, this section will be rather more technically involved than some of the earlier sections and will require familiarity with various matrix identities.

\subsection*{3.2.1 Geometry of the Gaussian}

We begin by considering the geometrical form of the Gaussian distribution. The functional dependence of the Gaussian on $\mathrm{x}$ is through the quadratic form

$$
\Delta^{2}=(\mathbf{x}-\boldsymbol{\mu})^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})
$$

which appears in the exponent. The quantity $\Delta$ is called the Mahalanobis distance from $\boldsymbol{\mu}$ to $\mathrm{x}$. It reduces to the Euclidean distance when $\boldsymbol{\Sigma}$ is the identity matrix. The Gaussian distribution is constant on surfaces in $\mathrm{x}$-space for which this quadratic form is constant.

First, note that the matrix $\boldsymbol{\Sigma}$ can be taken to be symmetric, without loss of generality, because any antisymmetric component would disappear from the exponent. Now consider the eigenvector equation for the covariance matrix

$$
\boldsymbol{\Sigma} \mathbf{u}_{i}=\lambda_{i} \mathbf{u}_{i}
$$

Exercise 3.12

Exercise 3.13

\section*{Appendix A}

Chapter 16 where $i=1, \ldots, D$. Because $\boldsymbol{\Sigma}$ is a real, symmetric matrix, its eigenvalues will be real, and its eigenvectors can be chosen to form an orthonormal set, so that

$$
\mathbf{u}_{i}^{\mathrm{T}} \mathbf{u}_{j}=I_{i j}
$$

where $I_{i j}$ is the $i, j$ element of the identity matrix and satisfies

$$
I_{i j}= \begin{cases}1, & \text { if } i=j \\ 0, & \text { otherwise }\end{cases}
$$

The covariance matrix $\Sigma$ can be expressed as an expansion in terms of its eigenvectors in the form

$$
\boldsymbol{\Sigma}=\sum_{i=1}^{D} \lambda_{i} \mathbf{u}_{i} \mathbf{u}_{i}^{\mathrm{T}}
$$

and similarly the inverse covariance matrix $\boldsymbol{\Sigma}^{-1}$ can be expressed as

$$
\boldsymbol{\Sigma}^{-1}=\sum_{i=1}^{D} \frac{1}{\lambda_{i}} \mathbf{u}_{i} \mathbf{u}_{i}^{\mathrm{T}}
$$

Substituting (3.32) into (3.27), the quadratic form becomes

$$
\Delta^{2}=\sum_{i=1}^{D} \frac{y_{i}^{2}}{\lambda_{i}}
$$

where we have defined

$$
y_{i}=\mathbf{u}_{i}^{\mathrm{T}}(\mathbf{x}-\boldsymbol{\mu})
$$

We can interpret $\left\{y_{i}\right\}$ as a new coordinate system defined by the orthonormal vectors $\mathbf{u}_{i}$ that are shifted and rotated with respect to the original $x_{i}$ coordinates. Forming the vector $\mathbf{y}=\left(y_{1}, \ldots, y_{D}\right)^{\mathrm{T}}$, we have

$$
\mathbf{y}=\mathbf{U}(\mathbf{x}-\boldsymbol{\mu})
$$

where $\mathbf{U}$ is a matrix whose rows are given by $\mathbf{u}_{i}^{\mathrm{T}}$. From (3.29) it follows that $\mathbf{U}$ is an orthogonal matrix, i.e., it satisfies $\mathbf{U} \mathbf{U}^{\mathrm{T}}=\mathbf{U}^{\mathrm{T}} \mathbf{U}=\mathbf{I}$, where $\mathbf{I}$ is the identity matrix.

The quadratic form, and hence the Gaussian density, is constant on surfaces for which (3.33) is constant. If all the eigenvalues $\lambda_{i}$ are positive, then these surfaces represent ellipsoids, with their centres at $\boldsymbol{\mu}$ and their axes oriented along $\mathbf{u}_{i}$, and with scaling factors in the directions of the axes given by $\lambda_{i}^{1 / 2}$, as illustrated in Figure 3.3.

For the Gaussian distribution to be well defined, it is necessary for all the eigenvalues $\lambda_{i}$ of the covariance matrix to be strictly positive, otherwise the distribution cannot be properly normalized. A matrix whose eigenvalues are strictly positive is said to be positive definite. When we discuss latent variable models, we will encounter Gaussian distributions for which one or more of the eigenvalues are zero, in

Figure 3.3 The red curve shows the elliptical surface of constant probability density for a Gaussian in a two-dimensional space $\mathrm{x}=$ $\left(x_{1}, x_{2}\right)$ on which the density is $\exp (-1 / 2)$ of its value at $\mathbf{x}=$ $\mu$. The axes of the ellipse are defined by the eigenvectors $\mathbf{u}_{i}$ of the covariance matrix, with corresponding eigenvalues $\lambda_{i}$.

![](https://cdn.mathpix.com/cropped/2024_05_13_1c6f5d15308081306a07g-1.jpg?height=564&width=787&top_left_y=216&top_left_x=857

ChatGPT figure/image summary: The image is a two-dimensional graphical illustration of a Gaussian probability density function. It includes the following elements:

- An ellipse (red curve), representing a surface of constant probability density for a two-dimensional Gaussian distribution.
- The \( x_1 \) and \( x_2 \) axes, representing a two-dimensional space in which the distribution exists.
- Two eigenvectors, \( \mathbf{u}_1 \) and \( \mathbf{u}_2 \), depicted as black arrows, indicating the principal directions of the distribution, with their origin at the mean \( \boldsymbol{\mu} \) of the distribution.
- The mean \( \boldsymbol{\mu} \) is represented as a blue dot at the center of the ellipse.
- Two orthogonal coordinate axes, \( y_1 \) and \( y_2 \), shown as blue arrows, which are aligned with the eigenvectors and represent the new coordinate system defined by the eigenvectors.
- The scaling factors \( \lambda_1^{1/2} \) and \( \lambda_2^{1/2} \), illustrated as arrow lengths along the \( y_1 \) and \( y_2 \) axes, corresponding to the square roots of the eigenvalues associated with the eigenvectors of the covariance matrix.

This figure visualizes how a multivariate Gaussian distribution can be characterized by its mean and covariance structure, with the eigenvectors aligning with the directions of maximum variance. The ellipsoid represents the shape of the probability density, and the length of the axes of the ellipsoid reflects the magnitude of the eigenvalues, which are a measure of the spread of the distribution along the corresponding eigenvector.)

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


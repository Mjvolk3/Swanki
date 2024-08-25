## Chapter: Standard Distributions

In this chapter, we delve into specific examples of probability distributions and their properties. These distributions are essential not only in their own right but also as foundational elements for more complex models. They play a crucial role in modeling the probability distribution of a random variable based on a finite set of observations, a task known as density estimation. However, density estimation is an inherently challenging problem because numerous probability distributions could potentially explain the observed finite data set. Selecting an appropriate distribution is closely tied to the broader issue of model selection, which stands as a central concern in machine learning.

### Section: Moments

We begin by examining the moments of the Gaussian distribution and interpreting the parameters Mu (mean) and Sigma (covariance). The expectation, or mean, of a random variable 'x' under the Gaussian distribution is determined through an integral that includes an exponential term and the variable 'x'. By substituting 'z' for 'x - Mu', and recognizing that the exponent is an even function of the components of 'z', we find that the term involving 'z' in the factor '(z + Mu)' cancels out due to symmetry. Thus, the expectation of 'x' equals Mu, identifying Mu as the mean of the Gaussian distribution.

Next, we consider second-order moments of the Gaussian distribution. For a multivariate Gaussian distribution, these moments include the expectations of the products of pairs of components, grouped into a matrix termed 'expectation of [x times x transpose]'. This expectation can be expressed as an integral involving an exponential term, 'x', and 'x transpose'. By substituting 'z' for 'x - Mu' and applying the eigenvector expansion of the covariance matrix, we find that the expectation of 'x times x transpose' equals 'Mu times Mu transpose + Sigma'.

The covariance of a random vector 'x' is defined by first subtracting the mean and then taking the second moment. Specifically, for a Gaussian distribution, the covariance of 'x' equals Sigma. Therefore, the matrix Sigma, which describes the covariance of 'x' under the Gaussian distribution, is known as the covariance matrix.

### Section: Limitations

Despite its widespread use, the Gaussian distribution has certain limitations. The number of free parameters grows quadratically with the dimensionality (D), making the manipulation and inversion of large matrices computationally challenging. To mitigate this, restricted forms of the covariance matrix, such as diagonal or isotropic matrices, can be employed. However, these simplifications limit the distribution's ability to capture complex correlations within the data.

Moreover, the Gaussian distribution is unimodal, meaning it has a single peak. Consequently, it cannot effectively approximate multimodal distributions. This duality of being both overly flexible (due to many parameters) and overly restrictive (unable to represent multiple modes) can be addressed by introducing latent variables, as we will explore later.

### Section: Conditional Distribution

An important property of a multivariate Gaussian distribution is the preservation of Gaussianity under both marginalization and conditioning. If two sets of variables are jointly Gaussian, the conditional distribution of one set given the other is also Gaussian. Similarly, the marginal distribution of any subset is Gaussian.

Consider a D-dimensional Gaussian vector 'x', which we partition into subsets 'x_a' and 'x_b'. Correspondingly, the mean vector Mu and covariance matrix Sigma are partitioned. The inverse of the covariance matrix, known as the precision matrix, also follows this partitioning structure.

Depending on the context, some properties of Gaussian distributions are more conveniently expressed in terms of the covariance matrix, while others are simpler when viewed through the precision matrix. Hence, both representations are utilized as needed.

### Section: Partitioned Gaussian Distributions

Partitioning Gaussian distributions allows us to understand the interactions between different parts of the distribution. For a multivariate Gaussian with mean vector Mu and covariance matrix Sigma, we can decompose these into smaller components, such as Mu_a, Mu_b, and the submatrices Sigma_aa, Sigma_ab, Sigma_ba, and Sigma_bb.

This decomposition helps establish relationships between different parts of the Gaussian distribution. For example, submatrices with the same subscript, like Sigma_aa and Lambda_aa, mirror each other across the main diagonal, although Lambda_aa is not simply the inverse of Sigma_aa.

### Section: Conditional Distribution

To illustrate the calculation of the conditional distribution in partitioned Gaussian distributions, consider fixing one part of the distribution and normalizing the resulting expression. The conditional distribution of 'x_a' given 'x_b' can be represented as a quadratic function of 'x_a'. The covariance of this conditional distribution is derived from the inverse of Lambda_aa, and the mean is a linear function of the observed value 'x_b'. This method, known as 'completing the square', is commonly used when working with Gaussian distributions.

### Section: Marginal Distribution

The marginal distribution of a subset of variables in a Gaussian distribution is also Gaussian. By integrating out one part of the joint distribution, the covariance of the marginal distribution is obtained from the inverse of a matrix formed from the partitioned precision matrices, while the mean remains unchanged.

Understanding partitioned Gaussian distributions, along with their conditional and marginal distributions, provides insights into the dependencies and relationships within a Gaussian distribution. This knowledge allows us to manipulate and analyze different parts of the distribution to gain a deeper understanding of the overall distribution.

### Section: Bayes' Theorem and Linear-Gaussian Models

Bayes' theorem is fundamental in updating probability distributions based on new data and is widely used in machine learning algorithms. In the context of Gaussian distributions, consider a Gaussian marginal distribution for variable 'x' and a Gaussian conditional distribution for variable 'y' given 'x'. If the mean of the conditional distribution is a linear function of 'x' and its variance remains constant, it forms a linear-Gaussian model.

The joint distribution of 'x' and 'y' is also Gaussian, with its mean derived as a linear function of the parameters of the marginal and conditional distributions. The precision of this joint distribution can be represented as a block matrix, similar to the partitioned precision matrix discussed earlier. The covariance of the joint distribution can be derived using the matrix inversion formula, and the mean can be obtained from the parameters of the marginal and conditional distributions and their precision matrices.

### Section: Mixture of Gaussians

Gaussian mixture models provide a powerful and flexible way to model complex data distributions. These models comprise a combination of Gaussian distributions, each defined by its own mean and covariance. The overall mixture model is a weighted sum of these components, with the weights, or mixing coefficients, summing to one.

The probability density function for a mixture of Gaussians is given by the sum of the weighted Gaussian densities. These mixing coefficients have a probabilistic interpretation, representing the prior probability of a data point belonging to a particular Gaussian component. By using Bayes' theorem, we can determine the posterior probabilities or responsibilities of each Gaussian component for each data point.

Finding the maximum likelihood estimates for the parameters of a Gaussian mixture model is complex due to the summation inside the logarithm in the likelihood function. Iterative optimization techniques or the expectation-maximization algorithm are typically used to find these estimates.

### Section: Periodic Variables

Periodic variables, such as wind direction or calendar time, exhibit repeating patterns over a specific period. Conventional distributions like the Gaussian are not suitable for these variables due to their periodic nature. For instance, wind direction measurements are better represented as points on a unit circle with two-dimensional unit vectors, ensuring that the origin of the angular coordinate does not affect the mean calculation.

### Section: Von Mises Distribution

The von Mises distribution is a suitable model for circular data, serving as the circular equivalent of the Gaussian distribution. This distribution respects the periodicity of the data, ensuring non-negative probability density, integration to one, and periodicity.

By representing the values as points on a unit circle and calculating the mean of these Cartesian representations, we can create a distribution that handles the circular nature of periodic variables effectively. The von Mises distribution can also be derived by conditioning a two-dimensional Gaussian distribution on the unit circle.

### Section: Introduction to Two-Dimensional Gaussian Distributions

Two-dimensional Gaussian distributions are characterized by a mean vector and a covariance matrix. The mean vector indicates the center of the distribution, and the covariance matrix describes the spread and orientation. When the covariance matrix is proportional to the identity matrix, the distribution becomes isotropic, meaning the spread is equal in all directions, resulting in circular contours of constant probability density.

By transitioning from Cartesian to polar coordinates, we can better understand the behavior of this distribution along a fixed radius.

### Example: Old Faithful Geyser Data Set

To illustrate these concepts, consider the Old Faithful geyser data set, which measures the duration of eruptions and the time until the next eruption. A simple Gaussian distribution fails to capture the structure of this data, as it forms two distinct clusters. However, by using a mixture of two Gaussian distributions, we can effectively model this data, demonstrating the power and flexibility of Gaussian mixtures in modeling complex, multimodal distributions.

In summary, selecting the model that best captures the underlying structure of the data—whether a simple Gaussian, a mixture of Gaussians, or a nonparametric model—depends on the specific characteristics of the data set. By combining these concepts, we can build robust and flexible models capable of handling a wide range of scenarios, enhancing our understanding of the mathematical foundations underpinning machine learning and data analysis.

## Chapter: Standard Distributions

In this chapter, we delve into specific examples of probability distributions and their properties. These distributions are essential not only in their own right but also as foundational elements for more complex models. They play a crucial role in modeling the probability distribution of a random variable based on a finite set of observations, a task known as density estimation. However, density estimation is an inherently challenging problem because numerous probability distributions could potentially explain the observed finite data set. Selecting an appropriate distribution is closely tied to the broader issue of model selection, which stands as a central concern in machine learning.

### Section: Moments

We begin by examining the moments of the Gaussian distribution and interpreting the parameters Mu (mean) and Sigma (covariance). The expectation, or mean, of a random variable 'x' under the Gaussian distribution is determined through an integral that includes an exponential term and the variable 'x'. By substituting 'z' for 'x - Mu', and recognizing that the exponent is an even function of the components of 'z', we find that the term involving 'z' in the factor '(z + Mu)' cancels out due to symmetry. Thus, the expectation of 'x' equals Mu, identifying Mu as the mean of the Gaussian distribution.

Next, we consider second-order moments of the Gaussian distribution. For a multivariate Gaussian distribution, these moments include the expectations of the products of pairs of components, grouped into a matrix termed 'expectation of [x times x transpose]'. This expectation can be expressed as an integral involving an exponential term, 'x', and 'x transpose'. By substituting 'z' for 'x - Mu' and applying the eigenvector expansion of the covariance matrix, we find that the expectation of 'x times x transpose' equals 'Mu times Mu transpose + Sigma'.

The covariance of a random vector 'x' is defined by first subtracting the mean and then taking the second moment. Specifically, for a Gaussian distribution, the covariance of 'x' equals Sigma. Therefore, the matrix Sigma, which describes the covariance of 'x' under the Gaussian distribution, is known as the covariance matrix.

### Section: Limitations

Despite its widespread use, the Gaussian distribution has certain limitations. The number of free parameters grows quadratically with the dimensionality (D), making the manipulation and inversion of large matrices computationally challenging. To mitigate this, restricted forms of the covariance matrix, such as diagonal or isotropic matrices, can be employed. However, these simplifications limit the distribution's ability to capture complex correlations within the data.

Moreover, the Gaussian distribution is unimodal, meaning it has a single peak. Consequently, it cannot effectively approximate multimodal distributions. This duality of being both overly flexible (due to many parameters) and overly restrictive (unable to represent multiple modes) can be addressed by introducing latent variables, as we will explore later.

### Section: Conditional Distribution

An important property of a multivariate Gaussian distribution is the preservation of Gaussianity under both marginalization and conditioning. If two sets of variables are jointly Gaussian, the conditional distribution of one set given the other is also Gaussian. Similarly, the marginal distribution of any subset is Gaussian.

Consider a D-dimensional Gaussian vector 'x', which we partition into subsets 'x_a' and 'x_b'. Correspondingly, the mean vector Mu and covariance matrix Sigma are partitioned. The inverse of the covariance matrix, known as the precision matrix, also follows this partitioning structure.

Depending on the context, some properties of Gaussian distributions are more conveniently expressed in terms of the covariance matrix, while others are simpler when viewed through the precision matrix. Hence, both representations are utilized as needed.

### Section: Partitioned Gaussian Distributions

Partitioning Gaussian distributions allows us to understand the interactions between different parts of the distribution. For a multivariate Gaussian with mean vector Mu and covariance matrix Sigma, we can decompose these into smaller components, such as Mu_a, Mu_b, and the submatrices Sigma_aa, Sigma_ab, Sigma_ba, and Sigma_bb.

This decomposition helps establish relationships between different parts of the Gaussian distribution. For example, submatrices with the same subscript, like Sigma_aa and Lambda_aa, mirror each other across the main diagonal, although Lambda_aa is not simply the inverse of Sigma_aa.

### Section: Conditional Distribution

To illustrate the calculation of the conditional distribution in partitioned Gaussian distributions, consider fixing one part of the distribution and normalizing the resulting expression. The conditional distribution of 'x_a' given 'x_b' can be represented as a quadratic function of 'x_a'. The covariance of this conditional distribution is derived from the inverse of Lambda_aa, and the mean is a linear function of the observed value 'x_b'. This method, known as 'completing the square', is commonly used when working with Gaussian distributions.

### Section: Marginal Distribution

The marginal distribution of a subset of variables in a Gaussian distribution is also Gaussian. By integrating out one part of the joint distribution, the covariance of the marginal distribution is obtained from the inverse of a matrix formed from the partitioned precision matrices, while the mean remains unchanged.

Understanding partitioned Gaussian distributions, along with their conditional and marginal distributions, provides insights into the dependencies and relationships within a Gaussian distribution. This knowledge allows us to manipulate and analyze different parts of the distribution to gain a deeper understanding of the overall distribution.

### Section: Bayes' Theorem and Linear-Gaussian Models

Bayes' theorem is fundamental in updating probability distributions based on new data and is widely used in machine learning algorithms. In the context of Gaussian distributions, consider a Gaussian marginal distribution for variable 'x' and a Gaussian conditional distribution for variable 'y' given 'x'. If the mean of the conditional distribution is a linear function of 'x' and its variance remains constant, it forms a linear-Gaussian model.

The joint distribution of 'x' and 'y' is also Gaussian, with its mean derived as a linear function of the parameters of the marginal and conditional distributions. The precision of this joint distribution can be represented as a block matrix, similar to the partitioned precision matrix discussed earlier. The covariance of the joint distribution can be derived using the matrix inversion formula, and the mean can be obtained from the parameters of the marginal and conditional distributions and their precision matrices.

### Section: Mixture of Gaussians

Gaussian mixture models provide a powerful and flexible way to model complex data distributions. These models comprise a combination of Gaussian distributions, each defined by its own mean and covariance. The overall mixture model is a weighted sum of these components, with the weights, or mixing coefficients, summing to one.

The probability density function for a mixture of Gaussians is given by the sum of the weighted Gaussian densities. These mixing coefficients have a probabilistic interpretation, representing the prior probability of a data point belonging to a particular Gaussian component. By using Bayes' theorem, we can determine the posterior probabilities or responsibilities of each Gaussian component for each data point.

Finding the maximum likelihood estimates for the parameters of a Gaussian mixture model is complex due to the summation inside the logarithm in the likelihood function. Iterative optimization techniques or the expectation-maximization algorithm are typically used to find these estimates.

### Section: Periodic Variables

Periodic variables, such as wind direction or calendar time, exhibit repeating patterns over a specific period. Conventional distributions like the Gaussian are not suitable for these variables due to their periodic nature. For instance, wind direction measurements are better represented as points on a unit circle with two-dimensional unit vectors, ensuring that the origin of the angular coordinate does not affect the mean calculation.

### Section: Von Mises Distribution

The von Mises distribution is a suitable model for circular data, serving as the circular equivalent of the Gaussian distribution. This distribution respects the periodicity of the data, ensuring non-negative probability density, integration to one, and periodicity.

By representing the values as points on a unit circle and calculating the mean of these Cartesian representations, we can create a distribution that handles the circular nature of periodic variables effectively. The von Mises distribution can also be derived by conditioning a two-dimensional Gaussian distribution on the unit circle.

### Section: Transformation from Cartesian to Polar Coordinates

We start by transforming the coordinates from Cartesian to polar, replacing x1 and x2 with r (radius) and theta (angle), respectively. We also express the mean in polar coordinates, which gives us two equations, one for x1 (or r cosine theta) and another for x2 (or r sine theta).

Next, we substitute these transformations into the two-dimensional Gaussian distribution. We then condition on the unit circle, where r equals 1, to focus on the dependence on theta only.

This transformation leads us to a result that involves the cosine of the difference between theta and theta_0, where theta_0 is the mean of the distribution in polar coordinates. This result is derived using trigonometric identities, including the Pythagorean identity and the formula for the cosine of a difference.

### Section: Maximum Likelihood Estimators for the von Mises Distribution

Next, we discuss the maximum likelihood estimators for the parameters of the von Mises distribution, theta_0 and m. The maximum likelihood estimators are found by maximizing the log-likelihood function with respect to the parameters.

The maximum likelihood estimator for theta_0 is found by setting the derivative of the log-likelihood function with respect to theta_0 equal to zero. This results in an equation that can be solved using a trigonometric identity, yielding a result that is equivalent to the mean of the observations viewed in a two-dimensional Cartesian space.

Similarly, maximizing the log-likelihood function with respect to m yields an equation in terms of a function A(m), which is the ratio of the first-order and zeroth-order modified Bessel functions. A(m) can be inverted numerically to find the maximum likelihood estimator for m.

### Section: Limitations and Alternatives to the von Mises Distribution

The von Mises distribution is unimodal, meaning it has only one peak. This can be a limitation when modeling periodic variables that exhibit multimodality, or multiple peaks. One solution is to form mixtures of von Mises distributions, which can handle multimodality.

There are also other techniques for constructing periodic distributions, such as using histograms or wrapping distributions over the real axis onto the unit circle. However, these alternatives can lead to more complex forms of distribution and may not offer significant advantages over the von Mises distribution.

### Section: Exponential Family Distributions

The exponential family of distributions is a broad class that includes many of the distributions we have studied so far. Distributions in this family are characterized by a specific form involving the exponential function.

The Bernoulli distribution, for example, can be rewritten in the form of an exponential family distribution. This involves expressing the Bernoulli distribution as the exponential of the logarithm, and then identifying the natural parameters and other components of the standard representation of an exponential family distribution.

In the case of the Bernoulli distribution, the natural parameter is the log odds ratio, and the function of the data is simply the data itself. The sigmoid function is introduced as the inverse of the log odds ratio, allowing us to express the Bernoulli distribution in terms of the sigmoid function.

### Section: Multinomial Distribution

Now let's move onto the multinomial distribution. The multinomial distribution is a generalization of the binomial distribution. While the binomial distribution counts the number of successes from binary trials, the multinomial distribution counts the number of outcomes of multi-category trials.

In practical terms, the multinomial distribution can be used to describe quantities that can take one of several possible values. A common representation for this is the 1-of-K scheme, or "one-hot encoding", where the variable is represented by a K-dimensional vector. For instance, if we have a variable that can take 6 states, a particular observation of the variable would be represented by a 6-dimensional vector, with one element equal to 1 and all other elements equal to 0.

The mean of the multinomial distribution is simply the probability of each outcome, and the probability of each outcome can be calculated as the number of times it occurs divided by the total number of observations.

### Section: Nonparametric Methods

In the realm of density estimation, nonparametric methods provide flexible techniques that do not assume a specific functional form for the distribution. Two widely used nonparametric methods are kernel density estimators and nearest neighbors.

#### Subsection: Kernel Density Estimators

Kernel density estimation (KDE) involves placing a smooth kernel function, such as a Gaussian, on each data point and summing these kernels to form a smooth estimate of the probability density function. The choice of kernel width, or bandwidth, is crucial: too small a bandwidth leads to an overfit, noisy estimate, while too large a bandwidth results in an overly smooth estimate that may miss important features in the data.

#### Subsection: Nearest Neighbor Methods

Nearest neighbor methods estimate the density at a point by considering the distance to the K nearest data points. The volume of the region containing these K points is used to estimate the density. This approach adapts to varying data densities, as the region size adjusts based on the local data density. However, the choice of K is critical: too few neighbors lead to noisy estimates, while too many can smooth out important structure.

### Section: Binomial Distribution and its Properties

The binomial distribution models the number of successes in a fixed number of independent Bernoulli trials. The mean of the binomial distribution is the product of the number of trials and the probability of success, while the variance is the product of the number of trials, the probability of success, and the probability of failure.

### Section: K-nearest Neighbor Classification

The K-nearest neighbor classifier assigns a class to a new point based on the majority class among its K nearest neighbors. This simple yet effective method has the property that, as the number of training points approaches infinity, its error rate will be at most twice the minimum achievable error rate of an optimal classifier using the true class distributions.

### Section: The Multivariate Gaussian Distribution

The multivariate Gaussian distribution is characterized by a mean vector and a covariance matrix. This distribution is widely used due to its properties, such as being completely described by its mean and covariance and having a symmetric, bell-shaped form. According to the Central Limit Theorem, the sum of a large number of independent and identically distributed random variables approaches a Gaussian distribution, making it a natural choice for many statistical models.

### Section: Geometry of the Gaussian Distribution

The Gaussian distribution can be characterized geometrically by the quadratic form involving the difference between a variable and the mean, scaled by the covariance matrix. This quadratic form defines ellipsoids in the variable space, where the axes are determined by the eigenvectors of the covariance matrix, and the lengths of the axes are determined by the square roots of the eigenvalues.

In summary, understanding the properties and applications of various probability distributions, from the Gaussian to the von Mises and beyond, provides a solid foundation for building and interpreting statistical models. By combining these concepts with nonparametric methods and classification techniques, we can develop robust and flexible models capable of handling a wide range of scenarios, enhancing our understanding of the mathematical foundations underpinning machine learning and data analysis.

### Section: Positive Definite and Semidefinite Covariance Matrices

When discussing the properties of a covariance matrix in a Gaussian distribution, it is important to note that all eigenvalues of the covariance matrix must be strictly positive for the matrix to be considered positive definite. A positive definite matrix ensures that the quadratic form defined by the covariance matrix is always positive, which is a critical property for defining the shape and spread of the Gaussian distribution. If all eigenvalues are non-negative, the covariance matrix is classified as positive semidefinite. This means that while the matrix does not define a strictly positive quadratic form, it is still non-negative.

### Section: Independent Distributions in New Coordinate Systems

The Gaussian distribution can be transformed into a set of independent univariate Gaussian distributions by shifting and rotating the coordinate system according to the eigenvectors of the covariance matrix. This transformation leads to a new set of coordinates where the joint probability distribution of the variables factorizes into a product of independent distributions. Each of these independent distributions corresponds to one of the principal components of the original distribution, defined by the eigenvectors and eigenvalues of the covariance matrix.

### Section: Importance of Gaussian Distribution

This comprehensive examination of the Gaussian distribution and its properties underscores its significance in statistics and data analysis. Its prevalence is attributed to several key factors:

1. **Mathematical Elegance:** The Gaussian distribution has a simple and elegant mathematical form, characterized by its mean and covariance matrix. This simplicity facilitates analytical tractability and ease of manipulation in various applications.

2. **Central Limit Theorem:** According to the Central Limit Theorem, the sum of a large number of independent and identically distributed random variables tends to follow a Gaussian distribution, regardless of the original distribution of the variables. This makes the Gaussian distribution a natural model for many real-world phenomena.

3. **Ubiquitous Real-World Applications:** The Gaussian distribution appears in numerous real-world contexts, from natural phenomena to human behaviors. Its ability to model a wide range of data types makes it a fundamental tool in both theoretical and applied statistics.

4. **Predictive Power:** Because it is fully defined by its mean and covariance, the Gaussian distribution allows for straightforward parameter estimation and prediction, making it a cornerstone in the field of machine learning and data analysis.

By understanding the properties and implications of the Gaussian distribution, we gain valuable insights into the behavior and interpretation of data, enabling us to build more robust and accurate statistical models. This knowledge forms a critical component of the mathematical foundations underpinning advanced data analysis techniques and machine learning algorithms.

## Chapter: Standard Distributions

In this chapter, we explore specific examples of probability distributions and their properties. These distributions are significant not only on their own but also as foundational elements for more complex models.

One key role of the distributions discussed here is to model the probability distribution of a random variable, given a finite set of observations. This problem is known as density estimation. However, density estimation is fundamentally ill-posed because there are infinitely many probability distributions that could explain the observed finite data set. This issue of selecting an appropriate distribution connects to the broader problem of model selection, which is central in machine learning.

## Section: Moments

We now examine the moments of the Gaussian distribution and interpret the parameters Mu and Sigma. The expectation of the variable 'x' under the Gaussian distribution involves an integral with an exponential term and the variable 'x'. In this integral, we change variables using 'z equals x minus Mu'. Since the exponent is an even function of the components of 'z', and the integrals over these components are taken over the full range of real numbers, the term involving 'z' in the factor '(z plus Mu)' vanishes by symmetry. Therefore, the expectation of 'x' equals Mu, and we refer to Mu as the mean of the Gaussian distribution.

We also consider second-order moments of the Gaussian distribution. For the multivariate Gaussian, there are D-squared second-order moments given by the expectation of 'x_i x_j', which we can group together to form the matrix 'expectation of x x transpose'. This expectation can be written as another integral involving an exponential term, 'x', and 'x transpose'. After changing variables using 'z equals x minus Mu' and employing the eigenvector expansion of the covariance matrix, we find that the expectation of 'x x transpose' equals 'Mu Mu transpose plus Sigma'.

We define the covariance of a random vector 'x' by subtracting the mean before taking the second moment. For the specific case of a Gaussian distribution, the covariance of 'x' equals Sigma. Therefore, the parameter matrix Sigma, which determines the covariance of 'x' in the Gaussian distribution, is called the covariance matrix.

## Section: Limitations

The Gaussian distribution, while often used as a simple density model, does have certain limitations. For large dimensions (D), the number of free parameters in the distribution can become quite large, making the computational task of manipulating and inverting the large matrices prohibitive. One way to address this problem is to use restricted forms of the covariance matrix, such as diagonal or isotropic covariance matrices. However, these approaches significantly restrict the form of the probability density and limit its ability to capture interesting correlations in the data.

Moreover, the Gaussian distribution is intrinsically unimodal, meaning it has a single maximum, and thus it cannot adequately approximate multimodal distributions. Therefore, the Gaussian distribution can be both too flexible, in terms of having too many parameters, and too limited, in terms of the range of distributions it can represent. Introducing latent variables later on allows us to address both of these issues.

## Section: Conditional Distribution

An important property of a multivariate Gaussian distribution is that if two sets of variables are jointly Gaussian, then the conditional distribution of one set conditioned on the other is also Gaussian. Similarly, the marginal distribution of either set is Gaussian as well.

To illustrate this, suppose 'x' is a D-dimensional vector with a Gaussian distribution, and we partition 'x' into two disjoint subsets, 'x_a' and 'x_b'. We also define corresponding partitions of the mean vector Mu and the covariance matrix Sigma.

In many situations, it is convenient to work with the inverse of the covariance matrix, known as the precision matrix. The precision matrix also has a partitioned form corresponding to the partitioning of the vector 'x'. Some properties of Gaussian distributions are most naturally expressed in terms of the covariance matrix, while others take a simpler form when viewed in terms of the precision matrix. Thus, we use both as needed.

## Section: Partitioned Gaussian Distributions

Let's delve into the concept of partitioned Gaussian distributions. We have a multivariate Gaussian distribution characterized by a mean vector, denoted by Mu, and a covariance matrix, denoted by Sigma.

We can partition these vectors and matrices into smaller components. For instance, the mean vector can be divided into two parts, Mu sub a and Mu sub b, and the covariance matrix can be partitioned into four sub-matrices: Sigma sub aa, Sigma sub ab, Sigma sub ba, and Sigma sub bb.

These partitions help us establish relationships between different parts of a Gaussian distribution. Understanding these relationships is crucial for working with complex models that involve multiple variables and their interactions.

## Section: Conditional Distribution

To better understand partitioned Gaussian distributions, let's explore how to calculate the conditional distribution of one part of the distribution, given another. We use the product rule of probability to evaluate the conditional distribution by fixing one part of the distribution and normalizing the resulting expression.

In mathematical terms, the conditional distribution, p of x sub a given x sub b, can be represented as a quadratic function of x sub a. After some calculations, we find that the covariance of the conditional distribution is given by the inverse of Lambda sub aa, and the mean is a result of a linear function of the observed value x sub b.

This process of 'completing the square'—finding the mean and covariance from the quadratic form—is common when dealing with Gaussian distributions.

## Section: Marginal Distribution

Now let's look at the marginal distribution, which is also Gaussian. We integrate out one part of the joint distribution to focus on the other part. After some calculations, we find that the covariance of the marginal distribution is given by the inverse of a matrix formed from the partitioned precision matrices, and the mean remains the same.

This exploration of partitioned Gaussian distributions, conditional distributions, and marginal distributions provides a deeper understanding of the relationships and dependencies within a Gaussian distribution. It illustrates how different parts of the distribution interact with each other, and how we can manipulate these parts to gain insights into the overall distribution.

## Section: Partitioned Gaussian Distributions

Let's consider a joint Gaussian distribution. The distribution can be partitioned into subcomponents x sub a and x sub b. Our task is to understand the marginal and conditional behavior of these subcomponents.

The partitioned precision matrix of this Gaussian can be represented as a two-by-two block matrix. Think of it as a square split into four smaller squares. The squares on the main diagonal represent the precision of each subcomponent (Lambda sub aa and Lambda sub bb), while the off-diagonal squares represent the precision cross terms (Lambda sub ab and Lambda sub ba).

An interesting aspect of such partitioned Gaussian distributions is that the inverted precision matrix equals the covariance matrix. This shows a direct relationship between the precision and covariance of the subcomponents and their cross terms.

The mean and covariance of a marginal distribution for a subcomponent can be inferred directly from the partitioned covariance matrix. This is intuitive because the marginal distribution, by definition, considers only that subcomponent, ignoring the others.

Now, let's consider a conditional distribution of one subcomponent given the other. The mean of this conditional distribution is a linear function of the other subcomponent, and its covariance can be obtained from the inverted precision of the subcomponent.

## Section: Bayes' Theorem and Linear-Gaussian Models

Bayes' theorem forms the basis for many machine learning algorithms. It allows us to update our beliefs (probability distributions) based on new data. We can also use it to find the marginal and conditional distributions in a Gaussian context.

Consider a Gaussian marginal distribution for the variable x and a Gaussian conditional distribution for variable y given x. If the mean of the conditional distribution is a linear function of x and its variance remains constant, this constitutes a linear-Gaussian model.

The joint distribution of x and y is also Gaussian, and its mean can be derived as a linear function of the parameters governing the means of the marginal and conditional distributions. The precision (inverse covariance) of this joint distribution can be represented as a block matrix, similar to the partitioned precision matrix we discussed earlier.

We can derive the covariance of the joint distribution using the matrix inversion formula. The mean of the joint distribution can also be derived using the parameters of the marginal and conditional distributions and their respective precision matrices.

Finally, the mean and covariance of the marginal distribution for y can be derived using the parameters of the marginal distribution for x and the conditional distribution of y given x.

All these concepts form the basis for a wide range of generative models in machine learning. They give us a powerful mathematical framework to express the relationships between different variables in a probabilistic manner.

## Section: Conditional Distribution in Gaussian Models

We see that the conditional distribution of a variable 'x' given another variable 'y' can be expressed in terms of the partitioned precision matrix. The mean and covariance of the conditional distribution are determined by a set of matrix operations on the precision matrix and other terms.

## Section: Learning and Parametric Distributions

In the context of learning, we look at distributions for discrete variables and the Gaussian distribution for continuous variables. These are examples of parametric distributions, which are governed by a set of adjustable parameters. Estimating suitable values for these parameters based on observed data often involves maximizing the likelihood function.

However, the parametric approach assumes a specific functional form for the distribution, which has its limitations. To address this, we briefly discuss nonparametric density estimation methods. These methods allow the form of the distribution to adapt to the size of the data set, offering more flexibility but potentially being inefficient for large data sets.

## Section: Bernoulli Distribution

For discrete variables, we explore the Bernoulli distribution. This distribution describes the probability of a binary event, such as a coin flip. It is defined by a single parameter Mu, which represents the probability of the event occurring (x equals 1). The Bernoulli distribution provides a concise and elegant way to express the probability of binary outcomes.

## Section: Maximum Likelihood Estimation

We then discuss the concept of maximum likelihood estimation, where the goal is to estimate the parameters of a distribution that maximize the likelihood of observing the given data. We derive the maximum likelihood estimates for the mean and covariance of a multivariate Gaussian distribution.

## Section: Sequential Estimation and Mixtures of Gaussians

Sequential estimation allows data points to be processed one by one, updating the parameter estimates as more data becomes available. This method is particularly useful in real-time applications where data arrives sequentially.

We also examine mixtures of Gaussian distributions, which can capture more complex structures in data sets. By combining several Gaussian distributions, each with its own mean and covariance, we can model data that exhibits multiple modes or clusters.

## Section: Example - Old Faithful Geyser Data Set

Let's consider an example to illustrate these concepts. We examine the Old Faithful geyser data set, which measures the duration of eruptions and the time until the next eruption. A simple Gaussian distribution fails to capture the structure of this data, as it forms two distinct clusters. However, using a mixture of two Gaussian distributions, we can effectively model this data. This example demonstrates the power and flexibility of Gaussian mixtures in modeling complex, multimodal distributions.

## Section: Model Selection

The goal is to select the model that best captures the underlying structure of the data. Depending on the specific characteristics of the data set, this might be a simple Gaussian, a mixture of Gaussians, or a nonparametric model. By combining these concepts, we can build robust and flexible models that handle a wide range of scenarios.

## Section: Mixture of Gaussians

Let's delve deeper into Gaussian mixture models. A Gaussian mixture model is a probabilistic model that combines multiple Gaussian distributions, often referred to as "components." Each component is defined by its own mean and covariance. The overall mixture model is a weighted sum of these components, with the weights known as "mixing coefficients." These coefficients are non-negative and sum to one.

The combined effect of the individual Gaussian components creates the overall distribution of the mixture model. This results in a more complex probability density function that captures the contribution from each component. Gaussian mixture models are valuable because they can approximate almost any continuous distribution with sufficient Gaussian components and appropriate adjustments to their means, covariances, and mixing coefficients.

The probability density function for a mixture of Gaussians is given by the sum of the weighted Gaussian densities, each parameterized by its mean and covariance. The mixing coefficients also have a probabilistic interpretation, representing the prior probability of a data point belonging to a specific Gaussian component.

This probabilistic interpretation is further highlighted when considering the posterior probabilities or "responsibilities" of the components for each data point. These responsibilities indicate the probability that a data point belongs to a particular Gaussian component, given the data point itself.

However, this flexibility comes with increased complexity. Finding the maximum likelihood estimates for the parameters of a Gaussian mixture model is more challenging than for a single Gaussian. The summation inside the logarithm in the likelihood function prevents a simple closed-form solution. Instead, iterative numerical optimization techniques, such as the expectation-maximization algorithm, are used to find the maximum likelihood estimates.

By understanding these concepts and methods, we can effectively utilize Gaussian mixture models to capture complex data structures and build more accurate probabilistic models.

## Section: Periodic Variables

Periodic variables exhibit a pattern of repeating values over a specific period. Examples include wind direction and calendar time. Conventional distributions, such as the Gaussian distribution, are not suitable for these types of variables due to their inherent periodicity.

Consider measuring wind direction. Applying a Gaussian distribution to this data would produce results heavily dependent on the arbitrary choice of origin. To address this, we view the data differently. We represent observations as points on a unit circle, using two-dimensional unit vectors. By calculating the mean of these vectors instead of the angles themselves, we ensure that our measure of central tendency is not affected by the origin of our angular coordinate system.

## Section: Von Mises Distribution

To address the issue of periodic variables, we introduce the von Mises distribution. This distribution is essentially the circular equivalent of the Gaussian distribution, designed to handle data on a circular domain. It ensures that the probability density of a variable is non-negative, integrates to one, and is periodic, meaning the density is the same for every complete rotation.

Instead of dealing directly with the angular variable, we represent the values in Cartesian coordinates as points on a unit circle. We then calculate the mean of these Cartesian representations. This approach respects the circular nature of periodic variables and avoids the problems that arise when a Gaussian distribution is applied to such data.

We can also derive the von Mises distribution by conditioning a two-dimensional Gaussian on the unit circle. This concept is illustrated with contour plots of a two-dimensional Gaussian and the unit circle on which the periodic variable lies.

## Section: Introduction to Two-Dimensional Gaussian Distributions

We begin by focusing on the two-dimensional Gaussian distribution, characterized by a mean vector and a covariance matrix. The mean vector indicates the center of the distribution, while the covariance matrix provides information about the spread and orientation.

When the covariance matrix is proportional to the identity matrix, the distribution becomes isotropic. This means the distribution's spread is equal in all directions, forming circular contours of constant probability density.

To understand the behavior of this distribution along a fixed radius, we transition from Cartesian to polar coordinates. A circle of fixed radius in the Cartesian plane becomes a straight line in the polar coordinate system.

## Section: Transformation from Cartesian to Polar Coordinates

We begin by transforming the coordinates from Cartesian to polar, replacing x1 and x2 with r (radius) and θ (angle), respectively. We also express the mean in polar coordinates, resulting in equations for x1 (r cosine theta) and x2 (r sine theta).

Next, we substitute these transformations into the two-dimensional Gaussian distribution and condition on the unit circle (r equals 1), focusing on the dependence on θ only.

This transformation leads to an expression involving the cosine of the difference between θ and θ0, where θ0 is the mean of the distribution in polar coordinates. This result is derived using trigonometric identities, including the Pythagorean identity and the formula for cosine of a difference.

## Section: The Von Mises Distribution

Our final expression describes the distribution of θ along the unit circle, known as the von Mises distribution or the circular normal. It has two parameters: the mean direction (θ0) and the concentration parameter (m). The concentration parameter is analogous to the inverse variance or precision for the Gaussian distribution.

The von Mises distribution is normalized using a special function, the zeroth-order modified Bessel function of the first kind, denoted as I0(m). This function is defined by an integral involving the exponential of m times cosine theta.

## Section: Maximum Likelihood Estimators for the Von Mises Distribution

Next, we discuss the maximum likelihood estimators for the parameters of the von Mises distribution, θ0 and m. These estimators are found by maximizing the log-likelihood function with respect to the parameters.

The maximum likelihood estimator for θ0 is determined by setting the derivative of the log-likelihood function with respect to θ0 to zero. This results in an equation that can be solved using a trigonometric identity, yielding a result equivalent to the mean of the observations in a two-dimensional Cartesian space.

Similarly, maximizing the log-likelihood function with respect to m yields an equation involving a function A(m), the ratio of the first-order and zeroth-order modified Bessel functions. A(m) can be inverted numerically to find the maximum likelihood estimator for m.

## Section: The von Mises Distribution

The von Mises distribution is unimodal, meaning it has only one peak. This can be a limitation when modeling periodic variables that exhibit multimodality, or multiple peaks. One solution is to form mixtures of von Mises distributions, which can handle multimodality.

There are also other techniques for constructing periodic distributions, such as using histograms or wrapping distributions over the real axis onto the unit circle. However, these alternatives can lead to more complex forms of distribution and may not offer significant advantages over the von Mises distribution.

## Section: Exponential Family Distributions

The exponential family of distributions is a broad class that includes many of the distributions we have studied so far. Distributions in this family are characterized by a specific form involving the exponential function.

The Bernoulli distribution, for example, can be rewritten in the form of an exponential family distribution. This involves expressing the Bernoulli distribution as the exponential of the logarithm, and then identifying the natural parameters and other components of the standard representation of an exponential family distribution.

In the case of the Bernoulli distribution, the natural parameter is the log odds ratio, and the function of the data is simply the data itself. The sigmoid function is introduced as the inverse of the log odds ratio, allowing us to express the Bernoulli distribution in terms of the sigmoid function.

## Section: Mathematical Equations and Density Modelling

Let's now delve into the application of mathematical equations in the context of distributions and density modeling. This includes concepts like the exponential family distribution, maximum likelihood estimation, sufficient statistics, and nonparametric methods such as histograms.

We start by exploring the equation "one minus sigma of eta equals sigma of negative eta." This can be easily proven from another equation that involves comparing terms and identifying sub-equations: u of x equals x, h of x equals 1, and g of eta equals sigma of negative eta.

Next, we examine the multinomial distribution for a single observation, denoted as vector x. This distribution can be expressed as the product of mu sub k raised to the power of x sub k, summed from k equals 1 to M. This formulation can be expanded to an exponential form involving the natural log of mu sub k and the transpose of vector x.

We can write this multinomial distribution in a standard representation where the parameters eta sub k are defined as the natural log of mu sub k. However, these parameters are not independent because the parameters mu sub k are subject to the constraint that their sum equals 1.

## Section: The Softmax Function and Gaussian Distribution

We also discuss the softmax function, or the normalized exponential, which is used in various machine learning algorithms. Additionally, we delve into the Gaussian distribution for univariate cases, exploring its properties and applications.

## Section: Maximum Likelihood Estimation and Sufficient Statistics

In terms of theorems and derivations, we discuss the maximum likelihood estimation technique and the concept of sufficient statistics. A sufficient statistic for a distribution is a function of the data that captures all the information needed to estimate a parameter. This is powerful because it means we do not need to store the entire data set, only the value of the sufficient statistic.

In the large data set limit, the maximum likelihood estimator will equal the true value of the parameter vector.

## Section: Nonparametric Methods for Density Estimation

We then turn our attention to nonparametric methods for density estimation, starting with histograms. Histograms partition a continuous variable into distinct bins and count the number of observations in each bin.

We walk through an example of histogram density estimation, observing how the choice of bin width significantly affects the final density model. Too small a bin width captures noise and non-representative fluctuations, while too large a bin width results in a model that fails to capture the true underlying distribution. An optimal bin width lies somewhere in between these extremes.

Despite its simplicity, the histogram approach has limitations, especially in high-dimensional data scenarios due to the curse of dimensionality. This term refers to the exponential increase in complexity with each additional dimension in the data.

## Section: Local Density Estimation

In this part of our discussion, we explore the concept of local density estimation. When estimating the probability density at a certain location, we should focus on data points that lie within a local neighborhood of that point. This concept of locality typically involves using a distance measure, such as Euclidean distance.

Understanding these concepts helps us build robust and flexible models for a wide range of scenarios, allowing for effective density estimation and probabilistic modeling.

## Section: Histograms and Smoothing

In the context of histograms, the neighborhood property is defined by bins, and there's a natural 'smoothing' parameter that describes the spatial extent of the local region, or the bin width. For good results, the smoothing parameter should be neither too large nor too small. This balancing act is similar to choosing model complexity in polynomial regression, where the degree of the polynomial or the value of the regularization parameter is optimal at an intermediate value. With these insights, we delve into two widely used nonparametric techniques for density estimation: kernel estimators and nearest neighbors.

## Section: Kernel Densities

Imagine we are drawing observations from an unknown probability density in a Euclidean space. We want to estimate this density at a particular point. From our prior discussion about locality, let's consider a small region containing this point. The probability mass associated with this region is the integral of the density over this region.

Suppose we've collected a dataset consisting of N observations drawn from our unknown density. Each data point has a probability of falling within our region, so the total number of points that lie inside this region follows a binomial distribution. For large N, this distribution is sharply peaked around the mean, so the number of points is approximately the total number of observations times the probability.

If we also assume that our region is sufficiently small so that the probability density is roughly constant over the region, then the probability is approximately the density times the volume of the region. Combining these results, we get our density estimate as the number of points divided by the product of the number of observations and the volume of the region.

However, this density estimate relies on two contradictory assumptions: that the region is sufficiently small for the density to be approximately constant over it, and yet sufficiently large for the number of points falling inside the region to be enough for the binomial distribution to be sharply peaked.

## Section: Nearest Neighbors

One issue with the kernel approach to density estimation is that the parameter governing the kernel width is fixed for all kernels. In regions of high data density, a large value of this parameter may lead to over-smoothing and a loss of crucial structure in the data. However, reducing the parameter may lead to noisy estimates elsewhere where the data density is smaller. Thus, the optimal choice for the kernel width may be dependent on the location within the data space. This issue is addressed by nearest-neighbor methods for density estimation.

In nearest-neighbor methods, we fix the number of points and use the data to find an appropriate value for the volume of the region. We consider a small sphere centered on the point at which we wish to estimate the density. We allow the radius of the sphere to grow until it contains precisely a fixed number of data points. The estimate of the density is then given by the number of points divided by the product of the number of observations and the volume of the resulting sphere. This technique is known as K-nearest neighbors.

Again, there is an optimal choice for K that is neither too large nor too small. Note that the model produced by K-nearest neighbors is not a true density model because the integral over all space diverges.

By applying the K-nearest-neighbor density estimation technique to each class separately and then making use of Bayes' theorem, we can extend this technique to the problem of classification. This approach simply requires storing the training set, which is both its strength and its weakness because the computational cost of evaluating the density grows linearly with the size of the data set.

In conclusion, both kernel estimators and nearest neighbors provide nonparametric techniques for density estimation. Both methods rely on the idea of considering local neighborhoods of data points and have parameters that control the degree of smoothing. Choosing the optimal value for these parameters is crucial for obtaining good results.

## Section: Binomial Distribution and its Properties

Let's talk about a key concept in probability and statistics: the binomial distribution. Consider a set of binary variables, each of which can take on one of two values, such as 0 or 1. The distribution of the sum of these variables is known as the binomial distribution.

The binomial distribution features prominently in statistical models, as it quantifies the number of successes in a sequence of independent and identically distributed Bernoulli trials. The counts of successes in a fixed number of trials form a binomial distribution.

The mean and variance of the binomial distribution are simple to compute. The mean is the product of the number of trials and the probability of success, also known as the expectation. The variance is the product of the number of trials, the probability of success, and the probability of failure. These are straightforward results that come from the properties of independent events, where the mean of the sum is the sum of the means, and the variance of the sum is the sum of the variances.

## Section: Multinomial Distribution

The multinomial distribution generalizes the binomial distribution to cases where each trial can result in one of several possible outcomes, rather than just two. While the binomial distribution counts the number of successes from binary trials, the multinomial distribution counts the number of outcomes in multi-category trials.

Practically, the multinomial distribution can describe quantities that can take one of several possible values. A common representation is the 1-of-K scheme, also known as "one-hot encoding," where the variable is represented by a K-dimensional vector. For example, if a variable can take six states, a particular observation of the variable would be represented by a six-dimensional vector, with one element equal to 1 and all other elements equal to 0.

The mean of the multinomial distribution is simply the probability of each outcome. These probabilities can be calculated as the number of times each outcome occurs divided by the total number of observations.

## Section: K-Nearest Neighbour Classification

The k-nearest neighbour classifier is a simple yet effective method for classification problems. This method classifies a new point based on the class membership of its 'K' nearest neighboring points from the training dataset. The 'K' closest points are determined based on some distance metric, and the new point is classified according to the majority class membership among these points.

An interesting property of the nearest-neighbour classifier, particularly when 'K' is 1, is that as the number of training points approaches infinity, the error rate of this classifier is never more than twice the minimum achievable error rate of an optimal classifier. This optimal classifier is one that uses the true underlying class distributions. This result illustrates the strength of this simple classification technique.

## Section: The Multivariate Gaussian

The Gaussian, or normal distribution, is a widely used model for continuous variables. For a single variable, the Gaussian distribution is defined by its mean and variance. For a D-dimensional vector, the multivariate Gaussian distribution is described by a D-dimensional mean vector and a D by D covariance matrix.

The Gaussian distribution is popular due to its desirable properties, including the fact that it can be completely described by its mean and variance, and its shape is symmetric and bell-shaped. Moreover, under certain conditions, the Central Limit Theorem states that the sum of a large number of independent and identically distributed random variables, irrespective of their individual distributions, tends towards a Gaussian distribution. This property makes the Gaussian distribution a natural choice for many statistical models.

## Section: The Gaussian Distribution and the Central Limit Theorem

The Gaussian distribution is crucial in statistics for two main reasons. Firstly, when dealing with a single variable, whether real or multivariate, the Gaussian distribution maximizes entropy. Secondly, the Gaussian distribution arises naturally when considering the sum of multiple random variables. The Central Limit Theorem demonstrates that under certain conditions, the sum of a set of random variables, each uniformly distributed over an interval, will increasingly approximate a Gaussian distribution as the number of terms in the sum increases. This concept can be visually illustrated with a histogram plot showing the distribution of the mean of ten uniformly distributed random variables.

Additionally, the Gaussian distribution has many important analytical properties. To explore these, familiarity with various matrix identities is necessary.

## Section: Geometry of the Gaussian

The Gaussian distribution can be characterized geometrically by the quadratic form of the difference between a variable 'x' and the mean of the distribution, denoted as Mu. This difference, referred to as the Mahalanobis distance, becomes the Euclidean distance when the covariance matrix, denoted as Sigma, is the identity matrix. The Gaussian distribution remains constant for surfaces in 'x'-space where this quadratic form is constant.

The covariance matrix Sigma is symmetric, as any antisymmetric components would disappear from the quadratic form. As a result, we can examine the eigenvector equation for the covariance matrix. The covariance matrix Sigma can be expressed as an expansion in terms of its eigenvectors, and the inverse covariance matrix can be similarly expressed.

The quadratic form then becomes the sum of the squares of the new coordinates over their corresponding eigenvalues. These new coordinates, denoted as y sub i, form a new coordinate system, defined by the orthonormal vectors that are shifted and rotated with respect to the original x sub i coordinates.

The Gaussian density remains constant on surfaces where this quadratic form is constant. If all eigenvalues are positive, these surfaces represent ellipsoids, with their centers at Mu and their axes oriented along the eigenvectors, with scaling factors in the directions of the axes given by the square root of the eigenvalues.

## Section: Positive Definite and Positive Semidefinite Matrices

For the covariance matrix to be positive definite, all its eigenvalues must be strictly positive. This ensures the matrix is invertible and that the quadratic form used to describe the Gaussian distribution is strictly convex. If all eigenvalues are non-negative, the covariance matrix is termed positive semidefinite. This still allows the matrix to be used in various statistical and machine learning applications, though it may not be invertible.

## Section: Gaussian Distribution in New Coordinates

In the transformed coordinate system defined by the eigenvectors of the covariance matrix, the Gaussian distribution can be expressed as a product of independent univariate Gaussian distributions. This means each new coordinate, corresponding to an eigenvector, has its own Gaussian distribution. The eigenvectors effectively define a new set of shifted and rotated coordinates in which the joint probability distribution factorizes into independent distributions. This property simplifies the analysis and manipulation of the Gaussian distribution, especially in high-dimensional spaces.

## Section: Importance of the Gaussian Distribution

This comprehensive exploration of the Gaussian distribution and its properties highlights why it is so prevalent in statistics and data analysis. The Gaussian distribution's mathematical elegance and its appearance in various real-world phenomena make it a fundamental concept for understanding and interpreting data. Its properties, such as being fully characterized by its mean and covariance, and its natural emergence in the context of the Central Limit Theorem, underscore its critical role in probabilistic modeling and statistical inference.

By understanding these aspects of the Gaussian distribution, one gains deeper insights into its applications and the reasoning behind its widespread use in statistical modeling and machine learning.

## Chapter Summary: Standard Distributions

### Key Points:

1. **Standard Distributions Overview**:
   - The chapter covers specific probability distributions and their properties, which serve as building blocks for more complex models.
   - Density estimation is a key application but is inherently ill-posed, linking to model selection in machine learning.

2. **Moments of Gaussian Distribution**:
   - The mean (Mu) and covariance (Sigma) of the Gaussian distribution are discussed.
   - Expectation and second-order moments are calculated, showing that Mu is the mean and Sigma is the covariance matrix.

3. **Limitations of Gaussian Distribution**:
   - In high dimensions, the number of parameters in the Gaussian distribution can be computationally prohibitive.
   - Gaussian distributions are unimodal and can't represent multimodal distributions effectively.

4. **Conditional and Marginal Distributions**:
   - Properties of partitioned multivariate Gaussian distributions are explored.
   - Conditional distributions of partitioned subsets remain Gaussian, and the precision matrix offers useful properties for these calculations.

5. **Bayes' Theorem and Linear-Gaussian Models**:
   - Bayes' theorem is used to update beliefs based on new data.
   - Linear-Gaussian models are described, including joint, marginal, and conditional distributions.

6. **Mixture of Gaussians**:
   - Gaussian mixture models combine multiple Gaussian distributions to capture more complex data structures.
   - Maximum likelihood estimation for these models is discussed, typically requiring iterative optimization like the expectation-maximization algorithm.

7. **Periodic Variables and Von Mises Distribution**:
   - Gaussian distributions are unsuitable for periodic data. The von Mises distribution, a circular analog of the Gaussian, is introduced.
   - Maximum likelihood estimation for the von Mises distribution is outlined.

8. **Exponential Family Distributions**:
   - The exponential family of distributions is discussed, which includes the Bernoulli and multinomial distributions.
   - The softmax function and Gaussian distribution are covered within this framework.

9. **Nonparametric Density Estimation**:
   - Histograms, kernel density estimators, and nearest-neighbor methods are discussed as nonparametric techniques.
   - These methods rely on local neighborhoods of data points and have parameters that control smoothing.

10. **Binomial and Multinomial Distributions**:
    - The binomial distribution describes the number of successes in binary trials.
    - The multinomial distribution generalizes this to multiple outcomes, useful for multi-category trials and one-hot encoding.

11. **K-Nearest Neighbour Classification**:
    - K-nearest neighbor (KNN) classifier uses the nearest training points to classify new points.
    - The error rate of KNN approaches the optimal classifier's error rate as the number of training points increases.

12. **Multivariate Gaussian and Central Limit Theorem**:
    - The Gaussian distribution is crucial due to maximizing entropy and approximating sums of random variables (Central Limit Theorem).
    - Geometric properties of the Gaussian involve eigenvector decomposition of the covariance matrix, leading to ellipsoidal contours.

13. **Positive Definite and Positive Semidefinite Matrices**:
    - Covariance matrices must be positive definite for invertibility.
    - Positive semidefinite matrices are also useful but may not be invertible.

14. **Gaussian Distribution in New Coordinates**:
    - In an eigenvector-defined coordinate system, the Gaussian distribution factorizes into independent univariate distributions.

15. **Importance of Gaussian Distribution**:
    - The Gaussian distribution's prevalence is due to its mathematical properties and natural emergence in many real-world scenarios.
    - Understanding its properties is fundamental for probabilistic modeling and statistical inference.

## Chapter: Standard Distributions

In this chapter, we'll explore specific examples of probability distributions and their properties. These distributions are of interest not only for their own sake but also as building blocks for more complex models.

A key role for the distributions discussed here is to model the probability distribution of a random variable, given a finite set of observations. This problem is known as density estimation. However, the problem of density estimation is fundamentally ill-posed because there are infinitely many probability distributions that could have given rise to the observed finite data set. The issue of choosing an appropriate distribution connects to the problem of model selection, which is a central issue in machine learning.

## Section: Moments

We will now examine the moments of the Gaussian distribution and provide an interpretation of the parameters Mu and Sigma. The expectation of 'x' under the Gaussian distribution is given by an integral that involves an exponential term and the variable 'x'. In this integral, we change variables using 'z equals x minus Mu'. As the exponent is an even function of the components of 'z', and because the integrals over these components are taken over the full range of real numbers, the term in 'z' in the factor '(z plus Mu)' will vanish by symmetry. Therefore, the expectation of 'x' is equal to Mu, so we refer to Mu as the mean of the Gaussian distribution.

We also consider second-order moments of the Gaussian. For the multivariate Gaussian, there are D-squared second-order moments given by the expectation of 'x sub i x sub j', which we can group together to form the matrix 'expectation of x times x transpose'. The expectation of 'x times x transpose' can be written as another integral involving an exponential term, 'x' and 'x transpose'. After changing variables using 'z equals x minus Mu' and using the eigenvector expansion of the covariance matrix, we obtain that the expectation of 'x times x transpose' is equal to 'Mu times Mu transpose plus Sigma'.

We define the covariance of a random vector 'x' by subtracting the mean before taking the second moment. For the specific case of a Gaussian distribution, we find that the covariance of 'x' is equal to Sigma. Therefore, the parameter matrix Sigma, which governs the covariance of 'x' under the Gaussian distribution, is called the covariance matrix.

## Section: Limitations

It's important to note that the Gaussian distribution, while often used as a simple density model, does have certain limitations. The number of free parameters in the distribution can become quite large for large D, and the computational task of manipulating and inverting the large matrices can become prohibitive. One way to address this problem is to use restricted forms of the covariance matrix, such as diagonal or isotropic covariance matrices. However, these approaches greatly restrict the form of the probability density and limit its ability to capture interesting correlations in the data.

Moreover, the Gaussian distribution is intrinsically unimodal, meaning it has a single maximum, and so it is unable to provide a good approximation to multimodal distributions. Thus, the Gaussian distribution can be both too flexible, in the sense of having too many parameters, and too limited in the range of distributions that it can adequately represent. Later, we will see that the introduction of latent variables allows both of these problems to be addressed.

## Section: Conditional Distribution

An important property of a multivariate Gaussian distribution is that if two sets of variables are jointly Gaussian, then the conditional distribution of one set conditioned on the other is again Gaussian. Similarly, the marginal distribution of either set is also Gaussian.

To illustrate this, suppose that 'x' is a D-dimensional vector with a Gaussian distribution and we partition 'x' into two disjoint subsets 'x sub a' and 'x sub b'. We also define corresponding partitions of the mean vector Mu and of the covariance matrix Sigma.

In many situations, it will be convenient to work with the inverse of the covariance matrix, which is known as the precision matrix. The precision matrix also has a partitioned form corresponding to the partitioning of the vector 'x'. Some properties of Gaussian distributions are most naturally expressed in terms of the covariance, whereas others take a simpler form when viewed in terms of the precision. So, we will use both as needed.

## Section: Partitioned Gaussian Distributions

Let's delve into the concept of partitioned Gaussian distributions. We are provided with a multivariate Gaussian distribution with a mean vector, denoted by the bold letter mu, and a covariance matrix, denoted by the bold symbol Sigma.

We can partition these vectors and matrices into smaller components. For instance, the mean vector can be divided into two parts, mu sub a and mu sub b, and the covariance matrix can be partitioned into four sub-matrices: Sigma sub aa, Sigma sub ab, Sigma sub ba, and Sigma sub bb.

These partitions help us establish relationships between different parts of a Gaussian distribution. For instance, sub-matrices with the same subscript, like Sigma sub aa and Lambda sub aa, are symmetric to each other, i.e., they mirror each other across the main diagonal. However, it's important to note that Lambda sub aa is not simply the inverse of Sigma sub aa.

## Section: Conditional Distribution

To better understand partitioned Gaussian distributions, let's explore how to calculate the conditional distribution of one part of the distribution, given another. We use the product rule of probability to evaluate the conditional distribution by fixing one part of the distribution and normalizing the resulting expression.

In mathematical terms, the conditional distribution, p of x sub a given x sub b, can be represented as a quadratic function of x sub a. After some calculations, we find that the covariance of the conditional distribution is given by the inverse of Lambda sub aa, and the mean is a result of a linear function of the observed value x sub b.

This process of 'completing the square'—finding the mean and covariance from the quadratic form—is common when dealing with Gaussian distributions.

## Section: Marginal Distribution

Now let's look at the marginal distribution, which is also Gaussian. We integrate out one part of the joint distribution to focus on the other part. After some calculations, we find that the covariance of the marginal distribution is given by the inverse of a matrix formed from the partitioned precision matrices, and the mean remains the same.

This exploration of partitioned Gaussian distributions, conditional distributions, and marginal distributions provides a deeper understanding of the relationships and dependencies within a Gaussian distribution. It illustrates how different parts of the distribution interact with each other, and how we can manipulate these parts to gain insights into the overall distribution.

## Section: Bayes' Theorem and Linear-Gaussian Models

Bayes' theorem forms the basis for many machine learning algorithms. It allows us to update our beliefs (probability distributions) based on new data. We can also use it to find the marginal and conditional distributions in a Gaussian context.

Consider a Gaussian marginal distribution for the variable x and a Gaussian conditional distribution for variable y given x. If the mean of the conditional distribution is a linear function of x and its variance remains constant, this constitutes a linear-Gaussian model.

The joint distribution of x and y is also Gaussian, and its mean can be derived as a linear function of the parameters governing the means of the marginal and conditional distributions. The precision (inverse covariance) of this joint distribution can be represented as a block matrix, similar to the partitioned precision matrix we discussed earlier.

We can derive the covariance of the joint distribution using the matrix inversion formula. The mean of the joint distribution can also be derived using the parameters of the marginal and conditional distributions and their respective precision matrices.

Finally, the mean and covariance of the marginal distribution for y can be derived using the parameters of the marginal distribution for x and the conditional distribution of y given x.

All these concepts form the basis for a wide range of generative models in machine learning. They give us a powerful mathematical framework to express the relationships between different variables in a probabilistic manner.

## Section: Mixture of Gaussians

Let's talk about Gaussian mixture models. A Gaussian mixture model is a probabilistic model that uses a combination of Gaussian distributions. Each of these Gaussian distributions, which are often called "components" of the mixture, is defined by its own mean and covariance. The overall mixture model is a weighted sum of these components. The weights, also known as "mixing coefficients", satisfy the constraints of probabilities, i.e., they are non-negative and sum to one.

The combined effect of the individual Gaussian components creates the overall distribution of the mixture model. This can result in a more complex probability density function that captures the contribution from each individual component. This is why Gaussian mixture models are useful: they can approximate almost any continuous distribution to arbitrary accuracy by using a sufficient number of Gaussians and adjusting their means, covariances, and the mixing coefficients.

The probability density function for a mixture of Gaussians is given by the sum of the weighted Gaussian densities, where each Gaussian density is parameterized by its mean and covariance.

Interestingly, these mixing coefficients also have a probabilistic interpretation. They can be seen as the prior probability of a data point belonging to a particular Gaussian component. This probabilistic interpretation becomes more significant when we consider the posterior probabilities or "responsibilities" of the components for each data point, given by Bayes' theorem. These responsibilities indicate the probability that a data point 'x' belongs to a particular Gaussian component, given the data point itself.

However, this flexibility comes with a cost in terms of complexity. For example, finding the maximum likelihood estimates for the parameters of a Gaussian mixture model is a more complex task than for a single Gaussian. It's because of the summation inside the logarithm in the likelihood function. As a result, we don't have a simple closed-form solution anymore. But we have iterative numerical optimization techniques or the expectation-maximization algorithm at our disposal to find the maximum likelihood estimates.

## Section: Periodic Variables

Let's shift our focus to a different topic now: Periodic variables. These are variables that exhibit a pattern of repeating values over a specific period. For instance, wind direction and calendar time are periodic variables. It's important to note that conventional distributions, like the Gaussian, are not suitable for these types of variables due to their inherent periodicity.

Take the example of measuring wind direction. If you were to apply a Gaussian distribution to this, the results would heavily depend on your arbitrary choice of origin. To address this, we look at the data in a different way. Think of the observations as points on a unit circle, represented by two-dimensional unit vectors. Then, we can calculate the mean of these vectors instead of the angles themselves. This ensures that our measure of central tendency, or the mean, is not affected by where we choose to put the origin of our angular coordinate.

## Section: Von Mises Distribution

To further address the issue of periodic variables, we introduce a new distribution: the von Mises distribution. It's essentially a circular equivalent to the Gaussian distribution, designed to handle data on a circular domain. It ensures that the probability density of a variable is non-negative, integrates to one, and is periodic, i.e., the density is the same for every complete rotation.

Instead of dealing directly with the angular variable, we can represent the values in Cartesian coordinates as points on a unit circle. Then, we can calculate the mean of these Cartesian representations. This approach allows us to create a distribution that respects the circular nature of periodic variables, avoiding the problems we'd face if we naively applied a Gaussian distribution to such data.

We can also derive the von Mises distribution by conditioning a two-dimensional Gaussian on the unit circle. This concept is illustrated in the provided figures, which show the contour plot of a two-dimensional Gaussian and the unit circle on which the periodic variable lies.

## Section: Introduction to Two-dimensional Gaussian Distributions

We begin our discussion focusing on the two-dimensional Gaussian distribution. This distribution is characterized by a mean vector and a covariance matrix. The mean vector indicates the center of the distribution, while the covariance matrix provides information about the spread and orientation.

In the case where the covariance matrix is proportional to the identity matrix, the distribution becomes isotropic. This means the spread of the distribution is equal in all directions, creating contours of constant probability density that form circles.

To understand the behavior of this distribution along a fixed radius, we transition from Cartesian to polar coordinates. A circle of fixed radius in the Cartesian plane becomes a straight line in the polar coordinate system.

## Section: Transformation from Cartesian to Polar Coordinates

We start by transforming the coordinates from Cartesian to polar, replacing x1 and x2 with r (radius) and θ (angle), respectively. We also express the mean in polar coordinates, which gives us two equations, one for x1 (or r cosine theta) and another for x2 (or r sine theta).

Next, we substitute these transformations into the two-dimensional Gaussian distribution. We then condition on the unit circle, r equals 1, to focus on the dependence on θ only.

This transformation leads us to a result that involves cosine of the difference between θ and θ0, where θ0 is the mean of the distribution in polar coordinates. This result is derived using trigonometric identities, including the Pythagorean identity and the formula for cosine of a difference.

## Section: The von Mises Distribution

Our final expression describes the distribution of θ along the unit circle, and this distribution is known as the von Mises distribution or the circular normal. It has two parameters: the mean direction, θ0, and the concentration parameter, m. The concentration parameter is analogous to the inverse variance or the precision for the Gaussian.

The von Mises distribution is normalized using a special function, the zeroth-order modified Bessel function of the first kind, denoted as I0(m). This function is defined by an integral involving the exponential of m times cosine theta.

## Section: Maximum Likelihood Estimators for the von Mises Distribution

Next, we discuss the maximum likelihood estimators for the parameters of the von Mises distribution, θ0 and m. The maximum likelihood estimators are found by maximizing the log likelihood function with respect to the parameters.

The maximum likelihood estimator for θ0 is found by setting the derivative of the log likelihood function with respect to θ0 equal to zero. This results in an equation that can be solved using a trigonometric identity, yielding a result that is equivalent to the mean of the observations viewed in a two-dimensional Cartesian space.

Similarly, maximizing the log likelihood function with respect to m yields an equation in terms of a function A(m), which is the ratio of the first-order and zeroth-order modified Bessel functions. A(m) can be inverted numerically to find the maximum likelihood estimator for m.

In our discussion, we've covered multiple mathematical concepts, including convolutions, conditional distributions, parametric distributions, and more. Let's take a moment to dive deeper into these topics.

We discovered that the mean of the convolution of two Gaussians is the sum of their means, and the covariance of the convolution is the sum of their covariances. This gives us a helpful way to understand how these distributions interact with each other.

Next, we explored the concept of conditional distributions, specifically p(x | y), or the probability of x given y. We saw that these distributions could be expressed in terms of the partitioned precision matrix. In particular, we found that the conditional distribution p(x | y) has its mean and covariance determined by a set of matrix operations on the precision matrix and other terms.

Moving onto the topic of learning, we looked at distributions for discrete variables and the Gaussian distribution for continuous variables. We found that these are examples of parametric distributions, which are governed by a set of adjustable parameters. We discussed how to estimate suitable values for these parameters based on observed data, focusing on maximizing the likelihood function.

Then, we considered the limitations of the parametric approach, which assumes a specific functional form for the distribution. We briefly discussed nonparametric density estimation methods, which allow the form of the distribution to depend on the size of the data set. Though they can be more flexible, nonparametric methods can also be inefficient for large data sets.

We then moved on to the topic of discrete variables, particularly the Bernoulli distribution. We saw that the probability distribution over x can be written in terms of the parameter μ, which represents the probability of x equals 1. The Bernoulli distribution expresses the probability of a binary event, such as a coin flip, in a concise and elegant way.

Following this, we discussed the concept of maximum likelihood, where we aim to estimate the parameters of a distribution that maximize the likelihood of observing our data. We then derived the maximum likelihood estimate for the mean and covariance of a multivariate Gaussian distribution.

Finally, we examined the concept of sequential estimation, which allows data points to be processed one by one, and mixtures of Gaussian distributions, which can capture more complex structures in data sets.

Each of these topics offers a unique perspective on understanding and modeling data. By combining these concepts, we can build robust and flexible models that can handle a wide range of scenarios. As we continue to explore these topics, we'll develop a deeper understanding of the mathematical foundations that underpin machine learning and data analysis.

Let's now consider an example to illustrate these concepts. We'll look at the Old Faithful geyser data set, which measures the duration of eruptions and the time until the next eruption. A simple Gaussian distribution fails to capture the structure of this data, as it forms two distinct clusters. However, by using a mixture of two Gaussian distributions, we can effectively model this data. This demonstrates the power and flexibility of Gaussian mixtures in modeling complex, multimodal distributions.

In general, the goal is to select the model that best captures the underlying structure of the data. Whether this is a simple Gaussian, a mixture of Gaussians, or a nonparametric model will depend on the specific characteristics of the data set.

## Section: Extending the von Mises Distribution

The von Mises distribution is unimodal, meaning it has only one peak. This can be a limitation when modeling periodic variables that exhibit multimodality, or multiple peaks. One solution is to form mixtures of von Mises distributions, which can handle multimodality.

There are also other techniques for constructing periodic distributions, such as using histograms or wrapping distributions over the real axis onto the unit circle. However, these alternatives can lead to more complex forms of distribution and may not offer significant advantages over the von Mises distribution.

## Section: Exponential Family Distributions

The exponential family of distributions is a broad class that includes many of the distributions we have studied so far. Distributions in this family are characterized by a specific form involving the exponential function.

The Bernoulli distribution, for example, can be rewritten in the form of an exponential family distribution. This involves expressing the Bernoulli distribution as the exponential of the logarithm, and then identifying the natural parameters and other components of the standard representation of an exponential family distribution.

In the case of the Bernoulli distribution, the natural parameter is the log odds ratio, and the function of the data is simply the data itself. The sigmoid function is introduced as the inverse of the log odds ratio, allowing us to express the Bernoulli distribution in terms of the sigmoid function.

We then delve into the world of mathematical equations and their application in the context of mathematical distributions and density modeling. Our discussion includes concepts like the exponential family distribution, maximum likelihood estimation, sufficient statistics, and nonparametric methods including histograms.

## Section: Multinomial Distribution

Next, we examine the multinomial distribution for a single observation denoted as vector x. This equation involves the product of the probabilities of observing each category, raised to the power of the observed counts. This can be rewritten using exponential functions and logarithms to align with the exponential family form.

The parameters of the multinomial distribution are subject to constraints, as the probabilities must sum to one. This introduces dependencies among the parameters, which must be accounted for in the analysis.

## Section: The Softmax Function

We also discuss the softmax function, or the normalized exponential, which is used to convert raw scores into probabilities. This function is particularly useful in classification problems involving multiple categories.

## Section: Maximum Likelihood Estimation

In terms of theorems and derivations, we discuss the maximum likelihood estimation technique and the concept of the sufficient statistic of a distribution, which is the sum of the function of the data points. This concept is powerful because it means we do not need to store the entire data set but only the value of the sufficient statistic.

In the large data set limit, the maximum likelihood estimator will equal the true value of the parameter vector.

## Section: Nonparametric Density Estimation

We then turn our attention to nonparametric methods for density estimation, starting with histograms. Histograms are simple tools that partition a continuous variable into distinct bins and then count the number of observations falling within each bin.

An example of histogram density estimation shows that the choice of bin width significantly affects the final density model. Too small a bin width results in a model that's too spiky, capturing noise and non-representative fluctuations. Too large a bin width results in a model that's too smooth and fails to capture the true underlying distribution. An optimal bin width lies somewhere in between these extremes.

Despite its simplicity, the histogram approach has limitations, especially in high-dimensional data scenarios due to the curse of dimensionality. This term refers to the exponential increase in complexity with each additional dimension in the data.

## Section: Local Density Estimation

When estimating the probability density at a certain location, we should focus on data points that lie within a local neighborhood of that point. This concept of locality typically involves some distance measure, such as Euclidean distance. As in histograms, the neighborhood property is defined by bins, and there's a natural 'smoothing' parameter that describes the spatial extent of the local region, or the bin width.

For good results, the smoothing parameter should be neither too large nor too small, similar to choosing model complexity in polynomial regression. With these insights, we delve into two widely used nonparametric techniques for density estimation, namely kernel estimators and nearest neighbors.

## Section: Kernel Densities

Let's say we are drawing observations from an unknown probability density in a Euclidean space. We want to estimate this density at a particular point. From our prior discussion about locality, let's consider a small region containing this point. The probability mass associated with this region is the integral of the density over this region.

Suppose we have collected a dataset consisting of N observations drawn from our unknown density. Each data point has a probability of falling within our region, so the total number of points that lie inside this region follows a binomial distribution. For large N, this distribution will be sharply peaked around the mean, so the number of points is approximately the total number of observations times the probability.

If we also assume that our region is sufficiently small so that the probability density is roughly constant over the region, then the probability is approximately the density times the volume of the region. Combining these results, we get our density estimate as the number of points divided by the product of the number of observations and the volume of the region.

However, this density estimate relies on two contradictory assumptions, namely that the region is sufficiently small for the density to be approximately constant over it, and yet sufficiently large for the number of points falling inside the region to be enough for the binomial distribution to be sharply peaked.

## Section: Nearest Neighbours

One issue with the kernel approach to density estimation is that the parameter governing the kernel width is fixed for all kernels. In regions of high data density, a large value of this parameter may lead to over-smoothing and a loss of crucial structure in the data. However, reducing the parameter may lead to noisy estimates elsewhere where the data density is smaller. Thus, the optimal choice for the kernel width may be dependent on the location within the data space. This issue is addressed by nearest-neighbour methods for density estimation.

In nearest-neighbour methods, we fix the number of points and use the data to find an appropriate value for the volume of the region. We consider a small sphere centred on the point at which we wish to estimate the density. We allow the radius of the sphere to grow until it contains precisely a fixed number of data points. The estimate of the density is then given by the number of points divided by the product of the number of observations and the volume of the resulting sphere. This technique is known as K-nearest neighbours.

Again, there is an optimal choice for K that is neither too large nor too small. Note that the model produced by K-nearest neighbours is not a true density model because the integral over all space diverges.

By applying the K-nearest-neighbour density estimation technique to each class separately and then making use of Bayes' theorem, we can extend this technique to the problem of classification. This approach simply requires storing the training set, which is both its strength and its weakness because the computational cost of evaluating the density grows linearly with the size of the data set.

In conclusion, both kernel estimators and nearest neighbours provide nonparametric techniques for density estimation. Bot
h methods rely on the idea of considering local neighbourhoods of data points and have parameters that control the degree of smoothing. Choosing the optimal value for these parameters is crucial for obtaining good results.

## Section: Binomial Distribution and its Properties

Let's talk about a key concept in probability and statistics, the binomial distribution. Consider a set of binary variables, each of which can take on one of two values, such as 0 or 1. The distribution of the sum of these variables is known as the binomial distribution.

The binomial distribution features prominently in statistical models, as it quantifies the number of successes in a sequence of independent and identically distributed Bernoulli trials. The counts of successes in a fixed number of trials form a binomial distribution.

The mean and variance of the binomial distribution are simple to compute. The mean is the product of the number of trials and the probability of success, also known as the expectation. The variance is the product of the number of trials, the probability of success, and the probability of failure. These are straightforward results that come from the properties of independent events where the mean of the sum is the sum of the means, and the variance of the sum is the sum of the variances.

## Section: Multinomial Distribution

Now let's move onto the multinomial distribution. The multinomial distribution is a generalization of the binomial distribution. While the binomial distribution counts the number of successes from binary trials, the multinomial distribution counts the number of outcomes of multi-category trials.

In practical terms, the multinomial distribution can be used to describe quantities that can take one of several possible values. A common representation for this is the 1-of-K scheme, or "one-hot encoding", where the variable is represented by a K-dimensional vector. For instance, if we have a variable that can take 6 states, a particular observation of the variable would be represented by a 6-dimensional vector, with one element equal to 1 and all other elements equal to 0.

The mean of the multinomial distribution is simply the probability of each outcome, and the probability of each outcome can be calculated as the number of times it occurs divided by the total number of observations.

## Section: K-nearest Neighbour Classification

The K-nearest neighbour classifier is a simple yet effective method for classification problems. This method classifies a new point based on the class membership of its 'K' nearest neighbouring points from the training dataset. The 'K' closest points are determined based on some distance metric, and the new point is classified according to the majority class membership among these points.

An interesting property of the nearest-neighbour classifier, where 'K' is 1, is that in the limit as the number of training points approaches infinity, the error rate of this classifier is never more than twice the minimum achievable error rate of an optimal classifier. This optimal classifier is one that uses the true underlying class distributions. This is a powerful result, illustrating the strength of this simple classification technique.

## Section: The Multivariate Gaussian

In the realm of continuous variables, the Gaussian, or normal distribution, is a widely used model. For a single variable, the Gaussian distribution is defined by the mean and variance. For a D-dimensional vector, the multivariate Gaussian distribution is described by a D-dimensional mean vector and a D by D covariance matrix.

The Gaussian distribution is widely used due to its numerous desirable properties, including the fact that it can be completely described by its mean and variance, and its shape is symmetric and bell-shaped. Moreover, under certain conditions, according to the Central Limit Theorem, the sum of a large number of independent and identically distributed random variables, irrespective of their individual distributions, tends towards a Gaussian distribution. This property makes the Gaussian distribution a natural choice for many statistical models.

## Section: The Gaussian Distribution and the Central Limit Theorem

In this section, we delve into the properties and implications of the Gaussian distribution, a crucial probability distribution in the world of statistics. The Gaussian distribution is significant for two main reasons. Firstly, when dealing with a single variable, whether real or multivariate, the Gaussian distribution is the one that maximizes entropy. Secondly, the Gaussian distribution arises naturally when we consider the sum of multiple random variables. This is demonstrated by the central limit theorem, which states that under certain conditions, the sum of a set of random variables, each uniformly distributed over the interval from 0 to 1, will increasingly approximate a Gaussian distribution as the number of terms in the sum increases. This is visually illustrated in a histogram plot showing the distribution of the mean of ten uniformly distributed random variables.

Moreover, the Gaussian distribution is also characterized by its many important analytical properties. To explore these, we need to be familiar with various matrix identities.

## Section: Geometry of the Gaussian

The Gaussian distribution can be characterized geometrically by the quadratic form of the difference between a variable x and the mean of the distribution, denoted as mu. This difference, referred to as the Mahalanobis distance, becomes the Euclidean distance when the covariance matrix, denoted as Sigma, is the identity matrix. The Gaussian distribution remains constant for surfaces in x-space where this quadratic form is constant.

Interestingly, the covariance matrix Sigma can be considered symmetric without loss of generality, as any antisymmetric components would disappear from the quadratic form. As a result, we can examine the eigenvector equation for the covariance matrix. The covariance matrix Sigma can be expressed as an expansion in terms of its eigenvectors, and the inverse covariance matrix can be similarly expressed.

The quadratic form then becomes the sum of the squares of the new coordinates over their corresponding eigenvalues. These new coordinates, denoted as y sub i, form a new coordinate system, defined by the orthonormal vectors that are shifted and rotated with respect to the original x sub i coordinates.

The Gaussian density remains constant on surfaces where this quadratic form is constant. If all eigenvalues are positive, these surfaces represent ellipsoids, with their centers at mu and their axes oriented along the eigenvectors, and with scaling factors in the directions of the axes given by the square root of the eigenvalues.

For the Gaussian distribution to be well-defined, all eigenvalues of the covariance matrix must be strictly positive, making the matrix positive definite. If all eigenvalues are non-negative, the covariance matrix is said to be positive semidefinite.

The Gaussian distribution in the new coordinate system is then the product of independent univariate Gaussian distributions. The eigenvectors, therefore, define a new set of shifted and rotated coordinates with respect to which the joint probability distribution factorizes into a product of independent distributions.

This comprehensive exploration of the Gaussian distribution and its properties provides a deep understanding of why it is so prevalent in statistics and data analysis. Its elegance in mathematical form and its ubiquity in real-world phenomena make it one of the most crucial concepts in understanding and interpreting data.

## Summary

The chapter on Standard Distributions delves into various probability distributions, their properties, and their roles in modeling and machine learning. Here's a summary of the main points:

1. **Standard Distributions and Density Estimation**: The chapter discusses the importance of standard probability distributions in modeling random variables based on finite observations, highlighting the challenge of density estimation and model selection.

2. **Moments of the Gaussian Distribution**: The Gaussian distribution's first and second moments are examined, explaining that the mean (Mu) and covariance (Sigma) are key parameters. The covariance matrix, Sigma, represents the spread and correlations of the distribution.

3. **Limitations of the Gaussian Distribution**: While commonly used, the Gaussian distribution has limitations, especially in handling large dimensions and multimodal data. Restricting the covariance matrix (e.g., to diagonal or isotropic forms) can simplify computations but at the cost of flexibility.

4. **Conditional and Partitioned Distributions**: Conditional distributions and partitioning of Gaussian distributions are explored, showing that both conditional and marginal distributions of subsets of a multivariate Gaussian are also Gaussian. The importance of the precision matrix (inverse covariance) in these contexts is emphasized.

5. **Gaussian Mixture Models**: Gaussian mixture models combine multiple Gaussian distributions to better capture complex, multimodal data. These models use mixing coefficients to weigh the contributions of each component, and the Expectation-Maximization (EM) algorithm is commonly used for parameter estimation.

6. **Periodic Variables and von Mises Distribution**: For periodic data, such as wind direction, the von Mises distribution is introduced as a circular equivalent to the Gaussian distribution. It respects the periodic nature of the data and is parameterized by mean direction and concentration.

7. **Exponential Family Distributions**: This broad class includes distributions like Bernoulli and Gaussian, characterized by their exponential forms. The chapter discusses how these distributions can be expressed in terms of natural parameters and sufficient statistics.

8. **Nonparametric Density Estimation**: Techniques like histograms, kernel density estimation, and K-nearest neighbors are presented as alternatives to parametric methods. These approaches estimate densities based on local data properties but have their own challenges, especially in high-dimensional spaces.

9. **Binomial and Multinomial Distributions**: The binomial distribution models the number of successes in binary trials, while the multinomial distribution generalizes this to multi-category outcomes. Both distributions are covered, with a focus on their mean and variance properties.

10. **K-nearest Neighbour Classification**: This simple yet effective method classifies points based on the majority class of their nearest neighbors. The method is robust, with error rates approaching those of optimal classifiers as the data set size increases.

11. **Multivariate Gaussian Distribution**: Detailed exploration of the properties and geometry of the multivariate Gaussian distribution, including the significance of the covariance matrix and the Central Limit Theorem.

12. **Geometry of the Gaussian**: The Gaussian distribution's properties in terms of Mahalanobis distance and its representation through eigenvectors and eigenvalues of the covariance matrix are discussed, providing insight into its geometric structure.

Overall, the chapter provides a comprehensive overview of various probability distributions, their applications in modeling and machine learning, and methods for density estimation, both parametric and nonparametric.

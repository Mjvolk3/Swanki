Introduction to Probability: Univariate Models

What is Probability?

Probability theory is a fascinating and essential branch of mathematics that helps us quantify uncertainty and make informed decisions. Pierre Laplace eloquently summed it up in 1812 as "nothing but common sense reduced to calculation." At its core, probability allows us to make predictions about the likelihood of various outcomes. For instance, when we say that a fair coin has a 50 percent chance of landing heads, we are using probability to express our expectations.

There are two main interpretations of probability: the frequentist and the Bayesian approach. The frequentist interpretation views probability as the long-run frequency of an event occurring through repeated trials. For example, the statement about the coin means that if we flip it many times, it will land heads approximately half the time. In contrast, the Bayesian interpretation sees probability as a measure of our uncertainty or belief about an event. This view is more flexible, allowing us to deal with one-off events, such as predicting whether the polar ice cap will melt by 2030. Since we can’t rely on repeated trials for such unique events, the Bayesian approach quantifies our uncertainty based on available information.

Adopting the Bayesian interpretation in our discussions makes it possible to model our uncertainty in a broader range of scenarios. For example, even if an event cannot happen multiple times, we can still assign a probability to it based on our current knowledge and beliefs. The basic rules of probability, such as how probabilities add up and multiply, remain consistent across both interpretations.

Section: Types of Uncertainty

Uncertainty in our predictions can arise from two main sources. The first source is our ignorance of the underlying mechanisms producing the data. This type of uncertainty is often due to hidden factors or variables that we do not fully understand or observe. For instance, consider a probability density function of a mixture of two one-dimensional Gaussians, where each Gaussian component has its own mean and variance. The mixture model, with equal mixing coefficients, shows two distinct peaks, each representing different possible states or conditions. This reflects our uncertainty about which state the data might belong to.

The second source of uncertainty stems from the inherent randomness in the data generation process. Even if we completely understand the mechanisms at play, the outcomes can still be random. For example, flipping a fair coin is inherently random, and no amount of knowledge about the coin can predict the outcome of a single flip with certainty. This randomness is captured by the probability distribution, which tells us the likelihood of various outcomes.

To elucidate these ideas, let’s consider the law of total expectation, which states that the expected value of a random variable can be found by taking the expected values conditional on another variable and then averaging them. For instance, consider the lifetime of a lightbulb produced in different factories. If factory one produces bulbs with an average lifetime of 5000 hours and factory two produces bulbs with an average of 4000 hours, and factory one supplies 60 percent of the bulbs, then the expected lifetime of a random bulb is a weighted average of these lifetimes, reflecting both the variability within each factory and the distribution of production across factories.

Section: Limitations of Summary Statistics

While summary statistics like mean and variance are useful for condensing information about a dataset, they often fail to capture the full complexity of the data. This limitation is strikingly illustrated by Anscombe's quartet, which consists of four different datasets that share identical summary statistics but have vastly different distributions. The quartet highlights the importance of data visualization in understanding the true nature of data.

For example, one dataset in the quartet may show a linear relationship, another a quadratic curve, and yet another may have an outlier that skews the perception of the data. Despite identical means, variances, and correlations, the visual representations reveal different underlying patterns. This underscores the danger of relying solely on summary statistics without visualizing the data.

An even more dramatic example is the Datasaurus Dozen, a collection of datasets including one that forms the shape of a dinosaur. All these datasets have the same summary statistics but look completely different when plotted. This collection was created using a technique called simulated annealing, which optimizes the datasets to match specific statistical properties while forming distinct shapes. This clearly demonstrates that identical statistical summaries can correspond to very different real-world distributions, emphasizing the necessity of visual data analysis.

Section: Bayes' Rule

Bayes' theorem is a cornerstone of probability theory, much like Pythagoras's theorem is for geometry. It provides a powerful framework for updating our beliefs in the light of new evidence. According to Bayes' rule, the probability of a hypothesis given some observed data is proportional to the prior probability of the hypothesis multiplied by the likelihood of the data given the hypothesis.

In simpler terms, Bayes' rule allows us to update our prior beliefs (what we thought before observing the data) based on the likelihood of the observed evidence. This updated belief is known as the posterior probability. The formula is straightforward: the posterior probability is equal to the prior probability times the likelihood, divided by the probability of the observed data. This process helps us refine our predictions and make more informed decisions.

For example, if we are trying to determine the probability of a medical condition given a positive test result, Bayes' rule lets us combine our prior knowledge about the prevalence of the condition with the accuracy of the test. This yields a more accurate assessment of the likelihood of having the condition, taking into account both the initial belief and the new evidence provided by the test result. Thus, Bayes' rule is an essential tool for making rational inferences and updating our understanding of the world.

Section: Likelihood and Bayesian Inference

Let’s dive into the concept of likelihood and its role in Bayesian inference. When we talk about the function representing the probability of the observed data given a hypothesis, we refer to this as the likelihood. Here, the observed data is fixed, and we are considering different hypotheses or hidden states. The likelihood is a function of the hidden state, given that the data is fixed. Importantly, the likelihood is not a probability distribution because it does not sum to one across all possible values of the hidden state.

To understand Bayesian inference, we start by combining the likelihood with the prior distribution. The prior represents our initial beliefs about the hidden state before observing any data. By multiplying the prior by the likelihood for each possible hidden state, we get the unnormalized joint distribution of the hidden state and the observed data. This joint distribution combines our prior beliefs with the information provided by the observed data.

To normalize this joint distribution and obtain a proper probability distribution, we divide by the marginal likelihood, which is the total probability of the observed data. This normalization ensures that the resulting posterior distribution is a valid probability distribution, summing to one across all possible hidden states. This process allows us to use Bayesian inference to update our beliefs based on new evidence and make more informed decisions.
Section: Posterior Distribution

When we observe new data, we update our beliefs about the hidden state. This updated belief is represented by the posterior distribution. The posterior distribution is the probability of the hidden state given the observed data. It combines our prior beliefs with the likelihood of the observed data to give us a new, updated probability distribution over the hidden states.

Section: Example: Testing for COVID-19

Let's apply Bayesian inference to a practical example: testing for COVID-19. Suppose you want to determine if you are infected with COVID-19 based on the result of a diagnostic test. Here, we denote being infected as hidden state 1 and not being infected as hidden state 0. If the test result is positive, we denote this as observed data 1, and if it is negative, we denote this as observed data 0. Our goal is to compute the probability of being infected given the observed test result.

To do this, we need two key pieces of information: the test's sensitivity and specificity. Sensitivity, or true positive rate, is the probability of a positive test given that you are infected. Specificity, or true negative rate, is the probability of a negative test given that you are not infected. We also need the prior probability of being infected, which represents the prevalence of the disease in your area.

Suppose the sensitivity of the test is 87.5 percent and the specificity is 97.5 percent. The prior probability of being infected is 10 percent, reflecting the prevalence in New York City in Spring 2020. If you test positive, the posterior probability of being infected is calculated using Bayes' rule: we multiply the sensitivity by the prior probability and then normalize by the total probability of a positive test. This results in a 79.5 percent chance of being infected if the test is positive. Conversely, if the test is negative, the probability of being infected is much lower, at 1.4 percent.

Section: Example: The Monty Hall Problem

Now, let’s explore a more playful application of Bayesian inference: the Monty Hall problem. Imagine a game show with three doors, one of which hides a prize. You pick one door, and the host, who knows where the prize is, opens another door that does not reveal the prize. You then have the option to stick with your initial choice or switch to the remaining unopened door.

Intuition might suggest that it makes no difference whether you switch or stay. However, using Bayes' rule, we can show that switching doors actually doubles your chances of winning. Initially, each door has an equal probability of hiding the prize, so the prior probabilities are one-third for each door.

When the host opens a door, this action provides additional information. If the host opens door three, for instance, the probabilities need to be updated. Given that the host's choice is influenced by the location of the prize, the likelihoods are different depending on where the prize actually is. Bayes' rule helps us update the probabilities, showing that the probability of the prize being behind the door you initially chose is one-third, while the probability of it being behind the other unopened door is two-thirds. Thus, you should switch doors to maximize your chances of winning.

Section: Inverse Problems

Inverse problems involve inferring unknown states of the world from observed data, essentially reversing the process of prediction. For instance, consider trying to infer a three-dimensional shape from a two-dimensional image. This is challenging because multiple three-dimensional shapes can project to the same two-dimensional image, making the problem fundamentally ill-posed.

To address inverse problems, we use Bayes' rule to compute the posterior distribution over the possible states of the world. This involves specifying a forward model, which gives the probability of observing the data given a particular state, and a prior distribution over the states. The posterior distribution then combines the prior information with the observed data to provide a probabilistic estimate of the true state. This approach is widely used in fields like computer vision and natural language understanding, where the goal is to infer hidden structures or meanings from observed data.

Section: Bernoulli and Binomial Distributions

Definition of the Bernoulli Distribution

The Bernoulli distribution is one of the most fundamental probability distributions used to model binary events. Imagine flipping a coin where the probability of landing heads lies between zero and one. If we let the variable Y equal one represent the event where the coin lands heads and Y equal zero for tails, we can describe this scenario using the Bernoulli distribution. This means that the probability of heads is equal to theta, and the probability of tails is equal to one minus theta.

Mathematically, we say that the variable Y follows a Bernoulli distribution with parameter theta. The probability mass function for this distribution specifies the probabilities for each possible value of Y. For Y equal to zero, the probability is one minus theta, and for Y equal to one, the probability is theta.

Understanding the Binomial Distribution

The Bernoulli distribution is actually a special case of a broader distribution known as the binomial distribution. Suppose you repeat a Bernoulli trial N times—think of tossing the coin N times. Let the variable s be the number of heads observed in these N trials. The number of heads s follows a binomial distribution, which is denoted as s follows Binomial distribution with parameters N and theta.

The binomial distribution gives us the probability of observing exactly s heads in N trials. The formula involves the binomial coefficient, often referred to as "N choose s", which counts the number of different ways to choose s heads out of N trials. The binomial probability is then given by the product of this coefficient, theta to the power of s, and one minus theta to the power of N minus s.

Section: Sigmoid (Logistic) Function

When predicting a binary outcome based on some input features, we often use a logistic function, also known as the sigmoid function. This function smoothly maps any real-valued number into a value between zero and one, making it ideal for probability predictions. The sigmoid function is commonly used in logistic regression, where the output is interpreted as the probability of a binary event occurring based on the input features. This makes it a powerful tool for binary classification tasks.
Section: Sigmoid (Logistic) Function (Continued)

The sigmoid function's S-shaped curve ensures that the output stays within the range of zero to one, which is necessary for interpreting it as a probability. This function can be viewed as a "soft" version of the Heaviside step function, which jumps from zero to one at a certain threshold. By providing a smooth transition, the sigmoid function allows for more nuanced interpretations of probability.

One important property of the sigmoid function is its derivative, which is the product of the sigmoid function itself and one minus the sigmoid function. This derivative is particularly useful in optimization algorithms during model training, as it helps in calculating gradients for updating model parameters. Additionally, the inverse of the sigmoid function is known as the logit function, which maps probabilities back to log-odds. This reverse mapping is useful in statistical modeling and analysis.

Section: Binary Logistic Regression

In binary logistic regression, the sigmoid function is used to model the probability of a binary outcome based on some input features. The model predicts the probability that the output, often denoted as Y, is one (such as the coin landing heads or a flower belonging to a particular species) based on a linear combination of the input features.

The logistic regression model defines the conditional probability of the binary outcome using the logistic function. The parameters of the model include a weight vector and a bias term. The logistic function ensures that the output of this linear combination is mapped to a valid probability between zero and one.

For example, when applied to a one-dimensional, two-class version of the Iris dataset, logistic regression can classify flowers based on petal width. The decision boundary is the value of petal width where the probability of being a particular class, such as Virginica, is 50 percent. As the petal width increases or decreases from this boundary, the model's confidence in its classification also increases. This illustrates the power and simplicity of logistic regression in binary classification tasks.

Section: Categorical and Multinomial Distributions

To represent a distribution over a finite set of labels, we use the categorical distribution. This is an extension of the Bernoulli distribution to cases where the number of possible outcomes is greater than two.

Section: Definition of the Categorical Distribution

The categorical distribution is a discrete probability distribution characterized by one parameter per class. The probability that the variable Y equals a specific class is given by the parameter associated with that class, denoted as theta sub c. These parameters must satisfy two constraints: each must lie between zero and one, inclusive, and the sum of all parameters must equal one. This implies that there are only C minus one independent parameters because the final parameter can be determined by the sum constraint.

We can also represent the categorical distribution using a one-hot vector, which has C elements where all entries are zero except for the one corresponding to the class label, which is one. For instance, if we have three classes, the one-hot encodings for classes one, two, and three would be (1,0,0), (0,1,0), and (0,0,1) respectively. This one-hot vector representation simplifies the categorical distribution into a form where the probability of each class is directly tied to the parameter associated with that class.

The categorical distribution is a special case of the multinomial distribution. Imagine rolling a C-sided die N times and counting the number of times each side appears. The resulting counts form a vector that follows a multinomial distribution. This distribution includes a multinomial coefficient representing the number of ways to divide a set of size N into subsets of specified sizes for each class. If N equals one, the multinomial distribution simplifies to the categorical distribution.

Section: Softmax Function

When dealing with conditional probabilities, we can define the probability of a class given some input and parameters as a categorical distribution where the parameters are a function of the input and parameters. This function must output a probability vector that sums to one and has each element between zero and one.

To achieve this, we often use the softmax function, also known as the multinomial logit function. The softmax function transforms a vector of values, called logits, into a probability distribution. It does this by exponentiating each logit, then normalizing these values by dividing by the sum of all exponentiated logits. This ensures that the output values fall between zero and one and sum to one, making them valid probabilities.

The softmax function is particularly useful because it can smoothly interpolate between the argmax function, which selects the largest value and assigns it a probability of one while all others get zero, and a uniform distribution, where all values have equal probability. By introducing a temperature parameter, we can control this behavior. At high temperatures, the distribution becomes more uniform, while at low temperatures, it becomes more peaked around the highest value.

Section: Multiclass Logistic Regression

In multiclass logistic regression, we use a linear predictor to model the logits, which are then passed through the softmax function to obtain probabilities. The linear predictor is a combination of a weight matrix and a bias vector applied to the input features.

For a given input, the logits are computed as a weighted sum of the input features plus a bias term. These logits are then transformed by the softmax function to produce the probability for each class. This approach generalizes binary logistic regression to multiple classes. In the binary case, the softmax function simplifies to the logistic function, and we only need a single weight vector rather than multiple.

An example of this is fitting a multinomial logistic regression model to the Iris dataset, where the model predicts the species of an Iris flower based on its petal length and width. The decision boundaries in this case are linear, reflecting the linear nature of the logistic regression model. However, more complex boundaries can be modeled by transforming the input features, such as using polynomial features.

Section: Log-Sum-Exp Trick

When working with the softmax function, we often encounter numerical stability issues due to the exponential operations involved. For instance, very large or very small values can lead to overflow or underflow errors.

To mitigate these issues, we use the log-sum-exp trick. This technique involves subtracting the maximum logit value from all logits before exponentiating them. By doing this, the largest exponentiated value becomes one, ensuring that we avoid overflow. This approach helps maintain numerical stability and ensures that the computations remain within a manageable range.
Section: Log-Sum-Exp Trick (Continued)

This trick is crucial for ensuring numerical stability when computing probabilities and is commonly used in the implementation of the cross-entropy loss function, which measures the difference between predicted and actual probability distributions.

Section: Univariate Gaussian (Normal) Distribution

The Gaussian distribution, also known as the normal distribution, is the most widely used distribution for real-valued random variables. It is characterized by its mean and variance, which determine its location and spread.

Section: Cumulative Distribution Function of the Gaussian Distribution

The cumulative distribution function (CDF) of a continuous random variable is the probability that the variable takes a value less than or equal to a given number. For the Gaussian distribution, the CDF is denoted by Phi and takes into account the mean and variance of the distribution.

The CDF is a monotonically non-decreasing function, meaning it never decreases as the input value increases. Using the CDF, we can compute the probability that a random variable lies within a specific interval by taking the difference of the CDF values at the endpoints of the interval. Understanding the CDF is essential for working with probabilities and intervals in the context of continuous random variables, particularly when dealing with Gaussian distributions.

We start by exploring the concept of the cumulative distribution function, or CDF, of a Gaussian distribution. The CDF is a function that maps a value to the probability that a random variable will take a value less than or equal to that number. For a Gaussian distribution, this can be written as the integral of the probability density function, or PDF, from negative infinity to a given value. Essentially, this integral sums up all the probabilities up to that value.

One common implementation of the Gaussian CDF uses the error function, denoted as "erf." The error function is a special mathematical function that arises in probability, statistics, and partial differential equations. It is defined as twice the integral from zero to a particular value of the exponential function e to the power of negative t squared, where t is a dummy variable of integration. This function is scaled by a factor involving the square root of pi to ensure it captures the correct probability mass.

In practical terms, when working with a Gaussian distribution characterized by a mean and a variance, the CDF can be expressed using the error function. This allows us to determine the probability that a random variable will fall within a certain range, which is particularly useful in statistical modeling and hypothesis testing. For instance, if we set the mean to zero and the standard deviation to one, we obtain the standard normal distribution, which simplifies the calculations and is often used as a benchmark in statistics.

Section: Probability Density Function of the Gaussian Distribution

Next, let's delve into the probability density function, or PDF, of the Gaussian distribution. The PDF is essentially the derivative of the CDF and provides the likelihood of the random variable taking on a specific value. For the Gaussian distribution, the PDF is a bell-shaped curve that is symmetric around the mean. This curve is mathematically described by an exponential function that diminishes as one moves away from the mean, scaled by a normalization factor to ensure the total probability sums to one.

The Gaussian PDF is defined by two main parameters: the mean, which determines the center of the distribution, and the variance, which dictates the spread or width of the distribution. The normalization constant, which involves the square root of two pi times the variance, ensures that the area under the curve equals one, satisfying the property of total probability.

One interesting property of the PDF is that it allows us to calculate the probability of the random variable falling within any given interval. For example, the probability that the variable falls between two values is given by the integral of the PDF from one value to the other. This is equivalent to the difference between the CDF values at those points. For very small intervals, the probability can be approximated by multiplying the PDF value at a point by the width of the interval, providing a practical way to understand the density at a specific location.

Section: Understanding Regression with Gaussian Output

Regression models often assume that the output variable follows a Gaussian distribution. In the simplest case, known as homoscedastic regression, the variance of the output is assumed to be constant and independent of the input variables. This means the spread of errors or deviations from the predicted mean remains the same regardless of the input values. Linear regression is a classic example where the mean of the output is modeled as a linear function of the input variables. The resulting model captures the central tendency of the data with a fixed spread around this central line.

However, in many real-world scenarios, the variance can change with different levels of the input variables. This leads to heteroscedastic regression, where the variability of the output depends on the input. In such cases, the Gaussian distribution used to model the output has a mean that is a linear function of the input but a variance that also changes with the input. This more flexible approach can better accommodate data where the spread of observations varies across the range of input values.

Visual representations, such as scatter plots with fitted regression lines and confidence intervals, help illustrate these concepts. In the case of homoscedastic regression, the intervals around the regression line are parallel, showing a constant spread. For heteroscedastic regression, these intervals can widen or narrow depending on the input values, reflecting the varying uncertainty in predictions.

Section: Importance of the Gaussian Distribution

The Gaussian distribution is extensively used in statistics and machine learning for several compelling reasons. Firstly, it has a simple mathematical form with only two parameters—the mean and the variance—which are easy to interpret and relate to the data. The mean reflects the central tendency, while the variance indicates the spread. This simplicity makes it a convenient choice for modeling.

Secondly, the central limit theorem provides a powerful justification for its use. This theorem states that the sum of a large number of independent random variables, regardless of their original distributions, tends to follow a Gaussian distribution. This underlies the rationale for using Gaussian distributions to model residual errors in various contexts.

Thirdly, the Gaussian distribution maximizes entropy, given the constraints of a specified mean and variance. This property means it makes the least number of assumptions about the data beyond these constraints, serving as a good default model in many situations. Its simplicity also leads to efficient computational methods, making it practical for a wide range of applications.

Historically, the Gaussian distribution was popularized by Carl Friedrich Gauss, although it was discovered earlier by other mathematicians.
can be misleading as it implies other distributions are "abnormal," which is not the case. The Gaussian distribution is special due to its unique properties and widespread applicability.

Section: Dirac Delta Function as a Limiting Case

The Dirac delta function is a concept that arises when considering the limit of a Gaussian distribution as its variance approaches zero. As the variance decreases, the Gaussian distribution becomes increasingly narrow and tall, concentrating its mass around the mean. In the limit, this results in an infinitely narrow spike at the mean, which is mathematically represented by the Dirac delta function. This function is zero everywhere except at a single point where it is infinitely high, and its integral over the entire real line is one.

The Dirac delta function is useful in various fields, including physics and engineering, as it can model idealized point sources or instantaneous impulses. In mathematical terms, it captures the idea of a distribution that is entirely concentrated at a single point, making it a powerful tool for theoretical analysis and practical applications.

In summary, understanding the Gaussian distribution, its properties, and extensions like the Dirac delta function provides a solid foundation for many statistical and machine learning models. These concepts are not only theoretically elegant but also practically useful in analyzing and interpreting real-world data.

Section: Some Other Common Univariate Distributions

In this section, we introduce a few univariate distributions that are commonly used in statistics and machine learning. Each of these distributions has unique properties and applications, making them versatile tools for modeling various types of data.

Section: Student's t-Distribution

To start, let's discuss the Student's t-distribution. Unlike the Gaussian distribution, which is quite sensitive to outliers, the Student's t-distribution is more robust and can handle data with outliers effectively. The probability density function of the Student's t-distribution is characterized by three parameters: the mean, a scale parameter, and the degrees of freedom. The degrees of freedom play a crucial role in shaping the distribution. When the degrees of freedom are large, the Student's t-distribution approximates a Gaussian distribution, but for smaller values, the distribution has heavier tails, making it more resistant to outliers.

Historically, this distribution was first published by William Sealy Gosset under the pseudonym "Student" because his employer, the Guinness brewery, did not allow him to publish under his name. The t-distribution is particularly useful in situations where the sample size is small or the data contain outliers. This robustness is visually evident in figure 2.16, which shows how both the Student and Laplace distributions remain relatively unaffected by outliers, unlike the Gaussian distribution, which gets significantly distorted.

Section: Cauchy Distribution

Next, when the degrees of freedom are set to one, the Student's t-distribution transforms into the Cauchy distribution, also known as the Lorentz distribution. The Cauchy distribution has extremely heavy tails. For instance, while 95 percent of the values from a standard normal distribution fall between negative 1.96 and positive 1.96, the same percentage for a standard Cauchy distribution lies between approximately negative 12.7 and positive 12.7. This means that the Cauchy distribution has more probability mass in the tails compared to the Gaussian, and as a result, it does not have a well-defined mean or variance. This property can be both an advantage and a disadvantage depending on the application, but it makes the Cauchy distribution particularly useful in Bayesian modeling for positive reals with heavy tails.

Section: Laplace Distribution

Moving on, let's explore the Laplace distribution, also known as the double-sided exponential distribution. The Laplace distribution is another robust alternative to the Gaussian distribution. It has a peak at its mean, similar to the Gaussian, but its tails fall off more slowly, making it resilient to outliers. The probability density function of the Laplace distribution is characterized by a location parameter and a scale parameter, and its variance is twice the square of the scale parameter. This distribution is used in various applications, including robust linear regression, where it helps to mitigate the influence of outliers on the model.

Section: Beta Distribution

Now, let’s consider the Beta distribution, which is defined over the interval from zero to one. The Beta distribution is parameterized by two positive parameters, a and b, which shape the distribution. Depending on the values of these parameters, the Beta distribution can take various forms, from uniform to highly skewed distributions. It is often used in Bayesian statistics to model the distribution of probabilities. For example, if both parameters are equal to one, the Beta distribution is uniform. If both parameters are less than one, the distribution becomes bimodal with spikes at zero and one. Conversely, if both parameters are greater than one, the distribution is unimodal.

Section: Gamma Distribution

Finally, let's discuss the Gamma distribution, which is a flexible distribution for modeling positive real-valued random variables. It is parameterized by a shape parameter and a rate parameter. The Gamma distribution is versatile and can take various shapes, making it suitable for a wide range of applications, including modeling waiting times in Poisson processes. Special cases of the Gamma distribution include the Exponential distribution, which is used to describe the time between events in a Poisson process.

In summary, understanding these distributions and their properties allows us to choose the right model for our data, ensuring that we can make accurate inferences and predictions. Each distribution has its strengths and is suited for different types of data and scenarios, making them invaluable tools in the field of statistics and machine learning.

Section: Empirical Distribution

Imagine we have a set of samples, say five in total, each representing a data point drawn from some unknown distribution. Our goal is to estimate the probability density function and the cumulative distribution function from these samples. This process of estimation from finite samples is what we call constructing the empirical distribution.

To approximate the probability density function, we use delta functions, often visualized as spikes, centered on each sample point. Picture this as a graph where each sample is represented by a vertical line or spike, and the height of these lines indicates the density at that point. For five samples, each spike contributes equally to the overall density. The empirical probability density function is essentially a sum of these spikes, and since we have five samples, each spike has a weight of one-fifth.

Now, let's consider the cumulative distribution function. The cumulative distribution function gives us the probability that a random variable is less than or equal to a certain value. In the empirical case, this is visualized as a staircase function, where each step corresponds to a sample. For our set of five samples, the cumulative distribution function increases by one-fifth at each sample point.
graph where the height of each step is one-fifth, reflecting the equal contribution of each sample to the cumulative probability.

Section: Chi-Squared and Inverse Gamma Distributions

The Chi-squared distribution holds significant importance in statistics, particularly in hypothesis testing and the construction of confidence intervals. Defined by its degrees of freedom, denoted as "nu," this distribution represents the sum of the squares of "nu" standard normal variables. Imagine each of these normal variables as a measure of some random phenomenon; squaring them ensures all values are positive. Summing the squares of multiple such phenomena results in the Chi-squared distribution, which is fundamental in assessing data variability from a theoretical perspective.

The Inverse Gamma distribution is more complex, characterized by two parameters: shape "a" and scale "b." This distribution proves useful in Bayesian statistics and other areas requiring the reciprocal of a gamma-distributed variable. It has specific properties, such as the mean and variance, which exist only under certain conditions for the shape parameter "a." Specifically, the mean exists if "a" is greater than one, and the variance exists if "a" is greater than two. This distribution is valuable for modeling scenarios where the rate or scale of a process is uncertain.

Section: Transformations of Random Variables

Transforming random variables is a powerful technique in probability and statistics, enabling us to understand how different operations affect the distributions of these variables. Consider a simple example: a random variable "x" that is uniformly distributed between zero and one. If we apply a transformation, such as "y equals two times x plus one," this operation stretches and shifts the distribution. Originally, the values of "x" ranged from zero to one. After the transformation, they now range from one to three, and the density adjusts accordingly to ensure the total probability remains one. This concept is visualized in a graph where the original and transformed distributions are compared.

For continuous variables, deriving the distribution of "y" involves working with cumulative distribution functions (CDFs). For an invertible transformation, which means you can reverse the operation, the probability density function (PDF) of "y" can be found by differentiating the CDF with respect to "y." This process involves a change of variables formula, which accounts for the rate of change of "x" with respect to "y." Essentially, it tells us how the density transforms under the function.

Section: Change of Variables: Multivariate Case

Extending these ideas to multiple dimensions, we deal with transformations involving multiple variables. Imagine transforming a two-dimensional space, such as shifting and rotating a square into a parallelogram. The transformation is represented by a matrix "A" and a vector "b." The determinant of matrix "A" provides a measure of how the area (or volume in higher dimensions) changes under the transformation. This determinant is crucial in adjusting the density to ensure the total probability remains consistent.

For instance, when transforming from Cartesian coordinates to polar coordinates, the Jacobian matrix represents the partial derivatives of the transformation. The determinant of this Jacobian gives us the scaling factor needed to adjust the density appropriately. In this case, transforming from Cartesian to polar coordinates involves a radial component "r" and an angular component "theta," and the determinant of the Jacobian is "r," reflecting the radial scaling.

By understanding these transformations, we can effectively model and analyze how various operations impact the distributions of random variables, providing deeper insights into the underlying probabilistic processes.

Section: Geometric Interpretation of Polar to Cartesian Coordinate Transformation

Geometrically, when we look at the transformation from polar to Cartesian coordinates, we can visualize the area of a small shaded patch in the polar coordinate system. This patch is defined by a small change in the radius from "r" to "r plus dr," and a small change in the angle from "theta" to "theta plus dtheta." The infinitesimal area of this patch is given by multiplying the radius, the small change in radius "dr," and the small change in angle "dtheta."

The area of this infinitesimal patch, therefore, is "r times dr times dtheta." This concept is crucial because it helps in understanding how density functions transform under a change of variables. Specifically, the probability that a point falls within this small patch is the density at the center of the patch times the size of the patch. This is represented as "p sub r, theta of r, theta times dr times dtheta."

When transforming this area into Cartesian coordinates, we need to account for the transformation of the density functions. The probability density function in Cartesian coordinates, "p sub x1, x2 of x, y," can be related to the density function in polar coordinates through the transformation "x equals r cosine theta" and "y equals r sine theta." The area "r times dr times dtheta" remains the same, and thus the density functions are related by "p sub r, theta of r, theta times dr times dtheta equals p sub x1, x2 of r cosine theta, r sine theta times r times dr times dtheta."

Section: Moments of a Linear Transformation

When dealing with linear transformations, we often seek to understand how moments like the mean and covariance transform. Suppose we have an affine function where "y equals A times x plus b." To find the mean of "y," we use the expectation operator. The expectation of "y" is "E of y equals E of A times x plus b."

Given that expectation is a linear operator, we can separate the terms, leading to "E of y equals A times E of x plus b." If the mean of "x" is denoted as "mu," then the mean of "y" is "A times mu plus b."

For the covariance of "y," recall that covariance measures how much two random variables vary together.
Section: Covariance of Linear Transformations

When dealing with linear transformations, we also need to understand how the covariance transforms. Suppose we have a linear transformation defined by the equation y equals A times x plus b, where A is a matrix and b is a constant vector. The covariance of y, denoted as Cov of y, is given by Cov of A times x plus b. Since b is a constant vector, it does not affect the covariance, leaving us with A times Cov of x times the transpose of A. Here, Sigma is the covariance matrix of x.

As a specific example, if y equals a transpose times x plus b, the variance of y, denoted as the variance of y, can be computed as a transpose times Sigma times a. This formula is particularly useful in scenarios like computing the variance of the sum of two scalar random variables by setting the appropriate vector a.

Section: The Convolution Theorem

Understanding the convolution theorem is essential when dealing with sums of random variables. Suppose y equals x1 plus x2, where x1 and x2 are independent random variables. If these variables are discrete, the probability mass function for the sum can be computed by summing the probabilities of all possible combinations of x1 and x2 that add up to y. This involves summing over all possible values of k, where k represents the value of x1 and y minus k represents the value of x2.

For continuous random variables with probability density functions p1 of x1 and p2 of x2, the cumulative distribution function of their sum y is given by integrating over the region where x1 plus x2 is less than or equal to y. The probability density function for y is then the derivative of this cumulative distribution function, yielding an integral of the form where p of y is the integral of p1 of x1 times p2 of y minus x1 with respect to x1.

This integral is known as the convolution of p1 and p2. For finite-length vectors, this convolution can be visualized as a "flip and drag" operation, where one function is flipped and then dragged over the other, multiplying elementwise and summing the results.

A practical example of this is the distribution of the sum of two dice rolls. Each die has a uniform distribution over the integers from one to six. The resulting distribution for the sum, y equals x1 plus x2, is not uniform but forms a triangular shape, peaking at seven. This distribution resembles a Gaussian distribution, as explained by the central limit theorem.

Section: The Central Limit Theorem

The central limit theorem is a foundational result in probability theory. It states that the sum of a large number of independent and identically distributed random variables, each with finite mean and variance, will approximately follow a normal distribution, regardless of the original distribution of the variables.

Consider N independent random variables, each with the same distribution, mean mu, and variance sigma squared. Let SN be the sum of these variables. As N becomes large, the distribution of SN approaches a normal distribution with mean N times mu and variance N times sigma squared.

Mathematically, this is represented by the probability density function of SN, which approaches the normal distribution with the given mean and variance. This result explains why many naturally occurring distributions tend to be Gaussian, as they can be seen as the sum of many small independent contributions.

In visual examples, we see discrete distributions on a state space. In one example, all outcomes are equally likely, representing a uniform distribution. In another example, all probability mass is concentrated on a single outcome, representing a degenerate or delta distribution. These visualizations help illustrate fundamental concepts in probability, such as how different distributions can be characterized and compared.

Section: Uniform and Degenerate Distributions

On one side, we have a uniform distribution, where the probability of any specific value within the distribution is constant. For instance, if the probability is one-fourth, it means each value in the distribution has an equal chance of occurring. On the other side, we have a degenerate distribution, which can be thought of as a distribution that assigns a probability of one to a single point—in this case, the value one. This is represented by an indicator function that equals one if and only if the variable is one. Essentially, this means our random variable is always equal to one, highlighting that random variables can also take on constant values.

Section: Continuous Random Variables

When dealing with real-valued quantities, we refer to them as continuous random variables. Unlike discrete random variables, which can take on a finite or countable set of values, continuous random variables can take any value within a given range. This means we can't list all possible values, but we can consider intervals on the real line. By associating events with these intervals, we can use methods similar to those for discrete random variables. The idea is that as we make these intervals smaller and smaller, we approach the notion of the probability of the random variable taking on a specific value.

Section: Cumulative Distribution Function (CDF)

The cumulative distribution function, or CDF, is a fundamental concept for continuous random variables. Let's define three events: A is the event that our random variable X is less than or equal to some value a; B is the event that X is less than or equal to some value b, where b is greater than a; and C is the event that X lies between a and b. Because A and C are mutually exclusive, the probability of B, which can be thought of as A or C, is simply the sum of their probabilities. Therefore, the probability that X lies in the interval between a and b is the probability of B minus the probability of A.

Section: Central Limit Theorem (Revisited)

The central limit theorem is a key concept in statistics. It states that as you increase the number of samples, the distribution of the sample means will approach a normal distribution, regardless of the original distribution of the data.

By understanding these fundamental concepts, you can better grasp the behavior of random variables and their distributions, providing a solid foundation for further explorations in probability and statistics.
Section: Application of the Central Limit Theorem

The central limit theorem (CLT) is a cornerstone of probability theory. To visualize its implications, consider the distribution of sample means for different sample sizes. For instance, one histogram might show the distribution for a single sample, while another shows the distribution for five samples. As the number of samples increases, the shape of the histogram becomes more bell-shaped, illustrating the CLT in action. This convergence towards a normal distribution, regardless of the original data distribution, underscores the power of the CLT in statistical analysis.

Section: Monte Carlo Approximation

Monte Carlo approximation is a powerful technique used when it's difficult to compute the distribution of a function of a random variable analytically. Instead, we draw a large number of samples from the random variable's distribution and use these samples to approximate the desired distribution. For example, imagine we have a random variable X uniformly distributed between negative one and one, and we want to find the distribution of Y, where Y is X squared. By drawing many samples of X, computing their squares, and examining the resulting distribution of Y, we approximate its distribution. This method, named after the famous Monte Carlo casino, is widely used in fields such as statistical physics and machine learning.

Monte Carlo methods are especially useful in scenarios involving complex or unknown distributions where traditional analytical methods fall short. They provide a flexible and powerful way to estimate probabilities and expectations by leveraging the law of large numbers. The more samples we draw, the closer our approximation will be to the true distribution, making Monte Carlo approximation a valuable tool in probabilistic modeling and inference.

Section: Probability Density Function (PDF)

The probability density function, or PDF, is the derivative of the cumulative distribution function (CDF). The PDF tells us the density of the probability at a specific point. For continuous variables, we can't talk about the probability of the variable being exactly equal to a specific value; instead, we talk about the probability of the variable lying within a small interval around that value. The probability is approximately the value of the PDF at that point times the width of the interval. Visual aids often illustrate this concept with a bell-shaped curve for the normal distribution, showing how the density changes across different values.

Understanding the PDF is crucial for working with continuous random variables. It allows us to calculate probabilities for intervals and understand the likelihood of different outcomes. For instance, the area under the PDF curve over a specific interval represents the probability that the random variable falls within that interval. This concept is fundamental in statistical analysis and probability theory, providing a way to quantify and model uncertainty in continuous domains.

Section: Quantiles

Quantiles are values that divide the probability distribution into intervals with equal probabilities. The most familiar quantile is the median, which divides the distribution into two equal halves. The CDF's inverse function, called the inverse CDF or quantile function, helps find these quantile values. For example, in a standard normal distribution, the 0.025 and 0.975 quantiles correspond to the points that enclose the central 95 percent of the distribution. These points are approximately negative 1.96 and positive 1.96, respectively, for a standard normal distribution. Quantiles are useful for understanding the spread and central tendency of the distribution.

Quantiles provide a deeper understanding of the distribution by highlighting the values at which certain percentages of the data lie below. They are particularly useful in statistical analysis for setting thresholds, creating confidence intervals, and performing robust comparisons between different datasets. By breaking down these concepts, we can see that probability and statistics offer powerful tools for understanding random variables and their behaviors. Whether we're dealing with uniform, degenerate, or continuous distributions, or applying the central limit theorem and Monte Carlo methods, these foundational ideas help us make sense of the randomness inherent in the world around us.

Section: Understanding Probabilistic Machine Learning: Joint, Marginal, and Conditional Distributions

When dealing with related random variables, it's crucial to understand the concept of joint distributions. Let's consider two random variables, X and Y. The joint distribution of these two variables can be expressed as the probability that X takes a specific value, and Y takes another specific value, simultaneously. This is denoted as the probability of X equals x and Y equals y. If both X and Y can only take on a finite number of values, we can represent the joint distribution in a two-dimensional table where each entry corresponds to a specific pair of values for X and Y, and the sum of all entries in the table equals one.

For instance, let's consider a simple example with binary variables X and Y. If we create a table where X and Y can each be either zero or one, and we fill in the table with probabilities for each pair, we might get something like 0.2 for X equals zero and Y equals zero, 0.3 for X equals zero and Y equals one, and so on. The sum of all these values in the table will be one, indicating a complete distribution.

If X and Y are independent of each other, the joint distribution can be simplified as the product of their individual distributions, or marginals. This means that if you know the probability distribution of X and the probability distribution of Y, you can multiply these distributions to get the joint distribution. For example, if the probability of X equals zero is 0.5 and the probability of Y equals zero is also 0.5, then the joint probability of X equals zero and Y equals zero would be 0.5 times 0.5, which equals 0.25.

Section: Marginal and Conditional Distributions

Given a joint distribution of X and Y, we can derive the marginal distribution of one variable by summing the joint probabilities over all possible values of the other variable. For instance, to find the marginal distribution of X, you would sum the probability of X equals x and Y equals y over all possible values of Y. This is referred to as the sum rule or the rule of total probability. Similarly, you can find the marginal distribution of Y by summing over all possible values of X.

Conditional distributions provide another layer of understanding. The conditional distribution of Y given X, denoted as the probability of Y equals y given X equals x, is calculated by dividing the joint probability of X equals x and Y equals y by the marginal probability of X equals x. This allows us to understand how Y behaves when X is known to take a particular value. Rearranging this equation gives us the product rule: the probability of X equals x and Y equals y equals the probability of X equals x times the probability of Y equals y given X equals x. This is a useful way to think about the relationships between variables.

Section: Independence and Conditional Independence

Two variables X and Y are said to be unconditionally or marginally independent if the joint distribution can be expressed as the product of the marginals, i.e., the probability of X equals x and Y equals y equals the probability of X equals x times the probability of Y equals y. This means that knowing the value of X provides no information about the value of Y and vice versa. This property can be extended to more than two variables. A set of variables is mutually independent if the joint distribution can be expressed as the product of their individual distributions for all subsets of the variables.

However, in real-world scenarios, unconditional independence is rare. Most variables are influenced by other variables in some way. More common is conditional independence, where two variables are independent given the value of a third variable. For example, X and Y are conditionally independent given Z if the probability of X equals x and Y equals y given Z equals z equals the probability of X equals x given Z equals z times the probability of Y equals y given Z equals z. This means that once we know the value of Z, knowing X provides no additional information about Y. Conditional independence is a powerful concept that allows us to simplify complex joint distributions, which can be represented using graphical models.

Understanding these concepts of joint, marginal, and conditional distributions is fundamental in probabilistic machine learning. They provide the basis for many models and algorithms, enabling us to capture and reason about the dependencies and independencies in complex data. This understanding lays the groundwork for more advanced topics like Bayesian networks and Markov models, which rely heavily on these foundational ideas.
Section: Mean of a Distribution

The mean, or expected value, is a crucial measure of a distribution that provides a sense of the central location of the random variable. For continuous random variables, the mean is calculated by integrating the product of the variable's value and its probability density over all possible values. If this integral is not finite, then the mean is not defined. For discrete random variables, the mean is calculated by summing the product of each possible value and its probability. This calculation is only meaningful if the values of the random variable are ordered in some way, such as integer counts.

One key property of the mean is that it is a linear operator. This means that if you have a linear transformation of a random variable, such as "aX plus b," the expected value of this transformation is "a times the expected value of X plus b." For a set of random variables, the expectation of their sum is the sum of their individual expectations. If the variables are independent, the expectation of their product is the product of their individual expectations. This linearity property makes the mean a very useful tool in both theoretical and applied contexts.

Section: Variance of a Distribution

Variance measures the spread or variability of a distribution. It is defined as the expected value of the squared deviation of the variable from its mean. For continuous random variables, this involves integrating the squared difference between the variable and its mean, multiplied by the probability density, over all possible values. For discrete random variables, this involves summing the squared differences multiplied by their probabilities. The variance provides a quantitative measure of how much the values of the random variable differ from the mean.

The variance can be broken down into the expectation of the square of the variable minus the square of the mean. This gives us a useful result: the expectation of the square of a variable equals the variance plus the square of the mean. The standard deviation, which is the square root of the variance, provides a measure of spread in the same units as the variable itself. The variance of a shifted and scaled version of a random variable is given by the square of the scaling factor times the original variance. For a set of independent random variables, the variance of their sum is the sum of their individual variances. The variance of their product involves more complex calculations but can be derived through a series of steps.

Section: Mode of a Distribution

The mode of a distribution is the value that has the highest probability or density. In other words, it is the most likely value of the random variable. However, distributions can be multimodal, meaning they have multiple modes, and these modes may not provide a good summary of the distribution as a whole. The mode is often used in descriptive statistics to give a quick sense of the most common value in a dataset, but it is less informative for datasets with multiple peaks.

Section: Conditional Moments

Conditional moments are used when dealing with dependent random variables. The law of iterated expectations, or the law of total expectation, states that the expectation of a random variable can be calculated by taking the expectation of its conditional expectation given another variable. This provides a way to break down complex expectations into simpler parts, making them easier to calculate and understand. For instance, if we have two random variables, X and Y, the expectation of X can be broken down into the expectation of the conditional expectation of X given Y. This law is particularly useful in scenarios where we have a hierarchical structure or where dependencies between variables can be exploited to simplify calculations.

Section: Chapter Summary

1. **Probability Theory**: Probability quantifies uncertainty and aids in making informed decisions. It has two main interpretations: frequentist (long-run frequency) and Bayesian (measure of belief).

2. **Sources of Uncertainty**: These include ignorance of underlying mechanisms and inherent randomness in data generation.

3. **Limitations of Summary Statistics**: Summary statistics like mean and variance may not capture data complexity, illustrated by Anscombe's quartet and the Datasaurus Dozen.

4. **Bayes' Rule**: Bayes' theorem updates beliefs based on new evidence, with applications in medical diagnostics and decision-making scenarios like the Monty Hall problem.

5. **Likelihood and Bayesian Inference**: Likelihood represents the probability of observed data given a hypothesis. Bayesian inference combines likelihood with prior beliefs to update understanding.

6. **Bernoulli and Binomial Distributions**: Used to model binary events, with Bernoulli for single trials and Binomial for repeated trials.

7. **Logistic Function**: The sigmoid function is used in binary logistic regression to predict probabilities based on input features.

8. **Categorical and Multinomial Distributions**: Extend the Bernoulli distribution to multiple outcomes, with the softmax function used to convert logits into a probability distribution.

9. **Gaussian Distribution**: Widely used in statistical modeling due to its simplicity and properties, such as maximizing entropy and being a limit case for sums of random variables.

10. **Dirac Delta Function**: Represents an idealized point source or instantaneous impulse, arising as the variance of a Gaussian distribution approaches zero.

11. **Student's t-Distribution**: More robust to outliers than the Gaussian distribution, useful for small sample sizes and data with outliers.

12. **Monte Carlo Approximation**: A technique for approximating distributions by drawing samples, useful for complex or unknown distributions.

13. **Joint, Marginal, and Conditional Distributions**: Fundamental concepts in probabilistic modeling, crucial for understanding dependencies between variables.

14. **Moments of a Distribution**: Include the mean, variance, and mode, providing measures of central tendency, spread, and most likely values. Conditional moments break down complex expectations into simpler parts.
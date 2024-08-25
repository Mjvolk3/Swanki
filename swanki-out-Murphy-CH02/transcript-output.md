**Introduction to Probability: Univariate Models**

**What is Probability?**

Probability theory is a fascinating and essential branch of mathematics that helps us quantify uncertainty and make informed decisions. It was eloquently summed up by Pierre Laplace in 1812 as "nothing but common sense reduced to calculation." At its core, probability allows us to make predictions about the likelihood of various outcomes. For instance, when we say that a fair coin has a 50 percent chance of landing heads, we are using probability to express our expectations.

There are two main interpretations of probability: the frequentist and the Bayesian approach. The frequentist interpretation views probability as the long-run frequency of an event occurring through repeated trials. For example, the statement about the coin means that if we flip it many times, it will land heads approximately half the time. In contrast, the Bayesian interpretation sees probability as a measure of our uncertainty or belief about an event. This view is more flexible, allowing us to deal with one-off events, such as predicting whether the polar ice cap will melt by 2030. Since we can’t rely on repeated trials for such unique events, the Bayesian approach quantifies our uncertainty based on available information.

Adopting the Bayesian interpretation in our discussions makes it possible to model our uncertainty in a broader range of scenarios. For example, even if an event cannot happen multiple times, we can still assign a probability to it based on our current knowledge and beliefs. The basic rules of probability, such as how probabilities add up and multiply, remain consistent across both interpretations.

**Types of Uncertainty**

Uncertainty in our predictions can arise from two main sources. The first source is our ignorance of the underlying mechanisms producing the data. This type of uncertainty is often due to hidden factors or variables that we do not fully understand or observe. For instance, consider a probability density function (PDF) of a mixture of two one-dimensional Gaussians, where each Gaussian component has its own mean and variance. The mixture model, with equal mixing coefficients, shows two distinct peaks, each representing different possible states or conditions. This reflects our uncertainty about which state the data might belong to.

The second source of uncertainty stems from the inherent randomness in the data generation process. Even if we completely understand the mechanisms at play, the outcomes can still be random. For example, flipping a fair coin is inherently random, and no amount of knowledge about the coin can predict the outcome of a single flip with certainty. This randomness is captured by the probability distribution, which tells us the likelihood of various outcomes.

To elucidate these ideas, let’s consider the law of total expectation, which states that the expected value of a random variable can be found by taking the expected values conditional on another variable and then averaging them. For instance, consider the lifetime of a lightbulb produced in different factories. If factory 1 produces bulbs with an average lifetime of 5000 hours and factory 2 produces bulbs with an average of 4000 hours, and factory 1 supplies 60 percent of the bulbs, then the expected lifetime of a random bulb is a weighted average of these lifetimes, reflecting both the variability within each factory and the distribution of production across factories.

**Limitations of Summary Statistics**

While summary statistics like mean and variance are useful for condensing information about a dataset, they often fail to capture the full complexity of the data. This limitation is strikingly illustrated by Anscombe's quartet, which consists of four different datasets that share identical summary statistics but have vastly different distributions. The quartet highlights the importance of data visualization in understanding the true nature of data.

For example, one dataset in the quartet may show a linear relationship, another a quadratic curve, and yet another may have an outlier that skews the perception of the data. Despite identical means, variances, and correlations, the visual representations reveal different underlying patterns. This underscores the danger of relying solely on summary statistics without visualizing the data.

An even more dramatic example is the Datasaurus Dozen, a collection of datasets including one that forms the shape of a dinosaur. All these datasets have the same summary statistics but look completely different when plotted. This collection was created using a technique called simulated annealing, which optimizes the datasets to match specific statistical properties while forming distinct shapes. This clearly demonstrates that identical statistical summaries can correspond to very different real-world distributions, emphasizing the necessity of visual data analysis.

**Bayes' Rule**

Bayes' theorem is a cornerstone of probability theory, much like Pythagoras's theorem is for geometry. It provides a powerful framework for updating our beliefs in the light of new evidence. According to Bayes' rule, the probability of a hypothesis given some observed data is proportional to the prior probability of the hypothesis multiplied by the likelihood of the data given the hypothesis.

In simpler terms, Bayes' rule allows us to update our prior beliefs (what we thought before observing the data) based on the likelihood of the observed evidence. This updated belief is known as the posterior probability. The formula is straightforward: the posterior probability is equal to the prior probability times the likelihood, divided by the probability of the observed data. This process helps us refine our predictions and make more informed decisions.

For example, if we are trying to determine the probability of a medical condition given a positive test result, Bayes' rule lets us combine our prior knowledge about the prevalence of the condition with the accuracy of the test. This yields a more accurate assessment of the likelihood of having the condition, taking into account both the initial belief and the new evidence provided by the test result. Thus, Bayes' rule is an essential tool for making rational inferences and updating our understanding of the world.
### Likelihood and Bayesian Inference

Let’s dive into the concept of likelihood and its role in Bayesian inference. When we talk about the function $p(Y=y \mid H=h)$, we refer to the likelihood. Here, $Y$ represents the observed data, and $H$ represents the hypothesis or hidden state. The likelihood is a function of the hidden state $h$, given that the data $y$ is fixed. Importantly, the likelihood is not a probability distribution because it does not sum to one across all possible values of $h$.

To understand Bayesian inference, we start by combining the likelihood with the prior distribution $p(H=h)$. The prior represents our initial beliefs about the hidden state before observing any data. By multiplying the prior $p(H=h)$ by the likelihood $p(Y=y \mid H=h)$ for each possible $h$, we get the unnormalized joint distribution $p(H=h, Y=y)$. This joint distribution combines our prior beliefs with the information provided by the observed data.

To normalize this joint distribution and obtain a proper probability distribution, we divide by the marginal likelihood $p(Y=y)$. This marginal likelihood is computed by summing over all possible values of the hidden state $H$, which gives us the total probability of observing the data $y$. The normalized distribution, $p(H=h \mid Y=y)$, is called the posterior distribution and represents our updated beliefs about the hidden state after observing the data.

### Example: Testing for COVID-19

Let's apply Bayesian inference to a practical example: testing for COVID-19. Suppose you want to determine if you are infected with COVID-19 based on the result of a diagnostic test. Here, $H=1$ denotes being infected, and $H=0$ denotes not being infected. If the test result is positive, $Y=1$, and if it is negative, $Y=0$. We aim to compute the probability of being infected given the observed test result, $p(H=h \mid Y=y)$.

To do this, we need two key pieces of information: the test's sensitivity and specificity. Sensitivity, or true positive rate, is the probability of a positive test given that you are infected, denoted as $p(Y=1 \mid H=1)$. Specificity, or true negative rate, is the probability of a negative test given that you are not infected, denoted as $p(Y=0 \mid H=0)$. We also need the prior probability of being infected, $p(H=1)$, which represents the prevalence of the disease in your area.

Suppose the sensitivity of the test is 87.5% and the specificity is 97.5%. The prior probability of being infected is 10%, reflecting the prevalence in New York City in Spring 2020. If you test positive, the posterior probability of being infected is calculated using Bayes' rule: we multiply the sensitivity by the prior probability and then normalize by the total probability of a positive test. This results in a 79.5% chance of being infected if the test is positive. Conversely, if the test is negative, the probability of being infected is much lower, at 1.4%.

### Example: The Monty Hall Problem

Now, let’s explore a more playful application of Bayesian inference: the Monty Hall problem. Imagine a game show with three doors, one of which hides a prize. You pick one door, and the host, who knows where the prize is, opens another door that does not reveal the prize. You then have the option to stick with your initial choice or switch to the remaining unopened door.

Intuition might suggest that it makes no difference whether you switch or stay. However, using Bayes' rule, we can show that switching doors actually doubles your chances of winning. Initially, each door has an equal probability of hiding the prize, so the prior probabilities are one-third for each door.

When the host opens a door, this action provides additional information. If the host opens door 3, for instance, the probabilities need to be updated. Given that the host's choice is influenced by the location of the prize, the likelihoods are different depending on where the prize actually is. Bayes' rule helps us update the probabilities, showing that the probability of the prize being behind the door you initially chose is one-third, while the probability of it being behind the other unopened door is two-thirds. Thus, you should switch doors to maximize your chances of winning.

### Inverse Problems

Inverse problems involve inferring unknown states of the world from observed data, essentially reversing the process of prediction. For instance, consider trying to infer a three-dimensional shape from a two-dimensional image. This is challenging because multiple three-dimensional shapes can project to the same two-dimensional image, making the problem fundamentally ill-posed.

To address inverse problems, we use Bayes' rule to compute the posterior distribution over the possible states of the world. This involves specifying a forward model, which gives the probability of observing the data given a particular state, and a prior distribution over the states. The posterior distribution then combines the prior information with the observed data to provide a probabilistic estimate of the true state. This approach is widely used in fields like computer vision and natural language understanding, where the goal is to infer hidden structures or meanings from observed data.
## Bernoulli and Binomial Distributions

### Definition of the Bernoulli Distribution

The Bernoulli distribution is one of the most fundamental probability distributions used to model binary events. Imagine flipping a coin where the probability of landing heads, denoted as \( \theta \), lies between 0 and 1. If we let \( Y = 1 \) represent the event where the coin lands heads and \( Y = 0 \) for tails, we can describe this scenario using the Bernoulli distribution. This means that the probability of heads \( p(Y = 1) \) is \( \theta \), and the probability of tails \( p(Y = 0) \) is \( 1 - \theta \).

Mathematically, we say that \( Y \) follows a Bernoulli distribution with parameter \( \theta \), which is written as \( Y \sim \text{Ber}(\theta) \). The probability mass function (pmf) for this distribution specifies the probabilities for each possible value of \( Y \). For \( Y = 0 \), the probability is \( 1 - \theta \), and for \( Y = 1 \), the probability is \( \theta \).

### Understanding the Binomial Distribution

The Bernoulli distribution is actually a special case of a broader distribution known as the binomial distribution. Suppose you repeat a Bernoulli trial \( N \) times—think of tossing the coin \( N \) times. Let \( s \) be the number of heads observed in these \( N \) trials. The number of heads \( s \) follows a binomial distribution, which is denoted as \( s \sim \text{Bin}(N, \theta) \).

The binomial distribution gives us the probability of observing exactly \( s \) heads in \( N \) trials. The formula involves the binomial coefficient, often referred to as "N choose s", which counts the number of different ways to choose \( s \) heads out of \( N \) trials. The binomial probability is then given by the product of this coefficient, \( \theta^s \), and \( (1 - \theta)^{N - s} \).

### Sigmoid (Logistic) Function

When predicting a binary outcome based on some input features, we often use a logistic function, also known as the sigmoid function. This function smoothly maps any real-valued number into a value between 0 and 1, making it ideal for probability predictions. 

The sigmoid function is defined as \( \sigma(a) = \frac{1}{1 + e^{-a}} \), where \( a \) is the input to the function. This S-shaped curve ensures that the output stays within the [0, 1] range, which is necessary for interpreting it as a probability. The sigmoid function can be viewed as a "soft" version of the Heaviside step function, which jumps from 0 to 1 at a certain threshold.

The sigmoid function has several important properties. For instance, its derivative is \( \sigma(a) \cdot (1 - \sigma(a)) \), which is useful in optimization algorithms during model training. The inverse of the sigmoid function is known as the logit function, mapping probabilities back to log-odds.

### Binary Logistic Regression

In binary logistic regression, we use the sigmoid function to model the probability of a binary outcome given some input features. The model predicts the probability that the output \( y \) is 1 (e.g., the coin lands heads or the flower is of a particular species) based on a linear combination of the input features \( \boldsymbol{x} \).

Formally, the conditional probability is given by \( p(y \mid \boldsymbol{x}, \boldsymbol{\theta}) = \text{Ber}(y \mid \sigma(\boldsymbol{w}^\top \boldsymbol{x} + b)) \), where \( \boldsymbol{w} \) and \( b \) are the parameters of the model. The logistic function \( \sigma \) ensures that the output of the linear combination is mapped to a valid probability.

For example, when applied to a 1-dimensional, 2-class version of the Iris dataset, logistic regression can classify flowers based on petal width. The decision boundary is the value of petal width where the probability of being a particular class (e.g., Virginica) is 0.5. As the petal width increases or decreases from this boundary, the model's confidence in its classification increases, illustrating the power and simplicity of logistic regression in binary classification tasks.
### 2.5 Categorical and Multinomial Distributions

To represent a distribution over a finite set of labels, which we’ll denote as 'y' taking values from 1 to C, we use the categorical distribution. This is an extension of the Bernoulli distribution to cases where the number of possible outcomes, C, is greater than two.

#### 2.5.1 Definition

The categorical distribution is a discrete probability distribution characterized by one parameter per class. Mathematically, it is represented as the product of the parameters raised to the power of an indicator function. In simpler terms, the probability that 'y' equals a specific class 'c' is given by the parameter associated with that class, denoted as theta sub c. These parameters must satisfy two constraints: each must lie between 0 and 1, inclusive, and the sum of all parameters must equal 1. This means there are actually only C-1 independent parameters because the final parameter can be determined by the sum constraint.

We can also represent the categorical distribution using a one-hot vector, which has C elements where all entries are zero except for the one corresponding to the class label, which is 1. For instance, if we have three classes, the one-hot encodings for classes 1, 2, and 3 would be (1,0,0), (0,1,0), and (0,0,1) respectively. This one-hot vector representation simplifies the categorical distribution into a form where the probability of each class is directly tied to the parameter associated with that class.

The categorical distribution is a special case of the multinomial distribution. Imagine rolling a C-sided die N times and counting the number of times each side appears. The resulting counts form a vector that follows a multinomial distribution. This distribution includes a multinomial coefficient representing the number of ways to divide a set of size N into subsets of specified sizes for each class. If N equals 1, the multinomial distribution simplifies to the categorical distribution.

### 2.5.2 Softmax Function

When dealing with conditional probabilities, we can define the probability of a class 'y' given some input 'x' and parameters 'theta' as a categorical distribution where the parameters are a function of 'x' and 'theta'. This function, denoted as 'f', must output a probability vector that sums to 1 and has each element between 0 and 1.

To achieve this, we often use the softmax function, also known as the multinomial logit function. The softmax function transforms a vector of values (called logits) into a probability distribution. It does this by exponentiating each logit, then normalizing these values by dividing by the sum of all exponentiated logits. This ensures the output values fall between 0 and 1 and sum to 1, making them valid probabilities.

The softmax function is particularly useful because it can smoothly interpolate between the argmax function, which selects the largest value and assigns it a probability of 1 while all others get 0, and a uniform distribution, where all values have equal probability. By introducing a temperature parameter, we can control this behavior. At high temperatures, the distribution becomes more uniform, while at low temperatures, it becomes more peaked around the highest value.

### 2.5.3 Multiclass Logistic Regression

In multiclass logistic regression, we use a linear predictor to model the logits, which are then passed through the softmax function to obtain probabilities. The linear predictor is a combination of a weight matrix and a bias vector applied to the input features.

For a given input 'x', the logits are computed as a weighted sum of the input features plus a bias term. These logits are then transformed by the softmax function to produce the probability for each class. This approach generalizes binary logistic regression to multiple classes. In the binary case, the softmax function simplifies to the logistic function, and we only need a single weight vector rather than multiple.

An example of this is fitting a multinomial logistic regression model to the Iris dataset, where the model predicts the species of an Iris flower based on its petal length and width. The decision boundaries in this case are linear, reflecting the linear nature of the logistic regression model. However, more complex boundaries can be modeled by transforming the input features, such as using polynomial features.

### 2.5.4 Log-Sum-Exp Trick

When working with the softmax function, we often encounter numerical stability issues due to the exponential operations involved. For instance, very large or very small values can lead to overflow or underflow errors.

To mitigate these issues, we use the log-sum-exp trick. This technique involves subtracting the maximum logit value from all logits before exponentiating them. By doing this, the largest exponentiated value becomes 1, ensuring that we avoid overflow. The resulting probabilities are then computed by normalizing these adjusted exponentiated values.

This trick is crucial for ensuring numerical stability when computing probabilities and is commonly used in the implementation of the cross-entropy loss function, which measures the difference between predicted and actual probability distributions.

### 2.6 Univariate Gaussian (Normal) Distribution

The Gaussian distribution, also known as the normal distribution, is the most widely used distribution for real-valued random variables. It is characterized by its mean and variance, which determine its location and spread.

#### 2.6.1 Cumulative Distribution Function

The cumulative distribution function (CDF) of a continuous random variable is the probability that the variable takes a value less than or equal to a given number. For the Gaussian distribution, the CDF is denoted by Phi and takes into account the mean and variance of the distribution.

The CDF is a monotonically non-decreasing function, meaning it never decreases as the input value increases. Using the CDF, we can compute the probability that a random variable lies within a specific interval by taking the difference of the CDF values at the endpoints of the interval.

Understanding the CDF is essential for working with probabilities and intervals in the context of continuous random variables, particularly when dealing with Gaussian distributions.
### Cumulative Distribution Function of the Gaussian Distribution

We start by exploring the concept of the cumulative distribution function, or CDF, of a Gaussian distribution. The CDF is a function that maps a value to the probability that a random variable will take a value less than or equal to that number. For a Gaussian distribution, this can be written as the integral of the probability density function, or PDF, from negative infinity to a given value \(y\). Essentially, this integral sums up all the probabilities up to \(y\).

One common implementation of the Gaussian CDF uses the error function, denoted as "erf". The error function is a special mathematical function that arises in probability, statistics, and partial differential equations. It is defined as twice the integral from zero to a particular value \(u\) of the exponential function \(e\) to the power of \(-t^2\), where \(t\) is a dummy variable of integration. This function is scaled by a factor involving the square root of pi to ensure it captures the correct probability mass.

In practical terms, when working with a Gaussian distribution characterized by a mean \( \mu \) and a variance \( \sigma^2 \), the CDF can be expressed using the error function. This allows us to determine the probability that a random variable will fall within a certain range, which is particularly useful in statistical modeling and hypothesis testing. For instance, if we set the mean to zero and the standard deviation to one, we obtain the standard normal distribution, which simplifies the calculations and is often used as a benchmark in statistics.

### Probability Density Function of the Gaussian Distribution

Next, let's delve into the probability density function, or PDF, of the Gaussian distribution. The PDF is essentially the derivative of the CDF and provides the likelihood of the random variable taking on a specific value. For the Gaussian distribution, the PDF is a bell-shaped curve that is symmetric around the mean \( \mu \). This curve is mathematically described by an exponential function that diminishes as one moves away from the mean, scaled by a normalization factor to ensure the total probability sums to one.

The Gaussian PDF is defined by two main parameters: the mean \( \mu \), which determines the center of the distribution, and the variance \( \sigma^2 \), which dictates the spread or width of the distribution. The normalization constant, which involves the square root of \(2\pi\) times the variance, ensures that the area under the curve equals one, satisfying the property of total probability.

One interesting property of the PDF is that it allows us to calculate the probability of the random variable falling within any given interval. For example, the probability that the variable \(Y\) falls between two values \(a\) and \(b\) is given by the integral of the PDF from \(a\) to \(b\). This is equivalent to the difference between the CDF values at \(b\) and \(a\). For very small intervals, the probability can be approximated by multiplying the PDF value at a point by the width of the interval, providing a practical way to understand the density at a specific location.

### Understanding Regression with Gaussian Output

Regression models often assume that the output variable follows a Gaussian distribution. In the simplest case, known as homoscedastic regression, the variance of the output is assumed to be constant and independent of the input variables. This means the spread of errors or deviations from the predicted mean remains the same regardless of the input values. Linear regression is a classic example where the mean of the output is modeled as a linear function of the input variables. The resulting model captures the central tendency of the data with a fixed spread around this central line.

However, in many real-world scenarios, the variance can change with different levels of the input variables. This leads to heteroscedastic regression, where the variability of the output depends on the input. In such cases, the Gaussian distribution used to model the output has a mean that is a linear function of the input but a variance that also changes with the input. This more flexible approach can better accommodate data where the spread of observations varies across the range of input values.

Visual representations, such as scatter plots with fitted regression lines and confidence intervals, help illustrate these concepts. In the case of homoscedastic regression, the intervals around the regression line are parallel, showing a constant spread. For heteroscedastic regression, these intervals can widen or narrow depending on the input values, reflecting the varying uncertainty in predictions.

### Importance of the Gaussian Distribution

The Gaussian distribution is extensively used in statistics and machine learning for several compelling reasons. Firstly, it has a simple mathematical form with only two parameters—the mean and the variance—which are easy to interpret and relate to the data. The mean reflects the central tendency, while the variance indicates the spread. This simplicity makes it a convenient choice for modeling.

Secondly, the central limit theorem provides a powerful justification for its use. This theorem states that the sum of a large number of independent random variables, regardless of their original distributions, tends to follow a Gaussian distribution. This underlies the rationale for using Gaussian distributions to model residual errors in various contexts.

Thirdly, the Gaussian distribution maximizes entropy, given the constraints of a specified mean and variance. This property means it makes the least number of assumptions about the data beyond these constraints, serving as a good default model in many situations. Its simplicity also leads to efficient computational methods, making it practical for a wide range of applications.

Historically, the Gaussian distribution was popularized by Carl Friedrich Gauss, although it was discovered earlier by other mathematicians. The term "normal distribution" is also used, but it can be misleading as it implies other distributions are "abnormal," which is not the case. The Gaussian distribution is special due to its unique properties and widespread applicability.

### Dirac Delta Function as a Limiting Case

The Dirac delta function is a concept that arises when considering the limit of a Gaussian distribution as its variance approaches zero. As the variance decreases, the Gaussian distribution becomes increasingly narrow and tall, concentrating its mass around the mean. In the limit, this results in an infinitely narrow spike at the mean, which is mathematically represented by the Dirac delta function. This function is zero everywhere except at a single point where it is infinitely high, and its integral over the entire real line is one.

The Dirac delta function is useful in various fields, including physics and engineering, as it can model idealized point sources or instantaneous impulses. In mathematical terms, it captures the idea of a distribution that is entirely concentrated at a single point, making it a powerful tool for theoretical analysis and practical applications.

In summary, understanding the Gaussian distribution, its properties, and extensions like the Dirac delta function provides a solid foundation for many statistical and machine learning models. These concepts are not only theoretically elegant but also practically useful in analyzing and interpreting real-world data.
### Section: Some Other Common Univariate Distributions

In this section, I’m going to introduce you to a few univariate distributions that are commonly used in statistics and machine learning. Each of these distributions has unique properties and applications, making them versatile tools for modeling various types of data.

### Student's t-Distribution

To start, let's discuss the Student's t-distribution. Unlike the Gaussian distribution, which is quite sensitive to outliers, the Student's t-distribution is more robust and can handle data with outliers effectively. The probability density function (pdf) of the Student's t-distribution is characterized by three parameters: the mean (μ), a scale parameter (σ), and the degrees of freedom (ν). The degrees of freedom, ν, play a crucial role in shaping the distribution. When ν is large, the Student's t-distribution approximates a Gaussian distribution, but for smaller values of ν, the distribution has heavier tails, making it more resistant to outliers.

Historically, this distribution was first published by William Sealy Gosset under the pseudonym "Student" because his employer, the Guinness brewery, did not allow him to publish under his name. The t-distribution is particularly useful in situations where the sample size is small or the data contain outliers. This robustness is visually evident in figure 2.16, which shows how both the Student and Laplace distributions remain relatively unaffected by outliers, unlike the Gaussian distribution, which gets significantly distorted.

### Cauchy Distribution

Next, when the degrees of freedom ν is set to 1, the Student's t-distribution transforms into the Cauchy distribution, also known as the Lorentz distribution. The Cauchy distribution has extremely heavy tails. For instance, while 95% of the values from a standard normal distribution fall between -1.96 and 1.96, the same percentage for a standard Cauchy distribution lies between approximately -12.7 and 12.7. This means that the Cauchy distribution has more probability mass in the tails compared to the Gaussian, and as a result, it does not have a well-defined mean or variance. This property can be both an advantage and a disadvantage depending on the application, but it makes the Cauchy distribution particularly useful in Bayesian modeling for positive reals with heavy tails.

### Laplace Distribution

Moving on, let's explore the Laplace distribution, also known as the double-sided exponential distribution. The Laplace distribution is another robust alternative to the Gaussian distribution. It has a peak at its mean, similar to the Gaussian, but its tails fall off more slowly, making it resilient to outliers. The pdf of the Laplace distribution is characterized by a location parameter (μ) and a scale parameter (b), and its variance is twice the square of the scale parameter. This distribution is used in various applications, including robust linear regression, where it helps to mitigate the influence of outliers on the model.

### Beta Distribution

Now, let’s consider the Beta distribution, which is defined over the interval [0,1]. The Beta distribution is parameterized by two positive parameters, a and b, which shape the distribution. Depending on the values of these parameters, the Beta distribution can take various forms, from uniform to highly skewed distributions. It is often used in Bayesian statistics to model the distribution of probabilities. For example, if both parameters are equal to 1, the Beta distribution is uniform. If both parameters are less than 1, the distribution becomes bimodal with spikes at 0 and 1. Conversely, if both parameters are greater than 1, the distribution is unimodal.

### Gamma Distribution

Finally, let's discuss the Gamma distribution, which is a flexible distribution for modeling positive real-valued random variables. It is parameterized by a shape parameter (a) and a rate parameter (b). The Gamma distribution is versatile and can take various shapes, making it suitable for a wide range of applications, including modeling waiting times in Poisson processes. Special cases of the Gamma distribution include the Exponential distribution, which is used to describe the time between events in a Poisson process.

In summary, understanding these distributions and their properties allows us to choose the right model for our data, ensuring that we can make accurate inferences and predictions. Each distribution has its strengths and is suited for different types of data and scenarios, making them invaluable tools in the field of statistics and machine learning.
### Empirical Distribution

Imagine we have a set of samples, say five in total, each representing a data point drawn from some unknown distribution. Our goal is to estimate the probability density function (pdf) and the cumulative distribution function (cdf) from these samples. This process of estimation from finite samples is what we call constructing the empirical distribution.

To approximate the pdf, we use delta functions, often visualized as spikes, centered on each sample point. Picture this as a graph where each sample is represented by a vertical line or spike, and the height of these lines indicates the density at that point. For five samples, each spike contributes equally to the overall density. The empirical pdf is essentially a sum of these spikes, and since we have five samples, each spike has a weight of one-fifth.

Now, let's consider the cumulative distribution function (cdf). The cdf gives us the probability that a random variable is less than or equal to a certain value. In the empirical case, this is visualized as a staircase function, where each step corresponds to a sample. For our set of five samples, the cdf increases by one-fifth at each sample point. This results in a step-like graph where the height of each step is one-fifth, reflecting the equal contribution of each sample to the cumulative probability.

### Chi-Squared and Inverse Gamma Distributions

The Chi-squared distribution is important in statistics, especially in hypothesis testing and the construction of confidence intervals. Defined by its degrees of freedom, denoted as "nu," it represents the distribution of the sum of the squares of "nu" standard normal variables. If you think about each of these normal variables as a measure of some random phenomenon, squaring them ensures all values are positive, and summing squares from multiple such phenomena gives you the Chi-squared distribution. This distribution is fundamental in assessing the variability of data from a theoretical perspective.

On the other hand, the Inverse Gamma distribution is a bit more complex. It's defined by two parameters: shape "a" and scale "b." This distribution is useful in Bayesian statistics and other areas where the reciprocal of a gamma-distributed variable is needed. It has particular properties, such as the mean and variance, which exist only under certain conditions for the shape parameter "a." Specifically, the mean exists if "a" is greater than one, and the variance exists if "a" is greater than two. This distribution helps in modeling scenarios where the rate or scale of a process is uncertain.

### Transformations of Random Variables

Transforming random variables is a powerful technique in probability and statistics, allowing us to understand how different operations affect the distributions of these variables. Let's start with a simple example: consider a random variable "x" that is uniformly distributed between zero and one. If we apply a transformation, say "y equals two times x plus one," this operation both stretches and shifts the distribution. Originally, the values of "x" ranged from zero to one. After the transformation, they now range from one to three, and the density adjusts accordingly to ensure the total probability remains one. This concept is visualized in a graph where the original and transformed distributions are compared.

If "x" is continuous, deriving the distribution of "y" involves working with cumulative distribution functions (cdfs). For an invertible transformation, which means you can reverse the operation, the pdf of "y" can be found by differentiating the cdf with respect to "y." This process involves a change of variables formula, which accounts for the rate of change of "x" with respect to "y." Essentially, it tells us how the density transforms under the function.

### Change of Variables: Multivariate Case

Extending these ideas to multiple dimensions, we deal with transformations involving multiple variables. Imagine transforming a two-dimensional space, such as shifting and rotating a square into a parallelogram. The transformation is represented by a matrix "A" and a vector "b." The determinant of matrix "A" gives us a measure of how the area (or volume in higher dimensions) changes under the transformation. This determinant is crucial in adjusting the density to ensure the total probability remains consistent.

For instance, when transforming from Cartesian coordinates to polar coordinates, the Jacobian matrix represents the partial derivatives of the transformation. The determinant of this Jacobian gives us the scaling factor needed to adjust the density appropriately. In this case, transforming from Cartesian to polar coordinates involves a radial component "r" and an angular component "theta," and the determinant of the Jacobian is "r," reflecting the radial scaling.

By understanding these transformations, we can effectively model and analyze how various operations impact the distributions of random variables, providing deeper insights into the underlying probabilistic processes.
### Geometric Interpretation of Polar to Cartesian Coordinate Transformation

Geometrically, when we look at the transformation from polar to Cartesian coordinates, we can visualize the area of a small shaded patch in the polar coordinate system. This is represented in Figure 2.21, where the shaded patch is defined by a small change in the radius, \( r \) to \( r + dr \), and a small change in the angle, \( \theta \) to \( \theta + d\theta \). The infinitesimal area of this patch is given by multiplying the radius, the small change in radius \( dr \), and the small change in angle \( d\theta \).

The area of this infinitesimal patch, therefore, is \( r \cdot dr \cdot d\theta \). This concept is crucial because it helps in understanding how density functions transform under a change of variables. Specifically, the probability that a point falls within this small patch is the density at the center of the patch times the size of the patch. This is represented as \( p_{r, \theta}(r, \theta) \cdot dr \cdot d\theta \).

When transforming this area into Cartesian coordinates, we need to account for the transformation of the density functions. The probability density function in Cartesian coordinates, \( p_{x_1, x_2}(x, y) \), can be related to the density function in polar coordinates through the transformation \( x = r \cos \theta \) and \( y = r \sin \theta \). The area \( r \cdot dr \cdot d\theta \) remains the same, and thus the density functions are related by \( p_{r, \theta}(r, \theta) \cdot dr \cdot d\theta = p_{x_1, x_2}(r \cos \theta, r \sin \theta) \cdot r \cdot dr \cdot d\theta \).

### Moments of a Linear Transformation

When dealing with linear transformations, we often seek to understand how moments like the mean and covariance transform. Suppose we have an affine function where \( \mathbf{y} = \mathbf{A} \mathbf{x} + \mathbf{b} \). To find the mean of \( \mathbf{y} \), we use the expectation operator. The expectation of \( \mathbf{y} \) is \( \mathbb{E}[\mathbf{y}] = \mathbb{E}[\mathbf{A} \mathbf{x} + \mathbf{b}] \).

Given that expectation is a linear operator, we can separate the terms, leading to \( \mathbb{E}[\mathbf{y}] = \mathbf{A} \mathbb{E}[\mathbf{x}] + \mathbf{b} \). If the mean of \( \mathbf{x} \) is denoted as \( \boldsymbol{\mu} \), then the mean of \( \mathbf{y} \) is \( \mathbf{A} \boldsymbol{\mu} + \mathbf{b} \).

For the covariance of \( \mathbf{y} \), recall that covariance measures how much two random variables vary together. The covariance of \( \mathbf{y} \), denoted as \( \operatorname{Cov}[\mathbf{y}] \), is given by \( \operatorname{Cov}[\mathbf{A} \mathbf{x} + \mathbf{b}] \). Since \( \mathbf{b} \) is a constant vector, it does not affect the covariance, leaving us with \( \mathbf{A} \operatorname{Cov}[\mathbf{x}] \mathbf{A}^\top \), where \( \boldsymbol{\Sigma} \) is the covariance matrix of \( \mathbf{x} \).

As a specific example, if \( y = \mathbf{a}^\top \mathbf{x} + b \), the variance of \( y \), denoted \( \mathbb{V}[y] \), can be computed as \( \mathbf{a}^\top \boldsymbol{\Sigma} \mathbf{a} \). This formula is particularly useful in scenarios like computing the variance of the sum of two scalar random variables by setting the appropriate vector \( \mathbf{a} \).

### The Convolution Theorem

Understanding the convolution theorem is essential when dealing with sums of random variables. Suppose \( y = x_1 + x_2 \), where \( x_1 \) and \( x_2 \) are independent random variables. If these variables are discrete, the probability mass function (pmf) for the sum can be computed as \( p(y = j) = \sum_k p(x_1 = k) p(x_2 = j - k) \). This summation runs over all possible values of \( k \).

For continuous random variables with probability density functions \( p_1(x_1) \) and \( p_2(x_2) \), the cumulative distribution function (cdf) of their sum \( y \) is given by an integral over the region where \( x_1 + x_2 \leq y \). The pdf for \( y \) is then the derivative of this cdf, yielding an integral of the form \( p(y) = \int p_1(x_1) p_2(y - x_1) dx_1 \).

This integral is known as the convolution of \( p_1 \) and \( p_2 \), denoted as \( p_1 \circledast p_2 \). For finite length vectors, this convolution can be visualized as a "flip and drag" operation, where one function is flipped and then dragged over the other, multiplying elementwise and summing the results.

A practical example of this is the distribution of the sum of two dice rolls. Each die has a uniform distribution over the integers 1 to 6. The resulting distribution for the sum, \( y = x_1 + x_2 \), is not uniform but forms a triangular shape, peaking at 7. This distribution resembles a Gaussian distribution as explained by the central limit theorem.

### The Central Limit Theorem

The central limit theorem is a foundational result in probability theory. It states that the sum of a large number of independent and identically distributed random variables, each with finite mean and variance, will approximately follow a normal distribution, regardless of the original distribution of the variables.

Consider \( N \) independent random variables, each with the same distribution, mean \( \mu \), and variance \( \sigma^2 \). Let \( S_N = \sum_{n=1}^N X_n \) be the sum of these variables. As \( N \) becomes large, the distribution of \( S_N \) approaches a normal distribution with mean \( N \mu \) and variance \( N \sigma^2 \).

Mathematically, this is represented by the pdf \( p(S_N = u) \), which approaches \( \frac{1}{\sqrt{2 \pi N \sigma^2}} \exp\left( -\frac{(u - N \mu)^2}{2 N \sigma^2} \right) \). This result explains why many naturally occurring distributions tend to be Gaussian, as they can be seen as the sum of many small independent contributions.

In Figure 2.1, we see examples of discrete distributions on a state space. In one, all outcomes are equally likely, representing a uniform distribution. In another, all probability mass is concentrated on a single outcome, representing a degenerate or delta distribution. These visualizations help illustrate fundamental concepts in probability, such as how different distributions can be characterized and compared.
### **Uniform and Degenerate Distributions**

On the left side, we have a uniform distribution, where the probability of any specific value within the distribution is constant. Here, this is denoted as one-fourth. On the right side, we have a degenerate distribution, which can be thought of as a distribution that assigns a probability of one to a single point – in this case, the value one. This is represented by an indicator function that equals one if and only if the variable is one. Essentially, this means our random variable is always equal to one, highlighting that random variables can also take on constant values.

### **Continuous Random Variables**

When dealing with real-valued quantities, we refer to them as continuous random variables. Unlike discrete random variables, which can take on a finite or countable set of values, continuous random variables can take any value within a given range. This means we can't list all possible values, but we can consider intervals on the real line. By associating events with these intervals, we can use methods similar to those for discrete random variables. The idea is that as we make these intervals smaller and smaller, we approach the notion of the probability of the random variable taking on a specific value.

### **Cumulative Distribution Function (cdf)**

The cumulative distribution function, or cdf, is a fundamental concept for continuous random variables. Let's define three events: A is the event that our random variable X is less than or equal to some value a; B is the event that X is less than or equal to some value b, where b is greater than a; and C is the event that X lies between a and b. Because A and C are mutually exclusive, the probability of B, which can be thought of as A or C, is simply the sum of their probabilities. Therefore, the probability that X lies in the interval between a and b is the probability of B minus the probability of A.

### **Central Limit Theorem**

The central limit theorem is a key concept in statistics. It states that as you increase the number of samples, the distribution of the sample means will approach a normal distribution, regardless of the original distribution of the data. Figures accompanying this discussion typically show histograms of sample means for different sample sizes. For instance, one histogram might show the distribution for a single sample, while another shows the distribution for five samples. As the number of samples increases, the shape of the histogram becomes more bell-shaped, illustrating the central limit theorem in action.

### **Monte Carlo Approximation**

Monte Carlo approximation is a powerful technique used when it's difficult to compute the distribution of a function of a random variable analytically. Instead, we draw a large number of samples from the random variable's distribution and use these samples to approximate the desired distribution. For example, if we have a random variable x uniformly distributed between -1 and 1, and we want to find the distribution of y, where y is x squared, we can draw many samples of x, compute their squares, and then look at the resulting distribution of y. This method, named after the famous Monte Carlo casino, is widely used in fields such as statistical physics and machine learning.

### **Probability Density Function (pdf)**

The probability density function, or pdf, is the derivative of the cdf. The pdf tells us the density of the probability at a specific point. For continuous variables, we can't talk about the probability of the variable being exactly equal to a specific value; instead, we talk about the probability of the variable lying within a small interval around that value. The probability is approximately the value of the pdf at that point times the width of the interval. Visual aids often illustrate this concept with a bell-shaped curve for the normal distribution, showing how the density changes across different values.

### **Quantiles**

Quantiles are values that divide the probability distribution into intervals with equal probabilities. The most familiar quantile is the median, which divides the distribution into two equal halves. The cdf's inverse function, called the inverse cdf or quantile function, helps find these quantile values. For example, in a standard normal distribution, the 0.025 and 0.975 quantiles correspond to the points that enclose the central 95% of the distribution. These points are approximately -1.96 and 1.96, respectively, for a standard normal distribution. Quantiles are useful for understanding the spread and central tendency of the distribution.

By breaking down these concepts, we can see that probability and statistics offer powerful tools for understanding random variables and their behaviors. Whether we're dealing with uniform, degenerate, or continuous distributions, or applying the central limit theorem and Monte Carlo methods, these foundational ideas help us make sense of the randomness inherent in the world around us.
### Understanding Probabilistic Machine Learning: Joint, Marginal, and Conditional Distributions

#### Sets of Related Random Variables

When dealing with related random variables, it's crucial to understand the concept of joint distributions. Let's consider two random variables, X and Y. The joint distribution of these two variables can be expressed as the probability that X takes a specific value, and Y takes another specific value, simultaneously. This is denoted as p(X equals x, Y equals y). If both X and Y can only take on a finite number of values, we can represent the joint distribution in a two-dimensional table where each entry corresponds to a specific pair of values for X and Y, and the sum of all entries in the table equals one.

For instance, let's consider a simple example with binary variables X and Y. If we create a table where X and Y can each be either 0 or 1, and we fill in the table with probabilities for each pair, we might get something like 0.2 for X equals 0 and Y equals 0, 0.3 for X equals 0 and Y equals 1, and so on. The sum of all these values in the table will be 1, indicating a complete distribution.

If X and Y are independent of each other, the joint distribution can be simplified as the product of their individual distributions, or marginals. This means that if you know the probability distribution of X and the probability distribution of Y, you can multiply these distributions to get the joint distribution. For example, if p(X equals 0) is 0.5 and p(Y equals 0) is also 0.5, then the joint probability p(X equals 0, Y equals 0) would be 0.5 times 0.5, which equals 0.25.

#### Marginal and Conditional Distributions

Given a joint distribution of X and Y, we can derive the marginal distribution of one variable by summing the joint probabilities over all possible values of the other variable. For instance, to find the marginal distribution of X, you would sum p(X equals x, Y equals y) over all possible values of Y. This is referred to as the sum rule or the rule of total probability. Similarly, you can find the marginal distribution of Y by summing over all possible values of X.

Conditional distributions provide another layer of understanding. The conditional distribution of Y given X, denoted as p(Y equals y given X equals x), is calculated by dividing the joint probability p(X equals x, Y equals y) by the marginal probability p(X equals x). This allows us to understand how Y behaves when X is known to take a particular value. Rearranging this equation gives us the product rule: p(X equals x, Y equals y) equals p(X equals x) times p(Y equals y given X equals x). This is a useful way to think about the relationships between variables.

#### Independence and Conditional Independence

Two variables X and Y are said to be unconditionally or marginally independent if the joint distribution can be expressed as the product of the marginals, i.e., p(X equals x, Y equals y) equals p(X equals x) times p(Y equals y). This means that knowing the value of X provides no information about the value of Y and vice versa. This property can be extended to more than two variables. A set of variables is mutually independent if the joint distribution can be expressed as the product of their individual distributions for all subsets of the variables.

However, in real-world scenarios, unconditional independence is rare. Most variables are influenced by other variables in some way. More common is conditional independence, where two variables are independent given the value of a third variable. For example, X and Y are conditionally independent given Z if p(X equals x, Y equals y given Z equals z) equals p(X equals x given Z equals z) times p(Y equals y given Z equals z). This means that once we know the value of Z, knowing X provides no additional information about Y. Conditional independence is a powerful concept that allows us to simplify complex joint distributions, which can be represented using graphical models.

### Moments of a Distribution

#### Mean of a Distribution

The mean, or expected value, of a distribution provides a central measure of the distribution. For continuous random variables, the mean is calculated by integrating the variable's value times its probability density over all possible values. If this integral is not finite, the mean is not defined. For discrete random variables, the mean is calculated by summing the product of each possible value and its probability. This calculation is only meaningful if the values of the random variable are ordered in some way, such as integer counts.

One key property of the mean is that it is a linear operator. This means that if you have a linear transformation of a random variable, such as aX plus b, the expected value of this transformation is a times the expected value of X plus b. For a set of random variables, the expectation of their sum is the sum of their individual expectations. If the variables are independent, the expectation of their product is the product of their individual expectations.

#### Variance of a Distribution

Variance measures the spread or variability of a distribution. It is defined as the expected value of the squared deviation of the variable from its mean. For continuous random variables, this involves integrating the squared difference between the variable and its mean, times the probability density, over all possible values. For discrete random variables, this involves summing the squared differences times their probabilities.

The variance can be broken down into the expectation of the square of the variable minus the square of the mean. This gives us a useful result: the expectation of the square of a variable equals the variance plus the square of the mean. The standard deviation, which is the square root of the variance, provides a measure of spread in the same units as the variable itself.

The variance of a shifted and scaled version of a random variable is given by the square of the scaling factor times the original variance. For a set of independent random variables, the variance of their sum is the sum of their individual variances. The variance of their product involves more complex calculations but can be derived through a series of steps.

#### Mode of a Distribution

The mode of a distribution is the value that has the highest probability or density. In other words, it is the most likely value of the random variable. However, distributions can be multimodal, meaning they have multiple modes, and these modes may not provide a good summary of the distribution as a whole.

#### Conditional Moments

Conditional moments are used when dealing with dependent random variables. The law of iterated expectations, or the law of total expectation, states that the expectation of a random variable can be calculated by taking the expectation of its conditional expectation given another variable. This provides a way to break down complex expectations into simpler parts, making them easier to calculate and understand.
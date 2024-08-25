### Single-layer Networks: Regression

In this chapter, I delve into the fundamental concepts behind neural networks using the framework of linear regression. This framework was briefly introduced when discussing polynomial curve fitting. A linear regression model can be seen as a simple form of a neural network with a single layer of learnable parameters. While single-layer networks might not be highly effective in practical applications, their simplistic nature provides an excellent foundation for understanding core concepts. These foundational concepts will be crucial as we move towards discussing deep neural networks in later sections.

### Decision Theory

In the context of regression, we model a conditional probability distribution, denoted as \( p(t \mid \mathbf{x}) \). Specifically, we assume that this conditional probability is Gaussian, meaning it follows a bell curve shape centered around a mean \( y(\mathbf{x}, \mathbf{w}) \) which depends on the input \( \mathbf{x} \) and parameters \( \mathbf{w} \), with a variance \( \sigma^2 \). Both the parameters \( \mathbf{w} \) and the variance \( \sigma^2 \) can be learned from data using a method called maximum likelihood. The result is a predictive distribution that can be expressed as a normal distribution with a mean \( y(\mathbf{x}, \mathbf{w}_{\text{ML}}) \) and variance \( \sigma_{\text{ML}}^2 \).

This predictive distribution reflects our uncertainty about the value of \( t \) given a new input \( \mathbf{x} \). However, in many practical scenarios, we need to predict a specific value for \( t \) rather than an entire distribution. For instance, if our goal is to determine the optimal radiation dose for treating a tumor, the model might predict a distribution over possible doses. We then need to use this distribution to decide on a specific dose. This decision-making process involves two stages: the inference stage and the decision stage. In the inference stage, we use training data to determine the predictive distribution \( p(t \mid \mathbf{x}) \). In the decision stage, we use this distribution to determine a specific value \( f(\mathbf{x}) \), which is optimal according to some criterion. This is typically done by minimizing a loss function that depends on the predictive distribution and the function \( f \).

One intuitive approach might be to choose the mean of the conditional distribution as our prediction, so we would use \( f(\mathbf{x}) = y(\mathbf{x}, \mathbf{w}) \). Sometimes this intuition is correct, but other times it can lead to poor results. To formalize this process and understand when this intuition applies, we use a framework called decision theory.

### Loss Functions and Expected Loss

When choosing a value \( f(\mathbf{x}) \) for our prediction, we incur a penalty or cost if the true value is \( t \). This penalty is determined by a loss function, denoted as \( L(t, f(\mathbf{x})) \). Since we do not know the true value of \( t \), we minimize the expected loss, which is the average penalty over all possible values of \( t \). This expected loss is given by integrating the loss function over the joint distribution of both the input \( \mathbf{x} \) and the target variable \( t \).

A common choice for the loss function in regression problems is the squared loss, which is the square of the difference between \( f(\mathbf{x}) \) and \( t \). The expected squared loss can be written as the integral of this squared difference over the joint distribution of \( \mathbf{x} \) and \( t \).

Our goal is to choose \( f(\mathbf{x}) \) to minimize this expected squared loss. If we assume \( f(\mathbf{x}) \) is a completely flexible function, we can use a mathematical tool called the calculus of variations to formally derive the optimal \( f(\mathbf{x}) \). The result is that the optimal \( f(\mathbf{x}) \) is the conditional average of \( t \) given \( \mathbf{x} \), also known as the regression function.

### The Regression Function

The regression function is the conditional average of \( t \) given \( \mathbf{x} \), denoted as \( \mathbb{E}[t \mid \mathbf{x}] \). For a Gaussian conditional distribution, this conditional mean is simply \( y(\mathbf{x}, \mathbf{w}) \). This result shows that the optimal least-squares predictor is given by the conditional mean. The variance term in the loss function represents the intrinsic variability of the target data and can be considered as noise, which is independent of \( f(\mathbf{x}) \).

While the squared loss is a common choice, it is not the only one. Another example is the Minkowski loss, which generalizes the squared loss by raising the absolute difference between \( f(\mathbf{x}) \) and \( t \) to a power \( q \). When \( q = 2 \), it reduces to the squared loss. Depending on the value of \( q \), the Minkowski loss can be more or less sensitive to outliers. For instance, when \( q = 1 \), it corresponds to the absolute loss, and when \( q \) approaches 0, it corresponds to the mode of the distribution.

### Flexibility and Practical Application

The calculus of variations used in deriving the optimal regression function assumes that we can optimize over all possible functions \( f(\mathbf{x}) \). While any parametric model we use in practice is limited in the range of functions it can represent, deep neural networks offer a highly flexible class of functions. These networks can approximate any desired function to a high degree of accuracy, making them powerful tools for regression and other tasks.

To understand the regression problem further, we can re-examine the squared term in the loss function by expanding it. This expansion shows that the optimal solution minimizes the term involving the difference between \( f(\mathbf{x}) \) and the conditional average \( \mathbb{E}[t \mid \mathbf{x}] \), reaffirming that the least-squares predictor is the conditional mean.

In summary, the concepts discussed in this chapter lay the groundwork for more complex models and methods in neural networks and machine learning. By understanding the fundamental principles of regression and decision theory, we can build more sophisticated models that are better suited to a wide range of practical applications.
### The Bias-Variance Trade-off

In the realm of linear models for regression, we frequently grapple with the challenge of balancing model complexity and avoiding over-fitting. This is where the concept of the bias-variance trade-off becomes crucial. Imagine you have a model trained to predict outcomes based on a set of data. If your model is too simple, it might not capture the underlying patterns in the data accurately, leading to high bias. Conversely, if the model is too complex, it might fit the training data too closely, including its noise, leading to high variance.

To better understand this trade-off, consider the frequentist perspective of model complexity. Here, we not only focus on how well the model fits the data but also on how the model generalizes to unseen data. The bias refers to the error introduced by approximating a real-world problem, which may be complex, by a simplified model. On the other hand, variance refers to the error introduced by the model's sensitivity to small fluctuations in the training set.

To illustrate, let's delve into the expected squared loss, which can be decomposed into three components: bias squared, variance, and noise. The noise term represents the inherent unpredictability in the data that cannot be captured by any model. Our objective is to minimize the expected loss by finding the optimal balance between bias and variance. This balance ensures that the model is neither too simplistic, failing to capture essential trends (high bias), nor too complex, capturing noise as if it were a significant trend (high variance).

### Understanding the Bias-Variance Decomposition

Let’s consider the mathematical formulation of the expected squared loss. The expected squared loss, which measures the average discrepancy between the predicted values and the actual values, can be broken down into components that reflect bias, variance, and noise. Here’s how it works: the squared bias component measures how much the average model prediction diverges from the true model. The variance component measures the variability of the model prediction for different training sets. By adding these components, we understand how model complexity impacts prediction accuracy.

For a given data set, if we run our learning algorithm multiple times with different training sets, we will get different prediction functions. The goal is then to average out these functions to assess the overall performance of the learning algorithm. This is captured by considering the squared difference between the prediction function and the true regression function, averaged over many data sets. This decomposition helps us see that the expected squared loss is the sum of the squared bias, the variance, and the noise.

In simpler terms, bias is about the accuracy of our predictions on average, while variance is about the consistency of our predictions across different training sets. High bias means the model is systematically off from the true values, whereas high variance means the model predictions are scattered and inconsistent. The noise term represents the irreducible error, which is the part of the error that remains no matter how well our model performs.

### Illustrative Example: Sinusoidal Data Set

To provide a more tangible example, consider fitting a sinusoidal function to a data set. We generate multiple data sets from the sinusoidal curve and fit models with different regularization parameters. When the regularization parameter is high, the model becomes rigid, leading to low variance but high bias. This means the model predictions are consistent but systematically off from the true sinusoidal function. Conversely, with a low regularization parameter, the model becomes flexible, leading to low bias but high variance. The predictions closely follow the true function but vary significantly across different training sets.

By averaging these multiple model fits, we observe that a good balance between bias and variance leads to the best predictive performance. This example underscores the importance of regularization in controlling model complexity and achieving a balance that minimizes the expected loss. The bias-variance trade-off is a fundamental concept that helps us understand the limitations and capabilities of our models, guiding us to make informed decisions about model selection and parameter tuning.

In summary, the bias-variance trade-off is about finding the sweet spot where the model is neither too simple nor too complex. This balance is essential for building models that generalize well to new data, providing accurate and reliable predictions. Understanding and managing this trade-off is key to successful machine learning and statistical modeling.
**The Balance Between Variance and Bias**

Let's explore the delicate balance between variance and bias in the context of model complexity, specifically using a regularization parameter denoted by lambda. Imagine you have a set of data points that you want to fit with a model, and you're adjusting how complex this model can be by tweaking lambda.

When lambda is very small, say around negative three, the model becomes highly flexible. This flexibility allows it to closely follow the data points, including any noise present in the data. In practical terms, if you were to plot multiple fits of the model on several datasets, you'd see that each fit (represented by red curves) would vary significantly. However, because the model is so attuned to the specific data points, it might not generalize well to new, unseen data. This situation is known as overfitting—the model has low bias but high variance.

Conversely, when lambda is very large (imagine the top row of the plots), the model becomes very rigid. It can't capture the intricacies of the data and thus shows high bias—it's too simplistic. The fits look almost the same across different datasets, meaning low variance, but they are not close to the true underlying function you're trying to model.

Now, what happens in the middle ground? With an optimal value of lambda, the model strikes a balance between bias and variance. It captures the essential trends in the data without overfitting to noise. This sweet spot is where the model's average fit is closest to the true function. The visualizations of these fits can help you understand how important it is to tune lambda properly to achieve good generalization.

**Illustrating Bias and Variance with Sinusoidal Data**

To make this more concrete, let's take an example using sinusoidal data. Imagine you have 100 datasets, each with 25 data points, generated from a sinusoidal function. You fit a model with 24 Gaussian basis functions, which means you're using 25 parameters including one bias parameter.

In the visualizations, the left column shows how the model fits the data for various values of the natural logarithm of lambda. Only 20 of these 100 fits are shown for clarity. The right column shows the average of these fits compared to the original sinusoidal function.

As lambda increases, the fits become smoother but deviate from the true sinusoidal function, showing higher bias. Conversely, as lambda decreases, the fits become wiggly and closely follow the noise in the data, indicating high variance. The goal is to find a lambda value that minimizes the sum of squared bias and variance, which corresponds to the lowest test error on new data.

**Understanding the Likelihood Function in Regression**

In linear regression, our aim is to predict continuous target variables given a set of input variables. Typically, we start with a training dataset comprising inputs and corresponding target values. We then formulate a function using a vector of parameters that can be learned from this data.

The simplest regression model is a linear combination of input variables. However, this model is limited as both the parameters and input variables are linear. To extend this, we use basis functions—nonlinear functions of the input variables. This allows the model to become a linear function of the parameters but a nonlinear function of the input variables.

Consider basis functions like polynomials, Gaussians, or sigmoids. These functions transform the input data into a higher-dimensional space where a linear combination can better fit the target data. This transformation is crucial for capturing complex patterns in the data.

When fitting a model to data, we often minimize a sum-of-squares error function, which can be interpreted as a maximum likelihood solution under a Gaussian noise assumption. This means we assume the target variable is a deterministic function of the input with some added Gaussian noise. This assumption forms the basis for deriving the likelihood function, which helps in estimating the parameters that best fit the data.

Understanding these concepts is vital for building models that generalize well to new data, striking the right balance between bias and variance, and using basis functions effectively to capture complex patterns in data.
**Likelihood Function and Log-Likelihood**

Let's begin by discussing the likelihood function, which is crucial for understanding the relationship between our model parameters and the data. The likelihood function is essentially the probability of the observed data given the parameters of the model. In this case, we assume that our data points are drawn independently from a normal distribution with some mean and variance. The mean is modeled as a linear combination of basis functions applied to the input data points, and the variance is a constant.

To express this mathematically, if we have N data points, the likelihood function is given by the product of individual probabilities of each data point. This product involves the normal distribution evaluated at each target value, with the mean given by a linear model involving the input data and the weights, and the variance being a constant. 

Now, to make things simpler, we often take the logarithm of the likelihood function, turning the product into a sum. This is known as the log-likelihood function. For our normal distribution, the log-likelihood function simplifies to a sum involving the log of the variance, a constant term, and a sum-of-squares error term. The sum-of-squares error term measures how far each predicted value is from the actual target value, scaled by the variance.

**Maximum Likelihood Estimation**

Next, we move on to Maximum Likelihood Estimation (MLE), which is a method for estimating the parameters of our model. The goal here is to find the values of the parameters that maximize the log-likelihood function. For our linear model, this involves finding the weights and the variance that make the observed data most probable.

Let's first focus on the weights. By taking the derivative of the log-likelihood function with respect to the weights and setting it to zero, we derive a system of linear equations known as the normal equations. Solving these equations gives us the weights that maximize the likelihood function. This solution is also known as the least-squares solution because it minimizes the sum-of-squares error term.

The normal equations can be solved directly, leading to an expression involving the inverse of a matrix known as the design matrix. This matrix is constructed from the basis functions applied to the input data points. If the design matrix is invertible, we can obtain a unique solution for the weights.

**Geometric Interpretation and Sequential Learning**

Understanding the geometry of the least-squares solution can provide valuable insights. Imagine an N-dimensional space where each axis represents one of the target values. In this space, the vector of target values is represented by a point. Each basis function, evaluated at all data points, can also be represented as a vector in this space.

The least-squares solution can be visualized as the orthogonal projection of the target vector onto the subspace spanned by the basis function vectors. Intuitively, this projection minimizes the distance between the target vector and the subspace, corresponding to minimizing the sum-of-squares error.

When dealing with large datasets, computing the least-squares solution can be computationally intensive. This is where sequential learning algorithms, such as stochastic gradient descent (SGD), come into play. Instead of processing the entire dataset at once, SGD updates the model parameters incrementally, using one data point at a time. This approach is particularly useful for real-time applications where data arrives continuously.

**Regularized Least Squares**

Finally, let's discuss regularization, which is a technique used to prevent overfitting. Overfitting occurs when a model performs well on the training data but poorly on unseen data. Regularization adds a penalty term to the error function, discouraging large values for the model parameters.

One common form of regularization is to add the sum of the squares of the weights to the error function. This is known as L2 regularization or ridge regression. By adding this term, we ensure that the weights do not become too large, thus improving the generalization of the model.

The regularized error function remains quadratic, allowing us to find its minimum in a closed form. The resulting solution is similar to the standard least-squares solution but with an additional term that incorporates the regularization parameter. This parameter controls the trade-off between minimizing the sum-of-squares error and keeping the weights small.

In summary, these concepts and methods provide a robust framework for building and understanding linear regression models, from the probabilistic foundations to practical considerations like numerical stability and real-time learning.
**Visualization of Linear Regression Models**

The diagram I am referring to is a conceptual representation of linear regression models, basis functions, and regularization. It extends these concepts to models predicting multiple outputs, which is vital when dealing with complex data. In this diagram, the bottom node, labeled with "phi-zero of x," signifies the bias node. This node is critical as it corresponds to the bias term in a linear model and consistently outputs one without needing any input. Above it, nodes labeled "phi-one of x" to "phi M-minus-one of x" represent the basis functions for the input data x.

Moving upwards, we have the top layer nodes labeled "y-one of x, w" to "y-K of x, w," representing the output nodes for multiple target variables. These nodes are crucial as they denote the predicted outputs of the model. Each output node is a result of a distinct weighted sum of the transformed input features through the basis functions. The arrows in the diagram illustrate the mapping from the input functions, represented by the phi nodes, to the output nodes. This setup serves as a visual aid to understand how linear regression models and basis functions work together to predict outputs, especially in scenarios where multiple outputs are involved.

**Multiple Outputs in Regression Models**

Now, let's delve into the concept of multiple outputs. Traditionally, we've worked with a single target variable, denoted as t. However, in many real-world applications, we might need to predict more than one target variable, say K target variables. These can be collectively represented by a target vector t, which is essentially a list of the target variables.

One straightforward approach is to use a different set of basis functions for each component of the target vector t. This would lead to multiple, independent regression problems. However, a more efficient approach is to use the same set of basis functions to model all components of the target vector. This approach can be expressed as "y of x, w equals W transpose times phi of x," where y is a K-dimensional column vector, W is an M by K matrix of parameters, and phi of x is an M-dimensional column vector with elements phi-j of x, where phi-zero of x equals one, as before. This can be visualized as a neural network with a single layer of parameters.

**Mathematical Formulation and Log-Likelihood**

Next, let's talk about the conditional distribution of the target vector, which we assume to be an isotropic Gaussian. This means the distribution can be written as "p of t given x, W, sigma-squared equals Normal distribution of t given W transpose phi of x, sigma-squared I." Here, I is the identity matrix, and sigma-squared represents the variance. 

Suppose we have a set of observations for the target vectors, denoted as t-one to t-N, we can combine these into a matrix T of size N by K, where each row corresponds to a target vector. Similarly, the input vectors x-one to x-N can be combined into a matrix X. The log-likelihood function, which is a measure of how well the model parameters explain the observed data, can be written as the sum of the log of the Gaussian distributions for each observation. This simplifies to minus half times N times K times the log of two pi sigma-squared, minus one over two sigma-squared times the sum of the squared differences between the observed and predicted target vectors.

To maximize this log-likelihood function with respect to the parameter matrix W, we get "W-ML equals the inverse of phi transpose phi times phi transpose T", where phi is the matrix combining the input feature vectors. For each target variable t-k, this can be written as "w-k equals the inverse of phi transpose phi times phi transpose t-k," which can also be expressed as "phi-dagger t-k," where phi-dagger represents the pseudo-inverse of the matrix phi. This result ties back to the principles of linear regression but extended to handle multiple outputs efficiently.
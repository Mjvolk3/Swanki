## Derivation of Backpropagation Algorithm

Describe the term 'backpropagation' as used in this book.

In this book, 'backpropagation' specifically refers to the computational procedure used in the numerical evaluation of derivatives such as the gradient of the error function with respect to the weights and biases of a neural network. This is distinct from the broader use of the term, which may refer to the network architecture or the end-to-end training procedure.

- #neural-networks, #gradient-descent.backpropagation


## Backpropagation Application

Identify the derivatives that the backpropagation procedure can be applied to evaluate.

The backpropagation procedure can be applied to evaluate important derivatives such as the Jacobian and Hessian matrices, in addition to the gradient of the error function with respect to the weights and biases of a neural network.

- #neural-networks, #mathematics.derivatives


## Evaluation of Error Functions

What is the general form of error functions of practical interest, particularly those defined by maximum likelihood?

Many error functions of practical interest, particularly those defined by maximum likelihood for a set of i.i.d. (independent and identically distributed) data, comprise a sum of terms, one for each data point in the training set:
$$
E(\mathbf{w})=\sum_{n=1}^{N} E_{n}(\mathbf{w})
$$
where $E(\mathbf{w})$ is the total error and $E_n(\mathbf{w})$ is the error for the $n$-th data point.

- #error-functions, #statistics.maximum-likelihood


## Gradient Evaluation for Stochastic Gradient Descent

Explain why evaluating $\nabla E_{n}(\mathbf{w})$ for one term in the error function is useful.

Evaluating $\nabla E_{n}(\mathbf{w})$ for one term in the error function is useful because it can be used directly for stochastic gradient descent. The results can also be accumulated over a set of training data points for batch or minibatch methods.

$E(\mathbf{w})=\sum_{n=1}^{N} E_{n}(\mathbf{w})$

- #gradient-descent, #mathematics.gradient-evaluation


## Linear Model Output Equation

Provide the equation that defines the outputs $y_k$ as linear combinations of the input variables $x_i$.

The outputs $y_{k}$ are linear combinations of the input variables $x_{i}$, defined by the equation:
$$
y_{k}=\sum_{i} w_{k i} x_{i}
$$
where $w_{ki}$ represents the weights.

- #linear-models, #mathematics.equations


## Sum-of-Squares Error Function

What is the form of the sum-of-squares error function for a particular input data point $n$?

For a particular input data point $n$, the sum-of-squares error function is given by:
$$
E_{n}=\frac{1}{2} \sum_{k}\left(y_{n k}-t_{n k}\right)^{2}
$$
where $y_{nk}$ is the predicted output and $t_{nk}$ is the target output for the $n$-th data point.

- #error-functions, #mathematics.sum-of-squares
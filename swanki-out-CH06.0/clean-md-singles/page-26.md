Exercise 6.9

\section*{Exercise 6.10}

Section 5.4.6

Section 5.4.6
Following the same argument as for a single target variable, we see that maximizing the likelihood function with respect to the weights is equivalent to minimizing the sum-of-squares error function:

$$
E(\mathbf{w})=\frac{1}{2} \sum_{n=1}^{N}\left\|\mathbf{y}\left(\mathbf{x}_{n}, \mathbf{w}\right)-\mathbf{t}_{n}\right\|^{2}
$$

The noise variance is then given by

$$
\sigma^{2 \star}=\frac{1}{N K} \sum_{n=1}^{N}\left\|\mathbf{y}\left(\mathbf{x}_{n}, \mathbf{w}^{\star}\right)-\mathbf{t}_{n}\right\|^{2}
$$

where $K$ is the dimensionality of the target variable. The assumption of conditional independence of the target variables can be dropped at the expense of a slightly more complex optimization problem.

Recall that there is a natural pairing of the error function (given by the negative $\log$ likelihood) and the output-unit activation function. In regression, we can view the network as having an output activation function that is the identity, so that $y_{k}=a_{k}$. The corresponding sum-of-squares error function then has the property

$$
\frac{\partial E}{\partial a_{k}}=y_{k}-t_{k}
$$

\subsection*{6.4.2 Binary classification}

Now consider binary classification in which we have a single target variable $t$ such that $t=1$ denotes class $\mathcal{C}_{1}$ and $t=0$ denotes class $\mathcal{C}_{2}$. Following the discussion of canonical link functions, we consider a network having a single output whose activation function is a logistic sigmoid (6.13) so that $0 \leqslant y(\mathbf{x}, \mathbf{w}) \leqslant 1$. We can interpret $y(\mathbf{x}, \mathbf{w})$ as the conditional probability $p\left(\mathcal{C}_{1} \mid \mathbf{x}\right)$, with $p\left(\mathcal{C}_{2} \mid \mathbf{x}\right)$ given by $1-y(\mathbf{x}, \mathbf{w})$. The conditional distribution of targets given inputs is then a Bernoulli distribution of the form

$$
p(t \mid \mathbf{x}, \mathbf{w})=y(\mathbf{x}, \mathbf{w})^{t}\{1-y(\mathbf{x}, \mathbf{w})\}^{1-t}
$$

If we consider a training set of independent observations, then the error function, which is given by the negative log likelihood, is then a cross-entropy error of the form

$$
E(\mathbf{w})=-\sum_{n=1}^{N}\left\{t_{n} \ln y_{n}+\left(1-t_{n}\right) \ln \left(1-y_{n}\right)\right\}
$$

where $y_{n}$ denotes $y\left(\mathbf{x}_{n}, \mathbf{w}\right)$. Simard, Steinkraus, and Platt (2003) found that using the cross-entropy error function instead of the sum-of-squares for a classification problem leads to faster training as well as improved generalization.

Note that there is no analogue of the noise variance $\sigma^{2}$ in (6.32) because the target values are assumed to be correctly labelled. However, the model is easily extended to allow for labelling errors by introducing a probability $\epsilon$ that the target
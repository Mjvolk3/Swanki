Exercise 4.7

Section 3.2.7 where $\mathbf{t}_{k}$ is an $N$-dimensional column vector with components $t_{n k}$ for $n=1, \ldots N$. Thus, the solution to the regression problem decouples between the different target variables, and we need compute only a single pseudo-inverse matrix $\boldsymbol{\Phi}^{\dagger}$, which is shared by all the vectors $\mathbf{w}_{k}$.

The extension to general Gaussian noise distributions having arbitrary covariance matrices is straightforward. Again, this leads to a decoupling into $K$ independent regression problems. This result is unsurprising because the parameters $\mathbf{W}$ define only the mean of the Gaussian noise distribution, and we know that the maximum likelihood solution for the mean of a multivariate Gaussian is independent of the covariance. From now on, we will therefore consider a single target variable $t$ for simplicity.

\subsection*{4.2. Decision theory}

We have formulated the regression task as one of modelling a conditional probability distribution $p(t \mid \mathbf{x})$, and we have chosen a specific form for the conditional probability, namely a Gaussian (4.8) with an $\mathbf{x}$-dependent mean $y(\mathbf{x}, \mathbf{w})$ governed by parameters $\mathbf{w}$ and with variance given by the parameter $\sigma^{2}$. Both $\mathbf{w}$ and $\sigma^{2}$ can be learned from data using maximum likelihood. The result is a predictive distribution given by

$$
p\left(t \mid \mathbf{x}, \mathbf{w}_{\mathrm{ML}}, \sigma_{\mathrm{ML}}^{2}\right)=\mathcal{N}\left(t \mid y\left(\mathbf{x}, \mathbf{w}_{\mathrm{ML}}\right), \sigma_{\mathrm{ML}}^{2}\right)
$$

The predictive distribution expresses our uncertainty over the value of $t$ for some new input $\mathbf{x}$. However, for many practical applications we need to predict a specific value for $t$ rather than returning an entire distribution, particularly where we must take a specific action. For example, if our goal is to determine the optimal level of radiation to use for treating a tumour and our model predicts a probability distribution over radiation dose, then we must use that distribution to decide the specific dose to be administered. Our task therefore breaks down into two stages. In the first stage, called the inference stage, we use the training data to determine a predictive distribution $p(t \mid \mathbf{x})$. In the second stage, known as the decision stage, we use this predictive distribution to determine a specific value $f(\mathbf{x})$, which will be dependent on the input vector $\mathbf{x}$, that is optimal according to some criterion. We can do this by minimizing a loss function that depends on both the predictive distribution $p(t \mid \mathbf{x})$ and on $f$.

Intuitively we might choose the mean of the conditional distribution, so that we would use $f(\mathbf{x})=y\left(\mathbf{x}, \mathbf{w}_{\mathrm{ML}}\right)$. In some cases this intuition will be correct, but in other situations it can give very poor results. It is therefore useful to formalize this so that we can understand when it applies and under what assumptions, and the framework for doing this is called decision theory.

Suppose that we choose a value $f(\mathbf{x})$ for our prediction when the true value is t. In doing so, we incur some form of penalty or cost. This is determined by a loss, which we denote $L(t, f(\mathbf{x}))$. Of course, we do not know the true value of $t$, so instead of minimizing $L$ itself, we minimize the average, or expected, loss which is
![](https://cdn.mathpix.com/cropped/2024_05_26_6bfc4af0ed55d2a80c82g-1.jpg?height=1253&width=1248&top_left_y=214&top_left_x=409

ChatGPT figure/image summary: The image contains text superimposed on an abstract, colorful background. The text reads:

4
Single-layer Networks: Regression

This is likely a section or chapter title from a textbook or educational material related to the study of single-layer neural networks and their application to regression problems in the context of machine learning or a related field. The number "4" suggests that this is the fourth chapter or section in the material. The abstract background provides a visually appealing design but does not convey specific information relevant to the topic of single-layer networks or regression.)

In this chapter we discuss some of the basic ideas behind neural networks using the

Section 1.2 framework of linear regression, which we encountered briefly in the context of polynomial curve fitting. We will see that a linear regression model corresponds to a simple form of neural network having a single layer of learnable parameters. Although single-layer networks have very limited practical applicability, they have simple analytical properties and provide an excellent framework for introducing many of the core concepts that will lay a foundation for our discussion of deep neural networks in later chapters.

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

Figure 4.5 The regression function $f^{\star}(x)$, which minimizes the expected squared loss, is given by the mean of the conditional distribution $p(t \mid x)$.

![](https://cdn.mathpix.com/cropped/2024_05_26_194577429b12ff8ccc6dg-1.jpg?height=539&width=708&top_left_y=219&top_left_x=938

ChatGPT figure/image summary: The image pertains to a graphical illustration from the paper referenced in the context. It depicts a graph with two axes, labeled "t" on the vertical axis and "x" on the horizontal axis. The graph includes two curves:

1. A probability distribution p(t|x0, w, σ^2), which is typically a Gaussian curve centered around a specific value of x (x0). This curve represents the probability distribution of the target variable "t" given a specific input "x0" and parameters "w" and "σ^2".

2. A regression function f*(x), which appears as a smooth curve and represents the expected value (mean) of the conditional distribution p(t|x). This function gives the optimal prediction, which minimizes the expected squared loss, as mentioned in the context provided.

The key point here is that the regression function curve simplifies the entire probability distribution for a given input "x" to a single optimal prediction value, which is the mean of that distribution. This is useful in practical applications where a specific prediction or decision needs to be made based on probabilistic models.)

given by

$$
\mathbb{E}[L]=\iint L(t, f(\mathbf{x})) p(\mathbf{x}, t) \mathrm{d} \mathbf{x} \mathrm{d} t
$$

where we are averaging over the distribution of both input and target variables, weighted by their joint distribution $p(\mathbf{x}, t)$. A common choice of loss function in regression problems is the squared loss given by $L(t, f(\mathbf{x}))=\{f(\mathbf{x})-t\}^{2}$. In this case, the expected loss can be written

$$
\mathbb{E}[L]=\iint\{f(\mathbf{x})-t\}^{2} p(\mathbf{x}, t) \mathrm{d} \mathbf{x} \mathrm{d} t
$$

It is important not to confuse the squared-loss function with the sum-of-squares error function introduced earlier. The error function is used to set the parameters during training in order to determine the conditional probability distribution $p(t \mid \mathbf{x})$, whereas the loss function governs how the conditional distribution is used to arrive at a predictive function $f(\mathbf{x})$ specifying a prediction for each value of $\mathbf{x}$.

Our goal is to choose $f(\mathbf{x})$ so as to minimize $\mathbb{E}[L]$. If we assume a completely

\section*{Appendix $B$} flexible function $f(\mathbf{x})$, we can do this formally using the calculus of variations to give

$$
\frac{\delta \mathbb{E}[L]}{\delta f(\mathbf{x})}=2 \int\{f(\mathbf{x})-t\} p(\mathbf{x}, t) \mathrm{d} t=0
$$

Solving for $f(\mathbf{x})$ and using the sum and product rules of probability, we obtain

$$
f^{\star}(\mathbf{x})=\frac{1}{p(\mathbf{x})} \int t p(\mathbf{x}, t) \mathrm{d} t=\int t p(t \mid \mathbf{x}) \mathrm{d} t=\mathbb{E}_{t}[t \mid \mathbf{x}]
$$

which is the conditional average of $t$ conditioned on $\mathrm{x}$ and is known as the regression function. This result is illustrated in Figure 4.5. It can readily be extended to multiple target variables represented by the vector $\mathbf{t}$, in which case the optimal solution is the conditional average $\mathbf{f}^{\star}(\mathbf{x})=\mathbb{E}_{t}[\mathbf{t} \mid \mathbf{x}]$. For a Gaussian conditional distribution of the

form (4.8), the conditional mean will be simply

$$
\mathbb{E}[t \mid \mathbf{x}]=\int t p(t \mid \mathbf{x}) \mathrm{d} t=y(\mathbf{x}, \mathbf{w})
$$

The use of calculus of variations to derive (4.37) implies that we are optimizing over all possible functions $f(\mathbf{x})$. Although any parametric model that we can implement in practice is limited in the range of functions that it can represent, the framework of deep neural networks, discussed extensively in later chapters, provides a highly flexible class of functions that, for many practical purposes, can approximate any desired function to high accuracy.

We can derive this result in a slightly different way, which will also shed light on the nature of the regression problem. Armed with the knowledge that the optimal solution is the conditional expectation, we can expand the square term as follows

$$
\begin{aligned}
& \{f(\mathbf{x})-t\}^{2}=\{f(\mathbf{x})-\mathbb{E}[t \mid \mathbf{x}]+\mathbb{E}[t \mid \mathbf{x}]-t\}^{2} \\
& =\{f(\mathbf{x})-\mathbb{E}[t \mid \mathbf{x}]\}^{2}+2\{f(\mathbf{x})-\mathbb{E}[t \mid \mathbf{x}]\}\{\mathbb{E}[t \mid \mathbf{x}]-t\}+\{\mathbb{E}[t \mid \mathbf{x}]-t\}^{2}
\end{aligned}
$$

where, to keep the notation uncluttered, we use $\mathbb{E}[t \mid \mathbf{x}]$ to denote $\mathbb{E}_{t}[t \mid \mathbf{x}]$. Substituting into the loss function (4.35) and performing the integral over $t$, we see that the crossterm vanishes and we obtain an expression for the loss function in the form

$$
\mathbb{E}[L]=\int\{f(\mathbf{x})-\mathbb{E}[t \mid \mathbf{x}]\}^{2} p(\mathbf{x}) \mathrm{d} \mathbf{x}+\int \operatorname{var}[t \mid \mathbf{x}] p(\mathbf{x}) \mathrm{d} \mathbf{x}
$$

The function $f(\mathbf{x})$ we seek to determine appears only in the first term, which will be minimized when $f(\mathbf{x})$ is equal to $\mathbb{E}[t \mid \mathbf{x}]$, in which case this term will vanish. This is simply the result that we derived previously, and shows that the optimal least-squares predictor is given by the conditional mean. The second term is the variance of the distribution of $t$, averaged over $\mathbf{x}$, and represents the intrinsic variability of the target data and can be regarded as noise. Because it is independent of $f(\mathbf{x})$, it represents the irreducible minimum value of the loss function.

The squared loss is not the only possible choice of loss function for regression. Here we consider briefly one simple generalization of the squared loss, called the Minkowski loss, whose expectation is given by

$$
\mathbb{E}\left[L_{q}\right]=\iint|f(\mathbf{x})-t|^{q} p(\mathbf{x}, t) \mathrm{d} \mathbf{x} \mathrm{d} t
$$

which reduces to the expected squared loss for $q=2$. The function $|f-t|^{q}$ is plotted against $f-t$ for various values of $q$ in Figure 4.6. The minimum of $\mathbb{E}\left[L_{q}\right]$ is given by the conditional mean for $q=2$, the conditional median for $q=1$, and the conditional mode for $q \rightarrow 0$.

Note that the Gaussian noise assumption implies that the conditional distribution of $t$ given $\mathbf{x}$ is unimodal, which may be inappropriate for some applications. In this case a squared loss can lead to very poor results and we need to develop more sophisticated approaches. For example, we can extend this model by using mixtures

![](https://cdn.mathpix.com/cropped/2024_05_26_39f071919089f32e7ef4g-1.jpg?height=1096&width=1512&top_left_y=209&top_left_x=148

ChatGPT figure/image summary: The image shows four plots of the Minkowski loss function \(L_{q} = |f - t|^q\) against \(f - t\) for various values of \(q\). Each plot corresponds to a different value of the exponent \(q\), as indicated above each plot. The graphs demonstrate how the Minkowski loss function changes shape as the exponent \(q\) varies.

The upper-left plot corresponds to \(q = 0.3\), resulting in a function that forms a well that is very steep around \(f - t = 0\) and flattens out quickly as \(f - t\) moves away from zero.

The upper-right plot corresponds to \(q = 1\), indicating the absolute loss which forms a V shape. This is the linear case where the gradient doesn't change with the distance between the prediction and the target.

The bottom-left plot corresponds to \(q = 2\), representing the standard squared loss function, where the function is a symmetrical parabola about \(f - t = 0\), indicating that the penalty increases quadratically as predictions deviate from the target.

The bottom-right plot corresponds to \(q = 10\), showing the function for a much larger value of \(q\), resulting in a very steep and narrow well around \(f - t = 0\), suggesting a very high penalty for even slight deviations from the target value.

These plots help to visualize the effect of different \(q\) values on the loss function's sensitivity to errors. For regression problems, the choice of \(q\) in the Minkowski loss function can significantly affect the robustness and sensitivity of the regression model to outliers.)

![](https://cdn.mathpix.com/cropped/2024_05_26_39f071919089f32e7ef4g-1.jpg?height=504&width=691&top_left_y=217&top_left_x=153

ChatGPT figure/image summary: This image shows a plot of a mathematical function, specifically a plot of \( |f-t|^q \) for \( q = 0.3 \), where \( f \) and \( t \) are variables representing the predicted value and the target value, respectively. The function is plotted on the Cartesian plane, with the horizontal axis labeled as \( f-t \) and the vertical axis labeled as \( |f-t|^{0.3} \).

The curve depicted has a V-like shape, which is characteristic for graphs of absolute value functions to a power less than 1. The plot shows that as the difference between \( f \) and \( t \) increases (either positively or negatively), the value of \( |f-t|^q \) also increases, but at a slower rate than linear due to the exponent \( 0.3 \) being less than 1. The purpose of such a plot is to illustrate how different values of \( q \) in the Minkowski loss function affect the shape of the loss curve, which is related to the penalty for errors in a regression task. A lower value of \( q \) makes the loss function less sensitive to outliers than the squared loss where \( q = 2 \).)

![](https://cdn.mathpix.com/cropped/2024_05_26_39f071919089f32e7ef4g-1.jpg?height=504&width=691&top_left_y=786&top_left_x=153

ChatGPT figure/image summary: The image appears to be a plot of a function which is labeled with the quantity \(|f - t|^q\) for \(q = 2\). The plot shows a parabola that opens upwards, with its vertex at the origin, indicating that the function plotted is a quadratic function of form \((f-t)^2\), which is consistent with the common form of the squared loss function used in regression problems. The horizontal axis represents the difference between a predicted value \(f\) and the true value \(t\), and the vertical axis represents the squared difference, which is the loss for a given prediction error. The label \(q=2\) denotes that the Minkowski loss function is being used with \(q=2\), which corresponds to the squared loss.)

![](https://cdn.mathpix.com/cropped/2024_05_26_39f071919089f32e7ef4g-1.jpg?height=503&width=689&top_left_y=220&top_left_x=955

ChatGPT figure/image summary: The image provided is a plot of the Minkowski loss function for \( q = 1 \), as indicated by the label on the plot. It is a V-shaped graph that shows the function \( L_q = |f - t|^q \), which in this case simplifies to the absolute value of \( f - t \) because \( q = 1 \). The plot has its vertex at the origin, (0, 0), and extends linearly upwards in both directions, indicating that as the difference between \( f \) and \( t \) increases, the loss increases linearly, irrespective of the sign of the difference. The plot has axes labeled, with the horizontal axis representing the difference \( f - t \), and the vertical axis representing the loss \( |f - t|^1 \). The linear nature of the plot when \( q = 1 \) reflects that the loss increases directly with the absolute deviation of the predictions from the true values, making it characteristic of the L1 loss or absolute loss, often used when the median is the desired measure of central tendency.)

![](https://cdn.mathpix.com/cropped/2024_05_26_39f071919089f32e7ef4g-1.jpg?height=503&width=689&top_left_y=789&top_left_x=955

ChatGPT figure/image summary: The image provided is a 2-dimensional plot of a mathematical function, specifically for \( L_q = |f - t|^q \) with \( q = 10 \). The horizontal axis is labeled as \( f - t \), and the vertical axis is presumably labeled as \( |f - t|^q \). The plot depicts the curve of the given function for \( q = 10 \), which shows that as \( f - t \) moves away from 0, the value of \( |f - t|^{10} \) increases sharply.

The plot has the typical shape of a high-degree even-power function, which means that the loss increases very steeply as the prediction \( f \) deviates from the target \( t \), resulting in a sharp U-shaped curve. This suggests that predictions that are not very close to \( t \) will incur a very high loss when using \( q = 10 \) in the Minkowski loss function, emphasizing accuracy in prediction.

This kind of visualization helps to understand the effect of different values of \( q \) on the Minkowski loss function, as mentioned in the text that accompanies the request for image identification. For \( q = 2 \), the plot would represent the expected squared loss, which is a commonly used loss function in regression problems. The steeper the curve, the more sensitive the loss function is to errors, punishing deviations from the target value \( t \) more severely.)

Figure 4.6 Plots of the quantity $L_{q}=|f-t|^{q}$ for various values of $q$.

Section 6.5 of Gaussians to give multimodal conditional distributions, which often arise in the solution of inverse problems. Our focus in this section has been on decision theory for regression problems, and in the next chapter we shall develop analogous concepts

Section 5.2 for classification tasks.

\title{
4.3. The Bias-Variance Trade-off
}

So far in our discussion of linear models for regression, we have assumed that the

Section 1.2 form and number of basis functions are both given. We have also seen that the use of maximum likelihood can lead to severe over-fitting if complex models are trained using data sets of limited size. However, limiting the number of basis functions to avoid over-fitting has the side effect of limiting the flexibility of the model to capture interesting and important trends in the data. Although a regularization term can control over-fitting for models with many parameters, this raises the question of how to determine a suitable value for the regularization coefficient $\lambda$. Seeking the

solution that minimizes the regularized error function with respect to both the weight

Section 4.2 vector $\mathbf{w}$ and the regularization coefficient $\lambda$ is clearly not the right approach, since this leads to the unregularized solution with $\lambda=0$.

It is instructive to consider a frequentist viewpoint of the model complexity issue, known as the bias-variance trade-off. Although we will introduce this concept in the context of linear basis function models, where it is easy to illustrate the ideas using simple examples, the discussion has very general applicability. Note, however, that over-fitting is really an unfortunate property of maximum likelihood and does not arise when we marginalize over parameters in a Bayesian setting (Bishop, 2006).

When we discussed decision theory for regression problems, we considered various loss functions, each of which leads to a corresponding optimal prediction once we are given the conditional distribution $p(t \mid \mathbf{x})$. A popular choice is the squared-loss function, for which the optimal prediction is given by the conditional expectation, which we denote by $h(\mathbf{x})$ and is given by

$$
h(\mathbf{x})=\mathbb{E}[t \mid \mathbf{x}]=\int t p(t \mid \mathbf{x}) \mathrm{d} t
$$

We have also seen that the expected squared loss can be written in the form

$$
\mathbb{E}[L]=\int\{f(\mathbf{x})-h(\mathbf{x})\}^{2} p(\mathbf{x}) \mathrm{d} \mathbf{x}+\iint\{h(\mathbf{x})-t\}^{2} p(\mathbf{x}, t) \mathrm{d} \mathbf{x} \mathrm{d} t
$$

Recall that the second term, which is independent of $f(\mathbf{x})$, arises from the intrinsic noise on the data and represents the minimum achievable value of the expected loss. The first term depends on our choice for the function $f(\mathbf{x})$, and we will seek a solution for $f(\mathbf{x})$ that makes this term a minimum. Because it is non-negative, the smallest value that we can hope to achieve for this term is zero. If we had an unlimited supply of data (and unlimited computational resources), we could in principle find the regression function $h(\mathbf{x})$ to any desired degree of accuracy, and this would represent the optimal choice for $f(\mathbf{x})$. However, in practice we have a data set $\mathcal{D}$ containing only a finite number $N$ of data points, and consequently, we cannot know the regression function $h(\mathbf{x})$ exactly.

If we were to model $h(\mathbf{x})$ using a function governed by a parameter vector $\mathbf{w}$, then from a Bayesian perspective, the uncertainty in our model would be expressed through a posterior distribution over $\mathrm{w}$. A frequentist treatment, however, involves making a point estimate of $\mathbf{w}$ based on the data set $\mathcal{D}$ and tries instead to interpret the uncertainty of this estimate through the following thought experiment. Suppose we had a large number of data sets each of size $N$ and each drawn independently from the distribution $p(t, \mathbf{x})$. For any given data set $\mathcal{D}$, we can run our learning algorithm and obtain a prediction function $f(\mathbf{x} ; \mathcal{D})$. Different data sets from the ensemble will give different functions and consequently different values of the squared loss. The performance of a particular learning algorithm is then assessed by taking the average over this ensemble of data sets.

Consider the integrand of the first term in (4.42), which for a particular data set $\mathcal{D}$ takes the form

$$
\{f(\mathbf{x} ; \mathcal{D})-h(\mathbf{x})\}^{2}
$$

Because this quantity will be dependent on the particular data set $\mathcal{D}$, we take its average over the ensemble of data sets. If we add and subtract the quantity $\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]$ inside the braces, and then expand, we obtain

$$
\begin{aligned}
& \left\{f(\mathbf{x} ; \mathcal{D})-\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]+\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]-h(\mathbf{x})\right\}^{2} \\
& =\left\{f(\mathbf{x} ; \mathcal{D})-\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]\right\}^{2}+\left\{\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]-h(\mathbf{x})\right\}^{2} \\
& +2\left\{f(\mathbf{x} ; \mathcal{D})-\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]\right\}\left\{\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]-h(\mathbf{x})\right\}
\end{aligned}
$$

We now take the expectation of this expression with respect to $\mathcal{D}$ and note that the final term will vanish, giving

$$
\begin{aligned}
& \mathbb{E}_{\mathcal{D}}\left[\{f(\mathbf{x} ; \mathcal{D})-h(\mathbf{x})\}^{2}\right] \\
& =\underbrace{\left\{\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]-h(\mathbf{x})\right\}^{2}}_{(\text {bias })^{2}}+\underbrace{\mathbb{E}_{\mathcal{D}}\left[\left\{f(\mathbf{x} ; \mathcal{D})-\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]\right\}^{2}\right]}_{\text {variance }}
\end{aligned}
$$

We see that the expected squared difference between $f(\mathbf{x} ; \mathcal{D})$ and the regression function $h(\mathbf{x})$ can be expressed as the sum of two terms. The first term, called the squared bias, represents the extent to which the average prediction over all data sets differs from the desired regression function. The second term, called the variance, measures the extent to which the solutions for individual data sets vary around their average, and hence, this measures the extent to which the function $f(\mathbf{x} ; \mathcal{D})$ is sensitive to the particular choice of data set. We will provide some intuition to support these definitions shortly when we consider a simple example.

So far, we have considered a single input value $\mathrm{x}$. If we substitute this expansion back into (4.42), we obtain the following decomposition of the expected squared loss:

$$
\text { expected loss }=(\text { bias })^{2}+\text { variance }+ \text { noise }
$$

where

$$
\begin{aligned}
(\text { bias })^{2} & =\int\left\{\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]-h(\mathbf{x})\right\}^{2} p(\mathbf{x}) \mathrm{d} \mathbf{x} \\
\text { variance } & =\int \mathbb{E}_{\mathcal{D}}\left[\left\{f(\mathbf{x} ; \mathcal{D})-\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]\right\}^{2}\right] p(\mathbf{x}) \mathrm{d} \mathbf{x} \\
\text { noise } & =\iint\{h(\mathbf{x})-t\}^{2} p(\mathbf{x}, t) \mathrm{d} \mathbf{x} \mathrm{d} t
\end{aligned}
$$

and the bias and variance terms now refer to integrated quantities.

Our goal is to minimize the expected loss, which we have decomposed into the sum of a (squared) bias, a variance, and a constant noise term. As we will see, there is a trade-off between bias and variance, with very flexible models having low bias and high variance, and relatively rigid models having high bias and low variance. The model with the optimal predictive capability is the one that leads to the best balance between bias and variance. This is illustrated by considering the sinusoidal data set introduced earlier. Here we independently generate 100 data sets, each containing

$N=25$ data points, from the sinusoidal curve $h(x)=\sin (2 \pi x)$. The data sets are indexed by $l=1, \ldots, L$, where $L=100$. For each data set $\mathcal{D}^{(l)}$, we fit a model with $M=24$ Gaussian basis functions along with a constant 'bias' basis function to give a total of 25 parameters. By minimizing the regularized error function (4.26), we obtain a prediction function $f^{(l)}(x)$, as shown in Figure 4.7.

The top row corresponds to a large value of the regularization coefficient $\lambda$ that gives low variance (because the red curves in the left plot look similar) but high bias (because the two curves in the right plot are very different). Conversely on the bottom row, for which $\lambda$ is small, there is large variance (shown by the high variability between the red curves in the left plot) but low bias (shown by the good fit between the average model fit and the original sinusoidal function). Note that the result of averaging many solutions for the complex model with $M=25$ is a very good fit to the regression function, which suggests that averaging may be a beneficial procedure. Indeed, a weighted averaging of multiple solutions lies at the heart of a Bayesian approach, although the averaging is with respect to the posterior distribution of parameters, not with respect to multiple data sets.

We can also examine the bias-variance trade-off quantitatively for this example. The average prediction is estimated from

$$
\bar{f}(x)=\frac{1}{L} \sum_{l=1}^{L} f^{(l)}(x)
$$

and the integrated squared bias and integrated variance are then given by

$$
\begin{aligned}
(\text { bias })^{2} & =\frac{1}{N} \sum_{n=1}^{N}\left\{\bar{f}\left(x_{n}\right)-h\left(x_{n}\right)\right\}^{2} \\
\text { variance } & =\frac{1}{N} \sum_{n=1}^{N} \frac{1}{L} \sum_{l=1}^{L}\left\{f^{(l)}\left(x_{n}\right)-\bar{f}\left(x_{n}\right)\right\}^{2}
\end{aligned}
$$

where the integral over $x$, weighted by the distribution $p(x)$, is approximated by a finite sum over data points drawn from that distribution. These quantities, along with their sum, are plotted as a function of $\ln \lambda$ in Figure 4.8. We see that small values of $\lambda$ allow the model to become finely tuned to the noise on each individual data set leading to large variance. Conversely, a large value of $\lambda$ pulls the weight parameters towards zero leading to large bias.

Note that the bias-variance decomposition is of limited practical value because it is based on averages with respect to ensembles of data sets, whereas in practice we have only the single observed data set. If we had a large number of independent training sets of a given size, we would be better off combining them into a single larger training set, which of course would reduce the level of over-fitting for a given model complexity. Nevertheless, the bias-variance decomposition often provides useful insights into the model complexity issue, and although we have introduced it in this chapter from the perspective of regression problems, the underlying intuition has broad applicability.


![](https://cdn.mathpix.com/cropped/2024_05_26_d7ac92f7ef61188399a4g-1.jpg?height=1486&width=1518&top_left_y=302&top_left_x=144

ChatGPT figure/image summary: The image shows three pairs of plots symbolizing the relationship between bias and variance with respect to model complexity in a regression context. Each pair corresponds to a different value of the regularization parameter $\lambda$, as indicated by the values of $\ln \lambda$: 3, 1, and -3.

For each pair of plots:

- The left plot in a pair shows the results of fitting a regression model to the data for that particular $\ln \lambda$ value. The red curves represent the model fits to each of the 20 randomly sampled out of the 100 data sets (from a larger total of $L=100$ data sets). The aim is to model a sinusoidal function (not shown in these individual plots), and how well the red curves match this sinusoidal form depends on the regularization parameter.

- The right plot in a pair displays the average of the 100 fits (red curve) alongside the original sinusoidal function (green curve) from which the data sets were generated. The average fit is calculated using the equation provided in the context, and its closeness to the sinusoidal curve is a measure of the overall model performance.

The three pairs of plots correspond to:

1. A relatively large regularization parameter (top row, $\ln \lambda = 3$), which results in low variance—the red curves in the left plot are quite similar to each other. However, it also leads to high bias, as the average model fit (right plot's red curve) significantly diverges from the actual sinusoidal function (green curve).

2. A moderate regularization parameter (middle row, $\ln \lambda = 1$), which strikes a balance between the amount of variance and bias. The red curves in the left plot show more variability compared to the top row, but less compared to the bottom row. The average model fit (right plot's red curve) is closer to the original sinusoidal function (green curve) than in the top row.

3. A small regularization parameter (bottom row, $\ln \lambda = -3$), which allows for a much higher variance—visible by the substantial differences between each red curve in the left plot. Even though this leads to a low bias, as the average model fit (right plot's red curve) closely follows the sinusoidal function, it also means that the model is likely overfitting to the noise within individual data sets.

Together, these visualizations illustrate how tuning the regularization parameter $\lambda$ can)

Figure 4.7 Illustration of the dependence of bias and variance on model complexity governed by a regularization parameter $\lambda$, using the sinusoidal data from Chapter 1 . There are $L=100$ data sets, each having $N=25$ data points, and there are 24 Gaussian basis functions in the model so that the total number of parameters is $M=25$ including the bias parameter. The left column shows the result of fitting the model to the data sets for various values of $\ln \lambda$ (for clarity, only 20 of the 100 fits are shown). The right column shows the corresponding average of the 100 fits (red) along with the sinusoidal function from which the data sets were generated (green).

Figure 4.8 Plot of squared bias and variance, together with their sum, corresponding to the results shown in Figure 4.7. Also shown is the average test set error for a test data set size of 1,000 points. The minimum value of (bias) ${ }^{2}+$ variance occurs around $\ln \lambda=0.43$, which is close to the value that gives the minimum error on the test data.

![](https://cdn.mathpix.com/cropped/2024_05_26_a42f38fa62538bcdd4efg-1.jpg?height=544&width=901&top_left_y=214&top_left_x=756

ChatGPT figure/image summary: The image is a graph representing the trade-off between bias and variance in a predictive model as a function of model complexity, which is governed by a regularization parameter \( \lambda \). Specifically, this is a plot of squared bias (in red), variance (in blue), and their sum (in green), along with the average test set error (in magenta) against the natural logarithm of the regularization parameter \( \ln \lambda \).

From the graph, we can deduce that as the regularization parameter increases (moving right along the x-axis), the bias tends to increase while the variance decreases. The graph shows a typical behavior where, with very low values of \( \lambda \), the model can have low bias but high variance, leading to overfitting. As \( \lambda \) increases, the model tends to underfit, exhibiting high bias but low variance.

The graph indicates that the minimum sum of squared bias and variance occurs around \( \ln \lambda = 0.43 \), which is close to the value that gives the minimum test error. This suggests an optimal balance between bias and variance, thereby minimizing the generalization error of the model. This balance is crucial in machine learning to ensure that the model performs well on unseen data.)

\title{
Exercises
}

4.1 ( $\star$ ) Consider the sum-of-squares error function given by (1.2) in which the function $y(x, \mathbf{w})$ is given by the polynomial (1.1). Show that the coefficients $\mathbf{w}=\left\{w_{i}\right\}$ that minimize this error function are given by the solution to the following set of linear equations:

$$
\sum_{j=0}^{M} A_{i j} w_{j}=T_{i}
$$

where

$$
A_{i j}=\sum_{n=1}^{N}\left(x_{n}\right)^{i+j}
$$

Here a suffix $i$ or $j$ denotes the index of a component, whereas $(x)^{i}$ denotes $x$ raised to the power of $i$.

4.2 ( $\star$ ) Write down the set of coupled linear equations, analogous to (4.53), satisfied by the coefficients $w_{i}$ that minimize the regularized sum-of-squares error function given by $(1.4)$.

4.3 ( $\star$ ) Show that the tanh function defined by

$$
\tanh (a)=\frac{e^{a}-e^{-a}}{e^{a}+e^{-a}}
$$

and the logistic sigmoid function defined by (4.6) are related by

$$
\tanh (a)=2 \sigma(2 a)-1
$$

Hence, show that a general linear combination of logistic sigmoid functions of the form

$$
y(x, \mathbf{w})=w_{0}+\sum_{j=1}^{M} w_{j} \sigma\left(\frac{x-\mu_{j}}{s}\right)
$$

\title{
4.1. Linear Regression
}

The goal of regression is to predict the value of one or more continuous target variables $t$ given the value of a $D$-dimensional vector $\mathbf{x}$ of input variables. Typically we are given a training data set comprising $N$ observations $\left\{\mathbf{x}_{n}\right\}$, where $n=1, \ldots, N$, together with corresponding target values $\left\{t_{n}\right\}$, and the goal is to predict the value of $t$ for a new value of $\mathbf{x}$. To do this, we formulate a function $y(\mathbf{x}, \mathbf{w})$ whose values for new inputs $\mathbf{x}$ constitute the predictions for the corresponding values of $t$, and where $\mathrm{w}$ represents a vector of parameters that can be learned from the training data.

The simplest model for regression is one that involves a linear combination of the input variables:

$$
y(\mathbf{x}, \mathbf{w})=w_{0}+w_{1} x_{1}+\ldots+w_{D} x_{D}
$$

where $\mathbf{x}=\left(x_{1}, \ldots, x_{D}\right)^{\mathrm{T}}$. The term linear regression sometimes refers specifically to this form of model. The key property of this model is that it is a linear function of the parameters $w_{0}, \ldots, w_{D}$. It is also, however, a linear function of the input variables $x_{i}$, and this imposes significant limitations on the model.

\subsection*{4.1.1 Basis functions}

We can extend the class of models defined by (4.1) by considering linear combinations of fixed nonlinear functions of the input variables, of the form

$$
y(\mathbf{x}, \mathbf{w})=w_{0}+\sum_{j=1}^{M-1} w_{j} \phi_{j}(\mathbf{x})
$$

where $\phi_{j}(\mathrm{x})$ are known as basis functions. By denoting the maximum value of the index $j$ by $M-1$, the total number of parameters in this model will be $M$.

The parameter $w_{0}$ allows for any fixed offset in the data and is sometimes called

Section 4.3

Section 6.1 a bias parameter (not to be confused with bias in a statistical sense). It is often convenient to define an additional dummy basis function $\phi_{0}(\mathbf{x})$ whose value is fixed at $\phi_{0}(\mathbf{x})=1$ so that $(4.2)$ becomes

$$
y(\mathbf{x}, \mathbf{w})=\sum_{j=0}^{M-1} w_{j} \phi_{j}(\mathbf{x})=\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}(\mathbf{x})
$$

where $\mathbf{w}=\left(w_{0}, \ldots, w_{M-1}\right)^{\mathrm{T}}$ and $\boldsymbol{\phi}=\left(\phi_{0}, \ldots, \phi_{M-1}\right)^{\mathrm{T}}$. We can represent the model (4.3) using a neural network diagram, as shown in Figure 4.1.

By using nonlinear basis functions, we allow the function $y(\mathbf{x}, \mathbf{w})$ to be a nonlinear function of the input vector $\mathbf{x}$. Functions of the form (4.2) are called linear models, however, because they are linear in $\mathbf{w}$. It is this linearity in the parameters that will greatly simplify the analysis of this class of models. However, it also leads to some significant limitations.

Figure 4.1 The linear regression model (4.3) can be expressed as a simple neural network diagram involving a single layer of parameters. Here each basis function $\phi_{j}(\mathbf{x})$ is represented by an input node, with the solid node representing the 'bias' basis function $\phi_{0}$, and the function $y(\mathbf{x}, \mathbf{w})$ is represented by an output node. Each of the parameters $w_{j}$ is shown by a line connecting the corresponding basis

![](https://cdn.mathpix.com/cropped/2024_05_26_28116a89444d4b7f5a3bg-1.jpg?height=332&width=528&top_left_y=215&top_left_x=1111

ChatGPT figure/image summary: The image is a diagram representing a simple neural network used to illustrate the linear regression model with basis functions. Here is a description of its components:

- There are several input nodes, each corresponding to a different basis function \(\phi_j(\textbf{x})\), where \(j\) ranges from 0 to \(M-1\). These are represented by the circles on the left side of the diagram.
- The basis functions are connected to an output node by lines, each line representing a parameter \(w_j\). 
- The solid node at the bottom left, representing \(\phi_0(\textbf{x})\), signifies the 'bias' basis function, which is often set to a constant value of 1.
- The output node, represented by the circle on the right side, corresponds to the function \(y(\textbf{x}, \textbf{w})\).
- The purpose of the diagram is to depict how a linear combination of weighted basis functions can be used to predict a continuous target variable.

Overall, this neural network diagram is a visual representation of the linear regression model from the paper, where the linear model is expressed as the weighted sum of basis functions, as described by the equation \(y(\textbf{x}, \textbf{w}) = \sum_{j=0}^{M-1} w_{j} \phi_{j}(\textbf{x})\).)
function to the output.

Before the advent of deep learning it was common practice in machine learning to use some form of fixed pre-processing of the input variables $\mathbf{x}$, also known as feature extraction, expressed in terms of a set of basis functions $\left\{\phi_{j}(\mathbf{x})\right\}$. The goal was to choose a sufficiently powerful set of basis functions that the resulting learning task could be solved using a simple network model. Unfortunately, it is very difficult to hand-craft suitable basis functions for anything but the simplest applications. Deep learning avoids this problem by learning the required nonlinear transformations of the data from the data set itself.

We have already encountered an example of a regression problem when we disChapter 1 cussed curve fitting using polynomials. The polynomial function (1.1) can be expressed in the form (4.3) if we consider a single input variable $x$ and if we choose basis functions defined by $\phi_{j}(x)=x^{j}$. There are many other possible choices for the basis functions, for example

$$
\phi_{j}(x)=\exp \left\{-\frac{\left(x-\mu_{j}\right)^{2}}{2 s^{2}}\right\}
$$

where the $\mu_{j}$ govern the locations of the basis functions in input space, and the parameter $s$ governs their spatial scale. These are usually referred to as 'Gaussian' basis functions, although it should be noted that they are not required to have a probabilistic interpretation. In particular the normalization coefficient is unimportant because these basis functions will be multiplied by learnable parameters $w_{j}$.

Another possibility is the sigmoidal basis function of the form

$$
\phi_{j}(x)=\sigma\left(\frac{x-\mu_{j}}{s}\right)
$$

where $\sigma(a)$ is the logistic sigmoid function defined by

$$
\sigma(a)=\frac{1}{1+\exp (-a)}
$$

Equivalently, we can use the tanh function because this is related to the logistic sigmoid by $\tanh (a)=2 \sigma(2 a)-1$, and so a general linear combination of logistic sigmoid functions is equivalent to a general linear combination of tanh functions in the sense that they can represent the same class of input-output functions. These various choices of basis function are illustrated in Figure 4.2.


![](https://cdn.mathpix.com/cropped/2024_05_26_e13468588350511df9e7g-1.jpg?height=438&width=1486&top_left_y=234&top_left_x=134

ChatGPT figure/image summary: The image shows three separate plots, each representing a different type of basis function used in the context of a linear regression model or a simple neural network.

On the left, the plot shows polynomial basis functions. These are curves that represent various polynomial equations, indicating the influence of different powers of a single input variable `x`. Essentially, the curves seem to represent the functions \( \phi_j(x) = x^j \) for different values of `j`, resulting in lines that vary from linear (a simple angled line) to higher-order polynomials (curved lines that can have multiple turning points).

The center plot displays Gaussian basis functions. In this case, the curves illustrate the Gaussian function as described in the text, which takes the form \( \phi_j(x) = \exp \left\{-\frac{(x-\mu_j)^2}{2s^2}\right\} \), where \( \mu_j \) indicates the location and `s` the scale. Each curve looks like a bell-shaped Gaussian distribution, centered at different values of `x`, corresponding to different \( \mu_j \) values.

On the right, the sigmoidal basis functions are illustrated. A sigmoidal basis function of the form \( \phi_j(x) = \sigma\left(\frac{x-\mu_j}{s}\right) \), where \( \sigma(a) = \frac{1}{1+\exp(-a)} \), is a logistic sigmoid function. Each curve in this plot represents a sigmoid function shifted along the x-axis (horizontal), indicating the different \( \mu_j \) values. The sigmoid functions display an "S"-shaped curve, transitioning smoothly from 0 to 1.

All of these basis functions are used to transform input data into a space where a linear combination can be made to best fit the target data, as per a regression or machine learning model. Each type offers a different way of representing features and contributes differently to the model's ability to approximate complex functions.)

Figure 4.2 Examples of basis functions, showing polynomials on the left, Gaussians of the form (4.4) in the centre, and sigmoidal basis functions of the form (4.5) on the right.

\section*{Section 4.1.7}

Section 1.2
Yet another possible choice of basis function is the Fourier basis, which leads to an expansion in sinusoidal functions. Each basis function represents a specific frequency and has infinite spatial extent. By contrast, basis functions that are localized to finite regions of input space necessarily comprise a spectrum of different spatial frequencies. In signal processing applications, it is often of interest to consider basis functions that are localized in both space and frequency, leading to a class of functions known as wavelets (Ogden, 1997; Mallat, 1999; Vidakovic, 1999). These are also defined to be mutually orthogonal, to simplify their application. Wavelets are most applicable when the input values live on a regular lattice, such as the successive time points in a temporal sequence or the pixels in an image.

Most of the discussion in this chapter, however, is independent of the choice of basis function set, and so we will not specify the particular form of the basis functions, except for numerical illustration. Furthermore, to keep the notation simple, we will focus on the case of a single target variable $t$, although we will briefly outline the modifications needed to deal with multiple target variables.

\subsection*{4.1.2 Likelihood function}

We solved the problem of fitting a polynomial function to data by minimizing a sum-of-squares error function, and we also showed that this error function could be motivated as the maximum likelihood solution under an assumed Gaussian noise model. We now return to this discussion and consider the least-squares approach, and its relation to maximum likelihood, in more detail.

As before, we assume that the target variable $t$ is given by a deterministic function $y(\mathbf{x}, \mathbf{w})$ with additive Gaussian noise so that

$$
t=y(\mathbf{x}, \mathbf{w})+\epsilon
$$

where $\epsilon$ is a zero-mean Gaussian random variable with variance $\sigma^{2}$. Thus, we can write

$$
p\left(t \mid \mathbf{x}, \mathbf{w}, \sigma^{2}\right)=\mathcal{N}\left(t \mid y(\mathbf{x}, \mathbf{w}), \sigma^{2}\right)
$$

Now consider a data set of inputs $\mathbf{X}=\left\{\mathbf{x}_{1}, \ldots, \mathbf{x}_{N}\right\}$ with corresponding target values $t_{1}, \ldots, t_{N}$. We group the target variables $\left\{t_{n}\right\}$ into a column vector that we denote by $\mathbf{t}$ where the typeface is chosen to distinguish it from a single observation of a multivariate target, which would be denoted $\mathbf{t}$. Making the assumption that these data points are drawn independently from the distribution (4.8), we obtain an expression for the likelihood function, which is a function of the adjustable parameters $\mathbf{w}$ and $\sigma^{2}$ :

$$
p\left(\mathbf{t} \mid \mathbf{X}, \mathbf{w}, \sigma^{2}\right)=\prod_{n=1}^{N} \mathcal{N}\left(t_{n} \mid \mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right), \sigma^{2}\right)
$$

where we have used (4.3). Taking the logarithm of the likelihood function and making use of the standard form (2.49) for the univariate Gaussian, we have

$$
\begin{aligned}
\ln p\left(\mathbf{t} \mid \mathbf{X}, \mathbf{w}, \sigma^{2}\right) & =\sum_{n=1}^{N} \ln \mathcal{N}\left(t_{n} \mid \mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right), \sigma^{2}\right) \\
& =-\frac{N}{2} \ln \sigma^{2}-\frac{N}{2} \ln (2 \pi)-\frac{1}{\sigma^{2}} E_{D}(\mathbf{w})
\end{aligned}
$$

where the sum-of-squares error function is defined by

$$
E_{D}(\mathbf{w})=\frac{1}{2} \sum_{n=1}^{N}\left\{t_{n}-\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right)\right\}^{2}
$$

The first two terms in (4.10) can be treated as constants when determining $\mathbf{w}$ because they are independent of $\mathbf{w}$. Therefore, as we saw previously, maximizing the likelihood function under a Gaussian noise distribution is equivalent to minimizing the sum-of-squares error function (4.11).

\title{
4.1.3 Maximum likelihood
}

Having written down the likelihood function, we can use maximum likelihood to determine $\mathbf{w}$ and $\sigma^{2}$. Consider first the maximization with respect to $\mathbf{w}$. The gradient of the $\log$ likelihood function (4.10) with respect to $\mathrm{w}$ takes the form

$$
\nabla_{\mathbf{w}} \ln p\left(\mathbf{t} \mid \mathbf{X}, \mathbf{w}, \sigma^{2}\right)=\frac{1}{\sigma^{2}} \sum_{n=1}^{N}\left\{t_{n}-\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right)\right\} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right)^{\mathrm{T}}
$$

Setting this gradient to zero gives

$$
0=\sum_{n=1}^{N} t_{n} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right)^{\mathrm{T}}-\mathbf{w}^{\mathrm{T}}\left(\sum_{n=1}^{N} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right) \boldsymbol{\phi}\left(\mathbf{x}_{n}\right)^{\mathrm{T}}\right)
$$

Solving for $\mathbf{w}$ we obtain

$$
\mathbf{w}_{\mathrm{ML}}=\left(\boldsymbol{\Phi}^{\mathrm{T}} \boldsymbol{\Phi}\right)^{-1} \boldsymbol{\Phi}^{\mathrm{T}} \mathbf{t}
$$

which are known as the normal equations for the least-squares problem. Here $\boldsymbol{\Phi}$ is an $N \times M$ matrix, called the design matrix, whose elements are given by $\Phi_{n j}=\phi_{j}\left(\mathbf{x}_{n}\right)$, so that

$$
\boldsymbol{\Phi}=\left(\begin{array}{cccc}
\phi_{0}\left(\mathbf{x}_{1}\right) & \phi_{1}\left(\mathbf{x}_{1}\right) & \cdots & \phi_{M-1}\left(\mathbf{x}_{1}\right) \\
\phi_{0}\left(\mathbf{x}_{2}\right) & \phi_{1}\left(\mathbf{x}_{2}\right) & \cdots & \phi_{M-1}\left(\mathbf{x}_{2}\right) \\
\vdots & \vdots & \ddots & \vdots \\
\phi_{0}\left(\mathbf{x}_{N}\right) & \phi_{1}\left(\mathbf{x}_{N}\right) & \cdots & \phi_{M-1}\left(\mathbf{x}_{N}\right)
\end{array}\right)
$$

The quantity

$$
\boldsymbol{\Phi}^{\dagger} \equiv\left(\boldsymbol{\Phi}^{\mathrm{T}} \boldsymbol{\Phi}\right)^{-1} \boldsymbol{\Phi}^{\mathrm{T}}
$$

is known as the Moore-Penrose pseudo-inverse of the matrix $\boldsymbol{\Phi}$ (Rao and Mitra, 1971; Golub and Van Loan, 1996). It can be regarded as a generalization of the notion of a matrix inverse to non-square matrices. Indeed, if $\boldsymbol{\Phi}$ is square and invertible, then using the property $(\mathbf{A B})^{-1}=\mathbf{B}^{-1} \mathbf{A}^{-1}$ we see that $\boldsymbol{\Phi}^{\dagger} \equiv \boldsymbol{\Phi}^{-1}$.

At this point, we can gain some insight into the role of the bias parameter $w_{0}$. If we make the bias parameter explicit, then the error function (4.11) becomes

$$
E_{D}(\mathbf{w})=\frac{1}{2} \sum_{n=1}^{N}\left\{t_{n}-w_{0}-\sum_{j=1}^{M-1} w_{j} \phi_{j}\left(\mathbf{x}_{n}\right)\right\}^{2}
$$

Setting the derivative with respect to $w_{0}$ equal to zero and solving for $w_{0}$, we obtain

$$
w_{0}=\bar{t}-\sum_{j=1}^{M-1} w_{j} \overline{\phi_{j}}
$$

where we have defined

$$
\bar{t}=\frac{1}{N} \sum_{n=1}^{N} t_{n}, \quad \overline{\phi_{j}}=\frac{1}{N} \sum_{n=1}^{N} \phi_{j}\left(\mathbf{x}_{n}\right)
$$

Thus, the bias $w_{0}$ compensates for the difference between the averages (over the training set) of the target values and the weighted sum of the averages of the basis function values.

We can also maximize the log likelihood function (4.10) with respect to the variance $\sigma^{2}$, giving

$$
\sigma_{\mathrm{ML}}^{2}=\frac{1}{N} \sum_{n=1}^{N}\left\{t_{n}-\mathbf{w}_{\mathrm{ML}}^{\mathrm{T}} \phi\left(\mathbf{x}_{n}\right)\right\}^{2}
$$

and so we see that the maximum likelihood value of the variance parameter is given by the residual variance of the target values around the regression function.

Figure 4.3 Geometrical interpretation of the leastsquares solution in an $N$-dimensional space whose axes are the values of $t_{1}, \ldots, t_{N}$. The least-squares regression function is obtained by finding the orthogonal projection of the data vector $\mathbf{t}$ onto the subspace spanned by the basis functions $\phi_{j}(\mathbf{x})$ in which each basis function is viewed as a vector $\varphi_{j}$ of length $N$ with elements $\phi_{j}\left(\mathbf{x}_{n}\right)$.

![](https://cdn.mathpix.com/cropped/2024_05_26_4d03a03b9a49734662f9g-1.jpg?height=367&width=543&top_left_y=217&top_left_x=1106

ChatGPT figure/image summary: The image is a geometric illustration of the least squares solution in an N-dimensional space. It shows a diagram with three axes. The red outline depicts a two-dimensional subspace 'S'. Inside this subspace, two vectors are shown, labeled as 'φ1' and 'φ2', which represent two basis functions projected in the N-dimensional space. The green vector labeled 't' stands perpendicularly outside of the subspace 'S', representing the vector of target values in the N-dimensional space. The blue vector labeled 'y' is inside the subspace 'S' and represents the least squares solution—it is the orthogonal projection of vector 't' onto the subspace 'S'. This diagram serves to visualize how the regression function in a least squares problem is effectively the projection of the data onto the subspace spanned by the basis functions.)

\title{
4.1.4 Geometry of least squares
}

At this point, it is instructive to consider the geometrical interpretation of the least-squares solution. To do this, we consider an $N$-dimensional space whose axes are given by the $t_{n}$, so that $\mathbf{t}=\left(t_{1}, \ldots, t_{N}\right)^{\mathrm{T}}$ is a vector in this space. Each basis function $\phi_{j}\left(\mathbf{x}_{n}\right)$, evaluated at the $N$ data points, can also be represented as a vector in the same space, denoted by $\varphi_{j}$, as illustrated in Figure 4.3. Note that $\varphi_{j}$ corresponds to the $j$ th column of $\boldsymbol{\Phi}$, whereas $\phi\left(\mathbf{x}_{n}\right)$ corresponds to the transpose of the $n$th row of $\boldsymbol{\Phi}$. If the number $M$ of basis functions is smaller than the number $N$ of data points, then the $M$ vectors $\phi_{j}\left(\mathbf{x}_{n}\right)$ will span a linear subspace $\mathcal{S}$ of dimensionality $M$. We define $\mathbf{y}$ to be an $N$-dimensional vector whose $n$th element is given by $y\left(\mathbf{x}_{n}, \mathbf{w}\right)$, where $n=1, \ldots, N$. Because $\mathbf{y}$ is an arbitrary linear combination of the vectors $\varphi_{j}$, it can live anywhere in the $M$-dimensional subspace. The sum-of-squares error (4.11) is then equal (up to a factor of $1 / 2$ ) to the squared Euclidean distance between $\mathbf{y}$ and $\mathbf{t}$. Thus, the least-squares solution for $\mathbf{w}$ corresponds to that choice of $\mathbf{y}$ that lies in subspace $\mathcal{S}$ and is closest to t. Intuitively, from Figure 4.3, we anticipate that this solution corresponds to the orthogonal projection of $\mathbf{t}$ onto the subspace $\mathcal{S}$. This is indeed the case, as can easily be verified by noting that the solution for $\mathbf{y}$ is given by $\boldsymbol{\Phi} \mathbf{w}_{\mathrm{ML}}$ and then confirming that this takes the form of an orthogonal projection.

In practice, a direct solution of the normal equations can lead to numerical difficulties when $\boldsymbol{\Phi}^{\mathrm{T}} \boldsymbol{\Phi}$ is close to singular. In particular, when two or more of the basis vectors $\varphi_{j}$ are co-linear, or nearly so, the resulting parameter values can have large magnitudes. Such near degeneracies will not be uncommon when dealing with real data sets. The resulting numerical difficulties can be addressed using the technique of singular value decomposition, or SVD (Deisenroth, Faisal, and Ong, 2020). Note that the addition of a regularization term ensures that the matrix is non-singular, even in the presence of degeneracies.

\subsection*{4.1.5 Sequential learning}

The maximum likelihood solution (4.14) involves processing the entire training set in one go and is known as a batch method. This can become computationally costly for large data sets. If the data set is sufficiently large, it may be worthwhile to use sequential algorithms, also known as online algorithms, in which the data points are considered one at a time and the model parameters updated after each such presentation. Sequential learning is also appropriate for real-time applications in which the data observations arrive in a continuous stream and predictions must be

\section*{Chapter 7}

Section 1.2

\section*{Exercise 4.6}

made before all the data points are seen.

We can obtain a sequential learning algorithm by applying the technique of stochastic gradient descent, also known as sequential gradient descent, as follows. If the error function comprises a sum over data points $E=\sum_{n} E_{n}$, then after presentation of data point $n$, the stochastic gradient descent algorithm updates the parameter vector $\mathbf{w}$ using

$$
\mathbf{w}^{(\tau+1)}=\mathbf{w}^{(\tau)}-\eta \nabla E_{n}
$$

where $\tau$ denotes the iteration number, and $\eta$ is a suitably chosen learning rate parameter. The value of $\mathbf{w}$ is initialized to some starting vector $\mathbf{w}^{(0)}$. For the sum-ofsquares error function (4.11), this gives

$$
\mathbf{w}^{(\tau+1)}=\mathbf{w}^{(\tau)}+\eta\left(t_{n}-\mathbf{w}^{(\tau) \mathrm{T}} \boldsymbol{\phi}_{n}\right) \boldsymbol{\phi}_{n}
$$

where $\phi_{n}=\phi\left(\mathbf{x}_{n}\right)$. This is known as the least-mean-squares or the LMS algorithm.

\title{
4.1.6 Regularized least squares
}

We have previously introduced the idea of adding a regularization term to an error function to control over-fitting, so that the total error function to be minimized takes the form

$$
E_{D}(\mathbf{w})+\lambda E_{W}(\mathbf{w})
$$

where $\lambda$ is the regularization coefficient that controls the relative importance of the data-dependent error $E_{D}(\mathbf{w})$ and the regularization term $E_{W}(\mathbf{w})$. One of the simplest forms of regularizer is given by the sum of the squares of the weight vector elements:

$$
E_{W}(\mathbf{w})=\frac{1}{2} \sum_{j} w_{j}^{2}=\frac{1}{2} \mathbf{w}^{\mathrm{T}} \mathbf{w}
$$

If we also consider the sum-of-squares error function given by

$$
E_{D}(\mathbf{w})=\frac{1}{2} \sum_{n=1}^{N}\left\{t_{n}-\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right)\right\}^{2}
$$

then the total error function becomes

$$
\frac{1}{2} \sum_{n=1}^{N}\left\{t_{n}-\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right)\right\}^{2}+\frac{\lambda}{2} \mathbf{w}^{\mathrm{T}} \mathbf{w}
$$

In statistics, this regularizer provides an example of a parameter shrinkage method because it shrinks parameter values towards zero. It has the advantage that the error function remains a quadratic function of $\mathbf{w}$, and so its exact minimizer can be found in closed form. Specifically, setting the gradient of (4.26) with respect to w to zero and solving for $\mathrm{w}$ as before, we obtain

$$
\mathbf{w}=\left(\lambda \mathbf{I}+\boldsymbol{\Phi}^{\mathrm{T}} \boldsymbol{\Phi}\right)^{-1} \boldsymbol{\Phi}^{\mathrm{T}} \mathbf{t} .
$$

This represents a simple extension of the least-squares solution (4.14).

Figure 4.4 Representation of a linear regression model as a neural network having a single layer of connections. Each basis function is represented by a node, with the solid node representing the 'bias' basis function $\phi_{0}$. Likewise each output $y_{1}, \ldots, y_{K}$ is represented by a node. The links between the nodes represent the corresponding weight and bias

![](https://cdn.mathpix.com/cropped/2024_05_26_0b66c2c41c506aebc39ag-1.jpg?height=338&width=649&top_left_y=212&top_left_x=992

ChatGPT figure/image summary: The image appears to be a schematic representation of a neural network with a single layer linear model architecture used in machine learning, specifically for regression tasks. The network consists of several nodes (represented as circles in the image) connected by lines, which typically symbolize the weighted connections between the inputs and outputs.

At the bottom, there is a node labeled with \(\phi_0(x)\), indicating the bias node, which usually corresponds to the bias term in a linear model where no input is needed (it always outputs 1). Above this node, there are other nodes labeled with \(\phi_1(x)\) to \(\phi_{M-1}(x)\), representing the basis functions for the input data \(x\).

The top layer nodes are labeled with \(y_1(x, w)\) to \(y_K(x, w)\), representing the output nodes of the network for multiple target variables \(y_1, \ldots, y_K\). They correspond to the predicted outputs of the model, each determined by a distinct weighted sum of the transformed input features through the basis functions. The solid arrows indicate the mapping from the input functions (\(\phi\) nodes) to the output nodes.

The diagram serves as a visualization for the concepts described in the text regarding linear regression models, basis functions, and regularization, as well as the extension of these concepts to models that predict multiple outputs (\(K>1\)).)
parameters.

\title{
4.1.7 Multiple outputs
}

So far, we have considered situations with a single target variable $t$. In some applications, we may wish to predict $K>1$ target variables, which we denote collectively by the target vector $\mathbf{t}=\left(t_{1}, \ldots, t_{K}\right)^{\mathrm{T}}$. This could be done by introducing a different set of basis functions for each component of $t$, leading to multiple, independent regression problems. However, a more common approach is to use the same set of basis functions to model all of the components the target vector so that

$$
\mathbf{y}(\mathbf{x}, \mathbf{w})=\mathbf{W}^{\mathrm{T}} \boldsymbol{\phi}(\mathbf{x})
$$

where $\mathbf{y}$ is a $K$-dimensional column vector, $\mathbf{W}$ is an $M \times K$ matrix of parameters, and $\phi(\mathbf{x})$ is an $M$-dimensional column vector with elements $\phi_{j}(\mathbf{x})$ with $\phi_{0}(\mathbf{x})=1$ as before. Again, this can be represented as a neural network having a single layer of parameters, as shown in Figure 4.4.

Suppose we take the conditional distribution of the target vector to be an isotropic Gaussian of the form

$$
p\left(\mathbf{t} \mid \mathbf{x}, \mathbf{W}, \sigma^{2}\right)=\mathcal{N}\left(\mathbf{t} \mid \mathbf{W}^{\mathrm{T}} \boldsymbol{\phi}(\mathbf{x}), \sigma^{2} \mathbf{I}\right)
$$

If we have a set of observations $\mathbf{t}_{1}, \ldots, \mathbf{t}_{N}$, we can combine these into a matrix $\mathbf{T}$ of size $N \times K$ such that the $n$th row is given by $\mathbf{t}_{n}^{\mathrm{T}}$. Similarly, we can combine the input vectors $\mathbf{x}_{1}, \ldots, \mathbf{x}_{N}$ into a matrix $\mathbf{X}$. The log likelihood function is then given by

$$
\begin{aligned}
\ln p\left(\mathbf{T} \mid \mathbf{X}, \mathbf{W}, \sigma^{2}\right) & =\sum_{n=1}^{N} \ln \mathcal{N}\left(\mathbf{t}_{n} \mid \mathbf{W}^{\mathrm{T}} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right), \sigma^{2} \mathbf{I}\right) \\
& =-\frac{N K}{2} \ln \left(2 \pi \sigma^{2}\right)-\frac{1}{2 \sigma^{2}} \sum_{n=1}^{N}\left\|\mathbf{t}_{n}-\mathbf{W}^{\mathrm{T}} \boldsymbol{\phi}\left(\mathbf{x}_{n}\right)\right\|^{2}
\end{aligned}
$$

As before, we can maximize this function with respect to $\mathbf{W}$, giving

$$
\mathbf{W}_{\mathrm{ML}}=\left(\boldsymbol{\Phi}^{\mathrm{T}} \boldsymbol{\Phi}\right)^{-1} \boldsymbol{\Phi}^{\mathrm{T}} \mathbf{T}
$$

where we have combined the input feature vectors $\phi\left(\mathbf{x}_{1}\right), \ldots, \phi\left(\mathbf{x}_{N}\right)$ into a matrix $\boldsymbol{\Phi}$. If we examine this result for each target variable $t_{k}$, we have

$$
\mathbf{w}_{k}=\left(\boldsymbol{\Phi}^{\mathrm{T}} \boldsymbol{\Phi}\right)^{-1} \boldsymbol{\Phi}^{\mathrm{T}} \mathbf{t}_{k}=\boldsymbol{\Phi}^{\dagger} \mathbf{t}_{k}
$$


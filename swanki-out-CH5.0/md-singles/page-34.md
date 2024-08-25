which is known as the probit function. It has a sigmoidal shape and is compared with the logistic sigmoid function in Figure 5.12. Note that the use of a Gaussian distribution with general mean and variances does not change the model because this is equivalent to a re-scaling of the linear coefficients \(\mathbf{w}\). Many numerical packages can evaluate a closely related function defined by

\[
\operatorname{erf}(a)=\frac{2}{\sqrt{\pi}} \int_{0}^{a} \exp \left(-\theta^{2} / 2\right) \mathrm{d} \theta
\]

and known as the erf function or error function (not to be confused with the error function of a machine learning model). It is related to the probit function by

\[
\Phi(a)=\frac{1}{2}\left\{1+\frac{1}{\sqrt{2}} \operatorname{erf}(a)\right\}
\]

The generalized linear model based on a probit activation function is known as probit regression. We can determine the parameters of this model using maximum likelihood by a straightforward extension of the ideas discussed earlier. In practice, the results found using probit regression tend to be like those of logistic regression.

One issue that can occur in practical applications is that of outliers, which can arise for instance through errors in measuring the input vector \(\mathrm{x}\) or through mislabelling of the target value \(t\). Because such points can lie a long way to the wrong side of the ideal decision boundary, they can seriously distort the classifier. The logistic and probit regression models behave differently in this respect because the tails of the logistic sigmoid decay asymptotically like \(\exp (-x)\) for \(|x| \rightarrow \infty\), whereas for the probit activation function, they decay like \(\exp \left(-x^{2}\right)\), and so the probit model can be significantly more sensitive to outliers.

\title{
5.4.6 Canonical link functions
}

For the linear regression model with a Gaussian noise distribution, the error function, corresponding to the negative \(\log\) likelihood, is given by (4.11). If we take the derivative with respect to the parameter vector \(\mathbf{w}\) of the contribution to the error function from a data point \(n\), this takes the form of the 'error' \(y_{n}-t_{n}\) times the feature vector \(\phi_{n}\), where \(y_{n}=\mathbf{w}^{\mathrm{T}} \phi_{n}\). Similarly, for the combination of the logisticsigmoid activation function and the cross-entropy error function (5.74) and for the softmax activation function with the multi-class cross-entropy error function (5.80), we again obtain this same simple form. We now show that this is a general result of assuming a conditional distribution for the target variable from the exponential family along with a corresponding choice for the activation function known as the canonical link function.

We again make use of the restricted form (3.169) of exponential family distributions. Note that here we are applying the assumption of exponential family distribution to the target variable \(t\), in contrast to Section 5.3.4 where we applied it to the input vector \(\mathrm{x}\). We therefore consider conditional distributions of the target variable of the form

\[
p(t \mid \eta, s)=\frac{1}{s} h\left(\frac{t}{s}\right) g(\eta) \exp \left\{\frac{\eta t}{s}\right\}
\]
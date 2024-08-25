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
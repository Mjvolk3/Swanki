\section*{Exercise 5.14}

Section 5.1.4

Section 11.2 .3

\section*{Exercise 5.16}

where we have defined

$$
\begin{aligned}
\mathbf{S} & =\frac{N_{1}}{N} \mathbf{S}_{1}+\frac{N_{2}}{N} \mathbf{S}_{2} \\
\mathbf{S}_{1} & =\frac{1}{N_{1}} \sum_{n \in \mathcal{C}_{1}}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{1}\right)\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{1}\right)^{\mathrm{T}} \\
\mathbf{S}_{2} & =\frac{1}{N_{2}} \sum_{n \in \mathcal{C}_{2}}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{2}\right)\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{2}\right)^{\mathrm{T}}
\end{aligned}
$$

Using the standard result for the maximum likelihood solution for a Gaussian distribution, we see that $\boldsymbol{\Sigma}=\mathbf{S}$, which represents a weighted average of the covariance matrices associated with each of the two classes separately.

This result is easily extended to the $K$-class problem to obtain the corresponding maximum likelihood solutions for the parameters in which each class-conditional density is Gaussian with a shared covariance matrix. Note that the approach of fitting Gaussian distributions to the classes is not robust to outliers, because the maximum likelihood estimation of a Gaussian is not robust.

\subsection*{5.3.3 Discrete features}

Let us now consider discrete feature values $x_{i}$. For simplicity, we begin by looking at binary feature values $x_{i} \in\{0,1\}$ and discuss the extension to more general discrete features shortly. If there are $D$ inputs, then a general distribution would correspond to a table of $2^{D}$ numbers for each class and have $2^{D}-1$ independent variables (due to the summation constraint). Because this grows exponentially with the number of features, we can seek a more restricted representation. Here we will make the naive Bayes assumption in which the feature values are treated as independent and conditioned on the class $\mathcal{C}_{k}$. Thus, we have class-conditional distributions of the form

$$
p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)=\prod_{i=1}^{D} \mu_{k i}^{x_{i}}\left(1-\mu_{k i}\right)^{1-x_{i}}
$$

which contain $D$ independent parameters for each class. Substituting into (5.46) then gives

$$
a_{k}(\mathbf{x})=\sum_{i=1}^{D}\left\{x_{i} \ln \mu_{k i}+\left(1-x_{i}\right) \ln \left(1-\mu_{k i}\right)\right\}+\ln p\left(\mathcal{C}_{k}\right)
$$

which again are linear functions of the input values $x_{i}$. For $K=2$ classes, we can alternatively consider the logistic sigmoid formulation given by (5.40). Analogous results are obtained for discrete variables that take $L>2$ states.

\subsection*{5.3.4 Exponential family}

As we have seen, for both Gaussian distributed and discrete inputs, the posterior class probabilities are given by generalized linear models with logistic sigmoid ( $K=$
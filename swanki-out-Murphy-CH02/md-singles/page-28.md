\title{
2.6.4 Why is the Gaussian distribution so widely used?
}

The Gaussian distribution is the most widely used distribution in statistics and machine learning. There are several reasons for this. First, it has two parameters which are easy to interpret, and which capture some of the most basic properties of a distribution, namely its mean and variance. Second, the central limit theorem (Section 2.8.6) tells us that sums of independent random variables have an approximately Gaussian distribution, making it a good choice for modeling residual errors or "noise". Third, the Gaussian distribution makes the least number of assumptions (has maximum entropy), subject to the constraint of having a specified mean and variance, as we show in Section 3.4.4; this makes it a good default choice in many cases. Finally, it has a simple mathematical form, which results in easy to implement, but often highly effective, methods, as we will see in Section 3.2.

From a historical perspective, it's worth remarking that the term "Gaussian distribution" is a bit misleading, since, as Jaynes [Jay03, p241] notes: "The fundamental nature of this distribution and its main properties were noted by Laplace when Gauss was six years old; and the distribution itself had been found by de Moivre before Laplace was born". However, Gauss popularized the use of the distribution in the 1800s, and the term "Gaussian" is now widely used in science and engineering.

The name "normal distribution" seems to have arisen in connection with the normal equations in linear regression (see Section 11.2.2.2). However, we prefer to avoid the term "normal", since it suggests other distributions are "abnormal", whereas, as Jaynes [Jay03] points out, it is the Gaussian that is abnormal in the sense that it has many special properties that are untypical of general distributions.

\subsection*{2.6.5 Dirac delta function as a limiting case}

As the variance of a Gaussian goes to 0 , the distribution approaches an infinitely narrow, but infinitely tall, "spike" at the mean. We can write this as follows:

\[
\lim _{\sigma \rightarrow 0} \mathcal{N}\left(y \mid \mu, \sigma^{2}\right) \rightarrow \delta(y-\mu)
\]

where \(\delta\) is the Dirac delta function, defined by

\[
\delta(x)= \begin{cases}+\infty & \text { if } x=0 \\ 0 & \text { if } x \neq 0\end{cases}
\]

where

\[
\int_{-\infty}^{\infty} \delta(x) d x=1
\]

A slight variant of this is to define

\[
\delta_{y}(x)= \begin{cases}+\infty & \text { if } x=y \\ 0 & \text { if } x \neq y\end{cases}
\]

Note that we have

\[
\delta_{y}(x)=\delta(x-y)
\]

Draft of "Probabilistic Machine Learning: An Introduction". August 8, 2022
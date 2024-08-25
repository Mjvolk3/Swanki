Figure 3.1 Histogram plot of the binomial distribution (3.9) as a function of \(m\) for \(N=10\) and \(\mu=0.25\).

![](https://cdn.mathpix.com/cropped/2024_05_13_f10b60699ae8e7fdd3dcg-1.jpg?height=513&width=732&top_left_y=232&top_left_x=911)

where

\[
\binom{N}{m} \equiv \frac{N!}{(N-m)!m!}
\]

Exercise 3.3

Exercise 2.10

is the number of ways of choosing \(m\) objects out of a total of \(N\) identical objects without replacement. Figure 3.1 shows a plot of the binomial distribution for \(N=10\) and \(\mu=0.25\).

The mean and variance of the binomial distribution can be found by using the results that, for independent events, the mean of the sum is the sum of the means and the variance of the sum is the sum of the variances. Because \(m=x_{1}+\ldots+x_{N}\) and because for each observation the mean and variance are given by (3.3) and (3.4), respectively, we have

\[
\begin{aligned}
\mathbb{E}[m] & \equiv \sum_{m=0}^{N} m \operatorname{Bin}(m \mid N, \mu)=N \mu \\
\operatorname{var}[m] & \equiv \sum_{m=0}^{N}(m-\mathbb{E}[m])^{2} \operatorname{Bin}(m \mid N, \mu)=N \mu(1-\mu)
\end{aligned}
\]

Exercise 3.4 These results can also be proved directly by using calculus.

\title{
3.1.3 Multinomial distribution
}

Binary variables can be used to describe quantities that can take one of two possible values. Often, however, we encounter discrete variables that can take on one of \(K\) possible mutually exclusive states. Although there are various alternative ways to express such variables, we will see shortly that a particularly convenient representation is the 1-of- \(K\) scheme, sometimes called 'one-hot encoding', in which the variable is represented by a \(K\)-dimensional vector \(\mathrm{x}\) in which one of the elements \(x_{k}\) equals 1 and all remaining elements equal 0 . So, for instance, if we have a variable that can take \(K=6\) states and a particular observation of the variable happens to
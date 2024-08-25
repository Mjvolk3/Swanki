\[
\begin{array}{cccccccc|l}
- & - & 1 & 2 & 3 & 4 & - & - & \\
\hline 7 & 6 & 5 & - & - & - & - & - & z_{0}=x_{0} y_{0}=5 \\
- & 7 & 6 & 5 & - & - & - & - & z_{1}=x_{0} y_{1}+x_{1} y_{0}=16 \\
- & - & 7 & 6 & 5 & - & - & - & z_{2}=x_{0} y_{2}+x_{1} y_{1}+x_{2} y_{0}=34 \\
- & - & - & 7 & 6 & 5 & - & - & z_{3}=x_{1} y_{2}+x_{2} y_{1}+x_{3} y_{0}=52 \\
- & - & - & - & 7 & 6 & 5 & - & z_{4}=x_{2} y_{2}+x_{3} y_{1}=45 \\
- & - & - & - & - & 7 & 6 & 5 & z_{5}=x_{3} y_{2}=28
\end{array}
\]

Table 2.4: Discrete convolution of \(\boldsymbol{x}=[1,2,3,4]\) with \(\boldsymbol{y}=[5,6,7]\) to yield \(\boldsymbol{z}=[5,16,34,52,45,28]\). In general, \(z_{n}=\sum_{k=-\infty}^{\infty} x_{k} y_{n-k}\). We see that this operation consists of "flipping" \(\boldsymbol{y}\) and then "dragging" it over \(\boldsymbol{x}\), multiplying elementwise, and adding up the results.

\title{
2.8.5 The convolution theorem
}

Let \(y=x_{1}+x_{2}\), where \(x_{1}\) and \(x_{2}\) are independent rv's. If these are discrete random variables, we can compute the pmf for the sum as follows:

\[
p(y=j)=\sum_{k} p\left(x_{1}=k\right) p\left(x_{2}=j-k\right)
\]

for \(j=\ldots,-2,-1,0,1,2, \ldots\)

If \(x_{1}\) and \(x_{2}\) have pdf's \(p_{1}\left(x_{1}\right)\) and \(p_{2}\left(x_{2}\right)\), what is the distribution of \(y\) ? The cdf for \(y\) is given by

\[
P_{y}\left(y^{*}\right)=\operatorname{Pr}\left(y \leq y^{*}\right)=\int_{-\infty}^{\infty} p_{1}\left(x_{1}\right)\left[\int_{-\infty}^{y^{*}-x_{1}} p_{2}\left(x_{2}\right) d x_{2}\right] d x_{1}
\]

where we integrate over the region \(R\) defined by \(x_{1}+x_{2}<y^{*}\). Thus the pdf for \(y\) is

\[
p(y)=\left[\frac{d}{d y^{*}} P_{y}\left(y^{*}\right)\right]_{y^{*}=y}=\int p_{1}\left(x_{1}\right) p_{2}\left(y-x_{1}\right) d x_{1}
\]

where we used the rule of differentiating under the integral sign:

\[
\frac{d}{d x} \int_{a(x)}^{b(x)} f(t) d t=f(b(x)) \frac{d b(x)}{d x}-f(a(x)) \frac{d a(x)}{d x}
\]

We can write Equation (2.170) as follows:

\[
p=p_{1} \circledast p_{2}
\]

where \(\circledast\) represents the convolution operator. For finite length vectors, the integrals become sums, and convolution can be thought of as a "flip and drag" operation, as illustrated in Table 2.4. Consequently, Equation (2.170) is called the convolution theorem.

For example, suppose we roll two dice, so \(p_{1}\) and \(p_{2}\) are both the discrete uniform distributions
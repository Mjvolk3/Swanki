![](https://cdn.mathpix.com/cropped/2024_06_13_0d3c3fabafab878573b2g-1.jpg?height=362&width=941&top_left_y=204&top_left_x=545)

Figure 2.12: Softmax distribution \(\operatorname{softmax}(\boldsymbol{a} / T)\), where \(\boldsymbol{a}=(3,0,1)\), at temperatures of \(T=100, T=2\) and \(T=1\). When the temperature is high (left), the distribution is uniform, whereas when the temperature is low (right), the distribution is "spiky", with most of its mass on the largest element. Generated by softmax_plot.ipynb.

shows up, i.e., \(y_{c}=N_{c} \triangleq \sum_{n=1}^{N} \mathbb{I}\left(y_{n}=c\right)\). Now \(\boldsymbol{y}\) is no longer one-hot, but is "multi-hot", since it has a non-zero entry for every value of \(c\) that was observed across all \(N\) trials. The distribution of \(\boldsymbol{y}\) is given by the multinomial distribution:

\[
\mathcal{M}(\boldsymbol{y} \mid N, \boldsymbol{\theta}) \triangleq\binom{N}{y_{1} \ldots y_{C}} \prod_{c=1}^{C} \theta_{c}^{y_{c}}=\binom{N}{N_{1} \ldots N_{C}} \prod_{c=1}^{C} \theta_{c}^{N_{c}}
\]

where \(\theta_{c}\) is the probability that side \(c\) shows up, and

\[
\binom{N}{N_{1} \ldots N_{C}} \triangleq \frac{N!}{N_{1}!N_{2}!\cdots N_{C}!}
\]

is the multinomial coefficient, which is the number of ways to divide a set of size \(N=\sum_{c=1}^{C} N_{c}\) into subsets with sizes \(N_{1}\) up to \(N_{C}\). If \(N=1\), the multinomial distribution becomes the categorical distribution.

\title{
2.5.2 Softmax function
}

In the conditional case, we can define

\[
p(y \mid \boldsymbol{x}, \boldsymbol{\theta})=\operatorname{Cat}(y \mid f(\boldsymbol{x} ; \boldsymbol{\theta}))
\]

which we can also write as

\[
p(y \mid \boldsymbol{x}, \boldsymbol{\theta})=\mathcal{M}(\boldsymbol{y} \mid 1, f(\boldsymbol{x} ; \boldsymbol{\theta}))
\]

We require that \(0 \leq f_{c}(\boldsymbol{x} ; \boldsymbol{\theta}) \leq 1\) and \(\sum_{c=1}^{C} f_{c}(\boldsymbol{x} ; \boldsymbol{\theta})=1\).

To avoid the requirement that \(f\) directly predict a probability vector, it is common to pass the output from \(f\) into the softmax function [Bri90], also called the multinomial logit. This is defined as follows:

\[
\operatorname{softmax}(\boldsymbol{a}) \triangleq\left[\frac{e^{a_{1}}}{\sum_{c^{\prime}=1}^{C} e^{a_{c^{\prime}}}}, \ldots, \frac{e^{a_{C}}}{\sum_{c^{\prime}=1}^{C} e^{a_{c^{\prime}}}}\right]
\]

Draft of "Probabilistic Machine Learning: An Introduction". August 8, 2022
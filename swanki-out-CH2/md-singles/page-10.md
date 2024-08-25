Figure 2.6 The concept of probability for discrete variables can be extended to that of a probability density \(p(x)\) over a continuous variable \(x\) and is such that the probability of \(x\) lying in the interval \((x, x+\delta x)\) is given by \(p(x) \delta x\) for \(\delta x \rightarrow 0\). The probability density can be expressed as the derivative of a cumulative distribution function \(P(x)\).

![](https://cdn.mathpix.com/cropped/2024_05_10_46157df5e120ef4bbe80g-1.jpg?height=545&width=767&top_left_y=216&top_left_x=891)

\title{
2.2. Probability Densities
}

As well as considering probabilities defined over discrete sets of values, we also wish to consider probabilities with respect to continuous variables. For instance, we might wish to predict what dose of drug to give to a patient. Since there will be uncertainty in this prediction, we want to quantify this uncertainty and again we can make use of probabilities. However, we cannot simply apply the concepts of probability discussed so far directly, since the probability of observing a specific value for a continuous variable, to infinite precision, will effectively be zero. Instead, we need to introduce the concept of a probability density. Here we will limit ourselves to a relatively informal discussion.

We define the probability density \(p(x)\) over a continuous variable \(x\) to be such that the probability of \(x\) falling in the interval \((x, x+\delta x)\) is given by \(p(x) \delta x\) for \(\delta x \rightarrow 0\). This is illustrated in Figure 2.6. The probability that \(x\) will lie in an interval \((a, b)\) is then given by

\[
p(x \in(a, b))=\int_{a}^{b} p(x) \mathrm{d} x
\]

Because probabilities are non-negative, and because the value of \(x\) must lie somewhere on the real axis, the probability density \(p(x)\) must satisfy the two conditions

\[
\begin{array}{r}
p(x) \geqslant 0 \\
\int_{-\infty}^{\infty} p(x) \mathrm{d} x=1
\end{array}
\]

The probability that \(x\) lies in the interval \((-\infty, z)\) is given by the cumulative distribution function defined by

\[
P(z)=\int_{-\infty}^{z} p(x) \mathrm{d} x
\]
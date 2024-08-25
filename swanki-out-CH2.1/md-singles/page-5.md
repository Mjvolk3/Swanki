Figure 2.4 We can derive the sum and product rules of probability by considering a random variable \(X\), which takes the values \(\left\{x_{i}\right\}\) where \(i=1, \ldots, L\), and a second random variable \(Y\), which takes the values \(\left\{y_{j}\right\}\) where \(j=\) \(1, \ldots, M\). In this illustration, we have \(L=5\) and \(M=3\). If we consider the total number \(N\) of instances of these variables, then we denote the number of instances where \(X=x_{i}\) and \(Y=y_{j}\) by \(n_{i j}\), which is the number of instances in the corresponding cell of the array. The number of instances in column \(i\), corresponding to \(X=x_{i}\), is denoted by \(c_{i}\), and the number of instances in row \(j\), corresponding to \(Y=y_{j}\), is denoted by \(r_{j}\).

![](https://cdn.mathpix.com/cropped/2024_05_10_0ac15dbddb7cf99e2d43g-1.jpg?height=361&width=539&top_left_y=215&top_left_x=1113)

given by the fraction of the total number of points that fall in column \(i\), so that

\[
p\left(X=x_{i}\right)=\frac{c_{i}}{N}
\]

Since \(\sum_{i} c_{i}=N\), we see that

\[
\sum_{i=1}^{L} p\left(X=x_{i}\right)=1
\]

and, hence, the probabilities sum to one as required. Because the number of instances in column \(i\) in Figure 2.4 is just the sum of the number of instances in each cell of that column, we have \(c_{i}=\sum_{j} n_{i j}\) and therefore, from (2.1) and (2.2), we have

\[
p\left(X=x_{i}\right)=\sum_{j=1}^{M} p\left(X=x_{i}, Y=y_{j}\right)
\]

which is the sum rule of probability. Note that \(p\left(X=x_{i}\right)\) is sometimes called the marginal probability and is obtained by marginalizing, or summing out, the other variables (in this case \(Y\) ).

If we consider only those instances for which \(X=x_{i}\), then the fraction of such instances for which \(Y=y_{j}\) is written \(p\left(Y=y_{j} \mid X=x_{i}\right)\) and is called the conditional probability of \(Y=y_{j}\) given \(X=x_{i}\). It is obtained by finding the fraction of those points in column \(i\) that fall in cell \(i, j\) and, hence, is given by

\[
p\left(Y=y_{j} \mid X=x_{i}\right)=\frac{n_{i j}}{c_{i}}
\]

Summing both sides over \(j\) and using \(\sum_{j} n_{i j}=c_{i}\), we obtain

\[
\sum_{j=1}^{M} p\left(Y=y_{j} \mid X=x_{i}\right)=1
\]
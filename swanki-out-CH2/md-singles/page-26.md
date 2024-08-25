the number of different ways of allocating the objects to the bins. There are \(N\) ways to choose the first object, \((N-1)\) ways to choose the second object, and so on, leading to a total of \(N\) ! ways to allocate all \(N\) objects to the bins, where \(N\) ! (pronounced ' \(N\) factorial') denotes the product \(N \times(N-1) \times \cdots \times 2 \times 1\). However, we do not wish to distinguish between rearrangements of objects within each bin. In the \(i\) th bin there are \(n_{i}\) ! ways of reordering the objects, and so the total number of ways of allocating the \(N\) objects to the bins is given by

\[
W=\frac{N!}{\prod_{i} n_{i}!}
\]

which is called the multiplicity. The entropy is then defined as the logarithm of the multiplicity scaled by a constant factor \(1 / N\) so that

\[
\mathrm{H}=\frac{1}{N} \ln W=\frac{1}{N} \ln N!-\frac{1}{N} \sum_{i} \ln n_{i}!
\]

We now consider the limit \(N \rightarrow \infty\), in which the fractions \(n_{i} / N\) are held fixed, and apply Stirling's approximation:

\[
\ln N!\simeq N \ln N-N
\]

which gives

\[
\mathrm{H}=-\lim _{N \rightarrow \infty} \sum_{i}\left(\frac{n_{i}}{N}\right) \ln \left(\frac{n_{i}}{N}\right)=-\sum_{i} p_{i} \ln p_{i}
\]

where we have used \(\sum_{i} n_{i}=N\). Here \(p_{i}=\lim _{N \rightarrow \infty}\left(n_{i} / N\right)\) is the probability of an object being assigned to the \(i\) th bin. In physics terminology, the specific allocation of objects into bins is called a microstate, and the overall distribution of occupation numbers, expressed through the ratios \(n_{i} / N\), is called a macrostate. The multiplicity \(W\), which expresses the number of microstates in a given macrostate, is also known as the weight of the macrostate.

We can interpret the bins as the states \(x_{i}\) of a discrete random variable \(X\), where \(p\left(X=x_{i}\right)=p_{i}\). The entropy of the random variable \(X\) is then

\[
\mathrm{H}[p]=-\sum_{i} p\left(x_{i}\right) \ln p\left(x_{i}\right)
\]

Distributions \(p\left(x_{i}\right)\) that are sharply peaked around a few values will have a relatively low entropy, whereas those that are spread more evenly across many values will have higher entropy, as illustrated in Figure 2.14.

Because \(0 \leqslant p_{i} \leqslant 1\), the entropy is non-negative, and it will equal its minimum value of 0 when one of the \(p_{i}=1\) and all other \(p_{j \neq i}=0\). The maximum entropy Appendix \(C\) configuration can be found by maximizing \(\mathrm{H}\) using a Lagrange multiplier to enforce the normalization constraint on the probabilities. Thus, we maximize

\[
\widetilde{\mathrm{H}}=-\sum_{i} p\left(x_{i}\right) \ln p\left(x_{i}\right)+\lambda\left(\sum_{i} p\left(x_{i}\right)-1\right)
\]
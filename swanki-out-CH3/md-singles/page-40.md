Figure 3.16 (a) In the \(K\)-nearestneighbour classifier, a new point, shown by the black diamond, is classified according to the majority class membership of the \(K\) closest training data points, in this case \(K=\) 3. (b) In the nearest-neighbour ( \(K=1\) ) approach to classification, the resulting decision boundary is composed of hyperplanes that form perpendicular bisectors of pairs of points from different classes.

![](https://cdn.mathpix.com/cropped/2024_05_13_8f53b2b39e722c44ef82g-1.jpg?height=491&width=515&top_left_y=214&top_left_x=622)

(a)

![](https://cdn.mathpix.com/cropped/2024_05_13_8f53b2b39e722c44ef82g-1.jpg?height=504&width=515&top_left_y=212&top_left_x=1130)

(b)

with each class:

\[
p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)=\frac{K_{k}}{N_{k} V}
\]

Similarly, the unconditional density is given by

\[
p(\mathbf{x})=\frac{K}{N V}
\]

and the class priors are given by

\[
p\left(\mathcal{C}_{k}\right)=\frac{N_{k}}{N}
\]

We can now combine (3.187), (3.188), and (3.189) using Bayes' theorem to obtain the posterior probability of class membership:

\[
p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)=\frac{p\left(\mathbf{x} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right)}{p(\mathbf{x})}=\frac{K_{k}}{K}
\]

We can minimize the probability of misclassification by assigning the test point \(\mathrm{x}\) to the class having the largest posterior probability, corresponding to the largest value of \(K_{k} / K\). Thus, to classify a new point, we identify the \(K\) nearest points from the training data set and then assign the new point to the class having the largest number of representatives amongst this set. Ties can be broken at random. The particular case of \(K=1\) is called the nearest-neighbour rule, because a test point is simply assigned to the same class as the nearest point from the training set. These concepts are illustrated in Figure 3.16.

An interesting property of the nearest-neighbour \((K=1)\) classifier is that, in the limit \(N \rightarrow \infty\), the error rate is never more than twice the minimum achievable error rate of an optimal classifier, i.e., one that uses the true class distributions (Cover and Hart, 1967) .

As discussed so far, both the \(K\)-nearest-neighbour method and the kernel density estimator require the entire training data set to be stored, leading to expensive
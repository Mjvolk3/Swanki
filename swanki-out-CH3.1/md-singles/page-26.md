Figure 3.9 Illustration of the representation of values \(\theta_{n}\) of a periodic variable as twodimensional vectors \(\mathbf{x}_{n}\) living on the unit circle. Also shown is the average \(\bar{x}\) of those vectors.

![](https://cdn.mathpix.com/cropped/2024_05_13_b304b92298c168b494aag-1.jpg?height=623&width=648&top_left_y=216&top_left_x=995)

of the observations are given by \(\mathbf{x}_{n}=\left(\cos \theta_{n}, \sin \theta_{n}\right)\), and we can write the Cartesian coordinates of the sample mean in the form \(\overline{\mathbf{x}}=(\bar{r} \cos \bar{\theta}, \bar{r} \sin \bar{\theta})\). Substituting into (3.117) and equating the \(x_{1}\) and \(x_{2}\) components then gives

\[
\bar{x}_{1}=\bar{r} \cos \bar{\theta}=\frac{1}{N} \sum_{n=1}^{N} \cos \theta_{n}, \quad \bar{x}_{2}=\bar{r} \sin \bar{\theta}=\frac{1}{N} \sum_{n=1}^{N} \sin \theta_{n}
\]

Taking the ratio, and using the identity \(\tan \theta=\sin \theta / \cos \theta\), we can solve for \(\bar{\theta}\) to give

\[
\bar{\theta}=\tan ^{-1}\left\{\frac{\sum_{n} \sin \theta_{n}}{\sum_{n} \cos \theta_{n}}\right\}
\]

Shortly, we will see how this result arises naturally as a maximum likelihood estimator.

First, we need to define a periodic generalization of the Gaussian called the von Mises distribution. Here we will limit our attention to univariate distributions, although analogous periodic distributions can also be found over hyperspheres of arbitrary dimension (Mardia and Jupp, 2000).

By convention, we will consider distributions \(p(\theta)\) that have period \(2 \pi\). Any probability density \(p(\theta)\) defined over \(\theta\) must not only be non-negative and integrate to one, but it must also be periodic. Thus, \(p(\theta)\) must satisfy the three conditions:

\[
\begin{aligned}
p(\theta) & \geqslant 0 \\
\int_{0}^{2 \pi} p(\theta) \mathrm{d} \theta & =1 \\
p(\theta+2 \pi) & =p(\theta)
\end{aligned}
\]

From (3.122), it follows that \(p(\theta+M 2 \pi)=p(\theta)\) for any integer \(M\).

We can easily obtain a Gaussian-like distribution that satisfies these three properties as follows. Consider a Gaussian distribution over two variables \(\mathbf{x}=\left(x_{1}, x_{2}\right)\)
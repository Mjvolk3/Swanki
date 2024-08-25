Figure 3.10 The von Mises distribution can be derived by considering a two-dimensional Gaussian of the form (3.123), whose density contours are shown in blue, and conditioning on the unit circle shown in red.

![](https://cdn.mathpix.com/cropped/2024_05_13_a727111505627aa0270dg-1.jpg?height=386&width=422&top_left_y=217&top_left_x=1225)

having mean \(\boldsymbol{\mu}=\left(\mu_{1}, \mu_{2}\right)\) and a covariance matrix \(\boldsymbol{\Sigma}=\sigma^{2} \mathbf{I}\) where \(\mathbf{I}\) is the \(2 \times 2\) identity matrix, so that

\[
p\left(x_{1}, x_{2}\right)=\frac{1}{2 \pi \sigma^{2}} \exp \left\{-\frac{\left(x_{1}-\mu_{1}\right)^{2}+\left(x_{2}-\mu_{2}\right)^{2}}{2 \sigma^{2}}\right\}
\]

The contours of constant \(p(\mathbf{x})\) are circles, as illustrated in Figure 3.10.

Now suppose we consider the value of this distribution along a circle of fixed radius. Then by construction, this distribution will be periodic, although it will not be normalized. We can determine the form of this distribution by transforming from Cartesian coordinates \(\left(x_{1}, x_{2}\right)\) to polar coordinates \((r, \theta)\) so that

\[
x_{1}=r \cos \theta, \quad x_{2}=r \sin \theta .
\]

We also map the mean \(\boldsymbol{\mu}\) into polar coordinates by writing

\[
\mu_{1}=r_{0} \cos \theta_{0}, \quad \mu_{2}=r_{0} \sin \theta_{0}
\]

Next we substitute these transformations into the two-dimensional Gaussian distribution (3.123), and then condition on the unit circle \(r=1\), noting that we are interested only in the dependence on \(\theta\). Focusing on the exponent in the Gaussian distribution we have

\[
\begin{aligned}
& -\frac{1}{2 \sigma^{2}}\left\{\left(r \cos \theta-r_{0} \cos \theta_{0}\right)^{2}+\left(r \sin \theta-r_{0} \sin \theta_{0}\right)^{2}\right\} \\
& \quad=-\frac{1}{2 \sigma^{2}}\left\{1+r_{0}^{2}-2 r_{0} \cos \theta \cos \theta_{0}-2 r_{0} \sin \theta \sin \theta_{0}\right\} \\
& \quad=\frac{r_{0}}{\sigma^{2}} \cos \left(\theta-\theta_{0}\right)+\text { const }
\end{aligned}
\]

where 'const' denotes terms independent of \(\theta\). We have made use of the following trigonometrical identities:

\[
\begin{aligned}
\cos ^{2} A+\sin ^{2} A & =1 \\
\cos A \cos B+\sin A \sin B & =\cos (A-B)
\end{aligned}
\]

If we now define \(m=r_{0} / \sigma^{2}\), we obtain our final expression for the distribution of \(p(\theta)\) along the unit circle \(r=1\) in the form

\[
p\left(\theta \mid \theta_{0}, m\right)=\frac{1}{2 \pi I_{0}(m)} \exp \left\{m \cos \left(\theta-\theta_{0}\right)\right\}
\]
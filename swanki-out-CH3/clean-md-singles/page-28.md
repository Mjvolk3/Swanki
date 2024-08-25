
![](https://cdn.mathpix.com/cropped/2024_05_13_d2a86a8e5b0b3cfb4473g-1.jpg?height=586&width=1354&top_left_y=232&top_left_x=192)

Figure 3.11 The von Mises distribution plotted for two different parameter values, shown as a Cartesian plot on the left and as the corresponding polar plot on the right.

which is called the von Mises distribution or the circular normal. Here the parameter $\theta_{0}$ corresponds to the mean of the distribution, whereas $m$, which is known as the concentration parameter, is analogous to the inverse variance (i.e. the precision) for the Gaussian. The normalization coefficient in (3.129) is expressed in terms of $I_{0}(m)$, which is the zeroth-order modified Bessel function of the first kind (Abramowitz and Stegun, 1965) and is defined by

$$
I_{0}(m)=\frac{1}{2 \pi} \int_{0}^{2 \pi} \exp \{m \cos \theta\} \mathrm{d} \theta
$$

\title{
Exercise 3.31
}

For large $m$, the distribution becomes approximately Gaussian. The von Mises distribution is plotted in Figure 3.11, and the function $I_{0}(m)$ is plotted in Figure 3.12.

Now consider the maximum likelihood estimators for the parameters $\theta_{0}$ and $m$ for the von Mises distribution. The log likelihood function is given by

$$
\ln p\left(\mathcal{D} \mid \theta_{0}, m\right)=-N \ln (2 \pi)-N \ln I_{0}(m)+m \sum_{n=1}^{N} \cos \left(\theta_{n}-\theta_{0}\right)
$$

Setting the derivative with respect to $\theta_{0}$ equal to zero gives

$$
\sum_{n=1}^{N} \sin \left(\theta_{n}-\theta_{0}\right)=0
$$

To solve for $\theta_{0}$, we make use of the trigonometric identity

$$
\sin (A-B)=\cos B \sin A-\cos A \sin B
$$

Exercise $3.32 \quad$ from which we obtain
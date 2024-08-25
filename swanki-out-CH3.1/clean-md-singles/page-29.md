
![](https://cdn.mathpix.com/cropped/2024_05_13_895fbab03e81bab56181g-1.jpg?height=512&width=1492&top_left_y=232&top_left_x=128)

Figure 3.12 Plot of the Bessel function $I_{0}(m)$ defined by (3.130), together with the function $A(m)$ defined by $(3.136)$

$$
\theta_{0}^{\mathrm{ML}}=\tan ^{-1}\left\{\frac{\sum_{n} \sin \theta_{n}}{\sum_{n} \cos \theta_{n}}\right\}
$$

which we recognize as the result (3.119) obtained earlier for the mean of the observations viewed in a two-dimensional Cartesian space.

Similarly, maximizing (3.131) with respect to $m$ and making use of $I_{0}^{\prime}(m)=$ $I_{1}(m)$ (Abramowitz and Stegun, 1965), we have

$$
A\left(m_{\mathrm{ML}}\right)=\frac{1}{N} \sum_{n=1}^{N} \cos \left(\theta_{n}-\theta_{0}^{\mathrm{ML}}\right)
$$

where we have substituted for the maximum likelihood solution for $\theta_{0}^{\mathrm{ML}}$ (recalling that we are performing a joint optimization over $\theta$ and $m$ ), and we have defined

$$
A(m)=\frac{I_{1}(m)}{I_{0}(m)}
$$

The function $A(m)$ is plotted in Figure 3.12. Making use of the trigonometric identity (3.128), we can write (3.135) in the form

$$
A\left(m_{\mathrm{ML}}\right)=\left(\frac{1}{N} \sum_{n=1}^{N} \cos \theta_{n}\right) \cos \theta_{0}^{\mathrm{ML}}+\left(\frac{1}{N} \sum_{n=1}^{N} \sin \theta_{n}\right) \sin \theta_{0}^{\mathrm{ML}}
$$

The right-hand side of (3.137) is easily evaluated, and the function $A(m)$ can be inverted numerically. One limitation of the von Mises distribution is that it is unimodal. By forming mixtures of von Mises distributions, we obtain a flexible framework for modelling periodic variables that can handle multimodality.

For completeness, we mention briefly some alternative techniques for constructing periodic distributions. The simplest approach is to use a histogram of observations in which the angular coordinate is divided into fixed bins. This has the virtue of
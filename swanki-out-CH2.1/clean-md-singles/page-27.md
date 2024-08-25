
![](https://cdn.mathpix.com/cropped/2024_05_10_86a2845941e286ae4e26g-1.jpg?height=648&width=1510&top_left_y=272&top_left_x=134)

Figure 2.14 Histograms of two probability distributions over 30 bins illustrating the higher value of the entropy $\mathrm{H}$ for the broader distribution. The largest entropy would arise from a uniform distribution which would give $\mathrm{H}=-\ln (1 / 30)=3.40$.

Exercise 2.22 Exercise 2.23 from which we find that all of the $p\left(x_{i}\right)$ are equal and are given by $p\left(x_{i}\right)=1 / M$ where $M$ is the total number of states $x_{i}$. The corresponding value of the entropy is then $\mathrm{H}=\ln M$. This result can also be derived from Jensen's inequality (to be discussed shortly). To verify that the stationary point is indeed a maximum, we can evaluate the second derivative of the entropy, which gives

$$
\frac{\partial \widetilde{\mathrm{H}}}{\partial p\left(x_{i}\right) \partial p\left(x_{j}\right)}=-I_{i j} \frac{1}{p_{i}}
$$

where $I_{i j}$ are the elements of the identity matrix. We see that these values are all negative and, hence, the stationary point is indeed a maximum.

\subsection*{2.5.3 Differential entropy}

We can extend the definition of entropy to include distributions $p(x)$ over continuous variables $x$ as follows. First divide $x$ into bins of width $\Delta$. Then, assuming that $p(x)$ is continuous, the mean value theorem (Weisstein, 1999) tells us that, for each such bin, there must exist a value $x_{i}$ in the range $i \Delta \leqslant x_{i} \leqslant(i+1) \Delta$ such that

$$
\int_{i \Delta}^{(i+1) \Delta} p(x) \mathrm{d} x=p\left(x_{i}\right) \Delta
$$

We can now quantize the continuous variable $x$ by assigning any value $x$ to the value $x_{i}$ whenever $x$ falls in the $i$ th bin. The probability of observing the value $x_{i}$ is then
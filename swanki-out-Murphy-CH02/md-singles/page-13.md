![](https://cdn.mathpix.com/cropped/2024_06_13_bc2b90831f76956b6fc5g-1.jpg?height=523&width=1533&top_left_y=193&top_left_x=264)

Figure 2.7: Illustration of 7 different datasets (left), the corresponding box plots (middle) and violin box plots (right). From Figure 8 of https://www. autodesk. com/research/publications/ same-stats-different-graphs. Used with kind permission of Justin Matejka.

that represent "degrees of certainty" using probability theory, and which leverage Bayes' rule \({ }^{7}\), to update the degree of certainty given data.

Bayes' rule itself is very simple: it is just a formula for computing the probability distribution over possible values of an unknown (or hidden) quantity \(H\) given some observed data \(Y=y\) :

\[
p(H=h \mid Y=y)=\frac{p(H=h) p(Y=y \mid H=h)}{p(Y=y)}
\]

This follows automatically from the identity

\[
p(h \mid y) p(y)=p(h) p(y \mid h)=p(h, y)
\]

which itself follows from the product rule of probability.

In Equation (2.51), the term \(p(H)\) represents what we know about possible values of \(H\) before we see any data; this is called the prior distribution. (If \(H\) has \(K\) possible values, then \(p(H)\) is a vector of \(K\) probabilities, that sum to 1.) The term \(p(Y \mid H=h)\) represents the distribution over the possible outcomes \(Y\) we expect to see if \(H=h\); this is called the observation distribution. When we evaluate this at a point corresponding to the actual observations, \(y\), we get the function \(p(Y=y \mid H=h)\), which is called the likelihood. (Note that this is a function of \(h\), since \(y\) is fixed, but it is not a probability distribution, since it does not sum to one.) Multiplying the prior distribution \(p(H=h)\) by the likelihood function \(p(Y=y \mid H=h)\) for each \(h\) gives the unnormalized joint distribution \(p(H=h, Y=y)\). We can convert this into a normalized distribution by dividing by \(p(Y=y)\), which is known as the marginal likelihood, since it is computed by marginalizing over the unknown \(H\) :

\[
p(Y=y)=\sum_{h^{\prime} \in \mathcal{H}} p\left(H=h^{\prime}\right) p\left(Y=y \mid H=h^{\prime}\right)=\sum_{h^{\prime} \in \mathcal{H}} p\left(H=h^{\prime}, Y=y\right)
\]
7. Thomas Bayes (1702-1761) was an English mathematician and Presbyterian minister. For a discussion of whether
to spell this as Bayes rule, Bayes' rule or Bayes's rule, see https://bit. 1y/2kDtLuK.

Author: Kevin P. Murphy. (C) MIT Press. CC-BY-NC-ND license
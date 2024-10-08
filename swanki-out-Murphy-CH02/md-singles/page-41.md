![](https://cdn.mathpix.com/cropped/2024_06_13_e1c4fa23ad624dcfc447g-1.jpg?height=472&width=1202&top_left_y=223&top_left_x=409)

Figure 2.24: Computing the distribution of \(y=x^{2}\), where \(p(x)\) is uniform (left). The analytic result is shown in the middle, and the Monte Carlo approximation is shown on the right. Generated by change_of_vars_demo1d.ipynb.

first developed in the area of statistical physics - in particular, during development of the atomic bomb - but are now widely used in statistics and machine learning as well. More details can be found in the sequel to this book, [Mur23], as well as specialized books on the topic, such as [Liu01; RC04; KTB11; BZ20].

\title{
2.9 Exercises
}

Exercise 2.1 [Conditional independence \(*]\)

(Source: Koller.)

a. Let \(H \in\{1, \ldots, K\}\) be a discrete random variable, and let \(e_{1}\) and \(e_{2}\) be the observed values of two other random variables \(E_{1}\) and \(E_{2}\). Suppose we wish to calculate the vector

\[
\vec{P}\left(H \mid e_{1}, e_{2}\right)=\left(P\left(H=1 \mid e_{1}, e_{2}\right), \ldots, P\left(H=K \mid e_{1}, e_{2}\right)\right)
\]

Which of the following sets of numbers are sufficient for the calculation?

\[
\begin{aligned}
& \text { i. } P\left(e_{1}, e_{2}\right), P(H), P\left(e_{1} \mid H\right), P\left(e_{2} \mid H\right) \\
& \text { ii. } P\left(e_{1}, e_{2}\right), P(H), P\left(e_{1}, e_{2} \mid H\right) \\
& \text { ii. } P\left(e_{1} \mid H\right), P\left(e_{2} \mid H\right), P(H)
\end{aligned}
\]

b. Now suppose we now assume \(E_{1} \perp E_{2} \mid H\) (i.e., \(E_{1}\) and \(E_{2}\) are conditionally independent given \(H\) ). Which of the above 3 sets are sufficient now?

Show your calculations as well as giving the final result. Hint: use Bayes rule.

Exercise 2.2 [Pairwise independence does not imply mutual independence]

We say that two random variables are pairwise independent if

\[
p\left(X_{2} \mid X_{1}\right)=p\left(X_{2}\right)
\]

and hence

\[
p\left(X_{2}, X_{1}\right)=p\left(X_{1}\right) p\left(X_{2} \mid X_{1}\right)=p\left(X_{1}\right) p\left(X_{2}\right)
\]

Author: Kevin P. Murphy. (C) MIT Press. CC-BY-NC-ND license
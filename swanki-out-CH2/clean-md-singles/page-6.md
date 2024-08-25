showing that the conditional probabilities are correctly normalized. From (2.1), (2.2), and (2.5), we can then derive the following relationship:

$$
\begin{aligned}
p\left(X=x_{i}, Y=y_{j}\right) & =\frac{n_{i j}}{N}=\frac{n_{i j}}{c_{i}} \cdot \frac{c_{i}}{N} \\
& =p\left(Y=y_{j} \mid X=x_{i}\right) p\left(X=x_{i}\right)
\end{aligned}
$$

which is the product rule of probability.

So far, we have been quite careful to make a distinction between a random variable, such as $X$, and the values that the random variable can take, for example $x_{i}$. Thus, the probability that $X$ takes the value $x_{i}$ is denoted $p\left(X=x_{i}\right)$. Although this helps to avoid ambiguity, it leads to a rather cumbersome notation, and in many cases there will be no need for such pedantry. Instead, we may simply write $p(X)$ to denote a distribution over the random variable $X$, or $p\left(x_{i}\right)$ to denote the distribution evaluated for the particular value $x_{i}$, provided that the interpretation is clear from the context.

With this more compact notation, we can write the two fundamental rules of probability theory in the following form:

$$
\begin{array}{cc}
\text { sum rule } & p(X)=\sum_{Y} p(X, Y) \\
\text { product rule } & p(X, Y)=p(Y \mid X) p(X)
\end{array}
$$

Here $p(X, Y)$ is a joint probability and is verbalized as 'the probability of $X$ and $Y^{\prime}$. Similarly, the quantity $p(Y \mid X)$ is a conditional probability and is verbalized as 'the probability of $Y$ given $X$ '. Finally, the quantity $p(X)$ is a marginal probability and is simply 'the probability of $X$ '. These two simple rules form the basis for all of the probabilistic machinery that we will use throughout this book.

\title{
2.1.3 Bayes' theorem
}

From the product rule, together with the symmetry property $p(X, Y)=p(Y, X)$, we immediately obtain the following relationship between conditional probabilities:

$$
p(Y \mid X)=\frac{p(X \mid Y) p(Y)}{p(X)}
$$

which is called Bayes' theorem and which plays an important role in machine learning. Note how Bayes' theorem relates the conditional distribution $p(Y \mid X)$ on the left-hand side of the equation, to the 'reversed' conditional distribution $p(X \mid Y)$ on the right-hand side. Using the sum rule, the denominator in Bayes' theorem can be expressed in terms of the quantities appearing in the numerator:

$$
p(X)=\sum_{Y} p(X \mid Y) p(Y)
$$

Thus, we can view the denominator in Bayes' theorem as being the normalization constant required to ensure that the sum over the conditional probability distribution on the left-hand side of (2.10) over all values of $Y$ equals one.
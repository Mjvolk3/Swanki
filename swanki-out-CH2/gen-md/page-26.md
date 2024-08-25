## How is the multiplicity $W$ defined in the context of allocating $N$ objects between bins?

Multiplicity $W$ is defined formally as

$$
W = \frac{N!}{\prod_i n_i!}
$$

where $N!$ represents the factorial of $N$, the total number of ways to order $N$ distinct objects, and $n_i!$ is the factorial of $n_i$, the number of objects in the $i$-th bin. Dividing by the product of the factorials of each bin's size corrects for the overcounting of indistinguishable arrangements within each bin.

- #combinatorics.factorial, #probability.multiplicity

## Define the entropy $H$ of allocating $N$ objects into bins and show its expression.

Entropy $H$ for the distribution of $N$ objects into bins is given by:

$$
H = \frac{1}{N} \ln W = \frac{1}{N} \ln N! - \frac{1}{N} \sum_i \ln n_i!
$$

Here, $\ln W$ represents the natural logarithm of the multiplicity, and the division by $N$ normalizes the entropy by the number of objects. Thus, entropy quantifies the uncertainty or randomness in the distribution of objects across bins, considering all possible microstates.

- #probability.entropy, #mathematics-logarithm

## Apply Stirling's approximation to find an expression for $H$ as $N \to \infty$.

Stirling’s approximation states that $\ln N! \approx N \ln N - N$. Using this, the entropy $H$ can be approximated as 

$$
H \approx -\lim_{N \to \infty} \sum_i \left(\frac{n_i}{N}\right) \ln \left(\frac{n_i}{N}\right) = -\sum_i p_i \ln p_i
$$

where $p_i = \lim_{N \to \infty} \left(\frac{n_i}{N}\right)$. This expression uses the definition that $p_i$ is the fraction of total objects in the $i$-th bin and simplifies to the expression of entropy for a discrete probability distribution, reflecting the average information content per choice from the distribution.

- #math.stirling-approximation, #probability.entropy-limit

## Discuss how entropy varies with the distribution of probability $p(x_i)$ for a random variable $X$.

Entropy $H[p]$ of a discrete random variable $X$ is defined as 

$$
H[p] = -\sum_i p(x_i) \ln p(x_i)
$$

Here, $p(x_i) = p_i$ represents the probability that $X$ takes on the value $x_i$. Entropy measures the expected uncertainty in $X$; distributions that are more uniformly distributed across several states (values of $X$) will have higher entropy. Conversely, probabilities that are highly peaked around one or a few states will result in lower entropy, indicating less uncertainty or randomness in the outcomes of $X$.

- #information-theory.entropy-distribution, #probability.random-variable

## How is maximum entropy of a discrete random variable $X$ determined under a normalization constraint?

The maximum entropy configuration is found by maximizing the Lagrange function:

$$
\widetilde{H} = -\sum_i p(x_i) \ln p(x_i) + \lambda \left(\sum_i p(x_i) - 1\right)
$$

This function includes a Lagrange multiplier $\lambda$ to enforce the probability normalization constraint, $\sum_i p(x_i) = 1$. By maximizing this function, we can determine the distribution $p(x_i)$ that leads to the highest entropy, subject to the probabilities summing to one. This method is particularly useful in deriving distributions under specified constraints, revealing the most likely macrostate configurations.

- #optimization.lagrange-multiplier, #probability.probability-constraint-maximization
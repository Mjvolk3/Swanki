```plaintext
## Define the Bernoulli distribution probability mass function (pmf) and express it concisely.

The Bernoulli distribution is a discrete probability distribution for a random variable which takes the value 1 with probability $\theta$ and the value 0 with probability $1-\theta$. The pmf is given by

$$
\operatorname{Ber}(y \mid \theta)= \begin{cases}1-\theta & \text { if } y=0 \\ \theta & \text { if } y=1\end{cases}
$$

It can be written concisely as:

$$
\operatorname{Ber}(y \mid \theta) \triangleq \theta^{y}(1-\theta)^{1-y}
$$

- #probability-theory.bernoulli-distribution, #math.pmf
```

```plaintext
## How is the binomial distribution related to the Bernoulli distribution?

The Bernoulli distribution is a special case of the binomial distribution. Specifically, if we observe $N$ Bernoulli trials, the total number of successes $s$ in those trials follows a binomial distribution:

$$
\operatorname{Bin}(s \mid N, \theta) \triangleq\binom{N}{s} \theta^{s}(1-\theta)^{N-s}
$$

Where $\binom{N}{s}$ is the binomial coefficient, defined as:

$$
\binom{N}{k} \triangleq \frac{N!}{(N-k)!k!}
$$

If $N=1$, the binomial distribution reduces to the Bernoulli distribution.

- #probability-theory.binomial-distribution, #probability-theory.bernoulli-distribution
```

```plaintext
## What is the significance of $s$ in the context of binomial distribution?

In the context of the binomial distribution, $s$ represents the total number of successes (e.g., heads in coin tosses) in $N$ Bernoulli trials. It is defined as:

$$
s \triangleq \sum_{n=1}^{N} \mathbb{I}\left(y_{n}=1\right)
$$

where $\mathbb{I}\left( y_{n} = 1 \right)$ is an indicator function that equals 1 if $y_n = 1$, and 0 otherwise.

- #probability-theory.binomial-distribution, #statistics.successes
```

```plaintext
## Describe how the probability mass function of the binomial distribution is formulated.

The pmf of the binomial distribution, which gives the probability of observing exactly $s$ successes in $N$ Bernoulli trials, is given by:

$$
\operatorname{Bin}(s \mid N, \theta) = \binom{N}{s} \theta^{s}(1-\theta)^{N-s}
$$

where $\binom{N}{s} = \frac{N!}{(N-s)!s!}$ is the binomial coefficient, $\theta$ is the success probability in a single trial, and $N$ is the number of trials.

- #probability-theory.binomial-distribution, #math.pmf
```

```plaintext
## How can the binomial distribution be visualized for various parameters?

The binomial distribution can be visualized for different values of $N$ and $\theta$ using histograms or probability mass function plots. For instance, the distribution of $s$ with $N=10$ and $\theta=0.25$ or $\theta=0.9$ shows how the likelihood of each number of successes ($s$) varies as a function of $\theta$.

(Refer to Figure 2.9: Illustration of the binomial distribution with $N=10$ and $\theta=0.25$ or $\theta=0.9$.)

- #probability-theory.binomial-distribution, #data-visualization
```

```plaintext
## Explain the significance of the binomial coefficient $\binom{N}{k}$ in the binomial distribution.

The binomial coefficient $\binom{N}{k}$ represents the number of distinct ways to choose $k$ successes out of $N$ trials. It is given by:

$$
\binom{N}{k} = \frac{N!}{(N-k)!k!}
$$

It plays a critical role in the pmf of the binomial distribution:

$$
\operatorname{Bin}(s \mid N, \theta) = \binom{N}{s} \theta^{s}(1-\theta)^{N-s}
$$

where $N!$ is the factorial of $N$, representing the total number of permutations.

- #probability-theory.binomial-distribution, #math.binomial-coefficient
```
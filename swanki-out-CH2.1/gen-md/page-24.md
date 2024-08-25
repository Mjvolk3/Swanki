## What is the measure of information content $h(x)$ for a discrete random variable $x$?
The measure of information content for a discrete random variable $x$, denoted as $h(x)$, is given by $$h(x) = -\log_2 p(x)$$ where $p(x)$ is the probability of observing the specific value of $x$. This formula reflects the amount of surprise or unexpectedness when observing the value of $x$.

- #information-theory.measure-of-information, #mathematics.logarithms

## How does the entropy $H[x]$ of a random variable $x$ encapsulate the average amount of information transmitted?
Entropy, $H[x]$, represents the average amount of information transmitted when a sender communicates the value of a random variable $x$ to a receiver. It is mathematically defined as: $$H[x] = -\sum_x p(x) \log_2 p(x)$$ Here, $p(x)$ is the probability distribution of $x$. This formula averages the information content over all possible values of the random variable, weighted by their probabilities.

- #information-theory.entropy, #mathematics.expectation

## Explain the relationship of the negative sign in the formula $h(x) = -\log_2 p(x)$
The negative sign in the formula $$h(x) = -\log_2 p(x)$$ is crucial as it ensures that the information content is always non-negative. This sign inversion is necessary because $\log_2 p(x)$ yields negative values for probabilities less than 1, which are typical in realistic scenarios. The negative sign thus transforms these values into positive measures of information content.

- #information-theory.information-content, #mathematics.logarithms

## Why are bits used as units in information theory?
Bits, short for 'binary digits', are used as units in information theory when logarithms are computed using base 2. For instance, in the formula $$h(x) = -\log_2 p(x)$$ using base 2 results in an interpretation of the information content in terms of bits. This binary measurement aligns with the digital nature of most modern communication and storage systems, making bits a practical unit of measure for information.

- #information-theory.bits, #technology.data-communication

## Clarify the implication of $\lim_{\epsilon \to 0}(\epsilon \ln \epsilon) = 0$ for entropies involving probabilities of zero.
In entropy calculations such as $$H[x] = -\sum_x p(x) \log_2 p(x)$$ there arises a need to handle terms where $p(x) = 0$. The limit $$\lim_{\epsilon \to 0}(\epsilon \ln \epsilon) = 0$$ is applied to justify that the contribution to entropy from such terms is zero. This avoids undefined or infinite values in the entropy expression, ensuring that the entropy is computable even when probabilities of some events are zero.

- #information-theory.limit-interpretation, #mathematics.limits
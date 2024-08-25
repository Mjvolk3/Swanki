## What are the prior probabilities of having cancer, $C=1$, and not having cancer, $C=0$, in the population according to the given example?

Prior probabilities are given by:

$$
p(C=1) = \frac{1}{100}, \quad p(C=0) = \frac{99}{100}
$$

These probabilities reflect the assumed prevalence of cancer in the population, where $C=1$ indicates the presence of cancer and $C=0$ the absence.

- #probability, #statistics, #medical-screening

## Define the conditional probabilities associated with test results given the cancer status, $T=1$ and $T=0$, based on the medical screening example.

The conditional probabilities for positive ($T=1$) and negative ($T=0$) test results, given the cancer status, are defined as:

$$
\begin{aligned}
p(T=1 \mid C=1) & = \frac{90}{100} \\
p(T=0 \mid C=1) & = \frac{10}{100} \\
p(T=1 \mid C=0) & = \frac{3}{100} \\
p(T=0 \mid C=0) & = \frac{97}{100}
\end{aligned}
$$

These probabilities determine how likely it is to receive a specific test result, depending on whether or not the individual actually has cancer. 

- #probability, #conditional-probability, #medical-screening

## How is the overall probability $p(T=1)$ of a positive test result calculated using the sum and product rules of probability?

The overall probability of a positive test result, $p(T=1)$, is calculated as:

$$
p(T=1) = p(T=1 \mid C=0) p(C=0) + p(T=1 \mid C=1) p(C=1) \\
= \frac{3}{100} \times \frac{99}{100} + \frac{90}{100} \times \frac{1}{100} = \frac{387}{10,000} = 0.0387
$$

This calculation illustrates how the sum and product rules of probability are applied to integrate the joint influences of cancer prevalence and test accuracy on the probability of obtaining a positive test result.

- #probability, #probability-rules, #medical-screening

## Calculate and explain the probability of a negative test result, $p(T=0)$, in the medical screening context.

The probability of a negative test result, $p(T=0)$, can be computed using the sum rule of probability, which states that the sum of probabilities of all complementary events must equal one:

$$
p(T=0) = 1 - p(T=1) = 1 - \frac{387}{10,000} = \frac{9613}{10,000} = 0.9613
$$

This value indicates that there is approximately a 96% chance that an individual tested will receive a negative test result, highlighting the test's likelihood of indicating no cancer when used at random within the general population.

- #probability, #sum-rule, #medical-screening

## What is the importance of normalizing the conditional probabilities of test results in the given medical screening example?

Normalization of conditional probabilities, such as:

$$
p(T=1 \mid C=1) + p(T=0 \mid C=1) = 1
$$
and
$$
p(T=1 \mid C=0) + p(T=0 \mid C=0) = 1
$$

ensures that the total probabilities for all possible outcomes of the test, given each state of cancer presence or absence, sum to one. This is crucial for maintaining the probabilistic model's consistency and accuracy in predictions, ensuring that no logical fallacies occur within the framework of probability theory.

- #probability, #normalization, #medical-screening
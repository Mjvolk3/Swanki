## What is the formula to calculate the probability of being infected given a positive test result, $p(H=1 \mid Y=1)$?

The formula for the probability of being infected given a positive test result is:

$$
p(H=1 \mid Y=1) = \frac{\mathrm{TPR} \times \text{prior}}{\mathrm{TPR} \times \text{prior} + \mathrm{FPR} \times (1 - \text{prior})}
$$

Where:
- $\mathrm{TPR}$ is the true positive rate
- $\mathrm{FPR}$ is the false positive rate
- $\text{prior}$ is the prior probability of being infected.

- #probability, #bayes-rule

## Calculate the probability of being infected given a positive test result using TPR = 0.875, FPR = 0.025, and prior = 0.1.

$$
\begin{aligned}
p(H=1 \mid Y=1) & = \frac{\mathrm{TPR} \times \text{prior}}{\mathrm{TPR} \times \text{prior} + \mathrm{FPR} \times (1 - \text{prior})} \\
& = \frac{0.875 \times 0.1}{0.875 \times 0.1 + 0.025 \times 0.9} \\
& = 0.795
\end{aligned}
$$

So, a $79.5\%$ chance you are infected.

- #probability, #bayes-rule

## What is the formula to calculate the probability of being infected given a negative test result, $p(H=1 \mid Y=0)$?

The formula for the probability of being infected given a negative test result is:

$$
p(H=1 \mid Y=0) = \frac{\text{FNR} \times \text{prior}}{\text{FNR} \times \text{prior} + \text{TNR} \times (1 - \text{prior})}
$$

Where:
- $\text{FNR}$ is the false negative rate
- $\text{TNR}$ is the true negative rate
- $\text{prior}$ is the prior probability of being infected.

- #probability, #bayes-rule

## Calculate the probability of being infected given a negative test result using FNR = 0.125, TNR = 0.975, and prior = 0.1.

$$
\begin{aligned}
p(H=1 \mid Y=0) & = \frac{\text{FNR} \times \text{prior}}{\text{FNR} \times \text{prior} + \text{TNR} \times (1 - \text{prior})} \\
& = \frac{0.125 \times 0.1}{0.125 \times 0.1 + 0.975 \times 0.9} \\
& = 0.014
\end{aligned}
$$

So, a $1.4\%$ chance you are infected.

- #probability, #bayes-rule

## What happens to the posterior probabilities if the base rate drops to $1\%$ for both positive and negative tests?

If the base rate (\text{prior}) is $1\%$:
- For a positive test: 

$$
p(H=1 \mid Y=1) = \frac{0.875 \times 0.01}{0.875 \times 0.01 + 0.025 \times 0.99} = 0.26
$$

So, a %%26 chance you are infected.

- For a negative test:

$$
p(H=1 \mid Y=0) = \frac{0.125 \times 0.01}{0.125 \times 0.01 + 0.975 \times 0.99} = 0.0013
$$

So, a 0.13% chance you are infected.

- #probability, #base-rate

## What does the Monty Hall problem illustrate with respect to Bayes rule?

In the Monty Hall problem, Bayes rule is used to update the probability of winning by switching doors. Initially, the probability is uniformly distributed among the three doors:

$$
P(\text{prize behind door 1}) = P(\text{prize behind door 2}) = P(\text{prize behind door 3}) = \frac{1}{3}
$$

After the host reveals a door without a prize, Bayes rule updates these probabilities, showing that switching doors improves the probability of winning to $\frac{2}{3}$ as opposed to sticking with the initial choice which has a $\frac{1}{3}$ probability.

- #probability, #bayes-rule, #monty-hall

## Should you switch doors in the Monty Hall problem and why?

You should switch doors in the Monty Hall problem because the probability of winning increases to $\frac{2}{3}$ by switching, compared to a $\frac{1}{3}$ chance by sticking with the initial choice. This uses Bayes rule to update the probabilities after the host opens a door.

- #probability, #bayes-rule, #monty-hall

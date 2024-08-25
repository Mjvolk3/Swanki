## Verify the normalization of the Bernoulli distribution
Show that the sum of probabilities for all outcomes of a Bernoulli-distributed random variable equals 1. Given the Bernoulli distribution:

$$
p(x \mid \mu) = \mu^x (1-\mu)^{1-x}
$$
for $x \in \{0,1\}$, confirm that:

$$
\sum_{x=0}^{1} p(x \mid \mu) = 1
$$

% Here is the expected step-by-step confirmation:

$$
\sum_{x=0}^{1} p(x \mid \mu) = p(0 | \mu) + p(1 | \mu) = (1-\mu) + \mu = 1
$$

This shows that the total probability mass is 1, confirming the distribution is normalized.

- #probability, #distributions.bernoulli, #normalization

## Calculate the mean of a Bernoulli distribution
Determine the expected value $\mathbb{E}[x]$ for a Bernoulli-distributed variable $x$, given:

$$
p(x \mid \mu) = \mu^x (1-\mu)^{1-x}
$$
for $x \in \{0,1\}$, utilizing:

$$
\mathbb{E}[x] = \sum_{x=0}^{1} x \cdot p(x \mid \mu)
$$

% Here is the detailed calculation:

$$
\mathbb{E}[x] = 0 \cdot p(0 \mid \mu) + 1 \cdot p(1 \mid \mu) = 0 \cdot (1-\mu) + 1 \cdot \mu = \mu
$$

This assumes that $x$ takes values 0 or 1, weighted by the respective probabilities dictated by the Bernoulli distribution.

- #probability, #distributions.bernoulli, #expected-value

## Compute the variance of a Bernoulli distribution
Derive the variance $\operatorname{var}[x]$ for a Bernoulli distribution, where:

$$
p(x \mid \mu) = \mu^x (1-\mu)^{1-x}
$$
for $x \in \{0,1\}$, by calculating:

$$
\operatorname{var}[x] = \mathbb{E}[x^2] - (\mathbb{E}[x])^2
$$

% Here is the complete derivation:

$$
\operatorname{var}[x] = \mathbb{E}[x^2] - (\mathbb{E}[x])^2 = \mu - \mu^2 = \mu(1-\mu)
$$

Note that for a Bernoulli random variable, $\mathbb{E}[x^2] = \mathbb{E}[x]$ as $x^2 = x$ for $x \in \{0,1\}$.

- #probability, #distributions.bernoulli, #variance

## Calculate entropy of a Bernoulli distribution
Prove that the entropy $\mathrm{H}[x]$ of a Bernoulli-distributed variable $x$ is given by:

$$
\mathrm{H}[x] = -\mu \ln \mu - (1-\mu) \ln (1-\mu)
$$

% Here is the derivation process:

The entropy $\mathrm{H}[x]$ of a random variable $x$ with probabilities $p(x)$ is:

$$
\mathrm{H}[x] = -\sum_{x} p(x) \ln p(x)
$$

For a Bernoulli distribution:

$$
\mathrm{H}[x] = -\left( \mu \ln \mu + (1-\mu) \ln (1-\mu) \right)
$$

This entropy formula quantifies the uncertainty in the Bernoulli distribution.

- #probability, #distributions.bernoulli, #entropy

## Show that an alternative Bernoulli distribution is normalized
For the alternative Bernoulli formulation with $x \in \{-1,1\}$, prove that the distribution:

$$
p(x \mid \mu) = \left(\frac{1-\mu}{2}\right)^{(1-x)/2} \left(\frac{1+\mu}{2}\right)^{(1+x)/2}
$$

is normalized, i.e.,

$$
\sum_{x \in \{-1,1\}} p(x \mid \mu) = 1
$$

% To prove the normalization, calculate:

$$
\sum_{x \in \{-1,1\}} p(x \mid \mu) = p(-1 \mid \mu) + p(1 \mid \mu) = \frac{1-\mu}{2} + \frac{1+\mu}{2} = 1
$$

This confirms that the total probability for this distribution sums to 1, demonstrating normalization.

- #probability, #distributions.bernoulli, #normalization-alternative 
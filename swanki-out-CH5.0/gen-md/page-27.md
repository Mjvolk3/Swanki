Sure, here are six Anki cards based on the provided text, focusing on scientific details and mathematical equations.

---

## Explain the form of the class-conditional density function $p\left(\mathbf{x} \mid \boldsymbol{\lambda}_{k}, s\right)$ given in the context of the exponential family of distributions.

The class-conditional density function is given by:

$$
p\left(\mathbf{x} \mid \boldsymbol{\lambda}_{k}, s\right) = \frac{1}{s} h\left(\frac{1}{s} \mathbf{x}\right) g\left(\boldsymbol{\lambda}_{k}\right) \exp \left\{\frac{1}{s} \boldsymbol{\lambda}_{k}^{\mathrm{T}} \mathbf{x}\right\}
$$

where:
- $s$ is a scaling parameter shared across all classes.
- $h\left(\frac{1}{s} \mathbf{x}\right)$ is a function that modulates the input $\mathbf{x}$ scaled by $\frac{1}{s}$.
- $g\left(\boldsymbol{\lambda}_{k}\right)$ is a function of the parameter vector $\boldsymbol{\lambda}_{k}$.
- $\exp \left\{\frac{1}{s} \boldsymbol{\lambda}_{k}^{\mathrm{T}} \mathbf{x}\right\}$ is an exponential term involving the dot product of $\boldsymbol{\lambda}_{k}$ and $\mathbf{x}$ scaled by $\frac{1}{s}$.

- #math.probability, #statistics.exponential-family, #generative-models

---

## For a two-class classification problem, derive the linear function $a(\mathbf{x})$ used in the logistic sigmoid transformation.

The linear function $a(\mathbf{x})$ is given by:

$$
a(\mathbf{x}) = \left(\boldsymbol{\lambda}_{1} - \boldsymbol{\lambda}_{2}\right)^{\mathrm{T}} \mathbf{x} + \ln g\left(\boldsymbol{\lambda}_{1}\right) - \ln g\left(\boldsymbol{\lambda}_{2}\right) + \ln p\left(\mathcal{C}_{1}\right) - \ln p\left(\mathcal{C}_{2}\right)
$$

where:
- $\boldsymbol{\lambda}_{1}$ and $\boldsymbol{\lambda}_{2}$ are the parameters for classes $\mathcal{C}_{1}$ and $\mathcal{C}_{2}$, respectively.
- $g(\cdot)$ is a function related to the class-conditional densities.
- $p(\mathcal{C}_{i})$ are the class priors for each class $\mathcal{C}_{i}$.

- #math.linear-algebra, #statistics.logistic-regression, #machine-learning

---

## How does the form of the posterior probability for the multi-class problem differ from the two-class case?

For the $K$-class problem, the posterior probability is given by a softmax transformation of linear functions of $\mathbf{x}$, as opposed to a logistic sigmoid in the two-class case.

The linear function $a_{k}(\mathbf{x})$ for the $K$-class problem is:

$$
a_{k}(\mathbf{x}) = \boldsymbol{\lambda}_{k}^{\mathrm{T}} \mathbf{x} + \ln g\left(\boldsymbol{\lambda}_{k}\right) + \ln p\left(\mathcal{C}_{k}\right)
$$

where:
- $\boldsymbol{\lambda}_{k}$ are the parameters for each class $\mathcal{C}_{k}$,
- $g(\cdot)$ is a function related to the class-conditional densities,
- $p(\mathcal{C}_{k})$ are the class priors for each class $\mathcal{C}_{k}$.

- #math.softmax, #statistics.multi-class, #machine-learning

---

## Define discriminative probabilistic modelling and compare it with generative modelling.

Discriminative probabilistic modelling focuses on directly modeling the conditional distribution $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$. It involves determining model parameters by maximizing the likelihood of this conditional distribution.

In contrast, generative modelling involves modeling the joint distribution $p\left(\mathbf{x}, \mathcal{C}_{k}\right)$ or the class-conditional densities $p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)$ and using Bayes' theorem to compute the posterior probabilities.

**Advantages of the discriminative approach:**
1. Fewer learnable parameters.
2. Potential for improved predictive performance, especially when the assumed class-conditional densities are not accurate representations of the true distributions.

- #machine-learning, #statistics.generative-discriminative, #probability

---

## Explain the role of the scaling parameter $s$ in the class-conditional density function.

In the exponential family representation of the class-conditional density:

$$
p\left(\mathbf{x} \mid \boldsymbol{\lambda}_{k}, s\right) = \frac{1}{s} h\left(\frac{1}{s} \mathbf{x}\right) g\left(\boldsymbol{\lambda}_{k}\right) \exp \left\{\frac{1}{s} \boldsymbol{\lambda}_{k}^{\mathrm{T}} \mathbf{x}\right\}
$$

the scaling parameter $s$:
- Is shared across all classes.
- Scales the input $\mathbf{x}$.
- Factors into the normalization term $\frac{1}{s}$ and the function $h\left(\frac{1}{s} \mathbf{x}\right)$.
- Scales the exponential term $\exp \left\{\frac{1}{s} \boldsymbol{\lambda}_{k}^{\mathrm{T}} \mathbf{x}\right\}$, controlling the influence of $\mathbf{x}$ and $\boldsymbol{\lambda}_{k}$ on the density.

- #math.scaling, #statistics.exponential-family, #generative-models

---

## What is the significance of using a logistic sigmoid or a softmax function in discriminative classifiers?

The logistic sigmoid and softmax functions are used to model posterior class probabilities:

- In a two-class problem, the posterior class probability is modeled as a logistic sigmoid function of a linear combination of $\mathbf{x}$: 

$$
\sigma(a(\mathbf{x})) = \frac{1}{1 + \exp(-a(\mathbf{x}))}
$$

where $a(\mathbf{x})$ is a linear function of $\mathbf{x}$.

- In a $K$-class problem, the posterior class probabilities are modeled as a softmax function of linear combinations of $\mathbf{x}$:

$$
p(\mathcal{C}_k \mid \mathbf{x}) = \frac{\exp(a_k(\mathbf{x}))}{\sum_{j=1}^{K} \exp(a_j(\mathbf{x}))}
$$

where $a_k(\mathbf{x})$ are linear functions of $\mathbf{x}$.

These functions ensure that the output probabilities range between 0 and 1 and sum to 1, making them appropriate for classification tasks.

- #math.probability-distributions, #statistics.sigmoid-softmax, #machine-learning
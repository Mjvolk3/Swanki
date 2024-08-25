### Flashcard 1

## Why is it problematic to train an adaptive model on a highly imbalanced data set in a cancer classification problem?

Training on a highly imbalanced data set can be problematic because the classifier might simply assign every point to the majority class (normal class in this case), achieving a high accuracy (e.g., 99.9%) but failing to identify cancer cases.

- #machine-learning, #data-imbalance

---

### Flashcard 2

## How can we adjust the posterior probabilities obtained from a balanced data set to reflect the actual class fractions in a population?

The posterior probabilities from a balanced data set can be adjusted by dividing by the class fractions in the balanced data set and then multiplying by the class fractions in the target population, followed by normalization.

$$
p(\mathcal{C}_k \mid \mathbf{x}) = \frac{p_{\text{balanced}}(\mathcal{C}_k \mid \mathbf{x})}{p_{\text{balanced}}(\mathcal{C}_k)} \cdot p_{\text{population}}(\mathcal{C}_k)
$$

- #machine-learning, #probability.theory, #data-imbalance

---

### Flashcard 3

## Derive the posterior probability for a class $\mathcal{C}_k$ given image and blood data, assuming conditional independence.

We start with the conditional independence assumption for distributions $p(\mathbf{x}_{\mathrm{I}}, \mathbf{x}_{\mathrm{B}} \mid \mathcal{C}_k)$:
$$
p\left(\mathbf{x}_{\mathrm{I}}, \mathbf{x}_{\mathrm{B}} \mid \mathcal{C}_{k}\right) = p\left(\mathbf{x}_{\mathrm{I}} \mid \mathcal{C}_{k}\right) p\left(\mathbf{x}_{\mathrm{B}} \mid \mathcal{C}_{k}\right)
$$

Applying Bayes' theorem:
$$
p\left(\mathcal{C}_{k} \mid \mathbf{x}_{\mathrm{I}}, \mathbf{x}_{\mathrm{B}}\right) \propto p\left(\mathbf{x}_{\mathrm{I}}, \mathbf{x}_{\mathrm{B}} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right)
$$

Substituting the conditional independence:
$$
p\left(\mathcal{C}_{k} \mid \mathbf{x}_{\mathrm{I}}, \mathbf{x}_{\mathrm{B}}\right) \propto p\left(\mathbf{x}_{\mathrm{I}} \mid \mathcal{C}_{k}\right) p\left(\mathbf{x}_{\mathrm{B}} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right)
$$

Rewriting with marginal likelihoods:
$$
p\left(\mathcal{C}_{k} \mid \mathbf{x}_{\mathrm{I}}\right) = \frac{p\left(\mathbf{x}_{\mathrm{I}} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right)}{p\left(\mathbf{x}_{\mathrm{I}}\right)}
$$

Thus:
$$
p\left(\mathcal{C}_{k} \mid \mathbf{x}_{\mathrm{I}}, \mathbf{x}_{\mathrm{B}}\right) \propto \frac{p\left(\mathcal{C}_{k} \mid \mathbf{x}_{\mathrm{I}}\right) p\left(\mathcal{C}_{k} \mid \mathbf{x}_{\mathrm{B}}\right)}{p\left(\mathcal{C}_{k}\right)}
$$

- #probability, #bayes-theorem, #conditional-independence

---

### Flashcard 4

## What is the significance of normalizing posterior probabilities in a classification problem?

Normalization is crucial to ensure that the posterior probabilities sum to one, maintaining them as valid probabilities.

---

### Flashcard 5

## Explain the concept of conditional independence in the context of combining image and blood data for classification.

Conditional independence implies that given a class $\mathcal{C}_{k}$, the distributions of the image data $\mathbf{x}_{\mathrm{I}}$ and blood data $\mathbf{x}_{\mathrm{B}}$ are independent:

$$
p\left(\mathbf{x}_{\mathrm{I}}, \mathbf{x}_{\mathrm{B}} \mid \mathcal{C}_{k}\right)=p\left(\mathbf{x}_{\mathrm{I}} \mid \mathcal{C}_{k}\right) p\left(\mathbf{x}_{\mathrm{B}} \mid \mathcal{C}_{k}\right)
$$

This allows for simplified calculations of joint probabilities, benefiting from Bayes' theorem’s application.

- #probability, #conditional-independence, #classification

---

### Flashcard 6

## Why might we prefer to build separate models for different data types (e.g., images and blood tests) rather than a single model?

Separate models for different data types (e.g., images and blood data) reduce the complexity of input space and can more effectively manage heterogeneous information. These models can later be combined using systematic probabilistic rules.

- #machine-learning, #model-combination, #data-types
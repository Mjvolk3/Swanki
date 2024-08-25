## Explain the two types of uncertainty discussed in the paper.

The paper discusses two types of uncertainty: epistemic uncertainty and aleatoric uncertainty.

- Epistemic uncertainty, or model uncertainty, arises from a lack of knowledge and can potentially be reduced by gathering more data.
- Aleatoric uncertainty, or data uncertainty, is intrinsic variability that cannot be reduced by collecting more data.

- #uncertainty.model-uncertainty, #uncertainty.data-uncertainty, #probability

## How does active learning typically handle uncertainty?

In active learning, a typical strategy is to query examples for which $\mathbb{H}(p(y \mid \boldsymbol{x}, \mathcal{D}))$ is large, where $\mathbb{H}(p)$ represents entropy. This entropy can indicate uncertainty about the parameters (epistemic) or inherent variability of the outcome (aleatoric).

$$
\mathbb{H}(p(y \mid \boldsymbol{x}, \mathcal{D})) = - \sum_{y} p(y \mid \boldsymbol{x}, \mathcal{D}) \log p(y \mid \boldsymbol{x}, \mathcal{D})
$$

- #active-learning, #uncertainty.entropy, #machine-learning

## Define the probability of an event $A$.

The probability of an event $A$, denoted as $\operatorname{Pr}(A)$, represents the likelihood that event $A$ is true. It must satisfy $0 \leq \operatorname{Pr}(A) \leq 1$. If $ \operatorname{Pr}(A)=0$, the event will not happen, and if $\operatorname{Pr}(A)=1$, the event will definitely occur.

- #probability.definition, #probability.events

## What is the probability of the complement of an event $A$?

The probability of the complement of an event $A$, denoted as $\operatorname{Pr}(\bar{A})$, is defined as:

$$
\operatorname{Pr}(\bar{A}) = 1 - \operatorname{Pr}(A)
$$

This indicates that the probability of $A$ not happening is $1$ minus the probability of $A$ happening.

- #probability.complement, #basic-rules

## Write the formula for the probability of the conjunction of two events $A$ and $B$, and explain it.

The probability of the conjunction of two events $A$ and $B$, denoted as $\operatorname{Pr}(A \wedge B)$ or $\operatorname{Pr}(A, B)$, is given by:

$$
\operatorname{Pr}(A \wedge B) = \operatorname{Pr}(A) \operatorname{Pr}(B)
$$

if $A$ and $B$ are independent events.

- #probability.conjunction, #rules.independence

## What is the formula for the probability of the union of two events $A$ and $B$?

The probability of the union of two events $A$ and $B$, denoted as $\operatorname{Pr}(A \vee B)$, is given by:

$$
\operatorname{Pr}(A \vee B) = \operatorname{Pr}(A) + \operatorname{Pr}(B) - \operatorname{Pr}(A \wedge B)
$$

This formula accounts for the overlap between events $A$ and $B$.

- #probability.union, #basic-rules
## How does introducing a threshold $\theta$ help in classification problems?

Introducing a threshold $\theta$ helps in classification problems by rejecting inputs $\mathbf{x}$ for which the largest posterior probability $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$ is less than or equal to $\theta$. This allows the system to classify images with high confidence and reject ambiguous cases.

$$
\max_k \{ p\left(\mathcal{C}_{k} \mid \mathbf{x}\right) \} \leq \theta
$$

- #classification, #threshold, #decision-making

## Explain how the value of $\theta$ affects the fraction of examples rejected in a classification system.

Setting $\theta = 1$ will ensure that **all** examples are rejected, while setting $\theta < \frac{1}{K}$ (where $K$ is the number of classes) will ensure that **no** examples are rejected. Thus, the fraction of examples that are rejected is controlled by the value of $\theta$.

$$
\theta = \frac{1}{K} \quad \text{will ensure} \quad \text{no examples are rejected}
$$

- #classification, #threshold-control, #data-handling

## Describe the inference and decision stages in a classification problem.

In classification problems, the **inference stage** uses training data to learn a model for the posterior probabilities $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$. The **decision stage** uses these posterior probabilities to make optimal class assignments by comparing probabilities.

$$
p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)
$$

- #classification, #inference, #decision-making

## What are the three distinct approaches to solving decision problems in classification, ranked by complexity?

The three approaches to solving decision problems are:

1. **Inference problem**: Determine the class-conditional densities $p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)$. Infer prior probabilities $p\left(\mathcal{C}_{k}\right)$. Use Bayes' theorem.

$$
p\left(\mathcal{C}_{k} \mid \mathbf{x}\right) = \frac{p\left(\mathbf{x} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right)}{p(\mathbf{x})}
$$

2. **Direct mapping**: Learn a function that maps inputs $\mathbf{x}$ directly into decisions (discriminant function).
3. **Optimize expected loss**: Minimize expected loss using a loss matrix.

- #classification, #decision-approaches, #complexity

## What is a discriminant function in the context of classification?

A discriminant function is a function that maps inputs $\mathbf{x}$ directly into decisions. It bypasses the two-stage process of inferring posterior probabilities and then making a decision based on those probabilities.

$$
f(\mathbf{x}) \rightarrow \text{Decision}
$$

- #classification, #discriminant-function, #decision-making

## How does Bayes' theorem apply to the classification decision stage?

In the decision stage, Bayes' theorem is used to find the posterior class probabilities from the class-conditional densities and prior probabilities:

$$
p\left(\mathcal{C}_{k} \mid \mathbf{x}\right) = \frac{p\left(\mathbf{x} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right)}{p(\mathbf{x})}
$$

- #classification, #bayes-theorem, #decision-making
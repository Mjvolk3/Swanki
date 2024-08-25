## What does the receiver operator characteristic (ROC) curve represent, and how is it used to evaluate classifiers?

The ROC curve is a plot of true positive rate (TPR) against false positive rate (FPR) that characterizes the trade-off between type 1 errors (false positives) and type 2 errors (false negatives) in a classification problem. The area under the ROC curve (AUC) is often used to evaluate the overall performance of classifiers. A classifier with a higher ROC curve is generally better.

- #machine-learning, #classification.roc-curve

## Derive the $F_1$ score from precision and recall. 

The $F_1$ score is a measure of a test's accuracy and is defined as the harmonic mean of precision and recall.

$$
\begin{aligned}
F_1 &= \frac{2 \times \text{precision} \times \text{recall}}{\text{precision} + \text{recall}} \\
    &= \frac{2N_{\text{TP}}}{2N_{\text{TP}} + N_{\text{FP}} + N_{\text{FN}}}
\end{aligned}
$$

where $N_{\text{TP}}$ is the number of true positives, $N_{\text{FP}}$ is the number of false positives, and $N_{\text{FN}}$ is the number of false negatives.

- #metrics, #classification.f1-score
  
## How can the confusion matrix and loss matrix be used together to compute expected loss?

To compute the expected loss, multiply the elements of the confusion matrix and the loss matrix pointwise, and then sum the resulting products. This method allows for calculating the cost associated with classification errors by considering both the type and frequency of errors.

- #metrics, #classification.confusion-matrix, #loss

## Explain the difference between discriminative and generative approaches to classification.

Discriminative approaches to classification directly model the decision boundary between classes by learning $p(\mathcal{C}_k \mid \mathbf{x})$ directly. Generative approaches, on the other hand, model the class-conditional densities $p(\mathbf{x} \mid \mathcal{C}_k)$ and class priors $p(\mathcal{C}_k)$, and use Bayes' theorem to compute the posterior probabilities $p(\mathcal{C}_k \mid \mathbf{x})$.

$$
p(\mathcal{C}_k \mid \mathbf{x}) = \frac{p(\mathbf{x} \mid \mathcal{C}_k)p(\mathcal{C}_k)}{\sum_{i} p(\mathbf{x} \mid \mathcal{C}_i)p(\mathcal{C}_i)}
$$

- #machine-learning, #classification.generative, #classification.discriminative

## What assumption leads to linear decision boundaries in generative classifiers?

Linear decision boundaries arise from the assumption that the class-conditional densities $p(\mathbf{x} \mid \mathcal{C}_k)$ are Gaussian with shared covariance matrices. This leads to the log-likelihood ratio being a linear function of $\mathbf{x}$, resulting in linear decision boundaries.

- #machine-learning, #classification.generative
  
## With regard to the ROC curve and its extension to more than two classes, explain why it becomes cumbersome.

The ROC curve can be extended to multi-class problems, but it becomes cumbersome because the number of pairwise comparisons between classes grows quadratically with the number of classes. This makes it difficult to visualize and interpret the performance of classifiers as the number of classes increases.

- #machine-learning, #classification.multi-class, #roc-curve
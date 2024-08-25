```markdown
## Explain why accuracy can be misleading in imbalanced class scenarios, using the cancer screening example from the paper.
  
Accuracy can be misleading in imbalanced class scenarios because it does not account for the distribution of class labels. For example, in a cancer screening setting where only 1 person in 1,000 has cancer, a classifier that predicts no one has cancer will achieve $99.9\%$ accuracy, but is completely useless as it fails to detect any actual cancer cases.

- .classification-problems, .performance-metrics

## Define the precision and recall metrics and explain their importance in the context of the cancer screening example.

Precision and recall can be defined as:

$$
\begin{aligned}
\text{Precision} &= \frac{N_{\mathrm{TP}}}{N_{\mathrm{TP}} + N_{\mathrm{FP}}} \\
\text{Recall} &= \frac{N_{\mathrm{TP}}}{N_{\mathrm{TP}} + N_{\mathrm{FN}}}
\end{aligned}
$$

In the cancer screening example, precision indicates the probability that a person who has a positive test actually has cancer, while recall indicates the probability that the test correctly identifies individuals who have cancer.

- .classification-problems, .metrics.precision-recall
  
## What does the false positive rate indicate in the context of a cancer screening test? Provide its mathematical definition.

The false positive rate indicates the probability that a person who is actually normal will be classified as having cancer. Mathematically, it is defined as:

$$
\text{False positive rate} = \frac{N_{\mathrm{FP}}}{N_{\mathrm{FP}} + N_{\mathrm{TN}}}
$$

- .classification-problems, .metrics.false-positive-rate

## {{c1::Receiver Operating Characteristic (ROC) curves}} are useful for understanding the trade-off between type 1 and type 2 errors. 

## How can you alter the trade-off between type 1 and type 2 errors for a probabilistic classifier?

To alter the trade-off between type 1 and type 2 errors for a probabilistic classifier, you can change the threshold value at which the classifier decides a positive or negative outcome. By varying this threshold, you can reduce type 1 errors (false positives) at the expense of increasing type 2 errors (false negatives), and vice versa.

- .classification-problems, .threshold-adjustment

## Define False Discovery Rate (FDR) and explain its implication in the context of a cancer screening test.

False Discovery Rate (FDR) is defined as:

$$
\text{False Discovery Rate} = \frac{N_{\mathrm{FP}}}{N_{\mathrm{FP}} + N_{\mathrm{TP}}}
$$

In the context of a cancer screening test, FDR represents the fraction of those testing positive who do not actually have cancer. It gives an estimate of the incorrect positive diagnoses.

- .classification-problems, .metrics.false-discovery-rate
  
## Explain how the regions $A, B, C, D, E$ in the decision boundary of a classifier relate to $N_{\mathrm{TP}}, N_{\mathrm{FP}}, N_{\mathrm{FN}}, N_{\mathrm{TN}}$.

The regions are related to the various true and false rates as follows:

$$
\begin{aligned}
& N_{\mathrm{FP}} / N = E \\
& N_{\mathrm{TP}} / N = D + E \\
& N_{\mathrm{FN}} / N = B + C \\
& N_{\mathrm{TN}} / N = A + C
\end{aligned}
$$

Here, $N$ represents the total number of observations, and $N_{\mathrm{TP}}, N_{\mathrm{FP}}, N_{\mathrm{FN}}, N_{\mathrm{TN}}$ represent the number of true positives, false positives, false negatives, and true negatives, respectively.

- .classification-problems, .decision-boundary
```
Figure 5.11 The receiver operator characteristic (ROC) curve is a plot of true positive rate against false positive rate, and it characterizes the trade-off between type 1 and type 2 errors in a classification problem. The upper blue curve represents a better classifier than the lower red curve. Here the dashed curve represents the performance of a simple random classifier.

![](https://cdn.mathpix.com/cropped/2024_05_26_1cbadc682ee2a0381817g-1.jpg?height=704&width=711&top_left_y=212&top_left_x=934)

recall, and is therefore defined by

\[
\begin{aligned}
F & =\frac{2 \times \text { precision } \times \text { recall }}{\text { precision }+ \text { recall }} \\
& =\frac{2 N_{\mathrm{TP}}}{2 N_{\mathrm{TP}}+N_{\mathrm{FP}}+N_{\mathrm{FN}}}
\end{aligned}
\]

Of course, we can also combine the confusion matrix in Figure 5.9 with the loss matrix in Figure 5.6 to compute the expected loss by multiplying the elements pointwise and summing the resulting products.

Although the ROC curve can be extended to more than two classes, it rapidly becomes cumbersome as the number of classes increases.

\title{
5.3. Generative Classifiers
}

We turn next to a probabilistic view of classification and show how models with linear decision boundaries arise from simple assumptions about the distribution of the data. We have already discussed the distinction between the discriminative and the generative approaches to classification. Here we will adopt a generative approach in which we model the class-conditional densities \(p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)\) as well as the class priors \(p\left(\mathcal{C}_{k}\right)\) and then use these to compute posterior probabilities \(p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)\) through Bayes' theorem.

First, consider problems having two classes. The posterior probability for class
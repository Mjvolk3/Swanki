Figure 5.7 Illustration of the reject option. Inputs $x$ such that the larger of the two posterior probabilities is less than or equal to some threshold $\theta$ will be rejected.

![](https://cdn.mathpix.com/cropped/2024_05_26_49629de898dc2113d75dg-1.jpg?height=523&width=672&top_left_y=215&top_left_x=973)

system to classify those images for which there is little doubt as to the correct class, while requesting a biopsy to classify the more ambiguous cases. We can achieve this by introducing a threshold $\theta$ and rejecting those inputs $\mathbf{x}$ for which the largest of the posterior probabilities $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$ is less than or equal to $\theta$. This is illustrated for two classes and a single continuous input variable $x$ in Figure 5.7. Note that setting $\theta=1$ will ensure that all examples are rejected, whereas if there are $K$ classes, then setting $\theta<1 / K$ will ensure that no examples are rejected. Thus, the fraction of examples that are rejected is controlled by the value of $\theta$.

We can easily extend the reject criterion to minimize the expected loss, when a loss matrix is given, by taking account of the loss incurred when a reject decision is made.

\title{
5.2.4 Inference and decision
}

We have broken the classification problem down into two separate stages, the inference stage in which we use training data to learn a model for $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$ and the subsequent decision stage in which we use these posterior probabilities to make optimal class assignments. An alternative possibility would be to solve both problems together and simply learn a function that maps inputs $\mathbf{x}$ directly into decisions. Such a function is called a discriminant function.

In fact, we can identify three distinct approaches to solving decision problems, all of which have been used in practical applications. These are, in decreasing order of complexity, as follows:

(a) First, solve the inference problem of determining the class-conditional densities $p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)$ for each class $\mathcal{C}_{k}$ individually. Separately infer the prior class probabilities $p\left(\mathcal{C}_{k}\right)$. Then use Bayes' theorem in the form

$$
p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)=\frac{p\left(\mathbf{x} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right)}{p(\mathbf{x})}
$$

to find the posterior class probabilities $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$. As usual, the denominator in
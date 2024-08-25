\begin{tabular}{cc|cc} 
& & \multicolumn{2}{|c}{ Observation } \\
& & 0 & 1 \\
\hline \multirow{2}{*}{ Truth } & 0 & $\mathrm{TNR}=$ Specificity $=0.975$ & $\mathrm{FPR}=1-\mathrm{TNR}=0.025$ \\
& 1 & $\mathrm{FNR}=1-\mathrm{TPR}=0.125$ & TPR $=$ Sensitivity $=0.875$
\end{tabular}

Table 2.1: Likelihood function $p(Y \mid H)$ for a binary observation $Y$ given two possible hidden states $H$. Each row sums to one. Abbreviations: TNR is true negative rate, TPR is true positive rate, FNR is false negative rate, FPR is false positive rate.

Normalizing the joint distribution by computing $p(H=h, Y=y) / p(Y=y)$ for each $h$ gives the posterior distribution $p(H=h \mid Y=y)$; this represents our new belief state about the possible values of $H$.

We can summarize Bayes rule in words as follows:

$$
\text { posterior } \propto \text { prior } \times \text { likelihood }
$$

Here we use the symbol $\propto$ to denote "proportional to", since we are ignoring the denominator, which is just a constant, independent of $H$. Using Bayes rule to update a distribution over unknown values of some quantity of interest, given relevant observed data, is called Bayesian inference, or posterior inference. It can also just be called probabilistic inference.

Below we give some simple examples of Bayesian inference in action. We will see many more interesting examples later in this book.

\title{
2.3.1 Example: Testing for COVID-19
}

Suppose you think you may have contracted COVID-19, which is an infectious disease caused by the SARS-CoV-2 virus. You decide to take a diagnostic test, and you want to use its result to determine if you are infected or not.

Let $H=1$ be the event that you are infected, and $H=0$ be the event you are not infected. Let $Y=1$ if the test is positive, and $Y=0$ if the test is negative. We want to compute $p(H=h \mid Y=y)$, for $h \in\{0,1\}$, where $y$ is the observed test outcome. (We will write the distribution of values, $[p(H=0 \mid Y=y), p(H=1 \mid Y=y)]$ as $p(H \mid y)$, for brevity.) We can think of this as a form of binary classification, where $H$ is the unknown class label, and $y$ is the feature vector.

First we must specify the likelihood. This quantity obviously depends on how reliable the test is. There are two key parameters. The sensitivity (aka true positive rate) is defined as $p(Y=1 \mid H=1)$, i.e., the probability of a positive test given that the truth is positive. The false negative rate is defined as one minus the sensitivity. The specificity (aka true negative rate) is defined as $p(Y=0 \mid H=0)$, i.e., the probability of a negative test given that the truth is negative. The false positive rate is defined as one minus the specificity. We summarize all these quantities in Table 2.1. (See Section 5.1.3.1 for more details.) Following https://nyti.ms/31mTZgV, we set the sensitivity to $87.5 \%$ and the specificity to $97.5 \%$.

Next we must specify the prior. The quantity $p(H=1)$ represents the prevalence of the disease in the area in which you live. We set this to $p(H=1)=0.1$ (i.e., $10 \%$ ), which was the prevalence in New York City in Spring 2020. (This example was chosen to match the numbers in https://nyti.ms/31MTZgV.)

Draft of "Probabilistic Machine Learning: An Introduction". August 8, 2022
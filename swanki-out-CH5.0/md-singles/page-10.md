to class \(\mathcal{C}_{1}\) is assigned to class \(\mathcal{C}_{2}\) or vice versa. The probability of this occurring is given by

\[
\begin{aligned}
p(\text { mistake }) & =p\left(\mathbf{x} \in \mathcal{R}_{1}, \mathcal{C}_{2}\right)+p\left(\mathbf{x} \in \mathcal{R}_{2}, \mathcal{C}_{1}\right) \\
& =\int_{\mathcal{R}_{1}} p\left(\mathbf{x}, \mathcal{C}_{2}\right) \mathrm{d} \mathbf{x}+\int_{\mathcal{R}_{2}} p\left(\mathbf{x}, \mathcal{C}_{1}\right) \mathrm{d} \mathbf{x}
\end{aligned}
\]

We are free to choose the decision rule that assigns each point \(\mathrm{x}\) to one of the two classes. Clearly, to minimize \(p\) (mistake) we should arrange that each \(\mathbf{x}\) is assigned to whichever class has the smaller value of the integrand in (5.20). Thus, if \(p\left(\mathbf{x}, \mathcal{C}_{1}\right)>p\left(\mathbf{x}, \mathcal{C}_{2}\right)\) for a given value of \(\mathbf{x}\), then we should assign that \(\mathbf{x}\) to class \(\mathcal{C}_{1}\). From the product rule of probability, we have \(p\left(\mathbf{x}, \mathcal{C}_{k}\right)=p\left(\mathcal{C}_{k} \mid \mathbf{x}\right) p(\mathbf{x})\). Because the factor \(p(\mathbf{x})\) is common to both terms, we can restate this result as saying that the minimum probability of making a mistake is obtained if each value of \(\mathrm{x}\) is assigned to the class for which the posterior probability \(p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)\) is largest. This result is illustrated for two classes and a single input variable \(x\) in Figure 5.5.

For the more general case of \(K\) classes, it is slightly easier to maximize the probability of being correct, which is given by

\[
\begin{aligned}
p(\text { correct }) & =\sum_{k=1}^{K} p\left(\mathbf{x} \in \mathcal{R}_{k}, \mathcal{C}_{k}\right) \\
& =\sum_{k=1}^{K} \int_{\mathcal{R}_{k}} p\left(\mathbf{x}, \mathcal{C}_{k}\right) \mathrm{d} \mathbf{x}
\end{aligned}
\]

which is maximized when the regions \(\mathcal{R}_{k}\) are chosen such that each \(\mathrm{x}\) is assigned to the class for which \(p\left(\mathbf{x}, \mathcal{C}_{k}\right)\) is largest. Again, using the product rule \(p\left(\mathbf{x}, \mathcal{C}_{k}\right)=\) \(p\left(\mathcal{C}_{k} \mid \mathbf{x}\right) p(\mathbf{x})\), and noting that the factor of \(p(\mathbf{x})\) is common to all terms, we see that each \(\mathrm{x}\) should be assigned to the class having the largest posterior probability \(p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)\).

\title{
5.2.2 Expected loss
}

For many applications, our objective will be more complex than simply minimizing the number of misclassifications. Let us consider again the medical diagnosis problem. We note that, if a patient who does not have cancer is incorrectly diagnosed as having cancer, the consequences may be that they experience some distress plus there is the need for further investigations. Conversely, if a patient with cancer is diagnosed as healthy, the result may be premature death due to lack of treatment. Thus, the consequences of these two types of mistake can be dramatically different. It would clearly be better to make fewer mistakes of the second kind, even if this was at the expense of making more mistakes of the first kind.

We can formalize such issues through the introduction of a loss function, also called a cost function, which is a single, overall measure of loss incurred in taking any of the available decisions or actions. Our goal is then to minimize the total loss incurred. Note that some authors consider instead a utility function, whose value
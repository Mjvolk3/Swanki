has cancer? This requires that we evaluate the probability of cancer conditional on the outcome of the test, whereas the probabilities in (2.14) to (2.17) give the probability distribution over the test outcome conditioned on whether the person has cancer. We can solve the problem of reversing the conditional probability by using Bayes' theorem (2.10) to give

\[
\begin{aligned}
p(C=1 \mid T=1) & =\frac{p(T=1 \mid C=1) p(C=1)}{p(T=1)} \\
& =\frac{90}{100} \times \frac{1}{100} \times \frac{10,000}{387}=\frac{90}{387} \simeq 0.23
\end{aligned}
\]

so that if a person is tested at random and the test is positive, there is a \(23 \%\) probability that they actually have cancer. From the sum rule, it then follows that \(p(C=\) \(0 \mid T=1)=1-90 / 387=297 / 387 \simeq 0.77\), which is a \(77 \%\) chance that they do not have cancer.

\title{
2.1.5 Prior and posterior probabilities
}

We can use the cancer screening example to provide an important interpretation of Bayes' theorem as follows. If we had been asked whether someone is likely to have cancer, before they have received a test, then the most complete information we have available is provided by the probability \(p(C)\). We call this the prior probability because it is the probability available before we observe the result of the test. Once we are told that this person has received a positive test, we can then use Bayes' theorem to compute the probability \(p(C \mid T)\), which we will call the posterior probability because it is the probability obtained after we have observed the test result \(T\).

In this example, the prior probability of having cancer is \(1 \%\). However, once we have observed that the test result is positive, we find that the posterior probability of cancer is now \(23 \%\), which is a substantially higher probability of cancer, as we would intuitively expect. We note, however, that a person with a positive test still has only a \(23 \%\) change of actually having cancer, even though the test appears, from Figure 2.3 to be reasonably 'accurate'. This conclusion seems counter-intuitive to many people. The reason has to do with the low prior probability of having cancer. Although the test provides strong evidence of cancer, this has to be combined with the prior probability using Bayes' theorem to arrive at the correct posterior probability.

\subsection*{2.1.6 Independent variables}

Finally, if the joint distribution of two variables factorizes into the product of the marginals, so that \(p(X, Y)=p(X) p(Y)\), then \(X\) and \(Y\) are said to be independent. An example of independent events would be the successive flips of a coin. From the product rule, we see that \(p(Y \mid X)=p(Y)\), and so the conditional distribution of \(Y\) given \(X\) is indeed independent of the value of \(X\). In our cancer screening example, if the probability of a positive test is independent of whether the person has cancer, then \(p(T \mid C)=p(T)\), which means that from Bayes' theorem (2.10) we have \(p(C \mid T)=p(C)\), and therefore probability of cancer is not changed by observing the test outcome. Of course, such a test would be useless because the outcome of the test tells us nothing about whether the person has cancer.
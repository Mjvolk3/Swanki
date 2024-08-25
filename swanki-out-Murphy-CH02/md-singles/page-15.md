Now suppose you test positive. We have

\[
\begin{aligned}
p(H=1 \mid Y=1) & =\frac{p(Y=1 \mid H=1) p(H=1)}{p(Y=1 \mid H=1) p(H=1)+p(Y=1 \mid H=0) p(H=0)} \\
& =\frac{\mathrm{TPR} \times \text { prior }}{\mathrm{TPR} \times \text { prior }+\mathrm{FPR} \times(1-\text { prior })} \\
& =\frac{0.875 \times 0.1}{0.875 \times 0.1+0.025 \times 0.9}=0.795
\end{aligned}
\]

So there is a \(79.5 \%\) chance you are infected.

Now suppose you test negative. The probability you are infected is given by

\[
\begin{aligned}
p(H=1 \mid Y=0) & =\frac{p(Y=0 \mid H=1) p(H=1)}{p(Y=0 \mid H=1) p(H=1)+p(Y=0 \mid H=0) p(H=0)} \\
& =\frac{\text { FNR } \times \text { prior }}{\text { FNR } \times \text { prior }+ \text { TNR } \times(1-\text { prior })} \\
& =\frac{0.125 \times 0.1}{0.125 \times 0.1+0.975 \times 0.9}=0.014
\end{aligned}
\]

So there is just a \(1.4 \%\) chance you are infected.

Nowadays COVID-19 prevalence is much lower. Suppose we repeat these calculations using a base rate of \(1 \%\); now the posteriors reduce to \(26 \%\) and \(0.13 \%\) respectively.

The fact that you only have a \(26 \%\) chance of being infected with COVID-19, even after a positive test, is very counter-intuitive. The reason is that a single positive test is more likely to be a false positive than due to the disease, since the disease is rare. To see this, suppose we have a population of 100,000 people, of whom 1000 are infected. Of those who are infected, \(875=0.875 \times 1000\) test positive, and of those who are uninfected, \(2475=0.025 \times 99,000\) test positive. Thus the total number of positives is \(3350=875+2475\), so the posterior probability of being infected given a positive test is \(875 / 3350=0.26\).

Of course, the above calculations assume we know the sensitivity and specificity of the test. See [GC20] for how to apply Bayes rule for diagnostic testing when there is uncertainty about these parameters.

\title{
2.3.2 Example: The Monty Hall problem
}

In this section, we consider a more "frivolous" application of Bayes rule. In particular, we apply it to the famous Monty Hall problem.

Imagine a game show with the following rules: There are three doors, labeled 1, 2, 3. A single prize (e.g., a car) has been hidden behind one of them. You get to select one door. Then the gameshow host opens one of the other two doors (not the one you picked), in such a way as to not reveal the prize location. At this point, you will be given a fresh choice of door: you can either stick with your first choice, or you can switch to the other closed door. All the doors will then be opened and you will receive whatever is behind your final choice of door.

For example, suppose you choose door 1 , and the gameshow host opens door 3 , revealing nothing behind the door, as promised. Should you (a) stick with door 1 , or (b) switch to door 2 , or (c) does it make no difference?

Author: Kevin P. Murphy. (C) MIT Press. CC-BY-NC-ND license
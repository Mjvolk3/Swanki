Figure 2.2 Probability can be viewed either as a frequency associated with a repeatable event or as a quantification of uncertainty. A bent coin can be used to illustrate the difference, as discussed in the text.

![](https://cdn.mathpix.com/cropped/2024_05_10_1ff7c1baa6bdceecd13ag-1.jpg?height=244&width=354&top_left_y=222&top_left_x=917)

$60 \%$

![](https://cdn.mathpix.com/cropped/2024_05_10_1ff7c1baa6bdceecd13ag-1.jpg?height=239&width=342&top_left_y=230&top_left_x=1302)

$40 \%$

know which side is heads and which is tails. If asked to take a bet on whether the coin will land heads or tails when flipped, then symmetry suggests that our bet should be based on the assumption that the probability of seeing heads is 0.5 , and indeed a more careful analysis shows that, in the absence of any additional information, this is indeed the rational choice. Here we are using probabilities in a more general sense than simply the frequency of events. Whether the convex side of the coin is heads or tails is not itself a repeatable event, it is simply unknown. The use of probability as a

Section 2.6 quantification of uncertainty is the Bayesian perspective and is more general in that it includes frequentist probability as a special case. We can learn about which side of the coin is heads if we are given results from a sequence of coin flips by making Exercise 2.40 use of Bayesian reasoning. The more results we observe, the lower our uncertainty as to which side of the coin is which.

Having introduced the concept of probability informally, we turn now to a more detailed exploration of probabilities and discuss how to use them quantitatively. Concepts developed in the remainder of this chapter will form a core foundation for many of the topics discussed throughout the book.

\title{
2.1. The Rules of Probability
}

In this section we will derive two simple rules that govern the behaviour of probabilities. However, in spite of their apparent simplicity, these rules will prove to be very powerful and widely applicable. We will motivate the rules of probability by first introducing a simple example.

\subsection*{2.1.1 A medical screening example}

Consider the problem of screening a population in order to provide early detection of cancer, and let us suppose that $1 \%$ of the population actually have cancer. Ideally our test for cancer would give a positive result for anyone who has cancer and a negative result for anyone who does not. However, tests are not perfect, so we will suppose that when the test is given to people who are free of cancer, $3 \%$ of them will test positive. These are known as false positives. Similarly, when the test is given to people who do have cancer, $10 \%$ of them will test negative. These are called false negatives. The various error rates are illustrated in Figure 2.3.

Given this information, we might ask the following questions: (1) 'If we screen the population, what is the probability that someone will test positive?', (2) 'If some-
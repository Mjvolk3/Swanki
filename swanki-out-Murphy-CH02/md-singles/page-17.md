![](https://cdn.mathpix.com/cropped/2024_06_13_ab164e7d058b84145366g-1.jpg?height=387&width=250&top_left_y=202&top_left_x=872)

Figure 2.8: Any planar line-drawing is geometrically consistent with infinitely many 3-D structures. From Figure 11 of [SA93]. Used with kind permission of Pawan Sinha.

\title{
2.3.3 Inverse problems *
}

Probability theory is concerned with predicting a distribution over outcomes \(y\) given knowledge (or assumptions) about the state of the world, \(h\). By contrast, inverse probability is concerned with inferring the state of the world from observations of outcomes. We can think of this as inverting the \(h \rightarrow y\) mapping.

For example, consider trying to infer a \(3 \mathrm{~d}\) shape \(h\) from a \(2 \mathrm{~d}\) image \(y\), which is a classic problem in visual scene understanding. Unfortunately, this is a fundamentally ill-posed problem, as illustrated in Figure 2.8, since there are multiple possible hidden \(h\) 's consistent with the same observed \(y\) (see e.g., [Piz01]). Similarly, we can view natural language understanding as an ill-posed problem, in which the listener must infer the intention \(h\) from the (often ambiguous) words spoken by the speaker (see e.g., [Sab21]).

To tackle such inverse problems, we can use Bayes' rule to compute the posterior, \(p(h \mid y)\), which gives a distribution over possible states of the world. This requires specifying the forwards model, \(p(y \mid h)\), as well as a prior \(p(h)\), which can be used to rule out (or downweight) implausible world states. We discuss this topic in more detail in the sequel to this book, [Mur23].

\subsection*{2.4 Bernoulli and binomial distributions}

Perhaps the simplest probability distribution is the Bernoulli distribution, which can be used to model binary events, as we discuss below.

\subsection*{2.4.1 Definition}

Consider tossing a coin, where the probability of event that it lands heads is given by \(0 \leq \theta \leq 1\). Let \(Y=1\) denote this event, and let \(Y=0\) denote the event that the coin lands tails. Thus we are assuming that \(p(Y=1)=\theta\) and \(p(Y=0)=1-\theta\). This is called the Bernoulli distribution, and can be written as follows

\[
Y \sim \operatorname{Ber}(\theta)
\]

Author: Kevin P. Murphy. (C) MIT Press. CC-BY-NC-ND license
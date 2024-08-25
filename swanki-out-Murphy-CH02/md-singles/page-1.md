\title{
Probability: Univariate Models
}

\subsection*{2.1 Introduction}

In this chapter, we give a brief introduction to the basics of probability theory. There are many good books that go into more detail, e.g., [GS97; BT08].

\subsection*{2.1.1 What is probability?}

Probability theory is nothing but common sense reduced to calculation. - Pierre Laplace, 1812

We are all comfortable saying that the probability that a (fair) coin will land heads is \(50 \%\). But what does this mean? There are actually two different interpretations of probability. One is called the frequentist interpretation. In this view, probabilities represent long run frequencies of events that can happen multiple times. For example, the above statement means that, if we flip the coin many times, we expect it to land heads about half the time. \({ }^{1}\)

The other interpretation is called the Bayesian interpretation of probability. In this view, probability is used to quantify our uncertainty or ignorance about something; hence it is fundamentally related to information rather than repeated trials [Jay03; Lin06]. In the Bayesian view, the above statement means we believe the coin is equally likely to land heads or tails on the next toss.

One big advantage of the Bayesian interpretation is that it can be used to model our uncertainty about one-off events that do not have long term frequencies. For example, we might want to compute the probability that the polar ice cap will melt by 2030 CE. This event will happen zero or one times, but cannot happen repeatedly. Nevertheless, we ought to be able to quantify our uncertainty about this event; based on how probable we think this event is, we can decide how to take the optimal action, as discussed in Chapter 5. We shall therefore adopt the Bayesian interpretation in this book. Fortunately, the basic rules of probability theory are the same, no matter which interpretation is adopted.

\subsection*{2.1.2 Types of uncertainty}

The uncertainty in our predictions can arise for two fundamentally different reasons. The first is due to our ignorance of the underlying hidden causes or mechanism generating our data. This is
\footnotetext{
1. Actually, the Stanford statistician (and former professional magician) Persi Diaconis has shown that a coin is about \(51 \%\) likely to land facing the same way up as it started, due to the physics of the problem [DHM07].
}
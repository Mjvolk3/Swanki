called epistemic uncertainty, since epistemology is the philosophical term used to describe the study of knowledge. However, a simpler term for this is model uncertainty. The second kind of uncertainty arises from intrinsic variability, which cannot be reduced even if we collect more data. This is sometimes called aleatoric uncertainty [Hac75; KD09], derived from the Latin word for "dice", although a simpler term would be data uncertainty. As a concrete example, consider tossing a fair coin. We might know for sure that the probability of heads is \(p=0.5\), so there is no epistemic uncertainty, but we still cannot perfectly predict the outcome.

This distinction can be important for applications such as active learning. A typical strategy is to query examples for which \(\mathbb{H}(p(y \mid \boldsymbol{x}, \mathcal{D})\) ) is large (where \(\mathbb{H}(p)\) is the entropy, discussed in Section 6.1). However, this could be due to uncertainty about the parameters, i.e., large \(\mathbb{H}(p(\boldsymbol{\theta} \mid \mathcal{D}))\), or just due to inherent variability of the outcome, corresponding to large entropy of \(p(y \mid \boldsymbol{x}, \boldsymbol{\theta})\). In the latter case, there would not be much use collecting more samples, since our epistemic uncertainty would not be reduced. See [Osb16] for further discussion of this point.

\title{
2.1.3 Probability as an extension of logic
}

In this section, we review the basic rules of probability, following the presentation of [Jay03], in which we view probability as an extension of Boolean logic.

\subsection*{2.1.3.1 Probability of an event}

We define an event, denoted by the binary variable \(A\), as some state of the world that either holds or does not hold. For example, \(A\) might be event "it will rain tomorrow", or "it rained yesterday", or "the label is \(y=1\) ", or "the parameter \(\theta\) is between 1.5 and 2.0", etc. The expression \(\operatorname{Pr}(A)\) denotes the probability with which you believe event \(A\) is true (or the long run fraction of times that \(A\) will occur). We require that \(0 \leq \operatorname{Pr}(A) \leq 1\), where \(\operatorname{Pr}(A)=0\) means the event definitely will not happen, and \(\operatorname{Pr}(A)=1\) means the event definitely will happen. We write \(\operatorname{Pr}(\bar{A})\) to denote the probability of event \(A\) not happening; this is defined to be \(\operatorname{Pr}(\bar{A})=1-\operatorname{Pr}(A)\).

\subsection*{2.1.3.2 Probability of a conjunction of two events}

We denote the joint probability of events \(A\) and \(B\) both happening as follows:

\[
\operatorname{Pr}(A \wedge B)=\operatorname{Pr}(A, B)
\]

If \(A\) and \(B\) are independent events, we have

\[
\operatorname{Pr}(A, B)=\operatorname{Pr}(A) \operatorname{Pr}(B)
\]

For example, suppose \(X\) and \(Y\) are chosen uniformly at random from the set \(\mathcal{X}=\{1,2,3,4\}\). Let \(A\) be the event that \(X \in\{1,2\}\), and \(B\) be the event that \(Y \in\{3\}\). Then we have \(\operatorname{Pr}(A, B)=\) \(\operatorname{Pr}(A) \operatorname{Pr}(B)=\frac{1}{2} \cdot \frac{1}{4}\).

\subsection*{2.1.3.3 Probability of a union of two events}

The probability of event \(A\) or \(B\) happening is given by

\[
\operatorname{Pr}(A \vee B)=\operatorname{Pr}(A)+\operatorname{Pr}(B)-\operatorname{Pr}(A \wedge B)
\]

Draft of "Probabilistic Machine Learning: An Introduction". August 8, 2022
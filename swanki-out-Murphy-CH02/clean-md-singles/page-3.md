If the events are mutually exclusive (so they cannot happen at the same time), we get

$$
\operatorname{Pr}(A \vee B)=\operatorname{Pr}(A)+\operatorname{Pr}(B)
$$

For example, suppose $X$ is chosen uniformly at random from the set $\mathcal{X}=\{1,2,3,4\}$. Let $A$ be the event that $X \in\{1,2\}$ and $B$ be the event that $X \in\{3\}$. Then we have $\operatorname{Pr}(A \vee B)=\frac{2}{4}+\frac{1}{4}$.

\title{
2.1.3.4 Conditional probability of one event given another
}

We define the conditional probability of event $B$ happening given that $A$ has occurred as follows:

$$
\operatorname{Pr}(B \mid A) \triangleq \frac{\operatorname{Pr}(A, B)}{\operatorname{Pr}(A)}
$$

This is not defined if $\operatorname{Pr}(A)=0$, since we cannot condition on an impossible event.

\subsection*{2.1.3.5 Independence of events}

We say that event $A$ is independent of event $B$ if

$$
\operatorname{Pr}(A, B)=\operatorname{Pr}(A) \operatorname{Pr}(B)
$$

\subsection*{2.1.3.6 Conditional independence of events}

We say that events $A$ and $B$ are conditionally independent given event $C$ if

$$
\operatorname{Pr}(A, B \mid C)=\operatorname{Pr}(A \mid C) \operatorname{Pr}(B \mid C)
$$

This is written as $A \perp B \mid C$. Events are often dependent on each other, but may be rendered independent if we condition on the relevant intermediate variables, as we discuss in more detail later in this chapter.

\subsection*{2.2 Random variables}

Suppose $X$ represents some unknown quantity of interest, such as which way a dice will land when we roll it, or the temperature outside your house at the current time. If the value of $X$ is unknown and/or could change, we call it a random variable or $\mathbf{r v}$. The set of possible values, denoted $\mathcal{X}$, is known as the sample space or state space. An event is a set of outcomes from a given sample space. For example, if $X$ represents the face of a dice that is rolled, so $\mathcal{X}=\{1,2, \ldots, 6\}$, the event of "seeing a 1 " is denoted $X=1$, the event of "seeing an odd number" is denoted $X \in\{1,3,5\}$, the event of "seeing a number between 1 and 3 " is denoted $1 \leq X \leq 3$, etc.

\subsection*{2.2.1 Discrete random variables}

If the sample space $\mathcal{X}$ is finite or countably infinite, then $X$ is called a discrete random variable. In this case, we denote the probability of the event that $X$ has value $x$ by $\operatorname{Pr}(X=x)$. We define the

Author: Kevin P. Murphy. (C) MIT Press. CC-BY-NC-ND license
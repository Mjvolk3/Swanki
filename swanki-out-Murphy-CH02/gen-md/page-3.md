## Given two mutually exclusive events A and B, what is the probability of either A or B occurring?

If the events are mutually exclusive (so they cannot happen at the same time), we get

$$
\operatorname{Pr}(A \vee B)=\operatorname{Pr}(A)+\operatorname{Pr}(B)
$$

For example, suppose $X$ is chosen uniformly at random from the set $\{1,2,3,4\}$. Let $A$ be the event that $X \in\{1,2\}$ and $B$ be the event that $X \in\{3\}$. Then we have

$$
\operatorname{Pr}(A \vee B)=\frac{2}{4}+\frac{1}{4}
$$.

- #probability.mutually-exclusive, #probability.basic-rules
  
## What is the definition of conditional probability of event B given event A?

The conditional probability of event $B$ happening given that $A$ has occurred is given by:

$$
\operatorname{Pr}(B \mid A) \triangleq \frac{\operatorname{Pr}(A, B)}{\operatorname{Pr}(A)}
$$

This is not defined if $\operatorname{Pr}(A)=0$, since we cannot condition on an impossible event.

- #probability.conditional-probability, #probability.basic-rules

## How is independence of events A and B defined?

Event $A$ is independent of event $B$ if

$$
\operatorname{Pr}(A, B)=\operatorname{Pr}(A) \operatorname{Pr}(B)
$$

- #probability.independence, #probability.basic-rules

## What is the definition of conditional independence of events A and B given event C?

Events $A$ and $B$ are conditionally independent given event $C$ if

$$
\operatorname{Pr}(A, B \mid C)=\operatorname{Pr}(A \mid C) \operatorname{Pr}(B \mid C)
$$

This is written as $A \perp B \mid C$.

- #probability.conditional-independence, #probability.basic-rules

## What is a random variable (rv) and what is the sample space or state space?

A random variable represents some unknown quantity of interest, such as the outcome of a dice roll, denoted as $X$. The set of possible values, denoted $\mathcal{X}$, is known as the sample space or state space. For example, if $X$ represents the face of a dice that is rolled, so $\mathcal{X}=\{1,2, \ldots, 6\}$, then different events can be:

- Seeing a 1: $X=1$
- Seeing an odd number: $X \in\{1,3,5\}$
- Seeing a number between 1 and 3: $1 \leq X \leq 3$

- #random-variables.definition, #probability.sample-space

## What are discrete random variables and how is the probability of a discrete event denoted?

If the sample space $\mathcal{X}$ is finite or countably infinite, then $X$ is called a discrete random variable. In this case, we denote the probability of the event that $X$ has value $x$ by $\operatorname{Pr}(X=x)$.

- #random-variables.discrete, #probability.discrete-events
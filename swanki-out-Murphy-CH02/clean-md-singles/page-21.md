In other words,

$$
p(y=1 \mid \boldsymbol{x} ; \boldsymbol{\theta})=\sigma\left(\boldsymbol{w}^{\top} \boldsymbol{x}+b\right)=\frac{1}{1+e^{-\left(\boldsymbol{w}^{\top} \boldsymbol{x}+b\right)}}
$$

This is called logistic regression.

For example consider a 1-dimensional, 2-class version of the iris dataset, where the positive class is "Virginica" and the negative class is "not Virginica", and the feature $x$ we use is the petal width. We fit a logistic regression model to this and show the results in Figure 2.11. The decision boundary corresponds to the value $x^{*}$ where $p\left(y=1 \mid x=x^{*}, \boldsymbol{\theta}\right)=0.5$. We see that, in this example, $x^{*} \approx 1.7$. As $x$ moves away from this boundary, the classifier becomes more confident in its prediction about the class label.

It should be clear from this example why it would be inappropriate to use linear regression for a (binary) classification problem. In such a model, the probabilities would increase above 1 as we move far enough to the right, and below 0 as we move far enough to the left.

For more detail on logistic regression, see Chapter 10.

\title{
2.5 Categorical and multinomial distributions
}

To represent a distribution over a finite set of labels, $y \in\{1, \ldots, C\}$, we can use the categorical distribution, which generalizes the Bernoulli to $C>2$ values.

\subsection*{2.5.1 Definition}

The categorical distribution is a discrete probability distribution with one parameter per class:

$$
\operatorname{Cat}(y \mid \boldsymbol{\theta}) \triangleq \prod_{c=1}^{C} \theta_{c}^{\mathbb{I}(y=c)}
$$

In other words, $p(y=c \mid \boldsymbol{\theta})=\theta_{c}$. Note that the parameters are constrained so that $0 \leq \theta_{c} \leq 1$ and $\sum_{c=1}^{C} \theta_{c}=1$; thus there are only $C-1$ independent parameters.

We can write the categorical distribution in another way by converting the discrete variable $y$ into a one-hot vector with $C$ elements, all of which are 0 except for the entry corresponding to the class label. (The term "one-hot" arises from electrical engineering, where binary vectors are encoded as electrical current on a set of wires, which can be active ("hot") or not ("cold").) For example, if $C=3$, we encode the classes 1,2 and 3 as $(1,0,0),(0,1,0)$, and $(0,0,1)$. More generally, we can encode the classes using unit vectors, where $\boldsymbol{e}_{c}$ is all 0 s except for dimension $c$. (This is also called a dummy encoding.) Using one-hot encodings, we can write the categorical distribution as follows:

$$
\operatorname{Cat}(\boldsymbol{y} \mid \boldsymbol{\theta}) \triangleq \prod_{c=1}^{C} \theta_{c}^{y_{c}}
$$

The categorical distribution is a special case of the multinomial distribution. To explain this, suppose we observe $N$ categorical trials, $y_{n} \sim \operatorname{Cat}(\cdot \mid \boldsymbol{\theta})$, for $n=1: N$. Concretely, think of rolling a $C$-sided dice $N$ times. Let us define $\boldsymbol{y}$ to be a vector that counts the number of times each face

Author: Kevin P. Murphy. (C) MIT Press. CC-BY-NC-ND license
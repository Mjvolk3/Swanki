We discuss this in more detail in Section 10.3. For now, we just give an example. Figure 2.13 shows what happens when we fit this model to the 3 -class iris dataset, using just 2 features. We see that the decision boundaries between each class are linear. We can create nonlinear boundaries by transforming the features (e.g., using polynomials), as we discuss in Section 10.3.1.

\title{
2.5.4 Log-sum-exp trick
}

In this section, we discuss one important practical detail to pay attention to when working with the softmax distribution. Suppose we want to compute the normalized probability $p_{c}=p(y=c \mid \boldsymbol{x})$, which is given by

$$
p_{c}=\frac{e^{a_{c}}}{Z(\boldsymbol{a})}=\frac{e^{a_{c}}}{\sum_{c^{\prime}=1}^{C} e^{a_{c^{\prime}}}}
$$

where $\boldsymbol{a}=f(\boldsymbol{x} ; \boldsymbol{\theta})$ are the logits. We might encounter numerical problems when computing the partition function $Z$. For example, suppose we have 3 classes, with logits $\boldsymbol{a}=(0,1,0)$. Then we find $Z=e^{0}+e^{1}+e^{0}=4.71$. But now suppose $\boldsymbol{a}=(1000,1001,1000)$; we find $Z=\infty$, since on a computer, even using 64 bit precision, np. $\exp (1000)=$ inf. Similarly, suppose $\boldsymbol{a}=(-1000,-999,-1000)$; now we find $Z=0$, since np. $\exp (-1000)=0$. To avoid numerical problems, we can use the following identity:

$$
\log \sum_{c=1}^{C} \exp \left(a_{c}\right)=m+\log \sum_{c=1}^{C} \exp \left(a_{c}-m\right)
$$

This holds for any $m$. It is common to use $m=\max _{c} a_{c}$ which ensures that the largest value you exponentiate will be zero, so you will definitely not overflow, and even if you underflow, the answer will be sensible. This is known as the log-sum-exp trick. We use this trick when implementing the lse function:

$$
\operatorname{lse}(\boldsymbol{a}) \triangleq \log \sum_{c=1}^{C} \exp \left(a_{c}\right)
$$

We can use this to compute the probabilities from the logits:

$$
p(y=c \mid \boldsymbol{x})=\exp \left(a_{c}-\operatorname{lse}(\boldsymbol{a})\right)
$$

We can then pass this to the cross-entropy loss, defined in Equation (5.41).

However, to save computational effort, and for numerical stability, it is quite common to modify the cross-entropy loss so that it takes the logits $\boldsymbol{a}$ as inputs, instead of the probability vector $\boldsymbol{p}$. For example, consider the binary case. The CE loss for one example is

$$
\mathcal{L}=-\left[\mathbb{I}(y=0) \log p_{0}+\mathbb{I}(y=1) \log p_{1}\right]
$$

where

$$
\begin{aligned}
& \log p_{1}=\log \left(\frac{1}{1+\exp (-a)}\right)=\log (1)-\log (1+\exp (-a))=0-\operatorname{lse}([0,-a]) \\
& \log p_{0}=0-\operatorname{lse}([0,+a])
\end{aligned}
$$

Draft of "Probabilistic Machine Learning: An Introduction". August 8, 2022
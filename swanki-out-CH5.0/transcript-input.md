![](https://cdn.mathpix.com/cropped/2024_05_26_bf6b853468e691ca09c4g-1.jpg?height=1250&width=1248&top_left_y=215&top_left_x=409

ChatGPT figure/image summary: The image is a cover or a section header from an academic or educational publication, likely a textbook or research paper on the topic of machine learning or neural networks. It features a title that reads "5 Single-layer Networks: Classification," indicating that this section or chapter focuses on single-layer neural networks in the context of classification tasks. The background of the image consists of an abstract, multi-colored swirl pattern that does not convey specific information related to the content but serves as a decorative element.)

In the previous chapter, we explored a class of regression models in which the output variables were linear functions of the model parameters and which can therefore be expressed as simple neural networks having a single layer of weight and bias parameters. We turn now to a discussion of classification problems, and in this chapter, we will focus on an analogous class of models that again can be expressed as single-layer neural networks. These will allow us to introduce many of the key concepts of classification before dealing with more general deep neural networks in later chapters.

The goal in classification is to take an input vector $\mathrm{x} \in \mathbb{R}^{D}$ and assign it to one of $K$ discrete classes $\mathcal{C}_{k}$ where $k=1, \ldots, K$. In the most common scenario, the classes are taken to be disjoint, so that each input is assigned to one and only one class. The input space is thereby divided into decision regions whose boundaries are called decision boundaries or decision surfaces. In this chapter, we consider linear

to class $\mathcal{C}_{1}$ is assigned to class $\mathcal{C}_{2}$ or vice versa. The probability of this occurring is given by

$$
\begin{aligned}
p(\text { mistake }) & =p\left(\mathbf{x} \in \mathcal{R}_{1}, \mathcal{C}_{2}\right)+p\left(\mathbf{x} \in \mathcal{R}_{2}, \mathcal{C}_{1}\right) \\
& =\int_{\mathcal{R}_{1}} p\left(\mathbf{x}, \mathcal{C}_{2}\right) \mathrm{d} \mathbf{x}+\int_{\mathcal{R}_{2}} p\left(\mathbf{x}, \mathcal{C}_{1}\right) \mathrm{d} \mathbf{x}
\end{aligned}
$$

We are free to choose the decision rule that assigns each point $\mathrm{x}$ to one of the two classes. Clearly, to minimize $p$ (mistake) we should arrange that each $\mathbf{x}$ is assigned to whichever class has the smaller value of the integrand in (5.20). Thus, if $p\left(\mathbf{x}, \mathcal{C}_{1}\right)>p\left(\mathbf{x}, \mathcal{C}_{2}\right)$ for a given value of $\mathbf{x}$, then we should assign that $\mathbf{x}$ to class $\mathcal{C}_{1}$. From the product rule of probability, we have $p\left(\mathbf{x}, \mathcal{C}_{k}\right)=p\left(\mathcal{C}_{k} \mid \mathbf{x}\right) p(\mathbf{x})$. Because the factor $p(\mathbf{x})$ is common to both terms, we can restate this result as saying that the minimum probability of making a mistake is obtained if each value of $\mathrm{x}$ is assigned to the class for which the posterior probability $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$ is largest. This result is illustrated for two classes and a single input variable $x$ in Figure 5.5.

For the more general case of $K$ classes, it is slightly easier to maximize the probability of being correct, which is given by

$$
\begin{aligned}
p(\text { correct }) & =\sum_{k=1}^{K} p\left(\mathbf{x} \in \mathcal{R}_{k}, \mathcal{C}_{k}\right) \\
& =\sum_{k=1}^{K} \int_{\mathcal{R}_{k}} p\left(\mathbf{x}, \mathcal{C}_{k}\right) \mathrm{d} \mathbf{x}
\end{aligned}
$$

which is maximized when the regions $\mathcal{R}_{k}$ are chosen such that each $\mathrm{x}$ is assigned to the class for which $p\left(\mathbf{x}, \mathcal{C}_{k}\right)$ is largest. Again, using the product rule $p\left(\mathbf{x}, \mathcal{C}_{k}\right)=$ $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right) p(\mathbf{x})$, and noting that the factor of $p(\mathbf{x})$ is common to all terms, we see that each $\mathrm{x}$ should be assigned to the class having the largest posterior probability $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$.

\title{
5.2.2 Expected loss
}

For many applications, our objective will be more complex than simply minimizing the number of misclassifications. Let us consider again the medical diagnosis problem. We note that, if a patient who does not have cancer is incorrectly diagnosed as having cancer, the consequences may be that they experience some distress plus there is the need for further investigations. Conversely, if a patient with cancer is diagnosed as healthy, the result may be premature death due to lack of treatment. Thus, the consequences of these two types of mistake can be dramatically different. It would clearly be better to make fewer mistakes of the second kind, even if this was at the expense of making more mistakes of the first kind.

We can formalize such issues through the introduction of a loss function, also called a cost function, which is a single, overall measure of loss incurred in taking any of the available decisions or actions. Our goal is then to minimize the total loss incurred. Note that some authors consider instead a utility function, whose value

![](https://cdn.mathpix.com/cropped/2024_05_26_7631da1ff57256b30effg-1.jpg?height=645&width=1258&top_left_y=227&top_left_x=270

ChatGPT figure/image summary: The first image (a) is a schematic illustration showing plots of joint probabilities \( p(x, \mathcal{C}_{1}) \) and \( p(x, \mathcal{C}_{2}) \) against an input variable \( x \). There are two decision regions, \( \mathcal{R}_{1} \) and \( \mathcal{R}_{2} \), with a decision boundary denoted as \( x = \widehat{x} \). The distribution for \( p(x, \mathcal{C}_{1}) \) is shown on the left, and the distribution for \( p(x, \mathcal{C}_{2}) \) is on the right.

In the regions where these distributions overlap, there's a potential for classification error. The red double-headed arrow indicates that by varying the location of the decision boundary, one can manage the classification errors differently. The red, green, and blue shaded areas represent regions where classification errors occur: red for the region where \( \mathcal{C}_{2} \) is incorrectly assigned to \( \mathcal{R}_{1} \), green for the overlap where either misclassification can occur, and blue where \( \mathcal{C}_{1} \) is incorrectly assigned to \( \mathcal{R}_{2} \).

This illustration supports the textual explanation of how to minimize the probability of making classification mistakes by assigning each point \( x \) to the class with the larger value of the probability density function at that point.

The second image (b) shows the same schematic after the decision boundary has been optimized. It appears at \( x = x_{0} \), where the two probability distributions cross. This point of intersection is where the decision boundary minimizes the misclassification errors (the red region disappears). The decision rule here would assign values of \( x \geqslant x_{0} \) to class \( \mathcal{C}_{2} \) (region \( \mathcal{R}_{2} \)) and values of \( x < x_{0} \) to class \( \mathcal{C}_{1} \) (region \( \mathcal{R}_{1} \)), corresponding to the highest posterior probability \( p(\mathcal{C}_{k} | x) \) for each \( x \).)

(a)

![](https://cdn.mathpix.com/cropped/2024_05_26_7631da1ff57256b30effg-1.jpg?height=652&width=1255&top_left_y=959&top_left_x=271

ChatGPT figure/image summary: This image displays a schematic representation of two probability distribution curves plotted against a single input variable, denoted by \( x \). The curves are labeled as \( p(x, \mathcal{C}_{1}) \) and \( p(x, \mathcal{C}_{2}) \), indicating the joint probability distributions for two classes, \(\mathcal{C}_{1}\) and \(\mathcal{C}_{2}\), based on the variable \( x \). There is a vertical line marking a decision boundary at a value of \( x \) denoted by \( \widehat{x} \). The decision boundary divides the space into two decision regions: \( \mathcal{R}_{1} \) to the left of \( \widehat{x} \) and \( \mathcal{R}_{2} \) to the right of \( \widehat{x} \).

The shaded regions under the curves represent areas where classification errors occur. For example, the green shaded area is the error due to instances from class \(\mathcal{C}_{2}\) incorrectly classified as \(\mathcal{C}_{1}\), and the blue shaded area is the error due to instances from class \(\mathcal{C}_{1}\) being misclassified as \(\mathcal{C}_{2}\). The optimal decision boundary is chosen to minimize these errors.

This illustration is typically used in the context of binary classification problems in statistics and machine learning, where the goal is to find the best decision boundary that separates the two classes with minimal classification error. The exact position of \( \widehat{x} \) is determined based on the distributions and by using the probabilistic criteria described in the contextual paper information provided.)

(b)

Figure 5.5 Schematic illustration of the joint probabilities $p\left(x, \mathcal{C}_{k}\right)$ for each of two classes plotted against $x$, together with the decision boundary $x=\widehat{x}$. Values of $x \geqslant \widehat{x}$ are classified as class $\mathcal{C}_{2}$ and hence belong to decision region $\mathcal{R}_{2}$, whereas points $x<\widehat{x}$ are classified as $\mathcal{C}_{1}$ and belong to $\mathcal{R}_{1}$. Errors arise from the blue, green, and red regions, so that for $x<\widehat{x}$, the errors are due to points from class $\mathcal{C}_{2}$ being misclassified as $\mathcal{C}_{1}$ (represented by the sum of the red and green regions). Conversely for points in the region $x \geqslant \widehat{x}$, the errors are due to points from class $\mathcal{C}_{1}$ being misclassified as $\mathcal{C}_{2}$ (represented by the blue region). By varying the location $\widehat{x}$ of the decision boundary, as indicated by the red double-headed arrow in (a), the combined areas of the blue and green regions remains constant, whereas the size of the red region varies. The optimal choice for $\widehat{x}$ is where the curves for $p\left(x, \mathcal{C}_{1}\right)$ and $p\left(x, \mathcal{C}_{2}\right)$ cross, as shown in (b) and corresponding to $\widehat{x}=x_{0}$, because in this case the red region disappears. This is equivalent to the minimum misclassification rate decision rule, which assigns each value of $x$ to the class having the higher posterior probability $p\left(\mathcal{C}_{k} \mid x\right)$.

Figure 5.6 An example of a loss matrix with elements $L_{k j}$ for the cancer treatment problem. The rows correspond to the true class, whereas the columns correspond to the assignment of class made by our decision criterion. $\left.\begin{array}{l}\text { normal } \\ \text { cancer }\end{array} \begin{array}{cc}\text { cancer } \\ 0 & 1 \\ 100 & 0\end{array}\right)$

they aim to maximize. These are equivalent concepts if we take the utility to be simply the negative of the loss. Throughout this text we will use the loss function convention. Suppose that, for a new value of $\mathbf{x}$, the true class is $\mathcal{C}_{k}$ and that we assign $\mathrm{x}$ to class $\mathcal{C}_{j}$ (where $j$ may or may not be equal to $k$ ). In so doing, we incur some level of loss that we denote by $L_{k j}$, which we can view as the $k, j$ element of a loss matrix. For instance, in our cancer example, we might have a loss matrix of the form shown in Figure 5.6. This particular loss matrix says that there is no loss incurred if the correct decision is made, there is a loss of 1 if a healthy patient is diagnosed as having cancer, whereas there is a loss of 100 if a patient having cancer is diagnosed as healthy.

The optimal solution is the one that minimizes the loss function. However, the loss function depends on the true class, which is unknown. For a given input vector x, our uncertainty in the true class is expressed through the joint probability distribution $p\left(\mathbf{x}, \mathcal{C}_{k}\right)$, and so we seek instead to minimize the average loss, where the average is computed with respect to this distribution and is given by

$$
\mathbb{E}[L]=\sum_{k} \sum_{j} \int_{\mathcal{R}_{j}} L_{k j} p\left(\mathbf{x}, \mathcal{C}_{k}\right) \mathrm{d} \mathbf{x}
$$

Each $\mathrm{x}$ can be assigned independently to one of the decision regions $\mathcal{R}_{j}$. Our goal is to choose the regions $\mathcal{R}_{j}$ to minimize the expected loss (5.22), which implies that for each $\mathbf{x}$, we should minimize $\sum_{k} L_{k j} p\left(\mathbf{x}, \mathcal{C}_{k}\right)$. As before, we can use the product rule $p\left(\mathbf{x}, \mathcal{C}_{k}\right)=p\left(\mathcal{C}_{k} \mid \mathbf{x}\right) p(\mathbf{x})$ to eliminate the common factor of $p(\mathbf{x})$. Thus, the decision rule that minimizes the expected loss assigns each new $\mathbf{x}$ to the class $j$ for which the quantity

$$
\sum_{k} L_{k j} p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)
$$

is a minimum. Once we have chosen values for the loss matrix elements $L_{k j}$, this is clearly trivial to do.

\title{
5.2.3 The reject option
}

We have seen that classification errors arise from the regions of input space where the largest of the posterior probabilities $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$ is significantly less than unity or equivalently where the joint distributions $p\left(\mathbf{x}, \mathcal{C}_{k}\right)$ have comparable values. These are the regions where we are relatively uncertain about class membership. In some applications, it will be appropriate to avoid making decisions on the difficult cases in anticipation of obtaining a lower error rate on those examples for which a classification decision is made. This is known as the reject option. For example, in our hypothetical cancer screening example, it may be appropriate to use an automatic

Figure 5.7 Illustration of the reject option. Inputs $x$ such that the larger of the two posterior probabilities is less than or equal to some threshold $\theta$ will be rejected.

![](https://cdn.mathpix.com/cropped/2024_05_26_49629de898dc2113d75dg-1.jpg?height=523&width=672&top_left_y=215&top_left_x=973

ChatGPT figure/image summary: The image is a graph showing two posterior probability curves for two different classes, labeled \( p(C_1|x) \) and \( p(C_2|x) \), as functions of a single continuous input variable \( x \). There are two vertical lines where the curves intersect the threshold \( \theta \), which is represented by a horizontal dashed line. Below the threshold \( \theta \), there is a region labeled as "reject region," indicating the range of values of \( x \) for which the classifier would choose not to make a decision because the highest posterior probability is not greater than the threshold \( \theta \). This introduces a mechanism to deal with uncertainty in classification, where rather than forcing a possibly incorrect classification, the decision is deferred for further analysis or additional information.)

system to classify those images for which there is little doubt as to the correct class, while requesting a biopsy to classify the more ambiguous cases. We can achieve this by introducing a threshold $\theta$ and rejecting those inputs $\mathbf{x}$ for which the largest of the posterior probabilities $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$ is less than or equal to $\theta$. This is illustrated for two classes and a single continuous input variable $x$ in Figure 5.7. Note that setting $\theta=1$ will ensure that all examples are rejected, whereas if there are $K$ classes, then setting $\theta<1 / K$ will ensure that no examples are rejected. Thus, the fraction of examples that are rejected is controlled by the value of $\theta$.

We can easily extend the reject criterion to minimize the expected loss, when a loss matrix is given, by taking account of the loss incurred when a reject decision is made.

\title{
5.2.4 Inference and decision
}

We have broken the classification problem down into two separate stages, the inference stage in which we use training data to learn a model for $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$ and the subsequent decision stage in which we use these posterior probabilities to make optimal class assignments. An alternative possibility would be to solve both problems together and simply learn a function that maps inputs $\mathbf{x}$ directly into decisions. Such a function is called a discriminant function.

In fact, we can identify three distinct approaches to solving decision problems, all of which have been used in practical applications. These are, in decreasing order of complexity, as follows:

(a) First, solve the inference problem of determining the class-conditional densities $p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)$ for each class $\mathcal{C}_{k}$ individually. Separately infer the prior class probabilities $p\left(\mathcal{C}_{k}\right)$. Then use Bayes' theorem in the form

$$
p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)=\frac{p\left(\mathbf{x} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right)}{p(\mathbf{x})}
$$

to find the posterior class probabilities $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$. As usual, the denominator in

Bayes' theorem can be found in terms of the quantities in the numerator, using

$$
p(\mathbf{x})=\sum_{k} p\left(\mathbf{x} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right)
$$

Equivalently, we can model the joint distribution $p\left(\mathbf{x}, \mathcal{C}_{k}\right)$ directly and then normalize to obtain the posterior probabilities. Having found the posterior probabilities, we use decision theory to determine the class membership for each new input $\mathbf{x}$. Approaches that explicitly or implicitly model the distribution of inputs as well as outputs are known as generative models, because by sampling from them, it is possible to generate synthetic data points in the input space.

(b) First, solve the inference problem of determining the posterior class probabilities $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$, and then subsequently use decision theory to assign each new $\mathbf{x}$ to one of the classes. Approaches that model the posterior probabilities directly are called discriminative models.

(c) Find a function $f(\mathbf{x})$, called a discriminant function, that maps each input $\mathbf{x}$ directly onto a class label. For instance, for two-class problems, $f(\cdot)$ might be binary valued and such that $f=0$ represents class $\mathcal{C}_{1}$ and $f=1$ represents class $\mathcal{C}_{2}$. In this case, probabilities play no role.

Let us consider the relative merits of these three alternatives. Approach (a) is the most demanding because it involves finding the joint distribution over both $\mathrm{x}$ and $\mathcal{C}_{k}$. For many applications, $\mathrm{x}$ will have high dimensionality, and consequently, we may need a large training set to be able to determine the class-conditional densities to reasonable accuracy. Note that the class priors $p\left(\mathcal{C}_{k}\right)$ can often be estimated simply from the fractions of the training set data points in each of the classes. One advantage of approach (a), however, is that it also allows the marginal density of data $p(\mathbf{x})$ to be determined from (5.25). This can be useful for detecting new data points that have low probability under the model and for which the predictions may be of low accuracy, which is known as outlier detection or novelty detection (Bishop, 1994; Tarassenko, 1995).

However, if we wish only to make classification decisions, then it can be wasteful of computational resources and excessively demanding of data to find the joint distribution $p\left(\mathbf{x}, \mathcal{C}_{k}\right)$ when in fact we really need only the posterior probabilities $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$, which can be obtained directly through approach (b). Indeed, the classconditional densities may contain a significant amount of structure that has little effect on the posterior probabilities, as illustrated in Figure 5.8. There has been much interest in exploring the relative merits of generative and discriminative approaches to machine learning and in finding ways to combine them (Jebara, 2004; Lasserre, Bishop, and Minka, 2006).

An even simpler approach is (c) in which we use the training data to find a discriminant function $f(\mathbf{x})$ that maps each $\mathbf{x}$ directly onto a class label, thereby combining the inference and decision stages into a single learning problem. In the example of Figure 5.8, this would correspond to finding the value of $x$ shown by


![](https://cdn.mathpix.com/cropped/2024_05_26_3a79e15ed1a634320c5fg-1.jpg?height=702&width=1494&top_left_y=235&top_left_x=147

ChatGPT figure/image summary: The image depicts two plots related to a binary classification problem in the context of probabilistic models for machine learning. 

On the left plot, we see the class-conditional densities \( p(x|\mathcal{C}_1) \) and \( p(x|\mathcal{C}_2) \) for two classes \( \mathcal{C}_1 \) and \( \mathcal{C}_2 \) with respect to a single input variable \( x \). The plot illustrates two probability density functions, one for each class. The density for \( \mathcal{C}_1 \) is shown in blue and has two modes, indicating two regions where samples from class \( \mathcal{C}_1 \) are more concentrated. The density for \( \mathcal{C}_2 \) is shown in red and has one mode, suggesting a single region of higher density for samples from class \( \mathcal{C}_2 \).

On the right plot, we see the corresponding posterior probabilities \( p(\mathcal{C}_1|x) \) and \( p(\mathcal{C}_2|x) \) as a function of \( x \). The blue curve represents the posterior probability for class \( \mathcal{C}_1 \) and the red curve for class \( \mathcal{C}_2 \). The green vertical line represents the decision boundary, which is the value of \( x \) that minimizes misclassification rate. According to the plot, if the value of \( x \) is to the left of the green line, the decision would favor class \( \mathcal{C}_1 \), while if it's to the right, the decision would favor class \( \mathcal{C}_2 \).

The decision boundary is chosen based on the assumption that the prior probabilities of both classes are equal. The figure is used to explain the concept of decision boundaries in the context of discriminative models and illustrates that certain features of the class-conditional densities may not affect the posterior probabilities and hence the decision boundary.)

Figure 5.8 Example of the class-conditional densities for two classes having a single input variable $x$ (left plot) together with the corresponding posterior probabilities (right plot). Note that the left-hand mode of the class-conditional density $p\left(\mathbf{x} \mid \mathcal{C}_{1}\right)$, shown in blue on the left plot, has no effect on the posterior probabilities. The vertical green line in the right plot shows the decision boundary in $x$ that gives the minimum misclassification rate, assuming the prior class probabilities, $p\left(\mathcal{C}_{1}\right)$ and $p\left(\mathcal{C}_{2}\right)$, are equal.

the vertical green line, because this is the decision boundary giving the minimum probability of misclassification.

With option (c), however, we no longer have access to the posterior probabilities $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$. There are many powerful reasons for wanting to compute the posterior probabilities, even if we subsequently use them to make decisions. These include:

Minimizing risk. Consider a problem in which the elements of the loss matrix are subjected to revision from time to time (such as might occur in a financial application). If we know the posterior probabilities, we can trivially revise the minimum risk decision criterion by modifying (5.23) appropriately. If we have only a discriminant function, then any change to the loss matrix would require that we return to the training data and solve the inference problem afresh.

Reject option. Posterior probabilities allow us to determine a rejection criterion that will minimize the misclassification rate, or more generally the expected loss, for a given fraction of rejected data points.

Section 2.1.1

Compensating for class priors. Consider our cancer screening example again, and suppose that we have collected a large number of images from the general population for use as training data, which we use to build an automated screening system. Because cancer is rare amongst the general population, we might find that, say, only 1 in every 1,000 examples corresponds to the presence of cancer.

If we used such a data set to train an adaptive model, we could run into severe difficulties due to the small proportion of those in the cancer class. For instance, a classifier that assigned every point to the normal class would achieve $99.9 \%$ accuracy, and it may be difficult to avoid this trivial solution. Also, even a large data set will contain very few examples of skin images corresponding to cancer, and so the learning algorithm will not be exposed to a broad range of examples of such images and hence is not likely to generalize well. A balanced data set with equal numbers of examples from each of the classes would allow us to find a more accurate model. However, we then have to compensate for the effects of our modifications to the training data. Suppose we have used such a modified data set and found models for the posterior probabilities. From Bayes' theorem (5.24), we see that the posterior probabilities are proportional to the prior probabilities, which we can interpret as the fractions of points in each class. We can therefore simply take the posterior probabilities obtained from our artificially balanced data set, divide by the class fractions in that data set, and then multiply by the class fractions in the population to which we wish to apply the model. Finally, we need to normalize to ensure that the new posterior probabilities sum to one. Note that this procedure cannot be applied if we have learned a discriminant function directly instead of determining posterior probabilities.

Combining models. For complex applications, we may wish to break the problem into a number of smaller sub-problems each of which can be tackled by a separate module. For example, in our hypothetical medical diagnosis problem, we may have information available from, say, blood tests as well as skin images. Rather than combine all of this heterogeneous information into one huge input space, it may be more effective to build one system to interpret the images and a different one to interpret the blood data. If each of the two models gives posterior probabilities for the classes, then we can combine the outputs systematically using the rules of probability. One simple way to do this is to assume that, for each class separately, the distributions of inputs for the images, denoted by $\mathbf{x}_{\mathrm{I}}$, and the blood data, denoted by $\mathbf{x}_{\mathrm{B}}$, are independent, so that

$$
p\left(\mathbf{x}_{\mathrm{I}}, \mathbf{x}_{\mathrm{B}} \mid \mathcal{C}_{k}\right)=p\left(\mathbf{x}_{\mathrm{I}} \mid \mathcal{C}_{k}\right) p\left(\mathbf{x}_{\mathrm{B}} \mid \mathcal{C}_{k}\right)
$$

Section 11.2

This is an example of a conditional independence property, because the independence holds when the distribution is conditioned on the class $\mathcal{C}_{k}$. The posterior probability, given both the image and blood data, is then given by

$$
\begin{aligned}
p\left(\mathcal{C}_{k} \mid \mathbf{x}_{\mathrm{I}}, \mathbf{x}_{\mathrm{B}}\right) & \propto p\left(\mathbf{x}_{\mathrm{I}}, \mathbf{x}_{\mathrm{B}} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right) \\
& \propto p\left(\mathbf{x}_{\mathrm{I}} \mid \mathcal{C}_{k}\right) p\left(\mathbf{x}_{\mathrm{B}} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right) \\
& \propto \frac{p\left(\mathcal{C}_{k} \mid \mathbf{x}_{\mathrm{I}}\right) p\left(\mathcal{C}_{k} \mid \mathbf{x}_{\mathrm{B}}\right)}{p\left(\mathcal{C}_{k}\right)}
\end{aligned}
$$

Thus, we need the class prior probabilities $p\left(\mathcal{C}_{k}\right)$, which we can easily estimate from the fractions of data points in each class, and then we need to normalize

Figure 5.9 The confusion matrix for the cancer treatment problem, in which the rows correspond to the true class and the columns correspond to the assignment of class made by our decision criterion. The elements of the matrix show the numbers of true negatives, false positives, false negatives, and true positives.

![](https://cdn.mathpix.com/cropped/2024_05_26_fc1c9f1146b37661bb76g-1.jpg?height=141&width=435&top_left_y=230&top_left_x=1050

ChatGPT figure/image summary: The image displays a confusion matrix, which is a specific table layout to visualize the performance of an algorithm, usually a classifier on a set of test data for which the true values are known. The rows of the matrix are labeled with the true class categories, while the columns are labeled with predicted class categories made by the classifier. In this context, the classification task relates to a medical diagnosis problem, specifically cancer screening.

The confusion matrix consists of four different categories:

- True Negatives (TN): The number of instances correctly identified as 'normal' (no cancer).
- False Positives (FP): The number of instances incorrectly classified as 'cancer' when they are actually 'normal'.
- False Negatives (FN): The number of instances incorrectly classified as 'normal' when they are actually 'cancer'.
- True Positives (TP): The number of instances correctly identified as 'cancer'.

These values are fundamental in computing various performance metrics for the classifier, such as accuracy, precision, recall, and the ROC curve as mentioned in the provided text. The matrix is a powerful tool for understanding not only the overall accuracy of the classifier but also how it errs, by providing details on the types of errors it makes (type 1 or type 2 errors).)

Section 11.2 .3

Chapter 7

Section 2.1.1 the resulting posterior probabilities so they sum to one. The particular conditional independence assumption (5.26) is an example of a naive Bayes model. Note that the joint marginal distribution $p\left(\mathbf{x}_{\mathrm{I}}, \mathbf{x}_{\mathrm{B}}\right)$ will typically not factorize under this model. We will see in later chapters how to construct models for combining data that do not require the conditional independence assumption (5.26). A further advantage of using models that output probabilities rather than decisions is that they can easily be made differentiable with respect to any adjustable parameters (such as the weight coefficients in the polynomial regression example), which allows them to be composed and trained jointly using gradient-based optimization methods.

\subsection*{5.2.5 Classifier accuracy}

The simplest measure of performance for a classifier is the fraction of test set points that are correctly classified. However, we have seen that different types of error can have different consequences, as expressed through the loss matrix, and often we therefore do not simply wish to minimize the number of misclassifications. By changing the location of the decision boundary, we can make trade-offs between different kinds of error, for example with the goal of minimizing an expected loss. Because this is such an important concept, we will introduce some definitions and terminology so that the performance of a classifier can be better characterized.

We will consider again our cancer screening example. For each person tested, there is a 'true label' of whether they have cancer or not, and there is also the prediction made by the classifier. If, for a particular person, the classifier predicts cancer and this is in fact the true label, then the prediction is called a true positive. However, if the person does not have cancer it is a false positive. Likewise, if the classifier predicts that a person does not have cancer and this is correct, then the prediction is called a true negative, otherwise it is a false negative. The false positives are also known as type 1 errors whereas the false negatives are called type 2 errors. If $N$ is the total number of people taking the test, then $N_{\mathrm{TP}}$ is the number of true positives, $N_{\mathrm{FP}}$ is the number of false positives, $N_{\mathrm{TN}}$ is the number of true negatives, and $N_{\mathrm{FN}}$ is the number of false negatives, where

$$
N=N_{\mathrm{TP}}+N_{\mathrm{FP}}+N_{\mathrm{TN}}+N_{\mathrm{FN}}
$$

This can be represented as a confusion matrix as shown in Figure 5.9. Accuracy, measured by the fraction of correct classifications, is then given by

$$
\text { Accuracy }=\frac{N_{\mathrm{TP}}+N_{\mathrm{TN}}}{N_{\mathrm{TP}}+N_{\mathrm{FP}}+N_{\mathrm{TN}}+N_{\mathrm{FN}}}
$$

We can see that accuracy can be misleading if there are strongly imbalanced classes. In our cancer screening example, for instance, where only 1 person in 1,000 has cancer, a naive classifier that simply decides that nobody has cancer will achieve $99.9 \%$ accuracy and yet is completely useless.

Several other quantities can be defined in terms of these numbers, of which the most commonly encountered are

$$
\begin{aligned}
\text { Precision } & =\frac{N_{\mathrm{TP}}}{N_{\mathrm{TP}}+N_{\mathrm{FP}}} \\
\text { Recall } & =\frac{N_{\mathrm{TP}}}{N_{\mathrm{TP}}+N_{\mathrm{FN}}} \\
\text { False positive rate } & =\frac{N_{\mathrm{FP}}}{N_{\mathrm{FP}}+N_{\mathrm{TN}}} \\
\text { False discovery rate } & =\frac{N_{\mathrm{FP}}}{N_{\mathrm{FP}}+N_{\mathrm{TP}}}
\end{aligned}
$$

In our cancer screening example, precision represents an estimate of the probability that a person who has a positive test does indeed have cancer, whereas recall is an estimate of the probability that a person who has cancer is correctly detected by the test. The false positive rate is an estimate of the probability that a person who is normal will be classified as having cancer, whereas the false discovery rate represents the fraction of those testing positive who do not in fact have cancer.

By altering the location of the decision boundary, we can change the trade-offs between the two kinds of errors. To understand this trade-off, we revisit Figure 5.5, but now we label the various regions as shown in Figure 5.10. We can relate the labelled regions to the various true and false rates as follows:

$$
\begin{aligned}
& N_{\mathrm{FP}} / N=E \\
& N_{\mathrm{TP}} / N=D+E \\
& N_{\mathrm{FN}} / N=B+C \\
& N_{\mathrm{TN}} / N=A+C
\end{aligned}
$$

where we are implicitly considering the limit $N \rightarrow \infty$ so that we can relate number of observations to probabilities.

\title{
5.2.6 ROC curve
}

A probabilistic classifier will output a posterior probability, which can be converted to a decision by setting a threshold. As the value of the threshold is varied, we can reduce type 1 errors at the expense of increasing type 2 errors, or vice versa. To better understand this trade-off, it is useful to plot the receiver operating characteristic or ROC curve (Fawcett, 2006), a name that originates from procedures to measure the performance of radar receivers. This is a graph of true positive rate versus false positive rate, as shown in Figure 5.11.

As the decision boundary in Figure 5.10 is moved from $-\infty$ to $\infty$, the ROC curve is traced out and can then be generated by plotting the cumulative fraction of

![](https://cdn.mathpix.com/cropped/2024_05_26_98bfcfce09fd11208616g-1.jpg?height=657&width=1275&top_left_y=214&top_left_x=254

ChatGPT figure/image summary: The image depicts a graph with two overlapping probability density functions (pdfs), one for each of two classes, C1 and C2. The x-axis represents the value of a variable x, which could be a measurement or feature used in a classification task, such as the result of a cancer screening test. The two classes represent the possible outcomes; for example, C1 might be 'normal' and C2 might be 'cancer'.

On the graph, there are five regions, A, B, C, D, and E, which correspond to different classification decisions and outcomes:

- Region A represents the area under the pdf for class C1 to the left of the decision boundary \( x_0 \). These are true negatives (TN), where instances of class C1 are correctly identified.
- Region B represents the overlap area to the left of the decision boundary between the two pdfs and corresponds to false negatives (FN). These are instances of class C2 that are incorrectly classified as class C1.
- Region C represents the overlap area to the right of the decision boundary between the two pdfs and corresponds to false positives (FP). These are instances of class C1 that are incorrectly classified as class C2.
- Region D represents the area under the pdf for class C2 that overlaps with the decision region \( \mathcal{R}_2 \) and corresponds to true positives (TP). These are instances of class C2 that are correctly identified.
- Region E represents the area under the pdf for class C2 to the right of the decision boundary. These are instances from class C2 that are correctly identified as such; it's an extension of the true positive area.
  
The decision boundary at \( x_0 \) separates the classification regions \( \mathcal{R}_1 \) and \( \mathcal{R}_2 \), where \( \mathcal{R}_1 \) is assigned to class C1 and \( \mathcal{R}_2 \) is assigned to class C2.

Two arrows indicate the range of values for which probabilities are calculated in their respective regions—class C1 to the left and class C2 to the right of \( x_0 \). The decision boundary and the assignment of regions can be adjusted to trade-off between false positives and false negatives, which would alter the shapes and sizes of the regions B, C, D, and E.

This type of graph is commonly used to illustrate the concept)

Figure 5.10 As in Figure 5.5, with the various regions labelled. In the cancer classification problem, region $\mathcal{R}_{1}$ is assigned to the normal class whereas region $\mathcal{R}_{2}$ is assigned to the cancer class.

correct detection of cancer on the $y$-axis versus the cumulative fraction of incorrect detection on the $x$-axis. Note that a specific confusion matrix represents one point along the ROC curve. The best possible classifier would be represented by a point at the top left corner of the ROC diagram. The bottom left corner represents a simple classifier that assigns every point to the normal class and therefore has no true positives but also no false positives. Similarly, the top right corner represents a classifier that assigns everything to the cancer class and therefore has no false negatives but also no true negatives. In Figure 5.11, the classifiers represented by the blue curve are better than those of the red curve for any choice of, say, false positive rate. It is also possible, however, for such curves to cross over, in which case the choice of which is better will depend on the choice of operating point.

As a baseline, we can consider a random classifier that simply assigns each data point to cancer with probability $\rho$ and to normal with probability $1-\rho$. As we vary the value of $\rho$ it will trace out an ROC curve given by a diagonal straight line, as shown in Figure 5.11. Any classifier below the diagonal line performs worse than random guessing.

Sometimes it is useful to have a single number that characterises the whole ROC curve. One approach is to measure the area under the curve (AUC). A value of 0.5 for the AUC represents random guessing whereas a value of 1.0 represents a perfect classifier.

Another measure is the $F$-score, which is the geometric mean of precision and

models for classification, by which we mean that the decision surfaces are linear functions of the input vector $\mathbf{x}$ and, hence, are defined by $(D-1)$-dimensional hyperplanes within the $D$-dimensional input space. Data sets whose classes can be separated exactly by linear decision surfaces are said to be linearly separable. Linear classification models can be applied to data sets that are not linearly separable, although not all inputs will be correctly classified.

We can broadly identify three distinct approaches to solving classification problems. The simplest involves constructing a discriminant function that directly assigns each vector $\mathrm{x}$ to a specific class. A more powerful approach, however, models the conditional probability distributions $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$ in an inference stage and subsequently uses these distributions to make optimal decisions. Separating inference and decision brings numerous benefits. There are two different approaches to determining the conditional probabilities $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$. One technique is to model them directly, for example by representing them as parametric models and then optimizing the parameters using a training set. This will be called a discriminative probabilistic model. Alternatively, we can model the class-conditional densities $p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)$, together with the prior probabilities $p\left(\mathcal{C}_{k}\right)$ for the classes, and then compute the required posterior probabilities using Bayes' theorem:

$$
p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)=\frac{p\left(\mathbf{x} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right)}{p(\mathbf{x})}
$$

This will be called a generative probabilistic model because it offers the opportunity to generate samples from each of the class-conditional densities $p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)$. In this chapter, we will discuss examples of all three approaches: discriminant functions, generative probabilistic models, and discriminative probabilistic models.

\title{
5.1. Discriminant Functions
}

A discriminant is a function that takes an input vector $\mathbf{x}$ and assigns it to one of $K$ classes, denoted $\mathcal{C}_{k}$. In this chapter, we will restrict attention to linear discriminants, namely those for which the decision surfaces are hyperplanes. To simplify the discussion, we consider first two classes and then investigate the extension to $K>2$ classes.

\subsection*{5.1.1 Two classes}

The simplest representation of a linear discriminant function is obtained by taking a linear function of the input vector so that

$$
y(\mathbf{x})=\mathbf{w}^{\mathrm{T}} \mathbf{x}+w_{0}
$$

where $\mathbf{w}$ is called a weight vector, and $w_{0}$ is a bias (not to be confused with bias in the statistical sense). An input vector $\mathbf{x}$ is assigned to class $\mathcal{C}_{1}$ if $y(\mathbf{x}) \geqslant 0$ and to class $\mathcal{C}_{2}$ otherwise. The corresponding decision boundary is therefore defined by the relation $y(\mathbf{x})=0$, which corresponds to a $(D-1)$-dimensional hyperplane within

Figure 5.11 The receiver operator characteristic (ROC) curve is a plot of true positive rate against false positive rate, and it characterizes the trade-off between type 1 and type 2 errors in a classification problem. The upper blue curve represents a better classifier than the lower red curve. Here the dashed curve represents the performance of a simple random classifier.

![](https://cdn.mathpix.com/cropped/2024_05_26_1cbadc682ee2a0381817g-1.jpg?height=704&width=711&top_left_y=212&top_left_x=934

ChatGPT figure/image summary: The image displays a Receiver Operating Characteristic (ROC) curve, which is a graphical plot that illustrates the diagnostic ability of a binary classifier system as its discrimination threshold is varied. The curve is a plot of the True Positive Rate (TPR) against the False Positive Rate (FPR) at various threshold settings.

The ROC curve features two lines:
- The blue curve represents a hypothetical classifier that is superior to random guessing. It shows how the true positive rate increases with the false positive rate but is consistently higher than what would be expected by chance. The better performance is indicated by the greater area under this curve compared to the dashed line.
- The red curve represents another hypothetical classifier that shows a performance between random guessing and the blue curve. It represents a lower true positive rate for the same false positive rate compared to the blue curve.

The dashed line represents the performance of a random classifier. It has a slope of 1, indicating an equal true positive rate and false positive rate at all thresholds. This line serves as a baseline to show the minimum expectation of a classifier; any meaningful classifier should strive to achieve performance above this line.

There are no axis labels or titles visible in the image, but based on the given description, we can interpret that the x-axis is the false positive rate and the y-axis is the true positive rate, both ranging from 0 to 1. The area under each curve (AUC) can be used to quantify the overall performance of the respective classifiers; a higher AUC indicates a better overall performance.)

recall, and is therefore defined by

$$
\begin{aligned}
F & =\frac{2 \times \text { precision } \times \text { recall }}{\text { precision }+ \text { recall }} \\
& =\frac{2 N_{\mathrm{TP}}}{2 N_{\mathrm{TP}}+N_{\mathrm{FP}}+N_{\mathrm{FN}}}
\end{aligned}
$$

Of course, we can also combine the confusion matrix in Figure 5.9 with the loss matrix in Figure 5.6 to compute the expected loss by multiplying the elements pointwise and summing the resulting products.

Although the ROC curve can be extended to more than two classes, it rapidly becomes cumbersome as the number of classes increases.

\title{
5.3. Generative Classifiers
}

We turn next to a probabilistic view of classification and show how models with linear decision boundaries arise from simple assumptions about the distribution of the data. We have already discussed the distinction between the discriminative and the generative approaches to classification. Here we will adopt a generative approach in which we model the class-conditional densities $p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)$ as well as the class priors $p\left(\mathcal{C}_{k}\right)$ and then use these to compute posterior probabilities $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$ through Bayes' theorem.

First, consider problems having two classes. The posterior probability for class

Figure 5.12 Plot of the logistic sigmoid function $\sigma(a)$ defined by (5.42), shown in red, together with the scaled probit function $\Phi(\lambda a)$, for $\lambda^{2}=\pi / 8$, shown in dashed blue, where $\Phi(a)$ is defined by (5.86). The scaling factor $\pi / 8$ is chosen so that the derivatives of the two curves are equal for $a=0$.

![](https://cdn.mathpix.com/cropped/2024_05_26_ecc13ea52b1adcd44cf9g-1.jpg?height=498&width=726&top_left_y=230&top_left_x=917

ChatGPT figure/image summary: This image depicts two curves on a Cartesian coordinate system. On the horizontal axis, we have the values ranging approximately from -7 to 7, and on the vertical axis, the values range from 0 to 1. The solid red curve represents the logistic sigmoid function, σ(a), which is an S-shaped curve that rises from near 0 on the left to approach 1 on the right. The dashed blue curve, which closely follows the red curve, represents a scaled probit function, Φ(λa), with the scaling factor λ² = π/8, where λ² is chosen such that the derivatives of both curves are equal at a = 0.

This sigmoid function transforms its input into a value between 0 and 1, which is useful for representing probabilities in classification algorithms. It shows how the input value, a, affects the output of the function, starting at very low values when a is negative and large in magnitude, and approaching 1 as a becomes positive and large. This function is often used in binary classification to delineate the probability of the input belonging to a particular class.)

$\mathcal{C}_{1}$ can be written as

$$
\begin{aligned}
p\left(\mathcal{C}_{1} \mid \mathbf{x}\right) & =\frac{p\left(\mathbf{x} \mid \mathcal{C}_{1}\right) p\left(\mathcal{C}_{1}\right)}{p\left(\mathbf{x} \mid \mathcal{C}_{1}\right) p\left(\mathcal{C}_{1}\right)+p\left(\mathbf{x} \mid \mathcal{C}_{2}\right) p\left(\mathcal{C}_{2}\right)} \\
& =\frac{1}{1+\exp (-a)}=\sigma(a)
\end{aligned}
$$

where we have defined

$$
a=\ln \frac{p\left(\mathbf{x} \mid \mathcal{C}_{1}\right) p\left(\mathcal{C}_{1}\right)}{p\left(\mathbf{x} \mid \mathcal{C}_{2}\right) p\left(\mathcal{C}_{2}\right)}
$$

and $\sigma(a)$ is the logistic sigmoid function defined by

$$
\sigma(a)=\frac{1}{1+\exp (-a)}
$$

which is plotted in Figure 5.12. The term 'sigmoid' means S-shaped. This type of function is sometimes also called a 'squashing function' because it maps the whole real axis into a finite interval. The logistic sigmoid has been encountered already in earlier chapters and plays an important role in many classification algorithms. It satisfies the following symmetry property:

$$
\sigma(-a)=1-\sigma(a)
$$

as is easily verified. The inverse of the logistic sigmoid is given by

$$
a=\ln \left(\frac{\sigma}{1-\sigma}\right)
$$

and is known as the logit function. It represents the log of the ratio of probabilities $\ln \left[p\left(\mathcal{C}_{1} \mid \mathbf{x}\right) / p\left(\mathcal{C}_{2} \mid \mathbf{x}\right)\right]$ for the two classes, also known as the log odds.

Note that in (5.40), we have simply rewritten the posterior probabilities in an equivalent form, and so the appearance of the logistic sigmoid may seem artificial.

However, it will have significance provided $a(\mathbf{x})$ has a constrained functional form. We will shortly consider situations in which $a(\mathbf{x})$ is a linear function of $\mathbf{x}$, in which case the posterior probability is governed by a generalized linear model.

If there are $K>2$ classes, we have

$$
\begin{aligned}
p\left(\mathcal{C}_{k} \mid \mathbf{x}\right) & =\frac{p\left(\mathbf{x} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right)}{\sum_{j} p\left(\mathbf{x} \mid \mathcal{C}_{j}\right) p\left(\mathcal{C}_{j}\right)} \\
& =\frac{\exp \left(a_{k}\right)}{\sum_{j} \exp \left(a_{j}\right)},
\end{aligned}
$$

which is known as the normalized exponential and can be regarded as a multi-class generalization of the logistic sigmoid. Here the quantities $a_{k}$ are defined by

$$
a_{k}=\ln \left(p\left(\mathbf{x} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right)\right)
$$

The normalized exponential is also known as the softmax function, as it represents a smoothed version of the ' $m$ max' function because, if $a_{k} \gg a_{j}$ for all $j \neq k$, then $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right) \simeq 1$, and $p\left(\mathcal{C}_{j} \mid \mathbf{x}\right) \simeq 0$.

We now investigate the consequences of choosing specific forms for the classconditional densities, looking first at continuous input variables $\mathbf{x}$ and then discussing briefly discrete inputs.

\title{
5.3.1 Continuous inputs
}

Let us assume that the class-conditional densities are Gaussian. We will then explore the resulting form for the posterior probabilities. To start with, we will assume that all classes share the same covariance matrix $\boldsymbol{\Sigma}$. Thus, the density for class $\mathcal{C}_{k}$ is given by

$$
p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)=\frac{1}{(2 \pi)^{D / 2}} \frac{1}{|\boldsymbol{\Sigma}|^{1 / 2}} \exp \left\{-\frac{1}{2}\left(\mathbf{x}-\boldsymbol{\mu}_{k}\right)^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}\left(\mathbf{x}-\boldsymbol{\mu}_{k}\right)\right\}
$$

First, suppose that we have two classes. From (5.40) and (5.41), we have

$$
p\left(\mathcal{C}_{1} \mid \mathbf{x}\right)=\sigma\left(\mathbf{w}^{\mathrm{T}} \mathbf{x}+w_{0}\right)
$$

where we have defined

$$
\begin{aligned}
\mathbf{w} & =\boldsymbol{\Sigma}^{-1}\left(\boldsymbol{\mu}_{1}-\boldsymbol{\mu}_{2}\right) \\
w_{0} & =-\frac{1}{2} \boldsymbol{\mu}_{1}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}_{1}+\frac{1}{2} \boldsymbol{\mu}_{2}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}_{2}+\ln \frac{p\left(\mathcal{C}_{1}\right)}{p\left(\mathcal{C}_{2}\right)}
\end{aligned}
$$

We see that the quadratic terms in $\mathrm{x}$ from the exponents of the Gaussian densities have cancelled (due to the assumption of common covariance matrices), leading to a linear function of $\mathrm{x}$ in the argument of the logistic sigmoid. This result is illustrated for a two-dimensional input space $\mathrm{x}$ in Figure 5.13. The resulting decision boundaries correspond to surfaces along which the posterior probabilities $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$


![](https://cdn.mathpix.com/cropped/2024_05_26_48954a2b928492e90315g-1.jpg?height=498&width=1492&top_left_y=227&top_left_x=153

ChatGPT figure/image summary: The image is a split-screen graphical representation with two plots. On the left side, there's a 3D plot showcasing two overlapping Gaussian distributions in a two-dimensional input space (labeled \( x_1 \) and \( x_2 \)). One Gaussian distribution is shaded in red and the other in blue. This plot represents the class-conditional densities for two classes, indicating how data points are distributed in each class.

The right side of the image features another 3D plot that depicts the posterior probability \( p(\mathcal{C}_{1} \mid \mathbf{x}) \) as a function of the two-dimensional input space. This is represented as a smooth surface transitioning from red to blue, indicating the probability of data points belonging to class \( \mathcal{C}_{1} \) (red) or class \( \mathcal{C}_{2} \) (blue). The surface is colored with shades of red and blue to reflect the mixture of posterior probabilities between the two classes, with areas of higher red intensity indicating higher probabilities for class \( \mathcal{C}_{1} \) and areas of higher blue intensity indicating higher probabilities for class \( \mathcal{C}_{2} \).

In summary, the left plot illustrates the class distributions, while the right plot visualizes the resulting decision boundary as influenced by these distributions, with the decision boundary presumably occurring where the colors blend into each other indicating a probability transition.)

Figure 5.13 The left-hand plot shows the class-conditional densities for two classes, denoted red and blue. On the right is the corresponding posterior probability $p\left(\mathcal{C}_{1} \mid \mathbf{x}\right)$, which is given by a logistic sigmoid of a linear function of $\mathbf{x}$. The surface in the right-hand plot is coloured using a proportion of red ink given by $p\left(\mathcal{C}_{1} \mid \mathbf{x}\right)$ and a proportion of blue ink given by $p\left(\mathcal{C}_{2} \mid \mathbf{x}\right)=1-p\left(\mathcal{C}_{1} \mid \mathbf{x}\right)$.

are constant and so will be given by linear functions of $\mathbf{x}$, and therefore the decision boundaries are linear in input space. The prior probabilities $p\left(\mathcal{C}_{k}\right)$ enter only through the bias parameter $w_{0}$, so that changes in the priors have the effect of making parallel shifts of the decision boundary and more generally of the parallel contours of constant posterior probability.

For the general case of $K$ classes, the posterior probabilities are given by (5.45) where, from (5.46) and (5.47), we have

$$
a_{k}(\mathbf{x})=\mathbf{w}_{k}^{\mathrm{T}} \mathbf{x}+w_{k 0}
$$

in which we have defined

$$
\begin{aligned}
\mathbf{w}_{k} & =\boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}_{k} \\
w_{k 0} & =-\frac{1}{2} \boldsymbol{\mu}_{k}^{\mathrm{T}} \boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}_{k}+\ln p\left(\mathcal{C}_{k}\right)
\end{aligned}
$$

We see that the $a_{k}(\mathbf{x})$ are again linear functions of $\mathbf{x}$ as a consequence of the cancellation of the quadratic terms due to the shared covariances. The resulting decision boundaries, corresponding to the minimum misclassification rate, will occur when two of the posterior probabilities (the two largest) are equal, and so will be defined by linear functions of $\mathbf{x}$. Thus, we again have a generalized linear model.

If we relax the assumption of a shared covariance matrix and allow each classconditional density $p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)$ to have its own covariance matrix $\boldsymbol{\Sigma}_{k}$, then the earlier cancellations will no longer occur, and we will obtain quadratic functions of $\mathbf{x}$, giving rise to a quadratic discriminant. The linear and quadratic decision boundaries are illustrated in Figure 5.14.

\title{
5.3.2 Maximum likelihood solution
}

Once we have specified a parametric functional form for the class-conditional densities $p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)$, we can then determine the values of the parameters, together with

![](https://cdn.mathpix.com/cropped/2024_05_26_bb6ce2823310d4cb97d4g-1.jpg?height=643&width=701&top_left_y=211&top_left_x=150

ChatGPT figure/image summary: This image illustrates the class-conditional densities for a scenario with three classes in a two-dimensional feature space, where the features are denoted as \( x_1 \) and \( x_2 \). Each class has a Gaussian distribution, and they are represented by different colors: red, green, and blue. The contours indicate areas of equal probability density for the respective classes.

The red and blue classes are depicted as having the same covariance matrix, which is why their contours are similar in shape and orientation but differ in their center or mean. The green class appears to have a different covariance matrix, as its contours are oriented differently from those of the red and blue classes.

The decision boundaries between the classes are also indicated in this plot. These are the lines or curves that separate the different classes. In accordance with the text preceding the image, the decision boundary between the red and blue classes is linear because they share the same covariance matrix. In contrast, the decision boundaries between the red and green classes, as well as between the blue and green classes, are quadratic due to the different covariance matrices.

Overall, this image serves to visualize the concept of class distributions, posterior probabilities, and decision boundaries in the context of a multiclass classification problem using Gaussian distributions and discriminant functions.)

$x_{1}$

![](https://cdn.mathpix.com/cropped/2024_05_26_bb6ce2823310d4cb97d4g-1.jpg?height=643&width=679&top_left_y=211&top_left_x=970

ChatGPT figure/image summary: The image you've provided is a two-dimensional plot illustrating the concept of class-conditional probabilities and decision boundaries for a three-class classification problem. The image depicts a color gradient where each color represents one of the three classes, labeled in the given context as red, blue, and green. The decision boundaries, which are the lines demarcating the regions of the different classes, are also shown.

In the plot, you can see that there are two types of decision boundaries:
- A linear boundary between the blue and red classes, indicated by the fact that these two classes share the same covariance matrix in their Gaussian distribution, as mentioned in the text.
- Quadratic boundaries between the green class and both the red and blue classes, which occurs because the green class has a different covariance matrix, meaning the assumption of a shared covariance matrix is relaxed.

The colors in any given point of the image represent the posterior probabilities for the three classes at that point. The darker the color, the higher the probability for the respective class at that location in the two-dimensional space labeled by \( x_1 \) and \( x_2 \).

The white dashed lines represent the decision boundaries, where the posterior probabilities of the neighboring classes are equal, making those lines the points of decision for classifying new data points.

This image is likely to be used to visualize the results of discriminant analysis, showing how a linear discriminant can be used for classification when the class covariances are equal, and how a quadratic discriminant is needed when the covariances differ.)

$x_{1}$

Figure 5.14 The left-hand plot shows the class-conditional densities for three classes each having a Gaussian distribution, coloured red, green, and blue, in which the red and blue classes have the same covariance matrix. The right-hand plot shows the corresponding posterior probabilities, in which each point on the image is coloured using proportions of red, blue, and green ink corresponding to the posterior probabilities for the respective three classes. The decision boundaries are also shown. Notice that the boundary between the red and blue classes, which have the same covariance matrix, is linear, whereas those between the other pairs of classes are quadratic.

the prior class probabilities $p\left(\mathcal{C}_{k}\right)$, using maximum likelihood. This requires a data set comprising observations of $\mathbf{x}$ along with their corresponding class labels.

First, suppose we have two classes, each having a Gaussian class-conditional density with a shared covariance matrix, and suppose we have a data set $\left\{\mathbf{x}_{n}, t_{n}\right\}$ where $n=1, \ldots, N$. Here $t_{n}=1$ denotes class $\mathcal{C}_{1}$ and $t_{n}=0$ denotes class $\mathcal{C}_{2}$. We denote the prior class probability $p\left(\mathcal{C}_{1}\right)=\pi$, so that $p\left(\mathcal{C}_{2}\right)=1-\pi$. For a data point $\mathbf{x}_{n}$ from class $\mathcal{C}_{1}$, we have $t_{n}=1$ and hence

$$
p\left(\mathbf{x}_{n}, \mathcal{C}_{1}\right)=p\left(\mathcal{C}_{1}\right) p\left(\mathbf{x}_{n} \mid \mathcal{C}_{1}\right)=\pi \mathcal{N}\left(\mathbf{x}_{n} \mid \boldsymbol{\mu}_{1}, \boldsymbol{\Sigma}\right)
$$

Similarly for class $\mathcal{C}_{2}$, we have $t_{n}=0$ and hence

$$
p\left(\mathbf{x}_{n}, \mathcal{C}_{2}\right)=p\left(\mathcal{C}_{2}\right) p\left(\mathbf{x}_{n} \mid \mathcal{C}_{2}\right)=(1-\pi) \mathcal{N}\left(\mathbf{x}_{n} \mid \boldsymbol{\mu}_{2}, \boldsymbol{\Sigma}\right)
$$

Thus, the likelihood function is given by

$$
p\left(\mathbf{t}, \mathbf{X} \mid \pi, \boldsymbol{\mu}_{1}, \boldsymbol{\mu}_{2}, \boldsymbol{\Sigma}\right)=\prod_{n=1}^{N}\left[\pi \mathcal{N}\left(\mathbf{x}_{n} \mid \boldsymbol{\mu}_{1}, \boldsymbol{\Sigma}\right)\right]^{t_{n}}\left[(1-\pi) \mathcal{N}\left(\mathbf{x}_{n} \mid \boldsymbol{\mu}_{2}, \boldsymbol{\Sigma}\right)\right]^{1-t_{n}}
$$

where $\mathbf{t}=\left(t_{1}, \ldots, t_{N}\right)^{\mathrm{T}}$. As usual, it is convenient to maximize the log of the likelihood function. Consider first the maximization with respect to $\pi$. The terms in

the $\log$ likelihood function that depend on $\pi$ are

$$
\sum_{n=1}^{N}\left\{t_{n} \ln \pi+\left(1-t_{n}\right) \ln (1-\pi)\right\}
$$

Setting the derivative with respect to $\pi$ equal to zero and rearranging, we obtain

$$
\pi=\frac{1}{N} \sum_{n=1}^{N} t_{n}=\frac{N_{1}}{N}=\frac{N_{1}}{N_{1}+N_{2}}
$$

where $N_{1}$ denotes the total number of data points in class $\mathcal{C}_{1}$, and $N_{2}$ denotes the total number of data points in class $\mathcal{C}_{2}$. Thus, the maximum likelihood estimate for $\pi$ is simply the fraction of points in class $\mathcal{C}_{1}$ as expected. This result is easily generalized to the multi-class case where again the maximum likelihood estimate of the prior probability associated with class $\mathcal{C}_{k}$ is given by the fraction of the training set points assigned to that class.

Now consider the maximization with respect to $\boldsymbol{\mu}_{1}$. Again, we can pick out of the $\log$ likelihood function those terms that depend on $\boldsymbol{\mu}_{1}$ :

$$
\sum_{n=1}^{N} t_{n} \ln \mathcal{N}\left(\mathbf{x}_{n} \mid \boldsymbol{\mu}_{1}, \boldsymbol{\Sigma}\right)=-\frac{1}{2} \sum_{n=1}^{N} t_{n}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{1}\right)^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{1}\right)+\text { const. }
$$

Setting the derivative with respect to $\boldsymbol{\mu}_{1}$ to zero and rearranging, we obtain

$$
\boldsymbol{\mu}_{1}=\frac{1}{N_{1}} \sum_{n=1}^{N} t_{n} \mathbf{x}_{n}
$$

which is simply the mean of all the input vectors $\mathbf{x}_{n}$ assigned to class $\mathcal{C}_{1}$. By a similar argument, the corresponding result for $\boldsymbol{\mu}_{2}$ is given by

$$
\boldsymbol{\mu}_{2}=\frac{1}{N_{2}} \sum_{n=1}^{N}\left(1-t_{n}\right) \mathbf{x}_{n}
$$

which again is the mean of all the input vectors $\mathbf{x}_{n}$ assigned to class $\mathcal{C}_{2}$.

Finally, consider the maximum likelihood solution for the shared covariance matrix $\boldsymbol{\Sigma}$. Picking out the terms in the log likelihood function that depend on $\boldsymbol{\Sigma}$, we have

$$
\begin{aligned}
& -\frac{1}{2} \sum_{n=1}^{N} t_{n} \ln |\boldsymbol{\Sigma}|-\frac{1}{2} \sum_{n=1}^{N} t_{n}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{1}\right)^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{1}\right) \\
& -\frac{1}{2} \sum_{n=1}^{N}\left(1-t_{n}\right) \ln |\boldsymbol{\Sigma}|-\frac{1}{2} \sum_{n=1}^{N}\left(1-t_{n}\right)\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{2}\right)^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{2}\right) \\
& =-\frac{N}{2} \ln |\boldsymbol{\Sigma}|-\frac{N}{2} \operatorname{Tr}\left\{\boldsymbol{\Sigma}^{-1} \mathbf{S}\right\}
\end{aligned}
$$

\section*{Exercise 5.14}

Section 5.1.4

Section 11.2 .3

\section*{Exercise 5.16}

where we have defined

$$
\begin{aligned}
\mathbf{S} & =\frac{N_{1}}{N} \mathbf{S}_{1}+\frac{N_{2}}{N} \mathbf{S}_{2} \\
\mathbf{S}_{1} & =\frac{1}{N_{1}} \sum_{n \in \mathcal{C}_{1}}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{1}\right)\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{1}\right)^{\mathrm{T}} \\
\mathbf{S}_{2} & =\frac{1}{N_{2}} \sum_{n \in \mathcal{C}_{2}}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{2}\right)\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{2}\right)^{\mathrm{T}}
\end{aligned}
$$

Using the standard result for the maximum likelihood solution for a Gaussian distribution, we see that $\boldsymbol{\Sigma}=\mathbf{S}$, which represents a weighted average of the covariance matrices associated with each of the two classes separately.

This result is easily extended to the $K$-class problem to obtain the corresponding maximum likelihood solutions for the parameters in which each class-conditional density is Gaussian with a shared covariance matrix. Note that the approach of fitting Gaussian distributions to the classes is not robust to outliers, because the maximum likelihood estimation of a Gaussian is not robust.

\subsection*{5.3.3 Discrete features}

Let us now consider discrete feature values $x_{i}$. For simplicity, we begin by looking at binary feature values $x_{i} \in\{0,1\}$ and discuss the extension to more general discrete features shortly. If there are $D$ inputs, then a general distribution would correspond to a table of $2^{D}$ numbers for each class and have $2^{D}-1$ independent variables (due to the summation constraint). Because this grows exponentially with the number of features, we can seek a more restricted representation. Here we will make the naive Bayes assumption in which the feature values are treated as independent and conditioned on the class $\mathcal{C}_{k}$. Thus, we have class-conditional distributions of the form

$$
p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)=\prod_{i=1}^{D} \mu_{k i}^{x_{i}}\left(1-\mu_{k i}\right)^{1-x_{i}}
$$

which contain $D$ independent parameters for each class. Substituting into (5.46) then gives

$$
a_{k}(\mathbf{x})=\sum_{i=1}^{D}\left\{x_{i} \ln \mu_{k i}+\left(1-x_{i}\right) \ln \left(1-\mu_{k i}\right)\right\}+\ln p\left(\mathcal{C}_{k}\right)
$$

which again are linear functions of the input values $x_{i}$. For $K=2$ classes, we can alternatively consider the logistic sigmoid formulation given by (5.40). Analogous results are obtained for discrete variables that take $L>2$ states.

\subsection*{5.3.4 Exponential family}

As we have seen, for both Gaussian distributed and discrete inputs, the posterior class probabilities are given by generalized linear models with logistic sigmoid ( $K=$

2 classes) or softmax ( $K \geqslant 2$ classes) activation functions. These are particular cases of a more general result obtained by assuming that the class-conditional densities $p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)$ are members of the subset of the exponential family of distributions given by

$$
p\left(\mathbf{x} \mid \boldsymbol{\lambda}_{k}, s\right)=\frac{1}{s} h\left(\frac{1}{s} \mathbf{x}\right) g\left(\boldsymbol{\lambda}_{k}\right) \exp \left\{\frac{1}{s} \boldsymbol{\lambda}_{k}^{\mathrm{T}} \mathbf{x}\right\}
$$

Here the scaling parameter $s$ is shared across all the classes.

For the two-class problem, we substitute this expression for the class-conditional densities into (5.41) and we see that the posterior class probability is again given by a logistic sigmoid acting on a linear function $a(\mathbf{x})$, which is given by

$$
a(\mathbf{x})=\left(\boldsymbol{\lambda}_{1}-\boldsymbol{\lambda}_{2}\right)^{\mathrm{T}} \mathbf{x}+\ln g\left(\boldsymbol{\lambda}_{1}\right)-\ln g\left(\boldsymbol{\lambda}_{2}\right)+\ln p\left(\mathcal{C}_{1}\right)-\ln p\left(\mathcal{C}_{2}\right)
$$

Similarly, for the $K$-class problem, we substitute the class-conditional density expression into (5.46) to give

$$
a_{k}(\mathbf{x})=\boldsymbol{\lambda}_{k}^{\mathrm{T}} \mathbf{x}+\ln g\left(\boldsymbol{\lambda}_{k}\right)+\ln p\left(\mathcal{C}_{k}\right)
$$

and so again is a linear function of $\mathbf{x}$.

\title{
5.4. Discriminative Classifiers
}

For the two-class classification problem, we have seen that the posterior probability of class $\mathcal{C}_{1}$ can be written as a logistic sigmoid acting on a linear function of $\mathbf{x}$, for a wide choice of class-conditional distributions $p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)$ from the exponential family. Similarly, for the multi-class case, the posterior probability of class $\mathcal{C}_{k}$ is given by a softmax transformation of linear functions of $\mathbf{x}$. For specific choices of the class-conditional densities $p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)$, we have used maximum likelihood to determine the parameters of the densities as well as the class priors $p\left(\mathcal{C}_{k}\right)$ and then used Bayes' theorem to find the posterior class probabilities. This represents an example of generative modelling, because we could take such a model and generate synthetic data by drawing values of $\mathbf{x}$ from the marginal distribution $p(\mathbf{x})$ or from any of the class-conditional densities $p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)$.

However, an alternative approach is to use the functional form of the generalized linear model explicitly and to determine its parameters directly by using maximum likelihood. In this direct approach, we maximize a likelihood function defined through the conditional distribution $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$, which represents a form of discriminative probabilistic modelling. One advantage of the discriminative approach is that there will typically be fewer learnable parameters to be determined, as we will see shortly. It may also lead to improved predictive performance, particularly when the assumed forms for the class-conditional densities represent a poor approximation to the true distributions.

\title{
5.4.1 Activation functions
}

Chapter 4

Section 5.2

Section 6.1
In linear regression, the model prediction $y(\mathbf{x}, \mathbf{w})$ is given by a linear function of the parameters

$$
y(\mathbf{x}, \mathbf{w})=\mathbf{w}^{\mathrm{T}} \mathbf{x}+w_{0}
$$

which gives a continuous-valued output in the range $(-\infty, \infty)$. For classification problems, however, we wish to predict discrete class labels, or more generally posterior probabilities that lie in the range $(0,1)$. To achieve this, we consider a generalization of this model in which we transform the linear function of $\mathbf{w}$ and $w_{0}$ using a nonlinear function $f(\cdot)$ so that

$$
y(\mathbf{x}, \mathbf{w})=f\left(\mathbf{w}^{\mathrm{T}} \mathbf{w}+w+0\right)
$$

In the machine learning literature, $f(\cdot)$ is known as an activation function, whereas its inverse is called a link function in the statistics literature. The decision surfaces correspond to $y(\mathbf{x})=$ constant, so that $\mathbf{w}^{\mathrm{T}} \mathbf{x}=$ constant, and hence the decision surfaces are linear functions of $\mathbf{x}$, even if the function $f(\cdot)$ is nonlinear. For this reason, the class of models described by (5.70) are called generalized linear models (McCullagh and Nelder, 1989). However, in contrast to the models used for regression, they are no longer linear in the parameters due to the nonlinear function $f(\cdot)$. This will lead to more complex analytical and computational properties than for linear regression models. Nevertheless, these models are still relatively simple compared to the much more flexible nonlinear models that will be studied in subsequent chapters.

\subsection*{5.4.2 Fixed basis functions}

So far in this chapter, we have considered classification models that work directly with the original input vector $\mathbf{x}$. However, all the algorithms are equally applicable if we first make a fixed nonlinear transformation of the inputs using a vector of basis functions $\phi(\mathbf{x})$. The resulting decision boundaries will be linear in the feature space $\phi$, and these correspond to nonlinear decision boundaries in the original $\mathbf{x}$ space, as illustrated in Figure 5.15. Classes that are linearly separable in the feature space $\phi(\mathrm{x})$ need not be linearly separable in the original observation space $\mathrm{x}$.

Note that as in our discussion of linear models for regression, one of the basis functions is typically set to a constant, say $\phi_{0}(\mathbf{x})=1$, so that the corresponding parameter $w_{0}$ plays the role of a bias.

For many problems of practical interest, there is significant overlap in $\mathrm{x}$-space between the class-conditional densities $p\left(\mathbf{x} \mid \mathcal{C}_{k}\right)$. This corresponds to posterior probabilities $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$, which, for at least some values of $\mathbf{x}$, are not 0 or 1 . In such cases, the optimal solution is obtained by modelling the posterior probabilities accurately and then applying standard decision theory. Note that nonlinear transformations $\phi(\mathbf{x})$ cannot remove such a class overlap, although they can increase the level of overlap or create an overlap where none existed in the original observation space. However, suitable choices of nonlinearity can make the process of modelling the posterior probabilities easier. However, such fixed basis function models have important limitations, and these will be resolved in later chapters by allowing the basis functions themselves to adapt to the data.


![](https://cdn.mathpix.com/cropped/2024_05_26_f271bce35f2c91024ce0g-1.jpg?height=740&width=1514&top_left_y=221&top_left_x=110

ChatGPT figure/image summary: The image depicts two plots that illustrate the role of nonlinear basis functions in a linear classification model, as described in the provided text. 

The left-hand plot represents the original input space, marked as x1 and x2 on the x-axis and y-axis respectively. In this space, data points are shown from two classes, labeled red and blue. Each class seems to be clustered around different centers, marked with green plus signs, which are the centers of two 'Gaussian' basis functions. The green circles represent the contours of these basis functions.

The right-hand plot represents the feature space obtained after applying the nonlinear basis functions, labeled as ϕ1 and ϕ2 on the x-axis and y-axis respectively. After the transformation, we can see that the data points now form distinct clusters that are separable by a straight line, which is shown as a black line in the plot. This black line is the linear decision boundary achieved through logistic regression, corresponding to a nonlinear decision boundary in the original input space. The nonlinear decision boundary is depicted in the left-hand plot by the black curve that separates the red and blue data points.

The image visualizes the concept that while the original input space may have non-linearly separable classes, transforming the input space using basis functions can lead to a feature space where the classes are linearly separable. Hence, it demonstrates how a logistic regression model can create a complex decision boundary in the original input space while maintaining a linear decision boundary in the transformed feature space.)

Figure 5.15 Illustration of the role of nonlinear basis functions in linear classification models. The left-hand plot shows the original input space $\left(x_{1}, x_{2}\right)$ together with data points from two classes labelled red and blue. Two 'Gaussian' basis functions $\phi_{1}(\mathbf{x})$ and $\phi_{2}(\mathbf{x})$ are defined in this space with centres shown by the green crosses and with contours shown by the green circles. The right-hand plot shows the corresponding feature space $\left(\phi_{1}, \phi_{2}\right)$ together with the linear decision boundary obtained given by a logistic regression model of the form discussed in Section 5.4.3. This corresponds to a nonlinear decision boundary in the original input space, shown by the black curve in the left-hand plot.

\title{
5.4.3 Logistic regression
}

We first consider the problem of two-class classification. In our discussion of generative approaches in Section 5.3, we saw that under rather general assumptions, the posterior probability of class $\mathcal{C}_{1}$ can be written as a logistic sigmoid acting on a linear function of the feature vector $\phi$ so that

$$
p\left(\mathcal{C}_{1} \mid \boldsymbol{\phi}\right)=y(\boldsymbol{\phi})=\sigma\left(\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}\right)
$$

with $p\left(\mathcal{C}_{2} \mid \phi\right)=1-p\left(\mathcal{C}_{1} \mid \phi\right)$. Here $\sigma(\cdot)$ is the logistic sigmoid function defined by (5.42). In the terminology of statistics, this model is known as logistic regression, although it should be emphasized that this is a model for classification rather than for continuous variable.

For an $M$-dimensional feature space $\phi$, this model has $M$ adjustable parameters. By contrast, if we had fitted Gaussian class-conditional densities using maximum likelihood, we would have used $2 M$ parameters for the means and $M(M+1) / 2$ parameters for the (shared) covariance matrix. Together with the class prior $p\left(\mathcal{C}_{1}\right)$, this gives a total of $M(M+5) / 2+1$ parameters, which grows quadratically with $M$, in contrast to the linear dependence on $M$ of the number of parameters in logistic regression. For large values of $M$, there is a clear advantage in working with the logistic regression model directly.

Figure 5.1 Illustration of the geometry of a linear discriminant function in two dimensions. The decision surface, shown in red, is perpendicular to $\mathbf{w}$, and its displacement from the origin is controlled by the bias parameter $w_{0}$. Also, the signed orthogonal distance of a general point $\mathrm{x}$ from the decision surface is given by $y(\mathbf{x}) /\|\mathbf{w}\|$.

![](https://cdn.mathpix.com/cropped/2024_05_26_54f3776e893a83ecd076g-1.jpg?height=698&width=898&top_left_y=215&top_left_x=760

ChatGPT figure/image summary: The provided image appears to be a two-dimensional graphical representation of a linear classifier. It includes an illustration of a linear decision boundary and the following elements:

- Two coordinate axes, \( x_1 \) and \( x_2 \), which are the axes of the input feature space.
- A red line labeled with \( y = 0 \) which represents the decision boundary separating two regions (\( R_1 \) and \( R_2 \)) on the plane. Points on one side of this line are classified differently than those on the other side.
- The regions labeled \( R_1 \) and \( R_2 \) are divided by the decision boundary. These regions represent the two classifications made by the linear decision function.
- A perpendicular distance is marked from a point \( x \) to the decision boundary, showing the relation of the point to the boundary. This is denoted by the fraction \( \frac{y(x)}{\|w\|} \), where \( y(x) \) is the output of the linear classifier for input \( x \), and \( \|w\| \) is the norm (magnitude) of the weight vector \( w \).
- The weight vector \( w \) is represented by a green arrow, indicating the orientation of the decision boundary in feature space.
- The blue dashed line shows the orthogonal projection from point \( x \) onto the decision boundary, and \( x_{\perp} \) marks the point where this projection intersects the decision boundary.
- The bias term \( \frac{-w_0}{\|w\|} \) is indicated on the \( x_1 \) axis, suggesting how the decision boundary's position is determined by the bias term relative to the origin.

This figure demonstrates key concepts in machine learning, including the geometric interpretation of a linear classifier, the role of weights in defining the orientation of the decision boundary, and how a bias term shifts the boundary away from the origin. The decision boundary effectively divides the input space into two regions, each corresponding to one of the two classes that the linear classifier aims to distinguish. The image likely supplements a discussion on linear classification methods, more specifically logistic regression, in the context of machine learning or statistical pattern recognition.)

the $D$-dimensional input space. Consider two points $\mathbf{x}_{\mathrm{A}}$ and $\mathbf{x}_{\mathrm{B}}$ both of which lie on the decision surface. Because $y\left(\mathbf{x}_{\mathrm{A}}\right)=y\left(\mathbf{x}_{\mathrm{B}}\right)=0$, we have $\mathbf{w}^{\mathrm{T}}\left(\mathbf{x}_{\mathrm{A}}-\mathbf{x}_{\mathrm{B}}\right)=0$ and hence the vector $\mathbf{w}$ is orthogonal to every vector lying within the decision surface, and so $\mathrm{w}$ determines the orientation of the decision surface. Similarly, if $\mathrm{x}$ is a point on the decision surface, then $y(\mathrm{x})=0$, and so the normal distance from the origin to the decision surface is given by

$$
\frac{\mathbf{w}^{\mathrm{T}} \mathbf{x}}{\|\mathbf{w}\|}=-\frac{w_{0}}{\|\mathbf{w}\|}
$$

We therefore see that the bias parameter $w_{0}$ determines the location of the decision surface. These properties are illustrated for the case of $D=2$ in Figure 5.1.

Furthermore, note that the value of $y(\mathbf{x})$ gives a signed measure of the perpendicular distance $r$ of the point $\mathbf{x}$ from the decision surface. To see this, consider an arbitrary point $\mathbf{x}$ and let $\mathbf{x}_{\perp}$ be its orthogonal projection onto the decision surface, so that

$$
\mathbf{x}=\mathbf{x}_{\perp}+r \frac{\mathbf{w}}{\|\mathbf{w}\|}
$$

Multiplying both sides of this result by $\mathbf{w}^{\mathrm{T}}$ and adding $w_{0}$, and making use of $y(\mathbf{x})=$ $\mathbf{w}^{\mathrm{T}} \mathbf{x}+w_{0}$ and $y\left(\mathbf{x}_{\perp}\right)=\mathbf{w}^{\mathrm{T}} \mathbf{x}_{\perp}+w_{0}=0$, we have

$$
r=\frac{y(\mathbf{x})}{\|\mathbf{w}\|}
$$

This result is illustrated in Figure 5.1.

Section 4.1.1

As with linear regression models, it is sometimes convenient to use a more compact notation in which we introduce an additional dummy 'input' value $x_{0}=1$ and then define $\widetilde{\mathbf{w}}=\left(w_{0}, \mathbf{w}\right)$ and $\widetilde{\mathbf{x}}=\left(x_{0}, \mathbf{x}\right)$ so that

$$
y(\mathbf{x})=\widetilde{\mathbf{w}}^{\mathrm{T}} \widetilde{\mathbf{x}}
$$

\section*{Exercise 5.18}

Exercise 5.19

Section 4.1.3

Chapter 7
We now use maximum likelihood to determine the parameters of the logistic regression model. To do this, we will make use of the derivative of the logistic sigmoid function, which can conveniently be expressed in terms of the sigmoid function itself:

$$
\frac{\mathrm{d} \sigma}{\mathrm{d} a}=\sigma(1-\sigma)
$$

For a data set $\left\{\boldsymbol{\phi}_{n}, t_{n}\right\}$, where $\boldsymbol{\phi}_{n}=\boldsymbol{\phi}\left(\mathbf{x}_{n}\right)$ and $t_{n} \in\{0,1\}$, with $n=1, \ldots, N$, the likelihood function can be written

$$
p(\mathbf{t} \mid \mathbf{w})=\prod_{n=1}^{N} y_{n}^{t_{n}}\left\{1-y_{n}\right\}^{1-t_{n}}
$$

where $\mathbf{t}=\left(t_{1}, \ldots, t_{N}\right)^{\mathrm{T}}$ and $y_{n}=p\left(\mathcal{C}_{1} \mid \boldsymbol{\phi}_{n}\right)$. As usual, we can define an error function by taking the negative logarithm of the likelihood, which gives the crossentropy error function:

$$
E(\mathbf{w})=-\ln p(\mathbf{t} \mid \mathbf{w})=-\sum_{n=1}^{N}\left\{t_{n} \ln y_{n}+\left(1-t_{n}\right) \ln \left(1-y_{n}\right)\right\}
$$

where $y_{n}=\sigma\left(a_{n}\right)$ and $a_{n}=\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}_{n}$. Taking the gradient of the error function with respect to $\mathbf{w}$, we obtain

$$
\nabla E(\mathbf{w})=\sum_{n=1}^{N}\left(y_{n}-t_{n}\right) \phi_{n}
$$

where we have made use of (5.72). We see that the factor involving the derivative of the logistic sigmoid has cancelled, leading to a simplified form for the gradient of the log likelihood. In particular, the contribution to the gradient from data point $n$ is given by the 'error' $y_{n}-t_{n}$ between the target value and the prediction of the model times the basis function vector $\phi_{n}$. Furthermore, comparison with (4.12) shows that this takes precisely the same form as the gradient of the sum-of-squares error function for the linear regression model.

The maximum likelihood solution corresponds to $\nabla E(\mathbf{w})=0$. However, from (5.75) we see that this no longer corresponds to a set of linear equations, due to the nonlinearity in $y(\cdot)$, and so this equation does not have a closed-form solution. One approach to finding a maximum likelihood solution would be to use stochastic gradient descent, in which $\nabla E_{n}$ is the $n$th term on the right-hand side of (5.75). Stochastic gradient descent will be the principal approach to training the highly nonlinear neural networks discussed in later chapters. However, the maximum likelihood equation is only 'slightly' nonlinear, and in fact the error function (5.74), in which the model is defined by (5.71), is a convex function of the parameters, which allows the error function to be minimized using a simple algorithm called iterative reweighted least squares or IRLS (Bishop, 2006). However, this does not easily generalize to more complex models such as deep neural networks.

Exercise 5.20

Chapter 9

Section 5.3

Exercise 5.21
Note that maximum likelihood can exhibit severe over-fitting for data sets that are linearly separable. This arises because the maximum likelihood solution occurs when the hyperplane corresponding to $\sigma=0.5$, equivalent to $\mathrm{w}^{\mathrm{T}} \phi=0$, separates the two classes and the magnitude of $\mathbf{w}$ goes to infinity. In this case, the logistic sigmoid function becomes infinitely steep in feature space, corresponding to a Heaviside step function, so that every training point from each class $k$ is assigned a posterior probability $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)=1$. Furthermore, there is typically a continuum of such solutions because any separating hyperplane will give rise to the same posterior probabilities at the training data points. Maximum likelihood provides no way to favour one such solution over another, and which solution is found in practice will depend on the choice of optimization algorithm and on the parameter initialization. Note that the problem will arise even if the number of data points is large compared with the number of parameters in the model, so long as the training data set is linearly separable. The singularity can be avoided by adding a regularization term to the error function.

\subsection*{5.4.4 Multi-class logistic regression}

In our discussion of generative models for multi-class classification, we have seen that, for a large class of distributions from the exponential family, the posterior probabilities are given by a softmax transformation of linear functions of the feature variables, so that

$$
p\left(\mathcal{C}_{k} \mid \boldsymbol{\phi}\right)=y_{k}(\boldsymbol{\phi})=\frac{\exp \left(a_{k}\right)}{\sum_{j} \exp \left(a_{j}\right)}
$$

where the pre-activations $a_{k}$ are given by

$$
a_{k}=\mathbf{w}_{k}^{\mathrm{T}} \boldsymbol{\phi}
$$

There we used maximum likelihood to determine separately the class-conditional densities and the class priors and then found the corresponding posterior probabilities using Bayes' theorem, thereby implicitly determining the parameters $\left\{\mathbf{w}_{k}\right\}$. Here we consider the use of maximum likelihood to determine the parameters $\left\{\mathbf{w}_{k}\right\}$ of this model directly. To do this, we will require the derivatives of $y_{k}$ with respect to all the pre-activations $a_{j}$. These are given by

$$
\frac{\partial y_{k}}{\partial a_{j}}=y_{k}\left(I_{k j}-y_{j}\right)
$$

where $I_{k j}$ are the elements of the identity matrix.

Next we write down the likelihood function. This is most easily done using the 1 -of- $K$ coding scheme in which the target vector $\mathbf{t}_{n}$ for a feature vector $\phi_{n}$ belonging to class $\mathcal{C}_{k}$ is a binary vector with all elements zero except for element $k$, which equals one. The likelihood function is then given by

$$
p\left(\mathbf{T} \mid \mathbf{w}_{1}, \ldots, \mathbf{w}_{K}\right)=\prod_{n=1}^{N} \prod_{k=1}^{K} p\left(\mathcal{C}_{k} \mid \boldsymbol{\phi}_{n}\right)^{t_{n k}}=\prod_{n=1}^{N} \prod_{k=1}^{K} y_{n k}^{t_{n k}}
$$

Figure 5.16 Representation of a multi-class linear classification model as a neural network having a single layer of connections. Each basis function is represented by a node, with the solid node representing the 'bias' basis function $\phi_{0}$, whereas each output $y_{1}, \ldots, y_{N}$ is also represented by a node. The links between the nodes represent the corresponding weight and bias

![](https://cdn.mathpix.com/cropped/2024_05_26_4ee214bfb89bd0af3d94g-1.jpg?height=344&width=654&top_left_y=209&top_left_x=992

ChatGPT figure/image summary: The image depicts a schematic representation of a multi-class linear classification model as a neural network with a single layer of connections. It shows nodes that represent basis functions with the solid node representing the 'bias' basis function (φ₀). Each output (y₁ to yₖ) is also represented by a node. The links between nodes indicate corresponding weight and bias parameters. This is a visual representation of the mathematical concepts expressed in the text which relates to multi-class logistic regression in a machine learning context.)
parameters.

where $y_{n k}=y_{k}\left(\boldsymbol{\phi}_{n}\right)$, and $\mathbf{T}$ is an $N \times K$ matrix of target variables with elements $t_{n k}$. Taking the negative logarithm then gives

$$
E\left(\mathbf{w}_{1}, \ldots, \mathbf{w}_{K}\right)=-\ln p\left(\mathbf{T} \mid \mathbf{w}_{1}, \ldots, \mathbf{w}_{K}\right)=-\sum_{n=1}^{N} \sum_{k=1}^{K} t_{n k} \ln y_{n k}
$$

which is known as the cross-entropy error function for the multi-class classification problem.

We now take the gradient of the error function with respect to one of the param-

Exercise 5.22

Chapter 7

Section 5.4.6 eter vectors $\mathbf{w}_{j}$. Making use of the result (5.78) for the derivatives of the softmax function, we obtain

$$
\nabla_{\mathbf{w}_{j}} E\left(\mathbf{w}_{1}, \ldots, \mathbf{w}_{K}\right)=\sum_{n=1}^{N}\left(y_{n j}-t_{n j}\right) \phi_{n}
$$

where we have made use of $\sum_{k} t_{n k}=1$. Again, we could optimize the parameters through stochastic gradient descent.

Once again, we see the same form arising for the gradient as was found for the sum-of-squares error function with the linear model and for the cross-entropy error with the logistic regression model, namely the product of the error $\left(y_{n j}-t_{n j}\right)$ times the basis function activation $\phi_{n}$. These are examples of a more general result that we will explore later.

Linear classification models can be represented as single-layer neural networks as shown in Figure 5.16. If we consider the derivative of the error function with respect to a weight $w_{i k}$, which links basis function $\phi_{i}(\mathbf{x})$ to output unit $t_{k}$, we have from $(5.81)$

$$
\frac{\partial E\left(\mathbf{w}_{1}, \ldots, \mathbf{w}_{K}\right)}{\partial w_{i j}}=\sum_{n=1}^{N}\left(y_{n k}-t_{n k}\right) \phi_{i}\left(\mathbf{x}_{n}\right)
$$

Comparing this with Figure 5.16, we see that, for each data point $n$ this gradient takes the form of the output of the basis function at the input end of the weight link with the 'error' $\left(y_{n k}-t_{n k}\right)$ at the output end.

Figure 5.17 Schematic example of a probability density $p(\theta)$ shown by the blue curve, given in this example by a mixture of two Gaussians, along with its cumulative distribution function $f(a)$, shown by the red curve. Note that the value of the blue curve at any point, such as that indicated by the vertical green line, corresponds to the slope of the red curve at the same point. Conversely, the value of the red curve at this point corresponds to the area under the blue curve indicated by the shaded green region. In the stochastic threshold model, the class label takes the value $t=1$ if the value of $a=\mathbf{w}^{\mathrm{T}} \phi$ exceeds a threshold, otherwise it takes the value $t=0$. This is equivalent to an activation function given by the cumulative distribution function $f(a)$.

![](https://cdn.mathpix.com/cropped/2024_05_26_5640d2959c04ab9cdc5eg-1.jpg?height=503&width=654&top_left_y=230&top_left_x=948

ChatGPT figure/image summary: The image displays two curves along with a vertical line and a shaded area beneath one of the curves. The blue curve represents a probability density function (PDF), which appears to be a mixture of two Gaussian distributions. The red curve is a cumulative distribution function (CDF), and its value at any point on the x-axis corresponds to the area under the blue curve up to that point. The vertical green line marks a specific value on the x-axis, and the area to the left of this line under the blue curve (shaded in green) represents the value of the red curve at the point where the green line intersects the red curve. The illustration demonstrates the relationship between the PDF and the CDF in the context of threshold-based probabilistic classification models discussed in the provided text.)

\title{
5.4.5 Probit regression
}

We have seen that, for a broad range of class-conditional distributions described by the exponential family, the resulting posterior class probabilities are given by a logistic (or softmax) transformation acting on a linear function of the feature variables. However, not all choices of class-conditional density give rise to such a simple form for the posterior probabilities, which suggests that it might be worth exploring other types of discriminative probabilistic model. Consider the two-class case, again remaining within the framework of generalized linear models, so that

$$
p(t=1 \mid a)=f(a)
$$

where $a=\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}$, and $f(\cdot)$ is the activation function.

One way to motivate an alternative choice for the link function is to consider a noisy threshold model, as follows. For each input $\phi_{n}$, we evaluate $a_{n}=\mathbf{w}^{\mathrm{T}} \phi_{n}$ and then we set the target value according to

$$
\begin{cases}t_{n}=1, & \text { if } a_{n} \geqslant \theta \\ t_{n}=0, & \text { otherwise }\end{cases}
$$

If the value of $\theta$ is drawn from a probability density $p(\theta)$, then the corresponding activation function will be given by the cumulative distribution function

$$
f(a)=\int_{-\infty}^{a} p(\theta) \mathrm{d} \theta
$$

as illustrated in Figure 5.17.

As a specific example, suppose that the density $p(\theta)$ is given by a zero-mean, unit-variance Gaussian. The corresponding cumulative distribution function is given by

$$
\Phi(a)=\int_{-\infty}^{a} \mathcal{N}(\theta \mid 0,1) \mathrm{d} \theta
$$

which is known as the probit function. It has a sigmoidal shape and is compared with the logistic sigmoid function in Figure 5.12. Note that the use of a Gaussian distribution with general mean and variances does not change the model because this is equivalent to a re-scaling of the linear coefficients $\mathbf{w}$. Many numerical packages can evaluate a closely related function defined by

$$
\operatorname{erf}(a)=\frac{2}{\sqrt{\pi}} \int_{0}^{a} \exp \left(-\theta^{2} / 2\right) \mathrm{d} \theta
$$

and known as the erf function or error function (not to be confused with the error function of a machine learning model). It is related to the probit function by

$$
\Phi(a)=\frac{1}{2}\left\{1+\frac{1}{\sqrt{2}} \operatorname{erf}(a)\right\}
$$

The generalized linear model based on a probit activation function is known as probit regression. We can determine the parameters of this model using maximum likelihood by a straightforward extension of the ideas discussed earlier. In practice, the results found using probit regression tend to be like those of logistic regression.

One issue that can occur in practical applications is that of outliers, which can arise for instance through errors in measuring the input vector $\mathrm{x}$ or through mislabelling of the target value $t$. Because such points can lie a long way to the wrong side of the ideal decision boundary, they can seriously distort the classifier. The logistic and probit regression models behave differently in this respect because the tails of the logistic sigmoid decay asymptotically like $\exp (-x)$ for $|x| \rightarrow \infty$, whereas for the probit activation function, they decay like $\exp \left(-x^{2}\right)$, and so the probit model can be significantly more sensitive to outliers.

\title{
5.4.6 Canonical link functions
}

For the linear regression model with a Gaussian noise distribution, the error function, corresponding to the negative $\log$ likelihood, is given by (4.11). If we take the derivative with respect to the parameter vector $\mathbf{w}$ of the contribution to the error function from a data point $n$, this takes the form of the 'error' $y_{n}-t_{n}$ times the feature vector $\phi_{n}$, where $y_{n}=\mathbf{w}^{\mathrm{T}} \phi_{n}$. Similarly, for the combination of the logisticsigmoid activation function and the cross-entropy error function (5.74) and for the softmax activation function with the multi-class cross-entropy error function (5.80), we again obtain this same simple form. We now show that this is a general result of assuming a conditional distribution for the target variable from the exponential family along with a corresponding choice for the activation function known as the canonical link function.

We again make use of the restricted form (3.169) of exponential family distributions. Note that here we are applying the assumption of exponential family distribution to the target variable $t$, in contrast to Section 5.3.4 where we applied it to the input vector $\mathrm{x}$. We therefore consider conditional distributions of the target variable of the form

$$
p(t \mid \eta, s)=\frac{1}{s} h\left(\frac{t}{s}\right) g(\eta) \exp \left\{\frac{\eta t}{s}\right\}
$$

Using the same line of argument as led to the derivation of the result (3.172), we see that the conditional mean of $t$, which we denote by $y$, is given by

$$
y \equiv \mathbb{E}[t \mid \eta]=-s \frac{d}{d \eta} \ln g(\eta)
$$

Thus, $y$ and $\eta$ must related, and we denote this relation through $\eta=\psi(y)$.

Following Nelder and Wedderburn (1972), we define a generalized linear model to be one for which $y$ is a nonlinear function of a linear combination of the input (or feature) variables so that

$$
y=f\left(\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}\right)
$$

where $f(\cdot)$ is known as the activation function in the machine learning literature, and $f^{-1}(\cdot)$ is known as the link function in statistics.

Now consider the log likelihood function for this model, which, as a function of $\eta$, is given by

$$
\ln p(\mathbf{t} \mid \eta, s)=\sum_{n=1}^{N} \ln p\left(t_{n} \mid \eta, s\right)=\sum_{n=1}^{N}\left\{\ln g\left(\eta_{n}\right)+\frac{\eta_{n} t_{n}}{s}\right\}+\text { const }
$$

where we are assuming that all observations share a common scale parameter (which corresponds to the noise variance for a Gaussian distribution, for instance) and so $s$ is independent of $n$. The derivative of the log likelihood with respect to the model parameters $\mathbf{w}$ is then given by

$$
\begin{aligned}
\nabla_{\mathbf{w}} \ln p(\mathbf{t} \mid \eta, s) & =\sum_{n=1}^{N}\left\{\frac{\mathrm{d}}{\mathrm{d} \eta_{n}} \ln g\left(\eta_{n}\right)+\frac{t_{n}}{s}\right\} \frac{\mathrm{d} \eta_{n}}{\mathrm{~d} y_{n}} \frac{\mathrm{d} y_{n}}{\mathrm{~d} a_{n}} \nabla_{\mathbf{w}} a_{n} \\
& =\sum_{n=1}^{N} \frac{1}{s}\left\{t_{n}-y_{n}\right\} \psi^{\prime}\left(y_{n}\right) f^{\prime}\left(a_{n}\right) \phi_{n}
\end{aligned}
$$

where $a_{n}=\mathbf{w}^{\mathrm{T}} \boldsymbol{\phi}_{n}$, and we have used $y_{n}=f\left(a_{n}\right)$ together with the result (5.90) for $\mathbb{E}[t \mid \eta]$. We now see that there is a considerable simplification if we choose a particular form for the link function $f^{-1}(y)$ given by

$$
f^{-1}(y)=\psi(y)
$$

which gives $f(\psi(y))=y$ and hence $f^{\prime}(\psi) \psi^{\prime}(y)=1$. Also, because $a=f^{-1}(y)$, we have $a=\psi$ and hence $f^{\prime}(a) \psi^{\prime}(y)=1$. In this case, the gradient of the error function reduces to

$$
\nabla \ln E(\mathbf{w})=\frac{1}{s} \sum_{n=1}^{N}\left\{y_{n}-t_{n}\right\} \boldsymbol{\phi}_{n}
$$

We have seen that there is a natural pairing between the choice of error function and the choice of output-unit activation function. Although we have derived this result in the context of single-layer network models, the same considerations apply to deep neural networks discussed in later chapters.


![](https://cdn.mathpix.com/cropped/2024_05_26_a79f6f03ec68f3fd25e6g-1.jpg?height=664&width=1450&top_left_y=212&top_left_x=152

ChatGPT figure/image summary: The image contains two diagrams illustrating the concept of ambiguous regions that can arise when constructing multi-class classifiers from combinations of two-class discriminants. The diagrams are designed to visually explain the challenges encountered in multi-class classification when using a one-versus-the-rest approach (on the left) and a one-versus-one approach (on the right).

On the left side of the image, there are three regions labeled \( R1 \), \( R2 \), and \( R3 \), each corresponding to a different class represented by \( C1 \), \( C2 \), and not \( C1 \) or not \( C2 \) respectively. The green shaded area marks the ambiguous region where the classification is uncertain because it is the intersection of the regions where a point is neither \( C1 \) nor \( C2 \) explicitly. This demonstrates the challenge with the one-versus-the-rest approach, where there could be areas of the input space that do not get a clear class assignment.

On the right side of the image, a different scenario is depicted involving three discriminant functions used to separate each pair of classes, \( C1 \), \( C2 \), and \( C3 \). In this one-versus-one approach, the green shaded area in the center illustrates an ambiguous region once again. This area is the intersection of the decision boundaries, which shows the possible confusion in class assignments that could arise from this method.

Both diagrams use solid and dashed red lines to represent the decision boundaries between the classes or comparisons in question. The question mark in the green area in both diagrams emphasizes the ambiguity in classifying points that fall within these regions. The diagrams serve to show why solely relying on these methods can lead to areas of input space where the class label is ambiguous and highlights the need for other approaches to construct a robust multi-class classifier.)

Figure 5.2 Attempting to construct a $K$-class discriminant from a set of two-class discriminant functions leads to ambiguous regions, as shown in green. On the left is an example with two discriminant functions designed to distinguish points in class $\mathcal{C}_{k}$ from points not in class $\mathcal{C}_{k}$. On the right is an example involving three discriminant functions each of which is used to separate a pair of classes $\mathcal{C}_{k}$ and $\mathcal{C}_{j}$.

In this case, the decision surfaces are $D$-dimensional hyperplanes passing through the origin of the $(D+1)$-dimensional expanded input space.

\title{
5.1.2 Multiple classes
}

Now consider the extension of linear discriminant functions to $K>2$ classes. We might be tempted to build a $K$-class discriminant by combining a number of two-class discriminant functions. However, this leads to some serious difficulties (Duda and Hart, 1973), as we now show.

Consider a model with $K-1$ classifiers, each of which solves a two-class problem of separating points in a particular class $\mathcal{C}_{k}$ from points not in that class. This is known as a one-versus-the-rest classifier. The left-hand example in Figure 5.2 shows an example involving three classes where this approach leads to regions of input space that are ambiguously classified.

An alternative is to introduce $K(K-1) / 2$ binary discriminant functions, one for every possible pair of classes. This is known as a one-versus-one classifier. Each point is then classified according to a majority vote amongst the discriminant functions. However, this too runs into the problem of ambiguous regions, as illustrated in the right-hand diagram of Figure 5.2.

We can avoid these difficulties by considering a single $K$-class discriminant comprising $K$ linear functions of the form

$$
y_{k}(\mathbf{x})=\mathbf{w}_{k}^{\mathrm{T}} \mathbf{x}+w_{k 0}
$$

and then assigning a point $\mathbf{x}$ to class $\mathcal{C}_{k}$ if $y_{k}(\mathbf{x})>y_{j}(\mathbf{x})$ for all $j \neq k$. The decision boundary between class $\mathcal{C}_{k}$ and class $\mathcal{C}_{j}$ is therefore given by $y_{k}(\mathbf{x})=y_{j}(\mathbf{x})$ and

Figure 5.3 Illustration of the decision regions for a multi-class linear discriminant, with the decision boundaries shown in red. If two points $\mathrm{x}_{\mathrm{A}}$ and $\mathrm{x}_{\mathrm{B}}$ both lie inside the same decision region $\mathcal{R}_{k}$, then any point $\widehat{\mathrm{x}}$ that lies on the line connecting these two points must also lie in $\mathcal{R}_{k}$, and hence, the decision region must be singly connected and convex.

![](https://cdn.mathpix.com/cropped/2024_05_26_c6820e8ed9a153596826g-1.jpg?height=418&width=581&top_left_y=211&top_left_x=1065

ChatGPT figure/image summary: The image is a diagrammatic representation of decision boundaries in a multi-class classification scenario. It illustrates a two-dimensional input space that has been partitioned into three distinct decision regions, each corresponding to a different class. These regions are labeled as \( R_i \), \( R_j \), and \( R_k \). The decision boundaries are indicated by the red lines, which demarcate the regions where a different class is the most likely classification.

Superimposed on the diagram are two points, labeled as \( x_A \) and \( x_B \), connected by a blue line with an intermediate point \( \widehat{x} \) lying on this line. As per the explanatory text, this might indicate that any point along the line connecting points \( x_A \) and \( x_B \) is also within the same decision region, demonstrating the concept of convexity and single connectedness of the decision region \( R_k \) to which both points belong. 

This visual is used to help explain why the decision regions of a discriminant comprising multiple linear functions form singly connected, convex shapes in the input space.)

hence corresponds to a $(D-1)$-dimensional hyperplane defined by

$$
\left(\mathbf{w}_{k}-\mathbf{w}_{j}\right)^{\mathrm{T}} \mathbf{x}+\left(w_{k 0}-w_{j 0}\right)=0
$$

This has the same form as the decision boundary for the two-class case discussed in Section 5.1.1, and so analogous geometrical properties apply.

The decision regions of such a discriminant are always singly connected and convex. To see this, consider two points $\mathrm{x}_{\mathrm{A}}$ and $\mathrm{x}_{\mathrm{B}}$ both of which lie inside decision region $\mathcal{R}_{k}$, as illustrated in Figure 5.3. Any point $\widehat{\mathbf{x}}$ that lies on the line connecting $\mathbf{x}_{\mathrm{A}}$ and $\mathbf{x}_{\mathrm{B}}$ can be expressed in the form

$$
\widehat{\mathbf{x}}=\lambda \mathbf{x}_{\mathrm{A}}+(1-\lambda) \mathbf{x}_{\mathrm{B}}
$$

where $0 \leqslant \lambda \leqslant 1$. From the linearity of the discriminant functions, it follows that

$$
y_{k}(\widehat{\mathbf{x}})=\lambda y_{k}\left(\mathbf{x}_{\mathrm{A}}\right)+(1-\lambda) y_{k}\left(\mathbf{x}_{\mathrm{B}}\right)
$$

Because both $\mathbf{x}_{\mathrm{A}}$ and $\mathbf{x}_{\mathrm{B}}$ lie inside $\mathcal{R}_{k}$, it follows that $y_{k}\left(\mathbf{x}_{\mathrm{A}}\right)>y_{j}\left(\mathbf{x}_{\mathrm{A}}\right)$ and that $y_{k}\left(\mathbf{x}_{\mathrm{B}}\right)>y_{j}\left(\mathbf{x}_{\mathrm{B}}\right)$, for all $j \neq k$, and hence $y_{k}(\widehat{\mathbf{x}})>y_{j}(\widehat{\mathbf{x}})$, and so $\widehat{\mathbf{x}}$ also lies inside $\mathcal{R}_{k}$. Thus, $\mathcal{R}_{k}$ is singly connected and convex.

Note that for two classes, we can either employ the formalism discussed here, based on two discriminant functions $y_{1}(\mathbf{x})$ and $y_{2}(\mathbf{x})$, or else use the simpler but essentially equivalent formulation based on a single discriminant function $y(\mathbf{x})$.

\title{
5.1.3 1-of- $K$ coding
}

For regression problems, the target variable $\mathbf{t}$ was simply the vector of real numbers whose values we wish to predict. In classification, there are various ways of using target values to represent class labels. For two-class problems, the most convenient is the binary representation in which there is a single target variable $t \in\{0,1\}$ such that $t=1$ represents class $\mathcal{C}_{1}$ and $t=0$ represents class $\mathcal{C}_{2}$. We can interpret the value of $t$ as the probability that the class is $\mathcal{C}_{1}$, with the probability values taking only the extreme values of 0 and 1 . For $K>2$ classes, it is convenient to use a 1 -of- $K$ coding scheme, also known as the one-hot encoding scheme, in which $\mathbf{t}$ is a vector of length $K$ such that if the class is $\mathcal{C}_{j}$, then all elements $t_{k}$ of $\mathbf{t}$ are zero

Section 4.1.3

Exercise 5.1 except element $t_{j}$, which takes the value 1 . For instance, if we have $K=5$ classes, then a data point from class 2 would be given the target vector

$$
\mathbf{t}=(0,1,0,0,0)^{\mathrm{T}}
$$

Again, we can interpret the value of $t_{k}$ as the probability that the class is $\mathcal{C}_{k}$ in which the probabilities take only the values 0 and 1 .

\subsection*{5.1.4 Least squares for classification}

With linear regression models, the minimization of a sum-of-squares error function leads to a simple closed-form solution for the parameter values. It is therefore tempting to see if we can apply the same least-squares formalism to classification problems. Consider a general classification problem with $K$ classes and a 1 -of- $K$ binary coding scheme for the target vector $t$. One justification for using least squares in such a context is that it approximates the conditional expectation $\mathbb{E}[\mathbf{t} \mid \mathbf{x}]$ of the target values given the input vector. For a binary coding scheme, this conditional expectation is given by the vector of posterior class probabilities. Unfortunately, these probabilities are typically approximated rather poorly, and indeed the approximations can have values outside the range $(0,1)$. However, it is instructional to explore these simple models and to understand how these limitations arise.

Each class $\mathcal{C}_{k}$ is described by its own linear model so that

$$
y_{k}(\mathbf{x})=\mathbf{w}_{k}^{\mathrm{T}} \mathbf{x}+w_{k 0}
$$

where $k=1, \ldots, K$. We can conveniently group these together using vector notation so that

$$
\mathbf{y}(\mathbf{x})=\widetilde{\mathbf{W}}^{\mathrm{T}} \widetilde{\mathbf{x}}
$$

where $\widetilde{\mathbf{W}}$ is a matrix whose $k$ th column comprises the $(D+1)$-dimensional vector $\widetilde{\mathbf{w}}_{k}=\left(w_{k 0}, \mathbf{w}_{k}^{\mathrm{T}}\right)^{\mathrm{T}}$ and $\widetilde{\mathbf{x}}$ is the corresponding augmented input vector $\left(1, \mathbf{x}^{\mathrm{T}}\right)^{\mathrm{T}}$ with a dummy input $x_{0}=1$. A new input $\mathbf{x}$ is then assigned to the class for which the output $y_{k}=\widetilde{\mathbf{w}}_{k}^{\mathrm{T}} \widetilde{\mathbf{x}}$ is largest.

We now determine the parameter matrix $\widetilde{\mathbf{W}}$ by minimizing a sum-of-squares error function. Consider a training data set $\left\{\mathbf{x}_{n}, \mathbf{t}_{n}\right\}$ where $n=1, \ldots, N$, and define a matrix $\mathbf{T}$ whose $n$th row is the vector $\mathbf{t}_{n}^{\mathrm{T}}$, together with a matrix $\widetilde{\mathbf{X}}$ whose $n$th row is $\widetilde{\mathbf{x}}_{n}^{\mathrm{T}}$. The sum-of-squares error function can then be written as

$$
E_{D}(\widetilde{\mathbf{W}})=\frac{1}{2} \operatorname{Tr}\left\{(\widetilde{\mathbf{X}} \widetilde{\mathbf{W}}-\mathbf{T})^{\mathrm{T}}(\widetilde{\mathbf{X}} \widetilde{\mathbf{W}}-\mathbf{T})\right\}
$$

Setting the derivative with respect to $\widetilde{\mathbf{W}}$ to zero and rearranging, we obtain the solution for $\widetilde{\mathbf{W}}$ in the form

$$
\widetilde{\mathbf{W}}=\left(\widetilde{\mathbf{X}}^{\mathrm{T}} \widetilde{\mathbf{X}}\right)^{-1} \widetilde{\mathbf{X}}^{\mathrm{T}} \mathbf{T}=\widetilde{\mathbf{X}}^{\dagger} \mathbf{T}
$$

Section 4.1.3

where $\widetilde{\mathbf{X}}^{\dagger}$ is the pseudo-inverse of the matrix $\widetilde{\mathbf{X}}$. We then obtain the discriminant

function in the form

$$
\mathbf{y}(\mathbf{x})=\widetilde{\mathbf{W}}^{\mathrm{T}} \widetilde{\mathbf{x}}=\mathbf{T}^{\mathrm{T}}\left(\widetilde{\mathbf{X}}^{\dagger}\right)^{\mathrm{T}} \widetilde{\mathbf{x}}
$$

An interesting property of least-squares solutions with multiple target variables is that if every target vector in the training set satisfies some linear constraint

$$
\mathbf{a}^{\mathrm{T}} \mathbf{t}_{n}+b=0
$$

for some constants a and $b$, then the model prediction for any value of $\mathrm{x}$ will satisfy

Exercise 5.3

Section 2.3 .4

Section 5.4.3

$$
\mathbf{a}^{\mathrm{T}} \mathbf{y}(\mathbf{x})+b=0
$$

Thus, if we use a 1 -of- $K$ coding scheme for $K$ classes, then the predictions made by the model will have the property that the elements of $\mathbf{y}(\mathbf{x})$ will sum to 1 for any value of $\mathbf{x}$. However, this summation constraint alone is not sufficient to allow the model outputs to be interpreted as probabilities because they are not constrained to lie within the interval $(0,1)$.

The least-squares approach gives an exact closed-form solution for the discriminant function parameters. However, even as a discriminant function (where we use it to make decisions directly and dispense with any probabilistic interpretation), it suffers from some severe problems. We have seen that the sum-of-squares error function can be viewed as the negative log likelihood under the assumption of a Gaussian noise distribution. If the true distribution of the data is markedly different from being Gaussian, then least squares can give poor results. In particular, least squares is very sensitive to the presence of outliers, which are data points located a long way from the bulk of the data. This is illustrated in Figure 5.4. Here we see that the additional data points in the right-hand figure produce a significant change in the location of the decision boundary, even though these points would be correctly classified by the original decision boundary in the left-hand figure. The sum-of-squares error function gives too much weight to data points that are a long way from the decision boundary, even though they are correctly classified. Outliers can arise due to rare events or may simply be due to mistakes in the data set. Techniques that are sensitive to a very few data points are said to lack robustness. For comparison, Figure 5.4 also shows results from a technique called logistic regression, which is more robust to outliers.

The failure of least squares should not surprise us when we recall that it corresponds to maximum likelihood under the assumption of a Gaussian conditional distribution, whereas binary target vectors clearly have a distribution that is far from Gaussian. By adopting more appropriate probabilistic models, we can obtain classification techniques with much better properties than least squares, and which can also be generalized to give flexible nonlinear neural network models, as we will see in later chapters.


![](https://cdn.mathpix.com/cropped/2024_05_26_eb0b6807a540759d07d1g-1.jpg?height=706&width=1470&top_left_y=238&top_left_x=151

ChatGPT figure/image summary: The image displays two plots which illustrate the decision boundaries for a classification problem with two classes. The two classes of data points are represented by red crosses and blue circles. On the left plot, a magenta curve and a green curve indicate the decision boundaries resulting from two different classification methods: least squares and logistic regression, respectively. On the right plot, additional data points have been added to the bottom right corner, showing how the magenta decision boundary from the least squares method has been significantly influenced by these outliers, moving away from the original position seen in the left plot. The green decision boundary from the logistic regression method appears to be much less affected by these added points, indicating its robustness to outliers. This visual demonstrates how the least squares method can be sensitive to data points that lie far from the main cluster of data, potentially leading to less reliable classification results compared to logistic regression, which seems more resilient to such anomalies.)

Figure 5.4 The left-hand plot shows data from two classes, denoted by red crosses and blue circles, together with the decision boundaries found by least squares (magenta curve) and by a logistic regression model (green curve). The right-hand plot shows the corresponding results obtained when extra data points are added at the bottom right of the diagram, showing that least squares is highly sensitive to outliers, unlike logistic regression.

\title{
5.2. Decision Theory
}

When we discussed linear regression we saw how the process of making predictions

Section 4.2 in machine learning can be broken down into the two stages of inference and decision. We now explore this perspective in much greater depth specifically in the context of classifiers.

Suppose we have an input vector $\mathbf{x}$ together with a corresponding vector $\mathbf{t}$ of target variables, and our goal is to predict $\mathbf{t}$ given a new value for $\mathbf{x}$. For regression problems, $\mathbf{t}$ will comprise continuous variables and in general will be a vector as we may wish to predict several related quantities. For classification problems, $\mathbf{t}$ will represent class labels. Again, $\mathbf{t}$ will in general be a vector if we have more than two classes. The joint probability distribution $p(\mathbf{x}, \mathbf{t})$ provides a complete summary of the uncertainty associated with these variables. Determining $p(\mathbf{x}, \mathbf{t})$ from a set of training data is an example of inference and is typically a very difficult problem whose solution forms the subject of much of this book. In a practical application, however, we must often make a specific prediction for the value of $t$ or more generally take a specific action based on our understanding of the values $t$ is likely to take, and this aspect is the subject of decision theory.

Consider, for example, our earlier medical diagnosis problem in which we have taken an image of a skin lesion on a patient, and we wish to determine whether the patient has cancer. In this case, the input vector $\mathbf{x}$ is the set of pixel intensities in

the image, and the output variable $t$ will represent the absence of cancer, which we denote by the class $\mathcal{C}_{1}$, or the presence of cancer, which we denote by the class $\mathcal{C}_{2}$. We might, for instance, choose $t$ to be a binary variable such that $t=0$ corresponds to class $\mathcal{C}_{1}$ and $t=1$ corresponds to class $\mathcal{C}_{2}$. We will see later that this choice of label values is particularly convenient when working with probabilities. The general inference problem then involves determining the joint distribution $p\left(\mathbf{x}, \mathcal{C}_{k}\right)$, or equivalently $p(\mathbf{x}, t)$, which gives us the most complete probabilistic description of the variables. Although this can be a very useful and informative quantity, ultimately, we must decide either to give treatment to the patient or not, and we would like this choice to be optimal according to some appropriate criterion (Duda and Hart, 1973). This is the decision step, and the aim of decision theory is that it should tell us how to make optimal decisions given the appropriate probabilities. We will see that the decision stage is generally very simple, even trivial, once we have solved the inference problem. Here we give an introduction to the key ideas of decision theory as required for the rest of the book. Further background, as well as more detailed accounts, can be found in Berger (1985) and Bather (2000).

Before giving a more detailed analysis, let us first consider informally how we might expect probabilities to play a role in making decisions. When we obtain the skin image $\mathrm{x}$ for a new patient, our goal is to decide which of the two classes to assign the image to. We are therefore interested in the probabilities of the two classes, given the image, which are given by $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$. Using Bayes' theorem, these probabilities can be expressed in the form

$$
p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)=\frac{p\left(\mathbf{x} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right)}{p(\mathbf{x})}
$$

Note that any of the quantities appearing in Bayes' theorem can be obtained from the joint distribution $p\left(\mathbf{x}, \mathcal{C}_{k}\right)$ by either marginalizing or conditioning with respect to the appropriate variables. We can now interpret $p\left(\mathcal{C}_{k}\right)$ as the prior probability for the class $\mathcal{C}_{k}$ and $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$ as the corresponding posterior probability. Thus, $p\left(\mathcal{C}_{1}\right)$ represents the probability that a person has cancer, before the image is taken. Similarly, $p\left(\mathcal{C}_{1} \mid \mathbf{x}\right)$ is the posterior probability, revised using Bayes' theorem in light of the information contained in the image. If our aim is to minimize the chance of assigning $\mathrm{x}$ to the wrong class, then intuitively we would choose the class having the higher posterior probability. We now show that this intuition is correct, and we also discuss more general criteria for making decisions.

\title{
5.2.1 Misclassification rate
}

Suppose that our goal is simply to make as few misclassifications as possible. We need a rule that assigns each value of $\mathrm{x}$ to one of the available classes. Such a rule will divide the input space into regions $\mathcal{R}_{k}$ called decision regions, one for each class, such that all points in $\mathcal{R}_{k}$ are assigned to class $\mathcal{C}_{k}$. The boundaries between decision regions are called decision boundaries or decision surfaces. Note that each decision region need not be contiguous but could comprise some number of disjoint regions. To find the optimal decision rule, consider first the case of two classes, as in the cancer problem, for instance. A mistake occurs when an input vector belonging


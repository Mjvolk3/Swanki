![](https://cdn.mathpix.com/cropped/2024_05_18_d7abda89797ce8f663e5g-1.jpg?height=1248&width=1224&top_left_y=216&top_left_x=421

ChatGPT figure/image summary: The image appears to be a cropped photograph of a page from a book or a document, with the highlight being the title "The Deep Learning Revolution" shown in a large red font, placed over a colorful abstract background. The number '1' indicates that this is likely the first chapter or first section of the document. It's suggesting a focus on the impact and transformation that deep learning has had on the field of technology and artificial intelligence.)

Machine learning today is one of the most important, and fastest growing, fields of technology. Applications of machine learning are becoming ubiquitous, and solutions learned from data are increasingly displacing traditional hand-crafted algorithms. This has not only led to improved performance for existing technologies but has opened the door to a vast range of new capabilities that would be inconceivable if new algorithms had to be designed explicitly by hand.

One particular branch of machine learning, known as deep learning, has emerged as an exceptionally powerful and general-purpose framework for learning from data. Deep learning is based on computational models called neural networks which were originally inspired by mechanisms of learning and information processing in the human brain. The field of artificial intelligence, or AI, seeks to recreate the powerful capabilities of the brain in machines, and today the terms machine learning and AI are often used interchangeably. Many of the AI systems in current use represent ap-

![](https://cdn.mathpix.com/cropped/2024_05_18_a0676cf8759377514923g-1.jpg?height=977&width=1512&top_left_y=203&top_left_x=148

ChatGPT figure/image summary: The image provided is a set of four plots showing polynomial curve fitting to data points for a one-dimensional regression problem. Each plot represents a polynomial of a different order, labeled with \(M\), where \(M\) denotes the order of the polynomial. The blue points are the given data points and the red curve represents the fitted polynomial. Each plot is a visualization of how polynomials of various orders fit the data points:

- Top-left \(M=0\): This plot shows a horizontal line since a polynomial of order \(M=0\) is just a constant.
- Top-right \(M=1\): This plot shows a straight line that is fitted through the data, representing a polynomial of first order.
- Bottom-left \(M=3\): This plot includes a cubic polynomial, which fits the data more closely than the \(M=0\) and \(M=1\) models.
- Bottom-right \(M=9\): Here, there is a ninth-order polynomial that fits all the data points exactly, but oscillates wildly, which is an indication of overfitting.

The context provided in the text discusses the problem of overfitting in machine learning and illustrates it with this figure by showing a well-fitting polynomial for \(M=3\) and an overfit polynomial for \(M=9\). Overfitting happens when a model is too complex and starts to capture the noise in the data rather than just the underlying relationship.

This figure complements the text's explanation of how different complexities of model (i.e., different values of \(M\)) can affect the prediction error on both training and test data sets. It visually demonstrates the concept of overfitting that occurs when a model is too complex (such as with \(M=9\)) and captures the noise in the training data, failing to generalize well to new, unseen data.)

![](https://cdn.mathpix.com/cropped/2024_05_18_a0676cf8759377514923g-1.jpg?height=427&width=706&top_left_y=214&top_left_x=155

ChatGPT figure/image summary: The image is a plot of a polynomial fitted to a set of data points. The polynomial has an order of M=0, shown as a red horizontal line, indicating a constant function. The data points are represented by blue dots on a graph that plots the variable 't' on the vertical axis against 'x' on the horizontal axis. The green curve represents the actual function from which the data points were generated, which, based on the context, seems to be the sine function sin(2πx). The horizontal line indicates that the model is not fitting the actual trend in the data well, as it does not capture any of the variations that the sine function exhibits.)

![](https://cdn.mathpix.com/cropped/2024_05_18_a0676cf8759377514923g-1.jpg?height=428&width=705&top_left_y=736&top_left_x=153

ChatGPT figure/image summary: The image is a graphical representation of a polynomial curve fitting exercise. The graph shows a red curve which represents a polynomial of order \( M = 3 \) fitted to a dataset illustrated by blue data points. The fitting has been done by minimizing some error function. The vertical axis is labeled "t" and the horizontal axis as "x," and the range for both axes is from 0 to 1. The blue data points appear to come from a function with a sinusoidal pattern, and the red curve attempts to capture the trend of these data points, resulting in delivering an approximation of the underlying function that generated the data.)

![](https://cdn.mathpix.com/cropped/2024_05_18_a0676cf8759377514923g-1.jpg?height=432&width=693&top_left_y=214&top_left_x=953

ChatGPT figure/image summary: The image provided is a two-dimensional plot with the x-axis labeled as "x" and the y-axis labeled as "t". It depicts a scatter plot of blue data points along with two curves. One curve is a red curve that represents a polynomial of order M = 1 fitted to the data points. The other curve appears to be a green curve that represents the true function from which the data points were likely generated or it could be a fit for a different model. This kind of visualization is typically used in machine learning to illustrate the fit of a model to data and to discuss concepts such as overfitting or underfitting, as mentioned in the provided contextual information.)

![](https://cdn.mathpix.com/cropped/2024_05_18_a0676cf8759377514923g-1.jpg?height=432&width=693&top_left_y=734&top_left_x=953

ChatGPT figure/image summary: The image contains a plot of a high-degree polynomial function fitted to a set of data points. The data points are shown as blue dots, and the polynomial function is depicted as a red curve. This plot illustrates the concept of overfitting in machine learning, where the fitted polynomial curve (of order M=9) passes through every data point, resulting in a model that is too complex for the underlying pattern it tries to capture, causing it to oscillate wildly between the points. The green curve represents the original function that generated the data, which is likely to be a sinusoid given the context (specifically, \( \sin(2 \pi x) \) as mentioned in the text). The x-axis represents the independent variable x, and the y-axis represents the target variable, marked as 't'. This example demonstrates how a more complex model does not necessarily yield a better prediction for new data points and can result in poor generalization.)

Figure 1.6 Plots of polynomials having various orders $M$, shown as red curves, fitted to the data set shown in Figure 1.4 by minimizing the error function (1.2).

passes exactly through each data point and $E\left(\mathbf{w}^{\star}\right)=0$. However, the fitted curve oscillates wildly and gives a very poor representation of the function $\sin (2 \pi x)$. This latter behaviour is known as over-fitting.

Our goal is to achieve good generalization by making accurate predictions for new data. We can obtain some quantitative insight into the dependence of the generalization performance on $M$ by considering a separate set of data known as a test set, comprising 100 data points generated using the same procedure as used to generate the training set points. For each value of $M$, we can evaluate the residual value of $E\left(\mathbf{w}^{\star}\right)$ given by (1.2) for the training data, and we can also evaluate $E\left(\mathbf{w}^{\star}\right)$ for the test data set. Instead of evaluating the error function $E(\mathbf{w})$, it is sometimes more convenient to use the root-mean-square (RMS) error defined by

$$
E_{\mathrm{RMS}}=\sqrt{\frac{1}{N} \sum_{n=1}^{N}\left\{y\left(x_{n}, \mathbf{w}\right)-t_{n}\right\}^{2}}
$$

in which the division by $N$ allows us to compare different sizes of data sets on an equal footing, and the square root ensures that $E_{\mathrm{RMS}}$ is measured on the same scale (and in the same units) as the target variable $t$. Graphs of the training-set and test-set

Figure 1.7 Graphs of the root-meansquare error, defined by ( 1.3 ), evaluated on the training set, and on an independent test set, for various values of $M$.

![](https://cdn.mathpix.com/cropped/2024_05_18_9b0445fe9c08724522fdg-1.jpg?height=428&width=879&top_left_y=216&top_left_x=779

ChatGPT figure/image summary: The provided images appear to be figures and tables from an academic paper or textbook related to machine learning or statistical modeling. Here's what each image represents:

1. The first image shows a plot of polynomials of various orders \(M\) fitted to a data set. These polynomial functions are depicted as red curves, likely plotted over data points, illustrating how they fit the given dataset with increased complexity as \(M\) increases.

2. The second image is the same as the first and shows one of the polynomial fits in greater detail.

3. The third image is also the same as the first and second, showing another polynomial fit to the data set in greater detail.

4. The fourth image is again the same as those above, highlighting one of the polynomial fits which is likely to represent overfitting due to its oscillatory behavior.

5. The fifth image also falls in line with the previous images, likely illustrating the same concept from a different angle or focus, perhaps zooming in on a different section of the polynomial’s behavior.

6. The sixth image is a graph of the root-mean-square (RMS) error for both a training set and a test set plotted against various values of \(M\). This shows how the error changes with the complexity of the polynomial model, indicating overfitting when \(M\) is too large and underfitting when \(M\) is too small.

7. The final image (Figure 1.8) presents plots of solutions using an \(M=9\) polynomial fitted to datasets of different sizes: \(N=15\) data points in the left plot and \(N=100\) data points in the right plot. These plots demonstrate how increasing the dataset's size can mitigate the overfitting problem. 

All these images relate to the understanding and demonstration of overfitting in predictive modeling, emphasizing the importance of balancing model complexity with the ability to generalize to new data.)

RMS errors are shown, for various values of $M$, in Figure 1.7. The test set error is a measure of how well we are doing in predicting the values of $t$ for new data observations of $x$. Note from Figure 1.7 that small values of $M$ give relatively large values of the test set error, and this can be attributed to the fact that the corresponding polynomials are rather inflexible and are incapable of capturing the oscillations in the function $\sin (2 \pi x)$. Values of $M$ in the range $3 \leqslant M \leqslant 8$ give small values for the test set error, and these also give reasonable representations of the generating function $\sin (2 \pi x)$, as can be seen for $M=3$ in Figure 1.6.

For $M=9$, the training set error goes to zero, as we might expect because this polynomial contains 10 degrees of freedom corresponding to the 10 coefficients $w_{0}, \ldots, w_{9}$, and so can be tuned exactly to the 10 data points in the training set. However, the test set error has become very large and, as we saw in Figure 1.6, the corresponding function $y\left(x, \mathbf{w}^{\star}\right)$ exhibits wild oscillations.

This may seem paradoxical because a polynomial of a given order contains all lower-order polynomials as special cases. The $M=9$ polynomial is therefore capable of generating results at least as good as the $M=3$ polynomial. Furthermore, we might suppose that the best predictor of new data would be the function $\sin (2 \pi x)$ from which the data was generated (and we will see later that this is indeed the case). We know that a power series expansion of the function $\sin (2 \pi x)$ contains terms of all orders, so we might expect that results should improve monotonically as we increase $M$.

We can gain some insight into the problem by examining the values of the coefficients $\mathbf{w}^{\star}$ obtained from polynomials of various orders, as shown in Table 1.1. We see that, as $M$ increases, the magnitude of the coefficients typically gets larger. In particular for the $M=9$ polynomial, the coefficients have become finely tuned to the data. They have large positive and negative values so that the corresponding polynomial function matches each of the data points exactly, but between data points (particularly near the ends of the range) the function exhibits the large oscillations observed in Figure 1.6. Intuitively, what is happening is that the more flexible polynomials with larger values of $M$ are increasingly tuned to the random noise on the target values.

Further insight into this phenomenon can be gained by examining the behaviour of the learned model as the size of the data set is varied, as shown in Figure 1.8. We see that, for a given model complexity, the over-fitting problem become less severe


![](https://cdn.mathpix.com/cropped/2024_05_18_0cdb432046472a497b67g-1.jpg?height=458&width=1512&top_left_y=200&top_left_x=148

ChatGPT figure/image summary: The image you provided displays two plots illustrating the results of fitting a ninth-order polynomial to two different datasets, one with 15 data points (left plot) and one with 100 data points (right plot). On both plots, the blue dots represent the data points, and there are two curves shown – presumably the green one represents the true underlying function \( \sin(2\pi x) \), and the red curve represents the fitted $M=9$ polynomial curve resulting from minimizing the sum-of-squares error function.

The left plot demonstrates overfitting for the smaller dataset with N=15, where the red curve passes through or very close to all the data points, causing it to exhibit large oscillations that do not reflect the true underlying green sine wave pattern well.

In contrast, the right plot shows that when the dataset is larger with N=100, the overfitting problem is mitigated, and the red polynomial curve provides a better approximation of the green sine wave, smoothly capturing the general trend of the data with less overfitting to the individual points.

These plots are used to illustrate the concept that increasing the size of the training dataset can help reduce the problem of overfitting, even when using a complex model with many parameters.)

Figure 1.8 Plots of the solutions obtained by minimizing the sum-of-squares error function (1.2) using the $M=9$ polynomial for $N=15$ data points (left plot) and $N=100$ data points (right plot). We see that increasing the size of the data set reduces the over-fitting problem.

as the size of the data set increases. Another way to say this is that with a larger data set, we can afford to fit a more complex (in other words more flexible) model to the data. One rough heuristic that is sometimes advocated in classical statistics is that the number of data points should be no less than some multiple (say 5 or 10) of the number of learnable parameters in the model. However, when we discuss deep learning later in this book, we will see that excellent results can be obtained using models that have significantly more parameters than the number of training data points.

\title{
1.2.5 Regularization
}

There is something rather unsatisfying about having to limit the number of parameters in a model according to the size of the available training set. It would seem more reasonable to choose the complexity of the model according to the complexity of the problem being solved. One technique that is often used to control the overfitting phenomenon, as an alternative to limiting the number of parameters, is that of regularization, which involves adding a penalty term to the error function (1.2) to discourage the coefficients from having large magnitudes. The simplest such penalty

Table 1.1 Table of the coefficients $\mathbf{w}^{\star}$ for polynomials of various order. Observe how the typical magnitude of the coefficients increases dramatically as the order of the polynomial increases.

\begin{tabular}{r|rrrr} 
& $M=0$ & $M=1$ & $M=3$ & $M=9$ \\
\hline$w_{0}^{\star}$ & 0.11 & 0.90 & 0.12 & 0.26 \\
$w_{1}^{\star}$ & & -1.58 & 11.20 & -66.13 \\
$w_{2}^{\star}$ & & & -33.67 & $1,665.69$ \\
$w_{3}^{\star}$ & & & 22.43 & $-15,566.61$ \\
$w_{4}^{\star}$ & & & & $76,321.23$ \\
$w_{5}^{\star}$ & & & & $-217,389.15$ \\
$w_{6}^{\star}$ & & & & $370,626.48$ \\
$w_{7}^{\star}$ & & & & $-372,051.47$ \\
$w_{8}^{\star}$ & & & & $202,540.70$ \\
$w_{9}^{\star}$ & & & & $-46,080.94$
\end{tabular}


![](https://cdn.mathpix.com/cropped/2024_05_18_e829ee8c78472bc3e50eg-1.jpg?height=448&width=1510&top_left_y=208&top_left_x=148

ChatGPT figure/image summary: The image contains two plots side by side. Both graphs depict curves that represent polynomial fits to a set of data points which are shown as blue dots.

On the left plot, we see a curve (possibly in red) closely following the trajectory of the blue data points, along with another smoother curve (possibly in green) that looks like a generalized fit to the data. The plot is labeled with "ln λ = -18", indicating that this is the curve resulting from fitting the M=9 polynomial to the data using a regularized error function with the natural logarithm of the regularization parameter λ being -18.

On the right plot, we similarly see the blue data points and two curves. However, the fit here seems less optimal, with the curve (possibly in red) showing relatively large deviations from the data points when compared to the left plot. This plot is labeled with "ln λ = 0", suggesting that it corresponds to a regularized fit with a different value of the regularization parameter λ.

The context suggests that these plots are used to illustrate the effects of regularization on polynomial fitting with the aim of controlling the overfitting phenomenon. The left plot with "ln λ = -18" displays a better fit, indicating that this level of regularization helps to suppress overfitting. In contrast, the right plot with "ln λ = 0" indicates a poorer fit, suggesting that excessive regularization can lead to underfitting.)

Figure 1.9 Plots of $M=9$ polynomials fitted to the data set shown in Figure 1.4 using the regularized error function (1.4) for two values of the regularization parameter $\lambda$ corresponding to $\ln \lambda=-18$ and $\ln \lambda=0$. The case of no regularizer, i.e., $\lambda=0$, corresponding to $\ln \lambda=-\infty$, is shown at the bottom right of Figure 1.6 .

term takes the form of the sum of the squares of all of the coefficients, leading to a modified error function of the form

$$
\widetilde{E}(\mathbf{w})=\frac{1}{2} \sum_{n=1}^{N}\left\{y\left(x_{n}, \mathbf{w}\right)-t_{n}\right\}^{2}+\frac{\lambda}{2}\|\mathbf{w}\|^{2}
$$

where $\|\mathbf{w}\|^{2} \equiv \mathbf{w}^{\mathrm{T}} \mathbf{w}=w_{0}^{2}+w_{1}^{2}+\ldots+w_{M}^{2}$, and the coefficient $\lambda$ governs the relative importance of the regularization term compared with the sum-of-squares error term. Note that often the coefficient $w_{0}$ is omitted from the regularizer because its inclusion causes the results to depend on the choice of origin for the target variable (Hastie, Tibshirani, and Friedman, 2009), or it may be included but with its own

Section 9.2.1 Exercise 4.2 regularization coefficient. Again, the error function in (1.4) can be minimized exactly in closed form. Techniques such as this are known in the statistics literature as shrinkage methods because they reduce the value of the coefficients. In the context of neural networks, this approach is known as weight decay because the parameters in a neural network are called weights and this regularizer encourages them to decay towards zero.

Figure 1.9 shows the results of fitting the polynomial of order $M=9$ to the same data set as before but now using the regularized error function given by (1.4). We see that, for a value of $\ln \lambda=-18$, the over-fitting has been suppressed and we now obtain a much closer representation of the underlying function $\sin (2 \pi x)$. If, however, we use too large a value for $\lambda$ then we again obtain a poor fit, as shown in Figure 1.9 for $\ln \lambda=0$. The corresponding coefficients from the fitted polynomials are given in Table 1.2, showing that regularization has the desired effect of reducing the magnitude of the coefficients.

The impact of the regularization term on the generalization error can be seen by plotting the value of the RMS error (1.3) for both training and test sets against $\ln \lambda$, as shown in Figure 1.10. We see that $\lambda$ now controls the effective complexity of the model and hence determines the degree of over-fitting.

Figure 1.10 Graph of the root-meansquare error (1.3) versus $\ln \lambda$ for the $M=9$ polynomial.

![](https://cdn.mathpix.com/cropped/2024_05_18_990fac6c15f219991e40g-1.jpg?height=440&width=884&top_left_y=212&top_left_x=779

ChatGPT figure/image summary: The image displays a plot with two curves, one represented in red and labeled as "Training" and the other in blue labeled as "Test." The horizontal axis is labeled with '\(M\)' and ranges approximately from -30 to 0. The vertical axis is labeled with 'E_{RMS}', which likely stands for the root-mean-square error, and ranges from 0 to about 0.6. 

The plot shows how the root-mean-square error (E_{RMS}) for both training and testing sets changes as the logarithm of the regularization parameter (denoted by 'ln λ') varies. The red curve represents the error on the training set, and the blue curve represents the error on the test set.

The 'Training' curve begins high on the left side, decreases sharply as \(M\) increases (moving rightward on the axis), then rises again as \(M\) approaches zero. The 'Test' curve follows a similar trend, but it remains below the 'Training' curve for the left part of the graph, crosses the 'Training' curve at a certain point, and then becomes higher as it approaches the middle. After crossing over each other, both curves rise towards the right side of the graph.

This plot is designed to illustrate the concept of model complexity and its effect on both training and validation errors. It underscores an essential concept in machine learning that choosing the appropriate level of model complexity can help balance fitting the training data well while still maintaining good generalization to new, unseen data.)

\title{
1.2.6 Model selection
}

The quantity $\lambda$ is an example of a hyperparameter whose values are fixed during the minimization of the error function to determine the model parameters $\mathrm{w}$. We cannot simply determine the value of $\lambda$ by minimizing the error function jointly with respect to $\mathbf{w}$ and $\lambda$ since this will lead to $\lambda \rightarrow 0$ and an over-fitted model with small or zero training error. Similarly, the order $M$ of the polynomial is a hyperparameter of the model, and simply optimizing the training set error with respect to $M$ will lead to large values of $M$ and associated over-fitting. We therefore need to find a way to determine suitable values for hyperparameters. The results above suggest a simple way of achieving this, namely by taking the available data and partitioning it into a training set, used to determine the coefficients $\mathbf{w}$, and a separate validation set, also called a hold-out set or a development set. We then select the model having the lowest error on the validation set. If the model design is iterated many times using a data set of limited size, then some over-fitting to the validation data can occur, and so it may be necessary to keep aside a third test set on which the performance of the selected model can finally be evaluated.

For some applications, the supply of data for training and testing will be limited. To build a good model, we should use as much of the available data as possible for training. However, if the validation set is too small, it will give a relatively noisy estimate of predictive performance. One solution to this dilemma is to use cross-

Table 1.2 Table of the coefficients $\mathrm{w}^{\star}$ for $M=9$ polynomials with various values for the regularization parameter $\lambda$. Note that $\ln \lambda=-\infty$ corresponds to a model with no regularization, i.e., to the graph at the bottom right in Figure 1.6. We see that, as the value of $\lambda$ increases, the magnitude of a typical coefficient gets smaller.

\begin{tabular}{c|rrr} 
& $\ln \lambda=-\infty$ & $\ln \lambda=-18$ & $\ln \lambda=0$ \\
\hline$w_{0}^{\star}$ & 0.26 & 0.26 & 0.11 \\
$w_{1}^{\star}$ & -66.13 & 0.64 & -0.07 \\
$w_{2}^{\star}$ & $1,665.69$ & 43.68 & -0.09 \\
$w_{3}^{\star}$ & $-15,566.61$ & -144.00 & -0.07 \\
$w_{4}^{\star}$ & $76,321.23$ & 57.90 & -0.05 \\
$w_{5}^{\star}$ & $-217,389.15$ & 117.36 & -0.04 \\
$w_{6}^{\star}$ & $370,626.48$ & 9.87 & -0.02 \\
$w_{7}^{\star}$ & $-372,051.47$ & -90.02 & -0.01 \\
$w_{8}^{\star}$ & $202,540.70$ & -70.90 & -0.01 \\
$w_{9}^{\star}$ & $-46,080.94$ & 75.26 & 0.00
\end{tabular}

Figure 1.11 The technique of $S$-fold cross-validation, illustrated here for the case of $S=4$, involves taking the available data and partitioning it into $S$ groups of equal size. Then $S-1$ of the groups

![](https://cdn.mathpix.com/cropped/2024_05_18_00737bf1ec602cb9d4a6g-1.jpg?height=74&width=410&top_left_y=217&top_left_x=1131

ChatGPT figure/image summary: The image appears to represent a segment of Figure 1.11 referenced in the text, showing an illustration of the technique of S-fold cross-validation, particularly for the case of S=4. It should depict the data partitioning process in which the available dataset is divided into four groups of equal size. The colored (likely red) section represents the 'held-out' group, which is not used in the training set for a specific run and is instead used for validation. The rest of the segments (white or uncolored) are used for training the model. This procedure is repeated for all S possible combinations to ensure every group is used for validation once.

However, since the image provided is small and only shows a part of one of the runs, without additional context it is difficult to determine more detail. The image likely corresponds to one of the four runs mentioned in the text, where the different runs have one of the four segments colored to represent the validation set for that particular run.)

run 1

![](https://cdn.mathpix.com/cropped/2024_05_18_00737bf1ec602cb9d4a6g-1.jpg?height=78&width=416&top_left_y=293&top_left_x=1128

ChatGPT figure/image summary: I'm sorry, but there is no image of Figure 1.10 in the content you've provided. You have included textual content that mentions a graph of the root-mean-square error versus the natural logarithm of the hyperparameter lambda for an M=9 polynomial, which is expected to be in Figure 1.10. However, you haven’t shared the actual image of that figure. If you would like me to analyze the mentioned figure, please provide the appropriate image.)

run 2 are used to train a set of models that are then evaluated on the remaining group. This procedure is then repeated for all $S$ possible choices for the held-out group, indicated here by the

![](https://cdn.mathpix.com/cropped/2024_05_18_00737bf1ec602cb9d4a6g-1.jpg?height=71&width=403&top_left_y=375&top_left_x=1127

ChatGPT figure/image summary: It appears that there has been a mistake in providing the relevant context for the image. You've given a detailed context about the importance of selecting hyperparameters in machine learning, including regularization parameters (like \(\lambda\)) and model complexity (like the polynomial order \(M\)), and you've discussed how validation sets, cross-validation, and specifically \(S\)-fold cross-validation can be used to assess model performance without overfitting.

However, the image provided at the end—a simple 4-block structure with one block filled in red—looks like a visual representation of one run in an \(S\)-fold cross-validation process. This illustration seems to correspond to the description of \(S\)-fold cross-validation from the text, where the red block represents the portion of the data held out for validation during that specific run. Since the context refers to run 3, this illustration likely depicts the third iteration of the cross-validation process, with the data being divided into 4 parts and the third part being used for validation.

The originally requested Figure 1.10, which should depict a graph of the root-mean-square error versus \(\ln \lambda\) for the \(M=9\) polynomial, is not present here. Without the specific image of that graph, I can't comment on its content. If you can provide the correct image for Figure 1.10, I would be able to help describe it.)
red blocks, and the performance scores from run 3

![](https://cdn.mathpix.com/cropped/2024_05_18_00737bf1ec602cb9d4a6g-1.jpg?height=71&width=410&top_left_y=453&top_left_x=1131

ChatGPT figure/image summary: The image appears to be a graphic or diagram containing a sequence of blocks. There are four blocks aligned horizontally, each representing a portion or segment of data (such as in a dataset). The fourth block from the left is colored in red, which typically highlights or distinguishes it from the other blocks. This coloring might indicate that this particular block is set apart for a specific purpose, such as validation or testing in a machine learning context. This is consistent with the text mentioning cross-validation and the use of hold-out groups, where the red blocks signify the data used for testing or validation during a specific run of a cross-validation process. However, without further context from the surrounding text or figure caption, I cannot provide more details about the specific meaning or significance of this image.)
run 4 the $S$ runs are then averaged.

validation, which is illustrated in Figure 1.11. This allows a proportion $(S-1) / S$ of the available data to be used for training while making use of all of the data to assess performance. When data is particularly scarce, it may be appropriate to consider the case $S=N$, where $N$ is the total number of data points, which gives the leave-oneout technique.

The main drawback of cross-validation is that the number of training runs that must be performed is increased by a factor of $S$, and this can prove problematic for models in which the training is itself computationally expensive. A further problem with techniques such as cross-validation that use separate data to assess performance is that we might have multiple complexity hyperparameters for a single model (for instance, there might be several regularization hyperparameters). Exploring combinations of settings for such hyperparameters could, in the worst case, require a number of training runs that is exponential in the number of hyperparameters. The state of the art in modern machine learning involves extremely large models, trained on commensurately large data sets. Consequently, there is limited scope for exploration of hyperparameter settings, and heavy reliance is placed on experience obtained with smaller models and on heuristics.

This simple example of fitting a polynomial to a synthetic data set generated from a sinusoidal function has illustrated many key ideas from machine learning, and we will make further use of this example in future chapters. However, realworld applications of machine learning differ in several important respects. The size of the data sets used for training can be many orders of magnitude larger, and there will generally be many more input variables, perhaps numbering in the millions for image analysis, for example, as well as multiple output variables. The learnable function that relates outputs to inputs is governed by a class of models known as neural networks, and these may have a large number of parameters perhaps numbering in the hundreds of billions, and the error function will be a highly nonlinear function of those parameters. The error function can no longer be minimized through a closed-form solution and instead must be minimized through iterative optimization techniques based on evaluation of the derivatives of the error function with respect to the parameters, all of which may require specialist computational hardware and incur substantial computational cost.

Figure 1.12 Schematic illustration showing two neurons from the human brain. These electrically active cells communicate through junctions called synapses whose strengths change as the network learns.

![](https://cdn.mathpix.com/cropped/2024_05_18_3d9cdec5c9bee0eb2fccg-1.jpg?height=481&width=886&top_left_y=233&top_left_x=739

ChatGPT figure/image summary: The image you've provided shows a schematic diagram of two neurons from the human brain. These are the basic processing units in the brain, and are electrically active cells that communicate with each other through synapses. The diagram illustrates the various components of a neuron, including the cell body, dendrites, axon, and synapses. The cell body is the central part of the neuron containing the nucleus, the dendrites are branching structures that receive electrical signals from other neurons, the axon is a long projection that transmits signals to other neurons, and the synapses are the junctures where the axon terminal of one neuron communicates with the dendrite or cell body of another neuron, typically via chemical neurotransmitters. This communication process is crucial for the functioning of neural networks in the brain and forms the biological basis of learning, memory, and information processing.)

\title{
1.3. A Brief History of Machine Learning
}

Machine learning has a long and rich history, including the pursuit of multiple alternative approaches. Here we focus on the evolution of machine learning methods based on neural networks as these represent the foundation of deep learning and have proven to be the most effective approach to machine learning for real-world applications.

Neural network models were originally inspired by studies of information processing in the brains of humans and other mammals. The basic processing units in the brain are electrically active cells called neurons, as illustrated in Figure 1.12. When a neuron 'fires', it sends an electrical impulse down the axon where it reaches junctions, called synapses, which form connections with other neurons. Chemical signals called neurotransmitters are released at the synapses, and these can stimulate, or inhibit, the firing of subsequent neurons.

A human brain contains around 90 billion neurons in total, each of which has on average several thousand synapses with other neurons, creating a complex network having a total of around 100 trillion $\left(10^{14}\right)$ synapses. If a particular neuron receives sufficient stimulation from the firing of other neurons then it too can be induced to fire. However, some synapses have a negative, or inhibitory, effect whereby the firing of the input neuron makes it less likely that the output neuron will fire. The extent to which one neuron can cause another to fire depends on the strength of the synapse, and it is changes in these strengths that represents a key mechanism whereby the brain can store information and learn from experience.

These properties of neurons have been captured in very simple mathematical models, known as artificial neural networks, which then form the basis for computational approaches to learning (McCulloch and Pitts, 1943). Many of these models describe the properties of a single neuron by forming a linear combination of the outputs of other neurons, which is then transformed using a nonlinear function. This

Figure 1.13 A simple neural network diagram representing the transformations (1.5) and (1.6) describing a single neuron. The polynomial function (1.1) can be seen as a special case of this model.

![](https://cdn.mathpix.com/cropped/2024_05_18_e3e9e09029c9f9357332g-1.jpg?height=338&width=379&top_left_y=212&top_left_x=1281

ChatGPT figure/image summary: As the provided text does not specifically describe the content of the image, and the given image is not the one described in the contextual information (Figure 1.12), I can only describe the image seen here directly.

The image is a diagram of a simple neural network. It represents a neuron's structure in an artificial neural network, which is akin to the simplified mathematical model of a biological neuron. In this model, there are several inputs labeled \( x_1, x_2, \ldots, x_M \), each of which is connected to an output neuron labeled \( y \). Each input is connected to the output via connections labeled with weights \( w_1, w_2, \ldots, w_M \). The outputs of the input neurons are multiplied by their respective weights and then summed together to produce the pre-activation \( a \), as indicated in the earlier text. This pre-activation value is then passed through a nonlinear activation function \( f \) to produce the output \( y \). This type of network is a one-layer perceptron model as it has only a single layer of processing (the transformation from the inputs to the output).)

can be expressed mathematically in the form

$$
\begin{aligned}
a & =\sum_{i=1}^{M} w_{i} x_{i} \\
y & =f(a)
\end{aligned}
$$

where $x_{1}, \ldots, x_{M}$ represent $M$ inputs corresponding to the activities of other neurons that send connections to this neuron, and $w_{1}, \ldots, w_{M}$ are continuous variables, called weights, which represent the strengths of the associated synapses. The quantity $a$ is called the pre-activation, the nonlinear function $f(\cdot)$ is called the activation function, and the output $y$ is called the activation. We can see that the polynomial (1.1) can be viewed as a specific instance of this representation in which the inputs $x_{i}$ are given by powers of a single variable $x$, and the function $f(\cdot)$ is just the identity $f(a)=a$. The simple mathematical formulation given by (1.5) and (1.6) has formed the basis of neural network models from the 1960s up to the present day, and can be represented in diagram form as shown in Figure 1.13.

\title{
1.3.1 Single-layer networks
}

The history of artificial neural networks can broadly be divided into three distinct phases according to the level of sophistication of the networks as measured by the number of 'layers' of processing. A simple neural model described by (1.5) and (1.6) can be viewed as having a single layer of processing corresponding to the single layer of connections in Figure 1.13. One of the most important such models in the history of neural computing is the perceptron (Rosenblatt, 1962) in which the activation function $f(\cdot)$ is a step function of the form

$$
f(a)= \begin{cases}0, & \text { if } a \leqslant 0 \\ 1, & \text { if } a>0\end{cases}
$$

This can be viewed as a simplified model of neural firing in which a neuron fires if, and only if, the total weighted input exceeds a threshold of 0 . The perceptron was pioneered by Rosenblatt (1962), who developed a specific training algorithm that has the interesting property that if there exists a set of weight values for which the perceptron can achieve perfect classification of its training data then the algorithm is guaranteed to find the solution in a finite number of steps (Bishop, 2006). As well as a learning algorithm, the perceptron also had a dedicated analogue hardware


![](https://cdn.mathpix.com/cropped/2024_05_18_5a226dd1c9d81d9fa045g-1.jpg?height=392&width=1538&top_left_y=214&top_left_x=110

ChatGPT figure/image summary: The image is a triptych of black and white photographs illustrating components of the Mark 1 perceptron hardware, described in the provided text.

The photograph on the left shows a person using a camera system that captures an image of a printed character, which is being illuminated by lights. The image is then focused onto a 20x20 array of photocells, effectively creating a primitive 400-pixel image.

The middle photograph displays what appears to be a patch board densely filled with wires. This component was used to test different configurations of input features, and in the perceptron, these configurations were often wired randomly to demonstrate the machine's learning capabilities independent of precise wiring patterns.

The photograph on the right features an individual adjusting one of several rotary variable resistors, known as potentiometers, which are connected to electric motors. This hardware was used to implement the learnable weights of the perceptron, allowing automatic adjustment of the weights by the learning algorithm.

These images provide visual context to the early days of artificial neural networks and machine learning, showcasing the perceptron's physical implementation, which was groundbreaking at the time.)

Figure 1.14 Illustration of the Mark 1 perceptron hardware. The photograph on the left shows how the inputs were obtained using a simple camera system in which an input scene, in this case a printed character, was illuminated by powerful lights, and an image focused onto a $20 \times 20$ array of cadmium sulphide photocells, giving a primitive 400 -pixel image. The perceptron also had a patch board, shown in the middle photograph, which allowed different configurations of input features to be tried. Often these were wired up at random to demonstrate the ability of the perceptron to learn without the need for precise wiring, in contrast to a modern digital computer. The photograph on the right shows one of the racks of learnable weights. Each weight was implemented using a rotary variable resistor, also called a potentiometer, driven by an electric motor thereby allowing the value of the weight to be adjusted automatically by the learning algorithm.

implementation, as shown in Figure 1.14. A typical perceptron configuration had multiple layers of processing, but only one of those layers was learnable from data, and so the perceptron is considered to be a 'single-layer' neural network.

At first, the ability of perceptrons to learn from data in a brain-like way was considered remarkable. However, it became apparent that the model also has major limitations. The properties of perceptrons were analysed by Minsky and Papert (1969), who gave formal proofs of the limited capabilities of single-layer networks. Unfortunately, they also speculated that similar limitations would extend to networks having multiple layers of learnable parameters. Although this latter conjecture proved to be wildly incorrect, the effect was to dampen enthusiasm for neural network models, and this contributed to the lack of interest, and funding, for neural networks during the 1970s and early 1980s. Furthermore, researchers were unable to explore the properties of multilayered networks due to the lack of an effective algorithm for training them, since techniques such as the perceptron algorithm were specific to single-layer models. Note that although perceptrons have long disappeared from practical machine learning, the name lives on because a modern neural network is also sometimes called a multilayer perceptron or MLP.

\title{
1.3.2 Backpropagation
}

The solution to the problem of training neural networks having more than one layer of learnable parameters came from the use of differential calculus and the application of gradient-based optimization methods. An important change was to replace the step function (1.7) with continuous differentiable activation functions having a non-zero gradient. Another key modification was to introduce differentiable error functions that define how well a given choice of parameter values predicts the target variables in the training set. We saw an example of such an error function when we

Figure 1.15 A neural network having two layers of parameters in which arrows denote the direction of information flow through the network. Each of the hidden units and each of the output units computes a function of the form given by (1.5) and (1.6) in which the activation function $f(\cdot)$ is differentiable.

![](https://cdn.mathpix.com/cropped/2024_05_18_a86eb08e4ac380f84a91g-1.jpg?height=493&width=669&top_left_y=230&top_left_x=975

ChatGPT figure/image summary: The given image is a simplified schematic representation of a feed-forward neural network. It shows three levels or layers of units: inputs on the left, hidden units in the middle, and outputs on the right. Each input unit is connected to every hidden unit, indicating that the value of each input node is transmitted to all of the hidden units. Similarly, each hidden unit is connected to every output unit, representing how the processed information from the hidden layer is passed on to the output layer. The arrows symbolize the direction of data flow through the network: from the input units through the hidden units and finally to the output units. This kind of network architecture is commonly used in machine learning to model complex functions and make predictions or decisions based on input data.)

Section 1.2.3

Chapter 8

Chapter 7 used the sum-of-squares error function (1.2) to fit polynomials.

With these changes, we now have an error function whose derivatives with respect to each of the parameters in the network can be evaluated. We can now consider networks having more than one layer of parameters. Figure 1.15 shows a simple network with two processing layers. Nodes in the middle layer called hidden units because their values do not appear in the training set, which only provides values for inputs and outputs. Each of the hidden units and each of the output units in Figure 1.15 computes a function of the form given by (1.5) and (1.6). For a given set of input values, the states of all of the hidden and output units can be evaluated by repeated application of (1.5) and (1.6) in which information is flowing forward through the network in the direction of the arrows. For this reason, such models are sometimes also called feed-forward neural networks.

To train such a network the parameters are first initialized using a random number generator and are then iteratively updated using gradient-based optimization techniques. This involves evaluating the derivatives of the error function, which can be done efficiently in a process known as error backpropagation. In backpropagation, information flows backwards through the network from the outputs towards the inputs (Rumelhart, Hinton, and Williams, 1986). There exist many different optimization algorithms that make use of gradients of the function to be optimized, but the one that is most prevalent in machine learning is also the simplest and is known as stochastic gradient descent.

The ability to train neural networks having multiple layers of weights was a breakthrough that led to a resurgence of interest in the field starting around the mid1980s. This was also a period in which the field moved beyond a focus on neurobiological inspiration and developed a more rigorous and principled foundation (Bishop, 1995b). In particular, it was recognized that probability theory, and ideas from the field of statistics, play a central role in neural networks and machine learning. One key insight is that learning from data involves background assumptions, sometimes called prior knowledge or inductive biases. These might be incorporated explicitly, for example by designing the structure of a neural network such that the classification of a skin lesion does not depend on the location of the lesion within the image, or they might take the form of implicit assumptions that arise from the mathematical

plications of machine learning which are designed to solve very specific and focused problems, and while these are extremely useful they fall far short of the tremendous breadth of capabilities of the human brain. This has led to the introduction of the term artificial general intelligence, or AGI, to describe the aspiration of building machines with this much greater flexibility. After many decades of steady progress, machine learning has now entered a phase of very rapid development. Recently,

Chapter 12 massive deep learning systems called large language models have started to exhibit remarkable capabilities that have been described as the first indications of artificial general intelligence (Bubeck et al., 2023).

\title{
1.1. The Impact of Deep Learning
}

We begin our discussion of machine learning by considering four examples drawn from diverse fields to illustrate the huge breadth of applicability of this technology and to introduce some basic concepts and terminology. What is particularly remarkable about these and many other examples is that they have all been addressed using variants of the same fundamental framework of deep learning. This is in sharp contrast to conventional approaches in which different applications are tackled using widely differing and specialist techniques. It should be emphasized that the examples we have chosen represent only a tiny fraction of the breadth of applicability for deep neural networks and that almost every domain where computation has a role is amenable to the transformational impact of deep learning.

\subsection*{1.1.1 Medical diagnosis}

Consider first the application of machine learning to the problem of diagnosing skin cancer. Melanoma is the most dangerous kind of skin cancer but is curable if detected early. Figure 1.1 shows example images of skin lesions, with malignant melanomas on the top row and benign nevi on the bottom row. Distinguishing between these two classes of image is clearly very challenging, and it would be virtually impossible to write an algorithm by hand that could successfully classify such images with any reasonable level of accuracy.

This problem has been successfully addressed using deep learning (Esteva $e t$ al., 2017). The solution was created using a large set of lesion images, known as

Figure 1.1 Examples of skin lesions corresponding to dangerous malignant melanomas on the top row and benign nevi on the bottom row. It is difficult for the untrained eye to distinguish between these two classes.

![](https://cdn.mathpix.com/cropped/2024_05_18_b4242664bcc6213fcfe3g-1.jpg?height=391&width=770&top_left_y=1717&top_left_x=873

ChatGPT figure/image summary: The image shown is a set of photographs displaying skin lesions. The lesions are categorized into two groups to illustrate the challenges in diagnosing skin cancer through visual inspection. The top row contains images of malignant melanomas, which are a dangerous form of skin cancer that can be cured if recognized and treated early. The bottom row shows images of benign nevi, which are harmless. Differentiating between the two can be very difficult by visual examination alone, highlighting the importance of machine learning approaches like deep learning for accurate medical diagnosis. This example demonstrates how deep learning can be applied to medical imaging to assist in identifying skin cancer, among other potential applications.)

form of the model or the way it is trained.

The development of backpropagation and gradient-based optimization dramatically increased the capability of neural networks to solve practical problems. However, it was also observed that in networks with many layers, it was only weights in the final two layers that would learn useful values. With a few exceptions, notably models used for image analysis known as convolutional neural networks (LeCun et al., 1998), there were very few successful applications of networks having more than two layers. Again, this constrained the complexity of the problems that could be addressed effectively with these kinds of network. To achieve reasonable performance on many applications, it was necessary to use hand-crafted pre-processing to transform the input variables into some new space where, it was hoped, the machine learning problem would be easier to solve. This pre-processing stage is sometimes also called feature extraction. Although this approach was sometimes effective, it would clearly be much better if features could be learned from the data rather than being hand-crafted.

By the start of the new millennium, the available neural network methods were once again reaching the limits of their capability. Researchers began to explore a raft of alternatives to neural networks, such as kernel methods, support vector machines, Gaussian processes, and many others. Neural networks fell into disfavour once again, although a core of enthusiastic researchers continued to pursue the goal of a truly effective approach to training networks with many layers.

\title{
1.3.3 Deep networks
}

The third, and current, phase in the development of neural networks began during the second decade of the 21st century. A series of developments allowed neural networks with many layers of weights to be trained effectively, thereby removing previous limitations on the capabilities of these techniques. Networks with many layers of weights are called deep neural networks and the sub-field of machine learning that focuses on such networks is called deep learning (LeCun, Bengio, and Hinton, 2015).

One important theme in the origins of deep learning was a significant increase in the scale of neural networks, measured in terms of the number of parameters. Although networks with a few hundred or a few thousand parameters were common in the 1980 s, this steadily rose to the millions, and then billions, whereas current stateof-the-art models can have in the region of one trillion $\left(10^{12}\right)$ parameters. Networks with many parameters require commensurately large data sets so that the training signals can produced good values for those parameters. The combination of massive models and massive data sets in turn requires computation on a massive scale when training the model. Specialist processors called graphics processing units, or GPUs, which had been developed for very fast rendering of graphical data for applications such as video games, proved to be well suited to the training of neural networks because the functions computed by the units in one layer of a network can be evaluated in parallel, and this maps well onto the massive parallelism of GPUs (Krizhevsky, Sutskever, and Hinton, 2012). Today, training for the largest models is performed on large arrays of thousands of GPUs linked by specialist high-speed interconnections.

![](https://cdn.mathpix.com/cropped/2024_05_18_dc0381fb1e39cc4997a4g-1.jpg?height=996&width=1470&top_left_y=225&top_left_x=171

ChatGPT figure/image summary: The image shows a plot illustrating the number of compute cycles required to train state-of-the-art neural network models over time, from around the 1960s to the present. The vertical axis represents the number of petaflop/s-days on a logarithmic scale, indicating the computational cost of training, while the horizontal axis represents time by year.

The plot has several labeled points that correspond to significant milestones in the development of neural network models, such as the Perceptron, LeNet-5, AlexNet, and more recent advances like AlphaGo Zero. Notably, there are two lines indicating periods of exponential growth in computational requirements: one with a doubling time of approximately two years, consistent with Moore's Law, and the more recent deep learning era showing a much steeper growth with a doubling time of 3.4 months.

Key models and milestones in machine learning and neural network development are highlighted on the plot, and two distinct epochs in the growth of computational need are visible, separated into a "First Era" and "Modern Era." The Modern Era showcases a rapid increase in computation demand for training deep neural networks, reflecting the advances and scaling described in the provided text.)

Figure 1.16 Plot of the number of compute cycles, measured in petaflop/s-days, needed to train a state-of-theart neural network as a function of date, showing two distinct phases of exponential growth. [From OpenAl with permission.]

Figure 1.16 illustrates how the number of compute cycles needed to train a stateof-the-art neural network has grown over the years, showing two distinct phases of growth. The vertical axis has an exponential scale and has units of petaflop/s-days, where a petaflop represents $10^{15}$ (a thousand trillion) floating point operations, and a petaflop/s is one petaflop per second. One petaflop/s-day represents computation at the rate of a petaflop/s for a period of 24 hours, which is roughly $10^{20}$ floating point operations, and therefore, the top line of the graph represents an impressive $10^{24}$ floating point operations. A straight line on the graph represents exponential growth, and we see that from the era of the perceptron up to around 2012, the doubling time was around 2 years, which is consistent with the general growth of computing power as a consequence of Moore's law. From 2012 onward, which marks the era of deep learning, we again see exponential growth but the doubling time is now 3.4 months corresponding to a factor of 10 increase in compute power every year!

It is often found that improvements in performance due to innovations in the architecture or incorporation of more sophisticated forms of inductive bias are soon

Section 12.3 .5

Section 10.3

Section 9.5 superseded simply by scaling up the quantity of training data, along with commensurate scaling of the model size and associated compute power used for training (Sutton, 2019). Not only can large models have superior performance on a specific task but they may be capable of solving a broader range of different problems with the same trained neural network. Large language models are a notable example as a single network not only has an extraordinary breadth of capability but is even able to outperform specialist networks designed to solve specific problems.

We have seen that depth plays an important role in allowing neural networks to achieve high performance. One way to view the role of the hidden layers in a deep neural network is that of representation learning (Bengio, Courville, and Vincent, 2012) in which the network learns to transform input data into a new representation that is semantically meaningful thereby creating a much easier problem for the final layer or layers to solve. Such internal representations can be repurposed to allow for the solution of related problems through transfer learning, as we saw for skin lesion classification. It is interesting to note that neural networks used to process images may learn internal representations that are remarkably like those observed in the mammalian visual cortex. Large neural networks that can be adapted or fine-tuned to a range of downstream tasks are called foundation models, and can take advantage of large, heterogeneous data sets to create models having broad applicability (Bommasani et al., 2021).

In addition to scaling, there were other developments that helped in the success of deep learning. For example, in simple neural networks, the training signals become weaker as they are backpropagated through successive layers of a deep network. One technique for addressing this is the introduction of residual connections (He et al., 2015a) that facilitate the training of networks having hundreds of layers. Another key development was the introduction of automatic differentiation methods in which the code that performs backpropagation to evaluate error function gradients is generated automatically from the code used to specify the forward propagation. This allows researchers to experiment rapidly with different architectures for a neural network and to combine different architectural elements in multiple ways very easily since only the relatively simple forward propagation functions need to be coded explicitly. Also, much of the research in machine learning has been conducted through open source, allowing researchers to build on the work of others, thereby further accelerating the rate of progress in the field.

a training set, each of which is labelled as either malignant or benign, where the labels are obtained from a biopsy test that is considered to provide the true class of the lesion. The training set is used to determine the values of some 25 million adjustable parameters, known as weights, in a deep neural network. This process of setting the parameter values from data is known as learning or training. The goal is for the trained network to predict the correct label for a new lesion just from the image alone without needing the time-consuming step of taking a biopsy. This is an example of a supervised learning problem because, for each training example, the network is told the correct label. It is also an example of a classification problem because each input must be assigned to a discrete set of classes (benign or malignant in this case). Applications in which the output consists of one or more continuous variables are called regression problems. An example of a regression problem would be the prediction of the yield in a chemical manufacturing process in which the inputs consist of the temperature, the pressure, and the concentrations of reactants.

An interesting aspect of this application is that the number of labelled training images available, roughly 129,000 , is considered relatively small, and so the deep neural network was first trained on a much larger data set of 1.28 million images of everyday objects (such as dogs, buildings, and mushrooms) and then fine-tuned on the data set of lesion images. This is an example of transfer learning in which the network learns the general properties of natural images from the large data set of everyday objects and is then specialized to the specific problem of lesion classification. Through the use of deep learning, the classification of skin lesion images has reached a level of accuracy that exceeds that of professional dermatologists (Brinker et al., 2019).

\title{
1.1.2 Protein structure
}

Proteins are sometimes called the building blocks of living organisms. They are biological molecules that consist of one or more long chains of units called amino acids, of which there are 22 different types, and the protein is specified by the sequence of amino acids. Once a protein has been synthesized inside a living cell, it folds into a complex three-dimensional structure whose behaviour and interactions are strongly determined by its shape. Calculating this 3D structure, given the amino acid sequence, has been a fundamental open problem in biology for half a century that had seen relatively little progress until the advent of deep learning.

The 3D structure can be measured experimentally using techniques such as Xray crystallography, cryogenic electron microscopy, or nuclear magnetic resonance spectroscopy. However, this can be extremely time-consuming and for some proteins can prove to be challenging, for example due to the difficulty of obtaining a pure sample or because the structure is dependent on the context. In contrast, the amino acid sequence of a protein can be determined experimentally at lower cost and higher throughput. Consequently, there is considerable interest in being able to predict the 3D structures of proteins directly from their amino acid sequences in order to better understand biological processes or for practical applications such as drug discovery. A deep learning model can be trained to take an amino acid sequence as input and generate the $3 \mathrm{D}$ structure as output, in which the training data

Figure 1.2 Illustration of the 3D shape of a protein called T1044/6VR4. The green structure shows the ground truth as determined by X-ray crystallography, whereas the superimposed blue structure shows the prediction obtained by a deep learning model called AlphaFold. [From Jumper et al. (2021) with permission.]

![](https://cdn.mathpix.com/cropped/2024_05_18_d0b5a498105d07217267g-1.jpg?height=637&width=640&top_left_y=226&top_left_x=1009

ChatGPT figure/image summary: The image shows the three-dimensional structure of a protein. The green structure represents the actual 3D conformation as determined by X-ray crystallography, which is considered the "ground truth" for the protein's shape. Superimposed on it in blue is the predicted structure as generated by a deep learning model, likely AlphaFold, as mentioned in the provided context. The close alignment of the two structures suggests that the deep learning model is very accurate in predicting the protein's 3D structure from its amino acid sequence.)

consist of a set of proteins for which the amino acid sequence and the 3D structure are both known. Protein structure prediction is therefore another example of supervised learning. Once the system is trained it can take a new amino acid sequence as input and can predict the associated 3D structure (Jumper et al., 2021). Figure 1.2 compares the predicted 3D structure of a protein and the ground truth obtained by X-ray crystallography.

\title{
1.1.3 Image synthesis
}

In the two applications discussed so far, a neural network learned to transform an input (a skin image or an amino acid sequence) into an output (a lesion classification or a 3D protein structure, respectively). We turn now to an example where the training data consist simply of a set of sample images and the goal of the trained network is to create new images of the same kind. This is an example of unsupervised learning because the images are unlabelled, in contrast to the lesion classification and protein structure examples. Figure 1.3 shows examples of synthetic images generated by a deep neural network trained on a set of images of human faces taken in a studio against a plain background. Such synthetic images are of exceptionally high quality and it can be difficult tell them apart from photographs of real people.

This is an example of a generative model because it can generate new output examples that differ from those used to train the model but which share the same statistical properties. A variant of this approach allows images to be generated that depend on an input text string known, as a prompt, so that the image content reflects

Chapter 10 the semantics of the text input. The term generative $A I$ is used to describe deep learning models that generate outputs in the form of images, video, audio, text, candidate drug molecules, or other modalities.

![](https://cdn.mathpix.com/cropped/2024_05_18_f994bbac8ad9a581d276g-1.jpg?height=777&width=1521&top_left_y=222&top_left_x=148

ChatGPT figure/image summary: The image displays a grid containing eight portraits of individuals' faces. The grid is arranged in two rows, with four images each, showing a diverse variety of facial characteristics, hairstyles, and expressions. These faces appear to be created using a deep neural network and represent artificial, synthetic human images. The technology behind their creation involves generative models, which, after being trained on numerous real photographs, can produce highly realistic yet nonexistent human likenesses. These models are commonly used as examples of unsupervised learning in the field of artificial intelligence.)

Figure 1.3 Synthetic face images generated by a deep neural network trained using unsupervised learning. [From https://generated.photos.]

\title{
1.1.4 Large language models
}

One of most important advances in machine learning in recent years has been the development of powerful models for processing natural language and other forms of sequential data such as source code. A large language model, or LLM, uses deep learning to build rich internal representations that capture the semantic properties of language. An important class of large language models, called autoregressive language models, can generate language as output, and therefore, they are a form of generative AI. Such models take a sequence of words as the input and for the output, generate a single word that represents the next word in the sequence. The augmented sequence, with the new word appended at the end, can then be fed through the model again to generate the subsequent word, and this process can be repeated to generate a long sequence of words. Such models can also output a special 'stop' word that signals the end of text generation, thereby allowing them to output text of finite length and then halt. At that point, a user could append their own series of words to the sequence before feeding the complete sequence back through the model to trigger further word generation. In this way, it is possible for a human to have a conversation with the neural network.

Such models can be trained on large data sets of text by extracting training pairs each consisting of a randomly selected sequence of words as input with the known next word as the target output. This is an example of self-supervised learning in which a function from inputs to outputs is learned but where the labelled outputs are obtained automatically from the input training data without needing separate human-

Figure 1.4 Plot of a training data set of $N=$ 10 points, shown as blue circles, each comprising an observation of the input variable $x$ along with the corresponding target variable $t$. The green curve shows the function $\sin (2 \pi x)$ used to generate the data. Our goal is to predict the value of $t$ for some new value of $x$, without knowledge of the green curve.

![](https://cdn.mathpix.com/cropped/2024_05_18_c2d6dddf0a986a1f7ca9g-1.jpg?height=430&width=706&top_left_y=215&top_left_x=956

ChatGPT figure/image summary: The image shows a plot of a synthetic data set used for illustrative purposes in machine learning. On the horizontal axis labeled "x," we see values ranging from 0 to 1. On the vertical axis labeled "t," we see values ranging from approximately -1 to 1. There are 10 blue points plotted on the graph, each corresponding to a pair of values (x, t). These represent the data points in the synthetic data set.

Additionally, there is a smooth green curve passing through the data points. This curve represents the function \(\sin(2\pi x)\), which was used to generate the target variable 't' for each observation of the input variable 'x'. The goal mentioned in the contextual information is to predict the value of 't' for new values of 'x', based on this training data set, without having explicit knowledge of the green sinusoidal curve that was used to generate the data.

The exercise demonstrates concepts in machine learning such as supervised learning, generalization, and fitting a model to the data to enable predictions.)

derived labels. Since large volumes of text are available from multiple sources, this approach allows for scaling to very large training sets and associated very large neural networks.

Large language models can exhibit extraordinary capabilities that have been described as the first indications of emerging artificial general intelligence (Bubeck et al., 2023), and we discuss such models at length later in the book. On the next page, we give an illustration of language generation, based on a model called GPT-4 (OpenAI, 2023), in response to an input prompt 'Write a proof of the fact that there are infinitely many primes; do it in the style of a Shakespeare play through a dialogue between two parties arguing over the proof.'.

\title{
1.2. A Tutorial Example
}

For the newcomer to the field of machine learning, many of the basic concepts and much of the terminology can be introduced in the context of a simple example involving the fitting of a polynomial to a small synthetic data set (Bishop, 2006). This is a form of supervised learning problem in which we would like to make a prediction for a target variable, given the value of an input variable.

\subsection*{1.2.1 Synthetic data}

We denote the input variable by $x$ and the target variable by $t$, and we assume that both variables take continuous values on the real axis. Suppose that we are given a training set comprising $N$ observations of $x$, written $x_{1}, \ldots, x_{N}$, together with corresponding observations of the values of $t$, denoted $t_{1}, \ldots, t_{N}$. Our goal is to predict the value of $t$ for some new value of $x$. The ability to make accurate predictions on previously unseen inputs is a key goal in machine learning and is known as generalization.

We can illustrate this using a synthetic data set generated by sampling from a sinusoidal function. Figure 1.4 shows a plot of a training set comprising $N=10$ data points in which the input values were generated by choosing values of $x_{n}$, for $n=$ $1, \ldots, N$, spaced uniformly in the range $[0,1]$. The associated target data values were obtained by first computing the values of the function $\sin (2 \pi x)$ for each value of $x$

\title{
GPT-4: Proof of infinitely many primes
}

```
FIRST PARTY:
Thou dost not understand, my friend,
There simply is no upper end
To primes, those numbers indivisible,
No matter if it seems impossible.
SECOND PARTY:
But how dost thou so surely know?
To prove this truth, what canst thou show?
FIRST PARTY:
Consider this, my doubtful peer,
A clever proof that will make clear:
Assume that there's a final prime,
The largest one we'll see in time.
Let's call this number "P" for short,
And then, my friend, we will purport
To build a number "Q" that's new,
One larger than "P" and prime too.
SECOND PARTY:
But how, my friend, will this be done?
The proof is not yet fairly won.
FIRST PARTY:
It's simple, friend, just wait and see,
We'll multiply the primes, that's key.
All primes from two to "P" combined,
Will make this new "Q" we will find.
But one thing more we must include,
To make the proof more watertight,
We'll add a one onto the end,
And now the proof is in our sight.
SECOND PARTY:
I see it now, it's crystal clear,
For "Q" must be a prime, my dear.
It can't divide by any prime,
All smaller than itself in time.
And since we chose "P" as the last,
This proves that our assumption's past.
There is no final prime, we see,
The numbers go on endlessly.
```

Section 2.3

Chapter 2

Chapter 5

Chapter 4 and then adding a small level of random noise (governed by a Gaussian distribution) to each such point to obtain the corresponding target value $t_{n}$. By generating data in this way, we are capturing an important property of many real-world data sets, namely that they possess an underlying regularity, which we wish to learn, but that individual observations are corrupted by random noise. This noise might arise from intrinsically stochastic (i.e., random) processes such as radioactive decay but more typically is due to there being sources of variability that are themselves unobserved.

In this tutorial example we know the true process that generated the data, namely the sinusoidal function. In a practical application of machine learning, our goal is to discover the underlying trends in the data given the finite training set. Knowing the process that generated the data, however, allows us to illustrate important concepts in machine learning.

\subsection*{1.2.2 Linear models}

Our goal is to exploit this training set to predict the value $\widehat{t}$ of the target variable for some new value $\widehat{x}$ of the input variable. As we will see later, this involves implicitly trying to discover the underlying function $\sin (2 \pi x)$. This is intrinsically a difficult problem as we have to generalize from a finite data set to an entire function. Furthermore, the observed data is corrupted with noise, and so for a given $\widehat{x}$ there is uncertainty as to the appropriate value for $\widehat{t}$. Probability theory provides a framework for expressing such uncertainty in a precise and quantitative manner, whereas decision theory allows us to exploit this probabilistic representation to make predictions that are optimal according to appropriate criteria. Learning probabilities from data lies at the heart of machine learning and will be explored in great detail in this book.

To start with, however, we will proceed rather informally and consider a simple approach based on curve fitting. In particular, we will fit the data using a polynomial function of the form

$$
y(x, \mathbf{w})=w_{0}+w_{1} x+w_{2} x^{2}+\ldots+w_{M} x^{M}=\sum_{j=0}^{M} w_{j} x^{j}
$$

where $M$ is the order of the polynomial, and $x^{j}$ denotes $x$ raised to the power of $j$. The polynomial coefficients $w_{0}, \ldots, w_{M}$ are collectively denoted by the vector $\mathbf{w}$. Note that, although the polynomial function $y(x, \mathbf{w})$ is a nonlinear function of $x$, it is a linear function of the coefficients $\mathbf{w}$. Functions, such as this polynomial, that are linear in the unknown parameters have important properties, as well as significant limitations, and are called linear models.

\subsection*{1.2.3 Error function}

The values of the coefficients will be determined by fitting the polynomial to the training data. This can be done by minimizing an error function that measures the misfit between the function $y(x, \mathbf{w})$, for any given value of $\mathbf{w}$, and the training set data points. One simple choice of error function, which is widely used, is the sum of

Figure 1.5 The error function (1.2) corresponds to (one half of) the sum of the squares of the displacements (shown by the vertical green arrows) of each data point from the function $y(x, \mathbf{w})$.

![](https://cdn.mathpix.com/cropped/2024_05_18_17918633c30415faad8eg-1.jpg?height=599&width=772&top_left_y=223&top_left_x=877

ChatGPT figure/image summary: The image is a graph illustrating a curve fitting problem in the context of machine learning and polynomial regression. It shows a two-dimensional plot where the horizontal axis represents the input variable \( x \), and the vertical axis represents the target variable \( t \).

There are blue points on the graph that signify the training data. Each blue point has a specific position on the horizontal \( x \) axis and a corresponding target value on the vertical \( t \) axis.

A red continuous curve represents the polynomial function \( y(x, \mathbf{w}) \), which has been fitted to the training data. This curve is the result of using a polynomial function to model the underlying trend in the training data.

Green arrows extend vertically from each of the blue points down to the red curve. These green arrows indicate the displacements between the actual target values (\( t_n \)) from the training data and the predictions made by the fitted polynomial (\( y(x_n, \mathbf{w}) \)). The length of an arrow represents the extent to which the model's prediction deviates from the actual data point.

The purpose of the illustration is to visually represent the concept of an error function -- in this case, a sum-of-squares error function -- which measures the difference between the prediction and the actual data points. The goal in curve fitting is to adjust the coefficients of the polynomial (\( \mathbf{w} \)) to minimize the sum of the squares of these errors.)

the squares of the differences between the predictions $y\left(x_{n}, \mathbf{w}\right)$ for each data point $x_{n}$ and the corresponding target value $t_{n}$, given by

$$
E(\mathbf{w})=\frac{1}{2} \sum_{n=1}^{N}\left\{y\left(x_{n}, \mathbf{w}\right)-t_{n}\right\}^{2}
$$

where the factor of $1 / 2$ is included for later convenience. We will later derive this

Section 2.3 .4

Exercise 4.1 error function starting from probability theory. Here we simply note that it is a nonnegative quantity that would be zero if, and only if, the function $y(x, \mathbf{w})$ were to pass exactly through each training data point. The geometrical interpretation of the sum-of-squares error function is illustrated in Figure 1.5.

We can solve the curve fitting problem by choosing the value of $\mathbf{w}$ for which $E(\mathbf{w})$ is as small as possible. Because the error function is a quadratic function of the coefficients $\mathbf{w}$, its derivatives with respect to the coefficients will be linear in the elements of $\mathbf{w}$, and so the minimization of the error function has a unique solution, denoted by $\mathbf{w}^{\star}$, which can be found in closed form. The resulting polynomial is given by the function $y\left(x, \mathbf{w}^{\star}\right)$.

\title{
1.2.4 Model complexity
}

There remains the problem of choosing the order $M$ of the polynomial, and as we will see this will turn out to be an example of an important concept called model comparison or model selection. In Figure 1.6, we show four examples of the results of fitting polynomials having orders $M=0,1,3$, and 9 to the data set shown in Figure 1.4.

Notice that the constant $(M=0)$ and first-order $(M=1)$ polynomials give poor fits to the data and consequently poor representations of the function $\sin (2 \pi x)$. The third-order $(M=3)$ polynomial seems to give the best fit to the function $\sin (2 \pi x)$ of the examples shown in Figure 1.6. When we go to a much higher order polynomial ( $M=9)$, we obtain an excellent fit to the training data. In fact, the polynomial


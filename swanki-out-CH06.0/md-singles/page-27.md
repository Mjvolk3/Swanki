Exercise 6.13

Exercise 6.14

Section 5.1.3

Section 5.4.4

Chapter 9

Exercise 6.15 value \(t\) has been flipped to the wrong value (Opper and Winther, 2000). Here \(\epsilon\) may be set in advance, or it may be treated as a hyperparameter whose value is inferred from the data.

If we have \(K\) separate binary classifications to perform, then we can use a network having \(K\) outputs each of which has a logistic-sigmoid activation function. Associated with each output is a binary class label \(t_{k} \in\{0,1\}\), where \(k=1, \ldots, K\). If we assume that the class labels are independent, given the input vector, then the conditional distribution of the targets is

\[
p(\mathbf{t} \mid \mathbf{x}, \mathbf{w})=\prod_{k=1}^{K} y_{k}(\mathbf{x}, \mathbf{w})^{t_{k}}\left[1-y_{k}(\mathbf{x}, \mathbf{w})\right]^{1-t_{k}}
\]

Taking the negative logarithm of the corresponding likelihood function then gives the following error function:

\[
E(\mathbf{w})=-\sum_{n=1}^{N} \sum_{k=1}^{K}\left\{t_{n k} \ln y_{n k}+\left(1-t_{n k}\right) \ln \left(1-y_{n k}\right)\right\}
\]

where \(y_{n k}\) denotes \(y_{k}\left(\mathbf{x}_{n}, \mathbf{w}\right)\). Again, the derivative of the error function with respect to the pre-activation for a particular output unit takes the form (6.31), just as in the regression case.

\subsection*{6.4.3 multiclass classification}

Finally, we consider the standard multiclass classification problem in which each input is assigned to one of \(K\) mutually exclusive classes. The binary target variables \(t_{k} \in\{0,1\}\) have a 1 -of- \(K\) coding scheme indicating the class, and the network outputs are interpreted as \(y_{k}(\mathbf{x}, \mathbf{w})=p\left(t_{k}=1 \mid \mathbf{x}\right)\), leading to the error function (5.80), which we reproduce here:

\[
E(\mathbf{w})=-\sum_{n=1}^{N} \sum_{k=1}^{K} t_{k n} \ln y_{k}\left(\mathbf{x}_{n}, \mathbf{w}\right)
\]

The output-unit activation function, which corresponds to the canonical link, is given by the softmax function:

\[
y_{k}(\mathbf{x}, \mathbf{w})=\frac{\exp \left(a_{k}(\mathbf{x}, \mathbf{w})\right)}{\sum_{j} \exp \left(a_{j}(\mathbf{x}, \mathbf{w})\right)}
\]

which satisfies \(0 \leqslant y_{k} \leqslant 1\) and \(\sum_{k} y_{k}=1\). Note that the \(y_{k}(\mathbf{x}, \mathbf{w})\) are unchanged if a constant is added to all of the \(a_{k}(\mathbf{x}, \mathbf{w})\), causing the error function to be constant for some directions in weight space. This degeneracy is removed if an appropriate regularization term is added to the error function. Once again, the derivative of the error function with respect to the pre-activation for a particular output unit takes the familiar form (6.31).
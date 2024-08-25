application. However, these models have some severe limitations, and so we will

Section 6.3.6 begin our discussion of neural networks by exploring these limitations and understanding why it is necessary to use basis functions that are themselves learned from data. This leads naturally to a discussion of neural networks having more than one

\title{
Section 6.3 .6
} layer of learnable parameters. These are known as feed-forward networks or multilayer perceptrons. We will also discuss the benefits of having many such layers of processing, leading to the key concept of deep neural networks that now dominate the field of machine learning.

\subsection*{6.1. Limitations of Fixed Basis Functions}

\section*{Chapter 5}

Chapter 4

Section 1.2
Linear basis function models for classification are based on linear combinations of basis functions \(\phi_{j}(\mathbf{x})\) and take the form

\[
y(\mathbf{x}, \mathbf{w})=f\left(\sum_{j=1}^{M} w_{j} \phi_{j}(\mathbf{x})+w_{0}\right)
\]

where \(f(\cdot)\) is a nonlinear output activation function. Linear models for regression take the same form but with \(f(\cdot)\) replaced by the identity. These models allow for an arbitrary set of nonlinear basis functions \(\left\{\phi_{i}(\mathbf{x})\right\}\), and because of the generality of these basis functions, such models can in principle provide a solution to any regression or classification problem. This is true in a trivial sense in that if one of the basis functions corresponds to the desired input-to-output transformation, then the learnable linear layer simply has to copy the value of this basis function to the output of the model.

More generally, we would expect that a sufficiently large and rich set of basis functions would allow any desired function to be approximated to arbitrary accuracy. It would seem therefore that such linear models constitute a general purpose framework for solving problems in machine learning. Unfortunately, there are some significant shortcomings with linear models, which arise from the assumption that the basis functions \(\phi_{j}(\mathbf{x})\) are fixed and independent of the training data. To understand these limitations, we start by looking at the behaviour of linear models as the number of input variables is increased.

\subsection*{6.1.1 The curse of dimensionality}

Consider a simple regression model for a single input variable given by a polynomial of order \(M\) in the form

\[
y(x, \mathbf{w})=w_{0}+w_{1} x+w_{2} x^{2}+\ldots+w_{M} x^{M}
\]

and let us see what happens if we increase the number of inputs. If we have \(D\) input variables \(\left\{x_{1}, \ldots, x_{D}\right\}\), then a general polynomial with coefficients up to order 3
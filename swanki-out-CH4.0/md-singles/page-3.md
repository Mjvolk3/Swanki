Figure 4.1 The linear regression model (4.3) can be expressed as a simple neural network diagram involving a single layer of parameters. Here each basis function \(\phi_{j}(\mathbf{x})\) is represented by an input node, with the solid node representing the 'bias' basis function \(\phi_{0}\), and the function \(y(\mathbf{x}, \mathbf{w})\) is represented by an output node. Each of the parameters \(w_{j}\) is shown by a line connecting the corresponding basis

![](https://cdn.mathpix.com/cropped/2024_05_26_28116a89444d4b7f5a3bg-1.jpg?height=332&width=528&top_left_y=215&top_left_x=1111)
function to the output.

Before the advent of deep learning it was common practice in machine learning to use some form of fixed pre-processing of the input variables \(\mathbf{x}\), also known as feature extraction, expressed in terms of a set of basis functions \(\left\{\phi_{j}(\mathbf{x})\right\}\). The goal was to choose a sufficiently powerful set of basis functions that the resulting learning task could be solved using a simple network model. Unfortunately, it is very difficult to hand-craft suitable basis functions for anything but the simplest applications. Deep learning avoids this problem by learning the required nonlinear transformations of the data from the data set itself.

We have already encountered an example of a regression problem when we disChapter 1 cussed curve fitting using polynomials. The polynomial function (1.1) can be expressed in the form (4.3) if we consider a single input variable \(x\) and if we choose basis functions defined by \(\phi_{j}(x)=x^{j}\). There are many other possible choices for the basis functions, for example

\[
\phi_{j}(x)=\exp \left\{-\frac{\left(x-\mu_{j}\right)^{2}}{2 s^{2}}\right\}
\]

where the \(\mu_{j}\) govern the locations of the basis functions in input space, and the parameter \(s\) governs their spatial scale. These are usually referred to as 'Gaussian' basis functions, although it should be noted that they are not required to have a probabilistic interpretation. In particular the normalization coefficient is unimportant because these basis functions will be multiplied by learnable parameters \(w_{j}\).

Another possibility is the sigmoidal basis function of the form

\[
\phi_{j}(x)=\sigma\left(\frac{x-\mu_{j}}{s}\right)
\]

where \(\sigma(a)\) is the logistic sigmoid function defined by

\[
\sigma(a)=\frac{1}{1+\exp (-a)}
\]

Equivalently, we can use the tanh function because this is related to the logistic sigmoid by \(\tanh (a)=2 \sigma(2 a)-1\), and so a general linear combination of logistic sigmoid functions is equivalent to a general linear combination of tanh functions in the sense that they can represent the same class of input-output functions. These various choices of basis function are illustrated in Figure 4.2.
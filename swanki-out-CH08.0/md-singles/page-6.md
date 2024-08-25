\title{
8. BACKPROPAGATION
}

In the above derivation we have implicitly assumed that each hidden or output unit in the network has the same activation function \(h(\cdot)\). However, the derivation is easily generalized to allow different units to have individual activation functions, simply by keeping track of which form of \(h(\cdot)\) goes with which unit.

\subsection*{8.1.3 A simple example}

The above derivation of the backpropagation procedure allowed for general forms for the error function, the activation functions, and the network topology. To illustrate the application of this algorithm, we consider a two-layer network of the form illustrated in Figure 6.9, together with a sum-of-squares error. The output units have linear activation functions, so that \(y_{k}=a_{k}\), and the hidden units have sigmoidal activation functions given by

\[
h(a) \equiv \tanh (a)
\]

where \(\tanh (a)\) is defined by (6.14). A useful feature of this function is that its derivative can be expressed in a particularly simple form:

\[
h^{\prime}(a)=1-h(a)^{2}
\]

We also consider a sum-of-squares error function, so that for data point \(n\) the error is given by

\[
E_{n}=\frac{1}{2} \sum_{k=1}^{K}\left(y_{k}-t_{k}\right)^{2}
\]

where \(y_{k}\) is the activation of output unit \(k\), and \(t_{k}\) is the corresponding target value for a particular input vector \(\mathbf{x}_{n}\).

For each data point in the training set in turn, we first perform a forward propagation using

\[
\begin{aligned}
a_{j} & =\sum_{i=0}^{D} w_{j i}^{(1)} x_{i} \\
z_{j} & =\tanh \left(a_{j}\right) \\
y_{k} & =\sum_{j=0}^{M} w_{k j}^{(2)} z_{j}
\end{aligned}
\]

where \(D\) is the dimensionality of the input vector \(\mathbf{x}\) and \(M\) is the total number of hidden units. Also we have used \(x_{0}=z_{0}=1\) to allow bias parameters to be included in the weights. Next we compute the \(\delta\) 's for each output unit using

\[
\delta_{k}=y_{k}-t_{k}
\]

Then, we backpropagate these errors to obtain \(\delta\) 's for the hidden units using

\[
\delta_{j}=\left(1-z_{j}^{2}\right) \sum_{k=1}^{K} w_{k j}^{(2)} \delta_{k}
\]
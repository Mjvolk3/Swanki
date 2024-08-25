![](https://cdn.mathpix.com/cropped/2024_05_26_f259a6e31b33764956acg-1.jpg?height=1248&width=1238&top_left_y=216&top_left_x=409

ChatGPT figure/image summary: The image appears to be a cover or a title page for a chapter or section of a book or document, which is titled "Backpropagation." The number "8" indicates that this could be chapter or section 8 in the material. The background is a colorful, abstract image with a pattern of interwoven light streaks that give a sense of connectivity or network, possibly representing the interconnected nature of neurons in a neural network, which would be in line with the context of backpropagation in machine learning.)

Our goal in this chapter is to find an efficient technique for evaluating the gradient of an error function $E(\mathbf{w})$ for a feed-forward neural network. We will see that this can be achieved using a local message-passing scheme in which information is sent backwards through the network and is known as error backpropagation, or sometimes simply as backprop.

Historically, the backpropagation equations would have been derived by hand and then implemented in software alongside the forward propagation equations, with both steps taking time and being prone to mistakes. Modern neural network software environments, however, allow virtually any derivatives of interest to be calculated efficiently with only minimal effort beyond that of coding up the original network function. This idea, called automatic differentiation, plays a key role in modern deep learning. However, it is valuable to understand how the calculations are performed so that we are not relying on 'black box' software solutions. In this chapter we

Section 3.4

Section 3.4

\section*{Exercise 8.5}

where $\delta_{k l}$ are the elements of the identity matrix and are defined by

$$
\delta_{k l}= \begin{cases}1, & \text { if } k=l \\ 0, & \text { otherwise }\end{cases}
$$

If we have individual logistic sigmoid activation functions at each output unit, then

$$
\frac{\partial y_{k}}{\partial a_{l}}=\delta_{k l} \sigma^{\prime}\left(a_{l}\right)
$$

whereas for softmax outputs, we have

$$
\frac{\partial y_{k}}{\partial a_{l}}=\delta_{k l} y_{k}-y_{k} y_{l}
$$

We can summarize the procedure for calculating the Jacobian matrix as follows. Apply the input vector corresponding to the point in input space at which the Jacobian matrix is to be evaluated, and forward propagate in the usual way to obtain the states of all the hidden and output units in the network. Next, for each row $k$ of the Jacobian matrix, corresponding to the output unit $k$, backpropagate using the recursive relation (8.30), starting with (8.31), (8.33) or (8.34), for all the hidden units in the network. Finally, use (8.29) for the backpropagation to the inputs. The Jacobian can also be evaluated using an alternative forward propagation formalism, which can be derived in an analogous way to the backpropagation approach given here.

Again, the implementation of such algorithms can be checked using numerical differentiation in the form

$$
\frac{\partial y_{k}}{\partial x_{i}}=\frac{y_{k}\left(x_{i}+\epsilon\right)-y_{k}\left(x_{i}-\epsilon\right)}{2 \epsilon}+\mathcal{O}\left(\epsilon^{2}\right)
$$

which involves $2 D$ forward propagation passes for a network having $D$ inputs and therefore requires $\mathcal{O}(D W)$ steps in total.

\title{
8.1.6 The Hessian matrix
}

We have shown how backpropagation can be used to obtain the first derivatives of an error function with respect to the weights in the network. Backpropagation can also be used to evaluate the second derivatives of the error, which are given by

$$
\frac{\partial^{2} E}{\partial w_{j i} \partial w_{l k}}
$$

It is often convenient to consider all the weight and bias parameters as elements $w_{i}$ of a single vector, denoted $\mathbf{w}$, in which case the second derivatives form the elements $H_{i j}$ of the Hessian matrix $\mathbf{H}$ :

$$
H_{i j}=\frac{\partial^{2} E}{\partial w_{i} \partial w_{j}}
$$

\section*{Exercise 8.6}

\section*{Exercise 8.8}

where $i, j \in\{1, \ldots, W\}$ and $W$ is the total number of weights and biases. The Hessian matrix arises in several nonlinear optimization algorithms used for training neural networks based on considerations of the second-order properties of the error surface (Bishop, 2006). It also plays a role in some Bayesian treatments of neural networks (MacKay, 1992; Bishop, 2006) and has been used to reduce the precision of the weights in large language models to lessen their memory footprint (Shen et al., 2019).

An important consideration for many applications of the Hessian is the efficiency with which it can be evaluated. If there are $W$ parameters (weights and biases) in the network, then the Hessian matrix has dimensions $W \times W$ and so the computational effort needed to evaluate the Hessian will scale like $\mathcal{O}\left(W^{2}\right)$ for each point in the data set. Extension of the backpropagation procedure (Bishop, 1992) allows the Hessian matrix to be evaluated efficiently with a scaling that is indeed $\mathcal{O}\left(W^{2}\right)$. Sometimes, we do not need the Hessian matrix explicitly but only the product ${ }^{\mathrm{T}} \mathbf{H}$ of the Hessian with some vector $\mathbf{v}$, and this product can be calculated efficiently in $\mathcal{O}(W)$ steps using an extension of backpropagation (Møller, 1993; Pearlmutter, 1994).

Since neural networks may contain millions or even billions of parameters, evaluating, or even just storing, the full Hessian matrix for many models is infeasible. Evaluating the inverse of the Hessian is even more demanding as this has $\mathcal{O}\left(W^{3}\right)$ computational scaling. Consequently there is interest in finding effective approximations to the full Hessian.

One approximation involves simply evaluating only the diagonal elements of the Hessian and implicitly setting the off-diagonal elements to zero. This requires $\mathcal{O}(W)$ storage and allows the inverse to be evaluated in $\mathcal{O}(W)$ steps but still requires $\mathcal{O}\left(W^{2}\right)$ computation (Ricotti, Ragazzini, and Martinelli, 1988), although with further approximation this can be reduced to $\mathcal{O}(W)$ steps (Becker and LeCun, 1989; LeCun, Denker, and Solla, 1990). In practice, however, the Hessian generally has significant off-diagonal terms, and so this approximation must be treated with care.

A more convincing approach, known as the outer product approximation, is obtained as follows. Consider a regression application using a sum-of-squares error function of the form

$$
E=\frac{1}{2} \sum_{n=1}^{N}\left(y_{n}-t_{n}\right)^{2}
$$

where we have considered a single output to keep the notation simple (the extension to several outputs is straightforward). We can then write the Hessian matrix in the form

$$
\mathbf{H}=\nabla \nabla E=\sum_{n=1}^{N} \nabla y_{n}\left(\nabla y_{n}\right)^{\mathrm{T}}+\sum_{n=1}^{N}\left(y_{n}-t_{n}\right) \nabla \nabla y_{n}
$$

where $\nabla$ denotes the gradient with respect to w. If the network has been trained on the data set and its outputs $y_{n}$ are very close to the target values $t_{n}$, then the final term in (8.39) will be small and can be neglected. More generally, however, it may be appropriate to neglect this term based on the following argument. Recall from Section 4.2 that the optimal function that minimizes a sum-of-squares loss is

\section*{Exercise 8.9}

Exercise 8.10

Exercise 8.11

Exercise 8.12 the conditional average of the target data. The quantity $\left(y_{n}-t_{n}\right)$ is then a random variable with zero mean. If we assume that its value is uncorrelated with the value of the second derivative term on the right-hand side of (8.39), then the whole term will average to zero in the summation over $n$.

By neglecting the second term in (8.39), we arrive at the Levenberg-Marquardt approximation, also known as the outer product approximation because the Hessian matrix is built up from a sum of outer products of vectors, given by

$$
\mathbf{H} \simeq \sum_{n=1}^{N} \nabla a_{n} \nabla a_{n}^{\mathrm{T}}
$$

Evaluating the outer product approximation for the Hessian is straightforward as it involves only first derivatives of the error function, which can be evaluated efficiently in $\mathcal{O}(W)$ steps using standard backpropagation. The elements of the matrix can then be found in $\mathcal{O}\left(W^{2}\right)$ steps by simple multiplication. It is important to emphasize that this approximation is likely to be valid only for a network that has been trained appropriately, and that for a general network mapping, the second derivative terms on the right-hand side of (8.39) will typically not be negligible.

For a cross-entropy error function for a network with logistic-sigmoid outputunit activation functions, the corresponding approximation is given by

$$
\mathbf{H} \simeq \sum_{n=1}^{N} y_{n}\left(1-y_{n}\right) \nabla a_{n} \nabla a_{n}^{\mathrm{T}}
$$

An analogous result can be obtained for multi-class networks having softmax outputunit activation functions. The outer product approximation can also be used to develop an efficient sequential procedure for approximating the inverse of a Hessian (Hassibi and Stork, 1993).

\subsection*{8.2. Automatic Differentiation}

We have seen the importance of using gradient information to train neural networks efficiently. There are essentially four ways in which the gradient of a neural network error function can be evaluated.

The first approach, which formed the mainstay of neural networks for many years, is to derive the backpropagation equations by hand and then to implement them explicitly in software. If this is done carefully it results in efficient code that gives precise results that are accurate to numerical precision. However, the process of deriving the equations as well as the process of coding them both take time and are prone to errors. It also results in some redundancy in the code because the forward propagation equations are coded separately from the backpropagation equations. As these often involve duplicated calculations, then if the model is altered, both the forward and backward implementations need to be changed in unison. This effort

Section 8.1.4

can easily become a limitation on how quickly and effectively different architectures can be explored empirically.

A second approach is to evaluate the gradients numerically using finite differences. This requires only a software implementation of the forward propagation equations. One problem with numerical differentiation is that it has limited computational accuracy, although this is unlikely to be an issue for network training as we may be using stochastic gradient descent in which each evaluation is only a very noisy estimate of the local gradient. The main drawback of this approach is that it scales poorly with the size of the network. However, the technique is useful for debugging other approaches, because the gradients are evaluated using only the forward propagation code and so can be used to confirm the correctness of backpropagation or other code used to evaluate gradients.

A third approach is called symbolic differentiation and makes use of specialist software to automate the analytical manipulations that are done by hand in the first approach. This process is an example of computer algebra or symbolic computation and involves the automatic application of the rules of calculus, such as the chain rule, in a completely mechanistic process. The resulting expressions are then implemented in standard software. An obvious advantage of this approach is that it avoids human error in the manual derivation of the backpropagation equations. Moreover, the gradients are again calculated to machine precision, and the poor scaling seen with numerical differentiation is avoided. The major downside of symbolic differentiation, however, is that the resulting expressions for derivatives can become exponentially longer than the original function, with correspondingly long evaluation times. Consider a function $f(x)$ given by the product of $u(x)$ and $v(x)$. The function and its derivative are given by

$$
\begin{aligned}
f(x) & =u(x) v(x) \\
f^{\prime}(x) & =u^{\prime}(x) v(x)+u(x) v^{\prime}(x)
\end{aligned}
$$

We see that there is redundant computation in that $u(x)$ and $v(x)$ must be evaluated both for the calculation of $f(x)$ and for $f^{\prime}(x)$. If the factors $u(x)$ and $v(x)$ themselves involve factors, then we end up with a nested duplication of expressions, which rapidly grow in complexity. This problem is called expression swell.

As a further illustration, consider a function that is structured like two layers of a neural network (Grosse, 2018) with a single input $x$, a hidden unit with activation $z$, and an output $y$ in which

$$
\begin{aligned}
& z=h\left(w_{1} x+b_{1}\right) \\
& y=h\left(w_{2} z+b_{2}\right)
\end{aligned}
$$

where $h(a)$ is the soft ReLU:

$$
\zeta(a)=\ln (1+\exp (a))
$$

The overall function is therefore given by

$$
y(x)=h\left(w_{2} h\left(w_{1} x+b_{1}\right)+b_{2}\right)
$$

and the derivative of the network output with respect to $w_{1}$, evaluated symbolically,

Exercise 8.13 is given by

$$
\frac{\partial y}{\partial w_{1}}=\frac{w_{2} x \exp \left(w_{1} x+b_{1}+b_{2}+w_{2} \ln \left[1+e^{w_{1} x+b_{1}}\right]\right)}{\left(1+e^{w_{1} x+b_{1}}\right)\left(1+\exp \left(b_{2}+w_{2} \ln \left[1+e^{w_{1} x+b_{1}}\right]\right)\right)}
$$

As well as being significantly more complex than the original function, we also see redundant computation where expressions such as $w_{1} x+b_{1}$ occur in several places.

A further major drawback with symbolic differentiation is that it requires that the expression to be differentiated is expressed in closed form. It therefore excludes important control flow operations such as loops, recursions, conditional execution, and procedure calls, which are valuable constructs that we might wish to use when defining the network function.

We therefore turn to the fourth technique for evaluating derivatives in neural networks called automatic differentiation, also known as 'autodiff' or 'algorithmic differentiation' (Baydin et al., 2018). Unlike symbolic differentiation, the goal of automatic differentiation is not to find a mathematical expression for the derivatives but to have the computer automatically generate the code that implements the gradient calculations given only the code for the forward propagation equations. It is accurate to machine precision, just as with symbolic differentiation, but is more efficient because it is able to exploit intermediate variables used in the definition of the forward propagation equations and thereby avoid redundant evaluations. It is important to note that not only can automatic differentiation handle conventional closed-form mathematical expressions but it can also deal with flow control elements such as branches, loops, recursion, and procedure calls, and is therefore significantly more powerful than symbolic differentiation. Automatic differentiation is a wellestablished field with broad applicability that was developed largely outside of the machine learning community. Modern deep learning is a largely empirical process, involving evaluating and comparing different architectures, and automatic differentiation therefore plays a key role in enabling this experimentation to be done accurately and efficiently.

The key idea of automatic differentiation is to take the code that evaluates a function, for example the forward propagation equations that evaluate the error function for a neural network, and augment the code with additional variables whose values are accumulated during code execution to obtain the required derivatives. There are two principal forms of automatic differentiation, known as forward mode and reverse mode. We start by looking at forward mode, which is conceptually somewhat simpler.

\title{
8.2.1 Forward-mode automatic differentiation
}

In forward-mode automatic differentiation, we augment each intermediate variable $z_{i}$, known as a 'primal' variable, involved in the evaluation of a function, such as the error function of a neural network, with an additional variable representing the value of some derivative of that variable, which we can denote $\dot{z}_{i}$, known as a 'tangent' variable. The tangent variables and their associated code are generated

Figure 8.4 Evaluation trace diagram showing the steps involved in the numerical evaluation of the function (8.49) using the primal equations $(8.50)$ to ( 8.56$)$.

![](https://cdn.mathpix.com/cropped/2024_05_26_ff30764196e5f01f8d35g-1.jpg?height=303&width=769&top_left_y=227&top_left_x=876

ChatGPT figure/image summary: The image provided contains a diagram (referred to as Figure 8.4 in the text) which is an evaluation trace diagram used in the numerical evaluation of a function. It is a visual representation of the computational steps or "primal equations" used to evaluate a function within the context of automatic differentiation, specifically forward-mode automatic differentiation.

The diagram shows a graph where nodes represent intermediate variables in the computation of a function (denoted as f), and arrows represent dependencies between these computations.

Here is a brief description of the elements:

- Nodes \( v_1 \) and \( v_2 \) at the top represent input variables, denoted as \( x_1 \) and \( x_2 \) respectively.
- Node \( v_3 \) represents the multiplication of \( v_1 \) and \( v_2 \), as indicated by the label \( v_1 v_2 \) and arrows coming from \( v_1 \) and \( v_2 \).
- Node \( v_4 \) represents the sine of \( v_2 \), labeled \( \sin(v_2) \), with the arrow coming from \( v_2 \) indicating the input to the sine function.
- Node \( v_5 \) represents the exponential of \( v_3 \), labeled as \( \exp(v_3) \), with an arrow coming from \( v_3 \).
- Node \( v_6 \) represents the subtraction of node \( v_4 \) from node \( v_3 \), labeled as \( v_3 - v_4 \), with arrows coming from both \( v_3 \) and \( v_4 \).
- Finally, node \( v_7 \) represents the addition of \( v_5 \) and \( v_6 \), leading to the final function output, f.

The arrows in the diagram depict the flow of computation required to evaluate the final function from the input variables. The diagram is part of an explanation of how intermediate calculations can be used concurrently to compute derivatives using forward-mode automatic differentiation, as described in the text. The primal equations (8.50) to (8.56) correspond to the propagation of the primal variables through this graph, and the tangent equations (8.58) to (8.64) pertain to the derivative calculations which are generated automatically and evaluated in conjunction with the primal computations.)

automatically by the software environment. Instead of simply doing forward propagation to compute $\left\{z_{i}\right\}$, the code now propagates tuples $\left(z_{i}, \dot{z}_{i}\right)$ so that variables and derivatives are evaluated in parallel. The original function is generally defined in terms of elementary operators consisting of arithmetic operations and negation as well as transcendental functions such as exponential, logarithm, and trigonometric functions, all of which have simple formulae for their derivatives. Using these derivatives in combination with the chain rule of calculus allows the code used to evaluate gradients to be constructed automatically.

As an example, consider the following function, which has two input variables:

$$
f\left(x_{1}, x_{2}\right)=x_{1} x_{2}+\exp \left(x_{1} x_{2}\right)-\sin \left(x_{2}\right)
$$

When implemented in software, the code consists of a sequence of operations that can be expressed as an evaluation trace of the underlying elementary operations. This trace can be visualized in the form of a graph, as shown in Figure 8.4. Here we have defined the following primal variables

$$
\begin{aligned}
& v_{1}=x_{1} \\
& v_{2}=x_{2} \\
& v_{3}=v_{1} v_{2} \\
& v_{4}=\sin \left(v_{2}\right) \\
& v_{5}=\exp \left(v_{3}\right) \\
& v_{6}=v_{3}-v_{4} \\
& v_{7}=v_{5}+v_{6}
\end{aligned}
$$

Now suppose we wish to evaluate the derivative $\partial f / \partial x_{1}$. We define the tangent variables by $\dot{v}_{i}=\partial v_{i} / \partial x_{1}$. Expressions for evaluating these can be constructed automatically using the chain rule of calculus:

$$
\dot{v}_{i}=\frac{\partial v_{i}}{\partial x_{1}}=\sum_{j \in \mathrm{pa}(i)} \frac{\partial v_{j}}{\partial x_{1}} \frac{\partial v_{i}}{\partial v_{j}}=\sum_{j \in \mathrm{pa}(i)} \dot{v}_{j} \frac{\partial v_{i}}{\partial v_{j}}
$$

where $\mathrm{pa}(i)$ denotes the set of parents of the node $i$ in the evaluation trace diagram, that is the set of variables with arrows pointing to node $i$. For example, in Figure 8.4 the parents of node $v_{3}$ are nodes $v_{1}$ and $v_{2}$. Applying (8.57) to the evaluation trace

\title{
8. BACKPROPAGATION
}

Figure 8.5 Extension of the example shown in Figure 8.4 to a function with two outputs $f_{1}$ and $f_{2}$.

![](https://cdn.mathpix.com/cropped/2024_05_26_4388dae6329660fd2fabg-1.jpg?height=300&width=785&top_left_y=226&top_left_x=858

ChatGPT figure/image summary: The image depicts an evaluation trace diagram that illustrates the computational graph of a function with two outputs, \( f_1 \) and \( f_2 \), as a sequence of operations based on two input variables, \( x_1 \) and \( x_2 \). The graph shows the steps involved in the evaluation of the function, with each node representing an intermediate variable (\( v_i \)) or output (\( f_i \)), and the edges representing the flow of computation. The intermediate variables are computed as follows:

- \( v_1 = x_1 \)
- \( v_2 = x_2 \)
- \( v_3 = v_1v_2 \)
- \( v_4 = \sin(v_2) \)
- \( v_5 = \exp(v_3) \)
- \( v_6 = v_3 - v_4 \)
- \( v_7 = v_5 + v_6 \) (which corresponds to output \( f_1 \))
- \( v_8 = v_5v_6 \) (which corresponds to output \( f_2 \))

The edges between the nodes indicate the flow of the input values \( x_1 \) and \( x_2 \) through the various operations represented by the intermediate variables, ultimately leading to the function outputs \( f_1 \) and \( f_2 \). This graph could be used to both evaluate the function and its derivatives using automatic differentiation algorithms, specifically by using the forward-mode or reverse-mode automatic differentiation techniques.)

equations (8.50) to (8.56), we obtain the following evaluation trace equations for the tangent variables

$$
\begin{aligned}
& \dot{v}_{1}=1 \\
& \dot{v}_{2}=0 \\
& \dot{v}_{3}=v_{1} \dot{v}_{2}+\dot{v}_{1} v_{2} \\
& \dot{v}_{4}=\dot{v}_{2} \cos \left(v_{2}\right) \\
& \dot{v}_{5}=\dot{v}_{3} \exp \left(v_{3}\right) \\
& \dot{v}_{6}=\dot{v}_{3}-\dot{v}_{4} \\
& \dot{v}_{7}=\dot{v}_{5}+\dot{v}_{6}
\end{aligned}
$$

We can summarize automatic differentiation for this example as follows. We first write code to implement the evaluation of the primal variables, given by (8.50) to (8.56). The associated equations and corresponding code for evaluating the tangent variables (8.58) to (8.64) are generated automatically. To evaluate the derivative $\partial f / \partial x_{1}$, we input specific values of $x_{1}$ and $x_{2}$ and the code then executes the primal

\section*{Exercise 8.17} and tangent equations, numerically evaluating the tuples $\left(v_{i}, \dot{v}_{i}\right)$ in sequence until we obtain $\dot{v}_{5}$, which is the required derivative.

Now consider an example with two outputs $f_{1}\left(x_{1}, x_{2}\right)$ and $f_{2}\left(x_{1}, x_{2}\right)$ where $f_{1}\left(x_{1}, x_{2}\right)$ is defined by (8.49) and

$$
f_{2}\left(x_{1}, x_{2}\right)=\left(x_{1} x_{2}-\sin \left(x_{2}\right)\right) \exp \left(x_{1} x_{2}\right)
$$

as illustrated by the evaluation trace diagram in Figure 8.5. We see that this involves only a small extension to the evaluation equations for the primal and tangent variables, and so both $\partial f_{1} / \partial x_{1}$ and $\partial f_{2} / \partial x_{1}$ can be evaluated together in a single forward pass. The downside, however, is that if we wish to evaluate derivatives with respect to a different input variable $x_{2}$ then we have to run a separate forward pass. In general, if we have a function with $D$ inputs and $K$ outputs then a single pass of forward-mode automatic differentiation produces a single column of the $K \times D$ Jacobian matrix:

$$
\mathbf{J}=\left[\begin{array}{ccc}
\frac{\partial f_{1}}{\partial x_{1}} & \cdots & \frac{\partial f_{1}}{\partial x_{D}} \\
\vdots & \ddots & \vdots \\
\frac{\partial f_{K}}{\partial x_{1}} & \cdots & \frac{\partial f_{K}}{\partial x_{D}}
\end{array}\right]
$$

To compute column $j$ of the Jacobian, we need to initialize the forward pass of the tangent equations by setting $\dot{x}_{j}=1$ and $\dot{x}_{i}=0$ for $i \neq j$. We can write this in vector form as $\dot{\mathbf{x}}=\mathbf{e}_{i}$ where $\mathbf{e}_{i}$ is the $i$ th unit vector. To compute the full Jacobian matrix we need $D$ forward-mode passes. However, if we wish to evaluate the product of the Jacobian with a vector $\mathbf{r}=\left(r_{1}, \ldots, r_{D}\right)^{\mathrm{T}}$ :

$$
\mathbf{J}=\left[\begin{array}{ccc}
\frac{\partial f_{1}}{\partial x_{1}} & \cdots & \frac{\partial f_{1}}{\partial x_{D}} \\
\vdots & \ddots & \vdots \\
\frac{\partial f_{K}}{\partial x_{1}} & \cdots & \frac{\partial f_{K}}{\partial x_{D}}
\end{array}\right]\left[\begin{array}{c}
r_{1} \\
\vdots \\
r_{D}
\end{array}\right]
$$

Exercise 8.18 then this can be done in single forward pass by setting $\dot{\mathbf{x}}=\mathbf{r}$.

We see that forward-mode automatic differentiation can evaluate the full $K \times D$ Jacobian matrix of derivatives using $D$ forward passes. This is very efficient for networks with a few inputs and many outputs, such that $K \gg D$. However, we often operate in a regime where we often have just one function, namely the error function used for training, and large numbers of variables that we want to differentiate with respect to, comprising the weights and biases in the network, of which there may be millions or billions. In such situations, forward-mode automatic differentiation is extremely inefficient. We therefore turn to an alternative version of automatic differentiation based on the a backwards flow of derivative data through the evaluation trace graph.

\title{
8.2.2 Reverse-mode automatic differentiation
}

We can think of reverse-mode automatic differentiation as a generalization of the error backpropagation procedure. As with forward mode, we augment each intermediate variable $v_{i}$ with additional variables, in this case called adjoint variables, denoted $\bar{v}_{i}$. Consider again a situation with a single output function $f$ for which the adjoint variables are defined by

$$
\bar{v}_{i}=\frac{\partial f}{\partial v_{i}}
$$

These can be evaluated sequentially starting with the output and working backwards by using the chain rule of calculus:

$$
\bar{v}_{i}=\frac{\partial f}{\partial v_{i}}=\sum_{j \in \operatorname{ch}(i)} \frac{\partial f}{\partial v_{j}} \frac{\partial v_{j}}{\partial v_{i}}=\sum_{j \in \operatorname{ch}(i)} \bar{v}_{j} \frac{\partial v_{j}}{\partial v_{i}}
$$

Here $\operatorname{ch}(i)$ denotes the children of node $i$ in the evaluation trace graph, in other words the set of nodes that have arrows pointing into them from node $i$. The successive evaluation of the adjoint variables represents a flow of information backwards

Figure 8.1

Exercise 8.16 through the graph, as we saw previously.

If we again consider the specific example function given by (8.50) to (8.56), we obtain the following evaluation equations for the evaluation of the adjoint variables

$$
\begin{aligned}
& \bar{v}_{7}=1 \\
& \bar{v}_{6}=\bar{v}_{7} \\
& \bar{v}_{5}=\bar{v}_{7} \\
& \bar{v}_{4}=-\bar{v}_{6} \\
& \bar{v}_{3}=\bar{v}_{5} v_{5}+\bar{v}_{6} \\
& \bar{v}_{2}=\bar{v}_{2} v_{1}+\bar{v}_{4} \cos \left(v_{2}\right) \\
& \bar{v}_{1}=\bar{v}_{3} v_{2}
\end{aligned}
$$

Note that these start at the output and then flow backwards through the graph to the inputs. Even with multiple inputs, only a single backward pass is required to evaluate the derivatives. For a neural network error function, the derivatives of $E$ with respect to the weight and biases are obtained as the corresponding adjoint variables. How-

Figure 8.5 ever, if we now have more than one output then we need to run a separate backward pass for each output variable.

Reverse mode is often more memory intensive than forward mode because all of the intermediate primal variables must be stored so that they will be available as needed when evaluating the adjoint variables during the backward pass. By contrast, with forward mode, the primal and tangent variables are computed together during the forward pass, and therefore variables can be discarded once they have been used. It is therefore also generally easier to implement forward mode compared to reverse mode.

For both forward-mode and reverse-mode automatic differentiation, a single pass through the network is guaranteed to take no more than 6 times the computational cost of a single function evaluation. In practice, the overhead is typically closer to a factor of 2 or 3 (Griewank and Walther, 2008). Hybrids of forward and reverse modes are also of interest. One situation in which this arises is in the evaluation of the product of a Hessian matrix with a vector, which can be calculated without explicit evaluation of the full Hessian (Pearlmutter, 1994). Here we can use reverse mode to calculate the gradient of code, which itself has been generated by the forward model. We start from a vector $\mathbf{b}$ and a point $\mathbf{x}$ at which the Hessian-vector product is to be evaluated. By setting $\dot{\mathbf{x}}=\mathbf{v}$ and using forward mode, we obtain the directional derivative $\mathbf{v}^{\mathrm{T}} \nabla f$. This is then differentiated using reverse mode to obtain $\nabla^{2} f \mathbf{v}=\mathbf{H v}$. If $W$ is the number of parameters in the neural network then this evaluation has $\mathcal{O}(W)$ complexity even though the Hessian is of size $W \times W$. The Hessian itself can also be evaluated explicitly using automatic differentiation but this has $\mathcal{O}\left(W^{2}\right)$ complexity.

\title{
Exercises
}

8.1 (*) By making use of (8.5), (8.6), (8.8), and (8.12), verify the backpropagation formula (8.13) for evaluating the derivatives of an error function.

8.2 ( $\star \star)$ Consider a network that consists of layers and rewrite the backpropagation formula (8.13) in matrix notation by starting with the forward propagation equation (6.19). Note that the result involves multiplication by the transposes of the matrices.

therefore explain the key concepts of backpropagation, and explore the framework of automatic differentiation in detail.

Note that the term 'backpropagation' is used in the neural computing literature in a variety of different ways. For instance, a feed-forward architecture may be called a backpropagation network. Also the term 'backpropagation' is sometimes used to describe the end-to-end training procedure for a neural network including the gradient descent parameter updates. In this book we will use 'backpropagation' specifically to describe the computational procedure used in the numerical evaluation of derivatives such as the gradient of the error function with respect to the weights and biases of a network. This procedure can also be applied to the evaluation of other important derivatives such as the Jacobian and Hessian matrices.

\title{
8.1. Evaluation of Gradients
}

We now derive the backpropagation algorithm for a general network having arbitrary feed-forward topology, arbitrary differentiable nonlinear activation functions, and a broad class of error function. The resulting formulae will then be illustrated using a simple layered network structure having a single layer of sigmoidal hidden units together with a sum-of-squares error.

Many error functions of practical interest, for instance those defined by maximum likelihood for a set of i.i.d. data, comprise a sum of terms, one for each data point in the training set, so that

$$
E(\mathbf{w})=\sum_{n=1}^{N} E_{n}(\mathbf{w})
$$

Here we will consider the problem of evaluating $\nabla E_{n}(\mathbf{w})$ for one such term in the error function. This may be used directly for stochastic gradient descent, or the results could be accumulated over a set of training data points for batch or minibatch methods.

\subsection*{8.1.1 Single-layer networks}

Consider first a simple linear model in which the outputs $y_{k}$ are linear combinations of the input variables $x_{i}$ so that

$$
y_{k}=\sum_{i} w_{k i} x_{i}
$$

together with a sum-of-squares error function that, for a particular input data point $n$, takes the form

$$
E_{n}=\frac{1}{2} \sum_{k}\left(y_{n k}-t_{n k}\right)^{2}
$$

where $y_{n k}=y_{k}\left(\mathbf{x}_{n}, \mathbf{w}\right)$, and $t_{n k}$ is the associated target value. The gradient of this error function with respect to a weight $w_{j i}$ is given by

$$
\frac{\partial E_{n}}{\partial w_{j i}}=\left(y_{n j}-t_{n j}\right) x_{n i}
$$

This can be interpreted as a 'local' computation involving the product of an 'error signal' $y_{n j}-t_{n j}$ associated with the output end of the link $w_{j i}$ and the variable $x_{n i}$ associated with the input end of the link. In Section 5.4.3, we saw how a similar formula arises with the logistic-sigmoid activation function together with the crossentropy error function and similarly for the softmax activation function together with its matching multivariate cross-entropy error function. We will now see how this simple result extends to the more complex setting of multilayer feed-forward networks.

\title{
8.1.2 General feed-forward networks
}

In general, a feed-forward network consists of a set of units each of which computes a weighted sum of its inputs:

$$
a_{j}=\sum_{i} w_{j i} z_{i}
$$

where $z_{i}$ is either the activation of another unit or an input unit that sends a connection to unit $j$, and $w_{j i}$ is the weight associated with that connection. Biases can be included in this sum by introducing an extra unit, or input, with activation fixed at +1 , and so we do not need to deal with biases explicitly. The sum in (8.5), known as a pre-activation, is transformed by a nonlinear activation function $h(\cdot)$ to give the activation $z_{j}$ of unit $j$ in the form

$$
z_{j}=h\left(a_{j}\right)
$$

Note that one or more of the variables $z_{i}$ in the sum in (8.5) could be an input, and similarly, the unit $j$ in (8.6) could be an output.

For each data point in the training set, we will suppose that we have supplied the corresponding input vector to the network and calculated the activations of all the hidden and output units in the network by successive application of (8.5) and (8.6). This process is called forward propagation because it can be regarded as a forward flow of information through the network.

Now consider the evaluation of the derivative of $E_{n}$ with respect to a weight $w_{j i}$. The outputs of the various units will depend on the particular input data point $n$. However, to keep the notation uncluttered, we will omit the subscript $n$ from the network variables. First note that $E_{n}$ depends on the weight $w_{j i}$ only via the summed input $a_{j}$ to unit $j$. We can therefore apply the chain rule for partial derivatives to give

$$
\frac{\partial E_{n}}{\partial w_{j i}}=\frac{\partial E_{n}}{\partial a_{j}} \frac{\partial a_{j}}{\partial w_{j i}}
$$

We now introduce a useful notation:

$$
\delta_{j} \equiv \frac{\partial E_{n}}{\partial a_{j}}
$$

\title{
8. BACKPROPAGATION
}

Figure 8.1 Illustration of the calculation of $\delta_{j}$ for hidden unit $j$ by backpropagation of the $\delta$ 's from those units $k$ to which unit $j$ sends connections. The black arrows denote the direction of information flow during forward propagation, and the red arrows indicate the backward propagation of error information.

![](https://cdn.mathpix.com/cropped/2024_05_26_5df28c9d7a64baac9eefg-1.jpg?height=308&width=491&top_left_y=215&top_left_x=1149

ChatGPT figure/image summary: The image illustrates the concept of backpropagation in the context of neural networks. It shows three nodes representing units in a network. The central unit (with activation \( z_j \)) connects to two other units (with activations \( z_i \) and \( \delta_k \), \( \delta_l \)) via weighted connections (represented by lines with arrows). The weights are labeled \( w_{ji} \) for the input weight and \( w_{kj} \) for the output weights.

The forward pass of information, represented by the black arrows, moves from the \( z_i \) node through the weight \( w_{ji} \), is processed in the \( z_j \) node, and then moves outwards through the weights \( w_{kj} \), \( w_{lj} \).

The red arrows indicate the backward propagation of the 'errors' (\( \delta \)'s) during the training phase when the network is adjusting its weights. The \( \delta_j \) at the \( z_j \) node represents the partial derivative of the error with respect to the pre-activation level of that unit. The errors from the subsequent units (\( \delta_k \), \( \delta_l \)) are backpropagated to the \( z_j \) unit to adjust \( w_{ji} \), \( w_{kj} \), and \( w_{lj} \) during the learning process.

This image serves to visualize the data flow and error propagation mechanisms within a feed-forward neural network while applying the backpropagation algorithm described in the textual excerpt provided.)

where the $\delta$ 's are often referred to as errors for reasons we will see shortly. Using (8.5), we can write

$$
\frac{\partial a_{j}}{\partial w_{j i}}=z_{i}
$$

Substituting (8.8) and (8.9) into (8.7), we then obtain

$$
\frac{\partial E_{n}}{\partial w_{j i}}=\delta_{j} z_{i}
$$

Equation (8.10) tells us that the required derivative is obtained simply by multiplying the value of $\delta$ for the unit at the output end of the weight by the value of $z$ for the unit at the input end of the weight (where $z=1$ for a bias). Note that this takes the same form as that found for the simple linear model in (8.4). Thus, to evaluate the derivatives, we need calculate only the value of $\delta_{j}$ for each hidden and output unit in the network and then apply (8.10).

As we have seen already, for the output units, we have

$$
\delta_{k}=y_{k}-t_{k}
$$

Section 5.4.6

provided we are using the canonical link as the output-unit activation function. To evaluate the $\delta$ 's for hidden units, we again make use of the chain rule for partial derivatives:

$$
\delta_{j} \equiv \frac{\partial E_{n}}{\partial a_{j}}=\sum_{k} \frac{\partial E_{n}}{\partial a_{k}} \frac{\partial a_{k}}{\partial a_{j}}
$$

where the sum runs over all units $k$ to which unit $j$ sends connections. The arrangement of units and weights is illustrated in Figure 8.1. Note that the units labelled $k$ include other hidden units and/or output units. In writing down (8.12), we are making use of the fact that variations in $a_{j}$ give rise to variations in the error function only through variations in the variables $a_{k}$.

If we now substitute the definition of $\delta_{j}$ given by (8.8) into (8.12) and make use

Exercise 8.1 of (8.5) and (8.6), we obtain the following backpropagation formula:

$$
\delta_{j}=h^{\prime}\left(a_{j}\right) \sum_{k} w_{k j} \delta_{k}
$$

which tells us that the value of $\delta$ for a particular hidden unit can be obtained by propagating the $\delta$ 's backwards from units higher up in the network, as illustrated

\title{
Algorithm 8.1: Backpropagation
}

Input: Input vector $\mathbf{x}_{n}$

Network parameters $\mathbf{w}$

Error function $E_{n}(\mathbf{w})$ for input $x_{n}$

Activation function $h(a)$

Output: Error function derivatives $\left\{\partial E_{n} / \partial w_{j i}\right\}$

// Forward propagation

for $j \in$ all hidden and output units do

$$
\begin{aligned}
& a_{j} \leftarrow \sum_{i} w_{j i} z_{i} / /\left\{z_{i}\right\} \text { includes inputs }\left\{x_{i}\right\} \\
& z_{j} \leftarrow h\left(a_{j}\right) / / \text { activation function }
\end{aligned}
$$

end for

// Error evaluation

for $k \in$ all output units do

$$
\delta_{k} \leftarrow \frac{\partial E_{n}}{\partial a_{k}} / / \text { compute errors }
$$

end for

// Backward propagation, in reverse order

for $j \in$ all hidden units do

$\delta_{j} \leftarrow h^{\prime}\left(a_{j}\right) \sum_{k} w_{k j} \delta_{k} / /$ recursive backward evaluation $\frac{\partial E_{n}}{\partial w_{j i}} \leftarrow \delta_{j} z_{i} / /$ evaluate derivatives

end for

return $\left\{\frac{\partial E_{n}}{\partial w_{j i}}\right\}$

in Figure 8.1. Note that the summation in (8.13) is taken over the first index on $w_{k j}$ (corresponding to backward propagation of information through the network), whereas in the forward propagation equation (8.5), it is taken over the second index. Because we already know the values of the $\delta$ 's for the output units, it follows that by recursively applying (8.13), we can evaluate the $\delta$ 's for all the hidden units in a feed-forward network, regardless of its topology. The backpropagation procedure is summarized in Algorithm 8.1.

For batch methods, the derivative of the total error $E$ can then be obtained by repeating the above steps for each data point in the training set and then summing over all data points in the batch or mini-batch:

$$
\frac{\partial E}{\partial w_{j i}}=\sum_{n} \frac{\partial E_{n}}{\partial w_{j i}}
$$

\title{
8. BACKPROPAGATION
}

In the above derivation we have implicitly assumed that each hidden or output unit in the network has the same activation function $h(\cdot)$. However, the derivation is easily generalized to allow different units to have individual activation functions, simply by keeping track of which form of $h(\cdot)$ goes with which unit.

\subsection*{8.1.3 A simple example}

The above derivation of the backpropagation procedure allowed for general forms for the error function, the activation functions, and the network topology. To illustrate the application of this algorithm, we consider a two-layer network of the form illustrated in Figure 6.9, together with a sum-of-squares error. The output units have linear activation functions, so that $y_{k}=a_{k}$, and the hidden units have sigmoidal activation functions given by

$$
h(a) \equiv \tanh (a)
$$

where $\tanh (a)$ is defined by (6.14). A useful feature of this function is that its derivative can be expressed in a particularly simple form:

$$
h^{\prime}(a)=1-h(a)^{2}
$$

We also consider a sum-of-squares error function, so that for data point $n$ the error is given by

$$
E_{n}=\frac{1}{2} \sum_{k=1}^{K}\left(y_{k}-t_{k}\right)^{2}
$$

where $y_{k}$ is the activation of output unit $k$, and $t_{k}$ is the corresponding target value for a particular input vector $\mathbf{x}_{n}$.

For each data point in the training set in turn, we first perform a forward propagation using

$$
\begin{aligned}
a_{j} & =\sum_{i=0}^{D} w_{j i}^{(1)} x_{i} \\
z_{j} & =\tanh \left(a_{j}\right) \\
y_{k} & =\sum_{j=0}^{M} w_{k j}^{(2)} z_{j}
\end{aligned}
$$

where $D$ is the dimensionality of the input vector $\mathbf{x}$ and $M$ is the total number of hidden units. Also we have used $x_{0}=z_{0}=1$ to allow bias parameters to be included in the weights. Next we compute the $\delta$ 's for each output unit using

$$
\delta_{k}=y_{k}-t_{k}
$$

Then, we backpropagate these errors to obtain $\delta$ 's for the hidden units using

$$
\delta_{j}=\left(1-z_{j}^{2}\right) \sum_{k=1}^{K} w_{k j}^{(2)} \delta_{k}
$$

which follows from (8.13) and (8.16). Finally, the derivatives with respect to the first-layer and second-layer weights are given by

$$
\frac{\partial E_{n}}{\partial w_{j i}^{(1)}}=\delta_{j} x_{i}, \quad \frac{\partial E_{n}}{\partial w_{k j}^{(2)}}=\delta_{k} z_{j}
$$

\title{
8.1.4 Numerical differentiation
}

One of the most important aspects of backpropagation is its computational efficiency. To understand this, let us examine how the number of compute operations required to evaluate the derivatives of the error function scales with the total number $W$ of weights and biases in the network.

A single evaluation of the error function (for a given input data point) would require $\mathcal{O}(W)$ operations, for sufficiently large $W$. This follows because, except for a network with very sparse connections, the number of weights is typically much greater than the number of units, and so the bulk of the computational effort in forward propagation arises from evaluation of the sums in (8.5), with the evaluation of the activation functions representing a small overhead. Each term in the sum in (8.5) requires one multiplication and one addition, leading to an overall computational cost that is $\mathcal{O}(W)$.

An alternative approach to backpropagation for computing the derivatives of the error function is to use finite differences. This can be done by perturbing each weight in turn and approximating the derivatives by using the expression

$$
\frac{\partial E_{n}}{\partial w_{j i}}=\frac{E_{n}\left(w_{j i}+\epsilon\right)-E_{n}\left(w_{j i}\right)}{\epsilon}+\mathcal{O}(\epsilon)
$$

where $\epsilon \ll 1$. In a software simulation, the accuracy of the approximation to the derivatives can be improved by making $\epsilon$ smaller, until numerical round-off problems arise. The accuracy of the finite differences method can be improved significantly by using symmetrical central differences of the form

$$
\frac{\partial E_{n}}{\partial w_{j i}}=\frac{E_{n}\left(w_{j i}+\epsilon\right)-E_{n}\left(w_{j i}-\epsilon\right)}{2 \epsilon}+\mathcal{O}\left(\epsilon^{2}\right)
$$

Exercise 8.3

In this case, the $\mathcal{O}(\epsilon)$ corrections cancel, as can be verified by a Taylor expansion of the right-hand side of (8.25), and so the residual corrections are $\mathcal{O}\left(\epsilon^{2}\right)$. Note, however, that the number of computational steps is roughly doubled compared with (8.24). Figure 8.2 shows a plot of the error between a numerical evaluation of a gradient using both finite differences (8.24) and central differences (8.25) versus the analytical result, as a function of the value of the step size $\epsilon$.

The main problem with numerical differentiation is that the highly desirable $\mathcal{O}(W)$ scaling has been lost. Each forward propagation requires $\mathcal{O}(W)$ steps, and there are $W$ weights in the network each of which must be perturbed individually, so that the overall computational cost is $\mathcal{O}\left(W^{2}\right)$.

However, numerical differentiation can play a useful role in practice, because a comparison of the derivatives calculated from a direct implementation of backpropagation, or from automatic differentiation, with those obtained using central differences provides a powerful check on the correctness of the software.

Figure 8.2 The red curve shows a plot of the error between the numerical evaluation of a gradient using finite differences (8.24) and the analytical result, as a function of $\epsilon$. As $\epsilon$ decreases, the plot initially shows a linear decrease in error, and this represents a power law behaviour since the axes are logarithmic. The slope of this line is 1 which shows that this error behaves like $\mathcal{O}(\epsilon)$. At some point the evaluated gradient reaches the limit of numerical round-off and further reduction in $\epsilon$ leads to a noisy line, which again follows a power law but where the error now increases with decreasing $\epsilon$. The blue curve shows the corresponding result for central differences (8.25). We see a much smaller error compared to finite differences, and the slope of the line is 2 which shows that the error is $\mathcal{O}\left(\epsilon^{2}\right)$.

![](https://cdn.mathpix.com/cropped/2024_05_26_076a5354f07695d4c0c6g-1.jpg?height=811&width=940&top_left_y=217&top_left_x=717

ChatGPT figure/image summary: The image shows a log-log plot comparing the errors in numerical gradient computation using two different methods: finite differences and central differences. The x-axis represents the step size (ε), on a logarithmic scale, decreasing from left to right. The y-axis represents the error in the numerical computation of the gradient of a function, also on a logarithmic scale.

The red curve represents the error associated with the finite differences method, which is linear on this log-log scale until it reaches a point where numerical round-off errors dominate. As the step size decreases (moving left along the x-axis), the error drops until it reaches this point, after which the error becomes noisy and begins to increase due to these numerical limitations.

The blue curve represents the error associated with the central differences method. This method results in a much smaller error overall compared to the finite differences method. The slope of this line indicates that the error behaves according to the order of ε^2, which shows a quadratic relationship between the error and the step size.

Overall, the plot demonstrates that central differences are a more accurate method than finite differences for computing numerical gradients, especially as the step size becomes very small. This is indicative of the practical considerations in numerical optimization and scientific computation when selecting an appropriate method for numerical differentiation.)

$\epsilon$

\title{
8.1.5 The Jacobian matrix
}

We have seen how the derivatives of an error function with respect to the weights can be obtained by propagating errors backwards through the network. Backpropagation can also be used to calculate other derivatives. Here we consider the evaluation of the Jacobian matrix, whose elements are given by the derivatives of the network outputs with respect to the inputs:

$$
J_{k i} \equiv \frac{\partial y_{k}}{\partial x_{i}}
$$

where each such derivative is evaluated with all other inputs held fixed. Jacobian matrices play a useful role in systems built from a number of distinct modules, as illustrated in Figure 8.3. Each module can comprise a fixed or learnable function, which can be linear or nonlinear, so long as it is differentiable.

Suppose we wish to minimize an error function $E$ with respect to the parameter $w$ in Figure 8.3. The derivative of the error function is given by

$$
\frac{\partial E}{\partial w}=\sum_{k, j} \frac{\partial E}{\partial y_{k}} \frac{\partial y_{k}}{\partial z_{j}} \frac{\partial z_{j}}{\partial w}
$$

in which the Jacobian matrix for the red module in Figure 8.3 appears as the middle term on the right-hand side.

Because the Jacobian matrix provides a measure of the local sensitivity of the outputs to changes in each of the input variables, it also allows any known errors $\Delta x_{i}$

Figure 8.3 Illustration of a modular deep learning architecture in which the Jacobian matrix can be used to backpropagate error signals from the outputs through to earlier modules in the system.

![](https://cdn.mathpix.com/cropped/2024_05_26_b806d19b62f773366399g-1.jpg?height=323&width=923&top_left_y=212&top_left_x=718

ChatGPT figure/image summary: The image appears to be a graph plotted on logarithmic axes, showing two curves that depict the variation of some error metric with respect to a parameter $\epsilon$. The graph is designed to analyze the behavior of two numerical methods (finite differences and central differences) for computing derivatives.

The red curve represents the error using a method referred to as finite differences. According to your description, as $\epsilon$ decreases, the error initially decreases linearly on a logarithmic scale, indicating a power law behavior with the error behaving like $\mathcal{O}(\epsilon)$. This means that for larger values of $\epsilon$, the error is proportional to $\epsilon$ itself. At a certain point, the curve flattens and becomes noisy due to the limits of numerical precision, with the error increasing as $\epsilon$ decreases further.

The blue curve shows the error for the central differences method. The curve reveals that the central differences method yields a significantly smaller error compared to finite differences. Also, the slope of the blue line is 2 in the logarithmic scale, which implies that the error scales with $\epsilon^2$ and is thus $\mathcal{O}\left(\epsilon^{2}\right)$.

Unfortunately, the actual image in the provided link has not been displayed, so I cannot confirm the visual details of the graph beyond your description. However, based on your description, the image is used to compare the accuracy and numerical performance of two methods for approximating derivatives, which is a critical aspect of numerical analysis and is particularly relevant in machine learning for things like backpropagation, optimization, and sensitivity analyses.)

associated with the inputs to be propagated through the trained network to estimate their contribution $\Delta y_{k}$ to the errors at the outputs, through the relation

$$
\Delta y_{k} \simeq \sum_{i} \frac{\partial y_{k}}{\partial x_{i}} \Delta x_{i}
$$

which assumes that the $\left|\Delta x_{i}\right|$ are small. In general, the network mapping represented by a trained neural network will be nonlinear, and so the elements of the Jacobian matrix will not be constants but will depend on the particular input vector used. Thus, (8.28) is valid only for small perturbations of the inputs, and the Jacobian itself must be re-evaluated for each new input vector.

The Jacobian matrix can be evaluated using a backpropagation procedure that is like the one derived earlier for evaluating the derivatives of an error function with respect to the weights. We start by writing the element $J_{k i}$ in the form

$$
\begin{aligned}
J_{k i}=\frac{\partial y_{k}}{\partial x_{i}} & =\sum_{j} \frac{\partial y_{k}}{\partial a_{j}} \frac{\partial a_{j}}{\partial x_{i}} \\
& =\sum_{j} w_{j i} \frac{\partial y_{k}}{\partial a_{j}}
\end{aligned}
$$

where we have made use of (8.5). The sum in (8.29) runs over all units $j$ to which the input unit $i$ sends connections (for example, over all units in the first hidden layer in the layered topology considered earlier). We now write down a recursive backpropagation formula for the derivatives $\partial y_{k} / \partial a_{j}$ :

$$
\begin{aligned}
\frac{\partial y_{k}}{\partial a_{j}} & =\sum_{l} \frac{\partial y_{k}}{\partial a_{l}} \frac{\partial a_{l}}{\partial a_{j}} \\
& =h^{\prime}\left(a_{j}\right) \sum_{l} w_{l j} \frac{\partial y_{k}}{\partial a_{l}}
\end{aligned}
$$

where the sum runs over all units $l$ to which unit $j$ sends connections (corresponding to the first index of $w_{l j}$ ). Again, we have made use of (8.5) and (8.6). This backpropagation starts at the output units, for which the required derivatives can be found directly from the functional form of the output-unit activation function. For linear output units, we have

$$
\frac{\partial y_{k}}{\partial a_{l}}=\delta_{k l}
$$


![](https://cdn.mathpix.com/cropped/2024_05_26_313d01a874b4d704a5d6g-1.jpg?height=1250&width=1248&top_left_y=215&top_left_x=409

ChatGPT figure/image summary: The image appears to be a cover or opening section for a chapter titled "6 Deep Neural Networks" from a book or educational material. The background features an abstract, multicolored design which could be artistically representing the complexity and interconnected nature of deep neural networks, which are a type of artificial neural network with multiple layers between the input and output layers. The number "6" is prominently displayed, likely indicating the chapter number, and it is superimposed over the title "Deep Neural Networks," signifying the focus of the chapter's content.)

Chapter 4

Chapter 5

In recent years, neural networks have emerged as, by far, the most important machine learning technology for practical applications, and we therefore devote a large fraction of this book to studying them. Previous chapters have already laid many of the foundations we will need. In particular, we have seen that linear regression models that comprise linear combinations of fixed nonlinear basis functions can be expressed as neural networks having a single layer of weight and bias parameters. Likewise, classification models based on linear combinations of basis functions can also be viewed as single-layer neural networks. These allowed us to introduce several important concepts before we embark on a discussion of more complex multilayered networks in this chapter.

Given a sufficient number of suitably chosen basis functions, such linear models can approximate any given nonlinear transformation from inputs to outputs to any desired accuracy and might therefore appear to be sufficient to tackle any practical

\title{
6.2. Multilayer Networks
}

Chapter 7

Section 6.3

Chapter 4
In the previous section, we saw that to apply linear models of the form (6.1) to problems involving large-scale data sets and high-dimensional spaces, we need to find a set of basis functions that is tuned to the problem being solved. The key idea behind neural networks is to choose basis functions $\phi_{j}(\mathbf{x})$ that themselves have learnable parameters and then allow these parameters to be adjusted, along with the coefficients $\left\{w_{j}\right\}$, during training. We then optimize the whole model by minimizing an error function using gradient-based optimization methods, such as stochastic gradient descent, where the error function is defined jointly across all the parameters in the model.

There are, of course, many ways to construct parametric nonlinear basis functions. One key requirement is that they must be differentiable functions of their learnable parameters so that we can apply gradient-based optimization. The most successful choice has been to use basis functions that follow the same form as (6.1), so that each basis function is itself a nonlinear function of a linear combination of the inputs, where the coefficients in the linear combination are learnable parameters. Note that this construction can clearly be extended recursively to give a hierarchical model with many layers, which forms the basis for deep neural networks.

Consider a basic neural network model having two layers of learnable parameters. First, we construct $M$ linear combinations of the input variables $x_{1}, \ldots, x_{D}$ in the form

$$
a_{j}^{(1)}=\sum_{i=1}^{D} w_{j i}^{(1)} x_{i}+w_{j 0}^{(1)}
$$

where $j=1, \ldots, M$, and the superscript (1) indicates that the corresponding parameters are in the first 'layer' of the network. We will refer to the parameters $w_{j i}^{(1)}$ as weights and the parameters $w_{j 0}^{(1)}$ as biases, while the quantities $a_{j}^{(1)}$ are called pre-activations. Each of the quantities $a_{j}$ is then transformed using a differentiable, nonlinear activation function $h(\cdot)$ to give

$$
z_{j}^{(1)}=h\left(a_{j}^{(1)}\right)
$$

which represent the outputs of the basis functions in (6.1). In the context of neural networks, these basis functions are called hidden units. We will explore various choices for the nonlinear function $h(\cdot)$ shortly, but here we note that provided the derivative $h^{\prime}(\cdot)$ can be evaluated, then the overall network function will be differentiable. Following (6.1), these values are again linearly combined to give

$$
a_{k}^{(2)}=\sum_{j=1}^{M} w_{k j}^{(2)} z_{j}^{(1)}+w_{k 0}^{(2)}
$$

where $k=1, \ldots, K$, and $K$ is the total number of outputs. This transformation corresponds to the second layer of the network, and again the $w_{k 0}^{(2)}$ are bias parameters. Finally, the $\left\{a_{k}^{(2)}\right\}$ are transformed using an appropriate output-unit activation

Figure 6.9 Network diagram for a two-layer neural network. The input, hidden, and output variables are represented by nodes, and the weight parameters are represented by links between the nodes. The bias parameters are denoted by links coming from additional input and hidden variables $x_{0}$ and $z_{0}$ which are themselves denoted by solid nodes. Arrows denote the direction of information flow through the network during forward propagation.
Hidden units

![](https://cdn.mathpix.com/cropped/2024_05_26_a31248c38a71950d5cfdg-1.jpg?height=532&width=709&top_left_y=274&top_left_x=935

ChatGPT figure/image summary: The image depicts a schematic diagram of a two-layer neural network. In this diagram:

- The circles on the left represent input nodes, labeled from \( x_0 \) to \( x_D \), where \( x_0 \) can be considered the bias input since it's often set to a value of 1.
- The circles in the middle represent hidden units or nodes, labeled from \( z_1 \) to \( z_M \), with \( z_0 \) being the bias unit for the hidden layer.
- The circles on the right represent output nodes, labeled from \( y_1 \) to \( y_K \).
- The arrows between the circles represent the weighted connections (synapses) between the nodes of different layers. Each connection has an associated weight \( w \), which is indicated on the diagram by \( w^{(1)} \) for the weights between the input and hidden layers, and \( w^{(2)} \) for the weights between the hidden and output layers.
- The superscript on the weights indicates the layer number, with (1) denoting the first layer (from input to hidden), and (2) denoting the second layer (from hidden to output).
- The weights \( w^{(1)}_{10} \) and \( w^{(2)}_{10} \) likely represent the weight of the bias terms for the connections from the bias units \( x_0 \) and \( z_0 \) to the first non-bias hidden unit and output unit, respectively.

The diagram visually summarizes the structure of a feedforward neural network, where information flows from left to right, starting from inputs through hidden units and eventually to outputs. Each input is linearly combined via weights to influence the hidden layer, which after going through a nonlinear activation function influences the output layer after another linear combination. This is a high-level representation of the computational operations within a neural network.)

function $f(\cdot)$ to give a set of network outputs $y_{k}$. A two-layer neural network can be represented in diagram form as shown in Figure 6.9.

\title{
6.2.1 Parameter matrices
}

Section 4.1.1

As we discussed in the context of linear regression models, the bias parameters in (6.7) can be absorbed into the set of weight parameters by defining an additional input variable $x_{0}$ whose value is clamped at $x_{0}=1$, so that (6.7) takes the form

$$
a_{j}=\sum_{i=0}^{D} w_{j i}^{(1)} x_{i}
$$

We can similarly absorb the second-layer biases into the second-layer weights, so that the overall network function becomes

$$
y_{k}(\mathbf{x}, \mathbf{w})=f\left(\sum_{j=0}^{M} w_{k j}^{(2)} h\left(\sum_{i=0}^{D} w_{j i}^{(1)} x_{i}\right)\right)
$$

Another notation that will prove convenient at various points in the book is to represent the inputs as a column vector $\mathbf{x}=\left(x_{1}, \ldots, x_{N}\right)^{\mathrm{T}}$ and then to gather the weight and bias parameters in (6.11) into matrices to give

$$
\mathbf{y}(\mathbf{x}, \mathbf{w})=f\left(\mathbf{W}^{(2)} h\left(\mathbf{W}^{(1)} \mathbf{x}\right)\right)
$$

where $f(\cdot)$ and $h(\cdot)$ are evaluated on each vector element separately.

\subsection*{6.2.2 Universal approximation}

The capability of a two-layer network to model a broad range of functions is illustrated in Figure 6.10. This figure also shows how individual hidden units work collaboratively to approximate the final function. The role of hidden units in a simple classification problem is illustrated in Figure 6.11.

Figure 6.10 Illustration of the capability of a two-layer neural network to approximate four different functions: (a) $f(x)=x^{2}$, (b) $f(x)=$ $\sin (x), \quad(\mathrm{c}), f(x)=|x|$, and (d) $f(x)=H(x)$ where $H(x)$ is the Heaviside step function. In each case, $N=50$ data points, shown as blue dots, have been sampled uniformly in $x$ over the interval $(-1,1)$ and the corresponding values of $f(x)$ evaluated. These data points are then used to train a two-layer network having three hidden units with tanh activation functions and linear output units. The resulting network functions are shown by the red curves, and the outputs of the three hidden units are shown by the three dashed curves.

![](https://cdn.mathpix.com/cropped/2024_05_26_53b5c38c9dec90db1928g-1.jpg?height=401&width=491&top_left_y=222&top_left_x=624

ChatGPT figure/image summary: The image shows the approximation of a quadratic function using a two-layer neural network. The network is used to model the function \( f(x) = x^2 \). Blue dots represent 50 data points sampled uniformly over the interval \([-1, 1]\). The red curve indicates the output of the trained neural network, which approximates the parabolic shape of the quadratic function. Additionally, there are three dashed curves, each in a different color, which represent the outputs from the three hidden units with tanh activation functions within the neural network. These curves illustrate how each hidden unit contributes to the overall approximation of the quadratic function by the network.)

(a)

![](https://cdn.mathpix.com/cropped/2024_05_26_53b5c38c9dec90db1928g-1.jpg?height=396&width=486&top_left_y=674&top_left_x=634

ChatGPT figure/image summary: The image you've provided appears to be an illustration from a paper or a book related to neural networks and machine learning. The image seems to show a graph derived from a neural network model. Specifically, it looks like one of the plots from Figure 6.10 referenced in the text, where different functions are approximated by a two-layer neural network with three hidden units.

Based on the context, assume this image corresponds to one of the cases discussed in the excerpt, which refers to a two-layer neural network approximating four different functions:

- \( f(x) = x^2 \)
- \( f(x) = \sin(x) \)
- \( f(x) = |x| \)
- \( f(x) = H(x) \) (where \( H(x) \) is the Heaviside step function)

The blue dots in the plot likely represent sampled data points used for training the neural network. The red curve represents the network's output function after training, while the dashed curves seem to show the output from individual hidden units. The neural network used here includes three hidden units with tanh activation functions and linear output units. 

Since it's not explicitly labeled, the exact function being approximated by this particular plot cannot be determined without additional context or labeling within the image itself. However, if this graph depicts one of the cases mentioned in your description, it could be representing how the neural network with tanh activation functions is being used to approximate one of the given functions, with training data (blue dots) and hidden unit activations (dashed lines) showing the intermediate steps in the network's approximation process.)

(c)

![](https://cdn.mathpix.com/cropped/2024_05_26_53b5c38c9dec90db1928g-1.jpg?height=391&width=493&top_left_y=232&top_left_x=1131

ChatGPT figure/image summary: The image appears to depict a network diagram for a two-layer neural network. It likely shows nodes representing the input, hidden, and output variables connected by links that represent the weight parameters of the network. Bias parameters might be indicated by links coming from additional nodes, typically marked as \(x_0\) and \(z_0\), which are typically set to a value of one. In the diagram, the direction of information flow through the network would be displayed by arrows, indicating the path from input to output during forward propagation of the neural network. The essence of the depicted network is a visualization of how data might be transformed as it passes through the network's layers, leading to a set of outputs \(y_k\). The diagram would be used to illustrate concepts discussed in the paper, such as the network's architecture, parameter matrices, and the computation performed by the network, combining the weight matrices with activation functions to produce outputs from inputs. Since I cannot visually process the image, I'm providing a description based on the context you've given. If you would like a detailed description of the actual image, you can enable image capabilities and ask for image details.)

(b)

![](https://cdn.mathpix.com/cropped/2024_05_26_53b5c38c9dec90db1928g-1.jpg?height=393&width=481&top_left_y=673&top_left_x=1142

ChatGPT figure/image summary: The image depicts the network diagram for a two-layer neural network as described in your provided context. The diagram likely features a set of nodes connected by links that represent the architecture of the neural network, including input nodes, hidden nodes, output nodes, and their corresponding weighted connections. The bias parameters are typically represented by connections coming from nodes with a fixed value (often set to 1), denoted by solid nodes $x_0$ and $z_0$. Since I don't have the ability to visualize or generate images on my own, I cannot provide the exact look of the figure. However, considering the description, the diagram would show arrows indicating the flow of information from the input layer through the hidden layer(s) to the output layer, reflecting the forward propagation of data through the network.)

(d)

The approximation properties of two-layer feed-forward networks were widely studied in the 1980s, with various theorems showing that, for a wide range of activation functions, such networks can approximate any function defined over a continuous subset of $\mathbb{R}^{D}$ to arbitrary accuracy (Funahashi, 1989; Cybenko, 1989; Hornik, Stinchcombe, and White, 1989; Leshno et al., 1993). A similar result holds for functions from any finite-dimensional discrete space to any another. Neural networks are therefore said to be universal approximators.

Although such theorems are reassuring, they tell us only that there exists a network that can represent the required function. In some cases, they may require networks that have an exponentially large number of hidden units. Moreover, they say nothing about whether such a network can be found by a learning algorithm. Fur-

Section 9.1.2 thermore, we will see later that the no free lunch theorem says that we can never find a truly universal machine learning algorithm. Finally, although networks having two layers of weights are universal approximators, in a practical application, there can be huge benefits in considering networks having many more than two layers that can learn hierarchical internal representations. All these points support the drive towards deep learning.

\title{
6.2.3 Hidden unit activation functions
}

We have seen that the activation functions for the output units are determined by the kind of distribution being modelled. For the hidden units, however, the only requirement is that they need to be differentiable, which leaves a wide range of pos-

Figure 6.11 Example of the solution of a simple two-class classification problem involving synthetic data using a neural network having two inputs, two hidden units with tanh activation functions, and a single output having a logistic-sigmoid activation function. The dashed blue lines show the $z=0.5$ contours for each of the hidden units, and the red line shows the $y=$ 0.5 decision surface for the network. For comparison, the green lines denote the optimal decision boundary computed from the distributions used to generate the data.

![](https://cdn.mathpix.com/cropped/2024_05_26_69d949d0ac2b0e71376dg-1.jpg?height=523&width=650&top_left_y=232&top_left_x=955

ChatGPT figure/image summary: This image appears to be a scatter plot with two types of points, shown as blue circles and red crosses, representing a synthetic data set for a two-class classification problem. The dashed blue lines correspond to the \( z=0.5 \) contours for each of the two hidden units in the neural network, which presumably have tanh activation functions. The solid red line indicates the \( y=0.5 \) decision surface of the neural network, which is the boundary used by the network to differentiate between the two classes. Additionally, there is a solid green line that represents the optimal decision boundary computed from the distributions used to generate the data points. This demonstrates how a neural network with a given architecture performs in terms of separating the classes based on the learned decision boundary compared to the ideal one.)

sibilities. In most cases, all the hidden units in a network will be given the same activation function, although in principle there is no reason why different choices could not be applied in different parts of the network.

The simplest option for a hidden unit activation function is the identity function, which means that all the hidden units become linear. However, for any such network, we can always find an equivalent network without hidden units. This follows from the fact that the composition of successive linear transformations is itself a linear transformation, and so its representational capability is no greater than that of a single linear layer. However, if the number of hidden units is smaller than either the number of input or output units, then the transformations that such a network can generate are not the most general possible linear transformation from inputs to outputs because information is lost in the dimensionality reduction at the hidden units. Consider a network with $N$ inputs, $M$ hidden units, and $K$ outputs, and where all activation functions are linear. Such a network has $M(N+K)$ parameters, whereas a linear transformation of inputs directly to outputs would have $N K$ parameters. If $M$ is small relative to $N$ or $K$, or both, this leads to a two-layer linear network having fewer parameters than the direct linear mapping, corresponding to a rank-deficient transformation. Such 'bottleneck' networks of linear units corresponds to a standard data analysis technique called principal component analysis. In general, however, there is limited interest in using multilayer networks of linear units since the overall function computed by such a network is still linear.

A simple, nonlinear differentiable function is the logistic sigmoid given by

$$
\sigma(a)=\frac{1}{1+\exp (-a)}
$$

which is plotted in Figure 5.12. This was widely used in the early years of work on multilayer neural networks and was partly inspired by studies of the properties of

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=1026&width=1497&top_left_y=200&top_left_x=150

ChatGPT figure/image summary: The image displays six graphs, each representing a different nonlinear activation function used in neural networks:

(a) tanh (hyperbolic tangent): A sigmoid-shaped function that outputs values between -1 and 1.
(b) hard tanh: A thresholded version of tanh that gives -1 for inputs less than -1 and 1 for inputs greater than 1, with a linear relationship between -1 and 1.
(c) softplus: A smooth approximation to the ReLU (Rectified Linear Unit) with a gradual curve, approaching the line y = x for large positive inputs.
(d) ReLU: A function that outputs the input directly for positive inputs and zero for negative inputs.
(e) leaky ReLU: Similar to ReLU but allows a small, non-zero output for negative inputs, defined by a slope parameter α.
(f) absolute: A function that outputs the absolute value of the input, creating a V-shaped graph.

Each graph plots the function’s output as a function of input values, demonstrating their different behaviors for activation in artificial neurons.)

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=442&width=473&top_left_y=214&top_left_x=169

ChatGPT figure/image summary: The image appears to be a plot of the hyperbolic tangent (tanh) activation function, which is commonly used in artificial neural networks. The plot shows the function's characteristic S-shaped curve, which asymptotically approaches 1 for large positive inputs and -1 for large negative inputs, with a transition around the origin (0,0). The tanh function is a rescaled version of the logistic sigmoid function that ranges from -1 to 1, making it zero-centered, which can sometimes lead to better performance in neural networks during training.)

(a)

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=437&width=486&top_left_y=719&top_left_x=158

ChatGPT figure/image summary: The image displays a graph of the Rectified Linear Unit (ReLU) activation function, which is a piecewise linear function that outputs zero for any negative input and outputs the input itself for any positive input. The graph shows the function over a range of values, demonstrating that the ReLU activation function is zero when the input is less than zero (the x-axis) and linear with a slope of 1 when the input is positive. The ReLU is widely used in the field of neural networks due to its computational efficiency and its ability to alleviate the vanishing gradients problem during training.)

(d)

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=442&width=476&top_left_y=216&top_left_x=658

ChatGPT figure/image summary: The image appears to be a graph plotting a piecewise linear function known as the "hard tanh." This function is generally used as an activation function in neural networks and is defined such that it outputs -1 for inputs less than -1, outputs +1 for inputs greater than 1, and is linear between -1 and 1 (a slope of 1). The graph shows the sharp transitions at the points where the input value is -1 and 1, which is characteristic of the "hard" version of the tanh function. This is in contrast to the smoother, sigmoid-shaped curve of the standard tanh function. The graph is annotated with the label "hard tanh" and includes axes with tick marks, illustrating the behavior of the function across a range of input values from approximately -2.5 to 2.5.)

(b)

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=440&width=481&top_left_y=723&top_left_x=658

ChatGPT figure/image summary: The image is a graphical representation of the leaky ReLU (Rectified Linear Unit) activation function used in neural networks. The function is given by the formula \( h(a) = \max(0, a) + \alpha \min(0, a) \), where \( \alpha \) is a small, positive parameter that allows for a non-zero gradient when the input \( a \) is negative. 

In the plot, the x-axis represents the input \( a \) to the activation function, while the y-axis represents the output \( h(a) \). For positive values of \( a \), the function has a positive slope (the identity function), and for negative values of \( a \), there is a smaller positive slope determined by \( \alpha \), instead of being zero as in the case of the standard ReLU. This gives the line its "leaky" characteristic, preventing the problem where units never activate (dying ReLU problem) during training because they have a negative input.

The dashed vertical and horizontal lines at 0 on the x-axis and y-axis probably denote the origin where the input 'a' is zero and serve as a reference for the function's behavior. The solid red line represents the leaky ReLU function itself. The label "leaky ReLU" in the graph confirms that this is a plot of the leaky ReLU activation function.)

(e)

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=442&width=491&top_left_y=219&top_left_x=1152

ChatGPT figure/image summary: In the image, there is a graph plotting the "softplus" activation function, which is a type of mathematical function used in neural network models. The x-axis represents the input to the activation function "a," and the y-axis represents the output "h(a)". The softplus function equation is given by \(h(a) = \ln(1 + \exp(a))\). This function gradually approaches a linear function for large positive input values, without becoming constant, which helps to alleviate the problem of vanishing gradients often encountered with traditional sigmoidal activation functions. The graph shows a smooth curve starting from the bottom left, gradually increasing and becoming more linear as the input value increases towards the right side.)

(c)

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=439&width=491&top_left_y=721&top_left_x=1152

ChatGPT figure/image summary: The image at the end of your message appears to depict a graph of an absolute value function, which is a piecewise function that outputs the absolute value of the input. The graph is V-shaped and shows how the function operates on inputs along the x-axis; it mirrors the input value about the y-axis when the input is negative, effectively removing any negative sign. The y-axis represents the function's output. This function is continuous, non-differentiable at the origin where the input is zero, and linear elsewhere. The context suggests that this is related to a variant of an activation function used in neural networks, which may be described as an 'absolute value activation function,' that outputs the absolute value of the input.)

(f)

Figure 6.12 A variety of nonlinear activation functions.

biological neurons. A closely related function is tanh, which is defined by

$$
\tanh (a)=\frac{e^{a}-e^{-a}}{e^{a}+e^{-a}}
$$

which is plotted in Figure 6.12(a). This function differs from the logistic sigmoid by a linear transformation of its input and its output values, and so for any network

\title{
Exercise 6.4
} with logistic-sigmoid hidden-unit activation functions, there is an equivalent network with tanh activation functions. However, when training a network, these are not necessarily equivalent because for gradient-based optimization, the network weights and biases need to be initialized, and so if the activation functions are changed, then the initialization scheme must be adjusted accordingly. A 'hard' version of the tanh function (Collobert, 2004) is given by

$$
h(a)=\max (-1, \min (1, a))
$$

and is plotted in Figure 6.12(b).

A major drawback of both the logistic sigmoid and the tanh activation functions is that the gradients go to zero exponentially when the inputs have either large positive or large negative values. We will discuss this 'vanishing gradients' issue later,

\section*{Exercise 6.7}

Exercise 6.5 but for the moment, we note that it will generally be better to use activation functions with non-zero gradients, at least when the input takes a large positive value. One such choice is the softplus activation function given by

$$
h(a)=\ln (1+\exp (a))
$$

which is plotted in Figure 6.12(c). For $a \gg 1$, we have $h(a) \simeq a$, and so the gradient remains non-zero even when the input to the activation function is large and positive, thereby helping to alleviate the vanishing gradients problem.

An even simpler choice of activation function is the rectified linear unit or $R e L U$, which is defined by

$$
h(a)=\max (0, a)
$$

and which is plotted in Figure 6.12(d). Empirically, this is one of the best-performing activation functions, and it is in widespread use. Note that strictly speaking, the derivative of the ReLU function is not defined when $a=0$, but in practice this can be safely ignored. The softplus function (6.16) can be viewed as a smoothed version of the ReLU and is therefore also sometimes called soft ReLU.

Although the ReLU has a non-zero gradient for positive input values, this is not the case for negative inputs, which can mean that some hidden units receive no 'error signal' during training. A modification of ReLU that seeks to avoid this issue is called a leaky ReLU and is defined by

$$
h(a)=\max (0, a)+\alpha \min (0, a),
$$

where $0<\alpha<1$. This function is plotted in Figure 6.12(e). Unlike ReLU, this has a nonzero gradient for input values $a<0$, which ensures that there is a signal to drive training. A variant of this activation function uses $\alpha=-1$, in which case $h(a)=|a|$, which is plotted in Figure 6.12(f). Another variant allows each hidden unit to have its own value $\alpha_{j}$, which can be learned during network training by evaluating gradients with respect to the $\left\{\alpha_{j}\right\}$ along with the gradients with respect to the weights and biases.

The introduction of ReLU gave a big improvement in training efficiency over previous sigmoidal activation functions (Krizhevsky, Sutskever, and Hinton, 2012). As well as allowing deeper networks to be trained efficiently, it is much less sensitive to the random initialization of the weights. It is also well suited to a low-precision implementation, such as 8 -bit fixed versus 64 -bit floating point, and it is computationally cheap to evaluate. Many practical applications simply use ReLU units as the default unless the goal is explicitly to explore the effects of different choices of activation function.

\subsection*{6.2.4 Weight-space symmetries}

One property of feed-forward networks is that multiple distinct choices for the weight vector $\mathbf{w}$ can all give rise to the same mapping function from inputs to outputs (Chen, Lu, and Hecht-Nielsen, 1993). Consider a two-layer network of the form shown in Figure 6.9 with $M$ hidden units having tanh activation functions and full connectivity in both layers. If we change the sign of all the weights and the bias

feeding into a particular hidden unit, then, for a given input data point, the sign of the pre-activation of the hidden unit will be reversed, and therefore so too will the activation, because tanh is an odd function, so that $\tanh (-a)=-\tanh (a)$. This transformation can be exactly compensated for by changing the sign of all the weights leading out of that hidden unit. Thus, by changing the signs of a particular group of weights (and a bias), the input-output mapping function represented by the network is unchanged, and so we have found two different weight vectors that give rise to the same mapping function. For $M$ hidden units, there will be $M$ such 'sign-flip' symmetries, and thus, any given weight vector will be one of a set $2^{M}$ equivalent weight vectors

Similarly, imagine that we interchange the values of all of the weights (and the bias) leading both into and out of a particular hidden unit with the corresponding values of the weights (and bias) associated with a different hidden unit. Again, this clearly leaves the network input-output mapping function unchanged, but it corresponds to a different choice of weight vector. For $M$ hidden units, any given weight vector will belong to a set of $M \times(M-1) \times \cdots \times 2 \times 1=M$ ! equivalent weight vectors associated with this interchange symmetry, corresponding to the $M$ ! different orderings of the hidden units. The network will therefore have an overall weight-space symmetry factor of $M!2^{M}$. For networks with more than two layers of weights, the total level of symmetry will be given by the product of such factors, one for each layer of hidden units.

It turns out that these factors account for all the symmetries in weight space (except for possible accidental symmetries due to specific choices for the weight values). Furthermore, the existence of these symmetries is not a particular property of the tanh function but applies to a wide range of activation functions (Kurková and Kainen, 1994). In general, these symmetries in weight space are of little practical consequence, since network training aims to find a specific setting for the parameters, and the existence of other, equivalent, settings is of little consequence. However, weight-space symmetries do play a role when Bayesian methods are used to evaluate the probability distribution over networks of different sizes (Bishop, 2006).

\title{
6.3. Deep Networks
}

We have motivated the development of neural networks by making the basis functions of a linear regression or classification model themselves be governed by learnable parameters, giving rise to the two-layer network model shown in Figure 6.9. For many years, this was the most widely used architecture, primarily because it proved difficult to train networks with more than two layers effectively. However, extending neural networks to have more than two layers, known as deep neural networks, brings many advantages as we will discuss shortly, and recent advances in techniques

Chapter 7 for training neural networks are effective for networks with many layers.

We can easily extend the two-layer network architecture (6.12) to any finite number $L$ of layers, in which layer $l=1, \ldots, L$ computes the following function:

$$
\mathbf{z}^{(l)}=h^{(l)}\left(\mathbf{W}^{(l)} \mathbf{z}^{(l-1)}\right)
$$

where $h^{(l)}$ denotes the activation function associated with layer $l$, and $\mathbf{W}^{(l)}$ denotes the corresponding matrix of weight and bias parameters. Also, $\mathbf{z}^{(0)}=\mathrm{x}$ represents the input vector and $\mathbf{z}^{(L)}=\mathbf{y}$ represents the output vector.

Note that there has been some confusion in the literature regarding the terminology for counting the number of layers in such networks. Thus, the network in Figure 6.9 is sometimes described as a three-layer network (which counts the number of layers of units and treats the inputs as units) or sometimes as a single-hiddenlayer network (which counts the number of layers of hidden units). We recommend a terminology in which Figure 6.9 is called a two-layer network, because it is the number of layers of learnable weights that is important for determining the network properties.

We have seen that a network of the form shown in Figure 6.9, having two layers of learnable parameters, has universal approximation capabilities. However, networks with more than two layers can sometimes represent a given function with far fewer parameters than a two-layer network. Montúfar et al. (2014) show that the network function divides the input space into a number of regions that is exponential in the depth of the network, but which is only polynomial in the width of the hidden layers. To represent the same function using a two-layer network would require an exponential number of hidden units.

\title{
6.3.1 Hierarchical representations
}

Although this is an interesting result, a more compelling reason to explore deep neural networks is that the network architecture encodes a particular form of inductive bias, namely that the outputs are related to the input space through a hierarchical representation. A good example is the task of recognizing objects in images. The relationship between the pixels of an image and a high-level concept such as 'cat' is highly complex and nonlinear, and would be an extremely challenging problem for a two-layer network. However, a deep neural network can learn to detect low-level features, such as edges, in the early layers, and can then combine these in subsequent layers to make higher-level features such as eyes or whiskers, which in turn can be combined in later layers to detect the presence of a cat. This can be viewed as a compositional inductive bias, in which higher-level objects, such as a cat, are composed of lower-level objects, such as eyes, which in turn have yet lower-level elements such as edges. We can also think of this in reverse by considering the process of generating an image starting with low-level features such as edges, then combining these to form simple shapes such as circles, and then combining those in turn to form higher-level objects such as cats. At each stage there are many ways to combine different components, giving an exponential gain in the number of possibilities with increasing depth.

\subsection*{6.3.2 Distributed representations}

Neural networks can take advantage of another form of compositionality called a distributed representation. Conceptually, each unit in a hidden layer can be thought of as representing a 'feature' at that level of the network, with a high value of the

Chapter 10

Section 1.1.1

Section 19.1 activation indicating that the corresponding feature is present and a low value indicating its absence. With $M$ units in a given layer, such a network can represent $M$ different features. However, the network could potentially learn a different representation in which combinations of hidden units represent features, thereby potentially allowing a hidden layer with $M$ units to represent $2^{M}$ different features, growing exponentially with the number of units. Consider, for example, a network designed to process images of faces. Each particular face image may or may not have glasses, it may or may not have a hat, and it may or may not have a beard, leading to eight different combinations. Although this could be represented by eight units each of which 'turns on' when it detects the corresponding combination, it could also be represented more compactly by just three units, one for each attribute. These can be present independently of each other (although statistically their presence is likely to be correlated to some degree). Later, we will explore in detail the kinds of internal representations that deep learning networks discover for themselves during training.

\subsection*{6.3.3 Representation learning}

We can view the successive layers of a deep neural network as performing transformations of the data, that make it easier to solve the desired task or tasks. For example, a neural network that successfully learns to classify skin lesions as benign or malignant must have learned to transform the original image data into a new space, represented by the outputs of the final layer of hidden units, such that the final layer of the network can distinguish the two classes. This final layer can be viewed as a simple linear classifier, and so in the representation of the last hidden layer, the two classes must be well separated by a linear surface. This ability to discover a nonlinear transformation of the data that makes subsequent tasks easier to solve is called representation learning (Bengio, Courville, and Vincent, 2012). The learned representation, sometimes called the embedding space, is given by the outputs of one of the hidden layers of the network, so that any input vector, either from the training set or from some new data set, can be transformed into this representation by forward propagation through the network.

Representation learning is especially powerful because it allows us to exploit unlabelled data. Often it is easy to collect a large quantity of unlabelled data, but acquiring the associated labels may be more difficult. For example, a video camera on a vehicle can gather large numbers of images of urban scenes as the vehicle is driven around a city, but taking those images and identifying relevant objects, such as pedestrians and road signs, would require expensive and time-consuming human labelling.

Learning from unlabelled data is called unsupervised learning, and many different algorithms have been developed to do this. For example, a neural network can be trained to take images as input and to create the same images as the output. To make this into a non-trivial task, the network may use hidden layers with fewer units than the number of pixels in the image, thereby forcing the network to learn some kind of compression of the images. Only unlabelled data is needed because each image in the training set acts as both the input vector and the target vector. Such networks are known as autoencoders. The goal is that this type of training will force the network

Chapter 12

Section 1.1.1

Chapter 10 to discover some internal representation for the data that is useful for solving other tasks, such as image classification.

Historically, unsupervised learning played an important role in enabling the first deep networks (apart from convolutional networks) to be successfully trained. Each layer of the network was first pre-trained using unsupervised learning and then the entire network was trained further using gradient-based supervised training. It was later discovered that the pre-training phase could be omitted and a deep network could be trained from scratch purely using supervised learning given appropriate conditions.

However, pre-training and representation learning remain central to deep learning in other contexts. The most notable example of pre-training is in natural language processing in which transformer models are trained on large quantities of text and are able to learn highly sophisticated internal representations of language that facilitates an impressive range of capabilities at human level and beyond.

\subsection*{6.3.4 Transfer learning}

The internal representation learned for one particular task might also be useful for related tasks. For example, a network trained on a large labelled data set of everyday objects can learn how to transform an image representation into one that is much better suited for classifying objects. Then, the final classification layer of the network can be retrained using a smaller labelled data set of skin lesion images to create a lesion classifier. This is an example of transfer learning (Hospedales et al., 2021), which allows higher accuracy to be achieved than if only the lesion image data were used for training, because the network can exploit commonalities shared by natural images in general. Transfer learning is illustrated in Figure 6.13.

In general, transfer learning can be used to improve performance on some task A, for which training data is in short supply, by using data from a related task B, for which data is more plentiful. The two tasks should have the same kind of inputs, and there should be some commonality between the tasks so that low-level features, or internal representations, learned from task B will be useful for task A. When we look at convolutional networks we will see that many image processing tasks require similar low-level features corresponding to the early layers of a deep neural network, whereas later layers are more specialized to a particular task, making such networks well suited to transfer learning applications.

When data for task A is very scarce, we might simply re-train the final layer of the network. In contrast, if there are more data points, it is feasible to retrain several layers. The process of learning parameters using one task that are then applied to one or more other tasks is called pre-training. Note that for the new task, instead of applying stochastic gradient descent to the whole network, it is much more efficient to send the new training data once through the fixed pre-trained network so as to evaluate the training inputs in the new representation. Iterative gradient-based optimization can then be applied just to the smaller network consisting of the final layers. As well as using a pre-trained network as a fixed pre-processor for a different task, it is also possible to apply fine-tuning in which the whole network is adapted to the data for task A. This is generally done with a very small learning rate for a lim-

application. However, these models have some severe limitations, and so we will

Section 6.3.6 begin our discussion of neural networks by exploring these limitations and understanding why it is necessary to use basis functions that are themselves learned from data. This leads naturally to a discussion of neural networks having more than one

\title{
Section 6.3 .6
} layer of learnable parameters. These are known as feed-forward networks or multilayer perceptrons. We will also discuss the benefits of having many such layers of processing, leading to the key concept of deep neural networks that now dominate the field of machine learning.

\subsection*{6.1. Limitations of Fixed Basis Functions}

\section*{Chapter 5}

Chapter 4

Section 1.2
Linear basis function models for classification are based on linear combinations of basis functions $\phi_{j}(\mathbf{x})$ and take the form

$$
y(\mathbf{x}, \mathbf{w})=f\left(\sum_{j=1}^{M} w_{j} \phi_{j}(\mathbf{x})+w_{0}\right)
$$

where $f(\cdot)$ is a nonlinear output activation function. Linear models for regression take the same form but with $f(\cdot)$ replaced by the identity. These models allow for an arbitrary set of nonlinear basis functions $\left\{\phi_{i}(\mathbf{x})\right\}$, and because of the generality of these basis functions, such models can in principle provide a solution to any regression or classification problem. This is true in a trivial sense in that if one of the basis functions corresponds to the desired input-to-output transformation, then the learnable linear layer simply has to copy the value of this basis function to the output of the model.

More generally, we would expect that a sufficiently large and rich set of basis functions would allow any desired function to be approximated to arbitrary accuracy. It would seem therefore that such linear models constitute a general purpose framework for solving problems in machine learning. Unfortunately, there are some significant shortcomings with linear models, which arise from the assumption that the basis functions $\phi_{j}(\mathbf{x})$ are fixed and independent of the training data. To understand these limitations, we start by looking at the behaviour of linear models as the number of input variables is increased.

\subsection*{6.1.1 The curse of dimensionality}

Consider a simple regression model for a single input variable given by a polynomial of order $M$ in the form

$$
y(x, \mathbf{w})=w_{0}+w_{1} x+w_{2} x^{2}+\ldots+w_{M} x^{M}
$$

and let us see what happens if we increase the number of inputs. If we have $D$ input variables $\left\{x_{1}, \ldots, x_{D}\right\}$, then a general polynomial with coefficients up to order 3

![](https://cdn.mathpix.com/cropped/2024_05_26_802d1a9c0b0fab763da6g-1.jpg?height=362&width=1453&top_left_y=210&top_left_x=172

ChatGPT figure/image summary: The image depicts a simplified illustration of a neural network being applied to an image classification task. An image on the left, featuring a cat, serves as the input to the network. The network consists of a series of layers, represented by red rectangles, which mimic the structure of a feed-forward neural network or a multilayer perceptron. The layers process the input image and ultimately provide an output, which is a classification of the image content. The output is shown on the right as a list of possible categories (e.g., tree, cat, dog, etc.), with a bar next to the category "cat" filled in blue, indicating that the network has classified the input image as that of a cat. This type of visualization is often used to explain how deep learning models process and classify visual information.)

(a)

![](https://cdn.mathpix.com/cropped/2024_05_26_802d1a9c0b0fab763da6g-1.jpg?height=356&width=1451&top_left_y=640&top_left_x=176

ChatGPT figure/image summary: The image depicts a schematic illustration of a neural network being used for transfer learning in the context of skin lesion classification. It shows a simplified representation of a deep neural network with multiple layers. The input to the network is an image of a skin lesion, which can be inferred from the text preceding the image in the given context.

The network comprises several layers, with the first few layers colored in red, indicating that these layers are copied from a network that was pre-trained on a different but related task, such as object classification of natural images, which typically has abundant data. These early layers are meant to capture the general features that can be shared across the different tasks.

The latter part of the network, shown in blue, represents the layers that are fine-tuned or retrained specifically for the task of classifying skin lesions as 'cancer' or 'normal'. This part of the network is adapted to recognize patterns specific to the classification of skin lesions, using a smaller dataset specific to this task.

The decision, signified by the blue squares, shows the output classification results of the network, with options for 'cancer' and 'normal'. This is a typical example of a binary classification problem in machine learning applied to medical diagnostics, where the goal is to correctly identify whether the lesion is indicative of cancer or not.

The overall conceptual illustration is meant to convey how transfer learning uses knowledge acquired from one task to improve performance in another task, especially when the data available for the new task is more limited.
)

(b)

Figure 6.13 Schematic illustration of transfer learning. (a) A network is first trained on a task with abundant data, such as object classification of natural images. (b) The early layers of the network (shown in red) are copied from the first task and the final few layers of the network (shown in blue) are then retrained on a new task such as skin lesion classification for which training data is more scarce.

ited number of iterations to ensure that the network does not over-fit to the relatively small data set available for the new task.

A related approach is multitask learning (Caruana, 1997) in which a network jointly learns more than one related task at the same time. For example, we might wish to construct a spam email filter that allows different users to have different classifiers tuned to their particular preferences. The training data may comprise examples of spam email and non-spam email for many different users, but the number of examples for any one user may be quite limited, and therefore training a separate classifier for each user would give poor results. Instead, we can combine the data sets to train a single larger network that might, for example, share early layers but have separate learnable parameters for the different users in later layers. Sharing data across tasks allows the network to exploit commonalities amongst the tasks, thereby improving the accuracy for all users. With a large number of training examples, a deeper network with more parameters can be used, again leading to improved performance.

Learning across multiple tasks can be extended to meta-learning, which is also called learning to learn. Whereas multitask learning aims to make predictions for a fixed set of tasks, the aim of meta-learning is to make predictions for future tasks that were not seen during training. This can be done by not only learning a shared

internal representation across tasks but also by learning the learning algorithm itself (Hospedales et al., 2021). Meta-learning can be used to facilitate generalization of, for example, a classification model to new classes when there are very few labelled examples of the new classes. This is referred to as few-shot learning. When only a single labelled example is used it is called one-shot learning.

\title{
6.3.5 Contrastive learning
}

One of the most common and powerful representation learning methods is contrastive learning (Gutmann and Hyvärinen, 2010; Oord, Li, and Vinyals, 2018; Chen, Kornblith, et al., 2020). The idea is to learn a representation such that certain pairs of inputs, referred to as positive pairs, are close in the embedding space, and other pairs of inputs, called negative pairs, are far apart. The intuition is that if we choose our positive pairs in such a way that they are semantically similar and choose negative pairs that are semantically dissimilar, then we will learn a representation space in which similar inputs are close, making downstream tasks, such as classification, much easier. As with other forms of representation learning, the outputs of the trained network are typically not used directly, and instead the activations at some earlier layer are used to form the embedding space. Contrastive learning is unlike most other machine learning tasks, in that the error function for a given input is defined only with respect to other inputs, instead of having a per-input label or target output.

Suppose we have a given data point $\mathrm{x}$ called the anchor, for which we have specified another data point $\mathbf{x}^{+}$that together with $\mathbf{x}$ makes up a positive pair. We must also specify a set of data points $\left\{\mathbf{x}_{1}^{-}, \ldots, \mathbf{x}_{N}^{-}\right\}$each of which makes up a negative pair with $\mathrm{x}$. We now need a loss function that will reward close proximity between the representations of $\mathbf{x}$ and $\mathbf{x}^{+}$while encouraging a large distance between each pair $\left\{\mathbf{x}, \mathbf{x}_{n}^{-}\right\}$. One example of such a function, and the most commonly used loss function for contrastive learning, is called the InfoNCE loss (Gutmann and Hyvärinen, 2010; Oord, Li, and Vinyals, 2018), where NCE denotes 'noise contrastive estimation'. Suppose we have a neural network function $\mathbf{f}_{\mathrm{w}}(\mathbf{x})$ that maps points from the input space $\mathrm{x}$ to a representation space, governed by learnable parameters $\mathrm{w}$. This representation is normalized so that $\left\|\mathbf{f}_{\mathbf{w}}(\mathbf{x})\right\|=1$. Then, for a data point $\mathbf{x}$, the InfoNCE loss is defined by

$$
E(\mathbf{w})=-\ln \frac{\exp \left\{\mathbf{f}_{\mathbf{w}}(\mathbf{x})^{\mathrm{T}} \mathbf{f}_{\mathbf{w}}\left(\mathbf{x}^{+}\right)\right\}}{\exp \left\{\mathbf{f}_{\mathbf{w}}(\mathbf{x})^{\mathrm{T}} \mathbf{f}_{\mathbf{w}}\left(\mathbf{x}^{+}\right)\right\}+\sum_{n=1}^{N} \exp \left\{\mathbf{f}_{\mathbf{w}}(\mathbf{x})^{\mathrm{T}} \mathbf{f}_{\mathbf{w}}\left(\mathbf{x}_{n}^{-}\right)\right\}}
$$

We can see that in this function, the cosine similarity $\mathbf{f}_{\mathbf{w}}(\mathbf{x})^{T} \mathbf{f}_{\mathbf{w}}\left(\mathbf{x}^{+}\right)$between the representation $f_{w}(x)$ of the anchor and the representation $f_{w}\left(x^{+}\right)$of the positive example provides our measure of how close the positive pair examples are in the learned space, and the same measure is used to assess how close the anchor is to the negative examples. Note that the function resembles a classification cross-entropy error function in which the cosine similarity of the positive pair gives the logit for the label class and the cosine similarities for the negative pairs give the logits for the incorrect classes. Also note that the negative pairs are crucial as without them the

embedding would simply learn the degenerate solution of mapping every point to the same representation.

A particular contrastive learning algorithm is defined predominantly by how the positive and negative pairs are chosen, which is how we use our prior knowledge to specify what a good representation should be. For example, consider the problem of learning representations of images. Here, a common choice is to create positive pairs by corrupting the input images in ways that should preserve the semantic information of the image while greatly altering the image in the pixel space (Wu et al., 2018; He et al., 2019; Chen, Kornblith, et al., 2020). Corruptions are closely related to data augmentations, and examples include rotation, translation, and colour shifts. Other images from the data set can then be used to create the negative pairs. This approach to contrastive learning is known as instance discrimination.

If, however, we have access to class labels, then we can use images of the same class as positive pairs and images of different classes as negative pairs. This relaxes the reliance on specifying the augmentations that the representation should be invariant to and also avoids treating two semantically similar images as a negative pair. This is referred to as supervised contrastive learning (Khosla et al., 2020) because of the reliance on the class labels, and it can often yield better results than simply learning the representation using cross-entropy classification.

The members of positive and negative pairs do not necessarily have to come from the same data modality. In contrastive-language image pretraining, or CLIP (Radford et al., 2021), a positive pair consists of an image and its corresponding text caption, and two separate functions, one for each modality, are used to map the inputs to the same representation space. Negative pairs are then mismatched images and captions. This is often referred to as weakly supervised, as it relies on captioned images, which are often easier to obtain by scraping data from the internet than by manually labelling images with their classes. The loss function in this case is given by

$$
\begin{aligned}
E(\mathbf{w})= & -\frac{1}{2} \ln \frac{\exp \left\{\mathbf{f}_{\mathbf{w}}\left(\mathbf{x}^{+}\right)^{\mathrm{T}} \mathbf{g}_{\boldsymbol{\theta}}\left(\mathbf{y}^{+}\right)\right\}}{\exp \left\{\mathbf{f}_{\mathbf{w}}\left(\mathbf{x}^{+}\right)^{\mathrm{T}} \mathbf{g}_{\boldsymbol{\theta}}\left(\mathbf{y}^{+}\right)\right\}+\sum_{n=1}^{N} \exp \left\{\mathbf{f}_{\mathbf{w}}\left(\mathbf{x}_{n}^{-}\right)^{\mathrm{T}} \mathbf{g}_{\boldsymbol{\theta}}\left(\mathbf{y}^{+}\right)\right\}} \\
& -\frac{1}{2} \ln \frac{\exp \left\{\mathbf{f}_{\mathbf{w}}\left(\mathbf{x}^{+}\right)^{\mathrm{T}} \mathbf{g}_{\boldsymbol{\theta}}\left(\mathbf{y}^{+}\right)\right\}}{\exp \left\{\mathbf{f}_{\mathbf{w}}\left(\mathbf{x}^{+}\right)^{\mathrm{T}} \mathbf{g}_{\boldsymbol{\theta}}\left(\mathbf{y}^{+}\right)\right\}+\sum_{m=1}^{M} \exp \left\{\mathbf{f}_{\mathbf{w}}\left(\mathbf{x}^{+}\right)^{\mathrm{T}} \mathbf{g}_{\boldsymbol{\theta}}\left(\mathbf{y}_{m}^{-}\right)\right\}}
\end{aligned}
$$

where $\mathbf{x}^{+}$and $\mathbf{y}^{+}$represent a positive pair in which $\mathrm{x}$ is an image and $\mathbf{y}$ is its corresponding text caption, $\mathbf{f}_{\mathbf{w}}$ represents the mapping from images to the representation space, and $\mathbf{g}_{\theta}$ is the mapping from text input to the representation space. We also require a set $\left\{\mathbf{x}_{1}^{-}, \ldots, \mathbf{x}_{N}^{-}\right\}$of other images from the data set, for which we can assume the text caption $\mathbf{y}^{+}$is inappropriate, and a set $\left\{\mathbf{y}_{1}^{-}, \ldots, \mathbf{y}_{M}^{-}\right\}$of text captions that are similarly mismatched to the input image $\mathbf{x}$. The two terms in the loss function ensure that (a) the representation of the image is close to its text caption representation relative to other image representations and (b) the text caption representation is close to the representation of the image it describes relative to other representations of text captions. Although CLIP uses text and image pairs, any data

![](https://cdn.mathpix.com/cropped/2024_05_26_2753d844c203dd6fd40ag-1.jpg?height=571&width=440&top_left_y=215&top_left_x=151

ChatGPT figure/image summary: The image you provided contains a visual representation of a contrastive learning paradigm, specifically the instance discrimination approach as described in the contextual information you shared. Here is a description of the components depicted in the image:

- At the top, there is a shaded sphere representing a unit hypersphere, which is a high-dimensional space where the learned representations of images are projected.
- Three arrows originate from the central point on the sphere, each pointing to a different representation on the sphere's surface. Each arrow corresponds to a different image representation obtained through the contrastive learning process.
- The red arrow points to a representation labeled as \( f_w(X^-) \), which represents a negative pair instance.
- The green arrow points to the representation of the original image, labeled as \( f_w(X) \).
- The black arrow points to a representation labeled as \( f_w(X^+) \), which is a positive pair instance, likely an augmented version of the original image represented by \( f_w(X) \).

Below the sphere, three images are displayed:

1. The left image, labeled as \( X \), shows a picture of a cat. This is the original image before any augmentations or transformations.
2. The center image, labeled as \( X^+ \), also shows the same cat, but the image might have been augmented, which could include changes like rotation, scaling, color shifting, or other transformations that preserve the semantic content while altering its appearance in pixel space.
3. The right image, labeled as \( X^- \), shows an unrelated image, in this case of a bicycle, which serves as a negative example in the contrastive learning process. It is assumed to be semantically different from the cat images.

In the context of contrastive learning, the loss function aims to bring the representations of positive pairs (such as \( X \) and \( X^+ \)) closer together while pushing the representations of negative pairs (such as those involving \( X^- \)) further apart in the representation space. The depicted unit hypersphere visually illustrates this objective, as the positive pairs would be near each other, and negative pairs would be distant.)

(a)

![](https://cdn.mathpix.com/cropped/2024_05_26_2753d844c203dd6fd40ag-1.jpg?height=528&width=452&top_left_y=212&top_left_x=663

ChatGPT figure/image summary: In the image, there are three smaller images at the bottom which appear to be illustrations for contrastive learning paradigms. These smaller images depict a ginger cat (on the left), a close-up of a similar-looking ginger cat's face (in the middle), and a bicycle leaning against a brick wall (on the right).

Above these images, there's a large depiction of a unit hypersphere and three connecting lines from the smaller images forming a triangle, pointing to three separate dots within the hypersphere. The line from the leftmost image (ginger cat) leads to a point on the hypersphere labeled \( f_w(\mathbf{x}) \), indicating the mapping of this image into the representation space. The line from the middle image (close-up of the cat's face) points to a point labeled \( f_w(\mathbf{x}^+) \), suggesting this is an augmented version of the original ginger cat image that forms a 'positive pair' with \( f_w(\mathbf{x}) \) in the representation space. The line from the image on the right (bicycle) leads to a point labeled \( f_w(\mathbf{x}^-) \), indicating that this image forms a 'negative pair' with the original cat image within the context of instance discrimination.

The red arrow between the points \( f_w(\mathbf{x}) \) and \( f_w(\mathbf{x}^-) \) visualizes the learning procedure pushing the representations of a negative pair apart, whereas the green arrow between \( f_w(\mathbf{x}) \) and \( f_w(\mathbf{x}^+) \) shows the representations of a positive pair being pulled closer together. This concept is an aspect of the contrastive learning approach for learning representations in which semantically similar images (positive pairs) are encouraged to have closer representations, and semantically different images (negative pairs) have representations that are further apart.)

$\mathbf{x}$

![](https://cdn.mathpix.com/cropped/2024_05_26_2753d844c203dd6fd40ag-1.jpg?height=520&width=452&top_left_y=214&top_left_x=1171

ChatGPT figure/image summary: The image depicts a conceptual illustration of the CLIP model discussed in the provided text excerpt, showing a positive pair made up of an image and its corresponding text caption, which are mapped to a representation space thought of as a unit hypersphere. The image shows a photo of a ginger cat sitting. Associated with this image is a matching text caption "a ginger cat sat on a wall," which forms the positive pair with the image. Additionally, there is an example of a negative text caption, "a bike leaning on a brick wall," which is not related to the image of the cat. The diagram visualizes how the CLIP model brings together the representations of the image and its correct caption, while pushing away the representation of the negative, unrelated caption. The mappings are indicated by \( f_w(x^+) \) for the image and \( g_\theta(y^+) \) for the related text caption.)

$\mathbf{x}^{+}$ $\mathbf{y}^{+}$

(c)

Figure 6.14 Illustration of three different contrastive learning paradigms. (a) The instance discrimination approach, where the positive pair is made up of the anchor and an augmented version of the same image. These are mapped to points in a normalized space that can be thought of as a unit hypersphere. The coloured arrows show that the loss encourages the representations of the positive pair to be closer together but pushes negative pairs further apart. (b) Supervised contrastive learning in which the positive pair consists of two different images from the same class. (c) The CLIP model in which the positive pair is made up of an image and an associated text snippet.

set with paired modalities can be used to learn representations. A comparison of the different contrastive learning methods we have discussed is shown in Figure 6.14.

\title{
6.3.6 General network architectures
}

So far, we have explored neural network architectures that are organized into a sequence of fully-connected layers. However, because there is a direct correspondence between a network diagram and its mathematical function, we can develop more general network mappings by considering more complex network diagrams. These must be restricted to a feed-forward architecture, in other words to one having no closed directed cycles, to ensure that the outputs are deterministic functions of the inputs. This is illustrated with a simple example in Figure 6.15. Each (hidden or output) unit in such a network computes a function given by

$$
z_{k}=h\left(\sum_{j \in \mathcal{A}(k)} w_{k j} z_{j}+b_{k}\right)
$$

where $\mathcal{A}(k)$ denotes the set of ancestors of node $k$, in other words the set of units that send connections to unit $k$, and $b_{k}$ denotes the associated bias parameter. For a given set of values applied to the inputs of the network, successive application of (6.22) allows the activations of all units in the network to be evaluated including those of the output units.

Figure 6.15 Example of a neural network having a general feed-forward topology. Note that each hidden and output unit has an associated bias parameter (omitted for clarity). inputs

outputs

![](https://cdn.mathpix.com/cropped/2024_05_26_ca627f312f31486fc9f7g-1.jpg?height=344&width=808&top_left_y=287&top_left_x=817

ChatGPT figure/image summary: The first image provided is an illustration of an instance discrimination approach used in contrastive learning. It displays two images, denoted as \(\mathbf{x}\) and \(\mathbf{x}^{+}\), with colored arrows indicating that the loss function encourages the representations of these positive pairs (anchor and augmented version of the same image) to be closer together in a normalized feature space, while pushing representations of negative pairs further apart.

The second image is a diagram of a neural network with a general feed-forward topology, which is used to describe a more complex network structure than a simple sequence of fully-connected layers. In this network diagram, there are two input units labeled \(x_1\) and \(x_2\), three hidden units labeled \(z_1\), \(z_2\), and \(z_3\), and two output units labeled \(y_1\) and \(y_2\). The diagram shows connections between units, depicting the structure of the neural network. Each hidden and output unit in the network would compute its activation as a function of its weighted inputs and a bias term, as described by the mathematical function provided in the text.

The context provided in the text explains various concepts related to neural networks, including different architectures, the role of tensors in representing data, supervised and unsupervised learning strategies, and regression approaches within the context of machine learning.)

\title{
6.3.7 Tensors
}

We see that linear algebra plays a central role in neural networks, with quantities such as data sets, activations, and network parameters represented as scalars, vectors, and matrices. However, we also encounter variables of higher dimensionality. Consider, for example, a data set of $N$ colour images each of which is $I$ pixels high and $J$ pixels wide. Each pixel is indexed by its row and column within the image and has red, green, and blue values. We have one such value for each image in the data set, and so we can represent a particular intensity value by a four-dimensional array $\mathbf{X}$ with elements $x_{i j k n}$ where $i \in\{1, \ldots, I\}$ and $j \in\{1, \ldots, J\}$ index the row and column within the image, $k \in\{1,2,3\}$ indexes the red, green, and blue intensities, and $n \in\{1, \ldots, N\}$ indexes the particular image within the data set. These higher-dimensional arrays are called tensors and include scalars, vectors, and matrices as special cases. We will see many examples of such tensors when we discuss more sophisticated neural network architectures later in the book. Massively parallel processors such as GPUs are especially well suited to processing tensors.

\subsection*{6.4. Error Functions}

Chapter 4 Chapter 5

Section 2.3.4
In earlier chapters, we explored linear models for regression and classification, and in the process we derived suitable forms for the error functions along with corresponding choices for the output-unit activation function. The same considerations for choosing an error function apply for multilayer neural networks, and so for convenience, we will summarize the key points here.

\subsection*{6.4.1 Regression}

We start by discussing regression problems, and for the moment we consider a single target variable $t$ that can take any real value. Following the discussion of regression in single-layer networks, we assume that $t$ has a Gaussian distribution with an $\mathrm{x}$-dependent mean, which is given by the output of the neural network, so that

$$
p(t \mid \mathbf{x}, \mathbf{w})=\mathcal{N}\left(t \mid y(\mathbf{x}, \mathbf{w}), \sigma^{2}\right)
$$

where $\sigma^{2}$ is the variance of the Gaussian noise. Of course this is a somewhat restrictive assumption, and in some applications we will need to extend this approach to allow for more general distributions. For the conditional distribution given by (6.23), it is sufficient to take the output-unit activation function to be the identity, because such a network can approximate any continuous function from $\mathbf{x}$ to $y$. Given a data set of $N$ i.i.d. observations $\mathbf{X}=\left\{\mathbf{x}_{1}, \ldots, \mathbf{x}_{N}\right\}$, along with corresponding target values $\mathbf{t}=\left\{t_{1}, \ldots, t_{N}\right\}$, we can construct the corresponding likelihood function:

$$
p\left(\mathbf{t} \mid \mathbf{X}, \mathbf{w}, \sigma^{2}\right)=\prod_{n=1}^{N} p\left(t_{n} \mid y\left(\mathbf{x}_{n}, \mathbf{w}\right), \sigma^{2}\right)
$$

Note that in the machine learning literature, it is usual to consider the minimization of an error function rather than the maximization of the likelihood, and so here we will follow this convention. Taking the negative logarithm of the likelihood function (6.24), we obtain the error function

$$
\frac{1}{2 \sigma^{2}} \sum_{n=1}^{N}\left\{y\left(\mathbf{x}_{n}, \mathbf{w}\right)-t_{n}\right\}^{2}+\frac{N}{2} \ln \sigma^{2}+\frac{N}{2} \ln (2 \pi)
$$

which can be used to learn the parameters $\mathbf{w}$ and $\sigma^{2}$. Consider first the determination of $\mathbf{w}$. Maximizing the likelihood function is equivalent to minimizing the sum-ofsquares error function given by

$$
E(\mathbf{w})=\frac{1}{2} \sum_{n=1}^{N}\left\{y\left(\mathbf{x}_{n}, \mathbf{w}\right)-t_{n}\right\}^{2}
$$

where we have discarded additive and multiplicative constants. The value of $\mathbf{w}$ found by minimizing $E(\mathbf{w})$ will be denoted $\mathbf{w}^{\star}$. Note that this will typically not correspond to the global maximum of the likelihood function because the nonlinearity of the network function $y\left(\mathbf{x}_{n}, \mathbf{w}\right)$ causes the error $E(\mathbf{w})$ to be non-convex, and so finding the global optimum is generally infeasible. Moreover, regularization

Chapter 9

\section*{Exercise 6.8} terms may be added to the error function and other modifications may be made to the training process, so that the resulting solution for the network parameters may differ significantly from the maximum likelihood solution.

Having found $\mathbf{w}^{\star}$, the value of $\sigma^{2}$ can be found by minimizing the error function $(6.25)$ to give

$$
\sigma^{2 \star}=\frac{1}{N} \sum_{n=1}^{N}\left\{y\left(\mathbf{x}_{n}, \mathbf{w}^{\star}\right)-t_{n}\right\}^{2}
$$

Note that this can be evaluated once the iterative optimization required to find $\mathbf{w}^{\star}$ is completed.

If we have multiple target variables, and we assume that they are independent, conditional on $\mathbf{x}$ and $\mathbf{w}$, with shared noise variance $\sigma^{2}$, then the conditional distribution of the target values is given by

$$
p(\mathbf{t} \mid \mathbf{x}, \mathbf{w})=\mathcal{N}\left(\mathbf{t} \mid \mathbf{y}(\mathbf{x}, \mathbf{w}), \sigma^{2} \mathbf{I}\right)
$$

Exercise 6.9

\section*{Exercise 6.10}

Section 5.4.6

Section 5.4.6
Following the same argument as for a single target variable, we see that maximizing the likelihood function with respect to the weights is equivalent to minimizing the sum-of-squares error function:

$$
E(\mathbf{w})=\frac{1}{2} \sum_{n=1}^{N}\left\|\mathbf{y}\left(\mathbf{x}_{n}, \mathbf{w}\right)-\mathbf{t}_{n}\right\|^{2}
$$

The noise variance is then given by

$$
\sigma^{2 \star}=\frac{1}{N K} \sum_{n=1}^{N}\left\|\mathbf{y}\left(\mathbf{x}_{n}, \mathbf{w}^{\star}\right)-\mathbf{t}_{n}\right\|^{2}
$$

where $K$ is the dimensionality of the target variable. The assumption of conditional independence of the target variables can be dropped at the expense of a slightly more complex optimization problem.

Recall that there is a natural pairing of the error function (given by the negative $\log$ likelihood) and the output-unit activation function. In regression, we can view the network as having an output activation function that is the identity, so that $y_{k}=a_{k}$. The corresponding sum-of-squares error function then has the property

$$
\frac{\partial E}{\partial a_{k}}=y_{k}-t_{k}
$$

\subsection*{6.4.2 Binary classification}

Now consider binary classification in which we have a single target variable $t$ such that $t=1$ denotes class $\mathcal{C}_{1}$ and $t=0$ denotes class $\mathcal{C}_{2}$. Following the discussion of canonical link functions, we consider a network having a single output whose activation function is a logistic sigmoid (6.13) so that $0 \leqslant y(\mathbf{x}, \mathbf{w}) \leqslant 1$. We can interpret $y(\mathbf{x}, \mathbf{w})$ as the conditional probability $p\left(\mathcal{C}_{1} \mid \mathbf{x}\right)$, with $p\left(\mathcal{C}_{2} \mid \mathbf{x}\right)$ given by $1-y(\mathbf{x}, \mathbf{w})$. The conditional distribution of targets given inputs is then a Bernoulli distribution of the form

$$
p(t \mid \mathbf{x}, \mathbf{w})=y(\mathbf{x}, \mathbf{w})^{t}\{1-y(\mathbf{x}, \mathbf{w})\}^{1-t}
$$

If we consider a training set of independent observations, then the error function, which is given by the negative log likelihood, is then a cross-entropy error of the form

$$
E(\mathbf{w})=-\sum_{n=1}^{N}\left\{t_{n} \ln y_{n}+\left(1-t_{n}\right) \ln \left(1-y_{n}\right)\right\}
$$

where $y_{n}$ denotes $y\left(\mathbf{x}_{n}, \mathbf{w}\right)$. Simard, Steinkraus, and Platt (2003) found that using the cross-entropy error function instead of the sum-of-squares for a classification problem leads to faster training as well as improved generalization.

Note that there is no analogue of the noise variance $\sigma^{2}$ in (6.32) because the target values are assumed to be correctly labelled. However, the model is easily extended to allow for labelling errors by introducing a probability $\epsilon$ that the target

Exercise 6.13

Exercise 6.14

Section 5.1.3

Section 5.4.4

Chapter 9

Exercise 6.15 value $t$ has been flipped to the wrong value (Opper and Winther, 2000). Here $\epsilon$ may be set in advance, or it may be treated as a hyperparameter whose value is inferred from the data.

If we have $K$ separate binary classifications to perform, then we can use a network having $K$ outputs each of which has a logistic-sigmoid activation function. Associated with each output is a binary class label $t_{k} \in\{0,1\}$, where $k=1, \ldots, K$. If we assume that the class labels are independent, given the input vector, then the conditional distribution of the targets is

$$
p(\mathbf{t} \mid \mathbf{x}, \mathbf{w})=\prod_{k=1}^{K} y_{k}(\mathbf{x}, \mathbf{w})^{t_{k}}\left[1-y_{k}(\mathbf{x}, \mathbf{w})\right]^{1-t_{k}}
$$

Taking the negative logarithm of the corresponding likelihood function then gives the following error function:

$$
E(\mathbf{w})=-\sum_{n=1}^{N} \sum_{k=1}^{K}\left\{t_{n k} \ln y_{n k}+\left(1-t_{n k}\right) \ln \left(1-y_{n k}\right)\right\}
$$

where $y_{n k}$ denotes $y_{k}\left(\mathbf{x}_{n}, \mathbf{w}\right)$. Again, the derivative of the error function with respect to the pre-activation for a particular output unit takes the form (6.31), just as in the regression case.

\subsection*{6.4.3 multiclass classification}

Finally, we consider the standard multiclass classification problem in which each input is assigned to one of $K$ mutually exclusive classes. The binary target variables $t_{k} \in\{0,1\}$ have a 1 -of- $K$ coding scheme indicating the class, and the network outputs are interpreted as $y_{k}(\mathbf{x}, \mathbf{w})=p\left(t_{k}=1 \mid \mathbf{x}\right)$, leading to the error function (5.80), which we reproduce here:

$$
E(\mathbf{w})=-\sum_{n=1}^{N} \sum_{k=1}^{K} t_{k n} \ln y_{k}\left(\mathbf{x}_{n}, \mathbf{w}\right)
$$

The output-unit activation function, which corresponds to the canonical link, is given by the softmax function:

$$
y_{k}(\mathbf{x}, \mathbf{w})=\frac{\exp \left(a_{k}(\mathbf{x}, \mathbf{w})\right)}{\sum_{j} \exp \left(a_{j}(\mathbf{x}, \mathbf{w})\right)}
$$

which satisfies $0 \leqslant y_{k} \leqslant 1$ and $\sum_{k} y_{k}=1$. Note that the $y_{k}(\mathbf{x}, \mathbf{w})$ are unchanged if a constant is added to all of the $a_{k}(\mathbf{x}, \mathbf{w})$, causing the error function to be constant for some directions in weight space. This degeneracy is removed if an appropriate regularization term is added to the error function. Once again, the derivative of the error function with respect to the pre-activation for a particular output unit takes the familiar form (6.31).

In summary, there is a natural choice of both output-unit activation function and matching error function according to the type of problem being solved. For regression, we use linear outputs and a sum-of-squares error, for multiple independent binary classifications, we use logistic sigmoid outputs and a cross-entropy error function, and for multi-class classification, we use softmax outputs with the corresponding multi-class cross-entropy error function. For classification problems involving two classes, we can use a single logistic sigmoid output, or alternatively, we can use a network with two outputs having a softmax output activation function.

This procedure is quite general, and by considering other forms of conditional distribution, we can derive the associated error functions as the corresponding negative log likelihood. We will see an example of this in the next section when we consider multimodal network outputs.

\title{
6.5. Mixture Density Networks
}

So far in this chapter we have discussed neural networks whose outputs represent simple probability distributions comprising either a Gaussian for continuous variables or a binary distribution for discrete variables. We close the chapter by showing how a neural network can represent more general conditional probabilities by treating the outputs of the network as the parameters of a more complex distribution, in this case a Gaussian mixture model. This is known as a mixture density network, and we will see how to define the associated error function and the corresponding output-unit activation functions.

\subsection*{6.5.1 Robot kinematics example}

The goal of supervised learning is to model a conditional distribution $p(\mathbf{t} \mid \mathbf{x})$, which for many simple regression problems is chosen to be Gaussian. However, practical machine learning problems can often have significantly non-Gaussian distributions. These can arise, for example, with inverse problems in which the distribution can be multimodal, in which case the Gaussian assumption can lead to very poor predictions.

As a simple illustration of an inverse problem, consider the kinematics of a robot arm, as illustrated in Figure 6.16. The forward problem involves finding the end effector position given the joint angles and has a unique solution. However, in practice we wish to move the end effector of the robot to a specific position, and to do this we must set appropriate joint angles. We therefore need to solve the inverse problem, which has two solutions, as seen in Figure 6.16.

Forward problems often correspond to causality in a physical system and generally have a unique solution. For instance, a specific pattern of symptoms in the human body may be caused by the presence of a particular disease. In machine learning, however, we typically have to solve an inverse problem, such as trying to predict the presence of a disease given a set of symptoms. If the forward problem involves a many-to-one mapping, then the inverse problem will have multiple solutions. For instance, several different diseases may result in the same symptoms.

Figure 6.16 (a) A two-link robot arm, in which the Cartesian coordinates $\left(x_{1}, x_{2}\right)$ of the end effector are determined uniquely by the two joint angles $\theta_{1}$ and $\theta_{2}$ and the (fixed) lengths $L_{1}$ and $L_{2}$ of the arms. This is known as the forward kinematics of the arm. (b) In practice, we have to find the joint angles that will give rise to a desired end effector position. This inverse kinematics has two solutions corresponding to 'el-

![](https://cdn.mathpix.com/cropped/2024_05_26_cf46115da84aa2e9c64eg-1.jpg?height=354&width=357&top_left_y=219&top_left_x=679

ChatGPT figure/image summary: The image is a schematic representation of a two-link robot arm as used in the explanation of forward kinematics. The robot arm is composed of two segments (links) labeled L1 and L2, which can pivot at their joints. The joint angles that determine the position of the end effector (the tip of the arm) are denoted by theta1 (θ1) and theta2 (θ2), corresponding to the first and second joints respectively. The Cartesian coordinates of the end effector are labeled as (x1, x2), represented in the image by a blue dot. This illustrates the unique relationship between the joint angles and the end effector's position in the case of forward kinematics problems.)

(a)

![](https://cdn.mathpix.com/cropped/2024_05_26_cf46115da84aa2e9c64eg-1.jpg?height=364&width=364&top_left_y=219&top_left_x=1127

ChatGPT figure/image summary: The image presented is a schematic diagram of a two-link robot arm demonstrating the inverse kinematics problem referenced in the provided paper. It depicts two possible configurations for the robot arm, which can result in the same end effector position (denoted as a point with Cartesian coordinates (x1, x2)). 

The two configurations are differentiated by the position of the 'elbow' of the robot arm:

1. "Elbow up": The elbow joint of the robot arm is oriented above the line connecting the base to the end effector.
2. "Elbow down": The elbow joint is oriented below that line.

The diagram is labeled to clarify the two distinct states of the elbow joint. The upper configuration shows the robot arm with a straightened look and the elbow pointing upwards, while the lower dotted configuration shows the arm folded with the elbow pointing downwards. Both configurations are connected to a base represented by the gray horizontal line at the bottom of the image.)

(b) bow up' and 'elbow down'.

In the robotics example, the kinematics is defined by geometrical equations, and the multimodality is readily apparent. However, in many machine learning problems the presence of multimodality, particularly in problems involving spaces of high dimensionality, can be less obvious. For tutorial purposes, however, we will consider a simple toy problem for which we can easily visualize the multimodality. The data for this problem is generated by sampling a variable $x$ uniformly over the interval $(0,1)$, to give a set of values $\left\{x_{n}\right\}$, and the corresponding target values $t_{n}$ are obtained by computing the function $x_{n}+0.3 \sin \left(2 \pi x_{n}\right)$ and then adding uniform noise over the interval $(-0.1,0.1)$. The inverse problem is then obtained by keeping the same data points but exchanging the roles of $x$ and $t$. Figure 6.17 shows the data sets for the forward and inverse problems, along with the results of fitting two-layer neural networks having six hidden units and a single linear output unit by minimizing a sum-of-squares error function. Least squares corresponds to maximum likelihood under a Gaussian assumption. We see that this leads to a good model for the forward problem but a very poor model for the highly non-Gaussian inverse problem.

\title{
6.5.2 Conditional mixture distributions
}

We therefore seek a general framework for modelling conditional probability distributions. This can be achieved by using a mixture model for $p(\mathbf{t} \mid \mathbf{x})$ in which

Figure 6.17 On the left is the data set for a simple forward problem in which the red curve shows the result of fitting a two-layer neural network by minimizing the sum-of-squares error function. The corresponding inverse problem, shown on the right, is obtained by exchanging the roles of $x$ and $t$. Here the same network, again trained by minimizing the sumof-squares error function, gives a poor fit to the data due to the multimodality of the data set.
![](https://cdn.mathpix.com/cropped/2024_05_26_cf46115da84aa2e9c64eg-1.jpg?height=470&width=984&top_left_y=1616&top_left_x=640

ChatGPT figure/image summary: The image displays two scatter plots side by side. Both scatter plots depict a range of data points distributed along the x-axis from 0 to 1 and along the y-axis from 0 to 1. 

The plot on the left represents a simple forward problem where we can see green circular data points spread around a red curve that seems to represent a fitted model. The data points are scattered but follow roughly the shape of the curve, with some variance around it. 

The plot on the right is for a corresponding inverse problem, where we see a similar scatter of green circular data points. However, in this plot, the data points form a distinctly multimodal distribution with two separate clusters of points, indicating two different regimes or solutions. The red curve, representing the fitted model, attempts to capture this multimodal nature but does not fit the data points as closely as in the left plot, indicating the complexity and the poor fit of the model to this non-Gaussian dataset. 

The scatter plots are visualizations of datasets, with the red curve likely representing the output of a machine learning model trained to fit the data. The plots are used to demonstrate the difference in modeling performance between a straightforward regression problem (forward problem) and a more complex, multimodal problem (inverse problem).)

Figure 6.1 Plot of the Iris data in which red, green, and blue points denote three species of iris flower and the axes represent measurements of the length and width of the sepal, respectively. Our goal is to classify a new test point such as the one denoted by $x$.

![](https://cdn.mathpix.com/cropped/2024_05_26_b8f14dbc6f67539ba08cg-1.jpg?height=684&width=706&top_left_y=222&top_left_x=956

ChatGPT figure/image summary: The image you provided displays a scatter plot with three distinct clusters of data points in different colors: red, green, and blue. These clusters represent measurements of the length and width of the sepal for three species of iris flowers. There is also a cross (denoted by "x") on the plot which appears to be a new test data point. The axes are labeled "sepal length" on the horizontal axis and "sepal width" on the vertical axis. The goal is to classify this new test point by determining which species it most likely belongs to based on its proximity to the clusters of data points corresponding to the three different species.)

would take the form

$$
y(\mathbf{x}, \mathbf{w})=w_{0}+\sum_{i=1}^{D} w_{i} x_{i}+\sum_{i=1}^{D} \sum_{j=1}^{D} w_{i j} x_{i} x_{j}+\sum_{i=1}^{D} \sum_{j=1}^{D} \sum_{k=1}^{D} w_{i j k} x_{i} x_{j} x_{k}
$$

As $D$ increases, the growth in the number of independent coefficients is $\mathcal{O}\left(D^{3}\right)$, whereas for a polynomial of order $M$, the growth in the number of coefficients is $\mathcal{O}\left(D^{M}\right)$ (Bishop, 2006). We see that in spaces of higher dimensionality, polynomials can rapidly become unwieldy and of little practical utility.

The severe difficulties that can arise in spaces of many dimensions is sometimes called the curse of dimensionality (Bellman, 1961). It is not limited to polynomial regression but is in fact quite general. Consider the use of linear models for solving classification problems. Figure 6.1 shows a plot of data from the Iris data set comprising 50 observations taken from each of three species of iris flowers. Each observation has four variables representing measurements of the sepal length, sepal width, petal length, and petal width. For this illustration, we consider only the sepal length and sepal width variables. Given these 150 observations as training data, our goal is to classify a new test point, such as the one denoted by the cross in Figure 6.1, by assigning it to one of the three species. We observe that the cross is close to several red points, and so we might suppose that it belongs to the red class. However, there are also some green points nearby, so we might think that it could instead belong to the green class. It seems less likely that it belongs to the blue class. The intuition here is that the identity of the cross should be determined more strongly by nearby points from the training set and less strongly by more distant points, and this intuition turns out to be reasonable.

One very simple way of converting this intuition into a learning algorithm would be to divide the input space into regular cells, as indicated in Figure 6.2. When we are given a test point and we wish to predict its class, we first decide which cell it

Figure 6.18 The mixture density network can represent general conditional probability densities $p(\mathbf{t} \mid \mathbf{x})$ by considering a parametric mixture model for the distribution of $t$ whose parameters are determined by the outputs of a neural network that takes $\mathrm{x}$ as its input vector.

![](https://cdn.mathpix.com/cropped/2024_05_26_fdc10e06182b216dcb8fg-1.jpg?height=442&width=952&top_left_y=221&top_left_x=696

ChatGPT figure/image summary: The shared image appears to be an illustration of a mixture density network, which is a type of neural network designed for predicting a probability distribution for an output variable \( t \) as a function of an input variable \( x \). The left side of the image shows a schematic representation of the neural network, and the right side depicts the resulting conditional probability density function \( p(t|x) \).

In the network diagram on the left, the blue circles represent neurons or nodes. There is an input layer at the bottom (\( x_1 \) to \( x_D \)) where \( D \) represents the dimensionality of the input vector. There is also an output layer at the top with \( θ_1 \) to \( θ_K \) nodes, which likely correspond to the outputs of the network that determine the parameters of the mixture model components and the mixing coefficients (although not explicitly labeled in the image).

On the right side, the graph is a plot of the conditional probability density function \( p(t|x) \) where \( t \) is on the horizontal axis. The blue curves likely represent individual Gaussian components of the mixture, each with its own mean and variance as determined by the neural network's outputs. The red curve would then represent the overall mixture distribution, which is the sum of all the individual components weighted by their mixing coefficients (\( \pi_k(x) \)).

This kind of network is powerful because it can represent a wide range of complex probability distributions for the output variable \( t \), making it applicable to problems in regression and classification where the outputs are uncertain or the uncertainty itself is an important aspect to model. The text provides additional context for understanding the operation and purpose of mixture density networks.)

both the mixing coefficients as well as the component densities are flexible functions of the input vector $\mathbf{x}$, giving rise to a mixture density network. For any given value of $\mathbf{x}$, the mixture model provides a general formalism for modelling an arbitrary conditional density function $p(\mathbf{t} \mid \mathbf{x})$. Provided we consider a sufficiently flexible network, we then have a framework for approximating arbitrary conditional distributions.

Here we will develop the model explicitly for Gaussian components, so that

$$
p(\mathbf{t} \mid \mathbf{x})=\sum_{k=1}^{K} \pi_{k}(\mathbf{x}) \mathcal{N}\left(\mathbf{t} \mid \boldsymbol{\mu}_{k}(\mathbf{x}), \sigma_{k}^{2}(\mathbf{x})\right)
$$

This is an example of a heteroscedastic model in which the noise variance on the data is a function of the input vector $\mathbf{x}$. Instead of Gaussians, we can use other distributions for the components, such as Bernoulli distributions if the target variables are binary rather than continuous. We have also specialized to the case of isotropic covariances for the components, although the mixture density network can readily be extended to allow for general covariance matrices by representing the covariances using a Cholesky factorization (Williams, 1996). Even with isotropic components, the conditional distribution $p(\mathbf{t} \mid \mathbf{x})$ does not assume factorization with respect to the components of $t$ (in contrast to the standard sum-of-squares regression model) as a consequence of the mixture distribution.

We now take the various parameters of the mixture model, namely the mixing coefficients $\pi_{k}(\mathbf{x})$, the means $\boldsymbol{\mu}_{k}(\mathbf{x})$, and the variances $\sigma_{k}^{2}(\mathbf{x})$, to be governed by the outputs of a neural network that takes $\mathrm{x}$ as its input. The structure of this mixture density network is illustrated in Figure 6.18. The mixture density network is closely related to the mixture-of-experts model (Jacobs et al., 1991). The principal difference is that a mixture of experts has independent parameters for each component model in the mixture, whereas in a mixture density network, the same function is used to predict the parameters of all the component densities as well as the mixing coefficients, and so the nonlinear hidden units are shared amongst the input-dependent functions.

The neural network in Figure 6.18 can, for example, be a two-layer network having sigmoidal $(\tanh )$ hidden units. If there are $K$ components in the mixture model (6.38), and if $\mathbf{t}$ has $L$ components, then the network will have $K$ output-

unit pre-activations denoted by $a_{k}^{\pi}$ that determine the mixing coefficients $\pi_{k}(\mathbf{x}), K$ outputs denoted by $a_{k}^{\sigma}$ that determine the Gaussian standard deviations $\sigma_{k}(\mathbf{x})$, and $K \times L$ outputs denoted by $a_{k j}^{\mu}$ that determine the components $\mu_{k j}(\mathbf{x})$ of the Gaussian means $\boldsymbol{\mu}_{k}(\mathbf{x})$. The total number of network outputs is given by $(L+2) K$, unlike the usual $L$ outputs for a network that simply predicts the conditional means of the target variables.

The mixing coefficients must satisfy the constraints

$$
\sum_{k=1}^{K} \pi_{k}(\mathbf{x})=1, \quad 0 \leqslant \pi_{k}(\mathbf{x}) \leqslant 1
$$

which can be achieved using a set of softmax outputs:

$$
\pi_{k}(\mathbf{x})=\frac{\exp \left(a_{k}^{\pi}\right)}{\sum_{l=1}^{K} \exp \left(a_{l}^{\pi}\right)}
$$

Similarly, the variances must satisfy $\sigma_{k}^{2}(\mathbf{x}) \geqslant 0$ and so can be represented in terms of the exponentials of the corresponding network pre-activations using

$$
\sigma_{k}(\mathbf{x})=\exp \left(a_{k}^{\sigma}\right)
$$

Finally, because the means $\boldsymbol{\mu}_{k}(\mathrm{x})$ have real components, they can be represented directly by the network outputs:

$$
\mu_{k j}(\mathbf{x})=a_{k j}^{\mu}
$$

in which the output-unit activation functions are given by the identity $f(a)=a$.

The learnable parameters of the mixture density network comprise the vector $\mathbf{w}$ of weights and biases in the neural network, which can be set by maximum likelihood or equivalently by minimizing an error function defined to be the negative logarithm of the likelihood. For independent data, this error function takes the form

$$
E(\mathbf{w})=-\sum_{n=1}^{N} \ln \left\{\sum_{k=1}^{K} \pi_{k}\left(\mathbf{x}_{n}, \mathbf{w}\right) \mathcal{N}\left(\mathbf{t}_{n} \mid \boldsymbol{\mu}_{k}\left(\mathbf{x}_{n}, \mathbf{w}\right), \sigma_{k}^{2}\left(\mathbf{x}_{n}, \mathbf{w}\right)\right)\right\}
$$

where we have made the dependencies on $\mathbf{w}$ explicit.

\title{
6.5.3 Gradient optimization
}

To minimize the error function, we need to calculate the derivatives of the error $E(\mathbf{w})$ with respect to the components of $\mathbf{w}$. We will see later how to compute these derivatives automatically. It is instructive, however, to derive suitable expressions for the derivatives of the error with respect to the output-unit pre-activations explicitly as this highlights the probabilistic interpretation of these quantities. Because the error function (6.43) is composed of a sum of terms, one for each training data point, we can consider the derivatives for a particular input vector $\mathbf{x}_{n}$ with associated target vector $\mathbf{t}_{n}$. The derivatives of the total error $E$ are obtained by summing over all

Chapter 7

\section*{Exercise 6.17}

Exercise 6.18

Exercise 6.19

Exercise 6.20 data points, or the individual gradients for each data point can be used directly in gradient-based optimization algorithms.

It is convenient to introduce the following variables:

$$
\gamma_{n k}=\gamma_{k}\left(\mathbf{t}_{n} \mid \mathbf{x}_{n}\right)=\frac{\pi_{k} \mathcal{N}_{n k}}{\sum_{l=1}^{K} \pi_{l} \mathcal{N}_{n l}}
$$

where $\mathcal{N}_{n k}$ denotes $\mathcal{N}\left(\mathbf{t}_{n} \mid \boldsymbol{\mu}_{k}\left(\mathbf{x}_{n}\right), \sigma_{k}^{2}\left(\mathbf{x}_{n}\right)\right)$. These quantities have a natural interpretation as posterior probabilities for the components of the mixture in which the mixing coefficients $\pi_{k}(\mathbf{x})$ are viewed as $\mathbf{x}$-dependent prior probabilities.

The derivatives of the error function with respect to the network output preactivations governing the mixing coefficients are given by

$$
\frac{\partial E_{n}}{\partial a_{k}^{\pi}}=\pi_{k}-\gamma_{n k}
$$

Similarly, the derivatives with respect to the output pre-activations controlling the component means are given by

$$
\frac{\partial E_{n}}{\partial a_{k l}^{\mu}}=\gamma_{n k}\left\{\frac{\mu_{k l}-t_{n l}}{\sigma_{k}^{2}}\right\}
$$

Finally, the derivatives with respect to the output pre-activations controlling the component variances are given by

$$
\frac{\partial E_{n}}{\partial a_{k}^{\sigma}}=\gamma_{n k}\left\{L-\frac{\left\|\mathbf{t}_{n}-\boldsymbol{\mu}_{k}\right\|^{2}}{\sigma_{k}^{2}}\right\}
$$

\subsection*{6.5.4 Predictive distribution}

We illustrate the use of a mixture density network by returning to the toy example of an inverse problem shown in Figure 6.17. Plots of the mixing coefficients $\pi_{k}(x)$, the means $\mu_{k}(x)$, and the conditional density contours corresponding to $p(t \mid x)$, are shown in Figure 6.19. The outputs of the neural network, and hence the parameters in the mixture model, are necessarily continuous single-valued functions of the input variables. However, we see from Figure 6.19(c) that the model is able to produce a conditional density that is unimodal for some values of $x$ and trimodal for other values by modulating the amplitudes of the mixing components $\pi_{k}(\mathbf{x})$.

Once a mixture density network has been trained, it can predict the conditional density function of the target data for any given value of the input vector. This conditional density represents a complete description of the generator of the data, so far as the problem of predicting the value of the output vector is concerned. From this density function, we can calculate more specific quantities that may be of interest in different applications. One of the simplest of these is the mean, corresponding to the conditional average of the target data, and is given by

$$
\mathbb{E}[\mathbf{t} \mid \mathbf{x}]=\int \mathbf{t} p(\mathbf{t} \mid \mathbf{x}) \mathrm{d} \mathbf{t}=\sum_{k=1}^{K} \pi_{k}(\mathbf{x}) \boldsymbol{\mu}_{k}(\mathbf{x})
$$

Figure 6.19 (a) Plot of the mixing coefficients $\pi_{k}(x)$ as a function of $x$ for the three mixture components in a mixture density network trained on the data shown in Figure 6.17. The model has three Gaussian components and uses a two-layer neural network with five tanh sigmoidal units in the hidden layer and nine outputs (corresponding to the three means and three variances of the Gaussian components and the three mixing coefficients). At both small and large values of $x$, where the conditional probability density of the target data is unimodal, only one of the Gaussian components has a high value for its prior probability, whereas at intermediate values of $x$, where the conditional density is trimodal, the three mixing coefficients have comparable values. (b) Plots of the means $\mu_{k}(x)$ using the same colour coding as for the mixing coefficients. (c) Plot of the contours of the corresponding conditional probability density of the target data for the same mixture density network. (d) Plot of the approximate conditional mode, shown by the red points, of the conditional density.

![](https://cdn.mathpix.com/cropped/2024_05_26_6a9b15d90f257837d782g-1.jpg?height=1033&width=945&top_left_y=219&top_left_x=661

ChatGPT figure/image summary: The image contains four subfigures labeled (a), (b), (c), and (d), each showcasing different plots related to a mixture density network analysis as described in the provided text.

Subfigure (a) shows a plot of the mixing coefficients $\pi_{k}(x)$ for three mixture components across a range of $x$ values. There are three lines, likely representing the mixing coefficients for three different Gaussian components of the mixture model. The y-axis presumably represents the value of the mixing coefficients ranging from 0 to 1, and the x-axis represents the input variable $x$ over which the coefficients are evaluated.

Subfigure (b) depicts plots of the means $\mu_{k}(x)$ of the Gaussian components as functions of $x$. The lines correspond to the means of each component and are color-coded to match the mixing coefficients in subfigure (a).

Subfigure (c) shows the contour plot of the conditional probability density of the target data for the same mixture density network. The contours may represent areas of equal likelihood, with different colors indicating the levels of density, from high to low as we move outward from the center of the peaks.

Subfigure (d) appears to be a scatter plot with empirical data points overlaid with an approximate conditional mode of the conditional density illustrated by a solid red line. The green dots represent individual observations, while the red line indicates the means of the most probable Gaussian components for different values of $x$.

These plots visualize the different aspects of a fitted mixture density network, showcasing how the network outputs (mixing coefficients, means, and conditional density) vary with the input variable $x$ and how they represent the underlying structure of the data.)

![](https://cdn.mathpix.com/cropped/2024_05_26_6a9b15d90f257837d782g-1.jpg?height=425&width=415&top_left_y=234&top_left_x=679

ChatGPT figure/image summary: The image shows a graph with three curves, each plotted against the same pair of axes. The x-axis is not labeled, but the range appears to go from 0 to 1, and the y-axis runs from 0 to what could be assumed to be 1, based on the scale of the graph. The three curves each have distinct colors - one is blue, one is green, and one is red. Their exact mathematical descriptions are not provided, but they seem to represent functions of x, with each curve peaking at different points along the x-axis. The shape of the curves suggests these could be the plots of mixing coefficients πk(x) from the context given, with each curve representing a different mixture component from a mixture density network. This particular visualization supports the narrative given in the contextual information provided, where the curves likely correspond to Figure 6.19 (a), which describes the variation of these coefficients as a function of the input variable x.)

(a)

![](https://cdn.mathpix.com/cropped/2024_05_26_6a9b15d90f257837d782g-1.jpg?height=432&width=418&top_left_y=766&top_left_x=675

ChatGPT figure/image summary: This image shows a plot of the contours of the corresponding conditional probability density of the target data for a mixture density network. The colors likely represent different levels of probability density, with denser areas depicted in warmer colors (like red or yellow), and less dense areas in cooler colors (like blue). The axes are scaled from 0 to 1, suggesting a normalized range for the data. This plot corresponds to part (c) of Figure 6.19 from the context provided, illustrating how the conditional density can be trimodal for some values of the input variable x, as indicated by the multiple peaks in the contour plot.)

(c)

![](https://cdn.mathpix.com/cropped/2024_05_26_6a9b15d90f257837d782g-1.jpg?height=427&width=418&top_left_y=231&top_left_x=1183

ChatGPT figure/image summary: The image is a plot of three curves within a two-dimensional coordinate system. It is a graphical representation with the x-axis ranging from approximately zero to one and the y-axis also ranging from zero to one.

The plot features three curves, each depicted in a different color:

- The red curve, which starts high near the y-axis and decreases as x increases, leveling off as it approaches x=1.
- The green curve shows a peak in the middle, starting and ending at lower values on the y-axis.
- The blue curve starts at zero near the y-axis and increases as x approaches one.

Given the context from the paper and mathematical notations, these are likely the plots of mixing coefficients (πk(x)) as a function of x for three mixture components within a mixture density network. Each mixture component curve represents the strength or weight of that component at each value of x, which are used in a machine learning model to predict complex probability distributions over the targets conditioned on the inputs. 

The different amplitudes of these plots indicate how different mixture components contribute to the overall mixture model at different input values (x).)

(b)

![](https://cdn.mathpix.com/cropped/2024_05_26_6a9b15d90f257837d782g-1.jpg?height=432&width=418&top_left_y=761&top_left_x=1183

ChatGPT figure/image summary: The image provided tells us that it is Figure 6.19(d) from the paper, which depicts a plot related to a mixture density network. This plot appears to show the approximate conditional mode of the conditional density. The red points likely represent the mean of the most probable component (with the largest mixing coefficient) at each value of \( \mathbf{x} \). The green circles are probably the data points from the toy example mentioned in the text.

Based on the contextual information, we can say that this plot serves to visualize how a trained mixture density network can predict and represent complex conditional density functions that are multimodal, as opposed to traditional networks which might only predict conditional means. The plot is thus a graphical representation of the neural network's output in response to varying inputs.)

(d)

where we have used (6.38). Because a standard network trained by least squares approximates the conditional mean, we see that a mixture density network can reproduce the conventional least-squares result as a special case. Of course, as we have already noted, for a multimodal distribution the conditional mean is of limited value.

We can similarly evaluate the variance of the density function about the conditional average, to give

$$
\begin{aligned}
s^{2}(\mathbf{x}) & =\mathbb{E}\left[\|\mathbf{t}-\mathbb{E}[\mathbf{t} \mid \mathbf{x}]\|^{2} \mid \mathbf{x}\right] \\
& =\sum_{k=1}^{K} \pi_{k}(\mathbf{x})\left\{\sigma_{k}^{2}(\mathbf{x})+\left\|\boldsymbol{\mu}_{k}(\mathbf{x})-\sum_{l=1}^{K} \pi_{l}(\mathbf{x}) \boldsymbol{\mu}_{l}(\mathbf{x})\right\|^{2}\right\}
\end{aligned}
$$

where we have used (6.38) and (6.48). This is more general than the corresponding least-squares result because the variance is a function of $\mathbf{x}$.

We have seen that for multimodal distributions, the conditional mean can give a poor representation of the data. For instance, in controlling the simple robot arm shown in Figure 6.16, we need to pick one of the two possible joint angle settings

to achieve the desired end-effector location, but the average of the two solutions is not itself a solution. In such cases, the conditional mode may be of more value. Because the conditional mode for the mixture density network does not have a simple analytical solution, a numerical iteration is required. A simple alternative is to take the mean of the most probable component (i.e., the one with the largest mixing coefficient) at each value of $\mathbf{x}$. This is shown for the toy data set in Figure 6.19(d).

\title{
Exercises
}

6.1 $(\star \star \star)$ Use the result (2.126) to derive an expression for the surface area $S_{D}$ and the volume $V_{D}$ of a hypersphere of unit radius in $D$ dimensions. To do this, consider the following result, which is obtained by transforming from Cartesian to polar coordinates:

$$
\prod_{i=1}^{D} \int_{-\infty}^{\infty} e^{-x_{i}^{2}} \mathrm{~d} x_{i}=S_{D} \int_{0}^{\infty} e^{-r^{2}} r^{D-1} \mathrm{~d} r
$$

Using the gamma function, defined by

$$
\Gamma(x)=\int_{0}^{\infty} t^{x-1} e^{-t} \mathrm{~d} t
$$

together with (2.126), evaluate both sides of this equation, and hence show that

$$
S_{D}=\frac{2 \pi^{D / 2}}{\Gamma(D / 2)}
$$

Next, by integrating with respect to the radius from 0 to 1 , show that the volume of the unit hypersphere in $D$ dimensions is given by

$$
V_{D}=\frac{S_{D}}{D}
$$

Finally, use the results $\Gamma(1)=1$ and $\Gamma(3 / 2)=\sqrt{\pi} / 2$ to show that (6.53) and (6.54) reduce to the usual expressions for $D=2$ and $D=3$.

6.2 ( $\star \star \star)$ Consider a hypersphere of radius $a$ in $D$ dimensions together with the concentric hypercube of side $2 a$, so that the hypersphere touches the hypercube at the centres of each of its sides. By using the results of Exercise 6.1, show that the ratio of the volume of the hypersphere to the volume of the cube is given by

$$
\frac{\text { volume of hypersphere }}{\text { volume of cube }}=\frac{\pi^{D / 2}}{D 2^{D-1} \Gamma(D / 2)} \text {. }
$$

Now make use of Stirling's formula in the form

$$
\Gamma(x+1) \simeq(2 \pi)^{1 / 2} e^{-x} x^{x+1 / 2}
$$

which is valid for $x \gg 1$, to show that, as $D \rightarrow \infty$, the ratio (6.55) goes to zero. Show also that the distance from the centre of the hypercube to one of the corners

Figure 6.2 Illustration of a simple approach for solving classification problems in which the input space is divided into cells and any new test point is assigned to the class that has the most representatives in the same cell as the test point. As we shall see shortly, this simplistic approach has some severe shortcomings.

![](https://cdn.mathpix.com/cropped/2024_05_26_628bb04fbcc19ed959eag-1.jpg?height=694&width=706&top_left_y=215&top_left_x=956

ChatGPT figure/image summary: The image shows a scatter plot with two axes: sepal width and sepal length. The plot is divided into a grid with different colored regions, representing different classifications based on the majority class within each cell. There are three distinct groups of data points, each represented by a different color: red, green, and blue. An 'X' marks an uncertain location where a new data point could be classified based on the majority class of the training data points within the cell it falls into. This type of visualization can be used to demonstrate a simple, naive approach to classification, where the input space is partitioned into a grid and test points are assigned to the class with the most representatives in the corresponding cell.)

belongs to, and then we find all the training data points that fall in the same cell. The identity of the test point is predicted to be the same as the class having the largest number of training points in the same cell as the test point (with ties being broken at random). We can view this as a basis function model in which there is a basis function $\phi_{i}(\mathrm{x})$ for each grid cell, which simply returns zero if $\mathrm{x}$ lies outside the grid cell, and otherwise returns the majority class of the training data points that fall inside the cell. The output of the model is then given by the sum of the outputs of all the basis functions.

There are numerous problems with this naive approach, but one of the most severe becomes apparent when we consider its extension to problems having larger numbers of input variables, corresponding to input spaces of higher dimensionality. The origin of the problem is illustrated in Figure 6.3, which shows that, if we divide a region of a space into regular cells, then the number of such cells grows exponentially with the dimensionality of the space. The challenge with an exponentially large number of cells is that we would need an exponentially large quantity of training

Figure 6.3 Illustration of the curse of dimensionality, showing how the number of regions of a regular grid grows exponentially with the dimensionality $D$ of the space. For clarity, only a subset of the cubical regions are shown for $D=3$.

![](https://cdn.mathpix.com/cropped/2024_05_26_628bb04fbcc19ed959eag-1.jpg?height=81&width=262&top_left_y=2006&top_left_x=638

ChatGPT figure/image summary: The image you provided is a simple one-dimensional (1D) representation of a space divided into regular segments, or cells, with red marks indicating the boundaries between the cells. This is denoted by "$D=1$" indicating that it illustrates a single dimension, labeled with $x_1$ as the axis. These kinds of illustrations are often used in the context of discussing concepts such as partitioning space for various computational algorithms, and more specifically, as mentioned in the text you provided, to show how the number of regions (cells) grows as the dimensionality $D$ increases. This image is used to depict the simplest case, where the space is one-dimensional and therefore the number of segments corresponds directly to the number of cells or partitions along the axis.)

$D=1$

![](https://cdn.mathpix.com/cropped/2024_05_26_628bb04fbcc19ed959eag-1.jpg?height=293&width=313&top_left_y=1773&top_left_x=918

ChatGPT figure/image summary: The image depicts a two-dimensional grid representing a conceptual space where the input space is divided into regular cells. There are two axes, \( x_1 \) and \( x_2 \), suggesting that this is a representation of a plane with two variables defining the coordinates within this space. The grid is made up of nine equal-sized squares, created by drawing horizontal and vertical lines that intersect. This division into cells might be used, for example, in a machine learning context for classifying data points based on which cell they fall into. This particular grid could be illustrating the idea of partitioning a space for a classification task, where each region (or cell) could be associated with a certain class based on the majority of training points that fall within that region.)

$D=2$

![](https://cdn.mathpix.com/cropped/2024_05_26_628bb04fbcc19ed959eag-1.jpg?height=412&width=394&top_left_y=1655&top_left_x=1244

ChatGPT figure/image summary: The image shows a three-dimensional representation of a regular grid, which divides the space into smaller cubic regions. The red outlines represent the cubes, and within these, the dotted lines represent the grid structure that creates the smaller regions or cells. The axes \( x_1 \), \( x_2 \), and \( x_3 \) are labeled, indicating the three dimensions of the space. This illustration serves as a visual aid for understanding the concept of dividing a region of space into cells, which is a topic of discussion related to high-dimensional spaces in the context of the provided text. This visual relates to the "curse of dimensionality," showing that as the dimensionality \( D \) increases, the number of cells grows exponentially, leading to the challenges in data classification and model complexity that were discussed.)

$D=3$

Figure 6.4 Plot of the fraction of the volume of a hypersphere of radius $r=1$ lying in the range $r=1-\epsilon$ to $r=1$ for various values of the dimensionality $D$.

![](https://cdn.mathpix.com/cropped/2024_05_26_5c32d245d93af9e68d2cg-1.jpg?height=696&width=723&top_left_y=214&top_left_x=935

ChatGPT figure/image summary: The image provided is a plot illustrating the volume fraction of a hypersphere of radius \( r=1 \) that lies in the range of \( r=1-\epsilon \) to \( r=1 \) for various values of the dimensionality \( D \). The plot shows curves for different dimensionalities (D = 1, D = 2, D = 5, D = 20) as functions of \( \epsilon \). Each curve represents the fraction of the hypersphere's volume near the surface as the dimensionality increases. The x-axis represents \( \epsilon \), which ranges from 0 to 1, whereas the y-axis represents the volume fraction, ranging from 0 to 1. As can be seen in the plot, for higher dimensions (like when D = 20), even a small \( \epsilon \) results in a large volume fraction near the hypersphere's surface, illustrating the concept known as the "curse of dimensionality".)

Section 6.1.4

Exercise 6.1

data to ensure that the cells are not empty. We have already seen in Figure 6.2 that some cells contain no training points. Hence, a test point in such cells cannot be classified. Clearly, we have no hope of applying such a technique in a space of more than a few variables. The difficulties with both the polynomial regression example and the Iris data classification example arise because the basis functions were chosen independently of the problem being solved. We will need to be more sophisticated in our choice of basis functions if we are to circumvent the curse of dimensionality.

\title{
6.1.2 High-dimensional spaces
}

First, however, we will look more closely at the properties of spaces with higher dimensionality where our geometrical intuitions, formed through a life spent in a space of three dimensions, can fail badly. As a simple example, consider a hypersphere of radius $r=1$ in a space of $D$ dimensions, and ask what is the fraction of the volume of the hypersphere that lies between radius $r=1-\epsilon$ and $r=1$. We can evaluate this fraction by noting that the volume $V_{D}(r)$ of a hypersphere of radius $r$ in $D$ dimensions must scale as $r^{D}$, and so we write

$$
V_{D}(r)=K_{D} r^{D}
$$

where the constant $K_{D}$ depends only on $D$. Thus, the required fraction is given by

$$
\frac{V_{D}(1)-V_{D}(1-\epsilon)}{V_{D}(1)}=1-(1-\epsilon)^{D}
$$

which is plotted as a function of $\epsilon$ for various values of $D$ in Figure 6.4. We see that, for large $D$, this fraction tends to 1 even for small values of $\epsilon$. Thus, we arrive at the remarkable result that, in spaces of high dimensionality, most of the volume of a hypersphere is concentrated in a thin shell near the surface!

Figure 6.5 Plot of the probability density with respect to radius $r$ of a Gaussian distribution for various values of the dimensionality $D$. In a highdimensional space, most of the probability mass of a Gaussian is located within a thin shell at a specific radius.

![](https://cdn.mathpix.com/cropped/2024_05_26_bc33d980debf73d6abd0g-1.jpg?height=508&width=706&top_left_y=220&top_left_x=951

ChatGPT figure/image summary: The image appears to be a graph showing the probability density with respect to radius \( r \) of a Gaussian distribution for various values of the dimensionality \( D \). The graph plots the function \( p(r) \) along the y-axis, representing the probability density, and the radius \( r \) along the x-axis. It shows three curves, each corresponding to a Gaussian distribution in different dimensional spaces: \( D = 1 \) (likely the green curve), \( D = 2 \) (likely the red curve), and \( D = 20 \) (likely the blue curve).

The plot illustrates that as the dimensionality \( D \) increases, the peak of the Gaussian distribution shifts to the right, and the distribution becomes increasingly concentrated within a thin shell at a specific radius. This visualization helps to understand the behavior of probability distributions in high-dimensional spaces and their significance in the context of machine learning and other areas where high-dimensional data is commonly encountered. 

The notion captured here is in line with the text's description that in high-dimensional spaces, most of the volume or probability mass is concentrated in a thin shell away from the center of the distribution, which is a counterintuitive property arising from the 'curse of dimensionality.')

As a further example of direct relevance to machine learning, consider the behaviour of a Gaussian distribution in a high-dimensional space. If we transform from Cartesian to polar coordinates and then integrate out the directional variables, we obtain an expression for the density $p(r)$ as a function of radius $r$ from the origin. Thus, $p(r) \delta r$ is the probability mass inside a thin shell of thickness $\delta r$ located at radius $r$. This distribution is plotted, for various values of $D$, in Figure 6.5 , and we see that for large $D$, the probability mass of the Gaussian is concentrated in a thin shell at a specific radius.

In this book, we make extensive use of illustrative examples involving one or two variables, because this makes it particularly easy to visualize these spaces graphically. The reader should be warned, however, that not all intuitions developed in spaces of low dimensionality will generalize to situations involving many dimensions.

Finally, although we have talked about the curse of dimensionality, there can also be advantages to working in high-dimensional spaces. Consider the situation shown in Figure 6.6. We see that this data set, in which each data point consists of a pair of values $\left(x_{1}, x_{2}\right)$, is linearly separable, but when only the value of $x_{1}$ is observed, the classes have a strong overlap. The classification problem is therefore much easier in the higher-dimensional space.

\title{
6.1.3 Data manifolds
}

With both the polynomial regression model and the grid-based classifier in Figure 6.2, we saw that the number of basis functions grows rapidly with dimensionality, making such methods impractical for applications involving even a few dozen variables, never mind the millions of inputs that often arise with, say, image processing. The problem is that the basis functions are fixed ahead of time and do not depend on the data, or indeed even on the specific problem being solved. We need to find a way to create basis functions that are tuned to the particular application.

Although the curse of dimensionality certainly raises important issues for machine learning applications, it does not prevent us from finding effective techniques applicable to high-dimensional spaces. One reason for this is that real data will generally be confined to a region of the data space having lower effective dimen-

![](https://cdn.mathpix.com/cropped/2024_05_26_0971150439f155ba27cfg-1.jpg?height=508&width=515&top_left_y=215&top_left_x=304

ChatGPT figure/image summary: The image provided appears to be a two-dimensional scatter plot with two distinct classes of data points. One class is represented by green circles and the other by red circles. A dashed diagonal line separates the two classes, suggesting that the line could be a decision boundary for a linear classifier. This graphical representation is used to illustrate the concept of linear separability in a two-dimensional feature space, where each data point consists of a pair $(x_1, x_2)$ corresponding to the axes of the plot. The presence of a linear decision boundary implies that a linear algorithm could be used to classify the data points successfully into their respective classes based on the values of the two features $x_1$ and $x_2$.)

(a) (b)

Figure 6.6 Illustration of a data set in two dimensions $\left(x_{1}, x_{2}\right)$ in which data points from the two classes depicted using green and red circles can be separated by a linear decision surface, as seen in (a). If, however, only the variable $x_{1}$ is measured then the classes are no longer separable, as seen in (b).

sionality. Consider the images shown in Figure 6.7. Each image is a point in a high-dimensional space whose dimensionality is determined by the number of pixels. Because the objects can occur at different vertical and horizontal positions within the image and in different orientations, there are three degrees of freedom of variability between images, and a set of images will, to a first approximation, live on a three-dimensional manifold embedded within the high-dimensional space. Due to the complex relationships between the object position or orientation and the pixel intensities, this manifold will be highly nonlinear.

In fact, the number of pixels is really an artefact of the image generation process since they represent measurements of a continuous world. Capturing the same image at a higher resolution increases the dimensionality $D$ of the data space without changing the fact that the images still live on a three-dimensional manifold. If we can associate localized basis functions with the data manifold, rather than with the entire high-dimensional data space, we might expect that the number of required basis functions would grow exponentially with the dimensionality of the manifold rather than with the dimensionality of the data space. Since the manifold will typically have a much lower dimensionality than the data space, this represents a huge

Figure 6.7 Examples of images of a handwritten digit that differ in the location of the digit within the images as well as in their orientation. This data lives on a nonlinear threedimensional manifold within the high-dimensional image space.
![](https://cdn.mathpix.com/cropped/2024_05_26_0971150439f155ba27cfg-1.jpg?height=384&width=554&top_left_y=1742&top_left_x=916

ChatGPT figure/image summary: The image contains a grid of six smaller images arranged in two rows and three columns. Each small image shows a handwritten digit "5" against a white background. The digit "5" appears in different locations within each small image frame and is drawn in red. The orientation of the digit also varies slightly from image to image, demonstrating variability in position and orientation within a set of images that are conceptually similar but have differences in detail. This could be used to illustrate the concept of a data manifold in machine learning, where each image represents a point on a manifold within a higher-dimensional space.)

![](https://cdn.mathpix.com/cropped/2024_05_26_0971150439f155ba27cfg-1.jpg?height=371&width=168&top_left_y=1751&top_left_x=1479

ChatGPT figure/image summary: The image shows two examples of handwritten digit "5", one positioned higher and the other lower in their respective white rectangular frames. The two images represent variations in vertical position within the images, which is part of the three degrees of freedom of variability (position and orientation) mentioned in the text. This exemplifies how a set of images with such variability can be understood as data points existing on a nonlinear three-dimensional manifold within the high-dimensional pixel space.)


![](https://cdn.mathpix.com/cropped/2024_05_26_d448ccb748bfa00d34aag-1.jpg?height=690&width=1044&top_left_y=230&top_left_x=507

ChatGPT figure/image summary: The image depicts a visual comparison between natural images and randomly generated images. In the top row, we see examples of natural images that are 64 by 64 pixels in size. These images display recognizable subjects such as an apparent blurry image on the left, a bicycle in the center, and a cat on the right. The bottom row shows images of the same size that were created by randomly generating pixel values from a uniform distribution for each pixel's color components (red, green, and blue). The resulting images are non-representational and appear as a noisy collection of multicolored pixels, demonstrating the difference between structured natural images and unstructured random noise. This comparison illustrates how real-world images occupy a small, structured portion of the high-dimensional space of possible images.)

Figure 6.8 The top row shows examples of natural images of size $64 \times 64$ pixels, whereas the bottom row shows randomly generated images of the same size obtained by drawing pixel values from a uniform probability distribution over the possible pixel colours.

improvement. Effectively, neural networks learn a set of basis functions that are adapted to data manifolds. Moreover, for a particular application, not all directions within the manifold may be significant. For example, if we wish to determine only the orientation, and not the position, of the object in Figure 6.7, then there is only one relevant degree of freedom on the manifold and not three. Neural networks are also able to learn which directions on the manifold are relevant to predicting the desired outputs.

Another way to see that real data is confined to low-dimensional manifolds is to consider the task of generating random images. In Figure 6.8 we see examples of natural images along with examples of synthetic images of the same resolution generated by sampling each of the red, green, and blue intensities at each pixel independently at random from a uniform distribution. We see that none of the synthetic images look at all like natural images. The reason is that these random images lack the very strong correlations between pixels that natural images exhibit. For example, two adjacent pixels in a natural image have a much higher probability of having the same, or very similar, colour, than would two adjacent images in the random examples. Each of the images in Figure 6.8 corresponds to a point in a high-dimensional space, yet natural images cover only a tiny fraction of this space.

\title{
6.1.4 Data-dependent basis functions
}

We have seen that simple basis functions that are chosen independently of the problem being solved can run into significant limitations, particularly in spaces of high dimensionality. If we want to use basis functions in such situations, then one approach would be to use expert knowledge to hand-craft the basis functions in a

way that is specific to each application. For many years, this was the mainstream approach in machine learning. Basis functions, often called features, would be determined by a combination of domain knowledge and trial-and-error. However, this approach met with limited success and was superseded by data-driven approaches in which basis functions are learned from the training data. Domain knowledge still plays a role in modern machine learning, but at a more qualitative level in designing network architectures where it can capture appropriate inductive bias, as we will see in later chapters.

Since data in a high-dimensional space may be confined to a low-dimensional manifold, we do not need basis functions that densely fill the whole input space, but instead we can use basis functions that are themselves associated with the data manifold. One way to do this is to have one basis function associated with each data point in the training set, which ensures that the basis functions are automatically adapted to the underlying data manifold. An example of such a model is that of radial basis functions (Broomhead and Lowe, 1988), which have the property that each basis function depends only on the radial distance (typically Euclidean) from a central vector. If the basis centres are chosen to be the input data values $\left\{\mathbf{x}_{n}\right\}$ then there is one basis function $\phi_{n}(\mathbf{x})$ for each data point, which will therefore capture the whole of the data manifold. A typical choice for a radial basis function is

$$
\phi_{n}(\mathbf{x})=\exp \left(-\frac{\left\|\mathbf{x}-\mathbf{x}_{n}\right\|^{2}}{s^{2}}\right)
$$

where $s$ is a parameter controlling the width of the basis function. Although it can be quick to set up such a model, a major problem with this technique is that it becomes computationally unwieldy for large data sets. Moreover, the model needs careful regularization to avoid severe over-fitting.

A related approach, called a support vector machine or SVM (Vapnik, 1995; Schölkopf and Smola, 2002; Bishop, 2006), addresses this by again defining basis functions that are centred on each of the training data points and then selecting a subset of these automatically during training. As a result, the effective number of basis functions in the resulting models is generally much smaller than the number of training points, although it is often still relatively large and typically increases with the size of the training set. Support vector machines also do not produce probabilistic outputs, and they do not naturally generalize to more than two classes. Methods such as radial basis functions and support vector machines have been superseded by deep neural networks, which are much better at exploiting very large data sets efficiently. Moreover, as we will see later, neural networks are able to learn deep hierarchical representations, which are crucial to achieving high prediction accuracy in more complex applications.


Figure 6.10 Illustration of the capability of a two-layer neural network to approximate four different functions: (a) $f(x)=x^{2}$, (b) $f(x)=$ $\sin (x), \quad(\mathrm{c}), f(x)=|x|$, and (d) $f(x)=H(x)$ where $H(x)$ is the Heaviside step function. In each case, $N=50$ data points, shown as blue dots, have been sampled uniformly in $x$ over the interval $(-1,1)$ and the corresponding values of $f(x)$ evaluated. These data points are then used to train a two-layer network having three hidden units with tanh activation functions and linear output units. The resulting network functions are shown by the red curves, and the outputs of the three hidden units are shown by the three dashed curves.

![](https://cdn.mathpix.com/cropped/2024_05_26_53b5c38c9dec90db1928g-1.jpg?height=401&width=491&top_left_y=222&top_left_x=624)

(a)

![](https://cdn.mathpix.com/cropped/2024_05_26_53b5c38c9dec90db1928g-1.jpg?height=396&width=486&top_left_y=674&top_left_x=634)

(c)

![](https://cdn.mathpix.com/cropped/2024_05_26_53b5c38c9dec90db1928g-1.jpg?height=391&width=493&top_left_y=232&top_left_x=1131)

(b)

![](https://cdn.mathpix.com/cropped/2024_05_26_53b5c38c9dec90db1928g-1.jpg?height=393&width=481&top_left_y=673&top_left_x=1142)

(d)

The approximation properties of two-layer feed-forward networks were widely studied in the 1980s, with various theorems showing that, for a wide range of activation functions, such networks can approximate any function defined over a continuous subset of $\mathbb{R}^{D}$ to arbitrary accuracy (Funahashi, 1989; Cybenko, 1989; Hornik, Stinchcombe, and White, 1989; Leshno et al., 1993). A similar result holds for functions from any finite-dimensional discrete space to any another. Neural networks are therefore said to be universal approximators.

Although such theorems are reassuring, they tell us only that there exists a network that can represent the required function. In some cases, they may require networks that have an exponentially large number of hidden units. Moreover, they say nothing about whether such a network can be found by a learning algorithm. Fur-

Section 9.1.2 thermore, we will see later that the no free lunch theorem says that we can never find a truly universal machine learning algorithm. Finally, although networks having two layers of weights are universal approximators, in a practical application, there can be huge benefits in considering networks having many more than two layers that can learn hierarchical internal representations. All these points support the drive towards deep learning.

\title{
6.2.3 Hidden unit activation functions
}

We have seen that the activation functions for the output units are determined by the kind of distribution being modelled. For the hidden units, however, the only requirement is that they need to be differentiable, which leaves a wide range of pos-
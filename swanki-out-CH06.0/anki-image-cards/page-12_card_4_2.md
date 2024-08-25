### Card 1

How were the $N=50$ data points sampled and used in training the neural network shown in the image?

![](https://cdn.mathpix.com/cropped/2024_05_26_53b5c38c9dec90db1928g-1.jpg?height=393&width=481&top_left_y=673&top_left_x=1142)

%

The $N=50$ data points, shown as blue dots, were sampled uniformly in $x$ over the interval $(-1,1)$. The corresponding values of $f(x)$ were then evaluated. These data points were used to train a two-layer network with three hidden units having tanh activation functions and linear output units. The red curves represent the resulting network functions, while the dashed curves show the outputs of the three hidden units.

- neural-networks.feed-forward, data-sampling.uniform, training.methods

### Card 2

What theorem justifies that two-layer feed-forward networks can approximate any function to arbitrary accuracy?

![](https://cdn.mathpix.com/cropped/2024_05_26_53b5c38c9dec90db1928g-1.jpg?height=393&width=481&top_left_y=673&top_left_x=1142)

%

The theorem that justifies that two-layer feed-forward networks can approximate any function to arbitrary accuracy is proved by Funahashi (1989), Cybenko (1989), Hornik, Stinchcombe, and White (1989), and Leshno et al. (1993). They showed that for a wide range of activation functions, such networks can approximate any function defined over a continuous subset of $\mathbb{R}^D$ to arbitrary accuracy. Therefore, neural networks are said to be universal approximators.

- neural-networks.feed-forward, universal-approximation.theorems, activation-functions.research
## How are the data points and the resulting network functions represented in the provided image for the network training?

![](https://cdn.mathpix.com/cropped/2024_05_26_53b5c38c9dec90db1928g-1.jpg?height=391&width=493&top_left_y=232&top_left_x=1131)

%

In the provided image:
- $N=50$ data points, shown as blue dots, have been sampled uniformly in $x$ over the interval $(-1,1)$, and the corresponding values of $f(x)$ evaluated.
- These data points are used to train a two-layer network with three hidden units using tanh activation functions.
- The red curves represent the resulting network functions.
- The outputs of the three hidden units are shown by the three dashed curves.

- #neural-networks, #network-training.data-representation, #function-approximation

---

## Explain the concept of "universal approximators" concerning two-layer feed-forward networks.

![](https://cdn.mathpix.com/cropped/2024_05_26_53b5c38c9dec90db1928g-1.jpg?height=391&width=493&top_left_y=232&top_left_x=1131)

%

Two-layer feed-forward networks are termed "universal approximators." This means that for a wide range of activation functions, such networks can approximate any function defined over a continuous subset of $\mathbb{R}^{D}$ to arbitrary accuracy. This concept is supported by various theorems by Funahashi (1989), Cybenko (1989), Hornik, Stinchcombe, and White (1989), and Leshno et al. (1993). A similar result holds for functions from any finite-dimensional discrete space to another. However, these theorems only guarantee the existence of a network that can represent the required function.

- #neural-networks, #universal-approximators, #theory



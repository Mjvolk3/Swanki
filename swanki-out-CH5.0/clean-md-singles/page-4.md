
![](https://cdn.mathpix.com/cropped/2024_05_26_a79f6f03ec68f3fd25e6g-1.jpg?height=664&width=1450&top_left_y=212&top_left_x=152)

Figure 5.2 Attempting to construct a $K$-class discriminant from a set of two-class discriminant functions leads to ambiguous regions, as shown in green. On the left is an example with two discriminant functions designed to distinguish points in class $\mathcal{C}_{k}$ from points not in class $\mathcal{C}_{k}$. On the right is an example involving three discriminant functions each of which is used to separate a pair of classes $\mathcal{C}_{k}$ and $\mathcal{C}_{j}$.

In this case, the decision surfaces are $D$-dimensional hyperplanes passing through the origin of the $(D+1)$-dimensional expanded input space.

\title{
5.1.2 Multiple classes
}

Now consider the extension of linear discriminant functions to $K>2$ classes. We might be tempted to build a $K$-class discriminant by combining a number of two-class discriminant functions. However, this leads to some serious difficulties (Duda and Hart, 1973), as we now show.

Consider a model with $K-1$ classifiers, each of which solves a two-class problem of separating points in a particular class $\mathcal{C}_{k}$ from points not in that class. This is known as a one-versus-the-rest classifier. The left-hand example in Figure 5.2 shows an example involving three classes where this approach leads to regions of input space that are ambiguously classified.

An alternative is to introduce $K(K-1) / 2$ binary discriminant functions, one for every possible pair of classes. This is known as a one-versus-one classifier. Each point is then classified according to a majority vote amongst the discriminant functions. However, this too runs into the problem of ambiguous regions, as illustrated in the right-hand diagram of Figure 5.2.

We can avoid these difficulties by considering a single $K$-class discriminant comprising $K$ linear functions of the form

$$
y_{k}(\mathbf{x})=\mathbf{w}_{k}^{\mathrm{T}} \mathbf{x}+w_{k 0}
$$

and then assigning a point $\mathbf{x}$ to class $\mathcal{C}_{k}$ if $y_{k}(\mathbf{x})>y_{j}(\mathbf{x})$ for all $j \neq k$. The decision boundary between class $\mathcal{C}_{k}$ and class $\mathcal{C}_{j}$ is therefore given by $y_{k}(\mathbf{x})=y_{j}(\mathbf{x})$ and
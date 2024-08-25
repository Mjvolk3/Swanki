Figure 6.2 Illustration of a simple approach for solving classification problems in which the input space is divided into cells and any new test point is assigned to the class that has the most representatives in the same cell as the test point. As we shall see shortly, this simplistic approach has some severe shortcomings.

![](https://cdn.mathpix.com/cropped/2024_05_26_628bb04fbcc19ed959eag-1.jpg?height=694&width=706&top_left_y=215&top_left_x=956)

belongs to, and then we find all the training data points that fall in the same cell. The identity of the test point is predicted to be the same as the class having the largest number of training points in the same cell as the test point (with ties being broken at random). We can view this as a basis function model in which there is a basis function $\phi_{i}(\mathrm{x})$ for each grid cell, which simply returns zero if $\mathrm{x}$ lies outside the grid cell, and otherwise returns the majority class of the training data points that fall inside the cell. The output of the model is then given by the sum of the outputs of all the basis functions.

There are numerous problems with this naive approach, but one of the most severe becomes apparent when we consider its extension to problems having larger numbers of input variables, corresponding to input spaces of higher dimensionality. The origin of the problem is illustrated in Figure 6.3, which shows that, if we divide a region of a space into regular cells, then the number of such cells grows exponentially with the dimensionality of the space. The challenge with an exponentially large number of cells is that we would need an exponentially large quantity of training

Figure 6.3 Illustration of the curse of dimensionality, showing how the number of regions of a regular grid grows exponentially with the dimensionality $D$ of the space. For clarity, only a subset of the cubical regions are shown for $D=3$.

![](https://cdn.mathpix.com/cropped/2024_05_26_628bb04fbcc19ed959eag-1.jpg?height=81&width=262&top_left_y=2006&top_left_x=638)

$D=1$

![](https://cdn.mathpix.com/cropped/2024_05_26_628bb04fbcc19ed959eag-1.jpg?height=293&width=313&top_left_y=1773&top_left_x=918)

$D=2$

![](https://cdn.mathpix.com/cropped/2024_05_26_628bb04fbcc19ed959eag-1.jpg?height=412&width=394&top_left_y=1655&top_left_x=1244)

$D=3$
Figure 6.1 Plot of the Iris data in which red, green, and blue points denote three species of iris flower and the axes represent measurements of the length and width of the sepal, respectively. Our goal is to classify a new test point such as the one denoted by \(x\).

![](https://cdn.mathpix.com/cropped/2024_05_26_b8f14dbc6f67539ba08cg-1.jpg?height=684&width=706&top_left_y=222&top_left_x=956)

would take the form

\[
y(\mathbf{x}, \mathbf{w})=w_{0}+\sum_{i=1}^{D} w_{i} x_{i}+\sum_{i=1}^{D} \sum_{j=1}^{D} w_{i j} x_{i} x_{j}+\sum_{i=1}^{D} \sum_{j=1}^{D} \sum_{k=1}^{D} w_{i j k} x_{i} x_{j} x_{k}
\]

As \(D\) increases, the growth in the number of independent coefficients is \(\mathcal{O}\left(D^{3}\right)\), whereas for a polynomial of order \(M\), the growth in the number of coefficients is \(\mathcal{O}\left(D^{M}\right)\) (Bishop, 2006). We see that in spaces of higher dimensionality, polynomials can rapidly become unwieldy and of little practical utility.

The severe difficulties that can arise in spaces of many dimensions is sometimes called the curse of dimensionality (Bellman, 1961). It is not limited to polynomial regression but is in fact quite general. Consider the use of linear models for solving classification problems. Figure 6.1 shows a plot of data from the Iris data set comprising 50 observations taken from each of three species of iris flowers. Each observation has four variables representing measurements of the sepal length, sepal width, petal length, and petal width. For this illustration, we consider only the sepal length and sepal width variables. Given these 150 observations as training data, our goal is to classify a new test point, such as the one denoted by the cross in Figure 6.1, by assigning it to one of the three species. We observe that the cross is close to several red points, and so we might suppose that it belongs to the red class. However, there are also some green points nearby, so we might think that it could instead belong to the green class. It seems less likely that it belongs to the blue class. The intuition here is that the identity of the cross should be determined more strongly by nearby points from the training set and less strongly by more distant points, and this intuition turns out to be reasonable.

One very simple way of converting this intuition into a learning algorithm would be to divide the input space into regular cells, as indicated in Figure 6.2. When we are given a test point and we wish to predict its class, we first decide which cell it
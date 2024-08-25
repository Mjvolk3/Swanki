![](https://cdn.mathpix.com/cropped/2024_05_18_a0676cf8759377514923g-1.jpg?height=977&width=1512&top_left_y=203&top_left_x=148)

![](https://cdn.mathpix.com/cropped/2024_05_18_a0676cf8759377514923g-1.jpg?height=427&width=706&top_left_y=214&top_left_x=155)

![](https://cdn.mathpix.com/cropped/2024_05_18_a0676cf8759377514923g-1.jpg?height=428&width=705&top_left_y=736&top_left_x=153)

![](https://cdn.mathpix.com/cropped/2024_05_18_a0676cf8759377514923g-1.jpg?height=432&width=693&top_left_y=214&top_left_x=953)

![](https://cdn.mathpix.com/cropped/2024_05_18_a0676cf8759377514923g-1.jpg?height=432&width=693&top_left_y=734&top_left_x=953)

Figure 1.6 Plots of polynomials having various orders $M$, shown as red curves, fitted to the data set shown in Figure 1.4 by minimizing the error function (1.2).

passes exactly through each data point and $E\left(\mathbf{w}^{\star}\right)=0$. However, the fitted curve oscillates wildly and gives a very poor representation of the function $\sin (2 \pi x)$. This latter behaviour is known as over-fitting.

Our goal is to achieve good generalization by making accurate predictions for new data. We can obtain some quantitative insight into the dependence of the generalization performance on $M$ by considering a separate set of data known as a test set, comprising 100 data points generated using the same procedure as used to generate the training set points. For each value of $M$, we can evaluate the residual value of $E\left(\mathbf{w}^{\star}\right)$ given by (1.2) for the training data, and we can also evaluate $E\left(\mathbf{w}^{\star}\right)$ for the test data set. Instead of evaluating the error function $E(\mathbf{w})$, it is sometimes more convenient to use the root-mean-square (RMS) error defined by

$$
E_{\mathrm{RMS}}=\sqrt{\frac{1}{N} \sum_{n=1}^{N}\left\{y\left(x_{n}, \mathbf{w}\right)-t_{n}\right\}^{2}}
$$

in which the division by $N$ allows us to compare different sizes of data sets on an equal footing, and the square root ensures that $E_{\mathrm{RMS}}$ is measured on the same scale (and in the same units) as the target variable $t$. Graphs of the training-set and test-set
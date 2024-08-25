Figure 2.3 Illustration of the accuracy of a cancer test. Out of every hundred people taking the test who do not have cancer, shown on the left, on average three will test positive. For those who have cancer, shown on the right, out of every hundred people taking the test, on average 90 will test positive.

![](https://cdn.mathpix.com/cropped/2024_05_10_103c75cae03fc6403b87g-1.jpg?height=564&width=745&top_left_y=216&top_left_x=912)

one receives a positive test result, what is the probability that they actually have cancer?'. We could answer such questions by working through the cancer screening case in detail. Instead, however, we will pause our discussion of this specific example and first derive the general rules of probability, known as the sum rule of probability and the product rule. We will then illustrate the use of these rules by answering our two questions.

\title{
2.1.2 The sum and product rules
}

To derive the rules of probability, consider the slightly more general example shown in Figure 2.4 involving two variables $X$ and $Y$. In our cancer example, $X$ could represent the presence or absence of cancer, and $Y$ could be a variable denoting the outcome of the test. Because the values of these variables can vary from one person to another in a way that is generally unknown, they are called random variables or stochastic variables. We will suppose that $X$ can take any of the values $x_{i}$ where $i=1, \ldots, L$ and that $Y$ can take the values $y_{j}$ where $j=1, \ldots, M$. Consider a total of $N$ trials in which we sample both of the variables $X$ and $Y$, and let the number of such trials in which $X=x_{i}$ and $Y=y_{j}$ be $n_{i j}$. Also, let the number of trials in which $X$ takes the value $x_{i}$ (irrespective of the value that $Y$ takes) be denoted by $c_{i}$, and similarly let the number of trials in which $Y$ takes the value $y_{j}$ be denoted by $r_{j}$.

The probability that $X$ will take the value $x_{i}$ and $Y$ will take the value $y_{j}$ is written $p\left(X=x_{i}, Y=y_{j}\right)$ and is called the joint probability of $X=x_{i}$ and $Y=y_{j}$. It is given by the number of points falling in the cell $i, j$ as a fraction of the total number of points, and hence

$$
p\left(X=x_{i}, Y=y_{j}\right)=\frac{n_{i j}}{N}
$$

Here we are implicitly considering the limit $N \rightarrow \infty$. Similarly, the probability that $X$ takes the value $x_{i}$ irrespective of the value of $Y$ is written as $p\left(X=x_{i}\right)$ and is
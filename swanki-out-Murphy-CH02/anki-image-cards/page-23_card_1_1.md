### Card 1

##

![](https://cdn.mathpix.com/cropped/2024_06_13_855eab66de586ca6078dg-1.jpg?height=367&width=554&top_left_y=207&top_left_x=733)

What does the scatter plot with decision boundaries in the image represent?

%

The scatter plot with decision boundaries represents multinomial logistic regression applied to a 3-class, 2-feature version of the Iris dataset. The horizontal axis marks the petal length, and the vertical axis shows the petal width. The plot depicts three Iris species:

- **Iris Virginica**: Green triangles
- **Iris Versicolor**: Yellow circles
- **Iris Setosa**: Blue squares

The background gradient and contour lines indicate class probabilities across the feature space. The decision boundaries highlight the regions where the logistic regression model classifies the Iris species. Key observations include a clear separation between Iris Setosa and the other species, and a slight overlap between Iris Virginica and Iris Versicolor, illustrating classification ambiguities based on these features.

- #machine-learning, datasets.iris, models.logistic-regression

### Card 2

##

![](https://cdn.mathpix.com/cropped/2024_06_13_855eab66de586ca6078dg-1.jpg?height=367&width=554&top_left_y=207&top_left_x=733)

Explain the mathematical properties of the softmax function used in multinomial logistic regression, as depicted in the image from the Iris dataset.

%

The softmax function transforms a vector $\mathbf{a}$ from $\mathbb{R}^{C}$ to $[0, 1]^{C}$ and adheres to two key properties:

1. $0 \leq \operatorname{softmax}(\boldsymbol{a})_{c} \leq 1$ for each class $c$.
2. The sum of the probabilities for all classes equals 1, i.e., $\sum_{c=1}^{C} \operatorname{softmax}(\boldsymbol{a})_{c} = 1$.

The function is defined as:

$$
\operatorname{softmax}(\mathbf{a})_{c} = \frac{e^{a_c}}{\sum_{k=1}^{C} e^{a_k}}
$$

This ensures that the output probabilities share mutual exclusivity and exhaustive completeness, key for multinomial logistic regression. In the context of the Iris dataset, these principles ensure each prediction reflects a well-calibrated probability distribution across the three classes.

- #machine-learning, functions.softmax, models.logistic-regression

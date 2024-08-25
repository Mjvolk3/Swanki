
![](https://cdn.mathpix.com/cropped/2024_05_26_eb0b6807a540759d07d1g-1.jpg?height=706&width=1470&top_left_y=238&top_left_x=151)

Figure 5.4 The left-hand plot shows data from two classes, denoted by red crosses and blue circles, together with the decision boundaries found by least squares (magenta curve) and by a logistic regression model (green curve). The right-hand plot shows the corresponding results obtained when extra data points are added at the bottom right of the diagram, showing that least squares is highly sensitive to outliers, unlike logistic regression.

\title{
5.2. Decision Theory
}

When we discussed linear regression we saw how the process of making predictions

Section 4.2 in machine learning can be broken down into the two stages of inference and decision. We now explore this perspective in much greater depth specifically in the context of classifiers.

Suppose we have an input vector \(\mathbf{x}\) together with a corresponding vector \(\mathbf{t}\) of target variables, and our goal is to predict \(\mathbf{t}\) given a new value for \(\mathbf{x}\). For regression problems, \(\mathbf{t}\) will comprise continuous variables and in general will be a vector as we may wish to predict several related quantities. For classification problems, \(\mathbf{t}\) will represent class labels. Again, \(\mathbf{t}\) will in general be a vector if we have more than two classes. The joint probability distribution \(p(\mathbf{x}, \mathbf{t})\) provides a complete summary of the uncertainty associated with these variables. Determining \(p(\mathbf{x}, \mathbf{t})\) from a set of training data is an example of inference and is typically a very difficult problem whose solution forms the subject of much of this book. In a practical application, however, we must often make a specific prediction for the value of \(t\) or more generally take a specific action based on our understanding of the values \(t\) is likely to take, and this aspect is the subject of decision theory.

Consider, for example, our earlier medical diagnosis problem in which we have taken an image of a skin lesion on a patient, and we wish to determine whether the patient has cancer. In this case, the input vector \(\mathbf{x}\) is the set of pixel intensities in
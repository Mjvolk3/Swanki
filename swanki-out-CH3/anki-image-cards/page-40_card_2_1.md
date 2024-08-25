## How does the $K$-nearest neighbour (K-NN) classifier determine the class of a new data point?

![](https://cdn.mathpix.com/cropped/2024_05_13_8f53b2b39e722c44ef82g-1.jpg?height=504&width=515&top_left_y=212&top_left_x=1130)

% 

In the $K$-nearest neighbour classifier, the class of a new point, depicted as a black diamond in the figure, is determined based on the majority class among the $K$ nearest points from the training dataset. For $K=3$, as shown in Figure 3.16(a), the class is assigned by counting which class (red or blue) appears most frequently among the three closest training data points to this new point.

- #machine-learning, #classification, #k-nearest-neighbour

## How is the decision boundary formed in a $K=1$ nearest-neighbour classifier?

![](https://cdn.mathpix.com/cropped/2024_05_13_8f53b2b39e722c44ef82g-1.jpg?height=504&width=515&top_left_y=212&top_left_x=1130)

% 

In the $K=1$ nearest-neighbour classification approach, the decision boundary consists of hyperplanes that act as perpendicular bisectors between pairs of nearest points that belong to different classes. This is evident from the nonlinear, complex pattern of the decision boundary as shown in Figure 3.16(b). The boundary adapts closely to the layout of individual nearest points, reflecting the principle that a new point is simply classified to the same class as its single nearest neighbour.

- #machine-learning, #classification, #nearest-neighbour
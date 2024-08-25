## How is a new point classified in a $K$-nearest neighbour classifier according to the provided image?

![](https://cdn.mathpix.com/cropped/2024_05_13_8f53b2b39e722c44ef82g-1.jpg?height=491&width=515&top_left_y=214&top_left_x=622)

%

In the $K$-nearest neighbour classifier as depicted in the image, a new point (represented by a black diamond) is classified based on the majority class membership among its closest $K$ neighbours. For this specific example, $K=3$, and it appears that the nearest three points are considered to determine the class of the new point. Each green line connects the black diamond to one of its nearest points, highlighting the proximity that influences its class determination.

- #data-science, #machine-learning.k-nn, #classification-methods.k-nearest-neighbour

## What does the nearest-neighbour (K=1) method of classification entail?

![](https://cdn.mathpix.com/cropped/2024_05_13_8f53b2b39e722c44ef82g-1.jpg?height=491&width=515&top_left_y=214&top_left_x=622)

%

In the nearest-neighbour ($K=1$) approach of classification, a new test point is simply classified to the same class as its nearest training point. The decision boundary in this approach, assuming points from dissimilar classes are present, is usually made up of hyperplanes that serve as perpendicular bisectors between pairs of points from these different classes. Thus, the decision boundary can be complex and highly sensitive to the specific locations of individual points in the training dataset. This method can show high variance in complex datasets.

- #data-science, #machine-learning.k-nn, #classification-methods.nearest-neighbour
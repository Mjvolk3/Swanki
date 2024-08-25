## What is the technique of $S$-fold cross-validation, illustrated here for $S=4$?

![](https://cdn.mathpix.com/cropped/2024_05_18_00737bf1ec602cb9d4a6g-1.jpg?height=78&width=416&top_left_y=293&top_left_x=1128)

%

$S$-fold cross-validation involves partitioning the available data into $S$ groups of equal size. For $S=4$, $S-1$ of the groups are used for training, and the remaining group is used for testing. This procedure is repeated for all $S$ possible choices for the held-out group, with the performance scores from the $S$ runs then averaged.

- #machine-learning, #model-validation.cross-validation, #statistical-methods

## In a 4-fold cross-validation, what proportion of the available data is used for training?

![](https://cdn.mathpix.com/cropped/2024_05_18_00737bf1ec602cb9d4a6g-1.jpg?height=78&width=416&top_left_y=293&top_left_x=1128)

%

For $S=4$ in $S$-fold cross-validation, the proportion of the available data used for training is $\frac{S-1}{S} = \frac{3}{4} = 0.75$.

- #machine-learning, #model-validation.cross-validation, #statistical-methods
## How does $S$-fold cross-validation work?

![](https://cdn.mathpix.com/cropped/2024_05_18_00737bf1ec602cb9d4a6g-1.jpg?height=71&width=403&top_left_y=375&top_left_x=1127)

%
 
In $S$-fold cross-validation, the data is partitioned into $S$ groups of equal size. For each of these $S$ iterations (or runs), $S-1$ groups are used for training, and the remaining group is used for validation. This process is repeated for all $S$ possible choices for the held-out group, and the performance scores from the $S$ runs are averaged. Each run’s validation performance is indicated by different red blocks.

- #machine-learning, #cross-validation, #model-validation


## In $S$-fold cross-validation, what is the proportion of data used for training?

![](https://cdn.mathpix.com/cropped/2024_05_18_00737bf1ec602cb9d4a6g-1.jpg?height=71&width=403&top_left_y=375&top_left_x=1127)

%

In $S$-fold cross-validation, the training data proportion is $(S-1)/S$ of the total data.

- #machine-learning, #cross-validation, #data-proportion
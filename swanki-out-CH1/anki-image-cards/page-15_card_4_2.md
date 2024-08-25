## Front

What is illustrated by the technique shown in this image?

![](https://cdn.mathpix.com/cropped/2024_05_18_00737bf1ec602cb9d4a6g-1.jpg?height=71&width=410&top_left_y=453&top_left_x=1131)

%
## Back

The image illustrates the technique of $S$-fold cross-validation, where the available data is partitioned into $S$ groups of equal size. One group is held out as a validation set (indicated by the red block), while the remaining $S-1$ groups are used for training. This process is repeated for all $S$ possible choices of the held-out group. The performance scores from the $S$ runs are then averaged to assess the model's performance.

- #machine-learning.cross-validation, #statistics.validation-techniques, #data-analysis

---

## Front

In the context of $S$-fold cross-validation as illustrated, what proportion of the available data is used for training, and what would be the special case when $S=N$?

![](https://cdn.mathpix.com/cropped/2024_05_18_00737bf1ec602cb9d4a6g-1.jpg?height=71&width=410&top_left_y=453&top_left_x=1131)

%
## Back

In $S$-fold cross-validation, the proportion $(S-1)/S$ of the available data is used for training while all of the data is used to assess performance. When $S=N$, where $N$ is the total number of data points, this technique is called leave-one-out cross-validation, where one data point is used for validation, and the rest for training in each iteration.

- #machine-learning.cross-validation, #statistics.leave-one-out, #data-analysis
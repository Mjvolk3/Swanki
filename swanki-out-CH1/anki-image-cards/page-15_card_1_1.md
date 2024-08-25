## What is illustrated by the concept of $S$-fold cross-validation as shown in the figure?

![](https://cdn.mathpix.com/cropped/2024_05_18_00737bf1ec602cb9d4a6g-1.jpg?height=74&width=410&top_left_y=217&top_left_x=1131)

%

The concept of $S$-fold cross-validation, particularly illustrated for $S=4$, involves splitting the available data into $S$ equally sized groups. For each run, $S-1$ groups are used to train the model, and the remaining group is used for validation. This process is repeated for all $S$ possible choices of the held-out group (indicated as red blocks in the image). The performance scores from these $S$ runs are then averaged. For $S=4$, it means each group will be used as the validation set once, while the others are used for training, ensuring maximum utilization of the dataset.

- #machine-learning, #validation.techniques

## During $S$-fold cross-validation, what proportion of the available data is used for training?

![](https://cdn.mathpix.com/cropped/2024_05_18_00737bf1ec602cb9d4a6g-1.jpg?height=74&width=410&top_left_y=217&top_left_x=1131)

%

During $S$-fold cross-validation, a proportion of $(S-1)/S$ of the available data is used for training. This allows for efficient use of the dataset, as each partition is used for validation exactly once, while the rest is used for training.

- #machine-learning, #training-validation.partitioning
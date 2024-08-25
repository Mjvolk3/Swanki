## Anki Card 2

![](https://cdn.mathpix.com/cropped/2024_05_18_00737bf1ec602cb9d4a6g-1.jpg?height=74&width=410&top_left_y=217&top_left_x=1131)

What technique is illustrated in the image, and how is it executed for the case of $S=4$?

%

The technique illustrated in the image is $S$-fold cross-validation, specifically for $S=4$. Here’s how it is executed:

1. The available dataset is partitioned into four groups of equal size.
2. During each run, $3$ groups are used to train the model, and $1$ group, indicated by the red block, is used to validate the model.
3. This procedure is repeated for all $4$ possible choices of the held-out group.
4. The performance scores from these $4$ runs are then averaged to assess overall model performance.

- #machine-learning, #model-validation, #cross-validation


## Anki Card 3 (based on same image and text as Card 2)

![](https://cdn.mathpix.com/cropped/2024_05_18_00737bf1ec602cb9d4a6g-1.jpg?height=74&width=410&top_left_y=217&top_left_x=1131)

Explain the significance of using $(S-1)/S$ of the data for training in $S$-fold cross-validation.

%

In $S$-fold cross-validation, using $(S-1)/S$ of the data for training is significant because:

1. It ensures that the model training utilizes a substantial proportion of the dataset, enhancing the training process.
2. It maintains the generalization ability as the process is repeated $S$ times, with each group having a turn as the validation set.
3. This methodology leverages the entire dataset for validation over multiple runs, optimizing the performance assessment accuracy.

- #machine-learning, #model-validation, #training-data
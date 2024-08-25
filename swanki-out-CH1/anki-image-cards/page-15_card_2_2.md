### Anki Card 1
![](https://cdn.mathpix.com/cropped/2024_05_18_00737bf1ec602cb9d4a6g-1.jpg?height=78&width=416&top_left_y=293&top_left_x=1128)

What is the technique of $S$-fold cross-validation and how is it performed?

%

$S$-fold cross-validation involves partitioning the available data into $S$ groups of equal size. For each fold, $S-1$ groups are used to train the model, and the remaining group is used to test it. This process is repeated for all $S$ choices of held-out groups. The performance scores from each run are then averaged, allowing for validation while using $(S-1)/S$ of the data for training and leveraging all data for performance assessment.

- #machine-learning, #model-evaluation, #cross-validation

### Anki Card 2
![](https://cdn.mathpix.com/cropped/2024_05_18_00737bf1ec602cb9d4a6g-1.jpg?height=78&width=416&top_left_y=293&top_left_x=1128)

Why is $S$-fold cross-validation a preferred method for model evaluation?

%

$S$-fold cross-validation is preferred because it allows the utilization of the entire dataset for both training and validation purposes. By averaging the performance scores from each fold, it provides a robust and less biased estimation of the model's performance, reducing the risk of overfitting and providing a more comprehensive evaluation.

- #machine-learning, #model-evaluation, #cross-validation
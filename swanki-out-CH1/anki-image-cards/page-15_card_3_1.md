## 

What technique is depicted in the image, and what does each run represent in this method?

![](https://cdn.mathpix.com/cropped/2024_05_18_00737bf1ec602cb9d4a6g-1.jpg?height=71&width=403&top_left_y=375&top_left_x=1127)

% 

The image illustrates the technique of $S$-fold cross-validation, shown for $S=4$. In each run, $S-1$ groups of data are used to train the model, and the remaining group is used for validation. The red block in each run indicates the portion of the data held out for validation. This process is repeated for all $S$ possible choices of the held-out group, and the performance scores from the $S$ runs are averaged to assess model performance.

- machine-learning.model-validation, #cross-validation.folds

## 

How is the proportion of data utilized for training calculated in $S$-fold cross-validation?

![](https://cdn.mathpix.com/cropped/2024_05_18_00737bf1ec602cb9d4a6g-1.jpg?height=71&width=403&top_left_y=375&top_left_x=1127)

%

In $S$-fold cross-validation, the proportion of data used for training is $(S-1)/S$. This ensures that the method makes use of almost all of the available data for training while reserving one part for validation. For example, with $S=4$, three parts are used for training and one part for validation, resulting in a training proportion of $3/4$.

- machine-learning.cross-validation, #data-splitting.methods, #training-validation-data
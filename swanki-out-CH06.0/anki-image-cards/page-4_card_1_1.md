### Card 1

How does the simple approach to classification, illustrated in the given image, assign a class to a new test point?

![](https://cdn.mathpix.com/cropped/2024_05_26_628bb04fbcc19ed959eag-1.jpg?height=694&width=706&top_left_y=215&top_left_x=956)

%

The simple approach to classification divides the input space into a grid of cells. For any new test point, it identifies the cell the test point belongs to and assigns the test point to the class that has the largest number of training data points within that cell. If there is a tie, it is broken randomly. Additionally, each cell has a basis function $\phi_{i}(\mathrm{x})$ that returns zero if $\mathrm{x}$ lies outside the cell and returns the majority class of the training data points inside the cell. The model's output is the sum of the outputs of all basis functions.

- #machine-learning.classification, #basis-functions, #data-visualization

### Card 2

Describe the basis function model used for the simple classification approach illustrated in the image.

![](https://cdn.mathpix.com/cropped/2024_05_26_628bb04fbcc19ed959eag-1.jpg?height=694&width=706&top_left_y=215&top_left_x=956)

%

The basis function model for the simple classification approach uses a basis function $\phi_{i}(\mathrm{x})$ for each grid cell. This basis function returns zero if $\mathrm{x}$ lies outside the grid cell. Otherwise, it returns the majority class of the training data points within that cell. The model's output is the sum of the outputs of all these basis functions, effectively determining the majority class within the cell containing the new test point.

- #machine-learning.classification, #basis-functions, #data-visualization
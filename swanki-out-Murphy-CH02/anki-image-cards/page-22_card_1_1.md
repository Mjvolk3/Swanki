## How does temperature affect the softmax distribution for the input vector $\boldsymbol{a}=(3,0,1)$?

![](https://cdn.mathpix.com/cropped/2024_06_13_0d3c3fabafab878573b2g-1.jpg?height=362&width=941&top_left_y=204&top_left_x=545)

%

The effect of temperature on the softmax distribution of the input vector $\boldsymbol{a}=(3,0,1)$ is as follows:

- **High Temperature ($T=100$)**: The distribution is almost uniform, indicating that all classes have similar probabilities. The high temperature makes the softmax function less sensitive to differences in the input scores.
- **Moderate Temperature ($T=2$)**: The distribution reflects greater differentiation among the classes. The class with the highest input score (logit of 3) has a higher probability, but the probabilities are still relatively smooth.
- **Low Temperature ($T=1$)**: The distribution exhibits a "winner-takes-all" behavior, with the highest input score class receiving most of the probability mass. 

Each graph demonstrates that lower temperatures make the softmax function behave more like the argmax function.

- #machine-learning, #softmax, #temperature-effects
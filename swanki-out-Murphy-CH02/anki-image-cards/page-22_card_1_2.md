####

Explain the effect of temperature $T$ on the softmax distribution $\operatorname{softmax}(\boldsymbol{a} / T)$ for the input vector $\boldsymbol{a} = (3, 0, 1)$ as shown in the figure.

![](https://cdn.mathpix.com/cropped/2024_06_13_0d3c3fabafab878573b2g-1.jpg?height=362&width=941&top_left_y=204&top_left_x=545)

%

The figure shows the softmax distribution $\operatorname{softmax}(\boldsymbol{a} / T)$ at three different temperatures ($T = 100$, $T = 2$, and $T = 1$):

- At $T = 100$: The distribution is almost uniform because the high temperature diminishes the differences in input scores, making the output probabilities similar for all classes.

- At $T = 2$: The distribution shows more variance, with the class corresponding to the highest input score having a higher probability. This demonstrates a moderate sensitivity to differences in input scores.

- At $T = 1$: The distribution is "spiky" with the highest probability mass concentrated on the class with the highest input score. This low temperature emphasizes the input differences strongly, leading to a near "winner-takes-all" behavior. 

These examples illustrate that increasing the temperature smooths the distribution, while decreasing it makes the distribution more sensitive to the input score differences.

- tags: #machine-learning, #softmax-function, #temperature-effect

####

Describe the behavior of the softmax function at high and low temperatures as shown in the figure for $\boldsymbol{a} = (3, 0, 1)$.

![](https://cdn.mathpix.com/cropped/2024_06_13_0d3c3fabafab878573b2g-1.jpg?height=362&width=941&top_left_y=204&top_left_x=545)

%

- At high temperature ($T = 100$): The softmax function produces a nearly uniform distribution, assigning similar probabilities to all classes, effectively neutralizing the effect of the input score differences.

- At low temperature ($T = 1$): The softmax function has a "spiky" distribution, heavily favoring the class with the highest input score, showcasing a strong sensitivity to the input score differences and resembling a "winner-takes-all" scenario.

- tags: #machine-learning, #softmax-function, #temperature-sensitivity
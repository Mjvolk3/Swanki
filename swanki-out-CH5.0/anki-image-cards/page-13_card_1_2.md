  
### Card 1

What does the graph in Figure 5.7 illustrate regarding the reject option in classification?

![](https://cdn.mathpix.com/cropped/2024_05_26_49629de898dc2113d75dg-1.jpg?height=523&width=672&top_left_y=215&top_left_x=973)

%

The graph illustrates the use of a reject option in classification systems, where inputs $x$ are rejected if the larger of the two posterior probabilities $p(C_k \mid x)$ is less than or equal to a threshold $\theta$. This is shown by the "reject region" below the threshold $\theta$, indicating that values of $x$ within this region do not allow for a confident classification.

- classification.reject-option, statistical-methods.posterior-probabilities, probability.threshold


### Card 2

Explain the effect of setting different values for the threshold $\theta$ in the context of the reject option in classification.

![](https://cdn.mathpix.com/cropped/2024_05_26_49629de898dc2113d75dg-1.jpg?height=523&width=672&top_left_y=215&top_left_x=973)

%

Setting $\theta=1$ ensures that all examples are rejected because no posterior probability $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$ can be greater than 1. Conversely, if there are $K$ classes, setting $\theta<1/K$ ensures that no examples are rejected since the largest posterior probability will always be greater than this threshold.

- classification.threshold, statistical-methods.posterior-probabilities
## Card 1

![](https://cdn.mathpix.com/cropped/2024_05_26_7631da1ff57256b30effg-1.jpg?height=652&width=1255&top_left_y=959&top_left_x=271)

What is the significance of the decision boundary $x = \widehat{x}$ in the context of the joint probabilities $p(x, \mathcal{C}_{k})$ for two classes?

%

The decision boundary $x = \widehat{x}$ is the point that divides the input variable space into two decision regions: $\mathcal{R}_{1}$ for class $\mathcal{C}_{1}$ (for values of $x < \widehat{x}$) and $\mathcal{R}_{2}$ for class $\mathcal{C}_{2}$ (for values of $x \geqslant \widehat{x}$). This boundary is chosen to minimize the classification errors, with the errors for $x < \widehat{x}$ due to class $\mathcal{C}_{2}$ instances being misclassified as class $\mathcal{C}_{1}$ (represented by the sum of the red and green regions), and for $x \geqslant \widehat{x}$ due to class $\mathcal{C}_{1}$ instances being misclassified as $\mathcal{C}_{2}$ (represented by the blue region).

- #machine-learning, #classification, #decision-boundaries


## Card 2

![](https://cdn.mathpix.com/cropped/2024_05_26_7631da1ff57256b30effg-1.jpg?height=652&width=1255&top_left_y=959&top_left_x=271)

What do the colored regions under the curves $p(x, \mathcal{C}_{1})$ and $p(x, \mathcal{C}_{2})$ represent in the joint probability graph?

%

The colored regions under the curves represent classification errors:

- The green shaded area represents errors due to instances from class $\mathcal{C}_{2}$ being misclassified as $\mathcal{C}_{1}$ when $x < \widehat{x}$.
- The red shaded area also represents errors from class $\mathcal{C}_{2}$ misclassified as $\mathcal{C}_{1}$.
- The blue shaded area represents errors due to instances from class $\mathcal{C}_{1}$ being misclassified as $\mathcal{C}_{2}$ when $x \geqslant \widehat{x}$.

These regions illustrate the trade-offs made in setting the decision boundary $x = \widehat{x}$ to minimize the overall classification errors.

- #machine-learning, #error-analysis, #classification
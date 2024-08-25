## What is illustrated in Figure 5.5 regarding the classification and errors of two classes against the input variable $x$?

![](https://cdn.mathpix.com/cropped/2024_05_26_7631da1ff57256b30effg-1.jpg?height=652&width=1255&top_left_y=959&top_left_x=271)

% 

Figure 5.5 illustrates the joint probabilities $p\left(x, \mathcal{C}_{k}\right)$ for each of two classes plotted against $x$, and highlights the decision boundary $x=\widehat{x}$. The figure shows that:
- Values of $x \geqslant \widehat{x}$ are classified as class $\mathcal{C}_{2}$, belonging to decision region $\mathcal{R}_{2}$.
- Values of $x < \widehat{x}$ are classified as class $\mathcal{C}_{1}$, belonging to decision region $\mathcal{R}_{1}$.

Errors, represented by shaded regions under the curves, arise:
- For $x < \widehat{x}$, errors are due to class $\mathcal{C}_{2}$ instances misclassified as $\mathcal{C}_{1}$ (sum of the red and green regions).
- For $x \geqslant \widehat{x}$, errors are due to class $\mathcal{C}_{1}$ instances misclassified as $\mathcal{C}_{2}$ (blue region).

The goal is to choose $\widehat{x}$ to minimize classification errors.

- #machine-learning, #classification, #decision-boundary


## Where do classification errors occur in the decision boundary illustration of Figure 5.5?

![](https://cdn.mathpix.com/cropped/2024_05_26_7631da1ff57256b30effg-1.jpg?height=652&width=1255&top_left_y=959&top_left_x=271)

%

Classification errors in Figure 5.5 occur in the shaded regions:
- For $x < \widehat{x}$, errors are due to points from class $\mathcal{C}_{2}$ being misclassified as $\mathcal{C}_{1}$, represented by the red and green areas.
- For $x \geqslant \widehat{x}$, errors are due to points from class $\mathcal{C}_{1}$ being misclassified as $\mathcal{C}_{2}$, represented by the blue area.

The optimal decision boundary $\widehat{x}$ aims to minimize these errors.

- #machine-learning, #classification, #error-analysis
```markdown
## What does the schematic illustration of joint probabilities p(x, \mathcal{C}_k) for two classes tell us about the decision boundary and classification errors?

![](https://cdn.mathpix.com/cropped/2024_05_26_7631da1ff57256b30effg-1.jpg?height=645&width=1258&top_left_y=227&top_left_x=270)

%

Figure 5.5 illustrates the joint probabilities $p(x, \mathcal{C}_1)$ and $p(x, \mathcal{C}_k)$ for two classes plotted against input variable $x$, showing two decision regions $\mathcal{R}_1$ and $\mathcal{R}_2$, separated by a boundary at $x=\widehat{x}$. Errors occur in the blue, green, and red regions. For $x<\widehat{x}$, errors are due to class $\mathcal{C}_2$ being misclassified as $\mathcal{C}_1$ (red and green regions). For $x\geqslant\widehat{x}$, errors are due to class $\mathcal{C}_1$ being misclassified as $\mathcal{C}_2$ (blue region).

- #probability, #classification.errors, #decision-boundary
```

```markdown
## What impact does optimizing the decision boundary have on classification errors according to the schematic illustration?

![](https://cdn.mathpix.com/cropped/2024_05_26_7631da1ff57256b30effg-1.jpg?height=645&width=1258&top_left_y=227&top_left_x=270)

%

Optimizing the decision boundary to $x = x_0$ (where the two probability distributions cross) minimizes classification errors. Post-optimization (Figure 5.5b), values of $x \geqslant x_0$ are assigned to class $\mathcal{C}_2$ and values of $x < x_0$ to class $\mathcal{C}_1$, corresponding to the highest posterior probability $p(\mathcal{C}_k|x)$ for each $x$.

- #probability.optimization, #classification.errors, #decision-boundary
```
   
## How are class-conditional densities and posterior probabilities represented in the given figure?

![](https://cdn.mathpix.com/cropped/2024_05_26_3a79e15ed1a634320c5fg-1.jpg?height=702&width=1494&top_left_y=235&top_left_x=147)

%

The figure represents class-conditional densities and posterior probabilities as follows:

- **Left Plot**: Displays the class-conditional densities $p(x|\mathcal{C}_1)$ (blue) and $p(x|\mathcal{C}_2)$ (red) for classes $\mathcal{C}_1$ and $\mathcal{C}_2$ across a single input variable \( x \). The density for $\mathcal{C}_1$ has two modes, while the density for $\mathcal{C}_2$ has one mode.
- **Right Plot**: Shows the posterior probabilities $p(\mathcal{C}_1|x)$ (blue curve) and $p(\mathcal{C}_2|x)$ (red curve) as functions of \( x \), with the vertical green line indicating the decision boundary. This decision boundary minimizes the misclassification rate, assuming equal prior probabilities for both classes.

- #machine-learning, #probability, #decision-boundary

## What role does the decision boundary play in minimizing misclassification rate in the context of equal prior class probabilities?

![](https://cdn.mathpix.com/cropped/2024_05_26_3a79e15ed1a634320c5fg-1.jpg?height=702&width=1494&top_left_y=235&top_left_x=147)

%

The decision boundary, shown as a vertical green line in the right plot, represents the value of \( x \) that minimizes the misclassification rate. It separates the input space such that:

- If \( x \) is to the left of the line, the decision favors class $\mathcal{C}_1$.
- If \( x \) is to the right of the line, the decision favors class $\mathcal{C}_2$.

This boundary is chosen based on the assumption that the prior probabilities of both classes, $p(\mathcal{C}_1)$ and $p(\mathcal{C}_2)$, are equal, ensuring the minimum probability of misclassification.

- #machine-learning, #classification, #decision-boundary
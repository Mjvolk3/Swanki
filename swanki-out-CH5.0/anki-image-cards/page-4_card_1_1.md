### Card 1

Diagram illustrating ambiguous regions in multi-class classification.

![](https://cdn.mathpix.com/cropped/2024_05_26_a79f6f03ec68f3fd25e6g-1.jpg?height=664&width=1450&top_left_y=212&top_left_x=152)

%

Explain the concept of ambiguous regions in multi-class classification as illustrated in the given diagrams.

%

The diagrams illustrate ambiguous regions that arise when attempting to construct multi-class classifiers from two-class discriminants. On the left, we see the one-versus-the-rest approach, where the green shaded area indicates uncertain classification—demonstrating that points falling in this area do not get a clear class assignment through this method. On the right, the one-versus-one approach results in an ambiguous region in the center, marked by the green area, due to the intersection of decision boundaries separating each pair of classes. These ambiguities highlight the challenges in multi-class classification using these methods and the need for more robust strategies.

- #machine-learning, #classification, #multi-class-classification

### Card 2

Diagram illustrating ambiguous regions in multi-class classification.

![](https://cdn.mathpix.com/cropped/2024_05_26_a79f6f03ec68f3fd25e6g-1.jpg?height=664&width=1450&top_left_y=212&top_left_x=152)

%

Describe the solutions depicted for multi-class classification in the left and right diagrams and their potential pitfalls.

%

The left diagram uses a one-versus-the-rest (OvR) approach, where each discriminant function (solid and dashed red lines) separates one class (e.g., $\mathcal{C}_1$, $\mathcal{C}_2$) from all other classes. The green shaded area represents an ambiguous region where classification is uncertain as it does not clearly belong to either class.

The right diagram employs a one-versus-one (OvO) approach, where each discriminant function separates a pair of classes (e.g., $\mathcal{C}_1$ vs $\mathcal{C}_2$, $\mathcal{C}_1$ vs $\mathcal{C}_3$, $\mathcal{C}_2$ vs $\mathcal{C}_3$). The green-shaded center area indicates an ambiguous region where none of the class separators can confidently classify a point.

Both approaches encounter difficulties in clearly resolving points in these intersection regions, thereby illustrating potential pitfalls in constructing multi-class classifiers based on two-class discriminant functions.

- #machine-learning, #classification-strategies, #ambiguity
### Card 1

![](https://cdn.mathpix.com/cropped/2024_05_26_a79f6f03ec68f3fd25e6g-1.jpg?height=664&width=1450&top_left_y=212&top_left_x=152)

Explain the problems encountered when creating a multi-class classifier using a one-versus-the-rest approach as shown on the left side of Figure 5.2.

%

The one-versus-the-rest approach in multi-class classification can lead to ambiguous regions where the classification is uncertain. In the left diagram of Figure 5.2, regions \(R1\), \(R2\), and \(R3\) correspond to classes \(C1\), \(C2\), and not \(C1\) or \(C2\) respectively. The green-shaded area marks the intersection where a point is neither \(C1\) nor \(C2\). This illustrates the difficulty in assigning a clear class, indicating potential uncertainty.

- #machine-learning, #classification, #multi-class-discriminant

### Card 2

![](https://cdn.mathpix.com/cropped/2024_05_26_a79f6f03ec68f3fd25e6g-1.jpg?height=664&width=1450&top_left_y=212&top_left_x=152)

Describe the challenges depicted in the right side of Figure 5.2 when using a one-versus-one approach for multi-class classification.

%

The one-versus-one approach can also result in ambiguous regions. The right diagram in Figure 5.2 shows three discriminant functions separating pairs of classes \(C1\), \(C2\), and \(C3\). The green-shaded area in the center, where decision boundaries intersect, represents regions of ambiguity. Here, the overlapping influences of decision boundaries showcase the potential confusion and difficulty in assigning a definitive class label to the points within these regions.

- #machine-learning, #classification, #decision-boundaries
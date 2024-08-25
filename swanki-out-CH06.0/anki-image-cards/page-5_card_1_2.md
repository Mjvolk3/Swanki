## Anki Cards

### Card 1

![](https://cdn.mathpix.com/cropped/2024_05_26_5c32d245d93af9e68d2cg-1.jpg?height=696&width=723&top_left_y=214&top_left_x=935)

Explain the significance of the plot provided in Figure 6.4 regarding the volume fraction of a hypersphere near its surface as the dimensionality \( D \) increases.

%

The plot illustrates the fraction of the volume of a hypersphere with radius \( r=1 \) that lies in the range from \( r=1-\epsilon \) to \( r=1 \) for various values of dimensionality \( D \). As dimensionality \( D \) increases, and for higher dimensions (such as when \( D=20 \)), even a small \( \epsilon \) results in a large volume fraction near the hypersphere's surface. This effect demonstrates the "curse of dimensionality", where the majority of the volume of high-dimensional spaces is concentrated near the boundaries.

- #geometry, #high-dimensional-spaces, #curse-of-dimensionality

### Card 2

![](https://cdn.mathpix.com/cropped/2024_05_26_5c32d245d93af9e68d2cg-1.jpg?height=696&width=723&top_left_y=214&top_left_x=935)

%Section 6.1.4 Exercise 6.1 states: "Some cells contain no training points. Hence, a test point in such cells cannot be classified. We have no hope of applying such a technique in a space of more than a few variables." How does Figure 6.4 illustrate this difficulty?

%

Figure 6.4 represents the fraction of the volume of a hypersphere with radius \( r=1 \) that lies near its surface for various dimensionalities \( D \). As \( D \) increases, even small radial distances from the surface (small \( \epsilon \)) account for a large fraction of the volume. This illustrates the "curse of dimensionality", where data points become sparse in high-dimensional spaces, leading to many empty cells with no training points. Consequently, it becomes challenging to classify test points in such high-dimensional spaces due to the lack of nearby training points.

- #classification, #curse-of-dimensionality, #high-dimensional-complexity
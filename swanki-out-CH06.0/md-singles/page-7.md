![](https://cdn.mathpix.com/cropped/2024_05_26_0971150439f155ba27cfg-1.jpg?height=508&width=515&top_left_y=215&top_left_x=304)

(a) (b)

Figure 6.6 Illustration of a data set in two dimensions \(\left(x_{1}, x_{2}\right)\) in which data points from the two classes depicted using green and red circles can be separated by a linear decision surface, as seen in (a). If, however, only the variable \(x_{1}\) is measured then the classes are no longer separable, as seen in (b).

sionality. Consider the images shown in Figure 6.7. Each image is a point in a high-dimensional space whose dimensionality is determined by the number of pixels. Because the objects can occur at different vertical and horizontal positions within the image and in different orientations, there are three degrees of freedom of variability between images, and a set of images will, to a first approximation, live on a three-dimensional manifold embedded within the high-dimensional space. Due to the complex relationships between the object position or orientation and the pixel intensities, this manifold will be highly nonlinear.

In fact, the number of pixels is really an artefact of the image generation process since they represent measurements of a continuous world. Capturing the same image at a higher resolution increases the dimensionality \(D\) of the data space without changing the fact that the images still live on a three-dimensional manifold. If we can associate localized basis functions with the data manifold, rather than with the entire high-dimensional data space, we might expect that the number of required basis functions would grow exponentially with the dimensionality of the manifold rather than with the dimensionality of the data space. Since the manifold will typically have a much lower dimensionality than the data space, this represents a huge

Figure 6.7 Examples of images of a handwritten digit that differ in the location of the digit within the images as well as in their orientation. This data lives on a nonlinear threedimensional manifold within the high-dimensional image space.
![](https://cdn.mathpix.com/cropped/2024_05_26_0971150439f155ba27cfg-1.jpg?height=384&width=554&top_left_y=1742&top_left_x=916)

![](https://cdn.mathpix.com/cropped/2024_05_26_0971150439f155ba27cfg-1.jpg?height=371&width=168&top_left_y=1751&top_left_x=1479)
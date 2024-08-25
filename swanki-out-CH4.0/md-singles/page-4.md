
![](https://cdn.mathpix.com/cropped/2024_05_26_e13468588350511df9e7g-1.jpg?height=438&width=1486&top_left_y=234&top_left_x=134)

Figure 4.2 Examples of basis functions, showing polynomials on the left, Gaussians of the form (4.4) in the centre, and sigmoidal basis functions of the form (4.5) on the right.

\section*{Section 4.1.7}

Section 1.2
Yet another possible choice of basis function is the Fourier basis, which leads to an expansion in sinusoidal functions. Each basis function represents a specific frequency and has infinite spatial extent. By contrast, basis functions that are localized to finite regions of input space necessarily comprise a spectrum of different spatial frequencies. In signal processing applications, it is often of interest to consider basis functions that are localized in both space and frequency, leading to a class of functions known as wavelets (Ogden, 1997; Mallat, 1999; Vidakovic, 1999). These are also defined to be mutually orthogonal, to simplify their application. Wavelets are most applicable when the input values live on a regular lattice, such as the successive time points in a temporal sequence or the pixels in an image.

Most of the discussion in this chapter, however, is independent of the choice of basis function set, and so we will not specify the particular form of the basis functions, except for numerical illustration. Furthermore, to keep the notation simple, we will focus on the case of a single target variable \(t\), although we will briefly outline the modifications needed to deal with multiple target variables.

\subsection*{4.1.2 Likelihood function}

We solved the problem of fitting a polynomial function to data by minimizing a sum-of-squares error function, and we also showed that this error function could be motivated as the maximum likelihood solution under an assumed Gaussian noise model. We now return to this discussion and consider the least-squares approach, and its relation to maximum likelihood, in more detail.

As before, we assume that the target variable \(t\) is given by a deterministic function \(y(\mathbf{x}, \mathbf{w})\) with additive Gaussian noise so that

\[
t=y(\mathbf{x}, \mathbf{w})+\epsilon
\]

where \(\epsilon\) is a zero-mean Gaussian random variable with variance \(\sigma^{2}\). Thus, we can write

\[
p\left(t \mid \mathbf{x}, \mathbf{w}, \sigma^{2}\right)=\mathcal{N}\left(t \mid y(\mathbf{x}, \mathbf{w}), \sigma^{2}\right)
\]
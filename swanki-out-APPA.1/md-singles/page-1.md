\title{
Appendix A. Linear Algebra
}

In this appendix, we gather together some useful properties and identities involving matrices and determinants. This is not intended to be an introductory tutorial, and it is assumed that the reader is already familiar with basic linear algebra. For some results, we indicate how to prove them, whereas in more complex cases we leave the interested reader to refer to standard textbooks on the subject. In all cases, we assume that inverses exist and that matrix dimensions are such that the formulae are correctly defined. A comprehensive discussion of linear algebra can be found in Golub and Van Loan (1996), and an extensive collection of matrix properties is given by Lütkepohl (1996). Matrix derivatives are discussed in Magnus and Neudecker \((1999)\).

\section*{A.1. Matrix Identities}

A matrix A has elements \(A_{i j}\) where \(i\) indexes the rows and \(j\) indexes the columns. We use \(\mathbf{I}_{N}\) to denote the \(N \times N\) identity matrix (also called the unit matrix), and if there is no ambiguity over dimensionality, we simply use \(\mathbf{I}\). The transpose matrix \(\mathbf{A}^{\mathrm{T}}\) has elements \(\left(\mathbf{A}^{\mathrm{T}}\right)_{i j}=A_{j i}\). From the definition of a transpose, we have

\[
(\mathbf{A B})^{\mathrm{T}}=\mathbf{B}^{\mathrm{T}} \mathbf{A}^{\mathrm{T}}
\]

which can be verified by writing out the indices. The inverse of \(\mathbf{A}\), denoted \(\mathbf{A}^{-1}\), satisfies

\[
\mathbf{A} \mathbf{A}^{-1}=\mathbf{A}^{-1} \mathbf{A}=\mathbf{I}
\]

![](https://cdn.mathpix.com/cropped/2024_05_27_25fa23d4d21ea443ccefg-1.jpg?height=44&width=544&top_left_y=1888&top_left_x=412)

\[
(\mathbf{A B})^{-1}=\mathbf{B}^{-1} \mathbf{A}^{-1}
\]

Also we have

\[
\left(\mathbf{A}^{\mathrm{T}}\right)^{-1}=\left(\mathbf{A}^{-1}\right)^{\mathrm{T}}
\]
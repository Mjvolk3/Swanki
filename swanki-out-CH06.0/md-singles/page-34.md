to achieve the desired end-effector location, but the average of the two solutions is not itself a solution. In such cases, the conditional mode may be of more value. Because the conditional mode for the mixture density network does not have a simple analytical solution, a numerical iteration is required. A simple alternative is to take the mean of the most probable component (i.e., the one with the largest mixing coefficient) at each value of \(\mathbf{x}\). This is shown for the toy data set in Figure 6.19(d).

\title{
Exercises
}

6.1 \((\star \star \star)\) Use the result (2.126) to derive an expression for the surface area \(S_{D}\) and the volume \(V_{D}\) of a hypersphere of unit radius in \(D\) dimensions. To do this, consider the following result, which is obtained by transforming from Cartesian to polar coordinates:

\[
\prod_{i=1}^{D} \int_{-\infty}^{\infty} e^{-x_{i}^{2}} \mathrm{~d} x_{i}=S_{D} \int_{0}^{\infty} e^{-r^{2}} r^{D-1} \mathrm{~d} r
\]

Using the gamma function, defined by

\[
\Gamma(x)=\int_{0}^{\infty} t^{x-1} e^{-t} \mathrm{~d} t
\]

together with (2.126), evaluate both sides of this equation, and hence show that

\[
S_{D}=\frac{2 \pi^{D / 2}}{\Gamma(D / 2)}
\]

Next, by integrating with respect to the radius from 0 to 1 , show that the volume of the unit hypersphere in \(D\) dimensions is given by

\[
V_{D}=\frac{S_{D}}{D}
\]

Finally, use the results \(\Gamma(1)=1\) and \(\Gamma(3 / 2)=\sqrt{\pi} / 2\) to show that (6.53) and (6.54) reduce to the usual expressions for \(D=2\) and \(D=3\).

6.2 ( \(\star \star \star)\) Consider a hypersphere of radius \(a\) in \(D\) dimensions together with the concentric hypercube of side \(2 a\), so that the hypersphere touches the hypercube at the centres of each of its sides. By using the results of Exercise 6.1, show that the ratio of the volume of the hypersphere to the volume of the cube is given by

\[
\frac{\text { volume of hypersphere }}{\text { volume of cube }}=\frac{\pi^{D / 2}}{D 2^{D-1} \Gamma(D / 2)} \text {. }
\]

Now make use of Stirling's formula in the form

\[
\Gamma(x+1) \simeq(2 \pi)^{1 / 2} e^{-x} x^{x+1 / 2}
\]

which is valid for \(x \gg 1\), to show that, as \(D \rightarrow \infty\), the ratio (6.55) goes to zero. Show also that the distance from the centre of the hypercube to one of the corners
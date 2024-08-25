Figure 5.12 Plot of the logistic sigmoid function \(\sigma(a)\) defined by (5.42), shown in red, together with the scaled probit function \(\Phi(\lambda a)\), for \(\lambda^{2}=\pi / 8\), shown in dashed blue, where \(\Phi(a)\) is defined by (5.86). The scaling factor \(\pi / 8\) is chosen so that the derivatives of the two curves are equal for \(a=0\).

![](https://cdn.mathpix.com/cropped/2024_05_26_ecc13ea52b1adcd44cf9g-1.jpg?height=498&width=726&top_left_y=230&top_left_x=917)

\(\mathcal{C}_{1}\) can be written as

\[
\begin{aligned}
p\left(\mathcal{C}_{1} \mid \mathbf{x}\right) & =\frac{p\left(\mathbf{x} \mid \mathcal{C}_{1}\right) p\left(\mathcal{C}_{1}\right)}{p\left(\mathbf{x} \mid \mathcal{C}_{1}\right) p\left(\mathcal{C}_{1}\right)+p\left(\mathbf{x} \mid \mathcal{C}_{2}\right) p\left(\mathcal{C}_{2}\right)} \\
& =\frac{1}{1+\exp (-a)}=\sigma(a)
\end{aligned}
\]

where we have defined

\[
a=\ln \frac{p\left(\mathbf{x} \mid \mathcal{C}_{1}\right) p\left(\mathcal{C}_{1}\right)}{p\left(\mathbf{x} \mid \mathcal{C}_{2}\right) p\left(\mathcal{C}_{2}\right)}
\]

and \(\sigma(a)\) is the logistic sigmoid function defined by

\[
\sigma(a)=\frac{1}{1+\exp (-a)}
\]

which is plotted in Figure 5.12. The term 'sigmoid' means S-shaped. This type of function is sometimes also called a 'squashing function' because it maps the whole real axis into a finite interval. The logistic sigmoid has been encountered already in earlier chapters and plays an important role in many classification algorithms. It satisfies the following symmetry property:

\[
\sigma(-a)=1-\sigma(a)
\]

as is easily verified. The inverse of the logistic sigmoid is given by

\[
a=\ln \left(\frac{\sigma}{1-\sigma}\right)
\]

and is known as the logit function. It represents the log of the ratio of probabilities \(\ln \left[p\left(\mathcal{C}_{1} \mid \mathbf{x}\right) / p\left(\mathcal{C}_{2} \mid \mathbf{x}\right)\right]\) for the two classes, also known as the log odds.

Note that in (5.40), we have simply rewritten the posterior probabilities in an equivalent form, and so the appearance of the logistic sigmoid may seem artificial.
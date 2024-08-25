\title{
Appendix B. Calculus of Variations
}

We can think of a function \(y(x)\) as being an operator that, for any input value \(x\), returns an output value \(y\). In the same way, we can define a functional \(F[y]\) to be an operator that takes a function \(y(x)\) and returns an output value \(F\). An example of a functional is the length of a curve drawn in a two-dimensional plane in which the path of the curve is defined in terms of a function. In the context of machine learning, a widely used functional is the entropy \(\mathrm{H}[x]\) for a continuous variable \(x\) because, for any choice of probability density function \(p(x)\), it returns a scalar value representing the entropy of \(x\) under that density. Thus, the entropy of \(p(x)\) could equally well have been written as \(\mathrm{H}[p]\).

A common problem in conventional calculus is to find a value of \(x\) that maximizes (or minimizes) a function \(y(x)\). Similarly, in the calculus of variations we seek a function \(y(x)\) that maximizes (or minimizes) a functional \(F[y]\). That is, of all possible functions \(y(x)\), we wish to find the particular function for which the functional \(F[y]\) is a maximum (or minimum). The calculus of variations can be used, for instance, to show that the shortest path between two points is a straight line or that the maximum entropy distribution is a Gaussian.

If we were not familiar with the rules of ordinary calculus, we could evaluate a conventional derivative \(\mathrm{d} y / \mathrm{d} x\) by making a small change \(\epsilon\) to the variable \(x\) and then expanding in powers of \(\epsilon\), so that

\[
y(x+\epsilon)=y(x)+\frac{\mathrm{d} y}{\mathrm{~d} x} \epsilon+\mathcal{O}\left(\epsilon^{2}\right)
\]

and finally taking the limit \(\epsilon \rightarrow 0\). Similarly, for a function of several variables \(y\left(x_{1}, \ldots, x_{D}\right)\), the corresponding partial derivatives are defined by

\[
y\left(x_{1}+\epsilon_{1}, \ldots, x_{D}+\epsilon_{D}\right)=y\left(x_{1}, \ldots, x_{D}\right)+\sum_{i=1}^{D} \frac{\partial y}{\partial x_{i}} \epsilon_{i}+\mathcal{O}\left(\epsilon^{2}\right)
\]

The analogous definition of a functional derivative arises when we consider how much a functional \(F[y]\) changes when we make a small change \(\epsilon \eta(x)\) to the function
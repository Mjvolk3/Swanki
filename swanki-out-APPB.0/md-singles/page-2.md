Figure B. 1 A functional derivative can be defined by considering how the value of a functional \(F[y]\) changes when the function \(y(x)\) is changed to \(y(x)+\epsilon \eta(x)\) where \(\eta(x)\) is an arbitrary function of \(x\).

![](https://cdn.mathpix.com/cropped/2024_05_26_af52565e380fe828a6d7g-1.jpg?height=254&width=500&top_left_y=291&top_left_x=1069)

\(y(x)\), where \(\eta(x)\) is an arbitrary function of \(x\), as illustrated in Figure B.1. We denote the functional derivative of \(F[y]\) with respect to \(y(x)\) by \(\delta F / \delta y(x)\) and define it by the following relation:

\[
F[y(x)+\epsilon \eta(x)]=F[y(x)]+\epsilon \int \frac{\delta F}{\delta y(x)} \eta(x) \mathrm{d} x+\mathcal{O}\left(\epsilon^{2}\right)
\]

This can be seen as a natural extension of (B.2) in which \(F[y]\) now depends on a continuous set of variables, namely the values of \(y\) at all points \(x\). Requiring that the functional be stationary with respect to small variations in the function \(y(x)\) gives

\[
\int \frac{\delta F}{\delta y(x)} \eta(x) \mathrm{d} x=0
\]

Because this must hold for an arbitrary choice of \(\eta(x)\), it follows that the functional derivative must vanish. To see this, imagine choosing a perturbation \(\eta(x)\) that is zero everywhere except in the neighbourhood of a point \(\widehat{x}\), in which case the functional derivative must be zero at \(x=\widehat{x}\). However, because this must be true for every choice of \(\widehat{x}\), the functional derivative must vanish for all values of \(x\).

Consider a functional that is defined by an integral over a function \(G\left(y, y^{\prime}, x\right)\), which depends on both \(y(x)\) and its derivative \(y^{\prime}(x)\) and has a direct dependence on \(x\) :

\[
F[y]=\int G\left(y(x), y^{\prime}(x), x\right) \mathrm{d} x
\]

where the value of \(y(x)\) is assumed to be fixed at the boundary of the region of integration (which might be at infinity). If we now consider variations in the function \(y(x)\), we obtain

\[
F[y(x)+\epsilon \eta(x)]=F[y(x)]+\epsilon \int\left\{\frac{\partial G}{\partial y} \eta(x)+\frac{\partial G}{\partial y^{\prime}} \eta^{\prime}(x)\right\} \mathrm{d} x+\mathcal{O}\left(\epsilon^{2}\right)
\]

We now have to cast this in the form (B.3). To do so, we integrate the second term by parts and note that \(\eta(x)\) must vanish at the boundary of the integral (because \(y(x)\) is fixed at the boundary). This gives

\[
F[y(x)+\epsilon \eta(x)]=F[y(x)]+\epsilon \int\left\{\frac{\partial G}{\partial y}-\frac{\mathrm{d}}{\mathrm{d} x}\left(\frac{\partial G}{\partial y^{\prime}}\right)\right\} \eta(x) \mathrm{d} x+\mathcal{O}\left(\epsilon^{2}\right)
\]
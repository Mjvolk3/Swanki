\title{
Appendix C. Lagrange Multipliers
}

Lagrange multipliers, also sometimes called undetermined multipliers, are used to find the stationary points of a function of several variables subject to one or more constraints.

Consider the problem of finding the maximum of a function $f\left(x_{1}, x_{2}\right)$ subject to a constraint relating $x_{1}$ and $x_{2}$, which we write in the form

$$
g\left(x_{1}, x_{2}\right)=0
$$

One approach would be to solve the constraint equation (C.1) and thus express $x_{2}$ as a function of $x_{1}$ in the form $x_{2}=h\left(x_{1}\right)$. This can then be substituted into $f\left(x_{1}, x_{2}\right)$ to give a function of $x_{1}$ alone of the form $f\left(x_{1}, h\left(x_{1}\right)\right)$. The maximum with respect to $x_{1}$ could then be found by differentiation in the usual way, to give the stationary value $x_{1}^{\star}$, with the corresponding value of $x_{2}$ given by $x_{2}^{\star}=h\left(x_{1}^{\star}\right)$.

One problem with this approach is that it may be difficult to find an analytic solution of the constraint equation that allows $x_{2}$ to be expressed as an explicit function of $x_{1}$. Also, this approach treats $x_{1}$ and $x_{2}$ differently and so spoils the natural symmetry between these variables.

A more elegant, and often simpler, approach introduces a parameter $\lambda$ called a Lagrange multiplier. We shall motivate this technique from a geometrical perspective. Consider a $D$-dimensional variable $\mathbf{x}$ with components $x_{1}, \ldots, x_{D}$. The constraint equation $g(\mathbf{x})=0$ then represents a $(D-1)$-dimensional surface in $\mathbf{x}$-space as indicated in Figure C.1.

First note that at any point on the constraint surface, the gradient $\nabla g(\mathbf{x})$ of the constraint function is orthogonal to the surface. To see this, consider a point $\mathbf{x}$ that lies on the constraint surface along with a nearby point $\mathbf{x}+\boldsymbol{\epsilon}$ that also lies on the surface. If we make a Taylor expansion around $\mathbf{x}$, we have

$$
g(\mathbf{x}+\boldsymbol{\epsilon}) \simeq g(\mathbf{x})+\boldsymbol{\epsilon}^{\mathrm{T}} \nabla g(\mathbf{x})
$$

Because both $\mathbf{x}$ and $\mathbf{x}+\boldsymbol{\epsilon}$ lie on the constraint surface, we have $g(\mathbf{x})=g(\mathbf{x}+\boldsymbol{\epsilon})$ and hence $\boldsymbol{\epsilon}^{\mathrm{T}} \nabla g(\mathbf{x}) \simeq 0$. In the limit $\|\boldsymbol{\epsilon}\| \rightarrow 0$, we have $\boldsymbol{\epsilon}^{\mathrm{T}} \nabla g(\mathbf{x})=0$, and because $\boldsymbol{\epsilon}$ is

Figure C. 1 A geometrical picture of the technique of Lagrange multipliers in which we seek to maximize a function $f(\mathbf{x})$, subject to the constraint $g(\mathbf{x})=0$. If $\mathbf{x}$ is $D$ dimensional, the constraint $g(\mathbf{x})=0$ corresponds to a subspace of dimensionality $D-1$, as indicated by the red curve. The problem can be solved by optimizing the Lagrangian function $L(\mathbf{x}, \lambda)=f(\mathbf{x})+\lambda g(\mathbf{x})$.

![](https://cdn.mathpix.com/cropped/2024_05_26_57d37ae5bb94cf2241e6g-1.jpg?height=509&width=535&top_left_y=212&top_left_x=1110

ChatGPT figure/image summary: The image displays a simple illustration related to the concept of Lagrange multipliers, a mathematical method for finding the maximum or minimum of a function subject to constraints. The image depicts a 2-dimensional closed curve (colored red), representing a constraint surface defined by a function g(x) = 0. On this surface, there's a point labeled "x_A". Two vectors emanate from this point: one labeled "∇f(x)" and the other labeled "∇g(x)". These represent the gradients of two functions at the point "x_A".

The vector ∇g(x) symbolizes the gradient of the constraint function g(x) at the point "x_A", which is orthogonal (at right angles) to the constraint surface at that point. The vector ∇f(x) represents the gradient of the objective function f(x) at "x_A".

In the context of the Lagrange multipliers method, the illustration is demonstrating that at the point on the constraint surface where the function f(x) is at a maximum or minimum, the gradient ∇f(x) will be parallel (or anti-parallel) to the gradient of the constraint function, ∇g(x). This means there must be some scalar λ, the Lagrange multiplier, for which the following holds true:

∇f(x) + λ∇g(x) = 0

The image is a visual aid to help understand the geometrical interpretation of this condition in the optimization process involving constraints. It demonstrates how Lagrange multipliers can be used to find stationary points of a function subject to equality constraints.)

then parallel to the constraint surface $g(\mathbf{x})=0$, we see that the vector $\nabla g$ is normal to the surface.

Next we seek a point $\mathbf{x}^{\star}$ on the constraint surface such that $f(\mathbf{x})$ is maximized. Such a point must have the property that the vector $\nabla f(\mathbf{x})$ is also orthogonal to the constraint surface, as illustrated in Figure C.1, because otherwise we could increase the value of $f(\mathbf{x})$ by moving a short distance along the constraint surface. Thus, $\nabla f$ and $\nabla g$ are parallel (or anti-parallel) vectors, and so there must exist a parameter $\lambda$ such that

$$
\nabla f+\lambda \nabla g=0
$$

where $\lambda \neq 0$ is known as a Lagrange multiplier. Note that $\lambda$ can have either sign.

At this point, it is convenient to introduce the Lagrangian function defined by

$$
L(\mathbf{x}, \lambda) \equiv f(\mathbf{x})+\lambda g(\mathbf{x})
$$

The constrained stationarity condition (C.3) is obtained by setting $\nabla_{\mathbf{x}} L=0$. Furthermore, the condition $\partial L / \partial \lambda=0$ leads to the constraint equation $g(\mathbf{x})=0$.

Thus, to find the maximum of a function $f(\mathbf{x})$ subject to the constraint $g(\mathbf{x})=0$, we define the Lagrangian function given by (C.4) and we then find the stationary point of $L(\mathbf{x}, \lambda)$ with respect to both $\mathbf{x}$ and $\lambda$. For a $D$-dimensional vector $\mathbf{x}$, this gives $D+1$ equations that determine both the stationary point $\mathbf{x}^{\star}$ and the value of $\lambda$. If we are interested only in $\mathbf{x}^{\star}$, then we can eliminate $\lambda$ from the stationarity equations without needing to find its value (hence, the term 'undetermined multiplier').

As a simple example, suppose we wish to find the stationary point of the function $f\left(x_{1}, x_{2}\right)=1-x_{1}^{2}-x_{2}^{2}$ subject to the constraint $g\left(x_{1}, x_{2}\right)=x_{1}+x_{2}-1=0$, as illustrated in Figure C.2. The corresponding Lagrangian function is given by

$$
L(\mathbf{x}, \lambda)=1-x_{1}^{2}-x_{2}^{2}+\lambda\left(x_{1}+x_{2}-1\right)
$$

The conditions for this Lagrangian to be stationary with respect to $x_{1}, x_{2}$, and $\lambda$ give the following coupled equations:

$$
\begin{aligned}
-2 x_{1}+\lambda & =0 \\
-2 x_{2}+\lambda & =0 \\
x_{1}+x_{2}-1 & =0
\end{aligned}
$$

Figure C. 2 A simple example of the use of Lagrange multipliers in which the aim is to maximize $f\left(x_{1}, x_{2}\right)=1-$ $x_{1}^{2}-x_{2}^{2}$ subject to the constraint $g\left(x_{1}, x_{2}\right)=0$ where $g\left(x_{1}, x_{2}\right)=x_{1}+x_{2}-1$. The circles show contours of the function $f\left(x_{1}, x_{2}\right)$, and the diagonal line shows the constraint surface $g\left(x_{1}, x_{2}\right)=0$.

![](https://cdn.mathpix.com/cropped/2024_05_26_ffad232c340143af6219g-1.jpg?height=469&width=515&top_left_y=212&top_left_x=1130

ChatGPT figure/image summary: The image provided is a mathematical diagram illustrating an example of using Lagrange multipliers. This is a two-dimensional graph with x1 as the horizontal axis and x2 as the vertical axis. It depicts several circular contours represented by concentric blue circles, which are level curves of a function f(x1, x2). The function f(x1, x2) is given in the paper as \( f(x_{1}, x_{2}) = 1 - x_{1}^{2} - x_{2}^{2} \).

The red line represents a constraint surface described by the equation \( g(x_{1}, x_{2}) = x_{1} + x_{2} - 1 = 0 \). This straight line crosses through the origin of the graph and forms a diagonal cutting across the circular contours.

At the intersection of the blue contour, which is locus of points giving the same value of the function f(x1, x2), and the red constraint line g(x1, x2) = 0, we have a black point. This point, labeled \( (x_{1}^{*}, x_{2}^{*}) \), represents the optimal solution—i.e., the stationary point under the constraint g(x1, x2) = 0—where the function f(x1, x2) reaches its maximum value given the constraint.

The image serves to aid in visualization of the concepts described in the paper and helps to illustrate the geometric interpretation of the Lagrange multiplier method when locating a maximum of a function subject to a constraint.)

Solving these equations then gives the stationary point as $\left(x_{1}^{\star}, x_{2}^{\star}\right)=(1 / 2,1 / 2)$, and the corresponding value for the Lagrange multiplier is $\lambda=1$.

So far, we have considered the problem of maximizing a function subject to an equality constraint of the form $g(\mathbf{x})=0$. We now consider the problem of maximizing $f(\mathbf{x})$ subject to an inequality constraint of the form $g(\mathbf{x}) \geqslant 0$, as illustrated in Figure C.3.

There are now two kinds of solution possible, according to whether the constrained stationary point lies in the region where $g(\mathbf{x})>0$, in which case the constraint is inactive, or whether it lies on the boundary $g(\mathbf{x})=0$, in which case the constraint is said to be active. In the former case, the function $g(\mathbf{x})$ plays no role and so the stationary condition is simply $\nabla f(\mathbf{x})=0$. This again corresponds to a stationary point of the Lagrange function (C.4) but this time with $\lambda=0$. The latter case, where the solution lies on the boundary, is analogous to the equality constraint discussed previously and corresponds to a stationary point of the Lagrange function (C.4) with $\lambda \neq 0$. Now, however, the sign of the Lagrange multiplier is crucial, because the function $f(\mathbf{x})$ is at a maximum only if its gradient is oriented away from the region $g(\mathbf{x})>0$, as illustrated in Figure C.3. We therefore have $\nabla f(\mathbf{x})=-\lambda \nabla g(\mathbf{x})$ for some value of $\lambda>0$.

For either of these two cases, the product $\lambda g(\mathbf{x})=0$. Thus, the solution to

Figure C. 3 Illustration of the problem of maximizing $f(\mathbf{x})$ subject to the inequality constraint $g(\mathbf{x}) \geqslant 0$.

![](https://cdn.mathpix.com/cropped/2024_05_26_ffad232c340143af6219g-1.jpg?height=511&width=611&top_left_y=1591&top_left_x=1033

ChatGPT figure/image summary: The image provided here appears to illustrate the concept of maximizing a function \( f(\mathbf{x}) \) subject to an inequality constraint \( g(\mathbf{x}) \geqslant 0 \) using Lagrange multipliers. It is likely related to Figure C.3 in the text, showing an area (highlighted in light brown/tan color) where \( g(x) > 0 \), indicating a feasible region defined by the inequality constraint. The function \( g(x) = 0 \) is represented by a black curve that marks the boundary of this feasible region.

Within this region, we see two points, labeled \( x_A \) and \( x_B \). At point \( x_A \), which lies on the boundary \( g(x) = 0 \), we see a vector \( \nabla f(x) \) pointing outwards, which represents the gradient of the function \( f(\mathbf{x}) \). Another vector \( \nabla g(x) \) is depicted at some location in the feasible region, and this vector is orthogonal to the boundary curve \( g(x) = 0 \), representing the gradient of the constraint function \( g(\mathbf{x}) \).

According to Lagrange multiplier theory, the maximum of the function occurs when the gradient \( \nabla f(x) \) is oriented away from the region where \( g(x) > 0 \) and is equal to \( -\lambda \nabla g(x) \) where \( \lambda > 0 \). The image is a graphical representation of this condition and is a common illustrative technique in optimization and calculus topics dealing with constrained optimization problems.)

the problem of maximizing $f(\mathbf{x})$ subject to $g(\mathbf{x}) \geqslant 0$ is obtained by optimizing the Lagrange function (C.4) with respect to $\mathrm{x}$ and $\lambda$ subject to the conditions

$$
\begin{aligned}
g(\mathbf{x}) & \geqslant 0 \\
\lambda & \geqslant 0 \\
\lambda g(\mathbf{x}) & =0
\end{aligned}
$$

These are known as the Karush-Kuhn-Tucker (KKT) conditions (Karush, 1939; Kuhn and Tucker, 1951).

Note that if we wish to minimize (rather than maximize) the function $f(\mathbf{x})$ subject to an inequality constraint $g(\mathbf{x}) \geqslant 0$, then we minimize the Lagrangian function $L(\mathbf{x}, \lambda)=f(\mathbf{x})-\lambda g(\mathbf{x})$ with respect to $\mathbf{x}$, again subject to $\lambda \geqslant 0$.

Finally, it is straightforward to extend the technique of Lagrange multipliers to cases with multiple equality and inequality constraints. Suppose we wish to maximize $f(\mathbf{x})$ subject to $g_{j}(\mathbf{x})=0$ for $j=1, \ldots, J$, and $h_{k}(\mathbf{x}) \geqslant 0$ for $k=1, \ldots, K$. We then introduce Lagrange multipliers $\left\{\lambda_{j}\right\}$ and $\left\{\mu_{k}\right\}$, and then optimize the Lagrangian function given by

$$
L\left(\mathbf{x},\left\{\lambda_{j}\right\},\left\{\mu_{k}\right\}\right)=f(\mathbf{x})+\sum_{j=1}^{J} \lambda_{j} g_{j}(\mathbf{x})+\sum_{k=1}^{K} \mu_{k} h_{k}(\mathbf{x})
$$

subject to $\mu_{k} \geqslant 0$ and $\mu_{k} h_{k}(\mathbf{x})=0$ for $k=1, \ldots, K$. Extensions to constrained functional derivatives are similarly straightforward. For a more detailed discussion of the technique of Lagrange multipliers, see Nocedal and Wright (1999).


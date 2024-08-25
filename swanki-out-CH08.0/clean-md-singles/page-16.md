\title{
8. BACKPROPAGATION
}

Figure 8.5 Extension of the example shown in Figure 8.4 to a function with two outputs $f_{1}$ and $f_{2}$.

![](https://cdn.mathpix.com/cropped/2024_05_26_4388dae6329660fd2fabg-1.jpg?height=300&width=785&top_left_y=226&top_left_x=858)

equations (8.50) to (8.56), we obtain the following evaluation trace equations for the tangent variables

$$
\begin{aligned}
& \dot{v}_{1}=1 \\
& \dot{v}_{2}=0 \\
& \dot{v}_{3}=v_{1} \dot{v}_{2}+\dot{v}_{1} v_{2} \\
& \dot{v}_{4}=\dot{v}_{2} \cos \left(v_{2}\right) \\
& \dot{v}_{5}=\dot{v}_{3} \exp \left(v_{3}\right) \\
& \dot{v}_{6}=\dot{v}_{3}-\dot{v}_{4} \\
& \dot{v}_{7}=\dot{v}_{5}+\dot{v}_{6}
\end{aligned}
$$

We can summarize automatic differentiation for this example as follows. We first write code to implement the evaluation of the primal variables, given by (8.50) to (8.56). The associated equations and corresponding code for evaluating the tangent variables (8.58) to (8.64) are generated automatically. To evaluate the derivative $\partial f / \partial x_{1}$, we input specific values of $x_{1}$ and $x_{2}$ and the code then executes the primal

\section*{Exercise 8.17} and tangent equations, numerically evaluating the tuples $\left(v_{i}, \dot{v}_{i}\right)$ in sequence until we obtain $\dot{v}_{5}$, which is the required derivative.

Now consider an example with two outputs $f_{1}\left(x_{1}, x_{2}\right)$ and $f_{2}\left(x_{1}, x_{2}\right)$ where $f_{1}\left(x_{1}, x_{2}\right)$ is defined by (8.49) and

$$
f_{2}\left(x_{1}, x_{2}\right)=\left(x_{1} x_{2}-\sin \left(x_{2}\right)\right) \exp \left(x_{1} x_{2}\right)
$$

as illustrated by the evaluation trace diagram in Figure 8.5. We see that this involves only a small extension to the evaluation equations for the primal and tangent variables, and so both $\partial f_{1} / \partial x_{1}$ and $\partial f_{2} / \partial x_{1}$ can be evaluated together in a single forward pass. The downside, however, is that if we wish to evaluate derivatives with respect to a different input variable $x_{2}$ then we have to run a separate forward pass. In general, if we have a function with $D$ inputs and $K$ outputs then a single pass of forward-mode automatic differentiation produces a single column of the $K \times D$ Jacobian matrix:

$$
\mathbf{J}=\left[\begin{array}{ccc}
\frac{\partial f_{1}}{\partial x_{1}} & \cdots & \frac{\partial f_{1}}{\partial x_{D}} \\
\vdots & \ddots & \vdots \\
\frac{\partial f_{K}}{\partial x_{1}} & \cdots & \frac{\partial f_{K}}{\partial x_{D}}
\end{array}\right]
$$
## Explain how the tangent variables $\dot{v}_i$ are evaluated in terms of $x_1$ and $x_2$.

To evaluate the tangent variables in a function with two outputs, we input specific values for $x_1$ and $x_2$. Let's detail how the tangent variables are computed:

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

By numerically evaluating the tuples $\left(v_{i}, \dot{v}_{i}\right)$, we obtain $\dot{v}_{5}$, which is the required derivative.


- #differentiation, #tangents

## Describe the modified evaluation for the function with two outputs $f_1$ and $f_2$.

When the function has two outputs $f_1\left(x_1, x_2\right)$ and $f_2\left(x_1, x_2\right)$, the evaluation equations for the primal and tangent variables are extended. For $f_2$, given by:

$$
f_{2}\left(x_{1}, x_{2}\right)=\left(x_{1} x_{2}-\sin \left(x_{2}\right)\right) \exp \left(x_{1} x_{2}\right)
$$

The same forward pass can be used to compute both $\partial f_{1} / \partial x_{1}$ and $\partial f_{2} / \partial x_{1}$. However, to evaluate derivatives with respect to a different variable $x_{2}$, a new forward pass is required.


- #calculus, #differentiation

## What does a single pass of forward-mode automatic differentiation produce for a function with $D$ inputs and $K$ outputs?

For a function with $D$ inputs and $K$ outputs, a single pass of forward-mode automatic differentiation produces a single column of the $K \times D$ Jacobian matrix:

$$
\mathbf{J}=\left[\begin{array}{ccc}
\frac{\partial f_{1}}{\partial x_{1}} & \cdots & \frac{\partial f_{1}}{\partial x_{D}} \\
\vdots & \ddots & \vdots \\
\frac{\partial f_{K}}{\partial x_{1}} & \cdots & \frac{\partial f_{K}}{\partial x_{D}}
\end{array}\right]
$$

Each forward pass calculates one column referring to derivatives with respect to a specific input variable.


- #differentiation, #jacobian

## How is the derivative $\partial f / \partial x_{1}$ evaluated?

To evaluate the derivative $\partial f / \partial x_{1}$, specific values for $x_1$ and $x_2$ are input into the code. The code then executes the evaluation of both primal and tangent equations to numerically compute the derivative by tracing tuples $\left(v_{i}, \dot{v}_{i}\right)$ until obtaining $\dot{v}_{5}$.


- #differentiation, #derivatives


## What is $\dot{v}_3$ in terms of $\dot{v}_{1}$ and $\dot{v}_{2}$?

The tangent variable $\dot{v}_3$ is defined as:

$$
\dot{v}_{3} = v_{1} \dot{v}_{2} + \dot{v}_{1} v_{2}
$$

Where $v_{1}$ and $v_{2}$ are primal variables and $\dot{v}_{1}$, $\dot{v}_{2}$ are tangent variables.


- #differentiation, #tangents

## In forward-mode automatic differentiation, why must a separate forward pass be run to evaluate derivatives with respect to different input variables?

In forward-mode automatic differentiation, a separate forward pass must be run to evaluate derivatives with respect to different input variables because each forward pass computes only one column of the Jacobian matrix. To fill all columns (each corresponding to different input variables), each pass needs specific values, thus requiring individual execution.

- #differentiation, #jacobian


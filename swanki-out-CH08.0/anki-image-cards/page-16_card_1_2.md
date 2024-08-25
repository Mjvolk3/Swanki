```markdown
## Computation graph for a function with two outputs

![](https://cdn.mathpix.com/cropped/2024_05_26_4388dae6329660fd2fabg-1.jpg?height=300&width=785&top_left_y=226&top_left_x=858)

What does the computational graph in the image represent?

%

The computational graph in the image represents the sequence of operations for a function with two outputs, $f_{1}$ and $f_{2}$, based on two input variables, $x_{1}$ and $x_{2}$. The intermediate variables are computed as follows:

\begin{align*}
v_{1} &= x_{1} \\
v_{2} &= x_{2} \\
v_{3} &= v_{1}v_{2} \\
v_{4} &= \sin(v_{2}) \\
v_{5} &= \exp(v_{3}) \\
v_{6} &= v_{3} - v_{4} \\
v_{7} &= v_{5} + v_{6} \quad \text{(corresponds to output } f_{1}) \\
v_{8} &= v_{5}v_{6} \quad \text{(corresponds to output } f_{2})
\end{align*}

The edges between the nodes indicate the flow of input values $x_{1}$ and $x_{2}$ through various operations, ultimately leading to the function outputs $f_{1}$ and $f_{2}$. This graph can be used for evaluating the function and its derivatives using automatic differentiation algorithms.

- #machine-learning, #algorithms, #computation-graph

---

## Automatic differentiation in computational graphs

![](https://cdn.mathpix.com/cropped/2024_05_26_4388dae6329660fd2fabg-1.jpg?height=300&width=785&top_left_y=226&top_left_x=858)

How are the tangent variables $\dot{v}_{i}$ evaluated in automatic differentiation for the given computational graph?

%

The tangent variables $\dot{v}_{i}$ are evaluated using the following sequential equations derived from the computational graph:

\begin{aligned}
& \dot{v}_{1}=1 \\
& \dot{v}_{2}=0 \\
& \dot{v}_{3}=v_{1} \dot{v}_{2}+\dot{v}_{1} v_{2} \\
& \dot{v}_{4}=\dot{v}_{2} \cos(v_{2}) \\
& \dot{v}_{5}=\dot{v}_{3} \exp(v_{3}) \\
& \dot{v}_{6}=\dot{v}_{3} - \dot{v}_{4} \\
& \dot{v}_{7}=\dot{v}_{5} + \dot{v}_{6}
\end{aligned}

To evaluate the derivative $\partial f / \partial x_{1}$, specific values of $x_{1}$ and $x_{2}$ are used as inputs, and the code executes both the primal and tangent equations, numerically updating the tuples $(v_{i}, \dot{v}_{i})$ sequentially until obtaining $\dot{v}_{5}$, which is the required derivative.

- #machine-learning, #algorithms, #automatic-differentiation
```

## Understanding the Evaluation Trace

What is represented by each node and edge in the computational graph for the function with two outputs $f_{1}$ and $f_{2}$ shown in the image?

![](https://cdn.mathpix.com/cropped/2024_05_26_4388dae6329660fd2fabg-1.jpg?height=300&width=785&top_left_y=226&top_left_x=858)

%

The nodes represent intermediate variables $v_i$ or outputs $f_i$, and the edges represent the flow of computation. Specifically:

- $ v_1 = x_1 $
- $ v_2 = x_2 $
- $ v_3 = v_1 v_2 $
- $ v_4 = \sin(v_2) $
- $ v_5 = \exp(v_3) $
- $ v_6 = v_3 - v_4 $
- $ v_7 = v_5 + v_6 $ (output $f_1$)
- $ v_8 = v_5 v_6 $ (output $f_2$)

The graph helps in both function evaluation and derivative calculation using automatic differentiation.

- #machine-learning, #backpropagation, #computational-graph

---

## Automatic Differentiation

How is the derivative $\partial f / \partial x_1$ evaluated in the context of the given computational graph for functions $f_1$ and $f_2$?

![](https://cdn.mathpix.com/cropped/2024_05_26_4388dae6329660fd2fabg-1.jpg?height=300&width=785&top_left_y=226&top_left_x=858)

%

The derivative $\partial f / \partial x_1$ is evaluated by executing the primal equations (based on the forward mode of automatic differentiation) and then sequentially computing the tangent variables $\dot{v_i}$ as follows:

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

The derivative $\dot{v}_5$ is numerically evaluated as the final result after processing these tangent variables.

- #machine-learning, #backpropagation, #automatic-differentiation
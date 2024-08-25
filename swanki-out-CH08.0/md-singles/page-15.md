Figure 8.4 Evaluation trace diagram showing the steps involved in the numerical evaluation of the function (8.49) using the primal equations \((8.50)\) to ( 8.56\()\).

![](https://cdn.mathpix.com/cropped/2024_05_26_ff30764196e5f01f8d35g-1.jpg?height=303&width=769&top_left_y=227&top_left_x=876)

automatically by the software environment. Instead of simply doing forward propagation to compute \(\left\{z_{i}\right\}\), the code now propagates tuples \(\left(z_{i}, \dot{z}_{i}\right)\) so that variables and derivatives are evaluated in parallel. The original function is generally defined in terms of elementary operators consisting of arithmetic operations and negation as well as transcendental functions such as exponential, logarithm, and trigonometric functions, all of which have simple formulae for their derivatives. Using these derivatives in combination with the chain rule of calculus allows the code used to evaluate gradients to be constructed automatically.

As an example, consider the following function, which has two input variables:

\[
f\left(x_{1}, x_{2}\right)=x_{1} x_{2}+\exp \left(x_{1} x_{2}\right)-\sin \left(x_{2}\right)
\]

When implemented in software, the code consists of a sequence of operations that can be expressed as an evaluation trace of the underlying elementary operations. This trace can be visualized in the form of a graph, as shown in Figure 8.4. Here we have defined the following primal variables

\[
\begin{aligned}
& v_{1}=x_{1} \\
& v_{2}=x_{2} \\
& v_{3}=v_{1} v_{2} \\
& v_{4}=\sin \left(v_{2}\right) \\
& v_{5}=\exp \left(v_{3}\right) \\
& v_{6}=v_{3}-v_{4} \\
& v_{7}=v_{5}+v_{6}
\end{aligned}
\]

Now suppose we wish to evaluate the derivative \(\partial f / \partial x_{1}\). We define the tangent variables by \(\dot{v}_{i}=\partial v_{i} / \partial x_{1}\). Expressions for evaluating these can be constructed automatically using the chain rule of calculus:

\[
\dot{v}_{i}=\frac{\partial v_{i}}{\partial x_{1}}=\sum_{j \in \mathrm{pa}(i)} \frac{\partial v_{j}}{\partial x_{1}} \frac{\partial v_{i}}{\partial v_{j}}=\sum_{j \in \mathrm{pa}(i)} \dot{v}_{j} \frac{\partial v_{i}}{\partial v_{j}}
\]

where \(\mathrm{pa}(i)\) denotes the set of parents of the node \(i\) in the evaluation trace diagram, that is the set of variables with arrows pointing to node \(i\). For example, in Figure 8.4 the parents of node \(v_{3}\) are nodes \(v_{1}\) and \(v_{2}\). Applying (8.57) to the evaluation trace
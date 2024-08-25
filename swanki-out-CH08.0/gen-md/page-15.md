```markdown
## Explain how the derivative of the function $f\left(x_{1}, x_{2}\right)$ can be evaluated via automatic differentiation, and outline the expression derived for $\dot{v}_{i}$.

In automatic differentiation, the code propagates tuples $(z_{i}, \dot{z}_{i})$ to evaluate variables and their derivatives in parallel. The derivative chain rule is used to automate the construction of gradient evaluation code. For a function such as

$$
f\left(x_{1}, x_{2}\right)=x_{1} x_{2}+\exp \left(x_{1} x_{2}\right)-\sin \left(x_{2}\right)
$$

we use primal ($v_i$) and tangent variables ($\dot{v}_i$). The expression for $\dot{v}_{i}$ based on the chain rule is:

$$
\dot{v}_{i}=\frac{\partial v_{i}}{\partial x_{1}}=\sum_{j \in \mathrm{pa}(i)} \frac{\partial v_{j}}{\partial x_{1}} \frac{\partial v_{i}}{\partial v_{j}}=\sum_{j \in \mathrm{pa}(i)} \dot{v}_{j} \frac{\partial v_{i}}{\partial v_{j}}
$$

where $\mathrm{pa}(i)$ denotes the set of parent nodes of $i$.

- #mathematics.#differential-calculus.#automatic-differentiation, #mathematics.calculus.chain-rule
```

```markdown
## Define the primal variables for the function $f(x_1,x_2) = x_1 x_2 + \exp(x_1 x_2) - \sin(x_2)$ in the context of Figure 8.4 and the evaluation trace.

For the function

$$
f\left(x_{1}, x_{2}\right)=x_{1} x_{2}+\exp \left(x_{1} x_{2}\right)-\sin \left(x_{2}\right)
$$

the primal variables $v_i$ are defined as follows:

$$
\begin{aligned}
& v_{1}=x_{1} \\
& v_{2}=x_{2} \\
& v_{3}=v_{1} v_{2} \\
& v_{4}=\sin \left(v_{2}\right) \\
& v_{5}=\exp \left(v_{3}\right) \\
& v_{6}=v_{3}-v_{4} \\
& v_{7}=v_{5}+v_{6}
\end{aligned}
$$

- #mathematics.#numerical-equations.#primal-variables, #computation.software
```

```markdown
## Using the chain rule, write the expression for the tangent variables $\dot{v}_{3}$ and $\dot{v}_{5}$ with respect to $x_1$ given the primal variables $v_3 = v_1 v_2$ and $v_5 = \exp(v_3)$.

Using the chain rule to derive expressions for the tangent variables $\dot{v}_3$ and $\dot{v}_5$ we start with:

$$
v_{3}=v_{1} v_{2} \Rightarrow \dot{v}_{3} =  \frac{\partial v_{3}}{\partial x_{1}} = v_{2} + v_{1} \cdot 0 = v_{2}
$$

$$
v_{5}=\exp \left(v_{3}\right) \Rightarrow \dot{v}_{5} = \frac{\partial v_5}{\partial x_1} =  \frac{\partial v_5}{\partial v_{3}} \frac{\partial v_{3}}{\partial x_1} = \exp \left(v_{3}\right) \cdot v_{2}
$$

- #mathematics.#differential-calculus.#chain-rule, #computation.automatic-differentiation
```

```markdown
## Derive the expression for $\partial f / \partial x_{1}$ for $f\left(x_{1}, x_{2}\right)=x_{1} x_{2}+\exp \left(x_{1} x_{2}\right)-\sin \left(x_{2}\right)$ using the evaluation trace and tangent variables.

To evaluate $\partial f / \partial x_{1}$, we use:

$$
\dot{v}_{7} = \frac{\partial v_{7}}{\partial v_{5}} \dot{v}_{5} + \frac{\partial v_{7}}{\partial v_{6}} \dot{v}_{6}
$$

Given,

$$
\begin{aligned}
&\dot{v}_{3} = v_{2} \\
&\dot{v}_{5} = \exp(v_{3}) \cdot v_{2} \\
&\dot{v}_{6} = \dot{v}_{3} - \dot{v}_{4} = v_{2} - \cos(v_{2}) \cdot 0 = v_{2} \\
&\dot{v}_{7} = \exp(v_{3}) \cdot v_{2} + v_{2}
\end{aligned}
$$

- #mathematics.#derivative-calculus.#function-derivatives, #differentiation.calculus
```

```markdown
## Explain the significance of the set $\mathrm{pa}(i)$ in the context of evaluating $\dot{v}_{i}$ using the chain rule.

The set $\mathrm{pa}(i)$ denotes the parents of node $i$ in the evaluation trace diagram, i.e., the set of variables with arrows pointing to node $i$. Using $\mathrm{pa}(i)$, we express $\dot{v}_{i}$ via the chain rule:

$$
\dot{v}_{i} = \sum_{j \in \mathrm{pa}(i)} \dot{v}_{j} \frac{\partial v_{i}}{\partial v_{j}}
$$

The parents of a node inform the summation and derivative structure in automatic differentiation.

- #mathematics.#automatic-differentiation.#evaluation-trace, #differential-calculus.chain-rule
```

```markdown
## Compute $\dot{v}_{6}$ for the function $f\left(x_{1}, x_{2}\right) = x_{1} x_{2} + \exp \left(x_{1} x_{2}\right) - \sin \left(x_{2}\right)$ using the defined primal and tangent variables.

Given:

$$
v_6 = v_3 - v_4 \,  \Rightarrow  \dot{v}_6 = \frac{\partial v_6}{\partial x_1}
$$

we know:

$$
\begin{aligned}
&v_3 = v_1 v_2 \Rightarrow \dot{v}_3 = v_2 \\
&v_4 = \sin(v_2) \Rightarrow \dot{v}_4 = \cos(v_2) \cdot 0 = 0 \\
\end{aligned}
$$

Therefore, 

$$
\dot{v}_{6} = \dot{v}_{3} - \dot{v}_{4} = v_{2} - 0 = v_{2}
$$

- #mathematics.#derivatives.#compute, #calculus.tangent-variables
```
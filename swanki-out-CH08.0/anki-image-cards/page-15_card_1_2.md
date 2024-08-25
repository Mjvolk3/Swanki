### Card 1

![](https://cdn.mathpix.com/cropped/2024_05_26_ff30764196e5f01f8d35g-1.jpg?height=303&width=769&top_left_y=227&top_left_x=876)

Explain the steps involved in the numerical evaluation of the function as shown in the figure.

% 

Figure 8.4 displays an evaluation trace diagram for the numerical evaluation of a function using the primal equations $(8.50)$ to $(8.56)$. The diagram represents the computational steps by showing nodes for each intermediate variable calculation and arrows indicating dependencies. The nodes include:

- \( v_1 \) and \( v_2 \) (inputs \( x_1 \) and \( x_2 \)),
- \( v_3 \) (multiplication of \( v_1 \) and \( v_2 \): \( v_1 v_2 \)),
- \( v_4 \) (sine of \( v_2 \): \( \sin(v_2) \)),
- \( v_5 \) (exponential of \( v_3 \): \( \exp(v_3) \)),
- \( v_6 \) (subtraction: \( v_3 - v_4 \)),
- \( v_7 \) (addition: \( v_5 + v_6 \)) leading to the final function output.

This diagram is used in forward-mode automatic differentiation, where variables and their derivatives are propagated in parallel.

- auto-generated.gradient, #differentiation.automatic, #numerics.evaluation

### Card 2

![](https://cdn.mathpix.com/cropped/2024_05_26_ff30764196e5f01f8d35g-1.jpg?height=303&width=769&top_left_y=227&top_left_x=876)

What key features make this diagram useful for forward-mode automatic differentiation?

%

The evaluation trace diagram shows key features essential for forward-mode automatic differentiation, including nodes representing intermediate variables and their computations, as well as arrows depicting the flow of dependencies. Besides merely showing forward propagation for variable computation $(\left\{z_{i}\right\})$, the diagram also illustrates the concurrent propagation of tuples $(z_{i}, \dot{z}_{i})$ for simultaneous evaluation of variables and their derivatives. The elementary operators and their simple derivative formulas combined with the chain rule allow automatic generation and evaluation of gradients alongside primal variable computations.

- #automatic-differentiation.forward-mode, #chain-rule.gradient-calculation, #numerics.evaluation


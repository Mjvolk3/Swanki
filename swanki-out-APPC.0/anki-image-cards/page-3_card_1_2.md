## Generating Anki Cards. Card 1 and Card 2.

### Card 1

![](https://cdn.mathpix.com/cropped/2024_05_26_ffad232c340143af6219g-1.jpg?height=469&width=515&top_left_y=212&top_left_x=1130)

What is the objective function \( f(x_{1}, x_{2}) \) and its constraint in the given diagram, and where is the stationary point?

%

The objective function is:

$$ f(x_{1}, x_{2}) = 1 - x_{1}^{2} - x_{2}^{2} $$

The constraint is:

$$ g(x_{1}, x_{2}) = x_{1} + x_{2} - 1 = 0 $$

The stationary point is at:

$$ (x_{1}^{\star}, x_{2}^{\star}) = \left( \frac{1}{2}, \frac{1}{2} \right) $$

with the corresponding value for the Lagrange multiplier being \( \lambda = 1 \).

- #mathematics, #optimization.langrange-multipliers
- #calculus.constraints

### Card 2

![](https://cdn.mathpix.com/cropped/2024_05_26_ffad232c340143af6219g-1.jpg?height=469&width=515&top_left_y=212&top_left_x=1130)

Explain the difference between equality and inequality constraints in optimization problems. 

%

When maximizing a function subject to constraints, there are two types:

1. **Equality Constraint**: This is of the form \( g(\mathbf{x}) = 0 \). The constraint must be exactly satisfied. In the diagram, this is shown by the red constraint line \( g(x_{1}, x_{2}) = x_{1} + x_{2} - 1 = 0 \).

2. **Inequality Constraint**: This is of the form \( g(\mathbf{x}) \geqslant 0 \). The constraint allows for a range of values where the function is feasible. The stationary point lies either within the feasible region (\( g(\mathbf{x}) > 0 \)) making the constraint inactive, or exactly on the boundary (\( g(\mathbf{x}) = 0 \)) making it active.

- #mathematics, #optimization.constraints
- #calculus.equality-vs-inequality
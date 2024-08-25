Section: Introduction to Lagrange Multipliers

Lagrange multipliers, also known as undetermined multipliers, offer a powerful method to find the stationary points of a function with multiple variables while adhering to one or more constraints. This technique is especially useful in optimization problems where we need to maximize or minimize a function subject to specific conditions.

To illustrate, imagine we are tasked with finding the maximum of a function of two variables, which we'll call f of x1 and x2, subject to a constraint that relates these two variables. We express this constraint as g of x1 and x2 equals zero. One straightforward approach might involve solving this constraint equation to express x2 as a function of x1. Substituting this back into the original function transforms it into a function of x1 alone, allowing us to find the maximum by differentiating with respect to x1. However, this method can be cumbersome and may disrupt the natural symmetry between the variables x1 and x2.

A more elegant solution introduces a parameter called a Lagrange multiplier, denoted by lambda. This technique can be motivated from a geometrical perspective. Consider a variable with multiple dimensions, represented as vector x, with components ranging from x1 to xD. The constraint equation g of x equals zero describes a surface in this multi-dimensional space. At any point on this constraint surface, the gradient of the constraint function, denoted as the gradient of g of x, is orthogonal to the surface. This orthogonality is due to the fact that any small movement along the surface does not change the value of g, implying that the gradient must be perpendicular to the surface.

Section: Finding the Maximum with Lagrange Multipliers

Next, we seek a point on the constraint surface where the function f of x is maximized. At this point, the gradient of f, denoted as the gradient of f of x, must also be orthogonal to the constraint surface. If it weren't, we could move along the surface to increase the value of f, contradicting the assumption that we are at a maximum. Thus, the gradients of f and g are parallel or anti-parallel, meaning there exists a parameter lambda such that the gradient of f plus lambda times the gradient of g equals zero. This parameter lambda is the Lagrange multiplier.

We can conveniently define a new function called the Lagrangian, denoted as L of x and lambda, which is the sum of the original function f of x and lambda times the constraint function g of x. The condition for constrained stationarity is obtained by setting the gradient of L with respect to x to zero. Additionally, setting the partial derivative of L with respect to lambda to zero gives us the constraint equation g of x equals zero.

To find the maximum of f of x subject to the constraint g of x equals zero, we define the Lagrangian and find its stationary point with respect to both x and lambda. For a multi-dimensional vector x, this gives us one more equation than the number of dimensions to solve for the stationary point x-star and the value of lambda. If we're only interested in the stationary point, we can eliminate lambda from the stationarity equations, hence the term 'undetermined multiplier'.

Section: Example and Extension to Inequality Constraints

Consider a simple example where we want to find the stationary point of the function f of x1 and x2 equals one minus x1 squared minus x2 squared, subject to the constraint g of x1 and x2 equals x1 plus x2 minus one equals zero. The corresponding Lagrangian function is L of x and lambda equals one minus x1 squared minus x2 squared plus lambda times x1 plus x2 minus one. Setting the conditions for this Lagrangian to be stationary with respect to x1, x2, and lambda gives us a set of coupled equations. Solving these equations yields the stationary point x1-star and x2-star equals one-half, one-half, with the Lagrange multiplier lambda equal to one.

Now, let's extend our discussion to inequality constraints. Suppose we want to maximize f of x subject to an inequality constraint g of x greater than or equal to zero. There are two possible types of solutions: one where the constrained stationary point lies within the region where g of x is greater than zero, and another where it lies on the boundary where g of x equals zero. In the former case, the constraint is inactive, and the stationary condition is simply the gradient of f of x equals zero. This corresponds to a stationary point of the Lagrangian function with lambda equal to zero. In the latter case, the constraint is active, and the solution lies on the boundary, analogous to the equality constraint scenario, with lambda not equal to zero.

The sign of the Lagrange multiplier matters here because the function f of x is at a maximum only if its gradient points away from the region where g of x is greater than zero. Thus, the gradient of f of x equals negative lambda times the gradient of g of x, with lambda greater than zero. For both cases, the product of lambda and g of x equals zero. The solution to the problem of maximizing f of x subject to g of x greater than or equal to zero is obtained by optimizing the Lagrangian function with respect to x and lambda, subject to the conditions that g of x is greater than or equal to zero, lambda is greater than or equal to zero, and lambda times g of x equals zero. These conditions are known as the Karush-Kuhn-Tucker (KKT) conditions.

Section: Extension to Multiple Constraints

Lastly, this technique can be extended to cases with multiple equality and inequality constraints. Suppose we want to maximize f of x subject to multiple equality constraints gj of x equals zero for j ranging from one to J, and multiple inequality constraints hk of x greater than or equal to zero for k ranging from one to K. We introduce Lagrange multipliers for each constraint and optimize the Lagrangian function, which includes terms for all constraints, subject to the conditions that the multipliers for the inequality constraints are non-negative and their product with the respective constraint functions equals zero. This method can also be adapted for constrained functional derivatives. For a detailed discussion, you may refer to the works by Nocedal and Wright.

Section: Chapter Summary

1. **Introduction to Lagrange Multipliers**:
   - Lagrange multipliers are used to find stationary points of a function with constraints.
   - Useful for optimization problems requiring maximization or minimization under specific conditions.

2. **Conceptual Illustration**:
   - For a function f(x1, x2) with a constraint g(x1, x2) = 0, traditional methods can be cumbersome.
   - Lagrange multipliers offer a more elegant solution by introducing a parameter λ (lambda).

3. **Geometric Motivation**:
   - Constraint g(x) = 0 describes a surface in multi-dimensional space.
   - Gradient of g is orthogonal to the constraint surface.
   - At maximum, the gradient of f must also be orthogonal to the constraint surface.

4. **Lagrange Multiplier Method**:
   - Gradients of f and g are parallel or anti-parallel.
   - Introduce λ such that ∇f + λ∇g = 0.

5. **Lagrangian Function**:
   - Define Lagrangian L(x, λ) = f(x) + λg(x).
   - Stationary condition: set gradient of L with respect to x and λ to zero.
   - Solving these equations yields the stationary point and λ value.

6. **Example**:
   - Maximize f(x1, x2) = 1 - x1^2 - x2^2 with constraint x1 + x2 - 1 = 0.
   - Lagrangian: L = 1 - x1^2 - x2^2 + λ(x1 + x2 - 1).
   - Solving gives stationary point (1/2, 1/2) and λ = 1.

7. **Inequality Constraints**:
   - Maximize f(x) subject to g(x) ≥ 0.
   - Two cases: constraint inactive (∇f = 0, λ = 0) or active (on boundary, ∇f = -λ∇g, λ > 0).
   - Karush-Kuhn-Tucker (KKT) conditions apply: g(x) ≥ 0, λ ≥ 0, λg(x) = 0.

8. **Extension to Multiple Constraints**:
   - Multiple equality constraints: gj(x) = 0 for j = 1 to J.
   - Multiple inequality constraints: hk(x) ≥ 0 for k = 1 to K.
   - Introduce Lagrange multipliers for each constraint.
   - Optimize the Lagrangian subject to non-negative multipliers for inequality constraints and their product with constraints being zero.

9. **Adaptation for Functional Derivatives**:
   - The method is adaptable for constrained functional derivatives.
   - For further details, refer to works by Nocedal and Wright.
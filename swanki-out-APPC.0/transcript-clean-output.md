Section: Appendix C. Lagrange Multipliers

Lagrange multipliers, sometimes referred to as undetermined multipliers, are a powerful mathematical technique used to identify the stationary points of a function of several variables when those variables are subject to one or more constraints. For instance, consider trying to find the maximum of a function of two variables, denoted as f of x1 and x2, while being subject to a constraint that relates x1 and x2, which can be expressed as g of x1 and x2 equals zero.

One traditional approach to solve this involves expressing one variable in terms of the other using the constraint equation. For example, if g of x1 and x2 equals zero, we can solve for x2 as a function of x1, say x2 equals h of x1. Substituting this back into f, we now have a function of x1 alone, f of x1 and h of x1. We then find the maximum of this new function by differentiating it with respect to x1 and finding where this derivative equals zero. This gives a stationary value for x1, denoted x1 star, and the corresponding value for x2 is given by x2 star equals h of x1 star. However, this method can be cumbersome and non-symmetric, as it treats x1 and x2 differently.

A more elegant solution is to introduce a parameter, lambda, known as a Lagrange multiplier. To understand this method geometrically, consider a D-dimensional variable x with components x1 through xD. The constraint g of x equals zero represents a (D-1)-dimensional surface in the space of x. At any point on this surface, the gradient of g, denoted nabla g of x, is orthogonal to the surface. This orthogonality can be visualized as follows: if we take a point x on the constraint surface and a nearby point x plus epsilon also on the surface, the Taylor expansion of g around x reveals that the gradient of g must be perpendicular to any small displacement epsilon on the surface.

When seeking a point x star that maximizes f of x on the constraint surface, this point must have the property that the gradient of f, nabla f of x, is also orthogonal to the constraint surface. Otherwise, it would be possible to increase f by moving along the constraint surface. Consequently, nabla f and nabla g must be parallel (or anti-parallel), implying the existence of a parameter lambda such that the gradient of f plus lambda times the gradient of g equals zero.

This leads us to define the Lagrangian function, L of x and lambda, which is f of x plus lambda times g of x. The stationary points of this function, where the gradient with respect to x equals zero, provide the solution to the constrained optimization problem. Additionally, setting the partial derivative of L with respect to lambda to zero enforces the constraint g of x equals zero.

To illustrate this, consider the function f of x1 and x2 equals one minus x1 squared minus x2 squared, with the constraint g of x1 and x2 equals x1 plus x2 minus one equals zero. The corresponding Lagrangian for this problem is L of x and lambda equals one minus x1 squared minus x2 squared plus lambda times (x1 plus x2 minus one). Setting the partial derivatives of L with respect to x1, x2, and lambda to zero yields a system of equations. Solving these, we find the stationary point (x1 star, x2 star) is one-half, one-half and the value of lambda is one.

Next, we consider constraints in the form of inequalities, where g of x is greater than or equal to zero. There are two types of solutions: one where the stationary point lies within the region where g of x is strictly positive, and the other where it lies on the boundary where g of x equals zero. In the first case, the constraint is inactive, and we only need to find where the gradient of f equals zero. In the second case, the constraint is active, and the solution is analogous to the equality constraint case, except the Lagrange multiplier lambda must be non-negative, ensuring that the gradient of f points away from the region where g of x is positive.

The conditions for this type of optimization are known as the Karush-Kuhn-Tucker (KKT) conditions. They state that g of x must be greater than or equal to zero, lambda must be non-negative, and the product of lambda and g of x must equal zero.

Finally, the method of Lagrange multipliers can be extended to cases involving multiple equality and inequality constraints. For multiple equality constraints, we introduce multiple Lagrange multipliers and optimize the Lagrangian function, which becomes a sum of f of x and terms involving each constraint multiplied by its corresponding Lagrange multiplier. For inequality constraints, the multipliers must also satisfy non-negativity conditions.

In summary, Lagrange multipliers provide a versatile and elegant method for solving constrained optimization problems by transforming them into problems of finding the stationary points of an augmented function, the Lagrangian.
Section: Appendix C. Lagrange Multipliers

Lagrange multipliers, sometimes referred to as undetermined multipliers, are a powerful mathematical technique used to identify the stationary points of a function of several variables when those variables are subject to one or more constraints. For instance, consider trying to find the maximum of a function of two variables, denoted as f of x1 and x2, while being subject to a constraint that relates x1 and x2, which can be expressed as g of x1 and x2 equals zero.

One traditional approach to solve this involves expressing one variable in terms of the other using the constraint equation. For example, if g of x1 and x2 equals zero, we can solve for x2 as a function of x1, say x2 equals h of x1. Substituting this back into f, we now have a function of x1 alone, f of x1 and h of x1. We then find the maximum of this new function by differentiating it with respect to x1 and finding where this derivative equals zero. This gives a stationary value for x1, denoted x1 star, and the corresponding value for x2 is given by x2 star equals h of x1 star. However, this method can be cumbersome and non-symmetric, as it treats x1 and x2 differently.

A more elegant solution is to introduce a parameter, lambda, known as a Lagrange multiplier. To understand this method geometrically, consider a D-dimensional variable x with components x1 through xD. The constraint g of x equals zero represents a (D-1)-dimensional surface in the space of x. At any point on this surface, the gradient of g, denoted nabla g of x, is orthogonal to the surface. This orthogonality can be visualized as follows: if we take a point x on the constraint surface and a nearby point x plus epsilon also on the surface, the Taylor expansion of g around x reveals that the gradient of g must be perpendicular to any small displacement epsilon on the surface.

When seeking a point x star that maximizes f of x on the constraint surface, this point must have the property that the gradient of f, nabla f of x, is also orthogonal to the constraint surface. Otherwise, it would be possible to increase f by moving along the constraint surface. Consequently, nabla f and nabla g must be parallel (or anti-parallel), implying the existence of a parameter lambda such that the gradient of f plus lambda times the gradient of g equals zero.

This leads us to define the Lagrangian function, L of x and lambda, which is f of x plus lambda times g of x. The stationary points of this function, where the gradient with respect to x equals zero, provide the solution to the constrained optimization problem. Additionally, setting the partial derivative of L with respect to lambda to zero enforces the constraint g of x equals zero.

To illustrate this, consider the function f of x1 and x2 equals one minus x1 squared minus x2 squared, with the constraint g of x1 and x2 equals x1 plus x2 minus one equals zero. The corresponding Lagrangian for this problem is L of x and lambda equals one minus x1 squared minus x2 squared plus lambda times (x1 plus x2 minus one). Setting the partial derivatives of L with respect to x1, x2, and lambda to zero yields a system of equations. Solving these, we find the stationary point (x1 star, x2 star) is one-half, one-half and the value of lambda is one.

Next, we consider constraints in the form of inequalities, where g of x is greater than or equal to zero. There are two types of solutions: one where the stationary point lies within the region where g of x is strictly positive, and the other where it lies on the boundary where g of x equals zero. In the first case, the constraint is inactive, and we only need to find where the gradient of f equals zero. In the second case, the constraint is active, and the solution is analogous to the equality constraint case, except the Lagrange multiplier lambda must be non-negative, ensuring that the gradient of f points away from the region where g of x is positive.

The conditions for this type of optimization are known as the Karush-Kuhn-Tucker (KKT) conditions. They state that g of x must be greater than or equal to zero, lambda must be non-negative, and the product of lambda and g of x must equal zero.

Finally, the method of Lagrange multipliers can be extended to cases involving multiple equality and inequality constraints. For multiple equality constraints, we introduce multiple Lagrange multipliers and optimize the Lagrangian function, which becomes a sum of f of x and terms involving each constraint multiplied by its corresponding Lagrange multiplier. For inequality constraints, the multipliers must also satisfy non-negativity conditions.

In summary, Lagrange multipliers provide a versatile and elegant method for solving constrained optimization problems by transforming them into problems of finding the stationary points of an augmented function, the Lagrangian.

Section: Chapter Summary

1. Lagrange multipliers are used to find stationary points of a function with constraints.
2. Traditional method: Express one variable in terms of another using the constraint, then find the stationary point.
3. Lagrange multipliers introduce a parameter, lambda, to handle constraints more elegantly.
4. Geometric interpretation: The gradient of the constraint function is orthogonal to the constraint surface.
5. For optimal solutions, the gradient of the objective function must be parallel to the gradient of the constraint function.
6. Define the Lagrangian function as the objective function plus lambda times the constraint function.
7. Stationary points of the Lagrangian function provide solutions to the constrained optimization problem.
8. Example: Maximizing a quadratic function with a linear constraint.
9. Inequality constraints introduce additional complexity: inactive constraints (where the constraint is not binding) and active constraints (where the constraint is binding).
10. Karush-Kuhn-Tucker (KKT) conditions generalize the method to inequality constraints.
11. KKT conditions: g(x) ≥ 0, lambda ≥ 0, and lambda * g(x) = 0.
12. Multiple constraints: Introduce multiple Lagrange multipliers, one for each constraint.
13. For inequality constraints, Lagrange multipliers must be non-negative.
14. Lagrange multipliers transform constrained optimization problems into finding stationary points of an augmented function.
## Explanation of one-versus-the-rest classifier for multiple classes

Describe the concept of one-versus-the-rest classifier for multiple classes. 

This is known as a one-versus-the-rest classifier, where $K-1$ classifiers are trained, each one solving the problem of separating points in a particular class $\mathcal{C}_k$ from points not in that class. This approach can lead to ambiguously classified regions as shown in the left-hand example of Figure 5.2.

- #machine-learning, #classification.one-vs-rest

## Ambiguities in one-versus-one and one-versus-the-rest classifiers

What are the ambiguities associated with one-versus-one and one-versus-the-rest classifiers?

Both one-versus-one and one-versus-the-rest classifiers lead to ambiguities. In the one-versus-the-rest classifier (left-hand example in Figure 5.2), some regions of input space are ambiguously classified. In the one-versus-one classifier (right-hand example in Figure 5.2), ambiguous regions also occur since multiple discriminant functions can give conflicting outputs.
 
- #machine-learning, #classification.ambiguity

## Illustration of linear discriminant functions for $K > 2$ classes

Explain the configuration of linear discriminant functions for $K > 2$ classes as a solution. %

The linear discriminant function for $K > 2$ classes can be defined as:
$$
y_k(\mathbf{x}) = \mathbf{w}_k^{\mathrm{T}} \mathbf{x} + w_{k0}
$$
A point $\mathbf{x}$ is assigned to class $\mathcal{C}_k$ if $y_k(\mathbf{x}) > y_j(\mathbf{x})$ for all $j \neq k$. The decision boundary between class $\mathcal{C}_k$ and class $\mathcal{C}_j$ is given by $y_k(\mathbf{x}) = y_j(\mathbf{x})$.

- #machine-learning, #linear-discriminant.functions

## Decision boundary for $K$-class linear discriminants

Provide the equation for the decision boundary between class $\mathcal{C}_k$ and class $\mathcal{C}_j$ when using $K$-class linear discriminants.

The decision boundary between class $\mathcal{C}_k$ and class $\mathcal{C}_j$ is given by:
$$
y_k(\mathbf{x}) = y_j(\mathbf{x})
$$

- #machine-learning, #classification.decision-boundary

## Equation of linear discriminant function

What is the general form of the linear discriminant function in a $K$-class problem?

The general form of the linear discriminant function in a $K$-class problem is:
$$
y_k(\mathbf{x}) = \mathbf{w}_k^{\mathrm{T}} \mathbf{x} + w_{k0}
$$

- #mathematics, #linear-algebra.discriminant-function

## Ambiguity in two-class vs multiple-class discriminant functions

How does ambiguity arise when attempting to extend two-class discriminant functions to $K$ classes?

Ambiguity arises when extending two-class discriminant functions to $K$ classes because regions of input space will be classified ambiguously. This happens because more complex boundary interactions occur that the two-class discriminant functions are not designed to handle, as indicated by the green regions in the Figure 5.2 examples.

- #machine-learning, #classification.ambiguity
## What is permutation invariance and equivariance in the context of Graph Neural Networks (GNNs)? 

Permutation invariance and equivariance are important symmetries in the design of GNNs. A function is considered permutation invariant if its output does not change when the order of its input nodes is permuted. A function is equivariant if applying a transformation to the input leads to a corresponding transformation of the output.

For example, a graph-level output such as the vector representation of a molecule should be invariant to the permutation of nodes, meaning the order of atoms does not matter. In contrast, node-level predictions such as the vector containing the predicted electronegativity of each atom are equivariant, meaning they depend on the node ordering.

$$
\begin{aligned}
&\text{Permutation Invariance:} f(\pi(\mathbf{X})) = f(\mathbf{X}) \\
&\text{Permutation Equivariance:} f(\pi(\mathbf{X})) = \pi(f(\mathbf{X}))
\end{aligned}
$$

Here, $\pi$ represents a permutation function and $\mathbf{X}$ is the input.

- #machine-learning, #graph-neural-networks, #symmetry

## Why is the Weisfeiler-Leman test important for understanding GNN expressivity? 

The Weisfeiler-Leman test (WL test) is a classical algorithm for determining graph isomorphism by repeatedly updating a node's label based on the labels of its neighbors. This method is analogous to message-passing layers in GNNs.

Because of this similarity, the WL test provides insight into the expressiveness of GNNs. Specifically, if two graphs cannot be distinguished by the WL test, then a standard GNN is unlikely to distinguish between them either. This impacts the GNN's ability to learn certain functions and capture particular patterns.

$$
\text{WL Test:  } h_v^{(t)} = \text{hash}(h_v^{(t-1)}, \{h_u^{(t-1)}, u \in \mathcal{N}(v)\})
$$

Where $h_v^{(t)}$ is the representation of node $v$ at iteration $t$, and $\mathcal{N}(v)$ are the neighbors of $v$.

- #machine-learning, #graph-neural-networks, #graph-isomorphism

## What role do permutation-invariant aggregation functions play in GNNs?

Permutation-invariant aggregation functions are crucial in ensuring that GNN outputs are independent of the input node order. These functions, such as mean, sum, and maximum, are used in message-passing and prediction layers to aggregate information from neighboring nodes.

$$
\text{Aggregation:  } \mathbf{h}_v^{(t)} = \text{Agg}(\{\mathbf{h}_u^{(t-1)} | \forall u \in \mathcal{N}(v)\})
$$

Here, $\mathbf{h}_v^{(t)}$ is the updated node representation and $\text{Agg}$ is a permutation-invariant function.

- #machine-learning, #graph-neural-networks, #aggregation-functions

## Explain the concept of "global expressivity" in GNNs.

Global expressivity refers to a GNN's ability to represent a wide range of functions over graphs. A critical measure of global expressivity is whether a GNN can distinguish between non-isomorphic graphs, which is closely connected to the problem of graph isomorphism.

Since distinguishing between all non-isomorphic graphs in polynomial time is infeasible, researchers instead study which classes of graphs a GNN architecture can distinguish, impacting its practical applications.

- #machine-learning, #graph-neural-networks, #expressivity

## How does imposing biases and symmetries affect the learning process in GNNs?

Imposing biases and symmetries in GNNs restricts the set of functions the model is capable of learning, leading to a reduction in the number of parameters and improved data efficiency. This helps prevent the model from learning spurious correlations and aids in generalization.

For instance, enforcing permutation invariance ensures that the model does not waste capacity on tracking node order, focusing instead on topology-related patterns.

$$
\text{Function set restriction: f(\pi(\mathbf{X})) = f(\mathbf{X})}
$$

- #machine-learning, #graph-neural-networks, #biases-and-symmetries

## What is the relationship between data efficiency and the inclusion of data symmetries in GNN architectures?

Incorporating data symmetries such as permutation invariance in GNN architectures enhances data efficiency by reducing the hypothesis space. This limits the number of functions that the model can potentially represent, thereby making it more likely that the learned functions will generalize well on unseen data, without overfitting.

For example, ensuring that the molecule's energy prediction model is rotation-invariant allows it to utilize data more effectively by not having to learn the same function multiple times for different orientations.

$$
\text{Energy invariance: } E(\mathbf{R}) = E(\mathbf{R}')
$$

Where $\mathbf{R}$ and $\mathbf{R}'$ are different representations of the same molecular configuration.

- #machine-learning, #graph-neural-networks, #data-efficiency
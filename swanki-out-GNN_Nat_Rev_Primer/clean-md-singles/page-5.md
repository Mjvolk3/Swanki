a

![](https://cdn.mathpix.com/cropped/2024_05_28_dfbaeefd189f717739c9g-1.jpg?height=529&width=1578&top_left_y=398&top_left_x=249)

b

![](https://cdn.mathpix.com/cropped/2024_05_28_dfbaeefd189f717739c9g-1.jpg?height=365&width=1610&top_left_y=1003&top_left_x=279)

Fig. 3 | Important data symmetries for GNNs. a, Examples of properties that are permutation and rotation invariant or equivariant. The energy of a molecule does not depend on its frame of reference, and so it is translation and rotation invariant. By contrast, the forces are translation and rotation equivariant vectors, as they rotate with the molecule in the new frame of reference.
The energy is invariant with respect to the reordering of the atoms, whereas the vector of atom types or charges is rearranged with the same ordering. $\mathbf{b}$, The challenge of graph isomorphism: the Weisfeiler-Leman test as a standard graph neural network (GNN) will never be able to distinguish the third graph from the first two, as nodes of the same colour will always have the same representation.
Permutation invariance and equivariance. Alongside soft inductive biases, data efficiency can be improved by building data symmetries into the architecture. This reduces the number of possible functions the model can represent and avoids learning meaningless correlations between specific node orderings and labels, making it more likely that the model will learn a generalizable function. For graphs, the most important symmetry is permutation invariance, according to which the graph under consideration does not change if the nodes are permuted, meaning node ordering does not matter.

This idea is formalized using the group theoretic concepts of invariance and equivariance. First, a set of transformations - formally a group ${ }^{13}-$ needs to be defined, such as permuting the order of nodes. A function is considered invariant to this set of transformations if its output does not change when one of the transformations is applied to its input. Similarly, a function is equivariant if informally applying a transformation to the input leads to a corresponding transformation of the output.

Graph-level outputsshould be invariant topermutations. For example, a vector representation of a molecule should be the same regardless of the order in which the atoms are written in. On the other hand, node-level predictions are equivariant. For example, the vector containing the predicted electronegativity of each atom should directly depend on the ordering used to represent the atoms in the graph (Fig. 3a). These properties are achieved in GNNs if permutation-invariant aggregation functions are used - for example, mean, sum and maximum - in the message-passing and final prediction layers.

\section*{Expressivity}

Imposing biases and symmetries controls the set of functions a model is not allowed to learn. By contrast, expressivity analysis looks at which set of functions a model is able to learn. Studying the expressiveness of GNNs provides an understanding of which patterns a model will and will not be able to capture, which is important for designing the best architecture and features to address the problem. In practice, an architecture should be chosen with an expressivity that captures the patterns critical for the task. An unjustified increase in the expressivity can lead to a worse generalization capacity due to overfitting.

Global expressivity. A necessary condition for a model to represent an arbitrary function on agraph is its ability to distinguish if two graphs are identical, a problem known as graph isomorphism. As no polynomial time algorithm is known to solve graph isomorphism for arbitrary graphs, there is currently no maximally expressive GNN whose runtime is polynomial in the number of nodes. As a result, researchers have studied the classes of graphs that GNN architectures can or cannot distinguish.

One key result for this analysis comes from the similarity ${ }^{14,15}$ between message-passing layers in GNNs and the Weisfeiler-Leman isomorphism test, a classical algorithm in which each node is repeatedly assigned the hash of the representation of its neighbours. This analogy implies that standard GNNs are not able to distinguish graphs like the ones shown in Fig. 3b and, therefore, would predict them to have
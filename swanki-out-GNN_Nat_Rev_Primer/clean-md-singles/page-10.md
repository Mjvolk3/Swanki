\title{
Primer
}

\section*{Glossary}

\section*{Big O notation}

Notation used in complexity theory to indicate how the worst-case runtime of an algorithm increases as the size of the input increases

\section*{Composition pattern}

A simple example composition pattern is if molecule $A$ binds to protein $B$ and protein $B$ is involved in the mechanism of disease $\mathrm{C}$, then $\mathrm{A}$ is a potentia candidate for $\mathrm{C}$

\section*{Deep learning}

Subset of machine learning that uses artificial neural network models with multiple layers learning to automatically extract features and complex patterns from data

\section*{Embeddings}

Arrays of numbers produced by a deep learning model abstractly capture a model's understanding of an object.

\section*{Features}

Information about the object under analysis that is passed as inputs to the model.

\section*{Knowledge graph completion}

Task in which missing information in a

knowledge graph is predicted based

on existing relationships and patterns within the graph.

\section*{Message-passing layer}

Fundamental component of graph

neural networks that iteratively

aggregates and updates the features

from neighbouring nodes, enabling the

propagation of information throughout the graph structure.
Planar graphs

A planar graph is one that can be drawn on a 2D page without edges crossing each other.

\section*{ReLU}

The rectified linear unit (ReLU) is the most common type of non-linear function used in neural networks and has the simple form $\operatorname{ReL} U(x)=\max (0, x)$.

\section*{Representations}

Arrays of numbers that capture attributes of an object.

\section*{ROC-AUC}

(Area under the curve of the receiver operator characteristic). A measure of the precision of a binary classifier that is informative in settings with unbalanced classes.

\section*{Scaffold}

Core substructures within molecular graphs shared by multiple compounds that often have similar properties

\section*{Transductive task}

Setting that involves making predictions at inference time on a partially labelled graph, for a subset of the nodes within the graph. Models trained in a transductive setting do not generalize to other graphs.

\section*{Uncertainty}

Uncertainty refers to the lack of confidence or precision in a model's prediction. Taking this ambiguity into account is often important in real-world applications of machine learning models
Pretraining. In pretraining approaches, a model is trained on a related task, for which more data are available, to teach the model to extract relevant features. Subsequently, the limited labelled data are used to learn how to recombine those features for the task at hand, referred to as fine-tuning. Pretraining GNNs has shown some success. In quantum chemistry-related tasks ${ }^{100,101}$, large datasets of molecular physical properties obtained via expensive calculations are used to pretrain expressive models. However, graph pretraining remains challenging for many domains, partly due to the failure of self-supervised learning approaches.

Self-supervised learning. Pretraining of large models in an unsupervised fashion has driven incredible progress for text ${ }^{102,103}$, protein sequences ${ }^{104}$ and images ${ }^{105-107}$. These methods use techniques like contrastive learning or masking to design synthetic tasks aimed at building expressive representations from large amounts of unlabelled data. However, direct application to molecules and other graph-structured data has not been successful ${ }^{108}$, likely due to limited relevance.

For example, predicting a masked word in a sentence requires meaningful digestion of its context, which is helpful for understanding natural language. In a molecule, however, it is almost trivial to infer an atom's element given its context due to the number of possible bonds. Similarly, in computer vision, contrastive learning helps models become invariant to data augmentations or distortions. For molecules, however, deleting an atom results in completely different chemical properties.

\section*{Technical limitations}

Oversmoothing. Oversmoothing is a widely known limitation of GNNs, in which individual node features become nearly identical as the number of GNN layers increases, because each message-passing layer behaves as a graph-smoothing operator ${ }^{109}$. This phenomenon prevents very deep networks, which are prevalent in other domains. Several methods to alleviate oversmoothing have been proposed. For instance, JKNets ${ }^{110}$ introduce skip connections in which the initial node features are added to the node features after every layer, Graff ${ }^{111}$ biases the information flow to alleviate oversmoothing and Gradient Gating ${ }^{12}$ uses a gating mechanism to control local information flow in the graph. Although these approaches afford improvements, there is still no clear solution to this challenge.

Oversquashing. Oversquashing refers to the topology of the graph causing bottlenecks in information flow, leading to little signal and influence between distant nodes ${ }^{113}$. At the bottlenecks, many nodes' features must be compressed into a single node's representation, which limits the GNNs' ability to capture long-range dependencies. Oversquashing has seen multiple analyses, with proposed solutions, such as adding a virtual global node or rewiring the graph ${ }^{114}$, but it remains an open problem.

\section*{Outlook}

GNNs are limited in their expressiveness, interpretability and data efficiency, with practitioners often partially relying on feature engineering. However, to overcome these challenges, there is active research, some of which is presented in this section.

Although GNNs are fundamentally bounded in expressivity by the intrinsic complexity of distinguishing general graphs, in practical domains arbitrary graphs are rarely encountered. Molecules and road networks, for example, are almost exclusively planar graphs in which scalability and interpretability. The generalization capacity of fingerprints is particularly helpful in the low data regime, in which large GNNs can overfit easily. For example, if the training data contain only several hundred examples with very few positives, a GNN with many parameters will likely overfit, as the model does not have enough supervision to learn which features are robust and which are spurious correlations. The lack of data in many areas of the life sciences is a big limitation to the application of GNNs. Building architectures that incorporate prior knowledge about the problem can alleviate this challenge, as the model does not have to learn these aspects from the scarce data. Another core method for addressing a lack of data is pretraining.
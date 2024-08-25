\title{
Primer
}

\section*{Introduction}

A wide variety of problems can be modelled as graph structures. These mathematical objects consist of nodes, which represent entities, and edges, which capture their relationships or interactions. Graphs can represent a diverse set of data types, from molecules, in which nodes are atoms and bonds are edges, to biomedical knowledge graphs, which link hundreds of thousands of genes, drugs and diseases.

Until recently, inference on graph structures was only possible through a fixed set of rules or features designed for each prediction task. For example, molecules were represented by a vector whose entries capture specific substructures and patterns known to be chemically relevant. Although such approaches can reflect valuable domain knowledge, their representation power is limited to what is known. They lack the flexibility to capture novel, complex patterns that may be important for problems of interest.

To overcome this challenge, a new class of deep learning methods, referred to asgraph neural networks (GNNs), has emerged \({ }^{1-3}\), and it has been successfully applied to many problems in the life sciences and beyond. Since their first introduction, the standard formulation of GNNs has evolved, and this Primer presents their modern view. Similarly to other deep learning architectures, GNNs use available training data for the problem to extract representations from graphs. These learned representations are high-dimensional vectors that encode task-relevant information in a machine-understandable format. For instance, a GNN can be trained on molecules to induce representations containing relevant information about their toxicity.

The GNN modelling framework can answer questions about a graph's nodes, edges or the full graph by formulating problems as prediction tasks. For example, inferring a molecule's toxicity is a graph-level prediction. At the same time, given a gene regulatory network, information may be desired about the function of an orphan gene (node prediction) or previously unknown interactions (edge prediction).

Despite their wide applicability, GNNs are not without limitations. For instance, if the labelled training examples fail to capture the diversity or breadth of the intended deployment data, learned models generalize poorly to real-world scenarios. Furthermore, interpretability and uncertainty estimation remain a challenge for large models. Finally, many GNN architectures lack the ability to recognize certain critical patterns in graphs. Therefore, although GNNs have proven successful in many applications, it is essential to understand their inner workings, strengths and weaknesses to maximize their effectiveness. This Primer aims to introduce these components, alongside an exploration of solutions and ongoing research to address the shortcomings of the technique.

In the following sections, the GNN framework, applications, limitations and directions for future research are introduced. The Experimentation section defines the GNN framework, using a molecular property prediction example to illustrate practical strengths and weaknesses. The Results section elaborates on different variations, theoretical properties and shortcomings of GNNs, as well as some proposed solutions. The Applications section features several successes of GNNs, with a focus on fundamental modelling principles, benchmark datasets and best practices. Finally, the Limitations section highlights some of the fundamental limitations of GNNs, ranging from data dependency to the technical limits of the mathematical frameworks. The article concludes with an outlook of pressing issues and promising directions for GNNs.

This Primer is intended as an introduction to GNNs for students and practitioners. It is assumed that readers are familiar with basic concepts in machine learning, including featurization, gradient descent and train/test splits. This is not a comprehensive survey of all the theoretical results and methodologies regarding GNNs. Interested readers are directed to refs. 4,5 for more exhaustive expositions on the theoretical foundations.

\section*{Experimentation}

This section introduces the fundamental building blocks of GNNs and some key practical considerations by working through a motivating example: predicting whether a small molecule inhibits HIV growth.

Molecular property predictors have become a fundamental tool in biochemistry, in which in silico virtual screening offers a promising alternative to expensive assays. Classical methods for molecular property prediction begin with a molecular fingerprint, a vector of hand-crafted features based on the molecular graph \({ }^{6}\). These features can be used as an input in simple machine learning models - for example, random forests, support vector machines and shallow feedforward networks - for property prediction. However, these handcrafted features are limited to existing knowledge about molecules.

To move beyond molecular fingerprints, GNNs were developed to learn more expressive and powerful representations directly from the graphs. Given a molecular graph as input, a GNN can be trained to predict properties such as drug absorption, distribution, metabolism, excretion, toxicity, protein binding affinity and solubility (Fig. 1). The implementation of the method accompanying this example is available in a Jupyter notebook on the GitHub repository provided.

\section*{Formalization}

In the worked example, the molecule is viewed as a graph. Agraph is a tuple \(G=(V, E)\) in which \(V\) is the set of nodes \(v_{i}-\) for instance, the atoms and \(E\) is the set of edges \(\left(v_{i}, v_{j}\right)\) connecting pairs of nodes, in this case, the covalent bonds between atoms. The set of neighbours of a node \(v_{i}\) are denoted as \(N_{i=}\left\{v_{j} \mid\left(v_{i}, v_{j}\right) \in E\right\}\).

The nodes \(v_{i}\) are first converted to machine-understandable vector representation, \(h_{i}^{(0)}\), in which the exponent 0 indicates the input, before the first layer. For instance, each atom type - for example, hydrogen, carbon or oxygen - is associated with a specific high-dimensional embedding. Similarly, edges can have representations \(e_{i j}\) that encode their properties, such as the bond type (single or double) between two atoms.

\section*{Message-passing}

The fundamental building block of a GNN is the message-passing layer. At every message-passing layer, each node collects messages in the form of vector representations from its neighbouring nodes, aggregates them into a single vector, and uses this vector to update its own representation. Iterative message-passing enables each node to build representations that capture larger, more complex patterns from the graph around them. The filters learned by each message-passing layer depend on the transformations applied to the messages' representations before and after the aggregation, which are parameterized with feedforward neural networks (FF-NNs) and whose weights are learned from data with stochastic gradient descent.

In the worked example, a simple instantiation of message-passing is used, in which the messages are the representations of the neighbours, the aggregation strategy is the vector summation of all messages, and the update is performed with a one-layer FF-NN with
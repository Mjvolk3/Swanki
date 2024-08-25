![](https://cdn.mathpix.com/cropped/2024_05_28_09a6ffb5cfe6176c86bbg-1.jpg?height=684&width=1811&top_left_y=372&top_left_x=146)

learnable linear transformation \(W^{(l)}\) and ReLU non-linearity. Therefore, the mathematical operation performed to update the representation \(h_{i}^{(l)}\) of node \(i\) at layer \(\ell\) can be written as:

\[
h_{i}^{(l+1)}=\operatorname{Re} L U\left(W^{(l+1)}\left(h_{i}^{(l)}+\sum_{j} h_{j}^{(l)}\right)\right)
\]

\section*{Final prediction}

After the final message-passing layer, the representations of individual nodes are aggregated and transformed to make task-specific predictions, as different problems may require outputs at different scales.

For example, the molecular property prediction task is a graphlevel problem in which to make a single prediction for the graph, the representations of all nodes - whose count may vary across molecules must be aggregated into a fixed-size vector that represents the whole molecule. In the provided implementation, after four message-passing layers, the final prediction (likelihood of inhibition) is reached by summing the nodes' features in the last layer and passing their sum through a linear layer with output dimension 1 .

By contrast, in node-level tasks, such as the functional characterization of proteins in a protein interaction network, the node representations after the message-passing layers can be directly used as outputs for prediction. Finally, the most common class of edge-level tasks is link prediction, in which the model is trained to predict missing edges in the graph, for example knowledge graph completion or recommendation systems. For this, a classifier is typically trained by aggregating the final representations of the two nodes or surrounding subgraphs connected by the edge in question.

\section*{Efficient implementation}

In many applications, GNNs are run on graphs with thousands or millions of nodes. In such cases, efficient sparse implementations of message-passing are necessary to run training and inference in a reasonable time. The computational complexity of a message-passing layer is \(O(|E|+|V|)=O(|E|)\), in which \(O\) indicated the big \(O\) notation, or linear in the number of edges, as messages have to be computed for every edge and in connected graphs \(|E| \geq|V|-1\). To run these operations efficiently on graphics processing unit or tensor processor unit hardware, it is critical to parallelize message computation and aggregation.
One approach to parallelize these operations is to store edge information and messages as pairwise matrices, which can be efficiently transformed via matrix and dot products. However, this method would incur a runtime and memory complexity of \(O\left(|V|^{2}\right)\), which is quadratic in the number of nodes, and for large sparse graphs it can be substantially larger than \(O(|E|)\).

Instead, if the graph is represented in a sparse matrix data structure or adjacency list, computations can be parallelized while maintaining the \(O(|E|)\) complexity. For large structures, such as the atomic resolution graph of a protein (typically \(1,000-10,000\) atoms) or large knowledge graph ( \(>100,000\) nodes \(^{7}\) ), sparse implementations enable the data to fit in memory, meaning the computation can be completed orders of magnitude faster. As these sparse computations require careful implementation, specialized libraries for GNNs have been developed. The most widely used include PyTorch Geometric \({ }^{8}\) and Deep Graph Library \({ }^{9}\) for general graphs, Chemprop \({ }^{10}\) for molecular graphs, and e3nn \({ }^{11}\) for 3D geometric graphs. These libraries provide instantiations of existing models, simplify the implementation of novel architectures (see Jupyter notebook on the GitHub repository provided) and give access to datasets and auxiliary tools, such as featurization.

\section*{Data format and splitting}

When using deep neural networks like GNNs, a key question is whether the features learned from the training data will generalize to real-world scenarios. To tackle this question without collecting additional data, splitting data between training and testing is critical. For graphs, data-splitting approaches differ between inductive and transductive settings.

Inductive tasks. Inductive tasks closely resemble the common paradigm of machine learning problems in which the training, validation and testing datasets involve separate objects. Each set contains different graphs over which the GNNs are trained and evaluated. Molecular property prediction is a common example, as models are trained and tested on different sets of molecules. Deciding how to split the graphs between the different sets often requires domain expertise. In drug discovery, although labelled data are sourced from commonly observed parts of molecular space, to find novel drugs, unexplored parts of the
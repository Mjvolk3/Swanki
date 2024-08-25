\title{
Primer
}

Table $1 \mid$ Message-passing function of popular graph neural network architectures

\begin{tabular}{llr}
\hline Name & Message-passing & Ref. \\
\hline GCN & $h^{(l+1)}=\sigma\left(\widetilde{D}^{-\frac{1}{2}} \widetilde{A} \widetilde{D}^{-\frac{1}{2}} h^{(l)} W+b\right)$ & 117 \\
\hline GAT & $h_{i}^{(l+1)}=\sigma\left(\sum_{j \in N_{i}} a\left(h_{i}^{(l)}, h_{j}^{(l)}\right) W h_{j}^{(l)}\right)$ & 30 \\
\hline GIN & $h_{i}^{(l+1)}=\rho\left((1+\varepsilon) h_{i}^{(l)}+\sum_{j \in N(i)} h_{j}^{(l)}\right)$ & 14 \\
\hline MPNN & $h_{i}^{(l+1)}=\rho\left(h_{i}^{(l)}, \sum_{j \in N_{i}} \mu\left(h_{i}^{(l)}, h_{j}^{(l)}\right)\right)$ & 73 \\
\hline PNA & $h_{i}^{(l+1)}=\rho\left(h_{i}^{(l)}, \quad \| \quad \underset{j}{\oplus} \mu\left(h_{i}^{(l)}, e_{i j}, h_{j}^{(l)}\right)\right)$ & 31 \\
& & \\
\hline
\end{tabular}

In the equations, $h^{(l)}$ Indicates the representations at layer $l$; $A$ is the adjacency matrix, $A^{*}=A+I N, D^{\star} i j=P j A^{*} i j ; \rho$ and $\mu$ are learnable feedforward transformation functions; $\sigma$ a simple nonlinearity; $\varepsilon$ and $\mathrm{W}$ are a scalar and matrix parameter, respectively; $a$ is a learned attention function; \|| represents concatenation; $\mathbb{A}$ is a set of aggregators. GAT, graph attention network; GCN, graph convolutional network; GIN, graph isomorphism network; MPNN, message passing neural network; PNA, principal neighbourhood aggregation.

the same properties. Several works have tried to extend the classes of distinguishable graphs by considering higher-order interaction ${ }^{15}$ or features ${ }^{16}$. These expressivity improvements often come at the cost of greater computational complexity and longer runtimes.

Given that the shortcomings of message-passing arise from symmetries in the graphs, an alternative strategy to provably improve expressivity is to make the nodes more distinguishable, for example, by augmenting the input node features with random vectors ${ }^{17,18}$ or positional encodings that indicate the global position of a node in the $\mathrm{graph}^{19-23}$. The most popular positional encoding features are the normalized eigenvectors of the Laplacian matrix, known in graph signal processing literature for their numerous desirable properties.

Global expressivity studies based on the Weisfeiler-Leman test have two drawbacks. First, they only consider the graph structure and ignore the node or edge features, which are an integral part of the input to the function defined with GNNs. Recent works have investigated the expressiveness properties of how GNNs treat feature information ${ }^{24,25}$. Second, Weisfeiler-Leman expressiveness does not provide a clear, interpretable understanding of a GNN's capacity. Increased expressiveness often does not correlate with improved empirical performance. For these reasons, several works have instead opted to study GNNs using lens of local expressivity.

Local expressivity. A related class of analysis looks at local patterns in the graphs that GNNs can and cannot detect. For example, GNNs are not able to count certain substructure types, such as cycles. However, rings are often critically important in molecules and cliques in social networks. Therefore, the initial node and edge features of GNNs are often augmented with number cycles to contain them ${ }^{26}$. Positional encodings can also help models recognize local motifs ${ }^{21}$. In practice, this creates a hybrid approach in which flexible inference of the deep learning model is augmented with hand-crafted features as inputs, because these are known to be relevant but cannot be captured by the architecture. Providing the features as part of the input enables the model to detect more complex patterns.

In knowledge graph completion, capturing logic inference patterns - such as composition pattern, hierarchy and mutual exclusionis critical. Therefore, GNN architectures and embedding spaces are designed to model as many patterns as possible ${ }^{27-29}$.

\section*{GNN variants}

GNN architectures. Mathematically, the general message-passing layer can be written as:

$$
h_{i}^{(l+1)}=\rho\left(h_{i}^{(l)}, \bigoplus_{j \in N_{i}} \mu\left(h_{i}^{(l)}, h_{j}^{(l)}, e_{i j}\right)\right)
$$

in which $\rho$ and $\mu$ are, for example, learnable feedforward transformation functions and $\oplus$ is a predetermined aggregation function. Although hundreds of GNN architectures have been proposed, most can be described by the specific choice of aggregation and transformation functions. A summary of the functions used in common architectures is provided in Table 1.

Among these, graph attention network ${ }^{30}$ and principal neighbourhood aggregation ${ }^{31}$ propose two complementary strategies to improve the aggregation step and reduce bottlenecks. Graph attention network uses an attention mechanism to actively determine the weight given to each neighbour, enabling it to focus on the most relevant ones. By contrast, principal neighbourhood aggregation integrates multiple aggregation functions, meaning the nodes receive further information to increase the expressive power of the network.

Beyond simple message-passing. Many works have proposed ideas that go beyond this simple framework based on theoretical or empirical motivations. For example, a simple strategy shown to be particularly effective for moleculargraphs is to update both the representation of nodes and edges, referred to as directional message passing neural network ${ }^{10}$.

In certain domains, it is beneficial to decouple the computational graph that determines the information flow from the graph that underlies the data. Approaches to achieve this include rewiring the graph ${ }^{32,33}$ to preserve a meaningful structure, while alleviating bottlenecks, or passing messages with multiple graphs ${ }^{34}$.

Graph rewiring is also used to address the challenge of reasoning over long-range interactions: GNNs struggle to model patterns covering large distances over the graph; however, these can be helpful in several applications ${ }^{35}$. A popular approach to capturing long-range patterns is to process graphs with transformer-like architectures that operate on all pairs of nodes and use the original structure to bias the attention weights or provide a positional encoding to each node ${ }^{36,37}$.

Flowing information via message-passing on the graph structure is not the only way to use the inductive bias from graph structures. New approaches to incorporate and parse graph structures have been proposed, borrowing ideas from topology and physics. Using topological concepts, graph structures are represented in terms of simplicial ${ }^{38}$ or cell complexes ${ }^{39}$, and message-passing interactions are generalized to these topological objects. Physics-inspired methods consider the graph structure as a discretization of a continuous manifold, in which the message-passing process is a diffusion partial differential equation on the manifold ${ }^{40}$. This framework enables graph structures to be treated as continuous objects, using ideas from the diffusion process in physical systems to improve message-passing over graphs ${ }^{41-43}$.

Geometric graphs. In some domains, the nodes in the graph are embedded in the 3D space. Although these coordinates could be used as features of the nodes, they are typically treated separately, because they only provide a meaningful feature when analysed in relation to one another. Therefore, geometricgraphs are modelled with specific types
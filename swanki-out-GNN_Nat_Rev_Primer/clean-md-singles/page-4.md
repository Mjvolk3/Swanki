\title{
Primer
}

chemical space are searched. To simulate this distribution shift, the community commonly uses scaffold splits (Fig. 2) or time splits, in which molecules in the training, validation and test sets have different molecular scaffolds or are sourced from experiments conducted over different time periods.

Transductive tasks. Transductive tasks (semi-supervised learning) train and test on the same graph, which is typically large and incomplete. For example, the goal of knowledge graph completion is to detect missing edges based on existing ones. In biological settings, it may be desirable to repurpose existing drugs for new diseases. In this case, drugs and diseases are nodes, whereas efficacy relationships are edges. Care must be taken when dividing the known edges of this single graph into training and testing splits. Randomly masking edges between drugs and diseases may lead the model to just learn that similar drugs are likely to work against similar diseases. Although valid, this conclusion would not allow the discovery of drugs for diseases that lack known treatments.

\section*{Training and evaluation}

The HIV inhibition prediction example is an inductive task, which uses data provided by the Drug Therapeutics Program of the NIH's National Cancer Institute, accessible from the Open Graph Benchmark $(\mathrm{OGB})^{12}$. The dataset contains 40,000 small molecules, together with a binary label indicating their ability to inhibit HIV growth. The standardized data splits from the OGB use scaffold splitting, with $80 \%$ of the molecules for training, $10 \%$ for validation and $10 \%$ for testing.

The example GNN is constructed based on the previously described architecture, with an embedding layer, four layers of message passing and a final add pooling and feedforward network. For this classification task, cross-entropy is used as the loss function. To evaluate model performance, the area under the receiver operating curve is measured (ROC-AUC).

After training for 100 epochs, the ROC-AUC is $82.5 \%$ on the training set compared with $73.0 \%$ on the validation set. The higher ROC-AUC for training is expected, as the model sees those scaffolds during its

a

![](https://cdn.mathpix.com/cropped/2024_05_28_bd3c909ee9f1652ddb8cg-1.jpg?height=548&width=863&top_left_y=1797&top_left_x=148)

Fig. 2 |Molecule similarity and overfitting. a, Examples of molecules that have the same or a different molecular scaffold (indicated by purple and blue colour), which is a core substructure. b, A clustered 2D embedding of molecules. Each point corresponds to a molecule, and similar ones are clustered together. Points' colouring corresponds to different data sources. The larger yellow points and grey points correspond to true positive and false positive antibiotic training process. However, such a substantial difference might indicate overfitting. Overfitting means that a model has so many parameters that it is able to memorize the training data and labels instead of learning to recognize patterns that generalize to unseen data points. This is a common problem for machine learning algorithms in data-scarce settings, which is often the case in the life sciences. To ensure that a method is useful for new data, it is crucial to check if overfitting occurred and to evaluate generalization capabilities, for instance, via scaffold splits (Fig. 2).

In the worked example, overfitting can be avoided by stopping the training early. As the losses are tracked across training, the training process can be stopped at the point of highest validation performance (77.9\% ROC-AUC) before the model starts overfitting, which translates to a $74.5 \%$ ROC-AUC on the test set. This is considerably better than the performance ( $70.5 \%$ test set ROC-AUC) obtained with a shallow FF-NN on Morgan fingerprints.

\section*{Results}

Properties of GNNs

Although deep learning models offer a way to learn complex patterns directly from raw data, this usually comes at the cost of data efficiency. Given the large number of parameters to optimize, if the number of labelled examples is not large enough, the deep learning models are likely to learn spurious correlations and miss patterns that would enable generalization to unseen data points. A key to the success of GNNs is that, compared with standard FF-NNs, they improve data efficiency and accuracy on graph-structured data due to two fundamental properties: locality bias and permutation equivariance.

Locality bias. Whenever data are represented as graphs, edges are drawn to connect objects with some relation to one another. It is thus natural to think that a better representation of a node can be built by looking at its neighbours, to provide more information than looking at another node at random. This locality inductive bias is the basis of the message-passing concept and induces the model to learn more generalizable functions ${ }^{4}$.

b

![](https://cdn.mathpix.com/cropped/2024_05_28_bd3c909ee9f1652ddb8cg-1.jpg?height=590&width=891&top_left_y=1781&top_left_x=1065)

activity predictions of a graph neural network. A scaffold split ensures that no molecules in the training data (purple curve) and test data (blue curve) have the same scaffold. The purpose is to evaluate the model's capability to generalize to a test distribution that is substantially different from the training data, which is expected in real-world applications. Part $\mathbf{b}$ adapted with permission from ref. 67, Elsevier.
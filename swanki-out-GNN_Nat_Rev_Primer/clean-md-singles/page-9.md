\title{
Primer
}

In rational protein design, message-passing-based tools are critical to tackling inverse folding ${ }^{85}$, in which the aim is to reconstruct the amino acid sequence from a 3D point cloud representing a backbone structure. Similar architectures have also been applied to predict the strength of the interaction between molecules. For instance, PiGNet ${ }^{86}$ predicts the affinity between a molecule and the protein it is bound to. For multiple additional drug design-related approaches, GNNs have been used as the base architecture for generative models over molecular structures. Notable examples include generating the most likely 3D structures of small molecules ${ }^{87,88}$ (conformer generation; Fig. 5b); the distribution of protein structures ${ }^{89,90}$ (protein folding); structures used by small molecules to bind to proteins ${ }^{91}$ (molecular docking; Fig. 5b); or structures of novel proteins ${ }^{92,93}$ (rational protein design).

Another common approach to determining the flexibility of biophysical structures is to learn their dynamics and increase their simulation speed. In this setting, GNNs are used as molecular potentials that are trained to predict the energy ${ }^{44,49,50,63}$ of a given atomic structure. Afterwards, the gradient, the predicted force, is used in the simulation to update theatompositions. Othermethods directly predictfutureatom positions ${ }^{94}$ or speed up molecular dynamics simulations by generating abstracted, lower dimensional, coarse-grained molecular representations ${ }^{95}$. GNNs can also undo coarse-grainings in a generative fashion ${ }^{96}$.

\section*{Reproducibility and data deposition}

Data releases and good reproducibility practices have helped develop GNNs. These have been partially driven by standardized benchmarks, such as the $\mathrm{OGB}^{12}$ and Therapeutic Data Commons ${ }^{97}$, which require code to reproduce results to be published. Despite this progress, lack of data is an issue for many life science applications, because data acquisition is more expensive and diverse than in computer vision or natural language processing, in which scraping the internet often suffices for data collection. These challenges highlight the value of collating and open-sourcing more data, alongside developing methods for the low data regime.

\section*{Data sources and benchmarks}

Benchmark suites - such as OGB, Therapeutic Data Commons or the Open Catalyst Project - provide collections of datasets with

a Fragment-based molecular generation

![](https://cdn.mathpix.com/cropped/2024_05_28_c0bf3ea8d2afef31b3f6g-1.jpg?height=590&width=904&top_left_y=1881&top_left_x=127)

Fig. 5 |Examples of GNNs for generative modelling. a, Example of fragment-based molecular generation process similar to ref. 80.b, Representation of the conformer generation and docking tasks. For docking tasks, the target protein to which the standardized train/validation/test sets and evaluation metrics. They come with PyTorch Geometric and Deep Graph Library interfaces for data loaders and evaluation metrics to set up experiments in a comparable and reproducible manner, with online leaderboards to compare state-of-the-art methods. In drug discovery, the Therapeutic Data Commons data collection is notable, with a wide range of tasks, from protein-ligand affinity to retrosynthesis and toxicity prediction.

Another large-scale data collection effort is the Protein Data Bank, which contains over 200,000 protein 3 Datomic structures and has enabled many developments in machine learning for structural biology. Multiple protein structures occur as complexes with small molecules, and PDBBind is an effort to extract and curate structures from the Protein Data Bank with publicly available binding affinity values. A large source of bioactivity data is ChEMBL, which has activity measurements for 2.4 million compounds. Drawing from these sources is the precision medicine knowledge graph ${ }^{7}$, which has relationships between 129,000 nodes, with types ranging from diseases, drugs and genes to anatomical regions and disease exposures. Finally, there are multiple sources of protein-protein interaction graphs, and more information can be found in ref. 98 , which surveys and compares 16 databases.

\section*{Limitations and optimizations Evaluation}

The variety of tasks that can be addressed with GNNs means there is ambiguity in evaluation criteria and a danger of using irrelevant metrics. This is particularly relevant for generative tasks, for which the goodness of an output is difficult to quantify. Whengenerating new drug-like molecules, simple metrics may include chemical validity, synthesizability, diversity and distance from the training data. However, to evaluate more complex biological phenomena, such as biological activity or toxicity, computational estimators can be inaccurate and misleading.

\section*{Data dependence}

Although GNNs are state of the art for many tasks on graph-structured data, they are not the universal best option due to several technical and data limitations. For instance, for some molecular property prediction tasks, molecular fingerprints offer better performance $\mathrm{e}^{10,99}$,
.

![](https://cdn.mathpix.com/cropped/2024_05_28_c0bf3ea8d2afef31b3f6g-1.jpg?height=663&width=904&top_left_y=1804&top_left_x=1050)

ligand is docked is visualized with both the amino acid sequence, which is how many graph neural network (GNN)-based methods represent it, and the surface. Protein structure from Protein Data Bank 6G29.
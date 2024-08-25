it is possible to build fully expressive architectures \({ }^{15}\). Considerations about particular domains will need to be integrated into efficient architectures that do not suffer from bottlenecks.

Methods to interpret GNNs are currently limited to identifying nodes or substructures that most influence a decision. Usually, this is not enough to truly understand the model's reasoning or build surrogate, less-expressive models. Instead, using domain knowledge and multi-modal integrations, interpretability can be directly built into the task the model optimizes for. For example, to predict if a molecule is toxic, instead of framing the task as a simple binary classification, the model could be trained to predict which human proteins the ligand binds to and whether that interaction causes adverse side effects. This prediction is substantially more interpretable and experimentally verifiable than a binary toxicity classification.

Finally, an underexplored GNN application in the life sciences is modelling dynamicgraphs. Many biological phenomena with a graph structure change over time. For instance, brain activity profiles can be modelled as brain networks with signals for nodes that evolve over time, or disease spread can be modelled as a dynamic graph in which better forecasts can have large positive impacts. Temporal graph networks are well researched for applications outside of the life sciences \({ }^{116}\). A promising direction could be applying them to life science problems.

Despite these limitations, GNNs have the capacity to strongly impact many applications in the life sciences and beyond. With new state-of-the-art approaches in fields from drug and antibiotic discovery and traffic prediction to structural biology and recommendation systems, it is expected that the application of GNNs, in their current and future forms, will enable discoveries and the development of a wide variety of new products.

\section*{Code availability}

Example code can be found at https://github.com/HannesStark/ GNN-primer/blob/main/GNN-primer_HIV_classification.ipynb.

Published online: 07 March 2024

\section*{References}

1. Gori, M., Monfardini, G. \& Scarselli, F. A new model for learning in graph domains. In Proceedings 2005 IEEE International Joint Conference Neural Networks 729-734 (IEEE, 2005).

2. Merkwirth, C. \& Lengauer, T. Automatic generation of complementary descriptors with molecular graph networks. J. Chem. Inf. Model. 45, 1159-1168 (2005).

3. Scarselli, F., Gori, M., Tsoi, A. C., Hagenbuchner, M. \& Monfardini, G. The graph neural network model. IEEE Trans. Neural Netw. 20, 61-80 (2008).

Although the genealogy of the development is multifaced, this is often considered as the first instance of GNNs.

4. Bronstein, M. M., Bruna, J., Cohen, T. \& Veličković, P. Geometric deep learning: grids, groups, graphs, geodesics, and gauges. Preprint at https://doi.org/10.48550/ arXiv.2104.13478 (2021).

Book with a very comprehensive introduction to the theoretical aspects behind GNNs and other geometric deep learning architectures.

5. Jegelka, S. Theory of graph neural networks: representation and learning. Preprint at https://doi.org/10.48550/arXiv.2204.07697 (2022).

6. Morgan, H. L. The generation of a unique machine description for chemical structures-a technique developed at chemical abstracts service. J. Chem. Doc. 5, 107-113 (1965).

7. Chandak, P., Huang, K. \& Zitnik, M. Building a knowledge graph to enable precision medicine. Sci. Data 10, 67 (2023).

8. Fey, M. \& Lenssen, J. E. Fast graph representation learning with PyTorch Geometric. Preprint at https://doi.org/10.48550/arXiv.1903.02428 (2019). PyTorch Geometric is the most widely used library to develop GNNs.

9. Wang, M. et al. Deep Graph Library: a graph-centric, highly-performant package for graph neural networks. Preprint at https://doi.org/10.48550/arXiv.1909.01315 (2019).

10. Yang, K. et al. Analyzing learned molecular representations for property prediction. J. Chem. Inf. Model. 59, 3370-3388 (2019).

11. Geiger, M. \& Smidt, T. e3nn: Euclidean neural networks. Preprint at https://doi.org/ 10.48550/arXiv.2207.09453 (2022).
12. Hu, W. et al. Open Graph Benchmark: datasets for machine learning on graphs. Adv. Neural Inf. Process. Syst. 22118-22133 (NeurIPS Proceedings, 2020). OGB is the most widely used benchmark for GNNs with a wide variety of datasets, each with its own leaderboard.

13. Dummit, D. S. \& Foote, R. M. Abstract algebra 7th edn (Wiley, 2004).

14. Xu, K., Hu, W., Leskovec, J. \& Jegelka, S. How powerful are Graph Neural Networks? In International Conference on Learning Representations (ICLR, 2019).

To our knowledge, this work, concurrently with [Mor+19], was the first to propose and use the analogy of GNNs to WL isomorphism test to study their expressivity.

15. Morris, C. et al. Weisfeiler and Leman go neural: higher-order graph neural networks, Proc. AAAI Conf. Artif. Intell. 33, 4602-4609 (2019).

16. Vignac, C., Loukas, A. \& Frossard, P. Building powerful and equivariant graph neural networks with structural message-passing. Adv. Neural Inf. Process. Syst. 33, 14143-14155 (2020).

17. Abboud, R., Ceylan, I.I., Grohe, M. \& Lukasiewicz, T. The surprising power of graph neural networks with random node initialization. In 3Oth International Joint Conferences on Artificial Intelligence 2112-2118 (International Joint Conferences on Artificial Intelligence Organization, 2021).

18. Sato, R., Yamada, M. \& Kashima, H. Random features strengthen graph neural networks. In Proceedings of the 2021 SIAM International Conference on Data Mining 333-341 (Society for Industrial and Applied Mathematics, 2021).

19. Dwivedi, V. P. et al. Benchmarking graph neural networks. J. Mach. Learn. Res. 24, 1-48 (2023).

20. Beaini, D. et al. Directional graph networks. In Proceedings of the 38th International Conference on Machine Learning 748-758 (PMLR, 2021).

21. Lim, D. et al. Sign and basis invariant networks for spectral graph representation learning. In International Conference on Learning Representations (ICLR, 2O23).

22. Keriven, N. \& Vaiter, S. What functions can Graph Neural Networks compute on random graphs? The role of Positional Encoding. Preprint at https://doi.org/10.48550/ arXiv.2305.14814 (2023).

23. Zhang, B., Luo, S., Wang, L. \& He, D. Rethinking the expressive power of GNNs via graph biconnectivity. In International Conference on Learning Representations (ICLR, 2023).

24. Di Giovanni, F. et al. How does over-squashing affect the power of GNNs? Preprint at https://doi.org/10.48550/arXiv.2306.03589 (2023).

25. Razin, N., Verbin, T. \& Cohen, N. On the ability of graph neural networks to model interactions between vertices. In 37th Conference on Neural Information Processing Systems (NeurIPS, 2023).

26. Bouritsas, G., Frasca, F., Zafeiriou, S. \& Bronstein, M. M. Improving graph neural network expressivity via subgraph isomorphism counting. IEEE Trans. Pattern Anal. Mach. Intell. 45, 657-668 (2023).

27. Sun, Z., Deng, Z.-H., Nie, J.-Y. \& Tang, J. RotatE: knowledge graph embedding by relational rotation in complex space. Preprint at https://doi.org/10.48550/arXiv.1902.10197 (2019).

28. Abboud, R., Ceylan, I., Lukasiewicz, T. \& Salvatori, T. BoxE: a box embedding model for knowledge base completion. Adv. Neural Inf. Process. Syst. 33, 9649-9661 (2020).

29. Pavlović, A. \& Sallinger, E. ExpressivE: a spatio-functional embedding for knowledge graph completion. In International Conference on Learning Representations (ICLR, 2023).

30. Veličković, P. et al. Graph attention networks. In International Conference on Learning Representations (ICLR, 2017).

Graph attention networks are the first application of the idea of attention to graphs, and they are one of the most widely used architectures to date.

31. Corso, G., Cavalleri, L., Beaini, D., Liò, P. \& Veličković, P. Principal neighbourhood aggregation for graph nets. Adv. Neural Inf. Process. Syst. 33, 13260-13271 (2020).

32. Gasteiger, J., Weißenberger, S. \& Günnemann, S. Diffusion improves graph learning Adv. Neural Inf. Process. Syst. 32, 13366-13378 (2019).

33. Gutteridge, B., Dong, X., Bronstein, M. \& Di Giovanni, F. DRew: dynamically rewired message passing with delay. In International Conference on Machine Learning (eds Krause, A. et. al.) 12252-12267 (ICML, 2O23).

34. Rampášek, L. et al. Recipe for a general, powerful, scalable graph transformer. Adv. Neural Inf. Process. Syst. 35, 14501-14515 (2022)

35. Dwivedi, V. P. et al. Long range graph benchmark. Adv. Neural Inf. Process. Syst. 35 22326-22340 (2022)

36. Dwivedi, V. P. \& Bresson, X. A generalization of transformer networks to graphs. Preprint at https://doi.org/10.48550/arXiv.2012.09699 (2020).

37. Kreuzer, D., Beaini, D., Hamilton, W., Létorneau, V. \& Tossou, P. Rethinking graph transformers with spectral attention. Adv. Neural Inf. Process. Syst. 34, 21618-21629 (2O21).

38. Bodnar, C. et al. Weisfeiler and Lehman go topological: message passing simplicial networks. In Proceedings of the 38th International Conference on Machine Learning (eds Meila, M. \& Zhang, T.) 1026-1037 (PMLR, 2021).

39. Bodnar, C. et al. Weisfeiler and Lehman go cellular: cw networks. Adv. Neural Inf. Process. Syst. 34, 2625-2640 (2021).

40. Chamberlain, B. et al. Grand: graph neural diffusion. In Proceedings of the 38th International Conference on Machine Learning (eds Meila, M. \& Zhang, T.) 1407-1418 (PMLR, 2021).

41. Chamberlain, B. et al. Beltrami flow and neural diffusion on graphs. Adv. Neural Inf Process. Syst. 34, 1594-1609 (2021).

42. Di Giovanni, F., Rowbottom, J., Chamberlain, B. P., Markovich, T. \& Bronstein, M. M. Graph neural networks as gradient flows. Preprint at https://doi.org/10.48550/arXiv.2206.10991 (2022).
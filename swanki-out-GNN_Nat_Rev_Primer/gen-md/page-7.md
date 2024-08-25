### Card 1

## Explain the significance of SE(3) invariance/equivariance in 3D graph-based models and how it pertains to the special Euclidean group.

The symmetry of a task with respect to translations and rotations in three-dimensional space is crucial for models dealing with 3D graph-based data such as molecular structures. This symmetry translates into SE(3) invariance or equivariance, where $\mathrm{SE}(3)$ represents the special Euclidean group in three dimensions ($\mathbb{R}^3$), encompassing all possible rotations and translations. SE(3)-invariance ensures that the model's predictions remain consistent regardless of the spatial orientation or position of the input data, which is particularly beneficial for accurately capturing geometric properties in 3D space.

- #machine-learning, #geometry.scientific-computing

---

### Card 2

## What is one way to achieve SE(3)-invariant message-passing in graphs, and why is it necessary?

To achieve SE(3)-invariant message-passing in graphs, one can extract relative distances between pairs of nodes and use these as edge features. This method is necessary because traditional coordinates or relative vectors as input features are problematic; they would change with translations or rotations of the frame of reference, leading to inconsistent model outputs.

- ## machine-learning, ## graphs.seinvariance

---

### Card 3

## What does the higher-order strategy in SE(3)-invariant architectures involve, and why is it used?

The higher-order strategy involves incorporating $\mathrm{SE}(3)$-invariant scalar features, $\mathrm{SE}(3)$-equivariant vectors, and higher-order representations in the hidden node representations. These complex features can encode physical properties but require specific equivariant operations like tensor products. The strategy is used to create more powerful and expressive models capable of capturing intricate relationships in the data.

- #machine-learning, #graphs.higher-order

---

### Card 4

## Describe the multi-hop interaction strategy for SE(3)-invariant GNNs and its components.

The multi-hop interaction strategy in SE(3)-invariant GNNs utilizes not just distances between pairs of nodes but also the angles between pairs of connected edges and dihedral angles between three consecutive edges. These additional features allow the model to capture complex relationships that simple pairwise distances might miss, resulting in more expressive and informative architectural designs.

- #machine-learning, #graphs.multi-hop

---

### Card 5

## What are two common strategies for interpretability in GNNs, and how do they function?

The two common strategies for interpretability in GNNs are gradient-based methods and perturbation-based methods. Gradient-based methods analyze the gradient of the loss with respect to input features to determine which features most affect the output. Perturbation-based methods, such as GNNExplainer, make modifications to the input data to see which subgraph and features are most crucial for the prediction.

- #machine-learning, #graphs.interpretability

---

### Card 6

## Explain the challenges of uncertainty estimation in GNNs and the tailored techniques developed to address these issues.

Uncertainty estimation in GNNs is challenging due to the data's graph structure, where epistemic uncertainty can arise from node features or incorrect/missing edges. The propagation of uncertainty through layers differs from simpler architectures, complicating traditional uncertainty estimation methods. Tailored techniques include custom Bayesian node updates and topology-dependent correction steps for disentangling epistemic and aleatoric uncertainty, addressing the unique challenges posed by GNNs.

- #machine-learning, #graphs.uncertainty-estimation

---


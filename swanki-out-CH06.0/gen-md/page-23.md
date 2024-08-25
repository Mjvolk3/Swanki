### Card 1
We see an image depicting three different contrastive learning paradigms. Focusing on part (a), explain what the instance discrimination approach is and how the positive pairs and negative pairs are treated in this method.

In the instance discrimination approach, the positive pair is made up of the anchor and an augmented version of the same image. The representations of these positive pairs are mapped to points in a normalized space, often visualized as a unit hypersphere. The primary objective of this method is to minimize the distance between these positive pairs while maximizing the distance between negative pairs (different images). This can be visualized using colored arrows which indicate the loss encourages this behavior.

- #contrastive-learning, #instance-discrimination

### Card 2
In supervised contrastive learning (as depicted in Figure 6.14(b)), what constitutes a positive pair and how does this method differ from instance discrimination?

In supervised contrastive learning, the positive pair consists of two different images from the same class. Unlike instance discrimination, which uses augmented versions of the same image, supervised contrastive learning leverages class labels to define positive pairs. This method incorporates supervised information to encourage representations of semantically similar images to be closer together.

- #contrastive-learning, #supervised-contrastive-learning

### Card 3
In the generalized network architecture described, what equation defines the output of a unit, and what do the variables in this equation represent?

The output $z_{k}$ of a unit in the generalized network architecture is defined by

$$
z_{k}=h\left(\sum_{j \in \mathcal{A}(k)} w_{k j} z_{j}+b_{k}\right)
$$

where $\mathcal{A}(k)$ denotes the set of ancestors of node $k$ (units sending connections to unit $k$), $w_{k j}$ are the weights, $b_{k}$ denotes the associated bias parameter, and $h$ is the activation function. This setup ensures that the network follows a feed-forward architecture without closed directed cycles.

- #neural-networks, #general-network-architectures

### Card 4
Why must complex neural network diagrams be restricted to a feed-forward architecture without closed directed cycles?

Complex neural network diagrams must be restricted to a feed-forward architecture with no closed directed cycles to ensure that the outputs are deterministic functions of the inputs. This restriction guarantees that each unit's activation can be computed in a sequential manner, without depending on future states, thereby avoiding potential issues like infinite loops and making the network's behavior predictable.

- #neural-networks, #network-architecture

### Card 5
Describe the components and purpose of the CLIP model as described in Figure 6.14(c).

The CLIP model pairs an image with an associated text snippet to form a positive pair. The purpose of this model is to leverage multimodal data (images and text) to learn joint representations. This approach allows the model to understand and align features across different modalities, which can enhance tasks like zero-shot learning and improve performance on visually-grounded tasks.

- #contrastive-learning, #CLIP-model, #multimodal-learning

### Card 6
In the context of the equation $z_{k}=h\left(\sum_{j \in \mathcal{A}(k)} w_{k j} z_{j}+b_{k}\right)$, how does the "set of ancestors" $\mathcal{A}(k)$ function in computing the activations in a neural network?

The set of ancestors $\mathcal{A}(k)$ includes all units that send connections to the unit $k$. When computing the activations for unit $k$, each ancestor unit $j$ contributes to the weighted sum $\sum_{j \in \mathcal{A}(k)} w_{k j} z_{j}$, which is then passed through an activation function $h$ along with a bias term $b_{k}$ to produce the output $z_{k}$. This hierarchical structure ensures that the forward pass of activations proceeds layer by layer from input to output.

- #neural-networks, #activation-functions
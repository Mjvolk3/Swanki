### Card 1

## What role did unsupervised learning historically play in the successful training of deep networks, aside from convolutional networks?

Unsupervised learning historically enabled the successful training of deep networks by pre-training each layer using unsupervised learning before further training the entire network using gradient-based supervised training. This approach made it possible to train deep networks even before the advent of training directly from scratch purely using supervised learning given appropriate conditions.

- #deep-learning, #unsupervised-learning

---

### Card 2

## Explain the concept of transfer learning and provide an example related to image classification.

Transfer learning involves using the internal representation learned for one task to improve performance on a related task with limited training data. For example, a network pre-trained on a large dataset of everyday objects can transform image representations and then retrain the final classification layer using a smaller dataset of skin lesion images, achieving better accuracy than training solely on the lesion dataset.

- #deep-learning, #transfer-learning.image-classification

---

### Card 3

## Under what conditions might you re-train only the final layer of a network in the context of transfer learning?

When the data for task A is very scarce, one might retrain only the final layer of the network. This is because the internal representations and lower layers, which were pre-trained on task B, remain useful and only minimal adaptation is required, making it computationally efficient.

- #deep-learning, #transfer-learning.scarce-data

---

### Card 4

## Describe how iterative gradient-based optimization can be applied in transfer learning.

In transfer learning, instead of applying stochastic gradient descent to the entire network, it is more efficient to pass the new training data through the fixed pre-trained network to evaluate the new representation. Then, iterative gradient-based optimization can be applied to just the smaller network consisting of the final layers, which minimizes computational effort.

- #deep-learning, #transfer-learning.gradient-opt

---

### Card 5

## What is fine-tuning in the context of transfer learning, and when is it generally applied?

Fine-tuning in transfer learning involves adapting the entire network to the data for task A at a lower learning rate. This technique is generally applied when more data is available, and a more comprehensive tuning of the network is deemed necessary.

- #deep-learning, #transfer-learning.fine-tuning

---

### Card 6

## What considerations should be made when deciding to use pre-training and representation learning for a new task?

When using pre-training and representation learning for a new task, considerations include the quantity and quality of available data for both the new and related tasks, the computational resources required, the similarity between tasks, and the appropriateness of pre-trained features for the new task. A higher level of pre-training and representation learning is typically more beneficial in cases of scarce training data and when tasks share significant commonalities.

- #deep-learning, #transfer-learning.representation-learning


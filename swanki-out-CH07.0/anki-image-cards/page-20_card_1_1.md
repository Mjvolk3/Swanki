## 

How are mean and variance computed differently in batch normalization and layer normalization in a neural network?

![](https://cdn.mathpix.com/cropped/2024_05_26_f174c62110b43edc3276g-1.jpg?height=788&width=1490&top_left_y=216&top_left_x=168)

%

In batch normalization, the mean and variance are computed across the mini-batch separately for each hidden unit. In layer normalization, the mean and variance are computed across the hidden units for each individual data point within the batch, independently of the batch size.

- #deep-learning, #neural-networks.normalization, #batch-vs-layer-normalization

## 

What are the advantages of layer normalization over batch normalization, particularly in specific types of neural networks?

![](https://cdn.mathpix.com/cropped/2024_05_26_f174c62110b43edc3276g-1.jpg?height=788&width=1490&top_left_y=216&top_left_x=168)

%

Layer normalization is independent of batch size, making it particularly useful for recurrent neural networks (RNNs) or when training on multiple GPUs, where maintaining consistent mini-batch statistics can be challenging.

- #deep-learning, #neural-networks.advantages, #layer-normalization
## Hidden units $\left\{\begin{array}{|l|l|l|ll}\hline & & & & C \\ \hline & & & & \\ \hline & & & & \square \\ \hline & & & & \square \\ \hline & & & & \square \\ \hline\end{array}\right.$ (a)

![](https://cdn.mathpix.com/cropped/2024_05_26_f174c62110b43edc3276g-1.jpg?height=788&width=1490&top_left_y=216&top_left_x=168)

What is the key difference between batch normalization and layer normalization in neural networks as illustrated?

%

In batch normalization (a), the mean and variance are computed across the mini-batch separately for each hidden unit, normalizing the activations within each mini-batch. In layer normalization (b), the mean and variance are computed across the hidden units separately for each data point, ensuring normalization per layer, independent of batch size.

- #deep-learning, #neural-networks.batch-normalization, #neural-networks.layer-normalization

---

## How is normalization conducted in layer normalization compared to batch normalization in neural networks?

![](https://cdn.mathpix.com/cropped/2024_05_26_f174c62110b43edc3276g-1.jpg?height=788&width=1490&top_left_y=216&top_left_x=168)

%

In layer normalization, normalization is conducted by computing the mean and variance across the hidden units separately for each data point within the batch, making it independent of the mini-batch size. In batch normalization, the mean and variance are computed across the mini-batch separately for each hidden unit.

- #deep-learning, #neural-networks.layer-normalization, #neural-networks.batch-normalization
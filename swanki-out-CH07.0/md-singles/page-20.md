Hidden units \(\left\{\begin{array}{|l|l|l|ll}\hline & & & & C \\ \hline & & & & \\ \hline & & & & \square \\ \hline & & & & \square \\ \hline & & & & \square \\ \hline\end{array}\right.\)

(a)

![](https://cdn.mathpix.com/cropped/2024_05_26_f174c62110b43edc3276g-1.jpg?height=788&width=1490&top_left_y=216&top_left_x=168)

(b)

Figure 7.8 Illustration of batch normalization and layer normalization in a neural network. In batch normalization, shown in (a), the mean and variance are computed across the mini-batch separately for each hidden unit. In layer normalization, shown in (b), the mean and variance are computed across the hidden units separately for each data point.

reduce its representational capability. We can compensate for this by re-scaling the pre-activations of the batch to have mean \(\beta_{i}\) and standard deviation \(\gamma_{i}\) using

\[
\widetilde{a}_{n i}=\gamma_{i} \widehat{a}_{n i}+\beta_{i}
\]

where \(\beta_{i}\) and \(\gamma_{i}\) are adaptive parameters that are learned by gradient descent jointly with the weights and biases of the network. These learnable parameters represent a key difference compared to input data normalization.

It might appear that the transformation (7.55) has simply undone the effect of the batch normalization since the mean and variance can now adapt to arbitrary values again. However, the crucial difference is in the way the parameters evolve during training. For the original network, the mean and variance across a mini-batch are determined by a complex function of all the weights and biases in the layer, whereas in the representation given by (7.55), they are determined directly by independent parameters \(\beta_{i}\) and \(\gamma_{i}\), which turn out to be much easier to learn during gradient descent.

Equations (7.52) - (7.55) describe a transformation of the variables that is differentiable with respect to the learnable parameters \(\beta_{i}\) and \(\gamma_{i}\). This can be viewed as an additional layer in the neural network, and so each standard hidden layer can be followed by a batch normalization layer. The structure of the batch-normalization process is illustrated in Figure 7.8.

Once the network is trained and we want to make predictions on new data, we
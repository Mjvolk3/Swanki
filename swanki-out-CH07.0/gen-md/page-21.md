### Card 1

## How are moving averages for mean and variance computed in the training phase in the context of batch normalization?

The moving averages for mean, $\mu_{i}$, and variance, $\sigma_{i}^{2}$, during the training phase in batch normalization are computed as follows:

$$
\begin{aligned}
& \bar{\mu}_{i}^{(\tau)}=\alpha \bar{\mu}_{i}^{(\tau-1)}+(1-\alpha) \mu_{i} \\
& \bar{\sigma}_{i}^{(\tau)}=\alpha \bar{\sigma}_{i}^{(\tau-1)}+(1-\alpha) \sigma_{i}
\end{aligned}
$$

where $0 \leqslant \alpha \leqslant 1$.

These moving averages play no role during training but are used to process new data points during the inference phase.

- #neural-networks, #batch-normalization

---

### Card 2

## Explain the motivation behind batch normalization and discuss why it might be effective in practice.

Batch normalization was originally motivated by noting that updates to weights in earlier layers of the network change the distribution of values seen by later layers, a phenomenon called internal covariate shift. This involves normalizing the inputs of each layer.

However, later studies (Santurkar et al., 2018) suggest that batch normalization improves training not because it addresses covariate shift, but because it improves the smoothness of the error function landscape.

- #neural-networks, #batch-normalization, #training

---

### Card 3

## What are some limitations of batch normalization, and how does layer normalization address these limitations?

With batch normalization, if the batch size is too small, the estimates of mean and variance become too noisy. Additionally, for very large training sets, minibatches may be split across different GPUs, rendering global normalization across the minibatch inefficient.

Layer normalization addresses these limitations by normalizing across the hidden-unit values for each data point separately, rather than across the batch:

$$
\begin{aligned}
\mu_{n} & =\frac{1}{M} \sum_{i=1}^{M} a_{n i} \\
\sigma_{n}^{2} & =\frac{1}{M} \sum_{i=1}^{M}\left(a_{n i}-\mu_{n}\right)^{2} \\
\widehat{a}_{n i} & =\frac{a_{n i}-\mu_{n}}{\sqrt{\sigma_{n}^{2}+\delta}}
\end{aligned}
$$

- #neural-networks, #batch-normalization, #layer-normalization

---

### Card 4

## Provide the equations for the mean ($\mu_{n}$) and variance ($\sigma_{n}^{2}$) under layer normalization.

Under layer normalization, the mean $\mu_{n}$ and variance $\sigma_{n}^{2}$ for each data point are computed as follows:

$$
\begin{aligned}
\mu_{n} & =\frac{1}{M} \sum_{i=1}^{M} a_{n i} \\
\sigma_{n}^{2} & =\frac{1}{M} \sum_{i=1}^{M}\left(a_{n i}-\mu_{n}\right)^{2}
\end{aligned}
$$

Where $i = 1, \ldots, M$ represents all hidden units in the layer.

- #neural-networks, #layer-normalization

---

### Card 5

## How does layer normalization normalize the hidden-unit values for each data point?

Layer normalization normalizes the hidden-unit values for each data point by using the following transformation:

$$
\widehat{a}_{n i} =\frac{a_{n i}-\mu_{n}}{\sqrt{\sigma_{n}^{2}+\delta}}
$$

where $\mu_{n}$ and $\sigma_{n}^{2}$ are the mean and variance of the hidden unit values for the data point.

- #neural-networks, #layer-normalization

---

### Card 6

## In the context of neural networks, what flexibility do trainable parameters introduce during normalization?

Both batch normalization and layer normalization allow for additional learnable mean ($\beta$) and standard deviation ($\gamma$) parameters to be introduced for each hidden unit separately. This adds flexibility to the normalization process, enabling the model to shift and scale the normalized values appropriately:

$$
\hat{a}'_{n i} = \gamma \widehat{a}_{n i} + \beta
$$

This modified normalization function is employed both during training and inference.

- #neural-networks, #batch-normalization, #layer-normalization
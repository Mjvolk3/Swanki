## Explain how the $K$-nearest neighbour method classifies a new data point.

In the $K$-nearest neighbour (KNN) classification, a new data point (test point $\mathbf{x}$) is classified by identifying the $K$ nearest training data points. The new point is then assigned to the most frequently occurring class among these $K$ points. This method thereby leverages the local class density to make predictions.

$$
p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)=\frac{p\left(\mathbf{x} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right)}{p(\mathbf{x})}=\frac{K_{k}}{K}
$$

Here, the posterior probability $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$ is proportional to the number of nearest neighbours $K_k$ belonging to class $\mathcal{C}_k$, out of the total $K$ nearest neighbours.

- #machine-learning, #classification.k-nearest-neighbour

## How does the decision boundary in the nearest-neighbour $(K=1)$ classifier work?

In the nearest-neighbour $(K=1)$ classifier, the decision boundary is formed by hyperplanes that are perpendicular bisectors of pairs of nearest data points that belong to different classes. This structure results in a boundary that non-linearly partitions the feature space, adapting closely to the data distribution.

- #machine-learning, #classification.nearest-neighbour

## What is the relationship between the posterior probability of class membership in KNN and the ratio $\frac{K_k}{K}$?

In the context of KNN, the posterior probability $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$ for a class $\mathcal{C}_k$, given the test point $\mathbf{x}$, is directly proportional to the ratio $\frac{K_k}{K}$. Here, $K_k$ represents the number of nearest neighbours among the $K$ that belong to class $\mathcal{C}_k$. This proportionality exploits the empirical frequency of the classes among the nearest neighbours to estimate the likelihood of class membership.

$$
p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)=\frac{K_{k}}{K}
$$

Thus, the classification decision aligns with assigning $\mathbf{x}$ to the class with the highest proportion of nearest neighbours.

- #probability, #statistics.k-nearest-neighbour, #machine-learning

## How does the error rate of the nearest-neighbour $(K=1)$ classifier compare to the optimal classifier as $N \rightarrow \infty$?

For the nearest-neighbour $(K=1)$ classifier, it has been shown that the error rate approaches at most twice the error rate of an optimal classifier, which exploits the true class distributions, as the number of training samples $N \rightarrow \infty$. This characteristic underscores the robust performance of the K=1 classifier in large sample scenarios, demonstrating significant efficacy in practical settings despite its simplicity.

- #machine-learning, #classification.nearest-neighbour, #theoretical-bounds

## Discuss the storage requirements and computational expense of the $K$-nearest neighbour method.

The $K$-nearest neighbour method necessitates retaining the entire training dataset in memory to facilitate classification of new data points. This requirement leads to significant storage demands, particularly for large datasets, and impacts the computational efficiency during the classification phase, as each query involves a search over the entire training set to find the nearest neighbours.

- #machine-learning, #classification.k-nearest-neighbour, #computational-efficiency
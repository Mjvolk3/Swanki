## Discuss Bayes' theorem in terms of the numerator's quantities.

Bayes' theorem can be found in terms of the quantities in the numerator using:
$$
p(\mathbf{x})=\sum_{k} p\left(\mathbf{x} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right)
$$

## Explain Approach (a) for solving classification problems.

Approach (a) involves finding the joint distribution over both $\mathbf{x}$ and $\mathcal{C}_{k}$.

It includes the following steps:
1. Estimating class priors $p(\mathcal{C}_{k})$ 
2. Estimating class-conditional densities $p(\mathbf{x} \mid \mathcal{C}_{k})$
3. Using these estimates to compute the marginal density $p(\mathbf{x})$

This allows for:
- Outlier or novelty detection
- Detection of new data points with low probabilities under the model

- #statistics, #machine-learning, #classification

## Explain Approach (b) and its computational advantages.

Approach (b) directly models the posterior class probabilities $p(\mathcal{C}_{k} \mid \mathbf{x})$.

Steps:
1. Solve the inference problem to determine $p(\mathcal{C}_{k} \mid \mathbf{x})$
2. Use decision theory to assign each new $\mathbf{x}$ to one of the classes

Advantages:
- Avoids estimating high-dimensional joint distributions
- Reduces computational resource requirements
- Focused directly on making classification decisions

- #machine-learning, #classification, #decision-theory

## Explain Approach (c) and its simplicity compared to (a) and (b).

Approach (c) finds a discriminant function $f(\mathbf{x})$ that maps each input $\mathbf{x}$ directly onto a class label.

Steps:
1. Train a model to find $f(\mathbf{x})$
2. Use $f(\mathbf{x})$ to directly get class labels for new inputs

Advantages:
- Integrates the inference and decision stages into a single step
- Simplifies the learning problem

Example:
For two-class problems, $f(\cdot)$ is binary-valued, where $f=0$ represents class $\mathcal{C}_{1}$ and $f=1$ represents class $\mathcal{C}_{2}$.

- #machine-learning, #classification, #discriminant-functions

## Discuss the relative merits of generative vs. discriminative approaches in machine learning.

Generative approaches (e.g., (a)):
- Model the input-output distribution
- Useful for tasks like outlier detection
- May require large training sets for high-dimensional $\mathbf{x}$

Discriminative approaches (e.g., (b)):
- Directly model posterior probabilities
- More efficient for classification tasks
- Avoid the complexity of modeling high-dimensional inputs

Many studies explore combining both approaches for robust machine learning solutions (e.g., Jebara, 2004; Lasserre, Bishop, Minka, 2006).

- #machine-learning, #generative-models, #discriminative-models

## Discuss how class priors $p(\mathcal{C}_{k})$ can be estimated and their role.

Class priors $p(\mathcal{C}_{k})$ often estimated from the fractions of the training set data points in each class.

Role:
- In generative models (e.g., (a)), combined with class-conditional densities to compute marginal density.
- Affect posterior probabilities $p(\mathcal{C}_{k} \mid \mathbf{x})$ computed in Approach (b).

Example:
If class $\mathcal{C}_{k}$ appears 30% of the time in training data, then $p(\mathcal{C}_{k}) = 0.3$.

- #statistics, #bayes-theorem, #machine-learning

## Discuss novelty detection and marginal density $p(\mathbf{x})$ in Approach (a).

Approach (a) allows for the determination of marginal density $p(\mathbf{x})$ using:
$$
p(\mathbf{x})=\sum_{k} p\left(\mathbf{x} \mid \mathcal{C}_{k}\right) p\left(\mathcal{C}_{k}\right)
$$

Applications:
- Detect new data points having low probability densities under the model.
- Useful for novelty or outlier detection.

Referenced works:
- Bishop, 1994
- Tarassenko, 1995

- #statistics, #novelty-detection, #classification
## Given the least-squares solution for a function

$$
\mathbf{y}(\mathbf{x})=\widetilde{\mathbf{W}}^{\mathrm{T}} \widetilde{\mathbf{x}}=\mathbf{T}^{\mathrm{T}}\left(\widetilde{\mathbf{X}}^{\dagger}\right)^{\mathrm{T}} \widetilde{\mathbf{x}}
$$

Show that for any target vector $\mathbf{t}_n$ satisfying a linear constraint $\mathbf{a}^{\mathrm{T}} \mathbf{t}_{n} + b = 0$, the model prediction $\mathbf{y}(\mathbf{x})$ satisfies $\mathbf{a}^{\mathrm{T}} \mathbf{y}(\mathbf{x}) + b = 0$.

The proof starts with the assumed linear constraint and uses the given least-squares solution form.

$$
\mathbf{a}^{\mathrm{T}} \mathbf{t}_{n} + b = 0 \implies \mathbf{a}^{\mathrm{T}} \mathbf{T}^{\mathrm{T}} (\widetilde{\mathbf{X}}^{\dagger})^{\mathrm{T}} \widetilde{\mathbf{x}} + b = 0 \implies \mathbf{a}^{\mathrm{T}} \mathbf{y}(\mathbf{x}) + b = 0
$$

This completes the proof that the model prediction upholds the same linear constraint as the target vector.

- #math.linear-algebra, #machine-learning.models, #least-squares

## Show that if we use a 1-of-$K$ coding scheme for $K$ classes in the least-squares solution, the elements of $\mathbf{y}(\mathbf{x})$ will sum to 1.

By using the linear constraint from the target vectors, we reach the following summation result.

Section 2.3 .4 mentions $$
\mathbf{a}^{\mathrm{T}} \mathbf{y}(\mathbf{x}) + b = 0
$$

If $\mathbf{y}(\mathbf{x})$ elements sum to 1 and $\mathbf{a} = \mathbf{1}$, then 

$$
\sum_{k=1}^{K} y_{k}(\mathbf{x}) = 1
$$

This result ensures the sum constraint for the least-squares solutions using a 1-of-$K$ coding scheme.

- #math.statistics, #machine-learning.coding-schemes, #least-squares

## Explain why the least-squares approach suffers from severe problems even when used as a discriminant function without probabilistic interpretation.

The least-squares method is sensitive to the distribution and presence of outliers, which affects its robustness. 

This is emphasized by its underpinning sum-of-squares error function: 

$$
E(\mathbf{W}) = \frac{1}{2} \sum_{n=1}^{N} \left(\mathbf{y}(\mathbf{x}_n) - \mathbf{t}_n\right)^2
$$

This leads to issues when data is not Gaussian distributed, impacting decision boundaries adversely when outliers are present.

- #machine-learning.robustness, #statistics.error-functions, #least-squares

## Describe an issue with using least-squares under the assumption of Gaussian noise distribution when it is markedly different for the true data.

Least-squares corresponds to the maximum likelihood under the Gaussian noise assumption. If the data is not Gaussian, this misalignment will cause poor classification performance, especially sensitive to outliers.

$$
P(\mathbf{t}|\mathbf{x}, \mathbf{W}) = \mathcal{N}(\mathbf{t}|\mathbf{y}(\mathbf{x}), \sigma^2)
$$

Where $\mathcal{N}$ denotes the Gaussian distribution.

- #statistics.noise-distributions, #machine-learning.assumptions, #least-squares

## Highlight how logistic regression demonstrates more robustness compared to least-squares according to Figure 5.4.

Logistic regression is less sensitive to outliers compared to least-squares, demonstrating better decision boundary stability as illustrated in Figure 5.4. This robustness is due to its probabilistic framework:

$$
\text{Logistic Regression: } \sigma(\mathbf{w}^\mathrm{T} \mathbf{x}) \text{, where } \sigma(z) = \frac{1}{1+e^{-z}}
$$

Compared to the sum-of-squares error giving undue weight to outliers.

- #machine-learning.logistic-regression, #statistics.robustness, #least-squares

## Discuss how probabilistic models improve classification techniques over least-squares and pave the way for flexible nonlinear neural network models.

By using probabilistic models, one can adjust assumptions to better fit the data structure, reducing sensitivity to outliers and allowing flexibility in modeling.

Future sections will delve into

$$
P(\mathbf{t}|\mathbf{x}, \mathbf{W}) = \mathcal{N}(\mathbf{t}|\mathbf{y}(\mathbf{x}), \sigma^2)
$$

Transforming this into neural networks for better flexibility and prediction accuracy.

- #machine-learning.neural-networks, #statistics.probability-models, #least-squares
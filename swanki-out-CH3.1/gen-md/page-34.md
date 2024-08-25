## How is the likelihood function for a dataset $\mathbf{X}$ expressed in terms of the function $h$, the function $g$, and the statistic function $\mathbf{u}$?
Given a dataset $\mathbf{X} = \{\mathbf{x}_1, \ldots, \mathbf{x}_n\}$, the likelihood function is expressed as:
$$
p(\mathbf{X} \mid \boldsymbol{\eta}) = \left(\prod_{n=1}^{N} h(\mathbf{x}_n)\right) g(\boldsymbol{\eta})^N \exp \left\{\boldsymbol{\eta}^\mathrm{T} \sum_{n=1}^{N} \mathbf{u}(\mathbf{x}_n)\right\}
$$
where $h(\mathbf{x}_n)$ is a function specific to each data point, $g(\boldsymbol{\eta})$ is a function of the parameter vector $\boldsymbol{\eta}$, and $\mathbf{u}(\mathbf{x}_n)$ is a statistic function of the data point $\mathbf{x}_n$.
- #statistics, #likelihood-function, #mathematical-modeling

## What is the condition for the maximum likelihood estimator $\boldsymbol{\eta}_{\mathrm{ML}}$ derived from the gradient of the log-likelihood?
The condition for finding the maximum likelihood estimator $\boldsymbol{\eta}_{\mathrm{ML}}$ is obtained by setting the gradient of $\ln p(\mathbf{X} \mid \boldsymbol{\eta})$ with respect to $\boldsymbol{\eta}$ to zero:
$$
-\nabla \ln g(\boldsymbol{\eta}_{\mathrm{ML}}) = \frac{1}{N} \sum_{n=1}^{N} \mathbf{u}(\mathbf{x}_n)
$$
This equation indicates a balance between the gradient of $\ln g$ and the average of the statistic function $\mathbf{u}$ over all data points.
- #statistics, #maximum-likelihood-estimator, #gradient-methods

## Define the term "sufficient statistic" and explain its significance in the context of the provided likelihood model.
A sufficient statistic, in the context of the likelihood function:
$$
p(\mathbf{X} \mid \boldsymbol{\eta}) = \left(\prod_{n=1}^{N} h(\mathbf{x}_n)\right) g(\boldsymbol{\eta})^N \exp \left\{\boldsymbol{\eta}^\mathrm{T} \sum_{n=1}^{N} \mathbf{u}(\mathbf{x}_n)\right\}
$$
is given by $\sum_{n=1}^N \mathbf{u}(\mathbf{x}_n)$. Its significance lies in its ability to encapsulate all necessary data information for estimating $\boldsymbol{\eta}$, meaning the full data set $\mathbf{X}$ does not need to be retained, only this statistic.
- #statistics, #sufficient-statistic, #data-reduction

## How does the estimator $\boldsymbol{\eta}_{\mathrm{ML}}$ behave as $N \rightarrow \infty$, and what does this imply about its consistency?
As $N \rightarrow \infty$, the estimator $\boldsymbol{\eta}_{\mathrm{ML}}$ converges to the true parameter value $\boldsymbol{\eta}$, because the equation:
$$
-\nabla \ln g(\boldsymbol{\eta}_{\mathrm{ML}}) = \frac{1}{N} \sum_{n=1}^{N} \mathbf{u}(\mathbf{x}_n)
$$
tends to $\mathbb{E}[\mathbf{u}(\mathbf{x})]$. This indicates that $\boldsymbol{\eta}_{\mathrm{ML}}$ is a consistent estimator of $\boldsymbol{\eta}$, improving in accuracy as the sample size increases.
- #statistics, #estimator-consistency, #asymptotic-behavior

## Discuss the limitations of parametric density estimation and introduce the concept of nonparametric methods.
Parametric density estimation often assumes a specific functional form of the probability distribution (like Gaussian), which can lead to poor modeling and predictive performance if the true distribution is not well-represented by this form (e.g., multimodal distributions). Nonparametric methods, conversely, make fewer assumptions about the form of the distribution, offering greater flexibility and potentially more accurate modeling for complex or unknown distribution shapes.
- #density-estimation, #parametric-methods, #nonparametric-methods
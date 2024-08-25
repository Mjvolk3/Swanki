## What is the first step in decomposing the expression $\mathbb{E}_{\mathcal{D}}\left[\{f(\mathbf{x} ; \mathcal{D})-h(\mathbf{x})\}^{2}\right]$?

By adding and subtracting $\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]$ inside the braces and then expanding the expression, the decomposition starts as follows:

$$
\begin{aligned}
& \left\{f(\mathbf{x} ; \mathcal{D})-\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]+\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]-h(\mathbf{x})\right\}^{2} \\
& =\left\{f(\mathbf{x} ; \mathcal{D})-\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]\right\}^{2}+\left\{\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]-h(\mathbf{x})\right\}^{2} \\
& +2\left\{f(\mathbf{x} ; \mathcal{D})-\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]\right\}\left\{\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]-h(\mathbf{x})\right\}
\end{aligned}
$$

- #statistics, #bias-variance-tradeoff

---

## Why is the term $2\left\{f(\mathbf{x} ; \mathcal{D})-\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]\right\}\left\{\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]-h(\mathbf{x})\right\}$ omitted when taking the expectation of the expression with respect to $\mathcal{D}$?

The term $2\left\{f(\mathbf{x} ; \mathcal{D})-\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]\right\}\left\{\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]-h(\mathbf{x})\right\}$ vanishes when taking the expectation with respect to $\mathcal{D}$ because it equals zero. This is due to the fact that $\mathbb{E}_{\mathcal{D}}\left[f(\mathbf{x};\mathcal{D})-\mathbb{E}_{\mathcal{D}}[f(\mathbf{x};\mathcal{D})]\right] = 0$.

- #statistics, #bias-variance-tradeoff

---

## What results from the decomposition of the expected squared difference $\mathbb{E}_{\mathcal{D}}\left[\{f(\mathbf{x} ; \mathcal{D})-h(\mathbf{x})\}^{2}\right]$?

The expected squared difference is decomposed into the sum of the squared bias and the variance, given by:

$$
\begin{aligned}
\mathbb{E}_{\mathcal{D}}\left[\{f(\mathbf{x} ; \mathcal{D})-h(\mathbf{x})\}^{2}\right] &= \underbrace{\left\{\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]-h(\mathbf{x})\right\}^{2}}_{(\text {bias })^{2}} \\
&+ \underbrace{\mathbb{E}_{\mathcal{D}}\left[\left\{f(\mathbf{x} ; \mathcal{D})-\mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]\right\}^{2}\right]}_{\text {variance }}
\end{aligned}
$$

- #statistics, #bias-variance-tradeoff

---

## How is the expected loss expressed in terms of bias, variance, and noise?

The expected loss can be decomposed into the bias squared, variance, and noise:

$$
\text{expected loss} = (\text{bias})^{2} + \text{variance} + \text{noise}
$$

where

$$
\begin{aligned}
(\text{bias})^2 &= \int \left\{ \mathbb{E}_{\mathcal{D}}[f(\mathbf{x}; \mathcal{D})] - h(\mathbf{x}) \right\}^{2} p(\mathbf{x}) \,d\mathbf{x} \\
\text{variance} &= \int \mathbb{E}_{\mathcal{D}}\left[\left\{f(\mathbf{x}; \mathcal{D}) - \mathbb{E}_{\mathcal{D}}[f(\mathbf{x}; \mathcal{D})] \right\}^{2}\right] p(\mathbf{x}) \,d\mathbf{x} \\
\text{noise} &= \iint \{ h(\mathbf{x}) - t \}^{2} p(\mathbf{x}, t) \,d\mathbf{x} \,d t
\end{aligned}
$$

- #statistics, #bias-variance-tradeoff, #expected-loss

---

## What is the goal when dealing with the bias-variance trade-off in models?

The goal is to minimize the expected loss, balancing between bias and variance. Flexible models tend to have low bias but high variance, while rigid models have high bias but low variance. The optimal model achieves the best trade-off between these two:

$$
\text{expected loss} = (\text{bias})^{2} + \text{variance} + \text{noise}
$$

- #statistics, #model-selection, #bias-variance-tradeoff

---

## Explain what the variance measures in the decomposition of the expected squared difference between $f(\mathbf{x} ; \mathcal{D})$ and $h(\mathbf{x})$.

The variance measures the extent to which the predictions for individual data sets deviate from their average prediction. Specifically,

$$
\text{variance} = \mathbb{E}_{\mathcal{D}}\left[\left\{f(\mathbf{x} ; \mathcal{D}) - \mathbb{E}_{\mathcal{D}}[f(\mathbf{x} ; \mathcal{D})]\right\}^{2}\right]
$$

- #statistics, #variance, #bias-variance-tradeoff
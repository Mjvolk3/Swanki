## Describe the sum-of-squares error function as mentioned in the paper.

The sum-of-squares error function is given by:

$$
E(\mathbf{w})=\frac{1}{2} \sum_{n=1}^{N}\left\{y\left(x_{n}, \mathbf{w}\right)-t_{n}\right\}^{2}
$$

This function represents the sum of the squares of the differences (errors) between the predicted values $y(x_{n}, \mathbf{w})$ for each data point $x_{n}$ and the corresponding target values $t_{n}$. The factor of $\frac{1}{2}$ is included for convenience in later computations.

- #error-functions, #machine-learning

---

## What happens to the error function $E(\mathbf{w})$ if the function $y(x, \mathbf{w})$ passes exactly through each training data point?

The error function $E(\mathbf{w})$ will be zero if, and only if, the function $y(x, \mathbf{w})$ passes exactly through each training data point. This means that for all $n$:

$$
y(x_{n}, \mathbf{w}) = t_{n}
$$

In such a scenario, the sum-of-squares of the differences is zero.

- #error-functions, #curve-fitting

---

## Explain why the error function minimization has a unique solution.

The error function $E(\mathbf{w})$ is a quadratic function of the coefficients $\mathbf{w}$. Due to the properties of quadratic functions, the derivatives of $E(\mathbf{w})$ with respect to the coefficients will be linear in the elements of $\mathbf{w}$. Therefore, the minimization of the error function has a unique solution, denoted by $\mathbf{w}^{\star}$. This unique solution can be found in closed form.

- #optimization, #curve-fitting

---

## What is the geometric interpretation of the sum-of-squares error function as illustrated in Figure 1.5?

The geometric interpretation of the sum-of-squares error function involves the vertical displacements of each data point from the function $y(x, \mathbf{w})$. The error function measures the total squared distance (vertical displacements) between the observed data points and their corresponding predicted values by the function.

- #error-functions, #geometry

---

## How does the order $M$ of the polynomial affect the complexity of the model and the fit to the data?

The order $M$ of the polynomial significantly affects the complexity of the model and its fit to the data:

- For $M=0$ (constant) and $M=1$ (first-order) polynomials, the fits are poor, providing inadequate representations of the underlying function, $\sin(2\pi x)$.
- For $M=3$ (third-order polynomial), the fit is more representative of the function $\sin(2\pi x)$, showing a good balance.
- For higher-order polynomials such as $M=9$, the fit matches the training data very well but may lead to overfitting, capturing noise along with the underlying pattern.

This balance is an example of model comparison or model selection.

- #model-complexity, #polynomial-fitting
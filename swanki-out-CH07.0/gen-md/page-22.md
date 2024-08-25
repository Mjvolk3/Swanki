```markdown
## Exercises

7.1 (*) By substituting (7.10) into (7.7) and using (7.8) and (7.9), show that the error function (7.7) can be written in the form (7.11).








---

## Consider a Hessian matrix $\mathbf{H}$ with the eigenvector equation (7.8). By setting the vector $\mathbf{v}$ in (7.14) equal to each of the eigenvectors $\mathbf{u}_{i}$ in turn, show that $\mathbf{H}$ is positive definite if, and only if, all its eigenvalues are positive.

The Hessian matrix $\mathbf{H}$ is positive definite if, and only if, all its eigenvalues are positive.




```math
While we're on the topic: The eigenvalue equation of a Hessian matrix is fundamental in optimization and can be written as:
\[
\mathbf{H} \mathbf{u} = \lambda \mathbf{u}
\]
Where $\mathbf{H}$ is the Hessian matrix, $\mathbf{u}$ is the eigenvector, and $\lambda$ is the eigenvalue.
\]
A matrix $\mathbf{H}$ is positive definite if for all non-zero vectors $\mathbf{z}$, we have:
\[
\mathbf{z}^{T} \mathbf{H} \mathbf{z} > 0
]
To show the implications for eigenvalues,

If $\mathbf{H}$ is positive definite, $\mathbf{z}^{T} \mathbf{H} \mathbf{z} > 0$. Consider $\mathbf{z} = \mathbf{u}_i$.

Then,
\[
\mathbf{u}_i^{T} \mathbf{H} \mathbf{u}_i = \mathbf{u}_i^{T} \lambda_i \mathbf{u}_i = \lambda_i (\mathbf{u}_i^{T} \mathbf{u}_i)
\]

Since $\mathbf{u}_i^{T} \mathbf{u}_i > 0$, it follows that:
\[
\lambda_i (\mathbf{u}_i^{T} \mathbf{u}_i) > 0 \quad \Rightarrow \quad \lambda_i > 0
This proves all eigenvalues must be positive.
---

7.2 (^) Consider a linear regression model with a single input variable $x$ and a single output variable $y$ of the form

$y(x,w,b) = wx + b$ together with a sum-of-squares error function given by 

$$
E(w, b)=\frac{1}{2} \sum_{n=1}^{N}\left\{y\left(x_{n}, w, b\right)-t_{n}\right\}^{2}
$$

Derive expressions for the elements of the $2 \times 2$ Hessian matrix given by the second derivatives of the error function with respect to the weight parameter $w$ and bias parameter $b$. Show that the trace and its determinant of this Hessian are both positive. Since the trace represents the sum of the eigenvalue and the determinant corresponds to the product of the eigenvalues, then both eigenvalues are positive and hence the stationary point of the error function is a minimum.

### Partial derivatices of y function
first derivative w.r.t weight ,$\frac{\partial w}$:
$$
\frac{\partial}{\partial w}E(w, b)=\frac{1}{2}\left[\frac{\partial}{\partial w}\sum\mathbb{N}_{1}\left\{wx_{n} - b -t_{n}\right\}^{2}=\sum\mathbb{N}_{1} \left(wx_{n} - b- t_{n}\right) . x_{n}\right\}
$$

first derivative w.r.t bias, $\frac{\partial b}$:
$$
\frac{\partial}{\partial b}E(w, b)=\frac{1}{2}\sum\mathbb{N}_{1}2\left \{wx_{n} -b -t_{n}\right\} . 1 
$$

Implementing second order functions,
$$
\frac{\partial^{2}}{\partial w^{2}}E(w, b)=\sum\mathbb{N}\frac{n=1} x_{n}\left((x_{n)^{2}E(w,b) - t_{0}t_{1}}
$$
$$

Finally, we form the Hessian matrix,

$$
\mathbf{H} = \begin{bmatrix}
H_{11} & H_{12}\\)
H_{12}& H_{22}
\end{bmatrix}
$$

The trace in diagIainal form trace(H)= H_{11}+H_{22} is given by;

$$
$\mathbf{p}{H}=trace[1,1]+H_{22}
&
$
which represent postive-definite Hessian matrix function.
\end{proof}

---

7.3 (*) Consider a single-layer classification model with a single input variable $x$ and a single output variable $y$ of the form

$y(x,w,b) = \sigma(wx +b)$ 

```markdown 
Context for recognizing in classification model,
where $\sigma(\cdot)$ is the logistic sigmoid function defined by (\5.42) together with cross-entropy,
\mathcal{E}( w,b ) = \sum\limits_{n= 1}^{N} \left\{t_{ n } ln( y(x_{n}, w,b)+ (1-t{n}) ln( 1-y(x_{n}, w, b)) \right\} hinter than  $(w,b)$

Again $\displaystyle From recall method log forward functions function second order derivatives..).

## The Taylor expansion of an error function about stationary point are representation $ \mathbf{\ W^{ \sigma w^{ },} }$ minimum criteria shows
---
7.4 (*)By considering Taylor expansion of an error function about a stationary point $\mathbf{w}^{*,}$ 

$$
Hessian- H^{ (*^{i} )} \mathbb{0}
$$% terminated 

9 - ( )7.2 minimum criterium
```
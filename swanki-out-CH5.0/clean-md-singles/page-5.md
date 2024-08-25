Figure 5.3 Illustration of the decision regions for a multi-class linear discriminant, with the decision boundaries shown in red. If two points $\mathrm{x}_{\mathrm{A}}$ and $\mathrm{x}_{\mathrm{B}}$ both lie inside the same decision region $\mathcal{R}_{k}$, then any point $\widehat{\mathrm{x}}$ that lies on the line connecting these two points must also lie in $\mathcal{R}_{k}$, and hence, the decision region must be singly connected and convex.

![](https://cdn.mathpix.com/cropped/2024_05_26_c6820e8ed9a153596826g-1.jpg?height=418&width=581&top_left_y=211&top_left_x=1065)

hence corresponds to a $(D-1)$-dimensional hyperplane defined by

$$
\left(\mathbf{w}_{k}-\mathbf{w}_{j}\right)^{\mathrm{T}} \mathbf{x}+\left(w_{k 0}-w_{j 0}\right)=0
$$

This has the same form as the decision boundary for the two-class case discussed in Section 5.1.1, and so analogous geometrical properties apply.

The decision regions of such a discriminant are always singly connected and convex. To see this, consider two points $\mathrm{x}_{\mathrm{A}}$ and $\mathrm{x}_{\mathrm{B}}$ both of which lie inside decision region $\mathcal{R}_{k}$, as illustrated in Figure 5.3. Any point $\widehat{\mathbf{x}}$ that lies on the line connecting $\mathbf{x}_{\mathrm{A}}$ and $\mathbf{x}_{\mathrm{B}}$ can be expressed in the form

$$
\widehat{\mathbf{x}}=\lambda \mathbf{x}_{\mathrm{A}}+(1-\lambda) \mathbf{x}_{\mathrm{B}}
$$

where $0 \leqslant \lambda \leqslant 1$. From the linearity of the discriminant functions, it follows that

$$
y_{k}(\widehat{\mathbf{x}})=\lambda y_{k}\left(\mathbf{x}_{\mathrm{A}}\right)+(1-\lambda) y_{k}\left(\mathbf{x}_{\mathrm{B}}\right)
$$

Because both $\mathbf{x}_{\mathrm{A}}$ and $\mathbf{x}_{\mathrm{B}}$ lie inside $\mathcal{R}_{k}$, it follows that $y_{k}\left(\mathbf{x}_{\mathrm{A}}\right)>y_{j}\left(\mathbf{x}_{\mathrm{A}}\right)$ and that $y_{k}\left(\mathbf{x}_{\mathrm{B}}\right)>y_{j}\left(\mathbf{x}_{\mathrm{B}}\right)$, for all $j \neq k$, and hence $y_{k}(\widehat{\mathbf{x}})>y_{j}(\widehat{\mathbf{x}})$, and so $\widehat{\mathbf{x}}$ also lies inside $\mathcal{R}_{k}$. Thus, $\mathcal{R}_{k}$ is singly connected and convex.

Note that for two classes, we can either employ the formalism discussed here, based on two discriminant functions $y_{1}(\mathbf{x})$ and $y_{2}(\mathbf{x})$, or else use the simpler but essentially equivalent formulation based on a single discriminant function $y(\mathbf{x})$.

\title{
5.1.3 1-of- $K$ coding
}

For regression problems, the target variable $\mathbf{t}$ was simply the vector of real numbers whose values we wish to predict. In classification, there are various ways of using target values to represent class labels. For two-class problems, the most convenient is the binary representation in which there is a single target variable $t \in\{0,1\}$ such that $t=1$ represents class $\mathcal{C}_{1}$ and $t=0$ represents class $\mathcal{C}_{2}$. We can interpret the value of $t$ as the probability that the class is $\mathcal{C}_{1}$, with the probability values taking only the extreme values of 0 and 1 . For $K>2$ classes, it is convenient to use a 1 -of- $K$ coding scheme, also known as the one-hot encoding scheme, in which $\mathbf{t}$ is a vector of length $K$ such that if the class is $\mathcal{C}_{j}$, then all elements $t_{k}$ of $\mathbf{t}$ are zero
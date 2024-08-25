Figure 5.6 An example of a loss matrix with elements $L_{k j}$ for the cancer treatment problem. The rows correspond to the true class, whereas the columns correspond to the assignment of class made by our decision criterion. $\left.\begin{array}{l}\text { normal } \\ \text { cancer }\end{array} \begin{array}{cc}\text { cancer } \\ 0 & 1 \\ 100 & 0\end{array}\right)$

they aim to maximize. These are equivalent concepts if we take the utility to be simply the negative of the loss. Throughout this text we will use the loss function convention. Suppose that, for a new value of $\mathbf{x}$, the true class is $\mathcal{C}_{k}$ and that we assign $\mathrm{x}$ to class $\mathcal{C}_{j}$ (where $j$ may or may not be equal to $k$ ). In so doing, we incur some level of loss that we denote by $L_{k j}$, which we can view as the $k, j$ element of a loss matrix. For instance, in our cancer example, we might have a loss matrix of the form shown in Figure 5.6. This particular loss matrix says that there is no loss incurred if the correct decision is made, there is a loss of 1 if a healthy patient is diagnosed as having cancer, whereas there is a loss of 100 if a patient having cancer is diagnosed as healthy.

The optimal solution is the one that minimizes the loss function. However, the loss function depends on the true class, which is unknown. For a given input vector x, our uncertainty in the true class is expressed through the joint probability distribution $p\left(\mathbf{x}, \mathcal{C}_{k}\right)$, and so we seek instead to minimize the average loss, where the average is computed with respect to this distribution and is given by

$$
\mathbb{E}[L]=\sum_{k} \sum_{j} \int_{\mathcal{R}_{j}} L_{k j} p\left(\mathbf{x}, \mathcal{C}_{k}\right) \mathrm{d} \mathbf{x}
$$

Each $\mathrm{x}$ can be assigned independently to one of the decision regions $\mathcal{R}_{j}$. Our goal is to choose the regions $\mathcal{R}_{j}$ to minimize the expected loss (5.22), which implies that for each $\mathbf{x}$, we should minimize $\sum_{k} L_{k j} p\left(\mathbf{x}, \mathcal{C}_{k}\right)$. As before, we can use the product rule $p\left(\mathbf{x}, \mathcal{C}_{k}\right)=p\left(\mathcal{C}_{k} \mid \mathbf{x}\right) p(\mathbf{x})$ to eliminate the common factor of $p(\mathbf{x})$. Thus, the decision rule that minimizes the expected loss assigns each new $\mathbf{x}$ to the class $j$ for which the quantity

$$
\sum_{k} L_{k j} p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)
$$

is a minimum. Once we have chosen values for the loss matrix elements $L_{k j}$, this is clearly trivial to do.

\title{
5.2.3 The reject option
}

We have seen that classification errors arise from the regions of input space where the largest of the posterior probabilities $p\left(\mathcal{C}_{k} \mid \mathbf{x}\right)$ is significantly less than unity or equivalently where the joint distributions $p\left(\mathbf{x}, \mathcal{C}_{k}\right)$ have comparable values. These are the regions where we are relatively uncertain about class membership. In some applications, it will be appropriate to avoid making decisions on the difficult cases in anticipation of obtaining a lower error rate on those examples for which a classification decision is made. This is known as the reject option. For example, in our hypothetical cancer screening example, it may be appropriate to use an automatic
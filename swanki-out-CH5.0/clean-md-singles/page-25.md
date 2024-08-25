the $\log$ likelihood function that depend on $\pi$ are

$$
\sum_{n=1}^{N}\left\{t_{n} \ln \pi+\left(1-t_{n}\right) \ln (1-\pi)\right\}
$$

Setting the derivative with respect to $\pi$ equal to zero and rearranging, we obtain

$$
\pi=\frac{1}{N} \sum_{n=1}^{N} t_{n}=\frac{N_{1}}{N}=\frac{N_{1}}{N_{1}+N_{2}}
$$

where $N_{1}$ denotes the total number of data points in class $\mathcal{C}_{1}$, and $N_{2}$ denotes the total number of data points in class $\mathcal{C}_{2}$. Thus, the maximum likelihood estimate for $\pi$ is simply the fraction of points in class $\mathcal{C}_{1}$ as expected. This result is easily generalized to the multi-class case where again the maximum likelihood estimate of the prior probability associated with class $\mathcal{C}_{k}$ is given by the fraction of the training set points assigned to that class.

Now consider the maximization with respect to $\boldsymbol{\mu}_{1}$. Again, we can pick out of the $\log$ likelihood function those terms that depend on $\boldsymbol{\mu}_{1}$ :

$$
\sum_{n=1}^{N} t_{n} \ln \mathcal{N}\left(\mathbf{x}_{n} \mid \boldsymbol{\mu}_{1}, \boldsymbol{\Sigma}\right)=-\frac{1}{2} \sum_{n=1}^{N} t_{n}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{1}\right)^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{1}\right)+\text { const. }
$$

Setting the derivative with respect to $\boldsymbol{\mu}_{1}$ to zero and rearranging, we obtain

$$
\boldsymbol{\mu}_{1}=\frac{1}{N_{1}} \sum_{n=1}^{N} t_{n} \mathbf{x}_{n}
$$

which is simply the mean of all the input vectors $\mathbf{x}_{n}$ assigned to class $\mathcal{C}_{1}$. By a similar argument, the corresponding result for $\boldsymbol{\mu}_{2}$ is given by

$$
\boldsymbol{\mu}_{2}=\frac{1}{N_{2}} \sum_{n=1}^{N}\left(1-t_{n}\right) \mathbf{x}_{n}
$$

which again is the mean of all the input vectors $\mathbf{x}_{n}$ assigned to class $\mathcal{C}_{2}$.

Finally, consider the maximum likelihood solution for the shared covariance matrix $\boldsymbol{\Sigma}$. Picking out the terms in the log likelihood function that depend on $\boldsymbol{\Sigma}$, we have

$$
\begin{aligned}
& -\frac{1}{2} \sum_{n=1}^{N} t_{n} \ln |\boldsymbol{\Sigma}|-\frac{1}{2} \sum_{n=1}^{N} t_{n}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{1}\right)^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{1}\right) \\
& -\frac{1}{2} \sum_{n=1}^{N}\left(1-t_{n}\right) \ln |\boldsymbol{\Sigma}|-\frac{1}{2} \sum_{n=1}^{N}\left(1-t_{n}\right)\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{2}\right)^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}\left(\mathbf{x}_{n}-\boldsymbol{\mu}_{2}\right) \\
& =-\frac{N}{2} \ln |\boldsymbol{\Sigma}|-\frac{N}{2} \operatorname{Tr}\left\{\boldsymbol{\Sigma}^{-1} \mathbf{S}\right\}
\end{aligned}
$$
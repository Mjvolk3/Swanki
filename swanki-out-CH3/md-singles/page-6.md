Setting the derivative of (3.20) with respect to \(\mu_{k}\) to zero, we obtain

\[
\mu_{k}=-m_{k} / \lambda
\]

We can solve for the Lagrange multiplier \(\lambda\) by substituting (3.21) into the constraint \(\sum_{k} \mu_{k}=1\) to give \(\lambda=-N\). Thus, we obtain the maximum likelihood solution for \(\mu_{k}\) in the form

\[
\mu_{k}^{\mathrm{ML}}=\frac{m_{k}}{N}
\]

which is the fraction of the \(N\) observations for which \(x_{k}=1\).

We can also consider the joint distribution of the quantities \(m_{1}, \ldots, m_{K}\), conditioned on the parameter vector \(\boldsymbol{\mu}\) and on the total number \(N\) of observations. From (3.17), this takes the form

\[
\operatorname{Mult}\left(m_{1}, m_{2}, \ldots, m_{K} \mid \boldsymbol{\mu}, N\right)=\binom{N}{m_{1} m_{2} \ldots m_{K}} \prod_{k=1}^{K} \mu_{k}^{m_{k}}
\]

which is known as the multinomial distribution. The normalization coefficient is the number of ways of partitioning \(N\) objects into \(K\) groups of size \(m_{1}, \ldots, m_{K}\) and is given by

\[
\binom{N}{m_{1} m_{2} \ldots m_{K}}=\frac{N!}{m_{1}!m_{2}!\ldots m_{K}!}
\]

Note that two-state quantities can be represented either as binary variables and modelled using the binomial distribution (3.9) or as 1 -of-2 variables and modelled using the distribution (3.14) with \(K=2\).

\title{
3.2. The Multivariate Gaussian
}

Section 2.3

Section 2.5
The Gaussian, also known as the normal distribution, is a widely used model for the distribution of continuous variables. We have already seen that for of a single variable \(x\), the Gaussian distribution can be written in the form

\[
\mathcal{N}\left(x \mid \mu, \sigma^{2}\right)=\frac{1}{\left(2 \pi \sigma^{2}\right)^{1 / 2}} \exp \left\{-\frac{1}{2 \sigma^{2}}(x-\mu)^{2}\right\}
\]

where \(\mu\) is the mean and \(\sigma^{2}\) is the variance. For a \(D\)-dimensional vector \(\mathbf{x}\), the multivariate Gaussian distribution takes the form

\[
\mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}, \boldsymbol{\Sigma})=\frac{1}{(2 \pi)^{D / 2}} \frac{1}{|\boldsymbol{\Sigma}|^{1 / 2}} \exp \left\{-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^{\mathrm{T}} \boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})\right\}
\]

where \(\boldsymbol{\mu}\) is the \(D\)-dimensional mean vector, \(\boldsymbol{\Sigma}\) is the \(D \times D\) covariance matrix, and det \(\boldsymbol{\Sigma}\) denotes the determinant of \(\boldsymbol{\Sigma}\).

The Gaussian distribution arises in many different contexts and can be motivated from a variety of different perspectives. For example, we have already seen that for
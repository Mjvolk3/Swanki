\title{
Algorithm 7.4: Adam optimization
}

Input: Training set of data points indexed by \(n \in\{1, \ldots, N\}\)

Batch size \(B\)

Error function per mini-batch \(E_{n: n+B-1}(\mathbf{w})\)

Learning rate parameter \(\eta\)

Decay parameters \(\beta_{1}\) and \(\beta_{2}\)

Stabilization parameter \(\delta\)

Output: Final weight vector w

\(n \leftarrow 1\)

\(\mathbf{s} \leftarrow \mathbf{0}\)

\(\mathbf{r} \leftarrow \mathbf{0}\)

repeat

Choose a mini-batch at random from \(\mathcal{D}\)

\(\mathbf{g}=-\nabla E_{n: n+B-1}(\mathbf{w}) / /\) evaluate gradient vector

\(\mathbf{s} \leftarrow \beta_{1} \mathbf{s}+\left(1-\beta_{1}\right) \mathbf{g}\)

\(\mathbf{r} \leftarrow \beta_{2} \mathbf{r}+\left(1-\beta_{2}\right) \mathbf{g} \odot \mathbf{g} / /\) element-wise multiply

\(\widehat{\mathbf{s}} \leftarrow \mathbf{s} /\left(1-\beta_{1}^{\tau}\right) / /\) bias correction

\(\widehat{\mathbf{r}} \leftarrow \mathbf{r} /\left(1-\beta_{2}^{\tau}\right) / /\) bias correction

\(\Delta \mathbf{w} \leftarrow-\eta \frac{\widehat{\mathbf{s}}}{\sqrt{\widehat{\mathbf{r}}}+\delta} / /\) element-wise operations

\(\mathbf{w} \leftarrow \mathbf{w}+\Delta \mathbf{w} / /\) weight vector update

\(n \leftarrow n+B\)

if \(n+B>N\) then

shuffle data

\(n \leftarrow 1\)

end if

until convergence

return w
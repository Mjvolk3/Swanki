### ## Discrete Convolution Explanation

Given the vectors $\boldsymbol{x}=[1,2,3,4]$ and $\boldsymbol{y}=[5,6,7]$, how do we compute the discrete convolution $\boldsymbol{z}$?

%
To compute the discrete convolution $\boldsymbol{z}$ of $\boldsymbol{x}$ and $\boldsymbol{y}$, we use the definition:

$$
z_{n} = \sum_{k=-\infty}^{\infty} x_{k} y_{n-k}
$$

Since $\boldsymbol{x}$ has finite length and $\boldsymbol{y}$ also has finite length, the summation will only be over valid indices.

Table 2.4 illustrates the step-by-step computation:

1. For $z_{0}$: $\boldsymbol{y}$ is flipped and aligned with $\boldsymbol{x}$, producing
$$
z_{0} = x_{0} \cdot y_{0} = 1 \cdot 5 = 5
$$

2. For $z_{1}$: $\boldsymbol{y}$ is shifted one position.
$$
z_{1} = x_{0} \cdot y_{1} + x_{1} \cdot y_{0} = 1 \cdot 6 + 2 \cdot 5 = 6 + 10 = 16
$$

3. For $z_{2}$: $\boldsymbol{y}$ is shifted two positions.
$$
z_{2} = x_{0} \cdot y_{2} + x_{1} \cdot y_{1} + x_{2} \cdot y_{0} = 1 \cdot 7 + 2 \cdot 6 + 3 \cdot 5 = 7 + 12 + 15 = 34
$$

4. Continue this process to compute the full vector $\boldsymbol{z} = [5, 16, 34, 52, 45, 28]$.

- #math, #convolution, #discrete-math

### ## Convolution Theorem for PMF of Sum

If $x_{1}$ and $x_{2}$ are independent discrete random variables, how do we find the pmf of their sum $y = x_{1} + x_{2}$?

%
We use the following equation to find the pmf of the sum of two independent discrete random variables $x_{1}$ and $x_{2}$:

$$
p(y=j) = \sum_{k} p(x_{1}=k) p(x_{2}=j-k)
$$

This is essentially the convolution of the two probability mass functions (pmfs) of $x_{1}$ and $x_{2}$.

For example, if $x_{1}$ and $x_{2}$ are the outcomes of rolling two dice, each following a discrete uniform distribution from 1 to 6, their sum's pmf $p(y=j)$ will be computed by convolving their individual pmfs.

- #math, #probability, #convolution-theorem

### ## Convolution of PDFs

What is the continuous analog of the convolution theorem for two independent random variables $x_{1}$ and $x_{2}$ with pdfs $p_{1}(x_{1})$ and $p_{2}(x_{2})$?

%
The continuous analog of the convolution theorem is given by the pdf of the sum $y = x_{1} + x_{2}$, derived using the cdf:

$$
P_{y}(y^{*}) = \operatorname{Pr}(y \leq y^{*}) = \int_{-\infty}^{\infty} p_{1}(x_{1}) \left[\int_{-\infty}^{y^{*} - x_{1}} p_{2}(x_{2}) dx_{2}\right] dx_{1}
$$

Differentiating this cdf, we get the pdf:

$$
p(y) = \left[\frac{d}{d y^{*}} P_{y}(y^{*})\right]_{y^{*}=y} = \int p_{1}(x_{1}) p_{2}(y - x_{1}) dx_{1}
$$

Thus, the convolution in the continuous case results in the pdf of the sum being the integral of the product of the individual pdfs.

- #math, #probability, #convolution-theorem

### ## Differentiation Under the Integral Sign

Explain the rule of differentiation under the integral sign used in the convolution theorem.

%
The rule of differentiation under the integral sign is used to differentiate an integral with varying limits. Given an integral of the form:

$$
\frac{d}{d x} \int_{a(x)}^{b(x)} f(t) dt
$$

where $a(x)$ and $b(x)$ are functions of $x$, the rule states:

$$
\frac{d}{d x} \int_{a(x)}^{b(x)} f(t) dt = f(b(x)) \frac{d b(x)}{d x} - f(a(x)) \frac{d a(x)}{d x}
$$

This rule allows us to differentiate the convolution integral in the cdf derivation, resulting in the pdf.

- #math, #calculus, #integrals

### ## "Flip and Drag" Operation

Describe the "flip and drag" operation in the context of discrete convolution.

%
The "flip and drag" operation consists of the following steps:

1. **Flip**: Reverse the order of elements in vector $\boldsymbol{y}$. If $\boldsymbol{y} = [5, 6, 7]$, flipping gives $\boldsymbol{y}^{\text{flipped}} = [7, 6, 5]$.
2. **Drag**: Shift $\boldsymbol{y}^{\text{flipped}}$ across vector $\boldsymbol{x}$, one position at a time.
3. **Elementwise Multiplication**: In each position, multiply corresponding elements of $\boldsymbol{x}$ and shifted $\boldsymbol{y}$.
4. **Sum Results**: Sum the products obtained in the elementwise multiplication to get each element of the result vector $\boldsymbol{z}$.

This method visualizes the computation of each element $z_{n}$ in the resultant convolution vector.

- #math, #convolution, #computational-methods

### ## Convolution Example with Uniform Distributions

How would the convolution theorem apply to the sum of two uniformly distributed random variables, such as rolling two dice?

%
For two uniformly distributed random variables such as rolls of two dice, each side $s$ of a die follows a discrete uniform distribution:

$$
p_{1}(s) = p_{2}(s) = \frac{1}{6} \text{ for } s \in \{1, 2, 3, 4, 5, 6\}
$$

The pmf of their sum $y = x_{1} + x_{2}$ is given by the convolution of their individual pmfs:
$$
p(y=j) = \sum_{k} p(x_{1}=k) p(x_{2}=j-k)
$$

For example, $p(y=7)$ is the probability of getting a sum of 7, which is the sum of probabilities of $(1,6)$, $(2,5)$, $(3,4)$, $(4,3)$, $(5,2)$, $(6,1)$ outcomes, each with probability $\frac{1}{36}$. Thus:

$$
p(7) = p(1,6) + p(2,5) + p(3,4) + p(4,3) + p(5,2) + p(6,1) = 6 \cdot \frac{1}{36} = \frac{1}{6}
$$

- #math, #probability, #discrete-distribution
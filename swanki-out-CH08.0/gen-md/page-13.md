### Card 1

## What is one primary drawback of using numerical differentiation for evaluating gradients in neural networks?

While numerical differentiation is useful for debugging due to its reliance only on the forward propagation equations, one primary drawback is that it scales poorly with the size of the network. 

- #machine-learning, #numerical-methods, #gradient-descent

### Card 2

## Differentiate the function $f(x) = u(x) v(x)$.

The differentiation of the function $f(x) = u(x) v(x)$ can be derived using the product rule of calculus:

$$
\begin{aligned}
f(x) & = u(x) v(x) \\
f^{\prime}(x) & = u^{\prime}(x) v(x) + u(x) v^{\prime}(x)
\end{aligned}
$$

This indicates that both $u(x)$ and $v(x)$ must be evaluated for both the calculation of $f(x)$ and $f^{\prime}(x)$.

- #calculus, #product-rule, #symbolic-differentiation

### Card 3

## Explain expression swell in the context of symbolic differentiation.

Expression swell occurs in symbolic differentiation when the resulting expressions for derivatives become exponentially longer than the original function. This happens due to redundant computations, where nested duplications of expressions grow in complexity, leading to longer evaluation times.

- #machine-learning, #symbolic-computation, #expression-swell

### Card 4

## Describe the structure and output function of a simple neural network with a single input $x$ and two layers, including necessary equations.

The structure of the simple neural network consists of a hidden unit with activation $z$ and an output $y$:

$$
\begin{aligned}
& z = h(w_{1} x + b_{1}) \\
& y = h(w_{2} z + b_{2})
\end{aligned}
$$

where \( h(a) \) is the soft ReLU function: 

$$
\zeta(a) = \ln (1 + \exp (a))
$$

The overall function is then given by:

$$
y(x) = h(w_{2} h(w_{1} x + b_{1}) + b_{2})
$$

- #neural-networks, #activation-functions, #backpropagation

### Card 5

## What is one advantage of using symbolic differentiation for evaluating gradients in machine learning models?

One advantage of symbolic differentiation is that it avoids human error in the manual derivation of backpropagation equations by automating the application of calculus rules, such as the chain rule. This ensures that gradients are calculated to machine precision.

- #machine-learning, #symbolic-computation, #gradient-descent

### Card 6

## Considering a function $h(a)$ defined as $\ln (1 + \exp (a))$, evaluate $h(w_{1} x + b_{1})$ and $h(w_{2} z + b_{2})$ if $z = h(w_{1} x + b_{1})$.

For the given function \( h(a) = \ln(1 + \exp(a)) \):

First, evaluate the hidden unit activation \( z \):

$$
z = \ln(1 + \exp(w_{1} x + b_{1}))
$$

Then, substitute \( z \) into the output function \( y \):

$$
y = \ln(1 + \exp(w_{2} \ln(1 + \exp(w_{1} x + b_{1})) + b_{2}))
$$

This shows the nested structure often seen in neural network models.

- #activation-functions, #neural-networks, #machine-learning
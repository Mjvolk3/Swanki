## How can any density \(p(y)\) be generated from a fixed density \(q(x)\)?
By utilizing a nonlinear change of variable \( y=f(x) \), where \( f(x) \) is a monotonic function ensuring \( 0 \leqslant f'(x) < \infty \), any density \( p(y) \) can be derived from \( q(x) \).

- #probability-density-functions, #transformations.nonlinear, #statistics

## How does a mode of a probability density transform under a change of variable?
Given a mode at \( \widehat{x} \) where \( f'(\widehat{x}) = 0 \), and transforming under \( y = f(x) \), the mode \( \widehat{y} \) in \( y \)-space is found where \( \tilde{f}'(\widehat{y}) = 0 \). Essentially, \( \widehat{x} = g(\widehat{y}) \) if \( g \) is the functional inverse of \( f \) and \( g'(\widehat{y}) \neq 0 \).

$$
\tilde{f}'(\widehat{y}) = f'(g(\widehat{y})) g'(\widehat{y}) = 0
$$

- #probability-density-functions, #mode.transformations, #statistics

## How does the probability density \( p_y(y) \) relate to \( p_x(x) \) under the change of variables \( x=g(y) \)?
The probability density transforms as \( p_y(y) = p_x(g(y)) s g'(y) \), assuming \( g'(y) = s |g'(y)| \), where \( s \in \{-1, +1\} \).

$$
p_y(y) = p_x(g(y)) s g'(y)
$$

- #probability-density-functions, #transformations.change-of-variables, #mathematics.differential-calculus

## What happens to the density's mode under a non-linear transformation?
Under a nonlinear transformation, the value of \( x \) that maximizes \( p_x(x) \) does not correspond to the value that maximizes \( p_y(y) \). For linear transformations, maximas coincide, but for nonlinear ones, the transformation affects the location due to the presence of \( g''(y) \) in:

$$
p_y'(y) = s p_x'(g(y))\{g'(y)\}^2 + s p_x(g(y)) g''(y)
$$

- #probability-density-functions, #nonlinear-transformations, #statistics.effects-of-transformation

## Demonstrate with an example the effect of a nonlinear change of variables on a probability distribution.
Considering a Gaussian distribution \( p_x(x) \), transforming it to \( y \)-space using \( x=g(y) = \ln(y) - \ln(1-y) + 5 \) and the inverse \( y = g^{-1}(x) = \frac{1}{1 + e^{-x+5}} \) shows how the distribution changes form. This illustrates the substantial effect of nonlinear variable transformations on the localization of modes and general distribution shape.

$$
x=g(y)=\ln (y)-\ln (1-y)+5, \quad y=g^{-1}(x)=\frac{1}{1+\exp (-x+5)}
$$

- #probability-density-functions, #examples.nonlinear-transformation, #statistics-distribution-change
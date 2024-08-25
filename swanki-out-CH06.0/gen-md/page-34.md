Here are six Anki cards based on the provided academic content:

### Card 1: Expression for the surface area $S_{D}$ of a hypersphere

## Using the result (2.126), derive an expression for the surface area $S_{D}$ of a hypersphere of unit radius in $D$ dimensions.

Consider the integral transformation from Cartesian to polar coordinates given by:

$$
\prod_{i=1}^{D} \int_{-\infty}^{\infty} e^{-x_{i}^{2}} \mathrm{~d} x_{i}=S_{D} \int_{0}^{\infty} e^{-r^{2}} r^{D-1} \mathrm{~d} r
$$

Use the gamma function:

$$
\Gamma(x)=\int_{0}^{\infty} t^{x-1} e^{-t} \mathrm{~d} t
$$

together with (2.126), evaluate both sides of this equation, and hence show that:

$$
S_{D}=\frac{2 \pi^{D / 2}}{\Gamma(D / 2)}
$$

%
The surface area $S_D$ of a hypersphere in $D$ dimensions is given by:

$$
S_{D}=\frac{2 \pi^{D / 2}}{\Gamma(D / 2)}
$$

We start by recognizing that transforming the Cartesian coordinates to polar coordinates yields:

$$
\prod_{i=1}^{D} \int_{-\infty}^{\infty} e^{-x_{i}^{2}} \mathrm{~d} x_{i}=S_{D} \int_{0}^{\infty} e^{-r^{2}} r^{D-1} \mathrm{~d} r
$$

The left-hand side equals $(\sqrt{\pi})^D$ by evaluating the Gaussian integrals. Employing the gamma function $\Gamma\left(\frac{D}{2}\right)$ on the right-hand side, we equate both sides to solve for $S_D$, yielding:

$$
S_D = \frac{2 \pi^{D/2}}{\Gamma(D/2)}
$$

- #math.geometry, #math.analysis
  
### Card 2: Volume $V_{D}$ of a unit hypersphere

## Next, show that the volume of the unit hypersphere in $D$ dimensions is given by $\frac{S_{D}}{D}$.

Use the derived surface area $S_D$:

$$
S_D = \frac{2 \pi^{D/2}}{\Gamma(D/2)}
$$

to integrate with respect to the radius from 0 to 1 and show that:

$$
V_{D} = \frac{S_D}{D}
$$

%
The volume $V_D$ of the unit hypersphere in $D$ dimensions is given by:

$$
V_D = \frac{S_D}{D}
$$

Given the surface area $S_D$ of a hypersphere:

$$
S_D = \frac{2 \pi^{D/2}}{\Gamma(D/2)}
$$

We use the integral to find the volume by integrating with respect to the radius from 0 to 1:

$$
V_D = \int_0^1 S_D r^{D-1} dr = S_D \int_0^1 r^{D-1} dr = \frac{S_D}{D}
$$

Thus,

$$
V_D = \frac{S_D}{D}
$$

- #math.geometry, #math.integration

### Card 3: Special cases for $D=2$ and $D=3$

## Use $\Gamma(1)=1$ and $\Gamma(3 / 2)=\sqrt{\pi} / 2$ to reduce the volume expressions for $D=2$ and $D=3$.

Given the known gamma function values:

$$
\Gamma(1) = 1, \quad \Gamma(3/2) = \sqrt{\pi}/2
$$

Show the volume expressions for cases $D=2$ and $D=3$.

%

For $D=2$:
$$
S_2 = \frac{2 \pi^{1}}{\Gamma(1)} = 2\pi
$$
$$
V_2 = \frac{2\pi}{2} = \pi
$$

For $D=3$:
$$
S_3 = \frac{2 \pi^{3/2}}{\Gamma(3/2)} = \frac{2 \pi^{3/2}}{\sqrt{\pi}/2} = 4\pi
$$
$$
V_3 = \frac{4\pi}{3}
$$

Thus, the volume expressions reduce to:

$$
V_2 = \pi \quad \text{and} \quad V_3 = \frac{4\pi}{3}
$$

- #math.geometry, #special-functions.gamma

### Card 4: Volume ratio of hypersphere to hypercube

## Show that the ratio of the volume of the hypersphere to the volume of the cube is given by $\frac{\pi^{D / 2}}{D 2^{D-1} \Gamma(D / 2)}$.

Use the results from Exercise 6.1 to derive the volume ratio expression for a hypersphere and a hypercube.

%
The ratio of the volume of a hypersphere to the volume of a hypercube is given by:

$$
\frac{\pi^{D / 2}}{D 2^{D-1} \Gamma(D / 2)}
$$

The volume of a hypersphere of unit radius in $D$ dimensions is:

$$
V_D = \frac{\pi^{D/2}}{\Gamma(D/2) D}
$$

The volume of a hypercube with side length $2$ in $D$ dimensions is:

$$
\text{Volume of hypercube}=2^D
$$

Thus, the ratio is:

$$
\frac{V_D}{2^D} = \frac{\pi^{D/2}}{D 2^{D-1} \Gamma(D/2)}
$$

- #math.geometry, #math.analysis

### Card 5: Stirling's approximation and volume ratio

## Use Stirling's formula $\Gamma(x+1) \simeq(2 \pi)^{1 / 2} e^{-x} x^{x+1 / 2}$ and show that, as $D \rightarrow \infty$, the volume ratio goes to zero.

Given Stirling's approximation for large $x$:

$$
\Gamma(x+1) \simeq (2\pi)^{1/2} e^{-x} x^{x+1/2}
$$

Show that the volume ratio approaches zero as $D \rightarrow \infty$.

%
Using Stirling's approximation:

$$
\Gamma(x+1) \simeq (2\pi)^{1/2} e^{-x} x^{x+1/2}
$$

We approximate $\Gamma(D/2)$ for large $D$:

$$
\Gamma(D/2) \approx \left(\frac{D}{2}\right)^{D/2-1/2} \sqrt{2 \pi} e^{-D/2}
$$

Substituting into the ratio:

$$
\frac{\pi^{D / 2}}{D 2^{D-1} \Gamma(D / 2)} \approx \frac{\pi^{D/2}}{D 2^{D-1} (2\pi)^{1/2} \left(\frac{D}{2}\right)^{D/2-1/2} e^{-D/2}}
$$

Simplifying:

$$
= \frac{(\pi e / D)^{D/2}}{D \cdot (2 / D)^{D/2-1/2}}
$$

As $D \rightarrow \infty$, $\left(\frac{\pi e}{D}\right)^{D/2}$ goes to zero, thus the ratio approaches zero.

- #math.approximations, #math.analysis

### Card 6: Distance from center of hypercube to corner

## Show that the distance from the center of the hypercube to one of its corners increases with $D$.

Determine the distance from the center of a hypercube of side $2a$ to one of its corners in $D$ dimensions.

%
The distance from the center of the hypercube to one of its corners is given by the Euclidean distance in $D$ dimensions.

For a hypercube of side $2a$, each coordinate ranges from $-a$ to $a$. The distance from the center to a corner is:

$$
\sqrt{a^2 + a^2 + \cdots + a^2} = \sqrt{D \cdot a^2} = a\sqrt{D}
$$

Thus, the distance scales with the square root of the number of dimensions $D$.

- #math.geometry, #math.distance
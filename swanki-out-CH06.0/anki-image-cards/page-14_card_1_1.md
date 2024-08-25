## Nonlinear Activation Functions: Hyperbolic Tangent
    
What is the definition and range of the hyperbolic tangent function ($\tanh$) and how is it plotted?

![6 nonlinear activation functions](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=1026&width=1497&top_left_y=200&top_left_x=150)

%

The hyperbolic tangent function ($\tanh$) is defined by: 

$$
\tanh (a) = \frac{e^a - e^{-a}}{e^a + e^{-a}}
$$ 

It outputs values between -1 and 1, and its plot is sigmoid-shaped, as shown in Figure 6.12(a).

- #neural-networks, #activation-functions, #hyperbolic-tangent

---

## Nonlinear Activation Functions: ReLU and Variants

What are the characteristics and definitions of the ReLU, leaky ReLU, and softplus functions?

![6 nonlinear activation functions](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=1026&width=1497&top_left_y=200&top_left_x=150)

%

1. **ReLU (Rectified Linear Unit)**: Outputs the input directly for positive inputs and zero for negative inputs.
2. **Leaky ReLU**: Similar to ReLU, but allows a small, non-zero output for negative inputs, defined by a slope parameter $\alpha$.
3. **Softplus**: A smooth approximation to ReLU with a gradual curve, approaching the line $y = x$ for large positive inputs.

- #neural-networks, #activation-functions, #relu-variants
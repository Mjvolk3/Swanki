### Front of Card 1

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=442&width=491&top_left_y=219&top_left_x=1152)

Describe the characteristics of the softplus activation function and its mathematical expression.

% 

### Back of Card 1

The softplus activation function is given by the equation:

$$
h(a) = \ln(1 + \exp(a))
$$

Characteristics:
- The function is smooth and differentiable.
- It asymptotically approaches a linear function for large positive values of the input $a$.
- This function helps alleviate the vanishing gradient problem commonly seen with traditional sigmoidal activation functions by not saturating.

- #neural-networks, #activation-functions, #softplus

---

### Front of Card 2

![](https://cdn.mathpix.com/cropped/2024_05_26_acdab4f582103bf8b8a9g-1.jpg?height=442&width=491&top_left_y=219&top_left_x=1152)

What problem is alleviated by using the softplus activation function, and why?

%

### Back of Card 2

The softplus activation function alleviates the vanishing gradient problem. Traditional sigmoidal activation functions (like the logistic sigmoid) can saturate, causing gradients to diminish to near-zero values for very large or very small inputs, hindering the learning process. The softplus function, however, does not saturate, allowing gradients to remain significant and thus facilitating better and more consistent learning.

- #neural-networks, #activation-functions, #vanishing-gradient


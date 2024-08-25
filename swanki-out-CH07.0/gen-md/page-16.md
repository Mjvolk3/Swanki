### Card 1
## How is the exponentially weighted moving average of the gradient calculated in Adam optimization method?

The exponentially weighted moving average of the gradient in the Adam optimization method is calculated using the equation:

$$
s_{i}^{(\tau)} = \beta_{1} s_{i}^{(\tau-1)} + (1-\beta_{1}) \left( \frac{\partial E(\mathbf{w})}{\partial w_{i}} \right)
$$

where:

- $s_{i}^{(\tau)}$ is the exponentially weighted moving average of the gradient at step $\tau$
- $\beta_{1}$ is the hyperparameter that controls the decay rate
- $\frac{\partial E(\mathbf{w})}{\partial w_{i}}$ is the gradient of the loss function $E(\mathbf{w})$ with respect to the parameter $w_{i}$

Typical value for $\beta_{1}$ is $0.9$.

- #optimizers.adam, #deep-learning.gradients

### Card 2
## How is the squared gradient exponentially weighted in Adam optimization method?

The squared gradient is exponentially weighted in the Adam optimization method using:

$$
r_{i}^{(\tau)} = \beta_{2} r_{i}^{(\tau-1)} + (1-\beta_{2})\left(\frac{\partial E(\mathbf{w})}{\partial w_{i}}\right)^2
$$

where:

- $r_{i}^{(\tau)}$ is the exponentially weighted moving average of the squared gradient at step $\tau$
- $\beta_{2}$ is the hyperparameter that controls the decay rate for the squared gradients
- Typical value for $\beta_{2}$ is $0.99$

- #optimizers.adam, #deep-learning.squared-gradients

### Card 3
## Explain the bias correction terms $\frac{1}{(1-\beta_{1}^{\tau})}$ and $\frac{1}{(1-\beta_{2}^{\tau})}$ in the Adam optimization method.

In the Adam optimization method, the bias correction terms $\frac{1}{(1-\beta_{1}^{\tau})}$ and $\frac{1}{(1-\beta_{2}^{\tau})}$ are used to correct for the initialization of $s_{i}^{(0)}$ and $r_{i}^{(0)}$ to zero. These terms address the bias introduced during early iterations. The corrected estimates are:

$$
\widehat{s}_{i}^{(\tau)} = \frac{s_{i}^{(\tau)}}{1 - \beta_{1}^{\tau}}
$$

$$
\widehat{r}_{i}^{\tau} = \frac{r_{i}^{\tau}}{1 - \beta_{2}^{\tau}}
$$

As $\tau$ becomes large, the bias goes to zero since $\beta_{i} < 1$.

- #optimizers.adam, #deep-learning.bias-correction

### Card 4
## What update rule does Adam use for parameter adjustment?

Adam uses the following update rule for parameter adjustment:

$$
w_{i}^{(\tau)} = w_{i}^{(\tau-1)} - \eta \frac{\widehat{s}_{i}^{\tau}}{\sqrt{\widehat{r}_{i}^{\tau}} + \delta}
$$

where:

- $w_{i}^{(\tau)}$ is the updated parameter at step $\tau$
- $\eta$ is the learning rate
- $\widehat{s}_{i}^{\tau}$ is the bias-corrected moving average of the gradient
- $\widehat{r}_{i}^{\tau}$ is the bias-corrected moving average of the squared gradient
- $\delta$ is a small constant to avoid division by zero

- #optimizers.adam, #deep-learning.parameter-update

### Card 5
## What is the typical value of the hyperparameter $\beta_{2}$ in the Adam optimization method and what role does it play?

The typical value of the hyperparameter $\beta_{2}$ in the Adam optimization method is $0.99$. It controls the decay rate for the exponentially weighted moving average of the squared gradients:

$$
r_{i}^{(\tau)} = \beta_{2} r_{i}^{(\tau-1)} + (1-\beta_{2})\left(\frac{\partial E(\mathbf{w})}{\partial w_{i}}\right)^2
$$

The higher the $\beta_{2}$ value, the more weight is given to the past squared gradients.

- #optimizers.adam, #deep-learning.hyperparameters

### Card 6
## What problem does normalization solve in neural networks?

Normalization in neural networks removes the need for the network to handle extremely large or extremely small values of the variables computed during the forward pass. This is crucial for effective training, as it allows the weights and biases to adapt without being destabilized by large gradients. The types of normalization can be across the input data, across mini-batches, or across layers.

- #neural-networks.normalization, #deep-learning.training-stability
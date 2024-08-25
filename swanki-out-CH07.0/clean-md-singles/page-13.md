Figure 7.5 For a situation in which successive steps of gradient descent are oscillatory, a momentum term has little influence on the effective value of the learning rate parameter.

![](https://cdn.mathpix.com/cropped/2024_05_26_26df87b0396463dc47e2g-1.jpg?height=679&width=689&top_left_y=217&top_left_x=955)

tend to cancel and the effective learning rate will be close to $\eta$. Thus, the momentum term can lead to faster convergence towards the minimum without causing divergent oscillations. A schematic illustration of the effect of a momentum term is shown in Figure 7.6.

Although the inclusion of momentum can lead to an improvement in the performance of gradient descent, it also introduces a second parameter $\mu$ whose value needs to be chosen, in addition to that of the learning rate parameter $\eta$. From (7.33) we see that $\mu$ should be in the range $0 \leqslant \mu \leqslant 1$. A typical value used in practice is $\mu=0.9$. Stochastic gradient descent with momentum is summarized in Algorithm 7.3.

The convergence can be further accelerated using a modified version of momentum called Nesterov momentum (Nesterov, 2004; Sutskever et al., 2013). In conventional stochastic gradient descent with momentum, we first compute the gradient at the current location then take a step that is amplified by adding momentum from the previous step. With the Nesterov method, we change the order of these and first compute a step based on the previous momentum, then calculate the gradient at this

Figure 7.6 Illustration of the effect of adding a momentum term to the gradient descent algorithm, showing the more rapid progress along the valley of the error function, compared with the unmodified gradient descent shown in Figure 7.3.

![](https://cdn.mathpix.com/cropped/2024_05_26_26df87b0396463dc47e2g-1.jpg?height=287&width=640&top_left_y=1703&top_left_x=989)
## A two-link robot arm: forward kinematics

![](https://cdn.mathpix.com/cropped/2024_05_26_cf46115da84aa2e9c64eg-1.jpg?height=354&width=357&top_left_y=219&top_left_x=679)

What are the Cartesian coordinates $\left(x_{1}, x_{2}\right)$ of the end effector in a two-link robot arm determined by?

%

The Cartesian coordinates $\left(x_{1}, x_{2}\right)$ of the end effector are determined uniquely by the two joint angles, $\theta_{1}$ and $\theta_{2}$, and the (fixed) lengths $L_{1}$ and $L_{2}$ of the arms.

- #robotics, #kinematics.forward


---

## A two-link robot arm: inverse kinematics

![](https://cdn.mathpix.com/cropped/2024_05_26_cf46115da84aa2e9c64eg-1.jpg?height=364&width=364&top_left_y=219&top_left_x=1127)

What is the goal of inverse kinematics in the context of a two-link robot arm, and how many solutions can it have?

%

The goal of inverse kinematics is to find the joint angles $\theta_{1}$ and $\theta_{2}$ that will position the end effector at a desired Cartesian coordinate $\left(x_{1}, x_{2}\right)$. In this scenario, it can have two solutions corresponding to 'elbow up' and 'elbow down' configurations.

- #robotics, #kinematics.inverse
```yaml
## Define the specific surface area \(\sigma_{\mathrm{p}}(\mathbf{x})\) in terms of the integral over \(\Sigma_{\mathrm{p}}\).

The specific surface area \(\sigma_{\mathrm{p}}(\mathbf{x})\) is defined as:

$$
\sigma_{\mathrm{p}}(\mathbf{x})=\oint_{\Sigma_{\mathrm{p}}} \widehat{G}\left(\mathbf{x}-\xi^{\Sigma}\right) \mathrm{d} \xi^{\Sigma}
$$

- #fluid-dynamics, #specific-surface-area

## Use the compact support property of the filter function \(\widehat{G}\) to simplify the volume average of the gradient operator.

The volume average of the gradient operator given by 

$$\overline{\nabla_{\xi} q}=\nabla_{\mathbf{x}} \bar{q}-\oint_{\Gamma} q\left(\xi^{\Gamma}\right) \widehat{G}\left(\mathbf{x}-\bar{\xi}^{\Gamma}\right){\mathrm{d} \xi^{\Gamma}}^{0}$$ 

can use the filter's compact support property $\widehat{G}\left(\mathbf{x}-\xi^{\Gamma}\right)=0$ to drop the surface integral term, simplifying to:

$$
\overline{\nabla_{\xi} q}=\nabla_{\mathbf{x}} \bar{q}
$$

- #mathematics, #volume-average

## What is the result of applying the even function property of \(\widehat{G}\) and the compact support property to the filter function when averaging the gradient of a function?

Applying the even function property of \(\widehat{G}\) and the compact support property ensures that the volume average of a gradient equals the gradient of the average:

$$
\overline{\nabla_{\xi} q}=\nabla_{\mathbf{x}} \bar{q}
$$

- #mathematics, #filter-function

## State the conservation of mass equation as used in the Das-Moser filtered wall LES formulation for a filtered velocity field \(\bar{u}_{j}\).

The conservation of mass equation in the Das-Moser filtered wall LES formulation is:

$$
\left(\bar{u}_{j}\right)_{, j} = 0
$$

- #fluid-dynamics, #conservation-of-mass

## Write down and explain the incompressible Navier-Stokes equations for intrinsic averaged variables in the DMLES formulation.

The incompressible Navier-Stokes equations for intrinsic averaged variables read:

$$
\begin{aligned}
\left(\epsilon_{\mathrm{w}}\left\langle u_{j}\right\rangle\right)_{, j} & = 0, \\
\left(\epsilon_{\mathrm{w}}\left\langle u_{i}\right\rangle\right)_{, t}+\left(\epsilon_{\mathrm{w}}\left\langle u_{i} u_{j}\right\rangle\right)_{, j}+\left(\epsilon_{\mathrm{w}}\langle p / \rho\rangle\right)_{, i}-\left(\epsilon_{\mathrm{w}}\left\langle\tau_{i j}\right\rangle\right)_{, j} & =-\sigma_{\mathrm{w}} \delta_{i 2}\left\langle(p / \rho)^{\Gamma_{\mathrm{w}}}\right\rangle+\sigma_{\mathrm{w}}\left\langle\left(\nu u_{i, 2}\right)^{\left.\Gamma_{\mathrm{w}}\right\rangle}
\end{aligned}
$$

These equations ensure the conservation of mass and momentum in the context of intrinsic averaged variables for incompressible flows near the wall.

- #fluid-dynamics, #navier-stokes-equations

## Explain Leonard's approach to splitting the dependent variables with a focus on large and small eddies.

Leonard's approach involves splitting the dependent variable $\mathbf{q}(\mathbf{x}+\xi)$ into its average part and a fluctuation part:

$$
\mathbf{q}(\mathbf{x}+\xi)=\overline{\mathbf{q}}(\mathbf{x}+\xi)+\mathbf{q}^{\prime}(\mathbf{x}+\xi)
$$

This method effectively separates large eddies (represented by the average $\overline{\mathbf{q}}$) from small eddies (represented by the fluctuation $\mathbf{q}^{\prime}$).

- #fluid-dynamics, #eddy-decomposition
```
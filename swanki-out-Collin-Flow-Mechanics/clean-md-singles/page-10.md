where

$$
\sigma_{\mathrm{p}}(\mathbf{x})=\oint_{\Sigma_{\mathrm{p}}} \widehat{G}\left(\mathbf{x}-\xi^{\Sigma}\right) \mathrm{d} \xi^{\Sigma}
$$

is the specific surface area.

The properties of the filter function are important for deriving the governing equations. The key importance of the two essential properties for a filter are illustrated when averaging the gradient of a function. Using integration by part for the volume average of the gradient operator yields

$$
\overline{\nabla_{\xi} q}=\nabla_{\mathbf{x}} \bar{q}-\oint_{\Gamma} q\left(\xi^{\Gamma}\right) \widehat{G}\left(\mathbf{x}-\bar{\xi}^{\Gamma}\right){\mathrm{d} \xi^{\Gamma}}^{0}
$$

The even function property of $\widehat{G}$ was used to commute the gradient, and the compact support, $\widehat{G}\left(\mathbf{x}-\xi^{\Gamma}\right)=0$, is used to drop the surface integral term. These two properties are key to ensuring that the average of a gradient is equal to the gradient of the average.

The Das-Moser filtered wall LES (DMLES) formulation (Das 2004, Bhattacharya et al. 2008) is an application of phase filtering. These authors considered the incompressible flow over a flat plate and defined the phase-mask over a flat plate as in Equation 1 where the two phases are the fluid and the solid. The equations for a nonmoving boundary derived by Das and Moser were for LES filtered velocities,

$$
\begin{aligned}
\left(\bar{u}_{j}\right)_{, j} & =0 \\
\left(\bar{u}_{i}\right)_{, t}+\left(\overline{u_{i} u_{j}}\right)_{, j}+(\overline{p / \rho})_{, i}-\left(\bar{\tau}_{i j}\right)_{, j} & =-\delta_{i 2} \overline{(p / \rho)^{\Gamma_{\mathrm{w}}}}+\overline{\left(v u_{i, 2}\right)^{\Gamma_{\mathrm{w}}}}
\end{aligned}
$$

where they use the superficial average velocity. Two effective volumetric forces appear on the right-hand side of the filtered LES equations when $\left|\mathbf{x}-\xi^{\mathrm{w}}\right|<\Delta:(a)$ a wall blockage volumetric pressure drag on the normal momentum component and (b) a volumetric viscous drag on the momentum components parallel to the wall. For incompressible flows, $u_{2,2}=0$; therefore, the volumetric viscous drag is zero on the wall-normal momentum. The LES filtering extends the domain to $y / \Delta=-1 / 2$. Away from the wall, $y / \Delta>1 / 2$, the equations revert to the conventional LES equations. In the DMLES formulation, boundary conditions need to be imposed at $-\Delta / 2$ unless the model for the body force ensures zero velocity at $-\Delta / 2$.

The incompressible Navier-Stokes equations for intrinsic averaged variables read

$$
\begin{aligned}
\left(\epsilon_{\mathrm{w}}\left\langle u_{j}\right\rangle\right)_{, j} & =0, \\
\left(\epsilon_{\mathrm{w}}\left\langle u_{i}\right\rangle\right)_{, t}+\left(\epsilon_{\mathrm{w}}\left\langle u_{i} u_{j}\right\rangle\right)_{, j}+\left(\epsilon_{\mathrm{w}}\langle p / \rho\rangle\right)_{, i}-\left(\epsilon_{\mathrm{w}}\left\langle\tau_{i j}\right\rangle\right)_{, j} & =-\sigma_{\mathrm{w}} \delta_{i 2}\left\langle(p / \rho)^{\Gamma_{\mathrm{w}}}\right\rangle+\sigma_{\mathrm{w}}\left\langle\left(\nu u_{i, 2}\right)^{\left.\Gamma_{\mathrm{w}}\right\rangle} .\right.
\end{aligned}
$$

Away from the wall, $\epsilon_{\mathrm{w}}=1$ and $\sigma_{\mathrm{w}}=0$, the equations revert to the filtered incompressible equations. No boundary conditions are required for the intrinsic averaged variables, as $\epsilon_{\mathrm{w}}=\sigma_{\mathrm{w}}=0$ at $y=-\Delta / 2$.

\title{
3.3. Splitting the Dependent Variables
}

A crucial step in closing the nonlinear averaged governing equation is the procedure used to express averaged products of dependent variables in terms of averaged dependent variables. The classical approach is to split the dependent variables into the averaged variables and their fluctuations from the average (Leonard 1975),

$$
\mathbf{q}(\mathbf{x}+\xi)=\overline{\mathbf{q}}(\mathbf{x}+\xi)+\mathbf{q}^{\prime}(\mathbf{x}+\xi)
$$

In this case $\overline{\mathbf{q}^{\prime}} \neq 0$. Leonard's objective was to split the dependent variables into large eddies and small eddies. This objective is clearly achieved and can be demonstrated by taking the Fourier
\[
\overline{\mathbf{q}^{\mathrm{p}}}(\mathbf{x})=\frac{1}{\mathcal{V}} \int_{\mathcal{V}_{\mathrm{p}}(\mathbf{x})} \mathbf{q}_{\mathrm{p}}(\mathbf{x}+\boldsymbol{\eta}) \mathrm{d} \boldsymbol{\eta}=\frac{1}{\mathcal{V}} \int_{\mathbb{R}^{3}} \gamma^{\mathrm{p}} \mathbf{q}_{\mathrm{p}}(\mathbf{x}+\boldsymbol{\eta}) \mathrm{d} \boldsymbol{\eta}
\]

For locally homogeneous systems, the AEV is set large enough to become a representative elementary volume (REV) where variables are smooth, but with \(\mathcal{V}\) small compared to large inhomogeneities in the system. The formulation can be made equivalent to filtering by introducing an even weight function, \(G(\xi-\mathbf{x})=G(\mathbf{x}-\xi)\), with compact support, \(G\left(\xi^{\Gamma}-\mathbf{x}\right)=0 \quad \forall \xi^{\Gamma} \in \Gamma_{\mathcal{V}}\), and outside the AEV (Bachmat \& Bear 1986). The top-hat filter,

\[
\widehat{G}(\xi-\mathbf{x})=\frac{G(\xi-\mathbf{x})}{\mathcal{V}}= \begin{cases}1 / \mathcal{V} & \forall|\xi-\mathbf{x}|<\Delta / 2 \\ 0 & \forall|\xi-\mathbf{x}| \geq \Delta / 2\end{cases}
\]

is used in most studies of porous media (Bear 1988, Whitaker 1999, Valdés-Parada \& Lasseux 2021). Multiplying the integrand in Equation 5 by \(G(\boldsymbol{\eta})\) and then changing the integration variable to \(\xi=\eta+\mathbf{x}\), the volume average of a dependent variable, \(\overline{\mathbf{q}^{p}}\), is rewritten as

\[
\overline{\mathbf{q}^{\mathrm{p}}}(\mathbf{x})=\int_{\mathbb{R}^{3}} \mathbf{q}^{\mathrm{p}}(\xi) \widehat{G}(\xi-\mathbf{x}) \mathrm{d} \xi=\int_{\mathbb{R}^{3}} \mathbf{q}^{\mathrm{p}}(\xi) \widehat{G}(\mathbf{x}-\xi) \mathrm{d} \xi=\left[\left(\gamma^{\mathrm{p}} \mathbf{q}_{\mathrm{p}}\right) \star \widehat{G}\right]
\]

The compact support property of \(\widehat{G}\) was used to extend the range to the entire space, \(\mathbb{R}^{3}\); the even function property of \(\widehat{G}\) was used to turn the integral into a convolution integral without changing the direction of integration. The function \(\widehat{G}\) is replaced with a weight function, which Marle (1982) attributes to Matheron (1965) in the porous media literature, while the LES formulation uses a filter function whose width is chosen to capture the large turbulence scales, attributed to Leonard (1975) in the turbulence literature.

In addition to dependent variables defined in the domain, surface species on reactive surfaces are defined on the surface per unit surface area they occupy. Volume averaging of these variables turns them into superficial average quantities (i.e., per unit averaging volume),

\[
\overline{\mathbf{q}^{\Sigma_{\mathrm{p}}}}(\mathbf{x})=\left[\mathbf{q}_{\mathrm{p}}(\xi) \delta\left(\xi^{\Sigma}-\xi\right) \star \widehat{G}\right]=\oint_{\Sigma_{\mathrm{p}}} \mathbf{q}_{\mathrm{p}}\left(\xi^{\Sigma}\right) \widehat{G}\left(\mathbf{x}-\xi^{\Sigma}\right) \mathrm{d} \xi^{\Sigma}
\]

where \(\xi^{\Sigma} \in \Sigma_{\mathrm{p}}\) is the coordinate vector of the interface of phase-p with other phases.

Finally, volume-averaged variables are variables per unit of the averaging volume. Volumeaveraged variables in porous media are termed superficial averaged variables. To illustrate the naming, consider the density of a fluid, \(\rho^{\ddagger}\), which is defined per differential volume occupied by the fluid. The volume-averaged density, \(\bar{\rho}\), is per volume of the AEV. In other words, it is no longer per volume occupied by the fluid. The intrinsic average of a quantity, \(\mathbf{q}^{\mathrm{p}}\), occupying phase-p is defined as

\[
\left\langle\mathbf{q}^{\mathrm{p}}\right\rangle(\mathbf{x})=\frac{1}{\epsilon_{\mathrm{p}}(\mathbf{x})}\left[\left(\gamma^{\mathrm{p}} \mathbf{q}_{\mathrm{p}}\right) \star \widehat{G}\right]=\frac{1}{\epsilon_{\mathrm{p}}(\mathbf{x})} \overline{\mathbf{q}^{\mathrm{p}}}(\mathbf{x})
\]

where

\[
\epsilon_{\mathrm{p}}(\mathbf{x})=\overline{\gamma^{\mathrm{p}}}(\mathbf{x})
\]

is the volume fraction of phase-p within the volume of the AEV. Note that the intrinsic average of a constant, \(C\), is the constant, \(C\). It is the volume fraction of the volume occupied by phase-p within the AEV for a top-hat filter. Intrinsic averaged variables are the physically meaningful dependent variables. The angle brackets are therefore the default symbols that we use for intrinsic averaging.

Similarly, the superficial average of surface variables (e.g., the force term in Equation 4b) should be turned into intrinsic variables by normalizing the superficial average with the effective specific surface (surface area of phase-p within the \(\mathrm{AEV}\) per volume of the \(\mathrm{AEV}\) ),

\[
\left\langle\mathbf{q}^{\Sigma_{\mathrm{p}}}\right\rangle(\mathbf{x})=\frac{1}{\sigma_{\mathrm{p}}(\mathbf{x})} \overline{\mathbf{q}^{\Sigma_{\mathrm{p}}}}(\mathbf{x})
\]
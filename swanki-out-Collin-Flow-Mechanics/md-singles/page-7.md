![](https://cdn.mathpix.com/cropped/2024_06_05_c61f1c04f668f80a804eg-1.jpg?height=741&width=1091&top_left_y=128&top_left_x=245)

Figure 2

Definition of phase-mask functions, \(\gamma_{\alpha}\) and \(\gamma_{\beta}\), for two phases, \(\alpha\) and \(\beta\), and derivatives of \(\gamma_{\alpha}\) in space and time.

at large scales that can be resolved with available computer resources. This is achieved by first extending the validity of the governing equations from \(\mathbb{R}_{\mathrm{p}}^{3}\) to the entire space \(\mathbb{R}^{3}\) (Salathe \& Sirovich 1967; Sirovich 1967, 1968). Phase-mask functions are used to distinguish between phases (Bear \& Bachmat 1967, Marle 1982, Breugem 2005, Wood \& Valdés-Parada 2013).

In ablators, the phase-mask function, \(\gamma^{\mathrm{p}}\), for a phase-p, is a function of position, \(\xi\), and time, \(t\), to account for a moving interface between phases caused by surface reactions (Figure 2). It is defined as

\[
\gamma^{\mathrm{p}}(\xi, t)=\left\{\begin{array}{cl}
1 & \forall \xi \in \mathbb{R}_{\mathrm{p}}^{3} \\
1 / 2 & \xi=\xi^{\Sigma} \in \Sigma_{\mathrm{p}} \\
0 & \text { Otherwise }
\end{array}\right.
\]

where \(\mathbb{R}_{\mathrm{p}}^{3}=\mathbb{R}_{0}^{3}\left(=\mathbb{R}_{\mathrm{f}}^{3}\right), \mathbb{R}_{1}^{3}, \mathbb{R}_{2}^{3}, \ldots, \mathbb{R}_{N_{\mathrm{p}}}^{3}\), with \(\mathbb{R}_{\mathrm{f}}^{3}\) the subspace of the fluid phase, \(\mathbb{R}_{\mathrm{i}}^{3}\) the subspace of solid phase-i, and \(N_{\mathrm{p}}\) the number of solid phases. The value of the phase-mask equals unity in the domain where the phase is defined, \(\mathbb{R}_{\mathrm{p}}^{3}\), equals zero outside the domain of the phase, and is arbitrary at the interface, \(\Sigma_{\mathrm{p}}\), usually set to \(1 / 2\).

To extend the validity of the governing equations, one starts by extending the definition of the dependent variables, \(\mathbf{q}_{\mathrm{p}}(\xi, t)\), from the domain occupied by phase-p, \(\forall \xi \in \mathbb{R}_{\mathrm{p}}^{3}\), to the entire space, \(\forall \xi \in \mathbb{R}^{3}\). This is achieved by setting

\[
\mathbf{q}^{\mathrm{p}}(\xi, t)=\left[\gamma^{\mathrm{p}}(\xi, t)\right]^{n} \mathbf{q}_{\mathrm{p}}(\xi, t)
\]

The phase-mask can be raised to any power of arbitrary natural number, \(n>1\). This generalization is used to extend the validity of the governing equations to \(\mathbb{R}^{3}\) (e.g., see the derivation of the momentum in Equation 4a presented below). It does not affect the properties of the time derivative or gradients of the phase-mask function, since derivatives of discontinuous functions are defined in the integral sense.

The governing equations for the extended dependent variables, \(\mathbf{q}^{\mathrm{p}}\), are derived by multiplying the governing equations and their boundary conditions in each phase by \(\left(\gamma^{\mathrm{p}}\right)^{n}\), using
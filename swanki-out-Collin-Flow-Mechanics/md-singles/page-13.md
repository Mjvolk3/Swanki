macroscale changes within the medium, \(L\), \(d_{\text {pore }} \ll \Delta \ll L\). Under these conditions, deviations from the intrinsic average have short correlation length with respect to the length scale of the \(\mathrm{AEV}\) and can be neglected regardless of whether the porous material is chemically active or inert (Whitaker 1999, Breugem et al. 2006).

The apparent drag term in the momentum equation is typically modeled within porous media by splitting the wall pressure into a volume-averaged pressure and a fluctuation pressure, \(\left.p_{\mathrm{f}}\right|^{\Sigma_{f}}=\) \(\left\langle p^{\uparrow}\right\rangle+\tilde{p}\), and modeling the surface integral to be proportional to the velocity (Whitaker 1986a),

\[
\left\langle(-\tilde{p} \boldsymbol{I}+\boldsymbol{\tau}) \cdot \boldsymbol{n}^{\mathrm{g}}\right\rangle=-\epsilon_{\mathrm{g}}^{2} \mu \underline{\mathbf{K}}^{-1} \cdot\langle\mathbf{u}\rangle
\]

where \(\underline{\mathbf{K}}\) is the Darcy coefficient (Darcy 1856). The coefficient has been investigated experimentally, numerically, and theoretically by several authors. Most theoretical work attempts to relate the nondimensional Darcy permeability (permeability divided by the square of the fiber radius) to the porosity of the structure. Several analyses carried on idealized porous media show that \(\underline{K}^{-1} \propto\left(1-\epsilon_{\mathrm{g}}\right)^{\alpha}\). In the low-Reynolds-number and high-Knudsen-number regime of interest for TPS, the Forchheimer correction term (Irmay 1958) is often neglected (Martin \& Boyd 2010). The Klinkenberg correction (Klinkenberg 1941) to Darcy's coefficient,

\[
\underline{\mathbf{K}}=\underline{\mathbf{K}}_{0} \cdot(\underline{\mathbf{I}}+\underline{\mathbf{b}} / p)
\]

is the appropriate form to use to account for noncontinuum flow effects. Both the continuum flow permeability, \(\underline{\mathbf{K}}_{0}\), and the slip parameter, \(\underline{\mathbf{b}}\), are dependent on the microstructure of the material (Marschall \& Milos 1998, Borner et al. 2017).

Closure models for the transition region in hypersonic flows between the multitemperature flow environment and the porous TPS material have not been extensively addressed. However, there is a large body of literature on the closure of the energy equations within porous materials. In general, the gas phase is assumed to be in thermal equilibrium, simplifying the thermodynamics. Similarly, the multiphase bulk is also assumed to be in thermal equilibrium due to its high thermal diffusivity \(\alpha=k_{\mathrm{b}} /\left(\rho C_{p}\right)_{\mathrm{b}} \gg 1\). This simplifies the heat transfer formulation to a two-temperature problem, one for the gas, \(T_{\mathrm{g}}\), and the other for the bulk, \(T_{\mathrm{b}}\). Two-temperature formulation was found necessary for the case of glass-filled polymer composites where glass melt and reactions with the carbonized polymer can result in significant convective heat transfer (Florio et al. 1991). But for composites where heat conduction within the preform structure drives the decomposition of the polymer resin and the Reynolds number of the flowing gas is \(\mathcal{O}(1)\), local thermal equilibrium is assumed to be valid.

Summing the averaged energy equations and using the interface boundary conditions leads to surface heat transfer integrals that sum to zero. Care must be taken to judicially solve for total bulk enthalpy that includes the latent heats of melt and evaporation (i.e., all of the energy absorbed by the surface decomposition lost by the gas phase). The resulting sum operation yields (Quintard 2015, Lachaud et al. 2017b)

\[
\frac{\partial\left\langle E_{t}\right\rangle}{\partial t}+\nabla \cdot\left(\epsilon_{\mathrm{g}}\langle\rho\rangle_{\mathrm{g}}\langle b\rangle_{\mathrm{g}}\langle\mathbf{u}\rangle_{\mathrm{g}}\right)+\nabla \cdot \sum_{k=1}^{N_{\mathrm{g}}}\langle\mathcal{Q}\rangle_{k}=-\nabla \cdot\left(\langle\mathbf{Q}\rangle+\left\langle\mathbf{Q}^{\mathrm{rad}}\right\rangle\right)
\]

In single-temperature formulation, the volume-averaged heat flux is modeled as

\[
\langle\mathbf{Q}\rangle+\left\langle\mathbf{Q}^{\mathrm{rad}}\right\rangle=-\underline{\mathbf{k}}^{\mathrm{eff}} \cdot \nabla\langle T\rangle
\]

where \(\underline{\mathbf{k}}^{\text {eff }}\) is the effective conductivity tensor of the material accounting for porous media radiation, gas, and solid conduction. Finally, the generation of species by pyrolysis occurs in regions with strong gradients of species concentration, temperature, and pressure. Multicomponent diffusion is potentially an important contributor to mass transport. A very convenient method that
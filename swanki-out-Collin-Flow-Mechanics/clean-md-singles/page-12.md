$n_{\mathrm{p}, c}$ : temperaturedependent exponent usually set to 1

$\chi_{\mathrm{p}, c}$ : advancement of pyrolysis reaction

$\mathcal{A}_{\mathrm{p}, c}$ : Arrhenius law preexponential factor

$\mathcal{E}_{\mathrm{p}, c}:$ Arrhenius law activation energy, $\mathrm{J} \cdot \mathrm{mol}^{-1}$

$\mathcal{R}$ : perfect gas constant,

$\mathrm{J} \cdot \mathrm{mol}^{-1} \cdot \mathrm{K}^{-1}$

$A_{k}$ : species, $k \in\left[1, N_{\mathrm{g}}\right]$, accounted for in the chemical system

$\zeta_{\mathrm{p}, c, k}:$ stoichiometric coefficients

$N_{\mathrm{g}}$ : total number of gaseous elements or species accounted for in the gas mixture
By definition, the intrinsic density of a solid phase, $\rho_{\mathrm{p}}$, is constant in time if swelling and shrinking are ignored. Therefore, the subphases, $\rho_{\mathrm{p}, c} \forall c \in\left[1, N_{\mathrm{p}, c}\right]$, are also constant in time. Here, $N_{\mathrm{p}, c}$ is the number of components in phase-p. To model the decomposition of the solid, Lachaud \& Mansour (2014) introduced the concept of progress variables, $\chi_{\mathrm{p}, c}$, which represents the remainder of the solid phase, i.e., $\chi_{\mathrm{p}, c}=1$ initially and $\chi_{\mathrm{p}, c}=0$ when the subphase is consumed. The advancement of $\chi_{\mathrm{p}, c}(t)$ is modeled using an Arrhenius law,

$$
\frac{1}{\left(1-\chi_{\mathrm{p}, c}\right)^{m_{\mathrm{p}, c}}} \frac{\partial \chi_{\mathrm{p}, c}}{\partial t}=T^{n_{\mathrm{p}, c}} \mathcal{A}_{\mathrm{p}, c} \exp \left(-\frac{\mathcal{E}_{\mathrm{p}, c}}{\mathcal{R} T}\right), \quad \forall \mathrm{p} \in\left[1, N_{\mathrm{p}}\right], \forall c \in\left[1, N_{\mathrm{p}, c}\right]
$$

This formulation for one solid phase $(\mathrm{p}=1)$ is the same as that used in almost all of the models currently in use.

The decomposition mechanism of the solid subphases produces elements/species, $A_{k}$, with stochiometry of the form (Lachaud \& Mansour 2014, Lachaud et al. 2017b)

$$
M P_{\mathrm{p}, c} \longrightarrow \sum_{k \in\left[1, N_{\mathrm{g}}\right]} \zeta_{\mathrm{p}, c, k} A_{k}, \quad \forall \mathrm{p} \in\left[1, N_{\mathrm{p}}\right], \forall c \in\left[1, N_{\mathrm{p}, c}\right]
$$

The chemistry within ablators is assumed to be in equilibrium, with source terms produced by the decomposition reactions (Equation 19). The derivation of the conservation equations for the element mass fractions $z_{k}$ under equilibrium chemistry is detailed by Giovangigli (1999). Volume averaging the element conservation equations and their boundary conditions yields

$$
\frac{\partial \epsilon_{\mathrm{g}}\left\langle\rho^{\mathrm{g}} z_{k}^{g}\right\rangle}{\partial t}+\nabla \cdot\left(\epsilon_{\mathrm{g}}\left\langle\rho^{\mathrm{g}} z_{k}^{\mathrm{g}} \mathbf{u}^{g}\right\rangle\right)+\nabla \cdot \epsilon_{\mathrm{g}}\left\langle\mathcal{F}_{k}^{g}\right\rangle=\epsilon_{\mathrm{g}}\left\langle\pi_{k}^{\mathrm{g}}\right\rangle, \forall k \in N_{\mathrm{g}}^{e}
$$

where $\epsilon_{g}\left\langle\pi_{k}^{g}\right\rangle$ is the production rate of elements by pyrolysis. The derivation of the expression for the diffusion flux, $\mathcal{F}_{k}$, is described in detail in the appendix of Lachaud et al. (2017b).

The volume-averaged momentum equation for incompressible flows was briefly discussed at the end of Section 3.2. For compressible flows, the extended momentum equation, Equation $4 \mathrm{a}$, with its associated boundary condition is volume averaged to yield the compressible version of the averaged incompressible equation discussed in Equation 3.2.

Finally, the derivation of the volume-averaged conservation of energy for multiphase systems starts by writing, in each phase, the conservation of energy with their associated boundary conditions. Each equation is multiplied by its corresponding phase-mask function to extend it to $\mathbb{R}^{3}$. Volume averaging the resulting equations yields the conservation of energy for reactive gases and bulk phase, with their associated no-surface-accumulation interface boundary conditions for two phases: gas phase, $\mathrm{f}$, and bulk phase, $\mathrm{b}$ (Lachaud et al. 2017b).

The boundary conditions are continuity of temperature and heat flux at the interface between the phases. Summing the averaged energy equations of all the phases eliminates the coupling terms between them, resulting in the conservation of total volume-averaged energy. However, after summing the energy equations, it will not be possible to extract separate volume-averaged temperatures for the fluid, $\left\langle T^{\mathrm{f}}\right\rangle$, and the bulk, $\left\langle T^{\mathrm{b}}\right\rangle$. Under local thermal equilibrium conditions (Whitaker 1986b), where $\left\langle T^{\mathrm{f}}\right\rangle \approx\left\langle T^{\mathrm{b}}\right\rangle$, the energy equations are summed to yield the volumeaveraged conservation of energy for a single volume-averaged temperature, $\langle T\rangle$. In this case, the volume-averaged temperature of the system is extracted by inverting the sum of the internal energies of the phases at constant pressure.

\subsection*{3.5. Closure Models}

Closure models are formally derived in porous media where the characteristic length of the averaging volume, $\Delta$, is much larger than the scale of the pores, $d_{\text {pore }}$, but is much smaller than
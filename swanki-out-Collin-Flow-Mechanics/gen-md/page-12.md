## Explain the temperature-dependent advancement of the pyrolysis reaction $\chi_{\mathrm{p}, c}$ in the context of solid phase decomposition using the Arrhenius law.

The advancement of the pyrolysis reaction $\chi_{\mathrm{p}, c}(t)$ is modeled using an Arrhenius law:

$$
\frac{1}{\left(1-\chi_{\mathrm{p}, c}\right)^{m_{\mathrm{p}, c}}} \frac{\partial \chi_{\mathrm{p}, c}}{\partial t} = T^{n_{\mathrm{p}, c}} \mathcal{A}_{\mathrm{p}, c} \exp \left(-\frac{\mathcal{E}_{\mathrm{p}, c}}{\mathcal{R} T}\right), \quad \forall \mathrm{p} \in \left[1, N_{\mathrm{p}}\right], \forall c \in \left[1, N_{\mathrm{p}, c}\right]
$$

Here, $\chi_{\mathrm{p}, c}=1$ initially and $\chi_{\mathrm{p}, c}=0$ when the subphase is consumed.

- **$T$**: Temperature
- **$n_{\mathrm{p}, c}$**: Temperature-dependent exponent, usually set to 1
- **$\mathcal{A}_{\mathrm{p}, c}$**: Arrhenius law preexponential factor
- **$\mathcal{E}_{\mathrm{p}, c}$**: Arrhenius law activation energy
- **$\mathcal{R}$**: Perfect gas constant
- **$m_{\mathrm{p}, c}$**: Kinetic exponent

- #chemical-reactions, #thermal-decomposition

## Define the stoichiometric coefficients $\zeta_{\mathrm{p}, c, k}$ and how they relate to the chemical system of species $A_{k}$.

The stoichiometric coefficients $\zeta_{\mathrm{p}, c, k}$ quantify the proportions of elements or species $A_{k}$ produced by the decomposition of solid subphases in the chemical system:

$$
M P_{\mathrm{p}, c} \longrightarrow \sum_{k \in \left[1, N_{\mathrm{g}}\right]} \zeta_{\mathrm{p}, c, k} A_{k}, \quad \forall \mathrm{p} \in \left[1, N_{\mathrm{p}}\right], \forall c \in \left[1, N_{\mathrm{p}, c}\right]
$$

- **$A_{k}$**: Chemical species in the system
- **$\zeta_{\mathrm{p}, c, k}$**: Stoichiometric coefficient for species $A_{k}$

- #stoichiometry, #chemical-reactions

## What equation models the conservation of element mass fractions $z_{k}$ in equilibrium chemistry and its boundary conditions?

The equation for conservation of element mass fractions $z_{k}$ under equilibrium chemistry is:

$$
\frac{\partial \epsilon_{\mathrm{g}} \left\langle \rho^{\mathrm{g}} z_{k}^{g} \right\rangle}{\partial t}+\nabla \cdot \left(\epsilon_{\mathrm{g}} \left\langle \rho^{\mathrm{g}} z_{k}^{\mathrm{g}} \mathbf{u}^{g} \right\rangle \right) + \nabla \cdot \epsilon_{\mathrm{g}} \left\langle \mathcal{F}_{k}^{g} \right\rangle = \epsilon_{\mathrm{g}} \left\langle \pi_{k}^{\mathrm{g}} \right\rangle, \quad \forall k \in N_{\mathrm{g}}^{e}
$$

- **$\epsilon_{\mathrm{g}} \left\langle \pi_{k}^{g} \right\rangle$**: Production rate of elements by pyrolysis
- **$\mathcal{F}_{k}$**: Diffusion flux 
- **$z_{k}$**: Element mass fraction 
- **$N_{\mathrm{g}}$**: Total number of gaseous elements

- #element-conservation, #chemical-equilibrium

## Describe the boundary conditions used in the derivation of the volume-averaged conservation of energy for multiphase systems.

The boundary conditions include continuity of temperature and heat flux at the interface between phases. Summing the averaged energy equations for all phases eliminates the coupling terms, resulting in the conservation of total volume-averaged energy:

The associated no-surface-accumulation interface boundary conditions for two phases (gas phase $\mathrm{f}$ and bulk phase $\mathrm{b}$) are:

- **Gas Phase ($\mathrm{f}$)**: 
- **Bulk Phase ($$\mathrm{b}$)**:
- **$\left\langle T^{\mathrm{f}} \right\rangle \approx \left\langle T^{\mathrm{b}} \right\rangle$** under local thermal equilibrium conditions.
- #energy-conservation, #multiphase-systems

## Summarize how the intrinsic density of a solid phase $\rho_{\mathrm{p}}$ remains constant in time and its implications.

The intrinsic density of a solid phase $\rho_{\mathrm{p}}$ is constant in time if swelling and shrinking are ignored. Consequently, the subphases $\rho_{\mathrm{p}, c} \forall c \in \left[1, N_{\mathrm{p}, c} \right]$ are also constant in time. 

- **Implications**: This assumption simplifies the modeling of decomposition kinetics and the calculation of progress variables $\chi_{\mathrm{p}, c}$, which represent the remainder of the solid phase.

- #density-constants, #solid-phase

## How does the concept of progress variables $\chi_{\mathrm{p}, c}$ help in modeling solid decomposition?

Progress variables $\chi_{\mathrm{p}, c}$ represent the remainder of the solid phase during decomposition, where $\chi_{\mathrm{p}, c}=1$ initially and $\chi_{\mathrm{p}, c}=0$ when the subphase is consumed:

$$
\chi_{\mathrm{p}, c}(t)
$$

- **Role**: Models the temporal advancement of decomposition using temperature-dependent kinetics, integrated with the Arrhenius law.

- #progress-variables, #solid-decomposition
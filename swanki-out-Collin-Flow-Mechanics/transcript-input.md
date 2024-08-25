\title{
Annual Review of Fluid Mechanis \\ Flow Mechanics in Ablative Thermal Protection Systems
}

\author{
Nagi N. Mansour, ${ }^{1,2}$ Francesco Panerai, ${ }^{1}$ Jean Lachaud, ${ }^{3}$ \\ and Thierry Magin ${ }^{4,5}$ \\ ${ }^{1}$ Center for Hypersonics and Entry Systems Studies (CHESS) and Department of Aerospace \\ Engineering, University of Illinois at Urbana-Champaign, Urbana, Illinois, USA; \\ email: nnm004@illinois.edu, nnmansour@gmail.com, fpanerai@illinois.edu \\ ${ }^{2}$ Computational Physics, LLC, Hillsborough, California, USA \\ ${ }^{3}$ Institute of Mechanics and Engineering, University of Bordeaux, Talence, France; \\ email: jean.lachaud@u-bordeaux.fr \\ ${ }^{4}$ Aero-Thermo-Mechanical Laboratory, Université Libre de Bruxelles, Brussels, Belgium \\ ${ }^{5}$ Aeronautics and Aerospace Department, von Karman Institute for Fluid Dynamics, \\ Rhode-St-Genese, Belgium; email: magin@vki.ac.be
}

Annu. Rev. Fluid Mech. 2024. 56:549-75

The Annual Review of Fluid Mechanics is online at fluid.annualreviews.org

https://doi.org/10.1146/annurev-fluid-030322010557

Copyright $๑ 2024$ by the author(s). This work is licensed under a Creative Commons Attribution 4.0 International License, which permits unrestricted use, distribution, and reproduction in any medium, provided the original author and source are credited. See credit lines of images or other third-party material in this article for license information.

![](https://cdn.mathpix.com/cropped/2024_06_05_12b654cc61e19ef45de4g-1.jpg?height=57&width=327&top_left_y=1745&top_left_x=152

ChatGPT figure/image summary: The image contains text that reads "ANNUAL REVIEWS CONNECT". It appears to be part of a logo or a heading for the Annual Reviews publication or its website. The design includes stylized text with the words "ANNUAL REVIEWS" in all caps and underlined, and the word "CONNECT" beneath it in a bold and larger font, signifying a connection or networking aspect associated with Annual Reviews. The overall color scheme of the text is red and white.)

www.annualreviews.org

- Download figures

- Navigate cited references

- Keyword search

- Explore related articles

- Share via email or social media

\section*{Keywords}

ablation, porous media, volume averaging, pyrolysis, gas-material interactions, thermal protection

\begin{abstract}
Ablative thermal protection systems have experienced renewed interest in the past decade owing to the retirement of NASA's Space Shuttle fleet and the US presidential mandate to develop technologies that enable humans to explore space beyond low Earth orbit. Blunt body architecture for spacecraft and the use of ablators for thermal protection systems returned as the primary choice in mission planning. This review addresses current progress in modernizing predictive tools for ablative material response. Current theory development leverages progress made in the theory of flows in porous media. This development, combined with progress in experimental techniques and high-end computing, is enabling the development of $3 \mathrm{D}$ macroscale models with realistic closure coefficients derived from direct numerical simulations of 3D microscale geometries of actual materials. While flight data quantifying ablative material response remain sparse, the next decade will be one of exploration in which heatshield instrumented spacecraft will provide crucial flight data for refining and validating closure models.
\end{abstract}

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

transform of Equation 14 for single-phase systems defined in $\mathbb{R}^{3}$. The split of the dependent variables for multiphase problems must consider that dependent variables are defined in $\mathbb{R}_{\mathrm{p}}^{3}$ only and that their volume average is defined in $\mathbb{R}^{3}$. The correct split defines the deviation with respect to the location of the AEV, $\mathbf{x}$ (Bachmat \& Bear 1986). Given that $\mathbf{q}_{\mathrm{p}}$ is defined only in phase-p, dependent variables are split as

$$
\mathbf{q}_{\mathrm{p}}(\mathbf{x}+\xi)=\gamma^{\mathrm{p}}(\mathbf{x}+\xi)\left\langle\mathbf{q}^{\mathrm{p}}\right\rangle(\mathbf{x})+\mathbf{q}_{\mathrm{p}}^{\prime \prime}(\mathbf{x}+\xi)
$$

Here the split is modified from Bachmat \& Bear's split by multiplying the intrinsic average, $\left\langle\mathbf{q}^{\mathbf{p}}\right\rangle$, by $\gamma^{\mathrm{p}}(\mathbf{x}+\xi)$ to be consistent with the fact that $\mathbf{q}_{\mathrm{p}}(\mathbf{x}+\xi)$ is defined only in phase-p. Multiplying Equation 15 by $\gamma^{\mathrm{p}}(\mathbf{x}+\boldsymbol{\xi}) \widehat{G}(\xi)$ and volume averaging yields

$$
\overline{\mathbf{q}^{\mathrm{p}}}=\epsilon_{\mathrm{p}}\left\langle\mathbf{q}^{\mathrm{p}}\right\rangle=\epsilon_{\mathrm{p}}\left\langle\mathbf{q}^{\mathrm{p}}\right\rangle+\overline{\left(\mathbf{q}^{\mathrm{p})^{\prime \prime}}\right.} \Rightarrow \overline{\left(\mathbf{q}^{\mathrm{p}}\right)^{\prime \prime}}=0
$$

In practice, order-of-magnitude analysis in porous media cases results in simplifications showing that differences between the two splits outlined in this section can be neglected (Davit et al. 2013). But the difference in the splits is important in IBM and LES applications.

\title{
3.4. Volume-Averaged Governing Equations of Ablators
}

In the free-stream region (environment) where $\epsilon_{\mathrm{f}}=1$, the volume-averaged governing equations revert to the LES-averaged equations. Splitting the dependent variables as in Equation 15 results in lumping together the Leonard's terms and the subgrid stress terms. Modeling of hypersonic environments has been recently reviewed by Candler (2019) and is not addressed here. Current practices use turbulence models developed for low-speed flows for closure of the governing equations (Candler 2019). It can be anticipated that closure models that address the transition region between the environment and the porous material for modeling TPS will borrow from recent progress in modeling incompressible flows over porous media (Breugem 2005, Breugem et al. 2006, Wood \& Valdés-Parada 2013, Wood et al. 2020, Valdés-Parada \& Lasseux 2021).

Within the porous TPS material, $\epsilon_{\mathrm{f}}<1$, the decomposition of the resin plays an important role in the protective function of the heatshield. The purpose of impregnating ablative composites with resin is to achieve endothermic resin decomposition that results in pressure buildup within the material that resists penetration of free-stream gases. The pressure within the porous material builds to levels of the surface pressure. Within the pores, the speed of gases generated by resin decomposition is a function of its decomposition rate. The decomposition rate of phenolic resin under typical atmospheric entry conditions and in-depth temperatures leads to low-speed viscous flows with velocities of the order of 0.2 to $1 \mathrm{~m} / \mathrm{s}$ in pores of effective diameters in the submillimeter range. This results in low-Reynolds-number flows, $\operatorname{Re}=\mathcal{O}(1)$, in the pores, well within the Darcy regime (Wood et al. 2020). Early resin pyrolysis models used a single kinetic equation of the Arrhenius form to represent the decomposition as a function of temperature (Scala \& Gilbert 1962). Unsatisfied with the performance of single-equation models, Goldstein (1965) introduced a two-reaction model that was immediately adopted by the community (Rindal et al. 1966). It is still used in today's mission designs and analyses (Chen \& Milos 1999, Beck et al. 2014, Wright et al. 2014, Meurisse et al. 2018). It is recognized that improvements to the engineering pyrolysis models are needed (Wright et al. 2015).

Modern pyrolysis models adopted in material response of TPS follow parallel decomposition reactions in which a solid phase, $\mathrm{p}$, occupying a subspace, $\mathbb{R}_{\mathrm{p}}^{3}$, is conceptually split into subphases, with intrinsic average density (Lachaud et al. 2017b),

$$
\left\langle\rho_{\mathrm{p}, c}\right\rangle=F_{\mathrm{p}, c}\left\langle\rho_{\mathrm{p}}\right\rangle
$$

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

macroscale changes within the medium, $L$, $d_{\text {pore }} \ll \Delta \ll L$. Under these conditions, deviations from the intrinsic average have short correlation length with respect to the length scale of the $\mathrm{AEV}$ and can be neglected regardless of whether the porous material is chemically active or inert (Whitaker 1999, Breugem et al. 2006).

The apparent drag term in the momentum equation is typically modeled within porous media by splitting the wall pressure into a volume-averaged pressure and a fluctuation pressure, $\left.p_{\mathrm{f}}\right|^{\Sigma_{f}}=$ $\left\langle p^{\uparrow}\right\rangle+\tilde{p}$, and modeling the surface integral to be proportional to the velocity (Whitaker 1986a),

$$
\left\langle(-\tilde{p} \boldsymbol{I}+\boldsymbol{\tau}) \cdot \boldsymbol{n}^{\mathrm{g}}\right\rangle=-\epsilon_{\mathrm{g}}^{2} \mu \underline{\mathbf{K}}^{-1} \cdot\langle\mathbf{u}\rangle
$$

where $\underline{\mathbf{K}}$ is the Darcy coefficient (Darcy 1856). The coefficient has been investigated experimentally, numerically, and theoretically by several authors. Most theoretical work attempts to relate the nondimensional Darcy permeability (permeability divided by the square of the fiber radius) to the porosity of the structure. Several analyses carried on idealized porous media show that $\underline{K}^{-1} \propto\left(1-\epsilon_{\mathrm{g}}\right)^{\alpha}$. In the low-Reynolds-number and high-Knudsen-number regime of interest for TPS, the Forchheimer correction term (Irmay 1958) is often neglected (Martin \& Boyd 2010). The Klinkenberg correction (Klinkenberg 1941) to Darcy's coefficient,

$$
\underline{\mathbf{K}}=\underline{\mathbf{K}}_{0} \cdot(\underline{\mathbf{I}}+\underline{\mathbf{b}} / p)
$$

is the appropriate form to use to account for noncontinuum flow effects. Both the continuum flow permeability, $\underline{\mathbf{K}}_{0}$, and the slip parameter, $\underline{\mathbf{b}}$, are dependent on the microstructure of the material (Marschall \& Milos 1998, Borner et al. 2017).

Closure models for the transition region in hypersonic flows between the multitemperature flow environment and the porous TPS material have not been extensively addressed. However, there is a large body of literature on the closure of the energy equations within porous materials. In general, the gas phase is assumed to be in thermal equilibrium, simplifying the thermodynamics. Similarly, the multiphase bulk is also assumed to be in thermal equilibrium due to its high thermal diffusivity $\alpha=k_{\mathrm{b}} /\left(\rho C_{p}\right)_{\mathrm{b}} \gg 1$. This simplifies the heat transfer formulation to a two-temperature problem, one for the gas, $T_{\mathrm{g}}$, and the other for the bulk, $T_{\mathrm{b}}$. Two-temperature formulation was found necessary for the case of glass-filled polymer composites where glass melt and reactions with the carbonized polymer can result in significant convective heat transfer (Florio et al. 1991). But for composites where heat conduction within the preform structure drives the decomposition of the polymer resin and the Reynolds number of the flowing gas is $\mathcal{O}(1)$, local thermal equilibrium is assumed to be valid.

Summing the averaged energy equations and using the interface boundary conditions leads to surface heat transfer integrals that sum to zero. Care must be taken to judicially solve for total bulk enthalpy that includes the latent heats of melt and evaporation (i.e., all of the energy absorbed by the surface decomposition lost by the gas phase). The resulting sum operation yields (Quintard 2015, Lachaud et al. 2017b)

$$
\frac{\partial\left\langle E_{t}\right\rangle}{\partial t}+\nabla \cdot\left(\epsilon_{\mathrm{g}}\langle\rho\rangle_{\mathrm{g}}\langle b\rangle_{\mathrm{g}}\langle\mathbf{u}\rangle_{\mathrm{g}}\right)+\nabla \cdot \sum_{k=1}^{N_{\mathrm{g}}}\langle\mathcal{Q}\rangle_{k}=-\nabla \cdot\left(\langle\mathbf{Q}\rangle+\left\langle\mathbf{Q}^{\mathrm{rad}}\right\rangle\right)
$$

In single-temperature formulation, the volume-averaged heat flux is modeled as

$$
\langle\mathbf{Q}\rangle+\left\langle\mathbf{Q}^{\mathrm{rad}}\right\rangle=-\underline{\mathbf{k}}^{\mathrm{eff}} \cdot \nabla\langle T\rangle
$$

where $\underline{\mathbf{k}}^{\text {eff }}$ is the effective conductivity tensor of the material accounting for porous media radiation, gas, and solid conduction. Finally, the generation of species by pyrolysis occurs in regions with strong gradients of species concentration, temperature, and pressure. Multicomponent diffusion is potentially an important contributor to mass transport. A very convenient method that

uses driving forces to estimate the bulk diffusion fluxes of mass $\mathcal{F}^{*}$ and energy $\mathcal{Q}^{*}$, when conserving either the species or the elements, was recently derived (Scoggins et al. 2020). The idea is to use the rigorous Maxwell model (Lachaud et al. 2017b) while simplifying its integration into the conservation equations by precomputing driving forces attributed to the pressure, temperature, and species mole fraction gradients. A simple model, inspired from the binary mixtures theory (Whitaker 1999), may be used as a first approximation to account for the porosity, $\epsilon_{\mathrm{g}}$, and the tortuosity, $\eta$, of the porous medium of interest. It reads

$$
\mathcal{F}=\frac{\epsilon_{\mathrm{g}}}{\eta} \mathcal{F}^{*}
$$

and

$$
\mathcal{Q}_{i}=\frac{\epsilon_{\mathrm{g}}}{\eta} \mathcal{Q}_{i}^{*}
$$

where $\eta$ is the material tortuosity factor.

\title{
4. THE ROLE OF EXPERIMENTS AND IMAGE-BASED DIRECT NUMERICAL SIMULATIONS
}

A combination of morphological, transport, and thermochemical properties are required to inform the closure model formulations presented in Section 3.4. An effective strategy consists of decoupling the multiphysics processes observed within an ablator into fundamental experiments under controlled conditions. Simple flow/material configurations are adopted, yet most experiments require a degree of computational modeling to extract the quantities of interest. Combined numerical/experimental approaches developed for lightweight carbon/phenolic ablators are reviewed in this section, with particular attention paid to image-based modeling techniques using X-ray computed microtomography $(\mu-\mathrm{CT})$. Recent advances in both synchrotron and laboratorybased $\mu$-CT and their application to ablator microstructures have provided access to a wealth of quantitative information for predicting ablator properties that are not easily attainable experimentally. Tomographic datasets describe porous media on a 3D grid of stacked gray images, where the voxel intensity value is proportional to the local material X-ray absorption. Morphological information on volume fraction of phases, material anisotropy, surface area, and porosity can be obtained from a straightforward analysis of material images or through direct numerical simulations (DNS). Figure $4 a$ shows the $\mu$-CT of FiberForm (the substrate of PICA), and Figure $4 b$ shows a flexible carbon felt used in the manufacture of conformal ablators. The microstructure of the material is resolved sufficiently, such that mesoscale features, including bulk porosity, fiber orientation, and anisotropic pore size, can be accurately computed using image segmentation and analysis (Ferguson et al. 2018). The images also resolve details at the microscale, such as fiber diameter, crenulated fiber cross-section, and fiber lumen (Panerai et al. 2017). An ongoing challenge in $\mu$-CT images of strongly anisotropic materials, such as weaves or fiber composites, is segmentation of the phases and determination of fiber and tow orientation. While these remain active areas of research, several methods to determine fiber orientation voxelwise from $\mu$-CT have been developed (Krause et al. 2010, MacNeil et al. 2019, Semeraro et al. 2020). Also noteworthy are recent advances in the quantification of uncertainties on effective properties calculated from 3D images due to segmentation errors (Krygier et al. 2021). A further challenge in thermal transport modeling is to numerically ensure the continuity of temperature and heat flux at the surface of each voxel. For this, the multipoint flux approximation class of methods is efficient and accurate (Semeraro et al. 2021, Aavatsmark 2002).

a
![](https://cdn.mathpix.com/cropped/2024_06_05_9c751454caf2681298f8g-1.jpg?height=814&width=530&top_left_y=170&top_left_x=240

ChatGPT figure/image summary: The image shows a computed microtomography (µ-CT) of a porous material with a complex three-dimensional fibrous structure. The upper part of the image illustrates the entire sample volume with a scale indicating that the sides of the cube measure 330 micrometers across, establishing the scale of the porous medium. The lower part of the image provides a close-up view that reveals the intricate web of fibers and the porosity within the material at a higher magnification, marked by a scale of 25 micrometers. This type of detailed imaging is crucial for analyzing the microstructure of materials, such as FiberForm or carbonized felt, and for informing simulations and models related to their physical properties, like thermal and mass transport.)

b
![](https://cdn.mathpix.com/cropped/2024_06_05_9c751454caf2681298f8g-1.jpg?height=812&width=520&top_left_y=171&top_left_x=822

ChatGPT figure/image summary: The image shows two representations of a fibrous material as derived from microtomography ($\mu$-CT) data. In the upper image (labeled as 'c'), we see a 3D rendering of the material's fibers, visualized as a cube with numerous elongated, cylindrical components intersecting each other, creating a complex and entangled network that illustrates the material's porous structure. In the lower image (labeled as 'd'), there is a close-up, 2D view of the fibers, providing detail on individual fiber morphology, such as the fiber diameter and the texture of the fiber surfaces. These images help researchers understand the physical characteristics of fibrous materials, like porosity and anisotropy, and are critical for simulations and models that predict the material's properties. The indication of a scale (25 µm) in the lower image provides a reference for the size of the features shown.)

Figure 4

Computed microtomography ( $\mu$-CT) voxel images of FiberForm $(a, c)$ and carbonized felt $(b, d)$. Figure adapted with permission from Panerai et al. (2017).

\title{
4.1. Thermal Transport
}

The effectiveness of lightweight ablators is sensitive to the conductivity of both the condensed phase and the gas phase. The large porosity limits the effective thermal conductivity to low values (typically below $1 \mathrm{~W} \mathrm{~m}^{-1} \mathrm{~K}^{-1}$ at room temperature), hindering conduction and limiting the temperature at the bondline between the TPS and the underlying structure. This bondline temperature is a design driver when sizing the thickness of the TPS. The microstructure of low-density ablators is highly anisotropic, usually transverse isotropic, optimized to minimize conductivity in the direction normal to the aeroshell interface with the environment, also known as the outer mold line (Panerai et al. 2017). The effective thermal diffusivity through high-porosity insulators is the result of combined solid conduction, gas conduction, and radiative transfer. These processes are closely coupled to the forced convection imposed by pressure gradients generated by the production of pyrolysis gases. Both radiation and conduction are important in the gas phase. The former is due to high temperatures and their large gradients experienced by ablators during flight. The latter is significant simply because the gas volume fraction is large in high-porosity materials. These transfer modes are both temperature and pressure dependent. Knudsen effects become prominent at low pressures and high temperatures that alter transport at the gas-solid interface. This is often accounted for by correcting the gas thermal conductivity based on the Knudsen number (Daryabeigi et al. 2011, Penide-Fernandez \& Sansoz 2021). A common approach to determining the effective thermal properties of ablators consists of using standard methods such as laser flash analysis, guarded hot plate, or comparative-longitudinal heat flow techniques at the expense of substantial approximations to actual flight conditions. Theoretical developments such as homogenization and volume averaging provide estimates of the effective conductivity of porous materials (Hornung 1997, Whitaker 1999, Leroy et al. 2013, Quintard 2015). These methods are

a

![](https://cdn.mathpix.com/cropped/2024_06_05_0d6b33a18daa3d6ea92cg-1.jpg?height=566&width=586&top_left_y=178&top_left_x=93

ChatGPT figure/image summary: The image provided depicts a computer-generated visualization of fluid flow through a porous medium. The colorful lines represent fluid streamlines, showing the direction and velocity of the flow, where various colors correspond to different velocities according to the legend at the bottom (ranging from 1.00 m/s to 7.50 m/s). The white structures possibly represent the solid framework of the porous medium, such as fibers in a fibrous mat or other solid obstacles within the flow path. This type of visualization is typically used in simulations of fluid dynamics to analyze the behavior of a fluid as it moves through complex geometries and helps in understanding phenomena like permeability, flow resistance, and the overall behavior of the fluid within the porous material.)

b

![](https://cdn.mathpix.com/cropped/2024_06_05_0d6b33a18daa3d6ea92cg-1.jpg?height=567&width=499&top_left_y=149&top_left_x=675

ChatGPT figure/image summary: In the image, you are looking at a 3D numerical simulation that represents the thermal transport in a fibrous porous material used as a Thermal Protection System (TPS). The image shows a complex network of fibers, with different colors on one face of the cube indicating a temperature gradient. This gradient is applied to understand how heat flows through the material's microstructure. The fibers appear in shades of gray and white, suggesting different levels of temperature or perhaps highlighting the complicated paths through which heat can transfer. The blue region around the fibers likely represents the cooler areas within the simulation, while warmer areas transition from green to red as the temperature increases, based on the typical convention used in heat maps.)

c

![](https://cdn.mathpix.com/cropped/2024_06_05_0d6b33a18daa3d6ea92cg-1.jpg?height=494&width=496&top_left_y=174&top_left_x=1196

ChatGPT figure/image summary: The first set of images from Figure 4:

a. Displayed is a $\mu$-CT voxel image of FiberForm, a material used in thermal protection systems (TPS). The image likely showcases its fibrous and porous structure, which contributes to its thermal insulation properties. Unfortunately, the image itself is not visible in the context you've provided, but based on the description, it would depict the intricate microstructure of FiberForm.

b. This image would be a $\mu$-CT voxel image of carbonized felt, another material used in TPS. Carbonized felt is known for its heat resistance and insulating capabilities. Just like with the previous image, the actual image is not presented here, but it would typically show a carbonized, porous textile structure.

As for the second set of images from Figure 5:

a. This would be an image-based simulation of flow transport within a porous material, which might illustrate how fluids move through the microscopic channels and voids within the material. The image should reveal pathways that allow for the transfer of gases or liquids.

b. This image would depict a simulation for thermal transport. It is likely to visualize the heat distribution and flow within a material, shedding light on how well the material conducts heat or how it traps and insulates against heat transfer.

c. The final image would be related to chemical transport and reactions within a material. This could include illustrations of how chemical reactions occur on a microscopic scale within the structure of the material or how chemicals might distribute within the pores.

To see the actual images, you would have to click on or open the attached images directly.)

Figure 5

Image-based simulation of effective properties: (a) flow transport (Borner et al. 2017), (b) thermal transport (Semeraro et al. 2021), and (c) chemistry (Ferguson et al. 2016, 2017). Panels $b$ and $c$ adapted from Ferguson et al. (2018) (CC BY 4.0).

useful for materials where the thermal conductivity of each phase is isotropic and the porosity is homogeneous. Semi-analytical models (Lee 1989, Marschall \& Milos 1997, Daryabeigi et al. 2011, Van Eekelen \& Lachaud 2011) and solutions to the radiative heat transfer equations (Petrov 1997, Le Foll et al. 2012) for fibrous media with anisotropic fiber orientation have been proposed. For cases where the microstructure is known and available either analytically or through $\mu-\mathrm{CT}$, Wiegmann \& Bube (2000) developed an efficient numerical method to solve the homogenization formulation for the conduction problem. For materials where the conductivity is anisotropic at the phase level and at the mesoscale (such as weaves), DNS using carefully chosen numerical methods is an effective approach (Semeraro et al. 2020). Recent studies have used stochastic techniques applied to microstructure data with opaque, transparent, or semitransparent phases to compute radiative conductivity of fiber-based TPS material (Nouri \& Martin 2015, Nouri et al. 2016). Well-established laboratory measurements are used to determine the heat capacity and the heat of pyrolysis by differential scanning calorimetry (Torres-Herrador et al. 2021). Figure 5 highlights a series of effective properties predictions based on carbon fiber microtomography measurements.

\title{
4.2. Mass and Momentum Transport
}

As illustrated in Section 3.5, the permeability in the Knudsen regime is of interest to TPS applications because the material pore scale is of the same order as the mean free path of the permeating gases. Permeability decreases as the Knudsen number increases but has a minimum in the transition regime (De Socio \& Marino 2006). DSMC is a natural choice for use with $\mu$-CT rendering of porous materials. This approach becomes computationally intensive at low Knudsen numbers, but results by DSMC have proven accurate when compared with experimental data (White et al. 2016, Borner et al. 2017). In the low-Knudsen-number regime, solving the low Reynolds number, incompressible equations are more efficient methods to estimate permeability from tomography data (Wiegmann 2007). Flow tube experiments provide validation sets for microscale and mesoscale simulations. Experimental efforts on ablative materials have demonstrated that both the intrinsic $\underline{\mathbf{K}}_{0}$ permeability and the Knudsen correction factor $\underline{\mathbf{b}}$ can be determined from differential pressure measurement across porous samples at increasing mass flows and average pressure

(Marschall \& Milos 1998, Panerai et al. 2016). Values at high temperatures can be easily estimated by scaling the effective permeability with gas viscosity, temperature, and molar mass to the values at room temperature, and corrections can be made to account for variability in material density. Tortuosity factors of fibrous ablators have been inferred using image-based simulations using both simplified geometries and 3D microtomography images. The factor was computed at all Knudsen regimes, from continuum to rarefied, by simulating Brownian motion diffusion with the use of random walk particle methods, DSMC, and finite-volume solutions of the diffusion equation, finding excellent agreement between the three techniques (see Ferguson et al. 2022 and references therein).

\title{
4.3. Chemical Transport and Rates
}

Pyrolysis decomposition is conventionally measured using a combination of thermogravimetric analysis and gas analysis techniques (e.g., gas chromatography and mass spectrometry), providing variation of material density as a function of time and temperature and quantification of gaseous products, respectively (Sykes 1967, Trick \& Saliba 1995, Trick et al. 1997). As part of recent experimental efforts, custom pyrolysis reactors have been developed to study the decomposition of PICA (Wong et al. 2016, Bessire \& Minton 2017). Bessire \& Minton (2017) showed that molar yields from the thermal decomposition of the phenolic resin SC-1008, used in most carbon/phenolic ablators, are dependent on heat rate, suggesting that pyrolysis of PICA is a nonequilibrium process.

Heterogeneous gas-material interactions remain an active field of research. Carbon-oxygen and carbon-nitrogen reactions at high temperature have been among the most studied processes in the literature, but many challenges remain for ablative TPS. Charring ablators can be made with various types of carbon fibers [e.g., rayon, polyacrylonitrile (PAN), pitch, or lyocell derived] and annealed and processed at different temperatures. These yield substantially different material properties. In addition, they decompose into heterogeneous carbonaceous phases in which fibers and charred matrix have significantly different microstructures and reactivities. While observations from high-enthalpy experiments suggest that reaction rates with oxygen are faster for matrix carbon than for fiber carbon, there are no quantitative data on this differential decomposition. Flow tube reactor and molecular beam experiments remain the main source of data for carbon oxidation and nitridation (Panerai et al. 2014, 2019; Murray et al. 2015, 2020; Murray \& Minton 2019). The quantification of oxidation and nitridation products in molecular beam data has enabled the development of new finite-rate ablation models for the carbon-air system (Poovathingal et al. 2016, 2017; Swaminathan-Gopalan et al. 2018; Prata et al. 2022). Compared with old models (Park 1976, Zhluktov \& Abe 1999), these models tend to favor the formation of $\mathrm{CO}$ relative to $\mathrm{CO}_{2}$, which leads to higher temperatures and lower recession compared to the equilibrium $B^{\prime}$ model. They show better agreement with experimental data (Candler 2019).

Image-based simulations enable modeling of the surface roughness during ablation. First developed for carbon/carbon ablators and extensively verified against analytical solutions (Lachaud 2006, Lachaud \& Vignoles 2009), these simulations have also been extended to porous carbon preforms (Ferguson et al. 2016, 2017, 2018; Panerai et al. 2017). Differences in ablation depth, differential reaction of matrix and fibers, and competing diffusion-reaction processes in rate-limited regimes are captured by these simulations and can be effectively used to predict microscale and mesoscale porous media evolution.

\section*{5. COUPLING THE ENVIRONMENT TO POROUS ABLATIVE MATERIAL}

Approaches to coupling the flow environment to the physics within porous systems follow three different levels of approximation (Chandesris \& Jamet 2007): (a) coupling down to the pore

![](https://cdn.mathpix.com/cropped/2024_06_05_4b8c4a7049080e7b018eg-1.jpg?height=901&width=1602&top_left_y=119&top_left_x=93

ChatGPT figure/image summary: The image you provided appears to be Figure 6 from an academic paper or similar publication, showing four different schematic representations of coupling flow to a porous wall. Each panel (a, b, c, and d) illustrates a different boundary condition or modeling approach for the interaction between a fluid flow (represented by blue lines for velocity profiles) and a porous material surface (shown in the micrographs below each schematic). Here's the detail of each panel:

a) Uncoupled/loosely coupled: There is a clear boundary layer edge with no modification to the straight velocity profile lines. Below it, a micrograph shows a highly porous material surface labeled as "Uncoupled/loosely coupled (FIAT/PATO)." The porous structure is untreated by the flow in the model, and the mass and energy balances are independent.

b) Slip velocity: This boundary condition allows for some slip at the interface surface, depicted by the small red dash lines near the surface in the velocity profile lines, indicating a shift in the boundary layer. Below this schematic, another micrograph of the porous material is labeled "Slip velocity (Beavers & Joseph 1967)."

c) Jump in shear stress: This condition shows a more pronounced adjustment to the velocity profile near the surface, with a "jump" in the shear forces at the interface, as noted by the thicker blue boundary layer line. Below the schematic, the associated micrograph is labeled "Jump in shear stress (Ochoa-Tapia & Whitaker 1995)."

d) Fully coupled: Here, the system treats the boundary layer edge and porous material surface as fully integrated, with the velocity profiles adjusting smoothly into the porous surface without any jumps or slips. Below this schematic, a micrograph of the porous surface is labeled "Fully coupled (Weng & Martin 2014, Schrooyen 2015)."

These schematics are combined with electron microscopy micrographs of a fiber-based porous material surface, illustrating the microstructure that would be involved in the theoretical modeling approaches. The use of such models is important in the context of analyzing how fluids interact with porous surfaces, a topic critical in materials science and engineering applications such as thermal protection systems for spacecraft.)

Figure 6

Coupling the flow to a porous wall: (a) uncoupled, (b) slip velocity, (c) jump in shear stress, and (d) fully coupled. $y_{\mathrm{e}}, h_{\mathrm{e}}$, and $p_{\mathrm{e}}$ are the boundary layer edge species mass fractions, specific enthalpy, and pressure, respectively. Abbreviations: BL, boundary layer; FIAT, fully implicit ablation and thermal; PATO, porous-material analysis toolbox based on OpenFOAM. Figure inspired by concepts presented in Beavers \& Joseph (1967), Ochoa-Tapia \& Whitaker (1995), Chandesris \& Jamet (2006), Weng \& Martin (2014), and Schrooyen (2015).

scale via DNS, (b) mesoscale coupling, and (c) macroscale coupling through interface boundary conditions. A schematic is shown in Figure $6 a$.

\title{
5.1. Direct Numerical Simulations at the Microscale
}

Current research trends in simulating flows over porous media lean toward using fully resolved DNS of turbulent incompressible flows (Breugem \& Boersma 2005, Chandesris et al. 2013, Jin \& Kuznetsov 2017, He et al. 2019, Wood et al. 2020, Valdés-Parada \& Lasseux 2021). These simulations are then used to test and develop closure models for the phase-averaged equations. DNS for compressible flows in regimes of interest to TPS applications have not received similar attention. We anticipate that simulations from the free stream to the interior of porous materials in support of fundamental studies will appear in publications within a few years as high-performance computers become more readily available.

\subsection*{5.2. Mesoscale Formulations}

Volume averaging closure models that resolve the transition between the environment and the ablative material are an active research area. In this approach, the gas phase in the ablator and the environment are treated as a single phase (see Figure 5d) separate from the solid phase. The transition between the environment and the porous ablator fluids is of the order of the filter width. Again, rapid progress is seen in mesoscale simulations of incompressible flows over porous materials (Breugem \& Boersma 2002, 2005; Valdés-Parada \& Lasseux 2021). Efforts to formulate mesoscale simulation models for ablative TPS are at the early stage of development

(Schrooyen 2015, Schrooyen et al. 2016, Weng \& Martin 2017). They demonstrate progress in porous plug flow-tube experiments (Panerai et al. 2014, 2019) designed to simulate fiber thinning during oxidation. Many challenges remain that need to be solved to mature the closure models and numerical solution methods of the volume-averaged governing equations. These include developing mesoscale models that reflect fiber pitting, melt flows, and robust numerical methods that handle all-Mach-number flows.

\title{
5.3. Macroscale Formulations
}

The current state of the art in planning space exploration missions or verifying and validating TPS design is to treat the environment and the material response as separate homogeneous regions that are coupled through boundary conditions. While velocity slip interface boundary conditions were developed for the momentum equations in the late 1960s (Beavers \& Joseph 1967, Saffman 1971) (see Figure 5b) and later refined by Ochoa-Tapia \& Whitaker (1995) (see Figure 5c), they have not been adopted by the ablation community. Proper interface boundary conditions for mass, momentum, and energy must satisfy balance equations between the two environments in order to tightly couple the two regions (Milos \& Rasky 1994, Martin et al. 2017). Coupling finite-rate chemistry plays an important role in interpreting arc jet data (Driver \& MacLean 2011). Recent trends lean toward coupling the hypersonic flow solver and the ablative material solver using finite-rate chemistry.

Uncoupled/loosely coupled modeling remains the most widely used approach. Modern variations build on work developed by the Aerotherm Corporation in the late 1960s. The computational capabilities at that time were limited to solving the boundary layer equations [Boundary Layer Implicit (BLIMP) code; Bartlett et al. 1968] for the fluids and a 1D material response code [Charring Material Thermal Response and Ablation Program (CMA); Moyer \& Rindal 1968] for the material thermal response. Current efforts use modern computational fluid dynamics (CFD) numerical methods and refined chemistry models for planetary entry environments (Gnoffo et al. 1989, Wright et al. 1998, Kirk 2007, Candler 2019). On the material response side, the adoption of porous ablative TPS materials for Mars exploration and future missions to the Moon and beyond renewed interest in 3D capabilities for the material response (Chen \& Milos 2005, Amar et al. 2011, Lachaud \& Mansour 2014, Weng \& Martin 2014, Lachaud et al. 2015, Weng et al. 2015, Meurisse et al. 2018, Yang et al. 2018). However, the current state of practice for coupling through an interface still relies on the work developed in the 1960s, where the CFD code simulates the environment and provides mass/species transfer and energy transfer from the environment to the wall is estimated through the use of Stanton numbers for mass $\left(C_{M}\right)$ and heat $\left(C_{H}\right)$ transfer and the values at the boundary layer edge for species and temperature. The current approach derives the coefficients from detailed CFD solution (Saunders \& Prabhu 2018). This effectively provides the correct heat transfer at the wall. The assumption of Lewis and Prandtl numbers of the same order provides an approximate species flux value at the wall. Using the same flux transfer coefficient for the species enables the use of $\mathrm{B}^{\prime}$ tables to estimate the surface recession, assuming equilibrium chemistry (Milos \& Chen 1997, Scoggins et al. 2020). The equilibrium assumption is a conservative estimate for wall recession and therefore it enables bounding risk analysis of atmospheric entry missions.

\section*{6. EXPLORING MARS: LESSONS LEARNED AND THE NEXT DECADE}

The heatshield of the MSL capsule that landed on Mars in 2012 was instrumented with thermocouples, recession sensors, and pressure sensors (Gazarik et al. 2008). These instruments provided for the first time detailed in-flight data during atmospheric entry. A similar suite of sensors was

\title{
1. INTRODUCTION
}

At 20:55 UTC on February 18, 2021, the Mission Control Center at NASA's Jet Propulsion Laboratory received confirmation of touchdown of the Mars 2020 mission at the Jezero Crater on Mars. The Mars 2020 spacecraft delivered Perseverance, a rover, and Ingenuity, a small robotic helicopter. It is the fifth spacecraft of NASA's Mars Exploration Program to successfully land a payload on the surface of the Red Planet. This achievement follows a series of successful landings by the Mars Exploration Rover, Phoenix, the Mars Science Laboratory (MSL), and Insight. Critical to the success of those missions is a series of spacecraft technologies that enable entry, descent, and landing (EDL), the shortest and most intense phase of exploration missions to planets with atmospheres. This phase is fondly referred to as "seven minutes of terror."

During entry, spacecraft blast through the atmosphere at hypersonic velocity, experiencing extreme aerodynamic heating. Blunt bodies, introduced in the early 1950s by H. Julian (Harvey) Allen (Allen \& Eggers 1953, Vincenti et al. 2007), are the most effective technical solution to handle extreme heating. They produce a large drag that rapidly decelerates the spacecraft and a detached bow shock that transfers far less heat to the vehicle than do oblique shocks generated by aerodynamically slender shapes. Allen's blunt body theory led to the development of ablative heatshields, a class of thermal protection system (TPS) materials that dissipate aerodynamic heating through thermo-chemo-mechanical decomposition processes. Compared with the reusable class, of which the Space Shuttle tiles are perhaps the most notable example, ablators are single-mission heatshield materials and enable spacecraft to survive entry velocities in excess of $10 \mathrm{~km} / \mathrm{s}$, such as those experienced during Moon or far Solar System return missions. Blunt bodies and ablative heatshields were instrumental in bringing the exploration pioneers back from the Moon during the Apollo program. They also protect intercontinental ballistic missiles from large peak heating at relatively low altitudes. Today, ablative heatshields are effectively used in defense, transportation, energy, and space exploration systems.

This review covers flow mechanics and thermochemical processes in lightweight, highly porous ablative heatshields for atmospheric entry. We focus on TPS materials characterized by densities below $0.5 \mathrm{~g} / \mathrm{cm}^{3}$ and large porosities ( $\gtrsim 80 \%$ ). This class is designed to achieve superior insulation performance by reducing the through-thickness heat transfer and by producing endothermic chemical processes within the material that blow cool gases through the structure into the boundary layer. A prominent example within the low-density class is NASA's phenolic impregnated carbon ablator (PICA), a porous material $\left(\sim 0.3 \mathrm{~g} / \mathrm{cm}^{3}\right)$ made of a rigid carbon fiber preform (FiberForm) and infused with a cross-linked phenolic resin (SC-1008). The Stardust sample return capsule, the fastest human-made object to enter Earth's atmosphere ( $12 \mathrm{~km} / \mathrm{s}$ ) to date, was equipped with a monolithic PICA TPS, while returning samples from the coma of the Wild 2 comet. Both Mars 2020 and MSL used a tiled PICA heatshield for thermal protection during atmospheric entry. SpaceX has adopted a variant of PICA, named PICA-X, to outfit its Dragon spacecraft for return from low Earth orbit. PICA-class heatshield materials such as ASTERM and Zuram are being developed in Europe for space exploration missions. We refer the reader to Natali et al. (2016) for a comprehensive review of the materials science of ablative TPS.

Sizing of the heatshield is a critical task in the design process of an atmospheric entry system. Preliminary selection and performance assessment are based on analytical entry heating calculations. Given an anticipated trajectory, the maximum heat flux $\dot{q}_{\max }$ and maximum surface-averaged heat flux $\bar{q}_{\text {max }}$ drive material selection, while the time integrated heat input (or heat load) $Q$ informs the material volume (thickness) required for thermal protection. For detailed design and qualification, researchers use engineering material response codes to compute the temperature at the interface between the ablator and its carrying structure, and perform sizing and margin analyses based on stochastic simulations. NASA uses the Fully Implicit Ablation and Thermal (FIAT)


![](https://cdn.mathpix.com/cropped/2024_06_05_ee8d0cddeb3fb2dc62fbg-1.jpg?height=522&width=1286&top_left_y=122&top_left_x=406

ChatGPT figure/image summary: The image you've provided contains two circular diagrams labeled (a) and (b), which are color-coded heat maps from a simulation or analysis.

Diagram (a) represents the predicted surface temperature of a structure, likely a heatshield, at a certain point in time after atmospheric entry (possibly of the Mars Science Laboratory mentioned in the text). The color scale on the left side of diagram (a) indicates the temperature in Kelvin, with red denoting higher temperatures and yellow to green denoting lower temperatures.

Diagram (b) illustrates the differential recession of the same structure, which indicates the material loss due to ablation during atmospheric entry. The color scale on the right side of diagram (b) indicates the depth of material recession in meters, with darker blue representing more recession and lighter blue to green indicating less recession.

Together, these diagrams are used to show the results of heat and material response simulations for space vehicles entering an atmosphere, providing insights into the thermal protection system's performance. The text states that these figures are adapted with permission from Meurisse et al. (2018) and are associated with the Mars Science Laboratory's heatshield during atmospheric entry.)

Figure 7

Predicted surface temperature (a) and differential recession (b) at 70 s after the Mars Science Laboratory's atmospheric entry interface. Figure adapted with permission from Meurisse et al. (2018).

mounted on the Mars 2020 capsule. Data from that lander are currently being analyzed. The data from MEDLI (Bose et al. 2014) provided the first flight data for in-depth response of the TPS temperature. Insight into the location of the boundary layer transition during Mars entry was achieved from the change in slope in the time evolution of the temperature profiles (Bose et al. 2014). Detailed analysis of the data shows that refinement of current models of boundary layer transition estimates and in-depth material response are needed.

The MEDLI data are still being used intensively to provide insight into the physics during atmospheric entry and to address the inherent uncertainty of existing models (Mahzari et al. 2015). The heatshield of MSL was built with PICA tiles with room-temperature-vulcanizing (RTV)-silicon-filled gaps in between them. Differential recession between the RTV and PICA (see Figure 7) results in discontinuities of the surface that may play a large role in the transition of the boundary layer from laminar to turbulent flows. This area of research has not been addressed to the extent necessary to provide an educated input to risk analysis.

In the next decade, several missions are planned and are being coordinated to bring back samples from Mars. Some of these missions will have instrumented heatshields that will enable refinement of aerothermal models of the Mars atmosphere as well as data within the porous heatshields. The efforts in the coming decade will culminate with the Mars sample return mission, which will bring back and release the Earth entry vehicle with an instrumented heatshield. The Earth entry vehicle is scheduled to return to Earth in 2031.

\title{
SUMMARY POINTS
}

1. Reviewing the scientific advancements and technological achievements of the 1960s and 1970s in support of space exploration leaves one in admiration of the scientists of that period. A large portion of advancements made during that period remain relevant and are in current practice. Their reports show that they understood the limitation of their methods given the available technology at the time.

2. Fast progress is observed in direct numerical simulations (DNS) of fully coupled free-stream/porous wall flows for incompressible flows that take advantage of modern

numerical methods and advancements in computational capabilities. These are proving extremely valuable for developing mesoscale closure models.

3. Advances in computed microtomography have enabled access to the microstructure of thermal protection system (TPS) materials. DNS of digitized TPS material geometry are enabling direct computation of effective transport properties.

4. Three-dimensional loosely coupled material response codes are being rapidly developed. Progress is being made in fully coupled simulations of chemically reactive flows and porous materials to study the oxidation of carbon preforms.

5. Direct simulation Monte Carlo methods are pioneering advances in fully coupled simulations in the Knudsen regime.

\title{
DISCLOSURE STATEMENT
}

The authors are not aware of any biases that might be perceived as affecting the objectivity of this review.

\section*{ACKNOWLEDGMENTS}

The authors gratefully acknowledge initial support from NASA's Entry Systems Modeling project that initiated their collaborations a decade age. They also thank M. Wright, A. Calomino, M. Munk, M. Barnhardt, and M. Stackpoole for their continued encouragement to pursue a fresh new look at modeling ablative heatshields of interest to planetary explorations. Finally, they give special thanks to A. Borner, B. Dias, and J. Meurisse for reviewing the article and for their collaborations on ablation modeling.

\section*{LITERATURE CITED}

Aavatsmark I. 2002. An introduction to multipoint flux approximations for quadrilateral grids. Comput. Geosci. $6(3): 405-32$

Allen HJ, Eggers AJJ. 1953. A study of the motion and aerodynamic heating of ballistic missiles entering the Earth's atmosphere at high supersonic speeds. Tech. Rep. NACA RM A53D28, Natl. Advis. Comm. Aeronaut., Moffett Field, CA

Amar A, Calvert N, Kirk B. 2011. Development and verification of the charring ablating thermal protection implicit system solver. Paper presented at 49th AIAA Aerospace Sciences Meeting including the New Horizons Forum and Aerospace Exposition, Orlando, FL, AIAA Pap. 2011-144

Bachmat Y, Bear J. 1986. Macroscopic modelling of transport phenomena in porous media. 1: The continuum approach. Transport Porous Media 1(3):213-40

Bailey SC, Bauer D, Panerai F, Splinter SC, Danehy PM, et al. 2018. Experimental analysis of spallation particle trajectories in an arc-jet environment. Exp. Thermal Fluid Sci. 93:319-25

Bartlett EP, Kendall RM, Rindal RA. 1968. An analysis of the coupled chemically reacting boundary layer and charring ablator: Part 3 - nonsimilar solution of the multicomponent laminar boundary layer by an integral matrix method. Tech. Rep. NASA CR-1062, Natl. Aeronaut. Space Adm., Moffett Field, CA

Bear J. 1988. Dynamics of Fluids in Porous Media. New York: Dover

Bear J, Bachmat Y. 1967. Generalized theory on hydrodynamic dispersion in porous media. Int. Union Geod. Geophys. Publ. 72:7-16

Beavers GS, Joseph DD. 1967. Boundary conditions at a naturally permeable wall. 7. Fluid Mech. 30(1):197-207 Beck RA, Driver DM, Wright MJ, Hwang HH, Edquist KT, Sepka SA. 2014. Development of the Mars Science Laboratory heatshield Thermal Protection System. 7. Spacecr. Rocket. 51(4):1139-50

code (Chen \& Milos 1999) and the Charring Ablator Response (CHAR) code (Amar et al. 2011) for TPS design and sizing. The underlying physical models in these tools are built on the Aerotherm model described in a collection of well-known reports from 1968 (Kendall et al. 1968).

The past decade has witnessed renewed interest in the development of ablation response codes and improved ablation models (Amar et al. 2011, Lachaud \& Mansour 2014, Lachaud et al. 2017b, Meurisse et al. 2018, Weng et al. 2021). The new interest was motivated by the retirement of NASA's Space Shuttle fleet and by new flight data available for model assessment and validation. The recovery of the Stardust heatshield enabled in-depth postflight analysis of PICA (Stackpoole et al. 2008), demonstrating in-depth density variations and volume ablation (Lachaud et al. 2010). The data from MSL Entry, Descent, and Landing Instrumentation (MEDLI) (Gazarik et al. 2008) and MEDLI-2 provided time traces of in-depth thermal responses of PICA, revealing discrepancies between flight data and engineering predictions (Bose et al. 2014). Today, higherfidelity ablation models are needed that enable robust reliability analyses and reduced margins, model TPS coatings and interfaces, and predict material responses to exotic atmospheres of unexplored planets. The steps of formulating state-of-the-art ablation models are reviewed in this article.

In Section 2, we discuss the pyrolysis and ablation phenomena that lightweight ablators experience when exposed to high heating rates. In Section 3, we review the theory of volume averaging and then summarize the governing equations (Section 3.4) that describe the thermochemical and chemistry processes within a low-density porous ablator. The formulation is general and can be adapted across ablator types, such as closed porosity media (e.g., AVCOAT) or dense carbon/phenolic ablators. It is also applicable to the analysis of any reactive porous medium at high temperature, including pyrolyzing biomasses, burning wood, and fire-protection materials. In Section 4, we describe experiments and computations at the microscale that support the development and closure of ablation models, with a focus on image-based simulations of effective properties and responses at the microscale and mesoscale. In Section 5, we review recent trends in modeling flows over porous media coupled with the environment and the flow within the porous material. Rapid progress is being achieved for incompressible flows in this area, and several efforts toward formulating a unified solver for TPS response are showing promise. In Section 6, we review exploration missions that have provided flight data on the heatshield response during Mars atmospheric entry. Planned Mars sample return missions have the potential to bring new data that will be used in the coming decades to validate theory and model developments.

\title{
2. ABLATION PHENOMENA
}

The main processes that occur when a PICA-class ablator is exposed to extreme heating are illustrated in Figure 1. The porous structure of a low-density carbon/phenolic ablator is made of a carbon-bonded carbon fiber preform (skeleton) with volume fractions of the order of $\epsilon_{\text {fiber }} \simeq$ 0.1 and pore diameters $d_{\text {pore }} \simeq 50-100 \mu \mathrm{m}$. Carbon fibers of the preform are discontinuous and have a diameter $d_{\text {fiber }} \approx 5-10 \mu \mathrm{m}$, depending on their precarbonization origin and graphitization process. They are organized in a layered transverse isotropic structure [i.e., they are preferentially $\left( \pm 20^{\circ}\right)$ aligned along a plane of isotropy]. This architecture favors in-plane heat transfer and flow transport compared to the through-thickness direction, improving insulation capabilities and limiting permeation of hot boundary layer gases into the material. Rigidity of the preform is achieved by bonding at fiber intersections by discrete regions of a carbon matrix. The pore space between the fibers is filled with a nano-dispersed high-surface-area resin matrix, with characteristic pore scales of $d_{\text {resin }} \simeq 1-100 \mathrm{~nm}$. The matrix has volume fractions of $\epsilon_{\text {resin }} \simeq 0.05-0.15$, rendering bulk solid fractions $\epsilon_{\text {bulk }} \simeq \epsilon_{\text {fiber }}+\epsilon_{\text {resin }} \simeq 0.15-0.25$ (i.e., porosities of $\epsilon_{\text {pore }}=1-\epsilon_{\text {bulk }} \simeq 0.75-0.85$ ).


![](https://cdn.mathpix.com/cropped/2024_06_05_af72f70fe3a00d9900e5g-1.jpg?height=1198&width=1534&top_left_y=123&top_left_x=128

ChatGPT figure/image summary: This image depicts various aspects of the ablation phenomenon as it pertains to thermal protection systems (TPS) materials like the phenolic impregnated carbon ablator (PICA) used in spacecraft heatshields.

Panel (a) provides an illustration and schematic overlay that describes the ablation process occurring as a heatshield encounters extreme temperatures during atmospheric re-entry. The schematic indicates various thermal and chemical processes involved in the ablation of TPS material, such as pyrolysis, sublimation, and oxidation, as well as the temperature ranges at which these processes occur. The background image seems to be an experimental setup possibly capturing the glow of hot material undergoing ablation.

Panels (b), (c), and (d) are micrographs showing different stages of the ablation process:
- Panel (b) shows the surface of the material that might have already undergone some ablation, as indicated by the fibers being exposed and looking frayed or melted.
- Panel (c) appears to show the material in a state of partial pyrolysis with fibers that are less defined, likely due to thermal degradation.
- Panel (d) depicts the virgin material in its initial, unexposed state with a clearer and more uniform structure of fibers before any ablation or pyrolysis has taken place.

The overall image provides both a visual and a conceptual understanding of the changes in the microstructure of TPS materials as they are exposed to the harsh environment of atmospheric re-entry, which is essential for advancing the design and reliability of future spacecraft heatshields.)

Figure 1

(a) Illustration of the ablation phenomenon. The background image is an ablation experiment in the Plasmatron facility at the von Karman Institute for Fluid Dynamics. (b-d) Micrographs of different stages of ablation: (b) surface, (c) partially pyrolyzed, and (d) virgin phenolic impregnated carbon ablator (PICA). Panel $b$ adapted with permission from Helber et al. (2015). Panels $c$ and $d$ provided by Mairead Stackpoole (NASA).

Typical heatshield thicknesses range between 3 and $8 \mathrm{~cm}$ depending on the mission. For example, MSL PICA tiles were $3.2 \mathrm{~cm}$ thick, while Stardust used a 6.5 -cm-thick monolithic aeroshell. Other ablators within the lightweight class feature different microstructures and solid phase combinations. For example, AVCOAT, used on Apollo and Orion, is made of polymer microballoons mixed with silica fibers, such that large volume fractions of the material consist of closed porosity, where gas transport is limited. The silicon impregnated reusable ceramic ablator (SIRCA), a lightweight material often used as backshell TPS, is made of a fibrous silica substrate with a silicone impregnant. Cork and certain super-lightweight ablators (SLAs) feature rectangular and honeycomb cells. Length scales in those media are similar to those in PICA. These length scales, together with the tailored fiber arrangement, drive all transport phenomena described hereafter.

During atmospheric entry, the ablative TPS progressively heats up as it encounters a denser atmosphere. Increasing temperatures modify the degree of cross-linking of the polymeric matrix, leading to progressive thermal degradation via pyrolysis. This decomposition process (charring)

begins at approximately $400 \mathrm{~K}$ and is heat rate dependent (Stokes 1995; Bessire \& Minton 2017; Torres-Herrador et al. 2019, 2020). In turn, heating rates are mission dependent, evolve during flight, and are a function of depth within the material. They range from a few to hundreds of kelvins per second. Pyrolysis generates a pressure-driven flow and thermochemical transport through the porous medium of gases that include water vapor, permanent gases, hydrocarbons, and aromatics. It also leads to a progressive change in material density and porosity at the pore scale of the matrix (transitioning from nanometer to micrometer scale), both contributing to modify the effective transport properties of the porous material. Pyrolysis products transported through the fibers and the matrix by advection and diffusion undergo homogeneous chemical reactions and heterogeneous reactions with the solid phases. Coking effects may occur at temperatures between 1,100 and $1,400 \mathrm{~K}$, when hydrocarbons interact with the char and deposit solid carbon, releasing hydrogen. The thermochemistry of pyrolysis is further discussed in Section 3.4. Heterogeneous pyrolysis gases-solid phase interactions remain an active field of research.

Because of the large temperature range, a distinct feature of the ablative system is that mass and momentum transport of gases spans regimes from continuum to rarefied. The mean free path of the gas mixture that increases with temperature and decreases with pressure can be of the same order of the pore scales at certain flight conditions. During entry, while the flow is mostly in the continuum regime at the scale of the hypersonic body, Knudsen numbers within the porous ablator are in the transitional $(0.1 \lesssim \mathrm{Kn} \lesssim 100)$ or slip $(0.02 \lesssim \mathrm{Kn} \lesssim 0.1)$ regime (Lachaud et al. 2010) and transport is substantially affected by wall collisions. Close to the surface, a transition occurs at high temperature from the continuum regime in the boundary layer to the noncontinuum regime within the porous material. While the phase-averaged models described in Section 3.4 are based on the assumption of continuum flow, the Boltzmann equation is often a more accurate model for dilute gas dynamics. This observation has motivated the use of particle-based simulations, such as the direct simulation Monte Carlo (DSMC) method, to determine Knudsen corrections to the momentum equation, for example, by introducing a pressure-dependent Klinkenberg term in Darcy's model for the permeability of porous ablators (Marschall \& Milos 1998, Panerai et al. 2016, Borner et al. 2017).

At temperatures above $1,200 \mathrm{~K}$, pyrolysis is complete and the remaining carbonaceous char layer interacts with both the pyrolysis gases and the reactants transported to the surface. This ablation zone is dominated by finite-rate heterogeneous reactions, such as oxidation and nitridation, phase changes (e.g., sublimation of solid carbon into gas carbon species), and mechanical material removal by friction and shear stresses (spallation) (Bailey et al. 2018, Price et al. 2022). The extent of the ablation zone is the result of competing diffusion-reaction processes. Diffusive transport within porous ablators is often modeled using Fickian diffusion. Fick's law can be derived from the Boltzmann equation and keeps the same form at all regimes, from the continuum to the rarefied. The effective diffusion coefficient uses a tortuosity factor $\eta$ to correct the reference diffusivity for species transport (cf. Section 3.5).

Effects of hydrodynamic dispersion on diffusive transport can be neglected both in the continuum regime, because of the small Péclet number for the mass transfer (owing to the small pore scales), and in the rarefied regime, because of the limited gas phase collisions. Reactions of the solid phases with radicals from the boundary layer are temperature-dependent processes, widely modeled as a set of Arrhenius rate equations. Several efforts have been dedicated to developing new models for carbon-oxygen systems based on modern experiments (Candler 2019). Competing diffusion-reaction processes are described by the Thiele number. In oxygen-rich environments, low Thiele numbers $(\Phi \rightarrow 0)$ pertain to a reaction-limited regime, in which oxygen can penetrate the porous medium, producing a large ablation zone (of hundreds of microns in depth) with a graded in-depth porosity. Porosity gradients, in turn, affect all effective transport processes. This

is a typical regime experienced during the late phase of an entry trajectory where temperatures are moderate and the char reactivity to oxygen is low. Conversely, high Thiele numbers $(\Phi \rightarrow \infty)$ pertain to a diffusion-limited regime, in which all available oxygen reacts near the surface, leading to rapid material recession. At near-unit Thiele numbers, diffusion and reaction processes balance each other and a reaction zone of the order of the pore scale is produced (Lachaud et al. 2010; Ferguson et al. 2016, 2017; Vignoles et al. 2018). The different carbon properties of the charred matrix and fiber lead to different reactivities. From the analysis of arc jet experiments, the charred matrix reacts with oxygen faster than the carbon fibers do. This leads to near-surface regions with large pore scales of the order of the FiberForm pore scale and needling of fibers (Figure 1b). Needle formation for carbon/carbon ablators is discussed and modeled by Lachaud et al. (2017a).

The mass transport and chemical phenomena described above are all tightly coupled to complex heat transport processes by solid conduction, gas conduction, and radiation. Heat transfer depends on temperature, heating rates, the evolution of fiber and matrix with decomposition, and proximity to the surface, where radiation from the gas phase can be substantial. Because of the small pore scale, Péclet numbers are small for typical values of velocity and thermal diffusivity found in porous ablators. Hence, at most conditions, solid and gas phases are in thermal equilibrium (Puiroux et al. 2004). For nonequilibrium conditions, two-temperature models are necessary and are briefly discussed in Section 3.5 .

\title{
3. GOVERNING EQUATIONS IN ABLATIVE POROUS MEDIA
}

The response to high enthalpy of ablative porous material at the macroscale is modeled as a multiphase system where the fluid and the material are treated as separate phases with known governing equations at the microscale. The macroscale governing equations are derived by upscaling through volume averaging the microscale equations to scales that can be resolved with modern numerical methods. The volume averaging method (VAM) is covered in numerous works and books on porous media (Bear \& Bachmat 1967, Marle 1967, Gray \& Lee 1977, Whitaker 1999, Wood \& Valdés-Parada 2013, Quintard 2015) and prior literature on fire protection, geophysics, composites, multiphase flows, and many other subtopics of fluid mechanics. However, the connection between VAM and other methods widely used in single-phase fluid mechanics is rarely identified. This section covers volume averaging the governing equations of ablative TPS materials in a manner that demonstrates the relations between VAM (Whitaker 1999), the immersed boundary method (IBM) (Peskin 1972, Goldstein et al. 2005, Mittal \& Iaccarino 2005), and the large-eddy simulation (LES) method (Leonard 1975).

To link VAM to IBM, one first extends the governing equations from their validity in the domain of interest in each phase to the entire space, $\mathbb{R}^{3}$; this is discussed in Section 3.1. The link between the spatial smoothing approach adopted in VAM and the filtering approach followed in LES is outlined in Section 3.2. Finally, the fundamental difference between VAM and LES of splitting the dependent variables into averaged and unresolved scales is briefly discussed in Section 3.3 .

\subsection*{3.1. Extending the Governing Equations to $\mathbb{R}^{3}$}

The phases in VAM are assumed to be separate, with known governing equations and boundary conditions at the interface between phases at all points in the domain of the phase, $\mathbb{R}_{\mathrm{p}}^{3}$. At the scale of physically distinct phases, which we term the microscale, the problem is in principle solvable, given there are enough computational resources to resolve the dynamics in the phases. However, the physics of interest in applications is at large scales that would require computational resources that are not readily available. The goal of VAM is to derive governing equations of the dynamics

![](https://cdn.mathpix.com/cropped/2024_06_05_c61f1c04f668f80a804eg-1.jpg?height=741&width=1091&top_left_y=128&top_left_x=245

ChatGPT figure/image summary: This image contains a schematic representation related to the volume averaging method (VAM) that's described in the paper. The figure shows a cross-sectional view of a two-phase system with distinct phase-mask functions represented for two different phases, labeled as α (alpha) and β (beta). The phase-mask functions, denoted as γα and γβ, have values that indicate the presence of a particular phase: they are marked as '1' within the domain of their respective phase, '1/2' at the interface, and '0' elsewhere.

The image also demonstrates how the surface of interface, labeled as Σα, is represented with a normal vector nα pointing outward. There is an indication of a Dirac delta function δ(ξ − ξΣα) along the interface, and its gradient, shown symbolically and represented with arrows, indicates the direction and magnitude of change.

At the bottom of the image, there are plots of the phase-mask functions as a function of position, showing the values transitioning from '1' to '0' along an arbitrary line A-A across the phases, which likely represents a 1D slice through the 3D volume depicted above.

The right side of the image shows a magnified view of an interface with the wall velocity vector w represented by dashed lines with arrowheads, and the effect of the wall on the interface, producing a change in the phase-mask function over time (∂γα/∂t). The Dirac delta function and its interaction with the wall velocity and the normal vector are illustrated.

Overall, the figure visualizes how one defines and uses phase-mask functions in the context of the VAM framework for dealing with multi-phase systems, which is important in the study of ablative porous materials discussed in the paper.)

Figure 2

Definition of phase-mask functions, $\gamma_{\alpha}$ and $\gamma_{\beta}$, for two phases, $\alpha$ and $\beta$, and derivatives of $\gamma_{\alpha}$ in space and time.

at large scales that can be resolved with available computer resources. This is achieved by first extending the validity of the governing equations from $\mathbb{R}_{\mathrm{p}}^{3}$ to the entire space $\mathbb{R}^{3}$ (Salathe \& Sirovich 1967; Sirovich 1967, 1968). Phase-mask functions are used to distinguish between phases (Bear \& Bachmat 1967, Marle 1982, Breugem 2005, Wood \& Valdés-Parada 2013).

In ablators, the phase-mask function, $\gamma^{\mathrm{p}}$, for a phase-p, is a function of position, $\xi$, and time, $t$, to account for a moving interface between phases caused by surface reactions (Figure 2). It is defined as

$$
\gamma^{\mathrm{p}}(\xi, t)=\left\{\begin{array}{cl}
1 & \forall \xi \in \mathbb{R}_{\mathrm{p}}^{3} \\
1 / 2 & \xi=\xi^{\Sigma} \in \Sigma_{\mathrm{p}} \\
0 & \text { Otherwise }
\end{array}\right.
$$

where $\mathbb{R}_{\mathrm{p}}^{3}=\mathbb{R}_{0}^{3}\left(=\mathbb{R}_{\mathrm{f}}^{3}\right), \mathbb{R}_{1}^{3}, \mathbb{R}_{2}^{3}, \ldots, \mathbb{R}_{N_{\mathrm{p}}}^{3}$, with $\mathbb{R}_{\mathrm{f}}^{3}$ the subspace of the fluid phase, $\mathbb{R}_{\mathrm{i}}^{3}$ the subspace of solid phase-i, and $N_{\mathrm{p}}$ the number of solid phases. The value of the phase-mask equals unity in the domain where the phase is defined, $\mathbb{R}_{\mathrm{p}}^{3}$, equals zero outside the domain of the phase, and is arbitrary at the interface, $\Sigma_{\mathrm{p}}$, usually set to $1 / 2$.

To extend the validity of the governing equations, one starts by extending the definition of the dependent variables, $\mathbf{q}_{\mathrm{p}}(\xi, t)$, from the domain occupied by phase-p, $\forall \xi \in \mathbb{R}_{\mathrm{p}}^{3}$, to the entire space, $\forall \xi \in \mathbb{R}^{3}$. This is achieved by setting

$$
\mathbf{q}^{\mathrm{p}}(\xi, t)=\left[\gamma^{\mathrm{p}}(\xi, t)\right]^{n} \mathbf{q}_{\mathrm{p}}(\xi, t)
$$

The phase-mask can be raised to any power of arbitrary natural number, $n>1$. This generalization is used to extend the validity of the governing equations to $\mathbb{R}^{3}$ (e.g., see the derivation of the momentum in Equation 4a presented below). It does not affect the properties of the time derivative or gradients of the phase-mask function, since derivatives of discontinuous functions are defined in the integral sense.

The governing equations for the extended dependent variables, $\mathbf{q}^{\mathrm{p}}$, are derived by multiplying the governing equations and their boundary conditions in each phase by $\left(\gamma^{\mathrm{p}}\right)^{n}$, using

differentiation by part and properties of the phase-mask. This will yield the extended governing equations derived by Sirovich $(1967,1968)$ that are the basis of the IBM (Peskin 1972, Goldstein et al. 2005, Mittal \& Iaccarino 2005).

As an example of extending a governing equation from $\mathbb{R}_{\mathrm{f}}^{3}$ to $\mathbb{R}^{3}$, consider the momentum equations for compressible flow in the fluid phase, $\mathrm{f}$, with a moving boundary,

$$
\left(\rho_{\mathrm{f}} \mathbf{u}_{\mathrm{f}}\right)_{t}+\nabla_{\mathfrak{\varepsilon}_{\mathrm{f}}} \cdot\left(\rho_{\mathrm{f}} \mathbf{u}_{\mathrm{f}} \otimes \mathbf{u}_{\mathrm{f}}\right)=\nabla_{\mathfrak{E}_{\mathfrak{f}}} \cdot\left(-p_{\mathrm{f}} \underline{I}+\underline{\tau}_{\mathrm{f}}\right) \quad \forall \varepsilon_{\mathrm{f}} \in \mathbb{R}_{\mathrm{f}}^{3}
$$

and

$$
\mathbf{u}_{\mathrm{f}}\left(\xi^{\Sigma_{f}}\right)=\mathbf{w}
$$

where $\mathbf{w}$ is the velocity of the wall as shown in Figure 2. Multiplying the above equation by the phase-mask of the fluid phase, $\left(\gamma^{f}\right)^{3}$, and then using differentiation by parts and properties of the gradients of the phase-mask function and rearranging the terms, we get

$$
\left(\rho^{\mathrm{f}} \mathbf{u}^{\mathrm{f}}\right)_{, t}+\nabla_{\mathcal{E}} \cdot\left(\rho^{\mathrm{f}} \mathbf{u}^{\mathrm{f}} \otimes \mathbf{u}^{\mathrm{f}}\right)=\nabla_{\underline{E}} \cdot\left(-p^{\mathrm{f}} \underline{\mathrm{I}}+\underline{\boldsymbol{\tau}}^{\mathrm{f}}\right)+\mathbf{F}^{\Sigma_{\mathrm{f}}}
$$

and

$$
\mathbf{F}^{\Sigma_{\mathrm{f}}}=\left(\rho_{\mathrm{f}} \mathbf{u}_{\mathrm{f}} \otimes \mathbf{w}-\rho_{\mathrm{f}} \mathbf{u}_{\mathrm{f}} \otimes \mathbf{u}_{\mathrm{f}}-p_{\mathrm{f}} \underline{I}+\underline{\boldsymbol{\tau}}_{\mathrm{f}}\right) \cdot \boldsymbol{n}^{\mathrm{f}} \delta\left(\boldsymbol{\xi}-\xi^{\Sigma_{\mathrm{f}}}\right)
$$

The use of $n=3$ when multiplying by $\left(\gamma^{\mathrm{f}}\right)^{n}$ enabled all dependent variables in the nonlinear terms to be formally defined in $\mathbb{R}^{3}$. Boundary forces appearing in the governing equations should be interpreted in the integral sense-in essence, this is the basis of the IBM (Peskin 1972, Goldstein et al. 1993).

\title{
3.2. Volume Averaging
}

For dependent variables that vary rapidly in space, VAM defines superficial averaged quantities of interest by averaging the variables over an arbitrary elementary volume (AEV), $\mathcal{V}$ (see Figure 3),

![](https://cdn.mathpix.com/cropped/2024_06_05_23237fc8fa5ea45d3cb7g-1.jpg?height=628&width=919&top_left_y=1297&top_left_x=594

ChatGPT figure/image summary: The image depicts a schematic representation of volumes and surfaces of solid and fluid phases within an arbitrary elementary volume (AEV), which is visualized as a large grey circle labelled with the variable 'V'. This diagram visualizes concepts from a theoretical or computational analysis of multiphase systems, particularly in the context of volume averaging mentioned in the provided text.

Here's what each symbol represents:
- \( \mathbf{x} \): The location of the AEV in the space \( \mathbb{R}^3 \).
- \( \xi \): A position vector within the AEV.
- \( \xi^Γ \): A coordinate vector pointing to a surface within the AEV.
- \( V \): The elementary volume where variables are averaged.
- \( V_p \) (where p is subscript and ranges from 0 to 4 in this diagram): The sub-volumes within the AEV corresponding to different phases or solids; for example, 'fluid phase' might be denoted as \( V_0 \), while different solid phases might be represented by \( V_1, V_2, \ldots \). Each \( V_p \) space is represented by a different colored shape.
- \( Σ_{0/1} \), \( Σ_{1/2} \): Surfaces between phases, indicated by dashed lines. These interfaces separate different volume spaces (phases) within the AEV and are the locations where certain physicochemical processes may occur, such as reactive interfaces in porous media or multiphase flow systems.

The inset on the right side of the image zooms in to show the interface between two phases with a surface reaction represented by a zigzag line, highlighting the width \( W \) and a possible boundary layer of thickness \( \delta \) (where \( \delta \) is a function of \( 0/1 \), indicating the dependence of thickness on the two phases in contact).

The diagram aids in visualizing how these concepts are spatially related and helps in the understanding of the mathematical definitions and equations presented in the context of the paper on volume averaging or in studies of porous media and multiphase systems.)

Figure 3

Definitions of volumes and surfaces of solid and fluid phases in an averaging volume, $\mathcal{V}$, at a location $\mathbf{x}$ in $\mathbb{R}^{3}$. The defined volume space of a phase within $\mathcal{V}$ is denoted by $\mathcal{V}_{\mathrm{p}}$; the surface between phase-p and its

![](https://cdn.mathpix.com/cropped/2024_06_05_23237fc8fa5ea45d3cb7g-1.jpg?height=37&width=1258&top_left_y=2049&top_left_x=415

ChatGPT figure/image summary: The image shared here is displaying a set of mathematical expressions and diagrams related to the text provided. From the context, it seems that the image would contain graphs or illustrations of phase-mask functions, γₚ, possibly graphs showing their values across different domains representing different phases, and maybe even their gradients or time derivatives. These would be related to the mathematical definitions given in the text for the phase-mask functions used in modeling multiphase systems, where phases could include solid, liquid, and gaseous states.

The diagrams could illustrate how the phase-mask value is 1 within the domain of a particular phase, 1/2 at the boundary between phases, and 0 outside the domain. Unfortunately, without seeing the specific image, I can't describe its exact content, but it likely includes visual representations of these concepts to aid in understanding the mathematical definitions and operations explained in the paper.)
$(\cdot)$ is $\boldsymbol{n}^{\mathrm{p} /(\cdot)} . \Delta$ is the weight function compact support width.

$$
\overline{\mathbf{q}^{\mathrm{p}}}(\mathbf{x})=\frac{1}{\mathcal{V}} \int_{\mathcal{V}_{\mathrm{p}}(\mathbf{x})} \mathbf{q}_{\mathrm{p}}(\mathbf{x}+\boldsymbol{\eta}) \mathrm{d} \boldsymbol{\eta}=\frac{1}{\mathcal{V}} \int_{\mathbb{R}^{3}} \gamma^{\mathrm{p}} \mathbf{q}_{\mathrm{p}}(\mathbf{x}+\boldsymbol{\eta}) \mathrm{d} \boldsymbol{\eta}
$$

For locally homogeneous systems, the AEV is set large enough to become a representative elementary volume (REV) where variables are smooth, but with $\mathcal{V}$ small compared to large inhomogeneities in the system. The formulation can be made equivalent to filtering by introducing an even weight function, $G(\xi-\mathbf{x})=G(\mathbf{x}-\xi)$, with compact support, $G\left(\xi^{\Gamma}-\mathbf{x}\right)=0 \quad \forall \xi^{\Gamma} \in \Gamma_{\mathcal{V}}$, and outside the AEV (Bachmat \& Bear 1986). The top-hat filter,

$$
\widehat{G}(\xi-\mathbf{x})=\frac{G(\xi-\mathbf{x})}{\mathcal{V}}= \begin{cases}1 / \mathcal{V} & \forall|\xi-\mathbf{x}|<\Delta / 2 \\ 0 & \forall|\xi-\mathbf{x}| \geq \Delta / 2\end{cases}
$$

is used in most studies of porous media (Bear 1988, Whitaker 1999, Valdés-Parada \& Lasseux 2021). Multiplying the integrand in Equation 5 by $G(\boldsymbol{\eta})$ and then changing the integration variable to $\xi=\eta+\mathbf{x}$, the volume average of a dependent variable, $\overline{\mathbf{q}^{p}}$, is rewritten as

$$
\overline{\mathbf{q}^{\mathrm{p}}}(\mathbf{x})=\int_{\mathbb{R}^{3}} \mathbf{q}^{\mathrm{p}}(\xi) \widehat{G}(\xi-\mathbf{x}) \mathrm{d} \xi=\int_{\mathbb{R}^{3}} \mathbf{q}^{\mathrm{p}}(\xi) \widehat{G}(\mathbf{x}-\xi) \mathrm{d} \xi=\left[\left(\gamma^{\mathrm{p}} \mathbf{q}_{\mathrm{p}}\right) \star \widehat{G}\right]
$$

The compact support property of $\widehat{G}$ was used to extend the range to the entire space, $\mathbb{R}^{3}$; the even function property of $\widehat{G}$ was used to turn the integral into a convolution integral without changing the direction of integration. The function $\widehat{G}$ is replaced with a weight function, which Marle (1982) attributes to Matheron (1965) in the porous media literature, while the LES formulation uses a filter function whose width is chosen to capture the large turbulence scales, attributed to Leonard (1975) in the turbulence literature.

In addition to dependent variables defined in the domain, surface species on reactive surfaces are defined on the surface per unit surface area they occupy. Volume averaging of these variables turns them into superficial average quantities (i.e., per unit averaging volume),

$$
\overline{\mathbf{q}^{\Sigma_{\mathrm{p}}}}(\mathbf{x})=\left[\mathbf{q}_{\mathrm{p}}(\xi) \delta\left(\xi^{\Sigma}-\xi\right) \star \widehat{G}\right]=\oint_{\Sigma_{\mathrm{p}}} \mathbf{q}_{\mathrm{p}}\left(\xi^{\Sigma}\right) \widehat{G}\left(\mathbf{x}-\xi^{\Sigma}\right) \mathrm{d} \xi^{\Sigma}
$$

where $\xi^{\Sigma} \in \Sigma_{\mathrm{p}}$ is the coordinate vector of the interface of phase-p with other phases.

Finally, volume-averaged variables are variables per unit of the averaging volume. Volumeaveraged variables in porous media are termed superficial averaged variables. To illustrate the naming, consider the density of a fluid, $\rho^{\ddagger}$, which is defined per differential volume occupied by the fluid. The volume-averaged density, $\bar{\rho}$, is per volume of the AEV. In other words, it is no longer per volume occupied by the fluid. The intrinsic average of a quantity, $\mathbf{q}^{\mathrm{p}}$, occupying phase-p is defined as

$$
\left\langle\mathbf{q}^{\mathrm{p}}\right\rangle(\mathbf{x})=\frac{1}{\epsilon_{\mathrm{p}}(\mathbf{x})}\left[\left(\gamma^{\mathrm{p}} \mathbf{q}_{\mathrm{p}}\right) \star \widehat{G}\right]=\frac{1}{\epsilon_{\mathrm{p}}(\mathbf{x})} \overline{\mathbf{q}^{\mathrm{p}}}(\mathbf{x})
$$

where

$$
\epsilon_{\mathrm{p}}(\mathbf{x})=\overline{\gamma^{\mathrm{p}}}(\mathbf{x})
$$

is the volume fraction of phase-p within the volume of the AEV. Note that the intrinsic average of a constant, $C$, is the constant, $C$. It is the volume fraction of the volume occupied by phase-p within the AEV for a top-hat filter. Intrinsic averaged variables are the physically meaningful dependent variables. The angle brackets are therefore the default symbols that we use for intrinsic averaging.

Similarly, the superficial average of surface variables (e.g., the force term in Equation 4b) should be turned into intrinsic variables by normalizing the superficial average with the effective specific surface (surface area of phase-p within the $\mathrm{AEV}$ per volume of the $\mathrm{AEV}$ ),

$$
\left\langle\mathbf{q}^{\Sigma_{\mathrm{p}}}\right\rangle(\mathbf{x})=\frac{1}{\sigma_{\mathrm{p}}(\mathbf{x})} \overline{\mathbf{q}^{\Sigma_{\mathrm{p}}}}(\mathbf{x})
$$


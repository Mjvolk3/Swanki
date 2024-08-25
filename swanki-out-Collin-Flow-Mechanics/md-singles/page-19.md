(Schrooyen 2015, Schrooyen et al. 2016, Weng \& Martin 2017). They demonstrate progress in porous plug flow-tube experiments (Panerai et al. 2014, 2019) designed to simulate fiber thinning during oxidation. Many challenges remain that need to be solved to mature the closure models and numerical solution methods of the volume-averaged governing equations. These include developing mesoscale models that reflect fiber pitting, melt flows, and robust numerical methods that handle all-Mach-number flows.

\title{
5.3. Macroscale Formulations
}

The current state of the art in planning space exploration missions or verifying and validating TPS design is to treat the environment and the material response as separate homogeneous regions that are coupled through boundary conditions. While velocity slip interface boundary conditions were developed for the momentum equations in the late 1960s (Beavers \& Joseph 1967, Saffman 1971) (see Figure 5b) and later refined by Ochoa-Tapia \& Whitaker (1995) (see Figure 5c), they have not been adopted by the ablation community. Proper interface boundary conditions for mass, momentum, and energy must satisfy balance equations between the two environments in order to tightly couple the two regions (Milos \& Rasky 1994, Martin et al. 2017). Coupling finite-rate chemistry plays an important role in interpreting arc jet data (Driver \& MacLean 2011). Recent trends lean toward coupling the hypersonic flow solver and the ablative material solver using finite-rate chemistry.

Uncoupled/loosely coupled modeling remains the most widely used approach. Modern variations build on work developed by the Aerotherm Corporation in the late 1960s. The computational capabilities at that time were limited to solving the boundary layer equations [Boundary Layer Implicit (BLIMP) code; Bartlett et al. 1968] for the fluids and a 1D material response code [Charring Material Thermal Response and Ablation Program (CMA); Moyer \& Rindal 1968] for the material thermal response. Current efforts use modern computational fluid dynamics (CFD) numerical methods and refined chemistry models for planetary entry environments (Gnoffo et al. 1989, Wright et al. 1998, Kirk 2007, Candler 2019). On the material response side, the adoption of porous ablative TPS materials for Mars exploration and future missions to the Moon and beyond renewed interest in 3D capabilities for the material response (Chen \& Milos 2005, Amar et al. 2011, Lachaud \& Mansour 2014, Weng \& Martin 2014, Lachaud et al. 2015, Weng et al. 2015, Meurisse et al. 2018, Yang et al. 2018). However, the current state of practice for coupling through an interface still relies on the work developed in the 1960s, where the CFD code simulates the environment and provides mass/species transfer and energy transfer from the environment to the wall is estimated through the use of Stanton numbers for mass \(\left(C_{M}\right)\) and heat \(\left(C_{H}\right)\) transfer and the values at the boundary layer edge for species and temperature. The current approach derives the coefficients from detailed CFD solution (Saunders \& Prabhu 2018). This effectively provides the correct heat transfer at the wall. The assumption of Lewis and Prandtl numbers of the same order provides an approximate species flux value at the wall. Using the same flux transfer coefficient for the species enables the use of \(\mathrm{B}^{\prime}\) tables to estimate the surface recession, assuming equilibrium chemistry (Milos \& Chen 1997, Scoggins et al. 2020). The equilibrium assumption is a conservative estimate for wall recession and therefore it enables bounding risk analysis of atmospheric entry missions.

\section*{6. EXPLORING MARS: LESSONS LEARNED AND THE NEXT DECADE}

The heatshield of the MSL capsule that landed on Mars in 2012 was instrumented with thermocouples, recession sensors, and pressure sensors (Gazarik et al. 2008). These instruments provided for the first time detailed in-flight data during atmospheric entry. A similar suite of sensors was
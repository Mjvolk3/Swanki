![](https://cdn.mathpix.com/cropped/2024_06_05_4b8c4a7049080e7b018eg-1.jpg?height=901&width=1602&top_left_y=119&top_left_x=93)

Figure 6

Coupling the flow to a porous wall: (a) uncoupled, (b) slip velocity, (c) jump in shear stress, and (d) fully coupled. $y_{\mathrm{e}}, h_{\mathrm{e}}$, and $p_{\mathrm{e}}$ are the boundary layer edge species mass fractions, specific enthalpy, and pressure, respectively. Abbreviations: BL, boundary layer; FIAT, fully implicit ablation and thermal; PATO, porous-material analysis toolbox based on OpenFOAM. Figure inspired by concepts presented in Beavers \& Joseph (1967), Ochoa-Tapia \& Whitaker (1995), Chandesris \& Jamet (2006), Weng \& Martin (2014), and Schrooyen (2015).

scale via DNS, (b) mesoscale coupling, and (c) macroscale coupling through interface boundary conditions. A schematic is shown in Figure $6 a$.

\title{
5.1. Direct Numerical Simulations at the Microscale
}

Current research trends in simulating flows over porous media lean toward using fully resolved DNS of turbulent incompressible flows (Breugem \& Boersma 2005, Chandesris et al. 2013, Jin \& Kuznetsov 2017, He et al. 2019, Wood et al. 2020, Valdés-Parada \& Lasseux 2021). These simulations are then used to test and develop closure models for the phase-averaged equations. DNS for compressible flows in regimes of interest to TPS applications have not received similar attention. We anticipate that simulations from the free stream to the interior of porous materials in support of fundamental studies will appear in publications within a few years as high-performance computers become more readily available.

\subsection*{5.2. Mesoscale Formulations}

Volume averaging closure models that resolve the transition between the environment and the ablative material are an active research area. In this approach, the gas phase in the ablator and the environment are treated as a single phase (see Figure 5d) separate from the solid phase. The transition between the environment and the porous ablator fluids is of the order of the filter width. Again, rapid progress is seen in mesoscale simulations of incompressible flows over porous materials (Breugem \& Boersma 2002, 2005; Valdés-Parada \& Lasseux 2021). Efforts to formulate mesoscale simulation models for ablative TPS are at the early stage of development
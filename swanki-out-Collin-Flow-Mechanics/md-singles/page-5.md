begins at approximately \(400 \mathrm{~K}\) and is heat rate dependent (Stokes 1995; Bessire \& Minton 2017; Torres-Herrador et al. 2019, 2020). In turn, heating rates are mission dependent, evolve during flight, and are a function of depth within the material. They range from a few to hundreds of kelvins per second. Pyrolysis generates a pressure-driven flow and thermochemical transport through the porous medium of gases that include water vapor, permanent gases, hydrocarbons, and aromatics. It also leads to a progressive change in material density and porosity at the pore scale of the matrix (transitioning from nanometer to micrometer scale), both contributing to modify the effective transport properties of the porous material. Pyrolysis products transported through the fibers and the matrix by advection and diffusion undergo homogeneous chemical reactions and heterogeneous reactions with the solid phases. Coking effects may occur at temperatures between 1,100 and \(1,400 \mathrm{~K}\), when hydrocarbons interact with the char and deposit solid carbon, releasing hydrogen. The thermochemistry of pyrolysis is further discussed in Section 3.4. Heterogeneous pyrolysis gases-solid phase interactions remain an active field of research.

Because of the large temperature range, a distinct feature of the ablative system is that mass and momentum transport of gases spans regimes from continuum to rarefied. The mean free path of the gas mixture that increases with temperature and decreases with pressure can be of the same order of the pore scales at certain flight conditions. During entry, while the flow is mostly in the continuum regime at the scale of the hypersonic body, Knudsen numbers within the porous ablator are in the transitional \((0.1 \lesssim \mathrm{Kn} \lesssim 100)\) or slip \((0.02 \lesssim \mathrm{Kn} \lesssim 0.1)\) regime (Lachaud et al. 2010) and transport is substantially affected by wall collisions. Close to the surface, a transition occurs at high temperature from the continuum regime in the boundary layer to the noncontinuum regime within the porous material. While the phase-averaged models described in Section 3.4 are based on the assumption of continuum flow, the Boltzmann equation is often a more accurate model for dilute gas dynamics. This observation has motivated the use of particle-based simulations, such as the direct simulation Monte Carlo (DSMC) method, to determine Knudsen corrections to the momentum equation, for example, by introducing a pressure-dependent Klinkenberg term in Darcy's model for the permeability of porous ablators (Marschall \& Milos 1998, Panerai et al. 2016, Borner et al. 2017).

At temperatures above \(1,200 \mathrm{~K}\), pyrolysis is complete and the remaining carbonaceous char layer interacts with both the pyrolysis gases and the reactants transported to the surface. This ablation zone is dominated by finite-rate heterogeneous reactions, such as oxidation and nitridation, phase changes (e.g., sublimation of solid carbon into gas carbon species), and mechanical material removal by friction and shear stresses (spallation) (Bailey et al. 2018, Price et al. 2022). The extent of the ablation zone is the result of competing diffusion-reaction processes. Diffusive transport within porous ablators is often modeled using Fickian diffusion. Fick's law can be derived from the Boltzmann equation and keeps the same form at all regimes, from the continuum to the rarefied. The effective diffusion coefficient uses a tortuosity factor \(\eta\) to correct the reference diffusivity for species transport (cf. Section 3.5).

Effects of hydrodynamic dispersion on diffusive transport can be neglected both in the continuum regime, because of the small Péclet number for the mass transfer (owing to the small pore scales), and in the rarefied regime, because of the limited gas phase collisions. Reactions of the solid phases with radicals from the boundary layer are temperature-dependent processes, widely modeled as a set of Arrhenius rate equations. Several efforts have been dedicated to developing new models for carbon-oxygen systems based on modern experiments (Candler 2019). Competing diffusion-reaction processes are described by the Thiele number. In oxygen-rich environments, low Thiele numbers \((\Phi \rightarrow 0)\) pertain to a reaction-limited regime, in which oxygen can penetrate the porous medium, producing a large ablation zone (of hundreds of microns in depth) with a graded in-depth porosity. Porosity gradients, in turn, affect all effective transport processes. This
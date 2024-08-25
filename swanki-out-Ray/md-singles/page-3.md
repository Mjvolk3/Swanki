dependence of thermal performance on pore size distribution, hydrophobicity change, and the role of contaminant fouling during continuous SWME operation is examined as part of a failure mode analysis. The specific objectives are: (i) developing a comprehensive mathematical model to accurately predict reported experimental thermal performances and estimating membrane structure parameter for SWME, (ii) performing a sensitivity analysis to understand the effect of input process variables on output thermal performance, (iii) understanding the role of contaminants and organic foulants on long-term thermal performance degradation and (iv) evaluating the conditions that can lead to critical failure modes.

\section*{2. Materials and methods}

Pore structure and morphology of the hollow fibers for SWME module (HF-SWME) were examined using a FEI Helios Nanolab 660 Focused Ion Beam/Scanning Electron Microscope (SEM) at the University of Kentucky Electron Microscopy Center (EMC). Samples were prepared for scanning electron microscopy (SEM) imaging by mounting on a \(90^{\circ}\) sample holder (aluminum stub) with double sided carbon tape (Nisshin). For lumen surface views, a small fiber piece was cut axially with scissors to expose the lumen. For cross-sectional views, fibers were cut using a sharp razor blade at room temperature and mounted on a silicon wafer with copper tape for polishing using an argon ion-beam polisher (JEOL cooling cross section polisher IB-19520CCP) with settings of \(4.0 \mathrm{kV}, 5.0 \mathrm{Ar}\) gas flow setting at \(-120^{\circ} \mathrm{C}\) with \(40 \mathrm{~s} / 20 \mathrm{~s}\) (on/off) for \(8 \mathrm{~h}\) and stage swing enabled) [25]. The polished samples were mounted on a \(90^{\circ}\) sample holder (aluminum stub) and sputter coated with \(5 \mathrm{~nm}\) Pt layer (using a Leica EM ACE600 instrument) prior to SEM imaging. Surface characterization of the hollow fibers was performed using \(\mathrm{N}_{2}\) sorption experiments conducted at \(77 \mathrm{~K}\) with a Micromeritics TriStar 3000 instrument. Specific surface area was determined using the Brunauer-Emmett-Teller (BET) isotherm method and pore volume, average pore size and pore size distribution were calculated using the method of Barrett, Joyner and Halenda (BJH).

\section*{3. Model development}

The model equations were developed assuming all fibers are identical and fluid distribution into the fibers from the distribution manifolds is uniform. Fig. 1 illustrates a single representative fiber and the operational variables: inlet water flow rate, \(\dot{m}_{i n}\); inlet water temperature, \(T_{i n}\); and the driving force for water vapor transport from lumen to shell side, \(\Delta P=P_{\text {vapor }}-P_{\text {shell }}\), where \(P_{\text {vapor }}\) is the water vapor pressure at the water temperature adjacent to the membrane and \(P_{\text {shell }}\) is the shell side pressure. Fig. 1 also illustrates the SWME module and the backpressure valve on the case used to control pressure in the shell-side space outside the fiber; the valve opens to reduce shell-side pressure if the target outlet water temperature is too high. Detailed model development from mass and energy balances for a control volume surrounding a differential fiber length (see Fig. 1) is provided in the Supplementary Information.

\subsection*{3.1. Overall model to predict SWME performance}

The variation of water flow rate in the lumen is given by:

\(\frac{d \dot{m}}{d \xi}=-J_{k} \pi d_{l} L\)

where, \(\dot{m}\) is the water mass flow rate \((\mathrm{kg} / \mathrm{s}), J_{k}\) is the vapor mass flux across the membrane \(\left(\mathrm{kg} / \mathrm{m}^{2} / \mathrm{s}\right), d_{l}\) is the lumen diameter, L is total fiber length, and \(\xi\) is the normalized dimensionless length. Note that the vapor flux depends on temperature and thus is a function of axial position. The initial condition for Eq. (1a) is:

\(\dot{m}=\dot{m}_{i n}\) at \(\xi=0\) where \(\dot{m}_{i n}\) is the inlet mass flow rate per fiber.

Similarly, the variation of water temperature in the lumen is given by Eq. (2a) (see Supplementary Information for detail):

\(\frac{d T}{d \xi}=\frac{-\lambda_{v}}{\dot{m} C_{p}}\left(J_{k} \pi d_{l} L\right)\)

where, \(C_{p}\) is the specific heat capacity of water (Joules \(/ \mathrm{kg} / \mathrm{K}\) ), a function of temperature and \(\lambda_{v}\) is the water latent heat of vaporization (Joules/ \(\mathrm{kg}\) ), also a function of temperature. Initial condition for Eq. (2a) is:

\(T=T_{\text {in }}\) at \(\xi=0\)

where \(T_{\text {in }}\) is the inlet temperature.

Since water vapor fluxes are small compared to the lumen flow rate, the lumen pressure drop is calculated from the differential Hagen-Poiseuille Equation:

\(\frac{d P_{\text {lumen }}}{d \xi}=-\frac{128 \mu \dot{m} L}{\pi \rho d_{l}^{4}}\)

where, \(\mu\) is the dynamic viscosity of water (Pa.s) and \(\rho\) is the density \((\mathrm{kg} /\) \(\mathrm{m}^{3}\) ). Note both are functions of lumen temperature. The initial condition for Eq. (3a) is:

\(P_{\text {lumen }}=\left(P_{\text {lumen }}\right)_{\text {in }}\) at \(\xi=0\)

where \(\left(P_{\text {lumen }}\right)_{\text {in }}\) is the inlet lumen water pressure.

The equation for convective heat transfer in lumen side boundary layer can be expressed as:

\(h_{c}\left(T-T_{p}\right)=-\lambda_{v} J_{k}\)

where, \(h_{c}\) is the convective heat transfer coefficient \(\left(\mathrm{W} / \mathrm{m}^{2} / \mathrm{K}\right)\) and \(T_{p}\) is the pore mouth temperature \((\mathrm{K})\), a function of position along the fiber (can be assumed equal to \(T_{m}\), liquid-vapor interface temperature when the interface is at the pore mouth).

The convective heat transfer coefficient is estimated from the Nusselt correlation for laminar flow in tubes. In the entry mass transfer limit, \(N u=\frac{h_{c} d_{l}}{\kappa_{w}}=1.86\left(\frac{R e P r d_{l}}{L}\right)^{0.33}\), where \(R e=\frac{v_{w} d_{l \rho}}{\mu}\) is the Reynolds number and \(\operatorname{Pr}=\frac{C_{p} \mu}{\kappa_{w}}\) is the Prandtl number. The thermal entry length is \(1 / 100\) th of the fiber length in the absence of evaporation and the flow in the lumen can be considered fully developed laminar flow. For fully developed laminar flow in the well-developed heat transfer limit, \(N u=4.36\). Since the shell is under high vacuum, heat conduction in the shell is negligible in VMD [15]. While the fluid thermal boundary layer is indeed included in the heat transfer calculations, the effect is small. The difference between the bulk and inner surface temperature is less than \(1^{\circ} \mathrm{C}\) for the results presented here. Also note that in our supplement we do discuss (Eq S7 and S8, and Eq (4) above)) and account for pore temp being not same as bulk lumen side water.

The calculation of water vapor flux through the pores is critical to modeling SWME performance. The flux should be calculated using either Knudsen diffusion or molecular diffusion based on the Knudsen number, \(K_{n}=\frac{l}{d_{p}}\), where \(l\) is the mean free path and \(d_{p}\) is the mean pore diameter.

The mean free path can be calculated from [27]:

\(l=\frac{k_{B} T_{p}}{\sqrt{2} \pi P \sigma^{2}}\)

where, \(k_{B}\) is the Boltzmann constant \(\left(k_{B}=1.381 \times 10^{-23} \mathrm{~J} / \mathrm{K}\right), T_{p}\) is the pore temperature, \(P\) is the mean pore pressure at pore opening ( \(P=\) \(\left.P_{\text {vapor }}\right)[28]\), and \(\sigma\) is the collision diameter ( \(2.641 \times 10^{-10} \mathrm{~m}\) for water).

When water permeation occurs by Knudsen diffusion, the water flux is given by:
$\mathrm{J}_{\mathrm{k}}=(0.0248) S_{P} \sqrt{\frac{1}{T_{p}}}(\Delta P)$

where $S_{p}$ is the overall membrane structure parameter $\left(S_{P}=\frac{d_{p} \varphi_{p}}{\delta \tau}\right), d_{p}$ is the mean pore diameter, $\varphi_{\mathrm{p}}$ is membrane porosity, $\delta$ is membrane thickness, and $\tau$ is membrane tortuosity.

Differential equations (1)-(3) are solved in MATLAB $\circledR^{\circ}$ using an adaptive Runge-Kutta method ("ode45 solver"). Values for the temperature dependent material properties are provided in the Supplemental Information (Table S1). Ranges of operational variables ( $\dot{m}_{\text {in }}, T_{i n}$, $\left(P_{\text {lumen }}\right)_{\text {in }}$ and $\left.P_{\text {shell }}\right)$ and membrane parameters used in the simulations are provided in Table S2 in the Supplementary information.

Model outputs are temperature and mass flow rate as a function of position. These are used to calculate heat rejection, total mass of water vaporized and lumen side pressure drop from Eqs. (7)-(9), respectively:

Heat rejection, $q=\int_{0}^{L} \lambda_{v} \dot{m}_{v} d z$

Total mass of water vaporized, $\left(\dot{m}_{v}\right)_{\text {tot }}=\dot{m}_{\text {in }}-\dot{m}_{\text {out }}$

Pressure drop across lumen side, $\Delta P_{\text {lumen }}=\left(P_{\text {lumen }}\right)_{\text {in }}-\left(P_{\text {lumen }}\right)_{\text {out }}$

In Eq. (7), $\lambda_{v}$ and $\dot{m}_{v}$ are temperature dependent and therefore vary with position.

For certain cases (low inlet water temperature, $<10^{\circ} \mathrm{C}$ ), one can convert the above equations into an algebraic form by considering the average properties of water at $T_{\text {avg }}=\left(T_{\text {in }}+T_{\text {out }}\right) / 2$. The result is given by (see Supporting Information for derivation):

$\left(h_{c}\right)_{\text {avg }}\left(T_{\text {in }}-\frac{\left(\lambda_{v}\right)_{\text {avg }}}{2\left(C_{p}\right)_{\text {avg }}} \ln \left(\frac{\dot{m}_{\text {in }}}{\dot{m}_{\text {in }}-\left(J_{k}\right)_{\text {avg }} \pi d_{l} L}\right)-\left(T_{p}\right)_{\text {avg }}\right)=+\left(\lambda_{v}\right)_{\text {avg }}\left(J_{k}\right)_{\text {avg }}$

where, $\left(J_{k}\right)_{\text {avg }},\left(\lambda_{v}\right)_{\text {avg }},\left(C_{p}\right)_{\text {avg }}$ and $\left(h_{c}\right)_{\text {avg }}$ are the vapor mass flux, latent heat of vaporization, water heat capacity, and convective heat transport coefficient evaluated at the average pore temperature $\left(T_{p}\right)_{\text {avg }}$. Eq. (10) is solved along with Eq. (6) to find $\left(T_{p}\right)_{\text {avg }}$. The value is used to calculate $\dot{m}_{\text {out }}$ and $T_{\text {out }}$ (see Supporting Information). Finally, heat rejection, mass of water vaporized, and lumen side pressure drop are calculated using Eqs. (7), (8) and (11) respectively.

$\Delta P_{\text {lumen }}=\frac{128 \mu_{\text {avg }} L(\dot{m})_{\text {avg }}}{\pi \rho_{\text {avg }} d_{l}^{4}}$

where, $\mu_{\text {avg }}$ and $\rho_{\text {avg }}$ are the viscosity and density of water evaluated at $T_{\text {avg }}$ and $(\dot{m})_{\text {avg }}=\frac{\dot{m}_{\text {in }}+\dot{m}_{\text {out }}}{2}$ is the average mass flow rate of water.

\subsection*{3.2. Liquid entry into the pores}

Liquid entry into the pores is analyzed by Laplace equation as shown in Eq. (11), which relates liquid entry pressure (LEP) to membrane and liquid properties.

$L E P=-\frac{4 B_{g} \gamma_{L} \cos \theta_{o}}{d_{P}}$

where, $\gamma_{L}$ and $\theta_{o}$ are the surface tension of the liquid and initial contact angle of the liquid with polymeric membrane, respectively, and $B_{g}$ is the geometric factor ( $B_{g}=1$, for cylindrical pores). Now if a portion of the pore in contact with liquid (lumen side) gets hydrophilized enough due to fouling such that the lumen side pressure is greater than LEP, liquid will enter the pores up to the end of hydrophilized portion (Fig. S1 in Supplementary information). For a single pore with partial liquid entry up to the length of $\delta_{\mathrm{L}}$, if the vapor traveling path length is $\delta_{\mathrm{V}}$, the water vapor flux in that case is given by:

$\left(J_{k}\right)_{v a p}=(0.0248) \frac{\delta}{\delta_{V}} S_{P} \sqrt{\frac{1}{T_{s}}}(\Delta P)$

where $T_{s}$ is the vapor liquid interface temperature. In the absence of liquid entry, $T_{s}$ is assumed to be equal to $T_{p}$ as discussed previously. However, in the case of partial liquid entry $T_{s} \neq T_{p}$ and $P_{\text {vapor }}$ in Eq. (12) is a function of $T_{s}$, which also is unknown.

If water wets the pores, the liquid mass flux can be estimated from the Hagen-Poiseulle equation for flow through the pores [29]:

$\left(J_{k}\right)_{\text {liq }}=\frac{\pi \rho d_{P}^{4}}{128 \mu \delta_{L}}\left(P_{\text {lumen }}-P_{\text {vapor }}+P_{c}\right)$

where, $P_{c}=\frac{4 \gamma_{L} \cos \theta}{d_{P}}$ is the capillary pressure and $\gamma_{L}$ and $\theta$ are the surface tension of the liquid and changed contact angle of the fiber in the portion of the membrane that is wetted, respectively. Physical properties $\mu$ and $\rho$ also are temperature dependent and can be evaluated at an average temperature of $\frac{T_{P}+T_{s}}{2}$.

\section*{4. Results and discussion}

The system of ordinary differential equations (ODEs) that comprise the conservation of mass, momentum, and energy equations for a single SWME fiber (Eqs. (1)-(3)) was solved with MATLAB® ode45 solver along with the equations for convective heat transfer coefficient in the lumen side and diffusion of vapor through the pores to obtain liquid water mass flow rate through the lumen, liquid water temperature, pore temperature and lumen side pressure profiles as a function of axial position. These results are then used to calculate the values of heat rejection, total mass of water loss, temperature drop and lumen side pressure drop that are critical to performance of the spacesuit SWME.

\subsection*{4.1. Hollow fiber characterization}

NASA experimental thermal performance measurements for the HFSWME were used to validate the model and estimate the membrane structural parameter $S_{p}$. Scanning electron microscopic (SEM) images of the lumen side surface, shell side surface and cross section of the HFSWME membranes are shown in Fig. 2. Images show more uniform pore structure in both lumen and shell side with somewhat ellipsoidal pore opening shape, whereas the internal pore structure is more fibrous than spongy (i.e. bounded by polymer strands (not ellipsoidal cavities) as observed in polyvinylidene fluoride or PVDF membranes) as seen in the cross-sectional image [25]. As a result, SWME fibers have less variability in pore size compared to more commonly used PVDF or polyether sulfone (PES) membranes. The lumen-side pore size distribution (major axis, minor axis and circular equivalent diameter, $\sqrt{\text { major axis } * \text { minor axis }}$ is provided in Supplementary Information Fig. S3 based on measurements of 120 random pores from SEM images like the one provided in Fig. 2a. The major axis has wide pore distribution, whereas minor axis (which is more important for the diffusion of water vapor) has narrower pore distribution with some pores skewed towards the $100 \mathrm{~nm}$ size. The equivalent circular diameter (Fig. S3c) shows $\sim 6 \%$ of the pores are larger than $100 \mathrm{~nm}$.

Sorption isotherms and the corresponding BJH pore size distribution obtained from the desorption branch are provided in the Supplementary Information Fig. S4. The isotherms showed capillary condensation with a hysteresis loop consistent with a pore size around $50 \mathrm{~nm}$ [25]. The BJH pore size distribution showed a peak at $34 \mathrm{~nm}$, which is consistent with minor axis pore size distribution of SEM images, with $5 \%$ of pores $>100$ $\mathrm{nm}$ based on the cumulative pore volume. Volumetric porosity calculated from the pore volume of nitrogen sorption are $24-28 \%$ for different experiments, which is much smaller than the $40 \%$ manufacturer reported porosity.
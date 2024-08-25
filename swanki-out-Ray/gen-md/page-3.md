## What type of equipment was used for examining pore structure and morphology of the hollow fibers for the SWME module (HF-SWME)?

The pore structure and morphology of the hollow fibers for SWME module (HF-SWME) were examined using a FEI Helios Nanolab 660 Focused Ion Beam/Scanning Electron Microscope (SEM) at the University of Kentucky Electron Microscopy Center (EMC).

- .materials, .microscopy
- .materials, .hollow-fibers
- .methods, .instrumentation

---

## Describe the method used to calculate specific surface area in the surface characterization of hollow fibers.

The specific surface area was determined using the Brunauer-Emmett-Teller (BET) isotherm method during the $\mathrm{N}_{2}$ sorption experiments conducted at $77 \mathrm{~K}$ with a Micromeritics TriStar 3000 instrument.

- .materials, .surface-characterization
- .methods, .BET-method
- .materials, .hollow-fibers

--- 

## What initial condition is used for the equation describing the variation of water flow rate in the lumen of the HF-SWME module?

The variation of water flow rate in the lumen is given by:

$$\frac{d \dot{m}}{d \xi}=-J_{k} \pi d_{l} L$$

The initial condition is:

$\dot{m}=\dot{m}_{i n}$ at $\xi=0$, where $\dot{m}_{i n}$ is the inlet mass flow rate per fiber.

- .mathematics, .flow-rate
- .model-development, .initial-conditions
- .SWME, .water-flow

---

## What equation is used to describe the variation of water temperature in the lumen, and what is its initial condition?

The variation of water temperature in the lumen is given by:

$$\frac{d T}{d \xi}=\frac{-\lambda_{v}}{\dot{m} C_{p}}\left(J_{k} \pi d_{l} L\right)$$

The initial condition for this equation is:

$T=T_{\text {in }}$ at $\xi=0$, where $T_{\text {in }}$ is the inlet temperature.

- .thermal-performance, .temperature-variation
- .model-development, .initial-conditions
- .SWME, .water-temperature

---

## What is the equation for the differential Hagen-Poiseuille equation used to calculate the lumen pressure drop?

The lumen pressure drop is calculated from the differential Hagen-Poiseuille equation:

$$\frac{d P_{\text {lumen }}}{d \xi}=-\frac{128 \mu \dot{m} L}{\pi \rho d_{l}^{4}}$$

where $\mu$ is the dynamic viscosity of water (Pa.s) and $\rho$ is the density $(\mathrm{kg} / \mathrm{m}^{3})$.

- .fluid-dynamics, .pressure-drop
- .SWME, .lumen-pressure
- .model-development, .Hagen-Poiseuille

---

## How is the mean free path in the Knudsen number calculated?

The mean free path, $l$, in the Knudsen number is calculated using the equation:

$$l=\frac{k_{B} T_{p}}{\sqrt{2} \pi P \sigma^{2}}$$

where $k_{B}$ is the Boltzmann constant $\left(k_{B}=1.381 \times 10^{-23} \mathrm{~J} / \mathrm{K}\right)$, $T_{p}$ is the pore temperature, $P$ is the mean pore pressure at the pore opening, and $\sigma$ is the collision diameter $\left(2.641 \times 10^{-10} \mathrm{~m}\right)$.

- .diffusion, .Knudsen-number
- .model-development, .mean-free-path
- .SWME, .calculation


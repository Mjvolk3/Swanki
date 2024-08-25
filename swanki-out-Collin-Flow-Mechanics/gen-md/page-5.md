## Explain the impact of pyrolysis on the properties of the porous material within the context of thermal protection systems (TPS).

Pyrolysis leads to changes in material density and porosity at the pore scale, which transitions from nanometer to micrometer scale. This significantly affects the transport properties of the porous material, impacting the effectiveness of TPS.

- #engineering, #material-science.porous-media

## What are the temperature ranges in which coking effects occur during pyrolysis, and what chemical interactions are observed?

Coking effects occur at temperatures between 1,100 and $1,400 \mathrm{~K}$, where hydrocarbons interact with char and deposit solid carbon, releasing hydrogen.

- #chemistry, #thermal-processes.pyrolysis

## Define the Knudsen number and describe its relevance in the context of momentum transport within ablative systems.

The Knudsen number (\mathrm{Kn}) is defined as the ratio of the mean free path of gas molecules to a characteristic physical length scale, which, in this case, is the pore scale:

$$
\mathrm{Kn} = \frac{\lambda}{L}
$$

In ablative systems, \mathrm{Kn} numbers within the porous ablator range from transitional (0.1 \lesssim \mathrm{Kn} \lesssim 100) to slip (0.02 \lesssim \mathrm{Kn} \lesssim 0.1) regimes, indicating the importance of wall collisions and impacting gas transport behavior.

- #fluid-dynamics, #thermodynamics.knudsen-number

## Discuss how Fick's law applies to diffusive transport in porous ablators and mention the key parameter that modifies the diffusion coefficient.

Fick's law models diffusive transport and maintains the same form across regimes, from continuum to rarefied. The effective diffusion coefficient is modified by a tortuosity factor $\eta$ to account for the complex pathways in the porous structure:

$$
J = -D_{\text{eff}} \nabla c \quad \text{where} \quad D_{\text{eff}} = \frac{D_{\text{ref}}}{\eta}
$$

Here, $J$ is the diffusive flux, $D_{\text{ref}}$ is the reference diffusivity, and $c$ is the concentration of the diffusing species.

- #diffusion, #material-science.fick's-law

## Explain the significance of the Thiele number in modeling competing diffusion-reaction processes within porous ablators.

The Thiele number (\Phi) is a dimensionless number that characterizes the ratio of the reaction rate to the diffusion rate. In oxygen-rich environments, low Thiele numbers $(\Phi \rightarrow 0)$ indicate a reaction-limited regime, leading to a larger ablation zone with graded in-depth porosity:

$$
\Phi = \left(\frac{R}{D}\right)^{1/2}
$$

where $R$ is the reaction rate and $D$ is the diffusivity.

- #reaction-engineering, #diffusion.thiele-number

## What is the role of hydrodynamic dispersion in diffusive transport within porous ablators, and why can it be neglected?

Hydrodynamic dispersion effects on diffusive transport can be neglected due to the small Péclet number for mass transfer in the continuum regime and limited gas phase collisions in the rarefied regime:

$$
\text{Péclet number} \quad \text{Pe} = \frac{uL}{D}
$$

In this context, $u$ is the fluid velocity, $L$ is the characteristic length, and $D$ is the diffusivity. Given the small pore scales, $\mathrm{Pe}$ is small, making hydrodynamic dispersion negligible.

- #transport-phenomena, #fluid-dynamics.peclet-number
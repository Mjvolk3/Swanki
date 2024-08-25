### Card 1

## Describe the apparent drag term in momentum equations within porous media.

The apparent drag term in the momentum equation within porous media can be described by splitting the wall pressure into a volume-averaged pressure and a fluctuation pressure, denoted as:

$$\left.p_{\mathrm{f}}\right|^{\Sigma_{f}}=\left\langle p^{\uparrow}\right\rangle+\tilde{p}$$

The surface integral is then modeled to be proportional to the velocity:

$$\left\langle(-\tilde{p} \boldsymbol{I}+\boldsymbol{\tau}) \cdot \boldsymbol{n}^{\mathrm{g}}\right\rangle=-\epsilon_{\mathrm{g}}^{2} \mu \underline{\mathbf{K}}^{-1} \cdot\langle\mathbf{u}\rangle$$

Here, $\underline{\mathbf{K}}$ is the Darcy coefficient, $\epsilon_{\mathrm{g}}$ is porosity, $\mu$ is the dynamic viscosity, and $\langle\mathbf{u}\rangle$ is the volume-averaged velocity.

- #fluid-dynamics, #porous-media, #momentum-equation

### Card 2

## What is the Klinkenberg correction to Darcy's coefficient and why is it used?

The Klinkenberg correction to Darcy's coefficient is used to account for noncontinuum flow effects. It is expressed as:

$$\underline{\mathbf{K}}=\underline{\mathbf{K}}_{0} \cdot(\underline{\mathbf{I}}+\underline{\mathbf{b}} / p)$$

Where $\underline{\mathbf{K}}_{0}$ is the continuum flow permeability and $\underline{\mathbf{b}}$ is the slip parameter, both dependent on the microstructure of the material.

- #fluid-dynamics, #porous-media, #noncontinuum-flow

### Card 3

## Derive the surface heat transfer integral sum from the averaged energy equations.

The sum of the averaged energy equations and using the interface boundary conditions leads to surface heat transfer integrals that sum to zero:

$$\frac{\partial\left\langle E_{t}\right\rangle}{\partial t}+\nabla \cdot\left(\epsilon_{\mathrm{g}}\langle\rho\rangle_{\mathrm{g}}\langle b\rangle_{\mathrm{g}}\langle\mathbf{u}\rangle_{\mathrm{g}}\right)+\nabla \cdot \sum_{k=1}^{N_{\mathrm{g}}}\langle\mathcal{Q}\rangle_{k}=-\nabla \cdot\left(\langle\mathbf{Q}\rangle+\left\langle\mathbf{Q}^{\mathrm{rad}}\right\rangle\right)$$

- #energy-equations, #surface-heat-transfer, #porous-media

### Card 4

## Why is a two-temperature formulation necessary for certain composites like glass-filled polymer composites?

A two-temperature formulation is necessary for composites such as glass-filled polymer composites where significant convective heat transfer occurs due to glass melt and reactions with the carbonized polymer. The temperatures for the gas ($T_{\mathrm{g}}$) and the bulk ($T_{\mathrm{b}}$) need to be separately considered because local thermal equilibrium cannot be assumed.

- #thermal-physics, #two-temperature-model, #composite-materials

### Card 5

## Explain how the volume-averaged heat flux is modeled in single-temperature formulations.

In single-temperature formulations, the volume-averaged heat flux is modeled as:

$$\langle\mathbf{Q}\rangle+\left\langle\mathbf{Q}^{\mathrm{rad}}\right\rangle=-\underline{\mathbf{k}}^{\mathrm{eff}} \cdot \nabla\langle T\rangle$$

Here, $\underline{\mathbf{k}}^{\text {eff }}$ is the effective conductivity tensor of the material, which accounts for porous media radiation, gas, and solid conduction.

- #thermal-physics, #heat-flux, #porous-media

### Card 6

## Under what conditions can deviations from the intrinsic average in porous materials be neglected, and which works discuss this?

Deviations from the intrinsic average in porous materials can be neglected when $d_{\text {pore }} \ll \Delta \ll L$, where $L$ represents macroscale changes within the medium. Under these conditions, deviations have short correlation lengths and are negligible regardless of chemical activity (Whitaker 1999, Breugem et al. 2006).

- #porous-media, #mathematical-modeling, #average-deviations
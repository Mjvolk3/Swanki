## What characterizes the late phase of an entry trajectory in terms of temperatures and char reactivity?

During the late phase of an entry trajectory, temperatures are moderate and the char reactivity to oxygen is low. In contrast, high Thiele numbers $(\Phi \rightarrow \infty)$ pertain to a diffusion-limited regime, where all available oxygen reacts near the surface, leading to rapid material recession.

- #materials.sci, #combustion
---

## What happens at near-unit Thiele numbers in the context of an entry trajectory?

At near-unit Thiele numbers, diffusion and reaction processes balance each other, and a reaction zone of the order of the pore scale is produced, as described in the literature (Lachaud et al. 2010; Ferguson et al. 2016, 2017; Vignoles et al. 2018).

$$
\Phi \approx 1
$$

- #materials.sci, #chemical-reactions
---

## Describe the difference in reactivity between the charred matrix and carbon fibers in an entry trajectory scenario.

From the analysis of arc jet experiments, the charred matrix reacts with oxygen faster than the carbon fibers do. This leads to near-surface regions with large pore scales, around the scale of the FiberForm pore scale, and results in the needling of fibers.

- #materials.sci, #combustion 
---

## What is needed for nonequilibrium conditions in thermal processes for porous ablators?

For nonequilibrium conditions, two-temperature models are needed. Since Péclet numbers are small due to the small pore scale and typical values of velocity and thermal diffusivity in porous ablators, solid and gas phases are often in thermal equilibrium under most conditions.

$$
\text{Péclet number} \rightarrow \mathrm{small}
$$

- #heat-transfer, #materials.sci 
---

## Explain the objective of Volume Averaging Method (VAM) in the context of ablative porous media.

The goal of VAM is to derive governing equations of the dynamics at the macroscale by upscaling microscale equations through volume averaging, making it compatible with modern numerical methods.

- #fluid-mechanics, #materials.sci
---

## How does VAM relate to IBM and LES methods in the study of ablative TPS materials?

VAM connects to IBM by extending the governing equations from valid domains in each phase to the entire space, $\mathbb{R}^3$. The link to LES is made by outlining the relation between VAM's spatial smoothing and LES's filtering approach. The key difference is in how VAM splits dependent variables into averaged and unresolved scales.

$$
\mathbb{R}^3 \leftarrow \mathbb{R}_{\mathrm{p}}^3
$$

- #fluid-mechanics, #numerical-methods
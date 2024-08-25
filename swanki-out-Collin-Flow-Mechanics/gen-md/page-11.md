## Derive the split of dependent variables for multiphase problems as given.

Given that $\mathbf{q}_{\mathrm{p}}$ is defined only in phase-p, dependent variables are split as:

$$
\mathbf{q}_{\mathrm{p}}(\mathbf{x}+\xi)=\gamma^{\mathrm{p}}(\mathbf{x}+\xi)\left\langle\mathbf{q}^{\mathrm{p}}\right\rangle(\mathbf{x})+\mathbf{q}_{\mathrm{p}}^{\prime \prime}(\mathbf{x}+\xi)
$$

Here:
- $\mathbf{q}_{\mathrm{p}}(\mathbf{x}+\xi)$ is the dependent variable in phase-p.
- $\gamma^{\mathrm{p}}(\mathbf{x}+\xi)$ is the phase-p indicator function.
- $\left\langle\mathbf{q}^{\mathrm{p}}\right\rangle(\mathbf{x})$ represents the intrinsic average.
- $\mathbf{q}_{\mathrm{p}}^{\prime \prime}(\mathbf{x}+\xi)$ is the deviation from the intrinsic average.

- #multiphase.flow, #dependent-variables.split, #phase.compute

## What does volume-averaging of the split dependent variables in phase-p yield, and what simplification occurs in practice?

Multiplying Equation 15 by $\gamma^{\mathrm{p}}(\mathbf{x}+\boldsymbol{\xi}) \widehat{G}(\xi)$ and volume averaging yields:

$$
\overline{\mathbf{q}^{\mathrm{p}}}=\epsilon_{\mathrm{p}}\left\langle\mathbf{q}^{\mathrm{p}}\right\rangle=\epsilon_{\mathrm{p}}\left\langle\mathbf{q}^{\mathrm{p}}\right\rangle+\overline{\left(\mathbf{q}^{\mathrm{p}}\right)^{\prime \prime}} \Rightarrow \overline{\left(\mathbf{q}^{\mathrm{p}}\right)^{\prime \prime}}=0
$$

In practice, order-of-magnitude analysis in porous media cases results in simplifications showing that differences between the two splits can be neglected.

- #volume-average, #porous-media.analysis, #dependent-variables.split

## What are the differences between the splits of dependent variables as outlined in the text, and in what applications is this difference significant?

Differences between the two splits outlined can be important in IBM (Immersed Boundary Method) and LES (Large Eddy Simulation) applications, despite them being negligible in porous media cases as per order-of-magnitude analysis (Davit et al. 2013).

- #dependent-variables.split, #IBM.LE.S, #multiphase.flow

## In regions where $\epsilon_{\mathrm{f}}=1$, what do the volume-averaged governing equations correspond to?

In the free-stream region (environment) where $\epsilon_{\mathrm{f}}=1$, the volume-averaged governing equations revert to the LES-averaged equations. 

- #volume-average, #free-stream.region, #LES-averaged.equations

## What function does impregnating ablative composites with resin serve within the porous TPS material?

The purpose of impregnating ablative composites with resin is to achieve endothermic resin decomposition that results in pressure buildup within the material, which resists penetration of free-stream gases.

- #resin.impregnation, #ablative-composites.function, #porous.material.TPS

## Describe the early resin pyrolysis models and the advancement introduced by Goldstein in 1965.

Early resin pyrolysis models used a single kinetic equation of the Arrhenius form to represent decomposition as a function of temperature (Scala \& Gilbert 1962). Goldstein (1965) introduced a two-reaction model, immediately adopted by the community and still in use today.

- #resin-pyrolysis.models, #Arrhenius.equation, #Goldstein.two-reaction.model
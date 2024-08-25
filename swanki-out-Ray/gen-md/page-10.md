### Card 1

## What effect does water intrusion have on thermal performance in polypropylene hollow fiber membranes?

Water intrusion reduces thermal performance due to the introduction of a stagnant liquid layer, which increases thermal resistance at the interface between the liquid and vapor. Although there can be an increase in vapor flux due to reduced vapor path length, the net effect is minimal. The introduction of water also affects the liquid entry pressure (LEP) which can lead to system failure if too high.

- #materials, #thermodynamics.water-intrusion
- #engineering, #material-science.polypropylene-membranes

### Card 2

## Explain how the liquid entry pressure (LEP) is calculated using the Laplace-Young equation. Include the relevant variables and their relationships.

The liquid entry pressure (LEP) can be calculated using the Laplace-Young equation:

$$
\mathrm{LEP} = \frac{4 \gamma \cos(\theta)}{d}
$$

where:
- $\gamma$ is the water surface tension,
- $\theta$ is the contact angle between the liquid and the surface,
- $d$ is the average pore diameter.

For non-cylindrical pores, a geometric factor $\mathrm{B}_{\mathrm{g}}$ (typically 0.4-0.6) is included, modifying the equation to:

$$
\mathrm{LEP} = \frac{4 \gamma \mathrm{B}_{\mathrm{g}} \cos(\theta)}{d}
$$

- #materials, #physics.lep-calculation
- #liquid-dynamics, #material-science.porous-materials

### Card 3

## What are the consequences of liquid entry into the pores of a membrane?

Liquid entry into the pores of a membrane can lead to:
1. Increased thermal resistance due to a stagnant liquid layer.
2. Reduced vapor path length, potentially increasing vapor flux.
3. Changes in interface temperature impacting water vapor pressure.
4. Critical system failure if LEP exceeds 1 bar, leading to significant water entry and heat rejection issues.

- #materials, #engineering.thermal-resistance
- #chemistry, #membrane-science.liquid-entry

### Card 4

## Derive the relationship for liquid entry pressure (LEP) considering non-cylindrical pores with a geometric factor.

For non-cylindrical pores, the geometric factor $\mathrm{B}_{\mathrm{g}}$ becomes necessary in modifying the Laplace-Young equation.

$$
\mathrm{LEP} = \frac{4 \gamma \cos(\theta)}{d}
$$

Including the geometric factor:

$$
\mathrm{LEP} = \frac{4 \gamma \mathrm{B}_{\mathrm{g}} \cos(\theta)}{d}
$$

Here,
- $\gamma$ is the surface tension,
- $\mathrm{B}_{\mathrm{g}}$ is the geometric factor (0.4-0.6 for non-cylindrical pores),
- $\theta$ is the contact angle,
- $d$ is the average pore diameter.

Deriving this relationship ensures that the measured pressure corresponds to the true pore geometry in non-cylindrical contexts.

- #materials, #mathematics.derived-equations
- #physics, #chemical-engineering.pores

### Card 5

## How does the presence of surfactants affect the functionality of the membrane system? Consider the effect on surface tension and LEP.

The presence of surfactants significantly impacts the functionality of the membrane system by:
1. Reducing water surface tension.
2. Lowering the Liquid Entry Pressure (LEP), leading to easier intrusion of water.
3. Decreasing vapor pressure, which affects the driving force for evaporation, reducing thermal performance.

For example, a 1 mM SDS (288 ppm) reduces surface tension by 3%, while 2 mM SDS (576 ppm) reduces it by 9-10%.

- #chemistry, #materials.sc surface-tension
- #physics, #membrane-science.surfactants

### Card 6

## What are the critical failure modes identified for the NASA SWME module?

The critical failure modes for the NASA SWME module include:
1. Significant water loss due to complete pore penetration by liquid water.
2. Fiber bursting is improbable due to high burst pressures (>30 bars).
3. Potential fiber detachment from epoxy casing causing substantial water loss.
4. Reduced vapor pressure due to surfactants leading to detrimental thermal performance.
5. Pore blockage or contamination resulting in reduced $S_p$, hindering heat rejection and achieving desired temperatures.

These factors affect the performance and sustainability of the SWME unit under operational conditions.

- #material-science, #engineering.failure-modes
- #chemical-engineering, #thermal-systems.swme
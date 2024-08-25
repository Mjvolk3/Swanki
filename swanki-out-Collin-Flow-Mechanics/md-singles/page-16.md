a

![](https://cdn.mathpix.com/cropped/2024_06_05_0d6b33a18daa3d6ea92cg-1.jpg?height=566&width=586&top_left_y=178&top_left_x=93)

b

![](https://cdn.mathpix.com/cropped/2024_06_05_0d6b33a18daa3d6ea92cg-1.jpg?height=567&width=499&top_left_y=149&top_left_x=675)

c

![](https://cdn.mathpix.com/cropped/2024_06_05_0d6b33a18daa3d6ea92cg-1.jpg?height=494&width=496&top_left_y=174&top_left_x=1196)

Figure 5

Image-based simulation of effective properties: (a) flow transport (Borner et al. 2017), (b) thermal transport (Semeraro et al. 2021), and (c) chemistry (Ferguson et al. 2016, 2017). Panels \(b\) and \(c\) adapted from Ferguson et al. (2018) (CC BY 4.0).

useful for materials where the thermal conductivity of each phase is isotropic and the porosity is homogeneous. Semi-analytical models (Lee 1989, Marschall \& Milos 1997, Daryabeigi et al. 2011, Van Eekelen \& Lachaud 2011) and solutions to the radiative heat transfer equations (Petrov 1997, Le Foll et al. 2012) for fibrous media with anisotropic fiber orientation have been proposed. For cases where the microstructure is known and available either analytically or through \(\mu-\mathrm{CT}\), Wiegmann \& Bube (2000) developed an efficient numerical method to solve the homogenization formulation for the conduction problem. For materials where the conductivity is anisotropic at the phase level and at the mesoscale (such as weaves), DNS using carefully chosen numerical methods is an effective approach (Semeraro et al. 2020). Recent studies have used stochastic techniques applied to microstructure data with opaque, transparent, or semitransparent phases to compute radiative conductivity of fiber-based TPS material (Nouri \& Martin 2015, Nouri et al. 2016). Well-established laboratory measurements are used to determine the heat capacity and the heat of pyrolysis by differential scanning calorimetry (Torres-Herrador et al. 2021). Figure 5 highlights a series of effective properties predictions based on carbon fiber microtomography measurements.

\title{
4.2. Mass and Momentum Transport
}

As illustrated in Section 3.5, the permeability in the Knudsen regime is of interest to TPS applications because the material pore scale is of the same order as the mean free path of the permeating gases. Permeability decreases as the Knudsen number increases but has a minimum in the transition regime (De Socio \& Marino 2006). DSMC is a natural choice for use with \(\mu\)-CT rendering of porous materials. This approach becomes computationally intensive at low Knudsen numbers, but results by DSMC have proven accurate when compared with experimental data (White et al. 2016, Borner et al. 2017). In the low-Knudsen-number regime, solving the low Reynolds number, incompressible equations are more efficient methods to estimate permeability from tomography data (Wiegmann 2007). Flow tube experiments provide validation sets for microscale and mesoscale simulations. Experimental efforts on ablative materials have demonstrated that both the intrinsic \(\underline{\mathbf{K}}_{0}\) permeability and the Knudsen correction factor \(\underline{\mathbf{b}}\) can be determined from differential pressure measurement across porous samples at increasing mass flows and average pressure
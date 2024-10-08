\title{
Performance evaluation and model of spacesuit cooling by hydrophobic hollow fiber-membrane based water evaporation through pores
}

\author{
M. Arif Khan \({ }^{\mathrm{a}}\), Glenn Lipscomb \({ }^{\mathrm{b}}\), Andrew Lin \({ }^{\mathrm{a}}\), Kevin C. Baldridge \({ }^{\mathrm{a}}\), Elspeth M. Petersen \({ }^{\mathrm{c}}\), \\ John Steele \({ }^{\mathrm{d}}\), Morgan B. Abney \({ }^{\mathrm{e}}\), Dibakar Bhattacharyya \({ }^{\mathrm{a},},{ }^{2}\) \\ \({ }^{a}\) Department of Chemical and Materials Engineering, University of Kentucky, Lexington, KY, 40506, USA \\ \({ }^{\mathrm{b}}\) Chemical Engineering Department, School of Green Chemistry and Engineering, University of Toledo, Toledo, OH, 43606, USA \\ \({ }^{\mathrm{c}}\) National Aeronautics and Space Administration, Kennedy Space Center, FL, 32899, USA \\ \({ }^{\mathrm{d}}\) MRI Technologies Inc., Houston, TX, 77058, USA \\ \({ }^{\mathrm{e}}\) National Aeronautics and Space Administration, Langley Research Center, Hampton, VA, 23666, USA
}

\begin{abstract}
A B S T R A C T
A comprehensive mathematical model is presented that accurately estimates and predicts failure modes through the computations of heat rejection, temperature drop and lumen side pressure drop of the hollow fiber (HF) membrane-based NASA Spacesuit Water Membrane Evaporator (SWME). The model is based on mass and energy balances in terms of the physical properties of water and membrane transport properties. The mass flux of water vapor through the pores is calculated based on Knudsen diffusion with a membrane structure parameter that accounts for effective mean pore diameter, porosity, thickness, and tortuosity. Lumen-side convective heat transfer coefficients are calculated from laminar flow boundary layer theory using the Nusselt correlation. Lumen side pressure drop is estimated using the Hagen-Poiseuille equation. The coupled ordinary differential equations for mass flow rate, water temperature and lumen side pressure are solved simultaneously with the equations for mass flux and convective heat transfer to determine overall heat rejection, water temperature and lumen side pressure drop. A sensitivity analysis is performed to quantify the effect of input variability on SWME response and identify critical failure modes. The analysis includes the potential effect of organic and/or inorganic contaminants and foulants, partial pore entry due to hydrophilization, and other unexpected operational failures such as bursting or fiber damage. The model can be applied to other hollow fiber membrane-based applications such as low temperature separation and concentration of valuable biomolecules from solution.
\end{abstract}

\section*{1. Introduction}

Polymeric hollow fiber membranes are ubiquitous in membranebased separations ranging from membrane distillation to pervaporation for water purification, desalination, gas separation, liquid-liquid extraction etc. [1-5]. Vacuum membrane distillation (VMD) in particular is used for water purification and treatment, desalination, liquid-liquid separation, removal of organics and recovery of solutes \([6-10]\).

The vast amount of literature published on VMD, and other membrane distillation applications using hollow fiber membranes, is relevant to the design of innovative devices like NASA's hollow fiber-based Spacesuit Water Membrane Evaporator (SWME) [11-14], The SWME is a critical component of the portable life support system in spacesuits used for extravehicular activities. It is designed to reject the heat generated by the crew member wearing the suit and the electrical components of the suit's portable life support subsystem. Heat is removed by circulating a heat transfer fluid (water) from a reservoir through a heat exchange network in the suit. The heated water is cooled by evaporating a portion of the water to space in the SWME and recirculated for thermal control. The rate of water evaporation and associated exiting liquid water temperature are controlled by adjusting the water vapor pressure in the shell of the hollow fiber module with a backpressure valve as illustrated in Fig. 1. The water reservoir is refilled as needed.

SWME operation is similar to VMD. A hot water stream is passed through a membrane module where evaporation and cooling occur. However, operational objectives are significantly different. VMD seeks to minimize heat loss due to evaporation while SWME seeks to maximize it. In contrast to VMD, SWME operations is at a lower inlet temperature and the main goal is to cool the water in the lumen side rather than producing a particular quality distillate.

VMD modeling [10,15-17] may be adapted for the SWME unit to reduce expensive experimental testing and performance evaluation and enables early detection of degradation that could lead to critical failures. This provides an added layer of operational protection for astronauts
\footnotetext{
* Corresponding author.

E-mail address: db@uky.edu (D. Bhattacharyya).
}
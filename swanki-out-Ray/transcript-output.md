**Performance Evaluation and Model of Spacesuit Cooling by Hydrophobic Hollow Fiber-Membrane Based Water Evaporation Through Pores**

**Introduction**

In the world of membrane-based separations, polymeric hollow fiber membranes are a staple, featuring prominently in processes such as membrane distillation, pervaporation for water purification, desalination, gas separation, and even liquid-liquid extraction. One particular application of these membranes is in vacuum membrane distillation, or VMD, which is utilized for a variety of purposes including water purification, desalination, liquid-liquid separation, and the recovery of solutes.

A fascinating and critical application of these membranes is within the NASA Spacesuit Water Membrane Evaporator, or SWME. This device is integral to the portable life support system found in spacesuits used during extravehicular activities, essentially spacewalks. The SWME's primary task is to manage the heat generated not only by the astronaut but also by the electrical components within the suit's life support subsystem. The mechanism involves circulating water as a heat transfer fluid through a network within the suit. The water, after absorbing heat, is cooled by evaporating a portion of it into space within the SWME. This cooled water is then recirculated to continue the thermal management process.

The operation of the SWME bears similarities to VMD. In both systems, a hot water stream is passed through a membrane module where evaporation and cooling take place. However, the goals differ significantly. VMD aims to minimize heat loss during evaporation, while the SWME's objective is to maximize it to ensure effective cooling. Additionally, the SWME operates at a lower inlet temperature, focusing on cooling the water within the lumen side rather than producing a specific quality of distillate.

The SWME's design and operational strategy can benefit greatly from modeling approaches previously developed for VMD. Adapting these models can help reduce the need for extensive experimental testing, thus saving costs and enabling early detection of potential system failures. This proactive approach is vital for the safety and efficiency of space missions, where the reliability of every component is crucial.

**Complete and Partial Pore Entry by Water**

One of the significant challenges with polypropylene hollow fiber membranes is their potential to experience water intrusion and a consequent reduction in surface contact angle over prolonged exposure to water. Studies indicate that exposure to deionized water can reduce the contact angle from over 115 degrees to around 100 degrees within 90 days at room temperature. This change in hydrophilicity can be exacerbated by particulates and scaling, which increase the hydrophilicity of the pore inner surface.

The presence of larger pores within the membrane can enhance heat rejection due to higher structural parameter values. However, if liquid water intrudes into these pores, it can have severe consequences. The intrusion process can be analyzed using the Laplace-Young equation, which relates the liquid intrusion pressure to parameters such as the geometric factor, water surface tension, contact angle, and average pore diameter.

For non-cylindrical pores, the geometric factor is usually less than one, meaning that the liquid entry pressure can be significantly lower for stretched membrane pores than for cylindrical ones of the same size. At an operating lumen pressure of approximately 1.2 bar, liquid water is likely to enter pores larger than 100 nanometers for a contact angle of 95 degrees, and pores larger than 200 nanometers for a contact angle of 100 degrees. Organic contaminants can also affect the surface tension of the water, though their impact is relatively small.

Partial liquid entry into the pores can reduce the vapor path length, increasing the structural parameter value. This change introduces additional thermal resistance due to the presence of a stagnant liquid layer, affecting the interface temperature between the liquid and vapor and thus the water vapor pressure driving evaporation. Modeling efforts suggest that partial liquid entry's net effect on the system could be relatively small, as the increased vapor flux from the reduced vapor path length offsets the increased thermal resistance from the liquid layer.

**Analysis of Critical Failure Modes for SWME Module**

Through the model results and subsequent analysis, several critical failure modes for the SWME module have been identified. One such mode involves complete liquid water penetration through a fraction of the pores due to changes in hydrophobicity. Even a small percentage of pore leakage can lead to significant water loss from the system, reducing the operational time of the spacesuit.

The burst pressure of various polymeric fibers has been found to exceed 30 bars across a temperature range from minus 40 to 160 degrees Celsius, making high lumen water pressure-induced fiber bursting unlikely under normal operating conditions. However, fiber detachment from the epoxy casing could lead to substantial water loss, thereby limiting the spacesuit's operational duration.

The presence of surfactants can significantly reduce vapor pressure and the driving force for evaporation, negatively impacting thermal performance. Although surfactants would not be introduced intentionally, accidental contamination must be avoided to prevent system failure.

Another critical failure mode involves the reduction of the structural parameter due to pore blockage, contamination, precipitation of particulates, or organic fouling. A decrease in the structural parameter results in reduced thermal performance and higher outlet temperatures. If the outlet temperature exceeds desired values, the system's pressure control mechanisms might be unable to maintain optimal performance, especially under maximum vacuum conditions, such as those found on Mars.

**Conclusions**

In this work, we developed a comprehensive predictive mathematical model to estimate the thermal performance of NASA's SWME. The model incorporates mass and energy balances during water evaporation through membrane pores, diffusive transport of water vapor, and the differential Hagen-Poiseuille equation for lumen-side water pressure drop. By correlating critical input variables such as inlet water temperature, mass flow rate, shell side pressure, and membrane structure parameter, the model predicts key output parameters like heat rejection, outlet water temperature, temperature drop, and lumen side pressure drop.

Using NASA's experimental data, we validated the model and performed a sensitivity analysis to understand the impact of changes in input variables on thermal performance. The analysis highlighted the effects of particulates, contaminants, and foulants on the SWME unit and discussed the implications of partial pore entry caused by changes in hydrophobicity.

Our findings indicate that a 45 percent reduction in the structural parameter due to pore blockage is tolerable under Martian surface atmospheric pressure conditions. Additionally, critical failure modes such as fiber bursting and leakage, surfactant contamination, and structural parameter reduction were analyzed, providing insights into potential system failures and their impact on operational performance.

Overall, this work advances the field of hollow fiber-based membrane applications by offering a robust mathematical framework to analyze and predict critical process parameters and the effects of contaminants and foulants on thermal performance. Future applications of this model could extend to predicting the performance of hollow fiber-based membrane separations for biomolecule concentration and purification at lower temperatures from dilute aqueous solutions.
### Understanding Key Parameters in Membrane-Based Systems

In order to fully comprehend the technical scope of membrane-based systems, particularly in the context of space applications, it's crucial to understand various parameters that define their performance. These parameters include physical constants, temperatures, radii, and velocities, all of which play significant roles in the system's operation.

For instance, the gas constant, denoted as 'R,' is a fundamental physical constant that appears in many thermodynamic equations, particularly those involving gases. Another important parameter is the radius of the lumen, 'r sub l,' which refers to the internal radius of the hollow fibers used in the membrane. This radius is critical as it affects the flow rate and pressure drop within the membrane system. Similarly, the pore radius, 'r sub p,' is essential for determining the membrane's permeability and its ability to filter molecules based on size.

Temperature parameters are also pivotal. For example, 'T' represents the liquid water temperature, while 'T sub p' stands for the pore temperature. These temperatures are important for understanding the thermal dynamics within the system, such as how heat transfer affects the evaporation and condensation processes. The water velocity, denoted as 'v sub w,' is equally important as it influences the flow dynamics and the efficiency of the membrane's operation.

### Greek Letters and Their Significance

Moving on to Greek letters, these often represent physical properties that are crucial for the detailed analysis of membrane systems. For example, 'gamma sub L' stands for the water surface tension, a key factor in determining how water interacts with the membrane surface. Surface tension affects processes like capillary action and wetting, which are vital for the membrane's functionality.

The membrane thickness, denoted as 'delta,' is another critical parameter. A thicker membrane might offer more structural integrity but could also impede flow and reduce efficiency. Conversely, 'delta sub L' and 'delta sub V' refer to the liquid entry length and vapor path length, respectively. These lengths are important for understanding how fluid enters and exits the membrane and how vapor travels through it.

Other significant Greek letters include 'kappa,' which represents thermal conductivity. This is crucial for analyzing how heat is transferred through different materials within the membrane system. 'Kappa sub p p' and 'kappa sub w' specifically refer to the thermal conductivities of polypropylene and water, respectively. These values are essential for designing systems that efficiently manage heat.

### Thermal Performance and Modeling

When it comes to the thermal performance of membrane systems, particularly for applications like the NASA SWME (Sweat Management Equipment) unit, a comprehensive model is essential. This model needs to predict how various factors affect heat rejection, temperature regulation, and water loss. Key performance metrics include the outlet water temperature, the rate of heat rejection, and the rate of water loss per unit of heat rejected.

To develop such a model, one must consider numerous variables, including the water inlet conditions and the membrane parameters like pore size, porosity, and tortuosity. These factors are critical because they directly influence the system's efficiency and performance. For example, pore size and distribution affect how easily vapor can pass through the membrane, while porosity impacts the overall permeability and structural integrity of the membrane.

The modeling process is complex, involving differential mass and energy balances. For instance, the vapor flux can be calculated using Knudsen diffusion, which takes into account the Knudsen number—a dimensionless number that characterizes gas flow through small pores. Additionally, lumen-side convective heat transfer can be estimated using correlations like the Nusselt number for laminar flow in circular channels.

### Figures and Practical Applications

Figures play a crucial role in visualizing the concepts discussed. For example, an illustration of an astronaut's spacesuit integrated with the SWME module can provide a clear understanding of how the system functions in a real-world scenario. Detailed schematics showing the internal components and their pathways for water and vapor flow help in comprehending the operational mechanics.

A simplified conceptual diagram of a single hollow fiber within the SWME module further elucidates the principles at play. It shows the direction of water flow, the vapor pressure difference across the membrane, and the temperature profile along the fiber's length. These visual aids are invaluable for grasping the complex interactions between various parameters and their impact on the system's performance.

Finally, it's important to consider the long-term performance of the membrane system. Factors like particulate contamination, organic fouling, and structural degradation can significantly affect the system's efficiency over time. Understanding these factors through comprehensive modeling and sensitivity analysis helps in designing more robust and effective membrane systems for critical applications, such as those required in space missions.

In summary, a deep understanding of the various physical parameters, thermal dynamics, and modeling techniques is essential for designing and optimizing membrane-based systems, particularly for challenging applications like those in space exploration.
### Section: Mathematical Formulations

In this section, we delve into the mathematical models and equations used to describe the processes occurring within a hollow fiber membrane during the vaporization of water. These processes are complex and involve the conservation of mass, energy, and momentum. The key variables include the lumen diameter, total fiber length, and normalized dimensionless length. 

The vapor flux, which is dependent on temperature and varies along the axial position of the fiber, is crucial. Starting with the mass flow rate equation, the initial condition is defined at the inlet where the mass flow rate per fiber is given. Next, the variation of water temperature in the lumen is expressed as a differential equation. This equation takes into account the latent heat of vaporization and the specific heat capacity of water, both of which are temperature-dependent. The initial condition here is the inlet temperature.

Furthermore, the pressure drop in the lumen is described by a differential form of the Hagen-Poiseuille equation, which relates the pressure gradient to the viscosity, density, and flow rate of water. The initial condition for this equation is the inlet pressure. Additionally, the convective heat transfer in the lumen boundary layer is considered, with the heat transfer coefficient estimated using the Nusselt number for laminar flow. This comprehensive model integrates these equations to predict the temperature, pressure, and mass flow rate along the fiber.

### Section: Liquid Entry into Pores

Liquid entry into the membrane pores is analyzed using the Laplace equation, which connects the liquid entry pressure (LEP) to the surface tension of the liquid and the contact angle with the membrane. The equation illustrates that the LEP is inversely proportional to the pore diameter. This means that smaller pores have a higher resistance to liquid entry. 

Should the lumen side of the membrane become hydrophilized due to fouling, the pressure could exceed the LEP, causing liquid to enter the pores up to a certain depth. The water vapor flux, in this scenario, is a function of this depth and the overall membrane structure parameter. The model also considers the possibility of partial liquid entry, which affects the vapor-liquid interface temperature and the resulting flux through the pores.

If water wets the pores, the liquid mass flux is estimated using the Hagen-Poiseuille equation for flow through small channels. This equation takes into account the capillary pressure, which is determined by the surface tension and the modified contact angle. The temperature-dependent physical properties like viscosity and density are also factored into these calculations, evaluated at an average temperature.

### Section: Results and Discussion

To solve the system of ordinary differential equations (ODEs) that describe these processes, the MATLAB® ode45 solver is used. This numerical method helps in obtaining the profiles of liquid water mass flow rate, temperature, pore temperature, and pressure along the length of the fiber. These profiles are essential to understand the performance of the Sweating Manikin Water Evaporator (SWME) in a spacesuit environment.

The results from this model are used to calculate critical performance metrics such as heat rejection, total mass of vaporized water, temperature drop, and pressure drop within the lumen. These calculations provide insights into the efficiency and effectiveness of the SWME system under various operating conditions.

### Section: Hollow Fiber Characterization

The characterization of the hollow fiber membrane is essential for validating the model. NASA's experimental measurements are used to estimate the membrane's structural parameter. Scanning Electron Microscope (SEM) images reveal the detailed pore structure on the lumen and shell side surfaces, as well as the cross-sectional view. These images show a more uniform pore structure compared to other commonly used membranes like PVDF or PES.

The SEM analysis indicates that the pores have an ellipsoidal shape, which affects the diffusion characteristics. The pore size distribution is crucial, with the minor axis being more significant for vapor diffusion. The presence of a fibrous internal structure rather than a spongy one suggests less variability in pore size, contributing to more consistent performance.

### Section: Estimation of Structure Parameter and Model Validation

The vapor transport through the membrane pores is modeled using Knudsen diffusion, which is applicable for small pore sizes and higher Knudsen numbers. The Knudsen number, which depends on the mean free path and pore diameter, is well above the threshold for Knudsen diffusion in this context. 

The overall membrane structure parameter, which includes pore diameter, porosity, membrane thickness, and tortuosity, is crucial for estimating the vapor flux. Using manufacturer-reported values, the model predictions are validated against experimental data. This validation ensures that the model accurately represents the physical processes within the SWME system, providing confidence in its use for performance predictions and optimizations.
**Model Predictions and Experimental Validation**

To understand the performance and optimization of hollow fiber membranes, we need to delve into the details of their pore structures and how these structures impact thermal properties. For our hollow fiber membrane evaporator (SWME), the tortuosity and porosity of the fibers are crucial parameters. Porosity is measured at 24%, but tortuosity was not verified experimentally. However, using nitrogen adsorption data and fitting model predictions with experimental thermal performance data from NASA, we can determine the best-fit value for the structure parameter, denoted as \( S_P \).

The initial value of \( S_P \) set at 4.0 times 10 to the power of negative 4 overpredicts heat rejection by a factor of two. By adjusting \( S_P \) to 1.04 times 10 to the power of negative 4, the model achieves an almost perfect fit with an R-squared value of 0.9965. This adjustment brings the error in heat rejection down to a mere 0.3%. With our parameters, including pore diameters of 42 and 46 nanometers for the shell and lumen surfaces respectively, and a thickness of 40 micrometers, we calculate the tortuosity to be approximately 2.44 and 2.67, which is consistent with previously reported values for polypropylene membrane hollow fibers. This accurate fit supports the robustness of our model in predicting the thermal performance of hollow fiber membranes.

Additionally, the model was validated against experimental vapor flux data for PVDF membranes, showing remarkable agreement even with non-uniform pore structures. This consistency across different membrane materials and structures provides confidence in the model's predictive capabilities.

**Model Prediction Results for New Generation SWME Module**

Using the best-fit structure parameter, the model was applied to a new SWME module design containing 27,900 fibers with an active length of 11.9 centimeters. The model predicted the liquid water temperature along the dimensionless length of the fibers for shell side pressures of 0.5 torr and 7 torr, which corresponds to Mars atmospheric pressure. For a shell side pressure of 0.5 torr, the temperature approaches zero degrees Celsius at the midpoint of the fiber length with the higher structure parameter value, whereas it remains above zero for the best-fit value of 1.04 times 10 to the power of negative 4. This is critical because a negative temperature would result in ice formation, which is undesirable for SWME applications.

For a shell side pressure of 7 torr, the outlet water temperature was 7.2 degrees Celsius and 12.9 degrees Celsius for the higher and best-fit structure parameter values, respectively. These results indicate that lower shell side pressures and higher structure parameters lead to rapid temperature drops, which can limit the effectiveness of the evaporator.

**Heat Rejection and Membrane Performance**

The performance metrics of the membrane, including heat rejection, total mass of water vaporized, outlet water temperature, and lumen side pressure drop, are influenced by the structure parameter and shell side pressure. Heat rejection and mass of water vaporized increase with higher structure parameters and lower shell pressures. However, there is a maximum beyond which no further increase is observed, indicating an optimal range for these parameters.

Inlet water temperature also plays a significant role, with higher temperatures increasing heat rejection and vaporization rates due to the enhanced driving force for vapor flux. At Mars atmospheric pressure (7 torr), the membrane performs effectively above an inlet temperature of 6 degrees Celsius, below which cooling is not feasible. This highlights the importance of optimizing inlet conditions to match the environmental constraints of the intended application, such as space missions.

**Fixed Lumen Outlet Water Temperature**

For spacewalks, where the heat load is about 350 watts, the SWME module must maintain a nominal inlet water temperature around 17 degrees Celsius, targeting an outlet temperature of 10 degrees Celsius. With the optimized membrane parameter, the outlet temperature can be closely controlled to meet these requirements, ensuring the astronaut's safety and comfort. The model's ability to predict these conditions accurately underscores its utility in designing effective thermal management systems for space applications.

In summary, the detailed modeling and validation against experimental data confirm the effectiveness of the hollow fiber membrane in managing heat rejection for various conditions. By optimizing the structure parameters and operational conditions, the SWME module can be tailored to meet the specific requirements of space missions, ensuring reliable performance in extreme environments.
### Dependence of Outlet Water Temperature on Inlet Temperature and Membrane Structure Parameter

When examining the performance of a thermal management system, it's crucial to understand how the outlet water temperature responds to changes in inlet water temperature and the membrane structure parameter, often denoted as \( S_P \). For a shell pressure of 7 torr, the relationship is depicted as a color heat map, illustrating that the outlet water temperature tends to increase with both higher inlet water temperatures and reductions in \( S_P \). This relationship is essential for controlling the thermal output and ensuring the system operates within desired temperature ranges.

The contour plots provided alongside the heat map offer a practical way to visualize and choose combinations of inlet water temperature and \( S_P \) that achieve a specific outlet temperature. For instance, if an outlet temperature of 10 degrees Celsius is targeted, one can refer to these plots to determine the appropriate inlet conditions and membrane properties required. This method simplifies the process of adjusting the system to meet specific thermal performance goals without extensive trial and error in physical experiments.

### Evaluation of Approximate Algebraic Solution

To predict heat rejection and temperature drop in a system, an approximate algebraic solution can be developed. This solution simplifies the comprehensive mathematical model, typically represented by ordinary differential equations (ODEs), by assuming that the physical properties of water remain constant. Such assumptions include averaging properties like density, heat capacity, and thermal conductivity over the temperature range of 5 to 30 degrees Celsius. Although water vapor pressure varies significantly with temperature, the algebraic model approximates it based on the average temperature between the inlet and outlet.

While the algebraic solution may introduce greater error at higher inlet temperatures and membrane structure parameters, it provides a quick and less computationally intensive method for predicting the system's thermal performance. For instance, figures from supplementary information show that heat rejection and temperature distribution predictions align reasonably well with the more accurate ODE model, particularly at lower inlet temperatures. This approach is valuable for preliminary assessments and operational planning, even though it may not replace detailed simulations for final design and optimization.

### Role of Particulates, Contaminants, and Foulants in Lumen Water

Fouling, caused by scaling or particulate deposition, significantly impacts the performance of membrane distillation systems like the SWME (Sweating Manikin Evaporator). Over time, contaminants such as calcium carbonate (CaCO_3) and other particulates can accumulate on the membrane surface, leading to reduced water flux and heat rejection. For instance, polypropylene hollow fiber membranes have shown notable scaling and flux reduction when exposed to tap water in distillation processes.

The effects of fouling are multifaceted. They can include pore blocking, which reduces pore size and surface porosity, ultimately lowering the membrane structure parameter \( S_P \). This reduction directly impacts the system's thermal performance, as smaller pore sizes and reduced porosity decrease heat rejection efficiency. Figures illustrate that even a reduction in pore size by half can significantly diminish heat rejection across various inlet temperatures. The linear relationship between pore size reduction and heat rejection underscores the need for effective fouling management and membrane maintenance.

Understanding these dynamics is crucial for maintaining the long-term efficiency and reliability of membrane-based systems, especially in critical applications such as space thermal management, where consistent performance is vital.

### Liquid Entry Pressure and Membrane Properties

The liquid entry pressure (LEP) of a membrane is influenced by factors such as the contact angle and average pore diameter, which vary with water surface tension. For different water surface tensions, ranging from 40 to 70 mN/m, 3D surface and contour plots illustrate how LEP changes. These plots provide valuable insights into the capillary properties of the membrane, helping to optimize its design for specific applications.

For instance, a higher contact angle or smaller pore diameter generally increases LEP, indicating a stronger resistance to liquid entry. This characteristic is crucial for applications requiring selective permeability and high separation efficiency. By adjusting these membrane properties, one can fine-tune the system to achieve desired performance metrics, balancing factors like permeability, selectivity, and mechanical strength.

These visualizations aid in understanding how physical membrane characteristics affect its operational effectiveness, informing decisions for improving design and troubleshooting existing systems. This knowledge is particularly relevant for optimizing desalination or separation processes, where maintaining high performance and minimizing fouling are critical for sustainable operation.
### Front
Provide the equation for the total mass of water vaporized in a system, given the inlet and outlet mass flow rates.

### Back
The total mass of water vaporized, $\left(\dot{m}_{v}\right)_{\text{tot}}$, is given by:

$$
\left(\dot{m}_{v}\right)_{\text{tot}} = \dot{m}_{\text{in}} - \dot{m}_{\text{out}}
$$

where:
- $\dot{m}_{\text{in}}$ is the inlet mass flow rate of water,
- $\dot{m}_{\text{out}}$ is the outlet mass flow rate of water.

- #fluid-dynamics, #heat-transfer, #water-vaporization

---

### Front
What is the expression for the pressure drop across the lumen side, $\Delta P_{\text{lumen}}$?

### Back
The pressure drop across the lumen side, $\Delta P_{\text{lumen}}$, is given by:

$$
\Delta P_{\text{lumen}} = \left(P_{\text{lumen}}\right)_{\text{in}} - \left(P_{\text{lumen}}\right)_{\text{out}}
$$

where:
- $\left(P_{\text{lumen}}\right)_{\text{in}}$ is the inlet lumen pressure,
- $\left(P_{\text{lumen}}\right)_{\text{out}}$ is the outlet lumen pressure.

- #fluid-dynamics, #pressure-drop, #membrane-processes

---

### Front
Define the membrane structure parameter $S_{P}$ using its variables.

### Back
The membrane structure parameter $S_{P}$ is defined as:

$$
S_{P} = \frac{d_{p} \varphi_{p}}{\delta \tau}
$$

where:
- $d_{p}$ is the mean pore diameter,
- $\varphi_{p}$ is the membrane porosity,
- $\delta$ is the membrane thickness,
- $\tau$ is the membrane tortuosity.

- #membrane-science, #fluid-transport, #porosity

---

### Front
What is the expression for the heat rejection rate $q$?

### Back
The heat rejection rate, $q$, is calculated by integrating the product of latent heat of vaporization and mass flow rate of vapor over the length of the membrane:

$$
q = \int_{0}^{L} \lambda_{v} \dot{m}_{v} \, dz
$$

where:
- $\lambda_{v}$ is the latent heat of vaporization,
- $\dot{m}_{v}$ is the mass flow rate of vapor,
- $L$ is the length of the membrane.

- #heat-transfer, #vaporization, #membrane-processes

---

### Front
Explain the term $J_{k}$ in the context of membrane transport.

### Back
The term $J_{k}$ represents the vapor mass flux through the membrane, and can be defined as:

$$
J_{k} = (0.0248) S_{P} \sqrt{\frac{1}{T_{P}}} (\Delta P)
$$

where:
- $S_{P}$ is the membrane structure parameter,
- $T_{P}$ is the temperature at the membrane pores,
- $\Delta P$ is the pressure difference across the membrane.

- #transport-phenomena, #membrane-flux, #vapor-transport

---

### Front
Provide the equation for liquid entry pressure (LEP) using membrane and liquid properties.

### Back
The liquid entry pressure (LEP) is given by the Laplace equation:

$$
LEP = -\frac{4 B_{g} \gamma_{L} \cos \theta_{o}}{d_{P}}
$$

where:
- $B_{g}$ is the geometric factor (typically, $B_{g}=1$ for cylindrical pores),
- $\gamma_{L}$ is the surface tension of the liquid,
- $\theta_{o}$ is the initial contact angle of the liquid with the membrane,
- $d_{P}$ is the mean pore diameter.

- #membrane-science, #liquid-entry-pressure, #fluid-properties
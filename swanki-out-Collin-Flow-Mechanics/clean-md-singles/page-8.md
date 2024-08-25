differentiation by part and properties of the phase-mask. This will yield the extended governing equations derived by Sirovich $(1967,1968)$ that are the basis of the IBM (Peskin 1972, Goldstein et al. 2005, Mittal \& Iaccarino 2005).

As an example of extending a governing equation from $\mathbb{R}_{\mathrm{f}}^{3}$ to $\mathbb{R}^{3}$, consider the momentum equations for compressible flow in the fluid phase, $\mathrm{f}$, with a moving boundary,

$$
\left(\rho_{\mathrm{f}} \mathbf{u}_{\mathrm{f}}\right)_{t}+\nabla_{\mathfrak{\varepsilon}_{\mathrm{f}}} \cdot\left(\rho_{\mathrm{f}} \mathbf{u}_{\mathrm{f}} \otimes \mathbf{u}_{\mathrm{f}}\right)=\nabla_{\mathfrak{E}_{\mathfrak{f}}} \cdot\left(-p_{\mathrm{f}} \underline{I}+\underline{\tau}_{\mathrm{f}}\right) \quad \forall \varepsilon_{\mathrm{f}} \in \mathbb{R}_{\mathrm{f}}^{3}
$$

and

$$
\mathbf{u}_{\mathrm{f}}\left(\xi^{\Sigma_{f}}\right)=\mathbf{w}
$$

where $\mathbf{w}$ is the velocity of the wall as shown in Figure 2. Multiplying the above equation by the phase-mask of the fluid phase, $\left(\gamma^{f}\right)^{3}$, and then using differentiation by parts and properties of the gradients of the phase-mask function and rearranging the terms, we get

$$
\left(\rho^{\mathrm{f}} \mathbf{u}^{\mathrm{f}}\right)_{, t}+\nabla_{\mathcal{E}} \cdot\left(\rho^{\mathrm{f}} \mathbf{u}^{\mathrm{f}} \otimes \mathbf{u}^{\mathrm{f}}\right)=\nabla_{\underline{E}} \cdot\left(-p^{\mathrm{f}} \underline{\mathrm{I}}+\underline{\boldsymbol{\tau}}^{\mathrm{f}}\right)+\mathbf{F}^{\Sigma_{\mathrm{f}}}
$$

and

$$
\mathbf{F}^{\Sigma_{\mathrm{f}}}=\left(\rho_{\mathrm{f}} \mathbf{u}_{\mathrm{f}} \otimes \mathbf{w}-\rho_{\mathrm{f}} \mathbf{u}_{\mathrm{f}} \otimes \mathbf{u}_{\mathrm{f}}-p_{\mathrm{f}} \underline{I}+\underline{\boldsymbol{\tau}}_{\mathrm{f}}\right) \cdot \boldsymbol{n}^{\mathrm{f}} \delta\left(\boldsymbol{\xi}-\xi^{\Sigma_{\mathrm{f}}}\right)
$$

The use of $n=3$ when multiplying by $\left(\gamma^{\mathrm{f}}\right)^{n}$ enabled all dependent variables in the nonlinear terms to be formally defined in $\mathbb{R}^{3}$. Boundary forces appearing in the governing equations should be interpreted in the integral sense-in essence, this is the basis of the IBM (Peskin 1972, Goldstein et al. 1993).

\title{
3.2. Volume Averaging
}

For dependent variables that vary rapidly in space, VAM defines superficial averaged quantities of interest by averaging the variables over an arbitrary elementary volume (AEV), $\mathcal{V}$ (see Figure 3),

![](https://cdn.mathpix.com/cropped/2024_06_05_23237fc8fa5ea45d3cb7g-1.jpg?height=628&width=919&top_left_y=1297&top_left_x=594)

Figure 3

Definitions of volumes and surfaces of solid and fluid phases in an averaging volume, $\mathcal{V}$, at a location $\mathbf{x}$ in $\mathbb{R}^{3}$. The defined volume space of a phase within $\mathcal{V}$ is denoted by $\mathcal{V}_{\mathrm{p}}$; the surface between phase-p and its

![](https://cdn.mathpix.com/cropped/2024_06_05_23237fc8fa5ea45d3cb7g-1.jpg?height=37&width=1258&top_left_y=2049&top_left_x=415)
$(\cdot)$ is $\boldsymbol{n}^{\mathrm{p} /(\cdot)} . \Delta$ is the weight function compact support width.
## Define the phase-mask function $\gamma^{\mathrm{p}}(\xi, t)$ for a phase-p.
The phase-mask function $\gamma^{\mathrm{p}}(\xi, t)$ for a phase-p is defined as follows:

$$
\gamma^{\mathrm{p}}(\xi, t)=\left\{\begin{array}{cl}
1 & \forall \xi \in \mathbb{R}_{\mathrm{p}}^{3} \\
1 / 2 & \xi=\xi^{\Sigma} \in \Sigma_{\mathrm{p}} \\
0 & \text { Otherwise }
\end{array}\right.
$$

- $ \mathbb{R}_{\mathrm{p}}^{3} $ is the domain where phase-p exists.
- $ \Sigma_{\mathrm{p}} $ is the interface where the phase boundary is located.

- #phase-mask-function, #phase-transitions, #mathematical-modeling

## Explain the subspace $\mathbb{R}_{\mathrm{p}}^{3}$ in the context of phase-mask functions.

The subspace $\mathbb{R}_{\mathrm{p}}^{3}$ where the phase-p is defined includes:

$$
\mathbb{R}_{\mathrm{p}}^{3}=\mathbb{R}_{0}^{3}\left(=\mathbb{R}_{\mathrm{f}}^{3}\right), \mathbb{R}_{1}^{3}, \mathbb{R}_{2}^{3}, \ldots, \mathbb{R}_{N_{\mathrm{p}}}^{3}
$$

Where $\mathbb{R}_{\mathrm{f}}^{3}$ is the subspace of the fluid phase and $\mathbb{R}_{\mathrm{i}}^{3}$ is the subspace of solid phase-i. $N_{\mathrm{p}}$ is the number of solid phases.

- #subspace, #phase-mask-function, #mathematical-modeling

## How does the phase-mask function $\gamma^{\mathrm{p}}(\xi, t)$ affect the dependent variables $\mathbf{q}^{\mathrm{p}}(\xi, t)$?

The dependent variables $\mathbf{q}^{\mathrm{p}}(\xi, t)$ are extended across the entire space $\mathbb{R}^{3}$ by the phase-mask function $\gamma^{\mathrm{p}}(\xi, t)$:

$$
\mathbf{q}^{\mathrm{p}}(\xi, t)=\left[\gamma^{\mathrm{p}}(\xi, t)\right]^{n} \mathbf{q}_{\mathrm{p}}(\xi, t)
$$

Where $n$ is an arbitrary natural number greater than 1.

- #dependent-variables, #phase-mask-function, #mathematical-modeling

## What is the role of the power $n$ in the expression $\left[\gamma^{\mathrm{p}}(\xi, t)\right]^{n}$?

The power $n$ in $\left[\gamma^{\mathrm{p}}(\xi, t)\right]^{n}$ generalizes the phase-mask function and aids in extending the validity of governing equations to the entire space $\mathbb{R}^{3}$. It does not affect the properties of the time derivative or gradients of the phase-mask function.

- #power-n, #phase-mask-function, #mathematical-modeling

## Why is the value of the phase-mask function arbitrary at the interface $\Sigma_{\mathrm{p}}$?

The phase-mask function value is arbitrary at the interface $\Sigma_{\mathrm{p}}$, often set to $\frac{1}{2}$ because this intermediate value simplifies the modeling of the phase boundary, even though $\gamma^{\mathrm{p}}(\xi, t)$ is defined only in an integral sense at discontinuities.

- #phase-boundary, #phase-mask-function, #mathematical-modeling

## How are governing equations for extended dependent variables $\mathbf{q}^{\mathrm{p}}$ derived using $\left(\gamma^{\mathrm{p}}\right)^{n}$?

Governing equations for extended dependent variables $\mathbf{q}^{\mathrm{p}}$ are derived by multiplying the respective equations and boundary conditions for each phase by $\left(\gamma^{\mathrm{p}}\right)^{n}$.

- #governing-equations, #dependent-variables, #phase-mask-function
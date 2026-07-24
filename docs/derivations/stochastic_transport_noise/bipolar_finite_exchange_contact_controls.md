# R06 bipolar finite-exchange contact controls

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #346  
**Scope:** dimensionless steady bipolar verification

## 1. Bulk conventional currents

The accepted dimensionless currents are

\[
j_n=d_n(\partial_xN-N\partial_x\psi),
\]

\[
j_p=-d_p(\partial_xP+P\partial_x\psi).
\]

Electron and hole conventional currents have different relations to particle flux, so their contact signs must be derived separately.

## 2. Outward particle exchange

For either carrier, the reduced classical exchange law is

\[
\nu\Gamma=S(c-c^{eq}),
\]

with outward normal `nu_L=-1` and `nu_R=+1`.

For electrons, `j_n=-q Gamma_n`, giving

\[
j_{n,L}=+S_{n,L}(N_L-N_L^{eq}),
\]

\[
j_{n,R}=-S_{n,R}(N_R-N_R^{eq}).
\]

For holes, `j_p=+q Gamma_p`, giving

\[
j_{p,L}=-S_{p,L}(P_L-P_L^{eq}),
\]

\[
j_{p,R}=+S_{p,R}(P_R-P_R^{eq}).
\]

The hole signs are therefore the opposite of the electron signs at each boundary.

## 3. Independent Biot controls

Define four dimensionless contact controls:

\[
Bi_{n,L}=\frac{S_{n,L}L}{D_n},\quad
Bi_{n,R}=\frac{S_{n,R}L}{D_n},
\]

\[
Bi_{p,L}=\frac{S_{p,L}L}{D_p},\quad
Bi_{p,R}=\frac{S_{p,R}L}{D_p}.
\]

They permit selective contacts: one carrier may be approximately ideal while the other is blocking or contact limited.

## 4. Exact zero-field currents

For zero field, zero screening, and no bulk source,

\[
j_n=\frac{D_n}{L}
\frac{N_R^{eq}-N_L^{eq}}
{1+Bi_{n,L}^{-1}+Bi_{n,R}^{-1}},
\]

\[
j_p=\frac{D_p}{L}
\frac{P_L^{eq}-P_R^{eq}}
{1+Bi_{p,L}^{-1}+Bi_{p,R}^{-1}}.
\]

The reversed density ordering in the hole numerator follows from `j_p=-D_p partial_x P` at zero field.

The exact profiles are linear:

\[
N(x)=N_L^{eq}+\frac{j_n}{S_{n,L}}+\frac{j_n}{D_n}x,
\]

\[
P(x)=P_L^{eq}-\frac{j_p}{S_{p,L}}-\frac{j_p}{D_p}x.
\]

## 5. Selective blocking

If either electron contact is exactly blocking, steady source-free electron current is zero. Hole current may remain finite if both hole contacts exchange.

Likewise, if either hole contact is blocking, steady source-free hole current is zero while electron current may remain finite.

With both contacts blocking for both carriers and zero screening, separate total electron and hole populations are conserved. The Jacobian therefore has two population null modes.

## 6. Total conventional current

For source-free steady transport,

\[
\partial_x j_n=0,\qquad \partial_x j_p=0,
\]

so

\[
\partial_x(j_n+j_p)=0.
\]

The implementation reports carrier-resolved boundary mismatches and the spatial variation of total conventional current independently.

## 7. Scientific boundary

This gate verifies signs, conservation, selective blocking, and ideal-reservoir reductions for a classical density-Robin closure. It does not specify metal/HgCdTe barriers, minority-carrier surface recombination, nonlinear electrochemical exchange, interface charge storage, or stochastic contact events.

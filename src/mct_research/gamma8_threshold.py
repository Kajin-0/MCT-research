"""Quadratic Gamma8 threshold kernel, with an explicit linear-term guard.

The result is conditional on an isolated quadratic valence maximum. It is
not applicable across a bulk-inversion-asymmetry linear splitting or to the
inverted HgTe continuum. Momenta and cell volume must use consistent units.
"""
import numpy as np
from numpy.polynomial.legendre import leggauss

from .sp3d5 import BONDS, bond_matrix


def quadratic_gamma8_matrices(model):
    """Return Gamma8's second-order coefficient in k_i k_j (a=1 units).

    The linear term is checked before eliminating remote states. The
    degenerate second-order resolvent contains all other binary bands.
    """
    sector = model.gamma_sectors()
    u = sector['states8']
    energies, states = np.linalg.eigh(model.bloch(np.zeros(3)))
    remote = np.abs(energies-sector['E8']) > 1e-7
    if np.sum(~remote) != 4:
        raise ValueError('An isolated Gamma8 quartet is required')
    resolvent = (states[:, remote]/(sector['E8']-energies[remote])) @ states[:, remote].conj().T
    first = np.zeros((3,36,36),dtype=complex)
    second = np.zeros((3,3,36,36),dtype=complex)
    for d in BONDS:
        hopping = bond_matrix(model.parameters,d)
        for i in range(3):
            first[i,:18,18:] += 1j*d[i]*hopping
            for j in range(3):
                second[i,j,:18,18:] -= d[i]*d[j]*hopping
    first[:,18:,:18] = first[:,:18,18:].conj().transpose(0,2,1)
    second[:,:,18:,:18] = second[:,:,:18,18:].conj().transpose(0,1,3,2)
    linear = np.array([u.conj().T @ h @ u for h in first])
    linear_norm = float(max(np.linalg.norm(h,ord=2) for h in linear))
    if linear_norm > 1e-10:
        raise ValueError('Nonzero Gamma8 linear term invalidates the quadratic-only limit')
    quadratic = np.array([[u.conj().T @ (.5*second[i,j]+first[i] @ resolvent @ first[j]) @ u
                           for j in range(3)] for i in range(3)])
    return quadratic,linear_norm


def angular_threshold_kernel(curvature, cell_volume, n_theta=24, n_phi=48):
    """Coefficient K of -G'(E_v+delta) ~ K/sqrt(delta).

    curvature(n) is the positive Hermitian alpha in H=E_v-q^2 alpha(n).
    Bloch integration uses cell_volume/(2 pi)^3. No cutoff or fitted DOS
    amplitude is introduced. A negative curvature is rejected.
    """
    if cell_volume <= 0 or n_theta < 2 or n_phi < 4:
        raise ValueError('Positive volume and adequate angular quadrature required')
    cosines,weights = leggauss(n_theta)
    result = None
    minimum,maximum = np.inf,-np.inf
    for cosine,weight in zip(cosines,weights):
        for phi in 2*np.pi*np.arange(n_phi)/n_phi:
            n = np.array([np.sqrt(1-cosine*cosine)*np.cos(phi),
                          np.sqrt(1-cosine*cosine)*np.sin(phi),cosine])
            alpha = np.asarray(curvature(n),dtype=complex)
            if not np.allclose(alpha,alpha.conj().T,atol=1e-10,rtol=1e-12):
                raise ValueError('Hermitian curvature required')
            eigen,vectors = np.linalg.eigh(alpha)
            if eigen.min() <= 0:
                raise ValueError('A quadratic valence maximum with positive curvatures is required')
            minimum,maximum = min(minimum,float(eigen.min())),max(maximum,float(eigen.max()))
            kernel = (vectors*eigen**(-1.5)) @ vectors.conj().T
            if result is None:
                result = np.zeros_like(kernel)
            result += weight*(2*np.pi/n_phi)*kernel
    return result*cell_volume/(32*np.pi**2),minimum,maximum

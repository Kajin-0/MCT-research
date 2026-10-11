"""Independent band, angular and radial checks of the threshold coefficient."""
import json
from pathlib import Path

import numpy as np
from scipy.integrate import quad
import pytest

from mct_research.gamma8_threshold import angular_threshold_kernel,quadratic_gamma8_matrices
from mct_research.sp3d5 import BinaryModel


def test_full_binary_bands_match_degenerate_second_order_curvature():
    parameters=json.loads((Path(__file__).resolve().parents[1]/'data/materials/schindler2012_sp3d5.json').read_text())
    model=BinaryModel(parameters['CdTe'])
    quadratic,linear_norm=quadratic_gamma8_matrices(model)
    assert linear_norm<1e-12
    edge=model.gamma_sectors()['E8']
    for n in [np.array([1.,0,0]),np.array([1.,1,0])/np.sqrt(2),np.ones(3)/np.sqrt(3)]:
        expected=np.linalg.eigvalsh(np.einsum('i,j,ijab->ab',n,n,quadratic))
        radius=1e-3
        energies=np.linalg.eigvalsh(model.bloch(radius*n))
        selected=np.sort(energies[np.argsort(np.abs(energies-edge))[:4]])
        # The [110] odd cubic splitting cancels in each pair's mean.
        actual=((selected-edge)/radius**2).reshape(2,2).mean(axis=1)
        np.testing.assert_allclose(actual,expected.reshape(2,2).mean(axis=1),atol=1.2e-6)


def test_spin_three_halves_projectors_give_half_each_spherical_coefficient():
    raising=np.diag([np.sqrt(3),2,np.sqrt(3)],1).astype(complex)
    j=np.array([(raising+raising.T)/2,(raising-raising.T)/(2j),np.diag([1.5,.5,-.5,-1.5])])
    heavy,light,volume=.3,2.1,.25
    def curvature(n):
        angular=np.einsum('i,iab->ab',n,j)
        heavy_projector=(angular@angular-.25*np.eye(4))/2
        return light*np.eye(4)+(heavy-light)*heavy_projector
    kernel,_,_=angular_threshold_kernel(curvature,volume,n_theta=8,n_phi=16)
    expected=volume/(16*np.pi)*(heavy**-1.5+light**-1.5)
    np.testing.assert_allclose(kernel,expected*np.eye(4),atol=2e-15)


def test_radial_green_integral_sets_fourier_normalization_and_exponent():
    alpha,volume=1.7,.25
    delta=1e-5
    # Integrate the actual squared-resolvent radial measure, including the
    # 4 pi angular measure, instead of evaluating the coefficient formula.
    radial,error=quad(lambda q:q*q/(delta+alpha*q*q)**2,0,np.inf,epsabs=1e-9)
    numerical=volume*4*np.pi/(2*np.pi)**3*radial*np.sqrt(delta)
    kernel,_,_=angular_threshold_kernel(lambda n:np.eye(1)*alpha,volume,n_theta=4,n_phi=8)
    np.testing.assert_allclose(kernel[0,0].real,numerical,rtol=2e-10)
    assert error<1e-6
    with pytest.raises(ValueError,match='positive curvatures'):
        angular_threshold_kernel(lambda n:np.diag([alpha,-alpha]),volume,n_theta=4,n_phi=8)

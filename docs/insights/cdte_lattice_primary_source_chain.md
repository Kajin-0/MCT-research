# CdTe lattice primary-source chain

## Question

Do Williams 1969, Smith and White 1975, and Horning and Staudenmann 1986 close the physical lattice gate for a validated 0 K CdTe calculation?

## Source identities

- Williams et al. 1969, DOI `10.1016/0038-1098(69)90296-8`, PDF SHA-256 `963891204abd0b3c434297eec3a1d337c7bc67a3b937eda4bdfc373746702bab`.
- Smith and White 1975, DOI `10.1088/0022-3719/8/13/012`, PDF SHA-256 `521e58912b46c6fba70f6e7c24135d79e8aa50d8ddc93addbaf97c4d38f74237`.
- Horning and Staudenmann 1986, DOI `10.1103/PhysRevB.34.3970`, PDF SHA-256 `c94207304b5967f4d955f0440c19589901f32404ad932368521971c30a2bfef9`.

## Absolute anchor

Williams measured 99.999 percent CdTe by X-ray powder diffraction from 20 to 420 C. Its fitted polynomial gives

```text
a(20 C) = 6.480841894 A
```

while the observed Table I value is `6.4809 A`. The maximum observed-minus-polynomial residual over the nine rows is `0.000418 A`. Combining that envelope conservatively with the stated `+-5 C` temperature-control bound gives an anchor bound of about `0.000579 A`.

The Table I calculated value `6.4827 A` at 206 C is a printing error. The published polynomial gives `6.4871809 A`, consistent with the observed `6.4870 A`.

## Low-temperature expansion

Smith and White provide primary capacitance-dilatometer measurements below 33 K, between 55 and 90 K, and at room temperature. Their CdTe2 result below 4 K is

```text
alpha(T) = -(170 +- 10) x 10^-12 T^3 K^-1.
```

Table II directly constrains the negative-expansion minimum and gives `alpha(85 K)=1.57e-6 K^-1` and a room-temperature value `alpha(283 K)=4.70e-6 K^-1`. The 57.5 and 65 K entries are explicitly literature values reprinted in parentheses.

## Horning boundary

Horning states `6.484 A at room temperature` in a figure caption, but the article is an intensity/vibrational study. It does not provide a traceable lattice-parameter extraction or uncertainty for that number. It is a contextual cross-check, not an admissible absolute anchor.

## Provisional 0 K diagnostic

Using Williams at 293.15 K, Smith and White through 85 K, a linear central bridge from 85 to 283 K, and monotone endpoint bounds for that unmeasured bridge gives

```text
a0 central = 6.477028 A
bounded range = 6.474443 to 6.479614 A
```

The range is not a confidence interval. It is a fail-closed envelope dominated by the missing 90-293 K primary integral.

## Decision

```text
The absolute room-temperature anchor is closed.
The low-temperature sign and curvature are closed.
The validated 0 K lattice gate remains open.
```

Do not populate `cdte_a0_run_spec.json` and do not set `ready_for_execution=true` from this diagnostic.

The next primary acquisitions are:

- Browder and Ballard, Applied Optics 11, 841-843 (1972), DOI `10.1364/AO.11.000841`;
- Greenough and Palmer, Journal of Physics D 6, 587-592 (1973), DOI `10.1088/0022-3727/6/5/315`.

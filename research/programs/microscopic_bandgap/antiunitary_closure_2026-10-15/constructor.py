"""Kramers-paired subspace cover. No occupation editing and no native launch."""
import numpy as np


def paired_cover(S, theta, tolerance=1e-10):
    """Return a Theta-invariant cover, with a measured residual certificate.

    This greedy construction is not claimed to minimize approximate dimension.
    Its exact-arithmetic range lies in S+ThetaS; each added pair is orthonormal.
    Floating residual and Gram certificates, rather than symbolic claims, gate
    use of its result. Theta must be an isometric antiunitary with square -I.
    """
    rows, columns = S.shape
    Q = np.empty((rows, 0), dtype=complex)
    R = S.copy()
    history = []
    for step in range(columns+1):
        if step % 8 == 0 or step == columns:
            R = S-Q@(Q.conj().T@S)
            error = float(np.linalg.norm(R, 2))
            history.append(dict(pairs=step, dimension=2*step, source_cover_op=error))
            if error <= tolerance:
                return Q, history
        if step == columns:
            raise ArithmeticError('no certified cover within doubled dimension')
        j = int(np.argmax(np.sum(abs(R)**2, axis=0)))
        q = R[:, j].copy()
        for _ in range(2):
            q -= Q@(Q.conj().T@q)
        norm = np.linalg.norm(q)
        if norm < 1e-14:
            raise ArithmeticError('unresolved floating direction; no silent rank drop')
        q /= norm
        pair = np.column_stack((q, theta(q[:, None])[:, 0]))
        Q = np.column_stack((Q, pair))
        R -= pair@(pair.conj().T@R)
    raise AssertionError('unreachable')

"""Pure reference mathematics for Cheng (2019), equations 16 and 22--25.

Forces and positions MUST be expressed in the same frame, positions in metres,
forces in N (or explicitly designated virtual N). Wrench order is [F, moment].
These helpers neither establish sensor validity nor authorize robot commands.
"""
from math import isfinite, sqrt


def vector(x, n=3):
    x = tuple(float(v) for v in x)
    if len(x) != n or not all(isfinite(v) for v in x):
        raise ValueError('wrong dimension or nonfinite vector')
    return x


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    a, b = vector(a), vector(b)
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def rotation(r):
    r = tuple(vector(row) for row in r)
    if len(r) != 3 or any(abs(dot(a, b) - (i == j)) > 1e-8
                         for i, a in enumerate(r) for j, b in enumerate(r)):
        raise ValueError('rotation must be orthonormal')
    if abs(dot(r[0], cross(r[1], r[2])) - 1) > 1e-8:
        raise ValueError('reflection is not a proper rotation')
    return r


def rotate(r, x):
    r, x = rotation(r), vector(x)
    return tuple(dot(row, x) for row in r)


def aggregate(contacts):
    """Sum (position_from_link_origin_m, force_in_link_axes) pairs.

    Empty contacts produce zero; callers must distinguish this from unavailable
    coverage. Individual contacts must also be retained for collision handling.
    """
    forces = [0.] * 3
    moments = [0.] * 3
    for p, f in contacts:
        p, f = vector(p), vector(f)
        moment = cross(p, f)
        for k in range(3):
            forces[k] += f[k]
            moments[k] += moment[k]
    return tuple(forces + moments)


def change_axes(wrench, r):
    """Rotate axes only, retaining the SAME physical reference origin."""
    w = vector(wrench, 6)
    return rotate(r, w[:3]) + rotate(r, w[3:])


def shift_origin(wrench, old_origin_from_new):
    """Same axes, new reference point: M_new=M_old+(O_old-O_new) x F."""
    w, arm = vector(wrench, 6), vector(old_origin_from_new)
    extra = cross(arm, w[:3])
    return w[:3] + tuple(w[k+3] + extra[k] for k in range(3))


def project(jacobian, wrench):
    """J rows [linear velocity; angular velocity], same axes/origin as wrench."""
    w = vector(wrench, 6)
    rows = tuple(tuple(float(v) for v in row) for row in jacobian)
    if len(rows) != 6 or not rows[0] or any(len(row) != len(rows[0]) for row in rows):
        raise ValueError('Jacobian must have 6 rows and at least 1 column')
    if not all(isfinite(x) for row in rows for x in row):
        raise ValueError('nonfinite Jacobian')
    return tuple(sum(row[j] * w[k] for k, row in enumerate(rows)) for j in range(len(rows[0])))


def virtual_force(intensity, outward_normal, gain, cap):
    """Compressive inward virtual effort; gain/cap are engineering settings.

    This converts normalized intensity into a command surrogate, NOT a measured
    physical contact force. No call is permitted for an invalid/unknown cell.
    """
    n = vector(outward_normal)
    if not all(isfinite(x) for x in (intensity, gain, cap)) or not 0 <= intensity <= 254 or gain < 0 or cap < 0:
        raise ValueError('invalid intensity/gain/cap')
    if abs(sqrt(dot(n, n)) - 1) > 1e-8:
        raise ValueError('normal must be unit length')
    magnitude = min(cap, gain * intensity / 254)
    return tuple(-magnitude * x for x in n)

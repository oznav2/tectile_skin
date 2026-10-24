#!/usr/bin/env python3
"""Combine measured masses and inertia tensors in a common coordinate frame.

No robot-model file is modified. Units: kg, m, kg*m^2.
"""
import math


def _vector(value):
    if len(value) != 3 or not all(math.isfinite(x) for x in value):
        raise ValueError('finite three-component vector required')


def point_mass_delta(mass_kg, position_m):
    """Parallel-axis contribution m * ((r dot r) I - r r^T)."""
    if not math.isfinite(mass_kg) or mass_kg <= 0:
        raise ValueError('positive finite measured mass required')
    _vector(position_m)
    r2 = sum(x*x for x in position_m)
    return [[mass_kg*((r2 if i == j else 0)-position_m[i]*position_m[j])
             for j in range(3)] for i in range(3)]


def _body(body):
    point_mass_delta(body['mass_kg'], body['com_m'])
    tensor = body['inertia_at_com']
    if len(tensor) != 3:
        raise ValueError('3x3 inertia tensor required')
    for row in tensor:
        _vector(row)
    scale = max(1e-12, max(abs(v) for row in tensor for v in row))
    tolerance = 1e-9 * scale
    for i in range(3):
        if tensor[i][i] < -tolerance:
            raise ValueError('inertia diagonal must be nonnegative')
        for j in range(3):
            if abs(tensor[i][j]-tensor[j][i]) > tolerance:
                raise ValueError('inertia tensor must be symmetric')
    # A physical inertia tensor corresponds to a positive-semidefinite second
    # moment matrix Q = 0.5 trace(I) identity - I. Checking all its principal
    # minors also catches triangle-inequality failures in rotated principal axes.
    half_trace = sum(tensor[i][i] for i in range(3))/2
    second = [[(half_trace if i == j else 0)-tensor[i][j] for j in range(3)] for i in range(3)]
    for i in range(3):
        if second[i][i] < -tolerance:
            raise ValueError('inertia violates the physical triangle inequality')
    for i, j in ((0,1), (0,2), (1,2)):
        if second[i][i]*second[j][j]-second[i][j]**2 < -1e-9*scale**2:
            raise ValueError('inertia is not physically realizable')
    a, b, c = second[0]
    d, e, f = second[1]
    g, h, k = second[2]
    determinant = a*(e*k-f*h)-b*(d*k-f*g)+c*(d*h-e*g)
    if determinant < -1e-9*scale**3:
        raise ValueError('inertia is not physically realizable')


def combine_link(original_mass, original_com, original_inertia_at_com, additions):
    """Return combined mass, COM and inertia at the combined COM.

    All vectors/tensors must already be expressed in the SAME parent-body axes.
    Inertia tensors are about each item's own COM, not about the frame origin.
    Rotate each tensor into the common axes before calling. A zero intrinsic
    tensor is a point-mass approximation and must be justified by the caller.
    Moving cable loops require a configuration-dependent model or measured bounds.
    """
    items = [{'mass_kg': original_mass, 'com_m': original_com,
              'inertia_at_com': original_inertia_at_com}] + list(additions)
    for item in items:
        _body(item)
    total = sum(item['mass_kg'] for item in items)
    com = [sum(item['mass_kg']*item['com_m'][i] for item in items)/total for i in range(3)]
    inertia = [[0.0]*3 for _ in range(3)]
    for item in items:
        delta = point_mass_delta(item['mass_kg'], [item['com_m'][i]-com[i] for i in range(3)])
        for i in range(3):
            for j in range(3):
                inertia[i][j] += item['inertia_at_com'][i][j] + delta[i][j]
    return {'mass_kg': total, 'com_m': com, 'inertia_at_com': inertia}

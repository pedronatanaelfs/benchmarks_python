"""Placeholder for MPDMP Octave equivalence.

MATLAB MPDMP classes require PlatEMO-style ``PROBLEM`` / ``nsidedpoly``
(Mapping Toolbox). GNU Octave does not provide those. Equivalence for MPDMP
is therefore analytical / geometry-based (see validation/audits/).
"""

import pytest

pytestmark = pytest.mark.skip(
    reason="MPDMP MATLAB classes need PlatEMO/nsidedpoly; OCTAVE_INCOMPATIBLE for full classdefs"
)


def test_mpdmp_octave_equivalence() -> None:
    assert False

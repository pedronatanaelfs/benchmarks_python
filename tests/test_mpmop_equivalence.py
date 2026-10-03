"""Placeholder: MATLAB/Octave equivalence requires GNU Octave.

Status: OCTAVE_NOT_INSTALLED in this environment.
"""

import pytest


@pytest.mark.skip(reason="GNU Octave not installed; see validation/validation_report.md")
def test_mpmop_octave_equivalence() -> None:
    assert False


@pytest.mark.skip(reason="GNU Octave not installed; see validation/validation_report.md")
def test_mpdmp_octave_equivalence() -> None:
    assert False

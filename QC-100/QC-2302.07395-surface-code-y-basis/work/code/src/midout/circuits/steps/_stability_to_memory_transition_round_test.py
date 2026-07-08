import itertools

import pytest

from midout.circuits.steps._stability_to_memory_transition_round import make_memory_to_stability_transition_round


@pytest.mark.parametrize("d,b", itertools.product(
    range(2, 10),
    ["X", "Z"],
))
def test_make_memory_to_stability_transition_round(d: int, b: str):
    make_memory_to_stability_transition_round(distance=d, basis=b).verify()
    make_memory_to_stability_transition_round(distance=d, basis=b).inverted().verify()

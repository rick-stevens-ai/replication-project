import itertools

import pytest
import stim

from midout import gen
from midout._make_circuit import make_circuit


@pytest.mark.parametrize("distance,basis", itertools.product(
    range(2, 10),
    'XYZ',
))
def test_idle_circuits(distance: int, basis: str):
    circuit = make_circuit(
        basis=basis + '_magic_idle',
        distance=distance,
        noise=gen.NoiseModel.si1000(1e-3),
        boundary_rounds=0,
        memory_rounds=3,
        verify_chunks=True,
    )

    dem = circuit.detector_error_model(decompose_errors=True, block_decomposition_from_introducing_remnant_edges=True)
    assert dem is not None

    actual_distance = len(circuit.shortest_graphlike_error())
    expected_distance = distance
    assert actual_distance == expected_distance

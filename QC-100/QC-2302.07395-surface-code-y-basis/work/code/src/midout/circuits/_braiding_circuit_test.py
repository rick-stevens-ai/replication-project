import pytest

from midout import gen
from midout.circuits._braiding_circuit import make_y_braiding_experiment_chunks
from midout._make_circuit import make_circuit


@pytest.mark.parametrize("distance", range(2, 8))
def test_make_y_braiding_experiment_chunks(distance: int):
    circuit = make_circuit(
        basis='Y_braid',
        distance=distance,
        noise=gen.NoiseModel.uniform_depolarizing(1e-3),
        boundary_rounds=distance // 2,
        memory_rounds=5,
        verify_chunks=True,
    )

    dem = circuit.detector_error_model(decompose_errors=True, block_decomposition_from_introducing_remnant_edges=True)
    assert dem is not None

    actual_distance = len(circuit.shortest_graphlike_error())
    expected_distance = distance
    assert actual_distance == expected_distance


def test_have_all_detectors():
    chunks = make_y_braiding_experiment_chunks(
        distance=5,
        memory_rounds=3,
        boundary_rounds=3,
    )
    for e in chunks:
        e.verify()
    c = gen.compile_chunks_into_circuit(chunks)
    c.detector_error_model()
    gen.verify_circuit_has_all_possible_detectors(c)

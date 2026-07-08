import pytest

from midout import gen
from midout._make_circuit import make_circuit
from midout.circuits.steps._folded_y import folded_x2y_chunk


@pytest.mark.parametrize("d", range(2, 10))
def test_folded_x2y_chunk(d: int):
    folded_x2y_chunk(distance=d, init=False).verify()


@pytest.mark.parametrize("d", range(2, 10))
def test_folded_x2y_chunk_init(d: int):
    folded_x2y_chunk(distance=d, init=True).verify()


@pytest.mark.parametrize("d", range(2, 10))
def test_circuit(d: int):
    circuit = make_circuit(
        basis="Y_folded",
        distance=d,
        memory_rounds=d,
        boundary_rounds=0,
        noise=gen.NoiseModel.uniform_depolarizing(1e-3),
    )
    assert len(circuit.shortest_graphlike_error()) == d

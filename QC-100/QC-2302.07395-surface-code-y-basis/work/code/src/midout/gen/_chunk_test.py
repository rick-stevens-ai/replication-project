from typing import Iterable, Dict, Callable

import stim

from midout import gen


def test_inverse_flows():
    chunk = gen.Chunk(
        circuit=stim.Circuit("""
            R 0 1 2 3 4
            CX 2 0
            M 0
        """),
        q2i={0: 0, 1: 1, 2: 2, 3: 3, 4: 4},
        flows=[
            gen.Flow(
                center=0,
                start=gen.PauliString({}),
                measurement_indices=[0],
                end=gen.PauliString({1: 'Z'}),
            ),
        ],
    )

    inverted = chunk.inverted()
    inverted.verify()
    assert len(inverted.flows) == len(chunk.flows)
    assert inverted.circuit == stim.Circuit("""
        R 0
        CX 2 0
        M 4 3 2 1 0
    """)


def test_inverse_circuit():
    chunk = gen.Chunk(
        circuit=stim.Circuit("""
            R 0 1 2 3 4
            CX 2 0 3 4
            X 1
            M 0
        """),
        q2i={0: 0, 1: 1, 2: 2, 3: 3, 4: 4},
        flows=[],
    )

    inverted = chunk.inverted()
    inverted.verify()
    assert len(inverted.flows) == len(chunk.flows)
    assert inverted.circuit == stim.Circuit("""
        R 0
        X 1
        CX 3 4 2 0
        M 4 3 2 1 0
    """)

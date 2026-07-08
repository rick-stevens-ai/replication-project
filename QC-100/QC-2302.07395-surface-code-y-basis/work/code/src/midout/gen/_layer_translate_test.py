import stim

from midout.gen._layer_translate import LayerCircuit, to_z_basis_interaction_circuit, _basis_before_rotation, R_ZXY


def test_to_cz_circuit_rotation_folding():
    assert to_z_basis_interaction_circuit(stim.Circuit("""
    """)) == stim.Circuit("""
    """)

    assert to_z_basis_interaction_circuit(stim.Circuit("""
        C_XYZ 0
        TICK
        M 0 1 2 3
    """)) == stim.Circuit("""
        C_XYZ 0
        TICK
        M 0 1 2 3
    """)

    assert to_z_basis_interaction_circuit(stim.Circuit("""
        I 0
        TICK
        C_XYZ 0
        TICK
        M 0 1 2 3
    """)) == stim.Circuit("""
        C_XYZ 0
        TICK
        M 0 1 2 3
    """)

    assert to_z_basis_interaction_circuit(stim.Circuit("""
        C_XYZ 0
        TICK
        I 0
        TICK
        M 0 1 2 3
    """)) == stim.Circuit("""
        C_XYZ 0
        TICK
        M 0 1 2 3
    """)

    assert to_z_basis_interaction_circuit(stim.Circuit("""
        H 0
        TICK
        H 0
        TICK
        M 0 1 2 3
    """)) == stim.Circuit("""
        M 0 1 2 3
    """)

    assert to_z_basis_interaction_circuit(stim.Circuit("""
        H 0 1 2 3 4 5
        TICK
        I 0
        H_YZ 1
        H_XY 2
        C_XYZ 3
        C_ZYX 4
        H 5
        TICK
        M 0 1 2 3
    """)) == stim.Circuit("""
        C_XYZ 1
        C_ZYX 2
        H 0
        S 4
        SQRT_X 3
        TICK
        M 0 1 2 3
    """)

    assert to_z_basis_interaction_circuit(stim.Circuit("""
        H_XY 0 1 2 3 4 5
        TICK
        I 0
        H_YZ 1
        H_XY 2
        C_XYZ 3
        C_ZYX 4
        H 5
        TICK
        M 0 1 2 3
    """)) == stim.Circuit("""
        C_XYZ 5
        C_ZYX 1
        H 3
        S 0
        SQRT_X 4
        TICK
        M 0 1 2 3
    """)

    assert to_z_basis_interaction_circuit(stim.Circuit("""
        H_YZ 0 1 2 3 4 5
        TICK
        I 0
        H_YZ 1
        H_XY 2
        C_XYZ 3
        C_ZYX 4
        H 5
        TICK
        M 0 1 2 3
    """)) == stim.Circuit("""
        C_XYZ 2
        C_ZYX 5
        H 4
        S 3
        SQRT_X 0
        TICK
        M 0 1 2 3
    """)

    assert to_z_basis_interaction_circuit(stim.Circuit("""
        C_XYZ 0 1 2 3 4 5
        TICK
        I 0
        H_YZ 1
        H_XY 2
        C_XYZ 3
        C_ZYX 4
        H 5
        TICK
        M 0 1 2 3
    """)) == stim.Circuit("""
        C_XYZ 0
        C_ZYX 3
        H 1
        S 5
        SQRT_X 2
        TICK
        M 0 1 2 3
    """)

    assert to_z_basis_interaction_circuit(stim.Circuit("""
        C_ZYX 0 1 2 3 4 5
        TICK
        I 0
        H_YZ 1
        H_XY 2
        C_XYZ 3
        C_ZYX 4
        H 5
        TICK
        M 0 1 2 3
    """)) == stim.Circuit("""
        C_XYZ 4
        C_ZYX 0
        H 2
        S 1
        SQRT_X 5
        TICK
        M 0 1 2 3
    """)

    assert to_z_basis_interaction_circuit(stim.Circuit("""
        I 0 1 2 3 4 5
        TICK
        I 0
        H_YZ 1
        H_XY 2
        C_XYZ 3
        C_ZYX 4
        H 5
        TICK
        M 0 1 2 3
    """)) == stim.Circuit("""
        C_XYZ 3
        C_ZYX 4
        H 5
        S 2
        SQRT_X 1
        TICK
        M 0 1 2 3
    """)


def test_basis_before_rotation():
    assert _basis_before_rotation('X', R_ZXY) == 'Y'
    assert _basis_before_rotation('Y', R_ZXY) == 'Z'
    assert _basis_before_rotation('Z', R_ZXY) == 'X'


def test_to_cz_circuit_loop_boundary_folding():
    assert to_z_basis_interaction_circuit(stim.Circuit("""
        H 2
        TICK
        CX rec[-1] 2 
        TICK
        S 2
        TICK
        M 0 1 2 3
    """)) == stim.Circuit("""
        CZ rec[-1] 2
        C_ZYX 2 
        TICK
        M 0 1 2 3
    """)

    assert to_z_basis_interaction_circuit(stim.Circuit("""
        MRX 0
        DETECTOR rec[-1]
        TICK
        M 0
        TICK
        H 0
    """)) == stim.Circuit("""
        H 0
        TICK
        M 0
        TICK
        R 0
        DETECTOR rec[-1]
        TICK
        H 0
        TICK
        M 0
    """)

    assert to_z_basis_interaction_circuit(stim.Circuit("""
        REPEAT 100 {
            C_XYZ 0
            TICK
            CZ 0 1
            TICK
            H 0
            TICK
        }
        M 0
    """)) == stim.Circuit("""
        C_XYZ 0
        TICK
        REPEAT 100 {
            CZ 0 1
            TICK
            SQRT_X 0
            TICK
        }
        C_ZYX 0
        TICK
        M 0
    """)


def test_to_cz_circuit_from_cnot():
    assert to_z_basis_interaction_circuit(stim.Circuit("""
        CX 0 1 2 3
        TICK
        CX 1 0 2 3
        TICK
        M 0 1 2 3
    """)) == stim.Circuit("""
        H 1 3
        TICK
        CZ 0 1 2 3
        TICK
        H 0 1
        TICK
        CZ 0 1 2 3
        TICK
        H 0 3
        TICK
        M 0 1 2 3
    """)


def test_to_cz_circuit_from_swap_cnot():
    assert to_z_basis_interaction_circuit(stim.Circuit("""
        CNOT 0 1
        TICK
        SWAP 0 1
        TICK
        M 0 1 2 3
    """)) == stim.Circuit("""
        H 1
        TICK
        ISWAP 0 1
        TICK
        C_XYZ 0
        S 1
        TICK
        M 0 1 2 3
    """)

    assert to_z_basis_interaction_circuit(stim.Circuit("""
        CNOT 0 1
        TICK
        SWAP 1 0
        TICK
        M 0 1 2 3
    """)) == stim.Circuit("""
        H 1
        TICK
        ISWAP 0 1
        TICK
        C_XYZ 0
        S 1
        TICK
        M 0 1 2 3
    """)

    assert to_z_basis_interaction_circuit(stim.Circuit("""
        SWAP 1 0
        TICK
        CNOT 1 0
        TICK
        M 0 1 2 3
    """)) == stim.Circuit("""
        H 1
        TICK
        ISWAP 0 1
        TICK
        C_XYZ 0
        S 1
        TICK
        M 0 1 2 3
    """)

    assert to_z_basis_interaction_circuit(stim.Circuit("""
        SWAP 0 1
        TICK
        CNOT 1 0
        TICK
        M 0 1 2 3
    """)) == stim.Circuit("""
        H 1
        TICK
        ISWAP 0 1
        TICK
        C_XYZ 0
        S 1
        TICK
        M 0 1 2 3
    """)

    assert to_z_basis_interaction_circuit(stim.Circuit("""
        CNOT 1 0
        TICK
        SWAP 0 1
        TICK
        M 0 1 2 3
    """)) == stim.Circuit("""
        H 0
        TICK
        ISWAP 0 1
        TICK
        C_XYZ 1
        S 0
        TICK
        M 0 1 2 3
    """)

    assert to_z_basis_interaction_circuit(stim.Circuit("""
        SWAP 0 1
        TICK
        CNOT 0 1
        TICK
        M 0 1 2 3
    """)) == stim.Circuit("""
        H 0
        TICK
        ISWAP 0 1
        TICK
        C_XYZ 1
        S 0
        TICK
        M 0 1 2 3
    """)


def test_with_squashed_rotations():
    assert LayerCircuit.from_stim_circuit(stim.Circuit("""
        S 0 1 2 3
        TICK
        CZ 1 2
        TICK
        H 0 3
        TICK
        CZ 1 2
        TICK
        S 0 1 2 3
    """)).with_squashed_rotations().to_stim_circuit() == stim.Circuit("""
        C_XYZ 0 3
        S 1 2
        TICK
        CZ 1 2
        TICK
        CZ 1 2
        TICK
        S 0 1 2 3
    """)

    assert LayerCircuit.from_stim_circuit(stim.Circuit("""
        S 0 1 2 3
        TICK
        CZ 0 2
        TICK
        H 0 3
        TICK
        CZ 1 2
        TICK
        S 0 1 2 3
    """)).with_squashed_rotations().to_stim_circuit() == stim.Circuit("""
        C_XYZ 3
        S 0 1 2
        TICK
        CZ 0 2
        TICK
        CZ 1 2
        TICK
        C_ZYX 0
        S 1 2 3
    """)


def test_with_rotations_before_resets_removed():
    # assert LayerCircuit.from_stim_circuit(stim.Circuit("""
    #     H 0 1 2 3
    #     TICK
    #     R 0 1
    #     TICK
    # """)).with_rotations_before_resets_removed().to_stim_circuit() == stim.Circuit("""
    #     H 2 3
    #     TICK
    #     R 0 1
    #     TICK
    # """)

    assert LayerCircuit.from_stim_circuit(stim.Circuit("""
        H 0 1 2 3
        TICK
        REPEAT 100 {
            R 0 1
            TICK
            H 0 1 2 3
            TICK
        }
        R 1 2
        TICK
    """)).with_rotations_before_resets_removed().to_stim_circuit() == stim.Circuit("""
        H 2 3
        TICK
        REPEAT 100 {
            R 0 1
            TICK
            H 0 2 3
            TICK
        }
        R 1 2
    """)


def test_with_rotations_merged_earlier():
    assert LayerCircuit.from_stim_circuit(stim.Circuit("""
        S 0 1 2 3
        TICK
        CZ 1 2 3 4
        TICK
        H 0 1 2 3
        TICK
        CZ 1 2
        TICK
        S 0 1 2 3
    """)).with_rotations_merged_earlier().to_stim_circuit() == stim.Circuit("""
        S 1 2 3
        SQRT_X 0
        TICK
        CZ 1 2 3 4
        TICK
        C_ZYX 3
        H 1 2
        TICK
        CZ 1 2
        TICK
        S 1 2
    """)

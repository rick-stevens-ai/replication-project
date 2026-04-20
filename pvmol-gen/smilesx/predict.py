"""Inference: load a trained model and classify new SMILES."""

import os
from typing import List, Optional, Tuple

import numpy as np
import torch

from .model import LSTMAttModel
from .tokenizer import SmilesTokenizer
from .augment import augment_smiles


def load_model(
    model_dir: str,
    fold: int = 0,
    device: Optional[str] = None,
    embed_dim: int = 512,
    lstm_units: int = 128,
    tdense_units: int = 128,
    dense_depth: int = 0,
) -> Tuple[LSTMAttModel, SmilesTokenizer]:
    """Load a trained model and its tokenizer.

    Parameters
    ----------
    model_dir : str
        Directory containing model_fold_*.pt and vocab.txt
    fold : int
        Which fold's model to load
    device : str, optional
        Device to load to

    Returns
    -------
    model, tokenizer
    """
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    device = torch.device(device)

    tokenizer = SmilesTokenizer.load(os.path.join(model_dir, "vocab.txt"))

    # We need max_length from the saved model's state dict
    model_path = os.path.join(model_dir, f"model_fold_{fold}.pt")
    state = torch.load(model_path, map_location=device, weights_only=True)

    # Infer max_length from attention layer bias shape
    max_length = state["attention.b"].shape[0]

    model = LSTMAttModel(
        vocab_size=tokenizer.vocab_size,
        max_length=max_length,
        embed_dim=embed_dim,
        lstm_units=lstm_units,
        tdense_units=tdense_units,
        dense_depth=dense_depth,
        model_type="classification",
    )
    model.load_state_dict(state)
    model.to(device)
    model.eval()

    return model, tokenizer


def predict(
    smiles_list: List[str],
    model: LSTMAttModel,
    tokenizer: SmilesTokenizer,
    threshold: float = 0.47,
    augment: bool = True,
    device: Optional[str] = None,
    batch_size: int = 64,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Predict class probabilities and labels for a list of SMILES.

    Parameters
    ----------
    smiles_list : list of str
    model : trained LSTMAttModel
    tokenizer : fitted SmilesTokenizer
    threshold : float
        Classification threshold (paper uses 0.47)
    augment : bool
        If True, average predictions over augmented variants
    device : str, optional
    batch_size : int

    Returns
    -------
    probs : np.ndarray (N,) — mean predicted probability per molecule
    preds : np.ndarray (N,) — binary predictions (0 or 1)
    stds : np.ndarray (N,) — std of predictions across augmented variants
    """
    if device is None:
        dev = next(model.parameters()).device
    else:
        dev = torch.device(device)

    # Get max_length from model
    max_length = model.attention.b.shape[0]

    # Augment
    aug_smiles, _, group_ids = augment_smiles(smiles_list, augment=augment)

    # Encode
    X = tokenizer.encode_batch(aug_smiles, max_length)
    X_tensor = torch.from_numpy(X).long().to(dev)

    # Predict in batches
    all_probs = []
    model.eval()
    with torch.no_grad():
        for i in range(0, len(X_tensor), batch_size):
            batch = X_tensor[i : i + batch_size]
            out = model(batch)
            all_probs.append(out.cpu().numpy().ravel())

    raw_probs = np.concatenate(all_probs)

    # Average by original molecule
    n_orig = len(smiles_list)
    probs = np.zeros(n_orig)
    stds = np.zeros(n_orig)
    for i in range(n_orig):
        mask = [j for j, g in enumerate(group_ids) if g == i]
        if mask:
            probs[i] = raw_probs[mask].mean()
            stds[i] = raw_probs[mask].std()
        else:
            probs[i] = 0.0
            stds[i] = 0.0

    preds = (probs >= threshold).astype(int)
    return probs, preds, stds

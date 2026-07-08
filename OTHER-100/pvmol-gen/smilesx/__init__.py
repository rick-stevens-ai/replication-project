"""SMILES-X PyTorch — BiLSTM + Attention classifier for SMILES strings."""

__version__ = "0.1.0"

from .model import LSTMAttModel, SoftAttention
from .tokenizer import SmilesTokenizer
from .augment import enumerate_smiles, augment_smiles
from .train import SmilesXClassifier

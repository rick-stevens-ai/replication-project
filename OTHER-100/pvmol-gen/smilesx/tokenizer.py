"""SMILES tokenization — character-level with special tokens.

Faithfully reproduces the tokenization from SMILES-X (token.py).
"""

import re
from typing import List, Optional, Dict, Set

import numpy as np


# Regex pattern matching SMILES tokens (atoms, bonds, branches, rings, brackets)
_SMILES_PATTERN = re.compile(
    r"(\*|"
    r"N|O|S|P|F|Cl?|Br?|I|"          # aliphatic
    r"b|c|n|o|s|p|j|"                  # aromatic + join token
    r"\[.*?\]|"                         # bracketed atoms
    r"-|=|#|\$|:|/|\\|\.|"             # bonds
    r"[0-9]|%[0-9]{2}|"               # ring closures
    r"\(|\))"                           # branches
)

PAD_TOKEN = "pad"
UNK_TOKEN = "unk"
START_END_TOKEN = " "  # space used as start/end delimiter in original


class SmilesTokenizer:
    """Character-level SMILES tokenizer compatible with the original SMILES-X."""

    def __init__(self):
        self.vocab: List[str] = []
        self.token_to_idx: Dict[str, int] = {}
        self.idx_to_token: Dict[int, str] = {}
        self._fitted = False

    def tokenize(self, smiles: str) -> List[str]:
        """Tokenize a single SMILES string. Returns list of tokens wrapped with spaces."""
        tokens = _SMILES_PATTERN.findall(smiles)
        if not tokens:
            return [None]
        return [START_END_TOKEN] + tokens + [START_END_TOKEN]

    def tokenize_batch(self, smiles_list: List[str]) -> List[List[str]]:
        """Tokenize a batch of SMILES strings."""
        return [self.tokenize(s) for s in smiles_list]

    def fit(self, smiles_list: List[str]) -> "SmilesTokenizer":
        """Build vocabulary from a list of SMILES strings."""
        all_tokens: Set[str] = set()
        for smiles in smiles_list:
            tokens = self.tokenize(smiles)
            if tokens[0] is not None:
                all_tokens.update(tokens)

        # Sort for reproducibility, then prepend special tokens
        self.vocab = [PAD_TOKEN, UNK_TOKEN] + sorted(all_tokens)
        self.token_to_idx = {t: i for i, t in enumerate(self.vocab)}
        self.idx_to_token = {i: t for i, t in enumerate(self.vocab)}
        self._fitted = True
        return self

    def encode(self, smiles: str, max_length: int) -> np.ndarray:
        """Encode a single SMILES to a padded integer vector."""
        tokens = self.tokenize(smiles)
        return self._encode_tokens(tokens, max_length)

    def encode_batch(self, smiles_list: List[str], max_length: Optional[int] = None) -> np.ndarray:
        """Encode a batch of SMILES to a padded integer array of shape (N, max_length)."""
        tokenized = self.tokenize_batch(smiles_list)
        if max_length is None:
            max_length = max(len(t) for t in tokenized)
        result = np.zeros((len(tokenized), max_length), dtype=np.int64)
        for i, tokens in enumerate(tokenized):
            result[i] = self._encode_tokens(tokens, max_length)
        return result

    def _encode_tokens(self, tokens: List[str], max_length: int) -> np.ndarray:
        """Encode token list to padded int vector (left-padded, matching original)."""
        assert self._fitted, "Call fit() before encode()"
        pad_idx = self.token_to_idx[PAD_TOKEN]
        unk_idx = self.token_to_idx[UNK_TOKEN]

        vec = np.full(max_length, pad_idx, dtype=np.int64)
        if len(tokens) <= max_length:
            # Left-pad (original behavior)
            offset = max_length - len(tokens)
            for j, t in enumerate(tokens):
                vec[offset + j] = self.token_to_idx.get(t, unk_idx)
        else:
            # Truncate from left (original behavior)
            for j, t in enumerate(tokens[-max_length:]):
                vec[j] = self.token_to_idx.get(t, unk_idx)
        return vec

    @property
    def vocab_size(self) -> int:
        return len(self.vocab)

    def save(self, path: str):
        """Save vocabulary to a text file."""
        with open(path, "w") as f:
            f.write(str(self.vocab))

    @classmethod
    def load(cls, path: str) -> "SmilesTokenizer":
        """Load vocabulary from a text file."""
        import ast
        tok = cls()
        with open(path, "r") as f:
            tok.vocab = ast.literal_eval(f.read())
        tok.token_to_idx = {t: i for i, t in enumerate(tok.vocab)}
        tok.idx_to_token = {i: t for i, t in enumerate(tok.vocab)}
        tok._fitted = True
        return tok

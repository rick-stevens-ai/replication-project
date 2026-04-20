"""PyTorch model: Embedding → BiLSTM → TimeDistributed Dense → Soft Attention → Output.

Faithfully reimplements the Keras LSTMAttModel from SMILES-X (model.py).
"""

from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F


class SoftAttention(nn.Module):
    """Soft attention layer matching the original SMILES-X implementation.

    Computes: et = tanh(x @ W + b), at = softmax(et), output = sum(x * at, dim=1)
    Where W has shape (features, 1) and b has shape (seq_len, 1).
    """

    def __init__(self, feature_dim: int, seq_len: int):
        super().__init__()
        self.W = nn.Parameter(torch.empty(feature_dim, 1))
        self.b = nn.Parameter(torch.zeros(seq_len, 1))
        nn.init.xavier_normal_(self.W)

    def forward(self, x: torch.Tensor, return_weights: bool = False) -> torch.Tensor:
        """
        Parameters
        ----------
        x : Tensor of shape (batch, seq_len, features)
        return_weights : if True, return attention weights instead of weighted sum

        Returns
        -------
        If return_weights: Tensor (batch, seq_len)
        Otherwise: Tensor (batch, features)
        """
        # et: (batch, seq_len)
        et = torch.tanh(torch.matmul(x, self.W).squeeze(-1) + self.b.squeeze(-1))
        # at: (batch, seq_len) — attention weights
        at = F.softmax(et, dim=1)

        if return_weights:
            return at

        # Weighted sum: (batch, features)
        atx = at.unsqueeze(-1)  # (batch, seq_len, 1)
        return (x * atx).sum(dim=1)


class LSTMAttModel(nn.Module):
    """BiLSTM + Attention classifier/regressor for SMILES.

    Architecture matches the original SMILES-X exactly:
    - Embedding(vocab_size, embed_dim)
    - Bidirectional LSTM(lstm_units) → output is 2*lstm_units
    - TimeDistributed Dense(tdense_units) → Linear applied at each timestep
    - SoftAttention → collapse sequence to single vector
    - Optional extra dense layers (halving in size)
    - Output Dense(1) with sigmoid (classification) or linear (regression)
    """

    def __init__(
        self,
        vocab_size: int,
        max_length: int,
        embed_dim: int = 512,
        lstm_units: int = 128,
        tdense_units: int = 128,
        dense_depth: int = 0,
        dropout: float = 0.0,
        model_type: str = "classification",
        n_extra_features: int = 0,
    ):
        super().__init__()
        self.model_type = model_type
        self.n_extra_features = n_extra_features

        # Embedding
        self.embedding = nn.Embedding(
            num_embeddings=vocab_size,
            embedding_dim=embed_dim,
            padding_idx=0,  # pad token index
        )

        # Dropout after embedding
        self.embed_dropout = nn.Dropout(dropout) if dropout > 0 else nn.Identity()

        # Bidirectional LSTM
        self.lstm = nn.LSTM(
            input_size=embed_dim,
            hidden_size=lstm_units,
            batch_first=True,
            bidirectional=True,
        )

        # Dropout after LSTM
        self.lstm_dropout = nn.Dropout(dropout) if dropout > 0 else nn.Identity()

        # TimeDistributed Dense (Linear applied at each timestep)
        self.tdense = nn.Linear(lstm_units * 2, tdense_units)

        # Soft Attention
        self.attention = SoftAttention(feature_dim=tdense_units, seq_len=max_length)

        # Dropout after attention
        self.att_dropout = nn.Dropout(dropout) if dropout > 0 else nn.Identity()

        # Dimension after attention + optional extra features concatenation
        concat_dim = tdense_units + n_extra_features

        # Optional extra dense layers
        extra_layers = []
        in_dim = concat_dim
        for _ in range(dense_depth):
            out_dim = in_dim // 2
            if out_dim < 2:
                break
            extra_layers.append(nn.Linear(in_dim, out_dim))
            extra_layers.append(nn.ReLU())
            if dropout > 0:
                extra_layers.append(nn.Dropout(dropout))
            in_dim = out_dim
        self.extra_dense = nn.Sequential(*extra_layers) if extra_layers else nn.Identity()

        # Output
        self.output_layer = nn.Linear(in_dim, 1)

    def forward(
        self,
        x: torch.Tensor,
        extra: Optional[torch.Tensor] = None,
        return_attention: bool = False,
    ) -> torch.Tensor:
        """
        Parameters
        ----------
        x : LongTensor of shape (batch, max_length) — encoded SMILES
        extra : FloatTensor of shape (batch, n_extra_features) — optional extra features
                (e.g. ha_num, o_num). Concatenated after attention, matching original SMILES-X.
        return_attention : if True, also return attention weights

        Returns
        -------
        out : Tensor (batch, 1) — predictions
        att : Tensor (batch, seq_len) — attention weights (only if return_attention=True)
        """
        # Embedding: (batch, seq, embed_dim)
        emb = self.embed_dropout(self.embedding(x))

        # BiLSTM: (batch, seq, 2*lstm_units)
        lstm_out, _ = self.lstm(emb)
        lstm_out = self.lstm_dropout(lstm_out)

        # TimeDistributed Dense: (batch, seq, tdense_units)
        td = self.tdense(lstm_out)

        # Attention: (batch, tdense_units)
        if return_attention:
            att_weights = self.attention(td, return_weights=True)
            context = (td * att_weights.unsqueeze(-1)).sum(dim=1)
        else:
            context = self.attention(td)
        context = self.att_dropout(context)

        # Concatenate extra features (ha_num, o_num) after attention — matches original
        if self.n_extra_features > 0 and extra is not None:
            context = torch.cat([context, extra], dim=1)

        # Extra dense layers
        h = self.extra_dense(context)

        # Output
        out = self.output_layer(h)
        if self.model_type == "classification":
            out = torch.sigmoid(out)

        if return_attention:
            return out, att_weights
        return out

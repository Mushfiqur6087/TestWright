"""Lazy singleton wrapper around a small sentence-transformers model.

The model is loaded the first time ``encode`` is called so commands that don't
need embeddings (``verify``, ``export-md``) never pay the import cost. The
default model is ``all-MiniLM-L6-v2`` (~80 MB, 384-dim vectors), pinned via
``EMBEDDING_MODEL_NAME`` so the choice is centralized.
"""

from __future__ import annotations

from typing import List, Optional

import numpy as np


EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_MODEL = None  # type: ignore[var-annotated]


def _get_model():
    """Lazy-load the embedding model on first use."""
    global _MODEL
    if _MODEL is None:
        from sentence_transformers import SentenceTransformer  # local import keeps cold-start cheap

        _MODEL = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _MODEL


def encode(texts: List[str]) -> np.ndarray:
    """Embed a list of texts. Returns an (N, D) float32 array.

    Empty input returns an empty (0, 0) array so callers can early-return.
    """
    if not texts:
        return np.zeros((0, 0), dtype=np.float32)
    model = _get_model()
    vecs = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return np.asarray(vecs, dtype=np.float32)


def cosine_sim_matrix(vecs: np.ndarray) -> np.ndarray:
    """Pairwise cosine similarity for an (N, D) matrix of L2-normalised vectors.

    ``encode`` returns L2-normalised vectors, so a dot product is the cosine
    similarity. Returns an (N, N) matrix; the diagonal is 1.0.
    """
    if vecs.size == 0:
        return np.zeros((0, 0), dtype=np.float32)
    return vecs @ vecs.T


def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    """Pairwise cosine similarity between two single vectors (already normalised)."""
    if a.size == 0 or b.size == 0:
        return 0.0
    return float(np.dot(a, b))

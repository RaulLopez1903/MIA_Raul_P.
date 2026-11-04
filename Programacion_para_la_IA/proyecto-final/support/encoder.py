from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray
from sentence_transformers import SentenceTransformer

from support.data import ProductRecord, ReviewRecord
from support.settings import Settings

FloatMatrix = NDArray[np.float32]
FloatVector = NDArray[np.float32]


def load_encoder(settings: Settings) -> SentenceTransformer:
    return SentenceTransformer(settings.model_name, device=settings.device)


def encode_texts(
    model: SentenceTransformer,
    texts: Sequence[str],
    batch_size: int,
) -> FloatMatrix:
    if not texts:
        return np.empty((0, 0), dtype=np.float32)
    vectors = model.encode(
        list(texts),
        batch_size=batch_size,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    return np.asarray(vectors, dtype=np.float32)


def _normalize(vector: FloatVector) -> FloatVector:
    norm = float(np.linalg.norm(vector))
    if norm == 0.0:
        raise ValueError("Cannot normalize a zero-length embedding")
    return np.asarray(vector / norm, dtype=np.float32)


def build_product_vectors(
    model: SentenceTransformer,
    products: Sequence[ProductRecord],
    reviews: Sequence[ReviewRecord],
    batch_size: int,
) -> tuple[list[str], FloatMatrix]:
    product_ids = [product["product_id"] for product in products]
    catalog_vectors = encode_texts(
        model,
        [product["catalog_text"] for product in products],
        batch_size,
    )
    review_vectors = encode_texts(model, [review["text"] for review in reviews], batch_size)
    reviews_by_product: dict[str, list[FloatVector]] = {product_id: [] for product_id in product_ids}
    for review, vector in zip(reviews, review_vectors, strict=True):
        reviews_by_product[review["product_id"]].append(vector)

    product_vectors: list[FloatVector] = []
    for index, product_id in enumerate(product_ids):
        product_review_vectors = reviews_by_product[product_id]
        if not product_review_vectors:
            raise ValueError(f"Product '{product_id}' has no reviews with text")
        review_summary = _normalize(np.mean(product_review_vectors, axis=0, dtype=np.float32))
        product_vector = _normalize(0.5 * catalog_vectors[index] + 0.5 * review_summary)
        product_vectors.append(product_vector)
    return product_ids, np.stack(product_vectors).astype(np.float32, copy=False)

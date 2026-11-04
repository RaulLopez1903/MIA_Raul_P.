from __future__ import annotations

import gzip
import json
from collections.abc import Iterator
from pathlib import Path
from typing import TypedDict


class ProductRecord(TypedDict):
    product_id: str
    title: str
    features: list[str]
    description: list[str]
    catalog_text: str


class ReviewRecord(TypedDict):
    review_id: str
    product_id: str
    text: str
    rating: float


def _default_data_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "datasets"


def _read_jsonl(path: Path) -> Iterator[tuple[int, dict[str, object]]]:
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError(f"Expected a JSON object in {path} at line {line_number}")
            yield line_number, record


def _required_string(record: dict[str, object], field: str, line_number: int) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Expected a non-empty '{field}' at line {line_number}")
    return value.strip()


def _string_list(record: dict[str, object], field: str, line_number: int) -> list[str]:
    value = record.get(field)
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ValueError(f"Expected a list of strings for '{field}' at line {line_number}")
    return [item.strip() for item in value if item.strip()]


def load_data(
    data_dir: Path | None = None,
) -> tuple[list[ReviewRecord], dict[str, ProductRecord]]:
    directory = data_dir or _default_data_dir()
    products: dict[str, ProductRecord] = {}

    for line_number, record in _read_jsonl(directory / "products.jsonl.gz"):
        product_id = _required_string(record, "parent_asin", line_number)
        title = _required_string(record, "title", line_number)
        features = _string_list(record, "features", line_number)
        description = _string_list(record, "description", line_number)
        catalog_parts = [title, *features, *description]
        if product_id in products:
            raise ValueError(f"Duplicate product ID '{product_id}' at line {line_number}")
        products[product_id] = {
            "product_id": product_id,
            "title": title,
            "features": features,
            "description": description,
            "catalog_text": " ".join(catalog_parts),
        }

    reviews: list[ReviewRecord] = []
    review_ids: set[str] = set()
    for line_number, record in _read_jsonl(directory / "reviews.jsonl.gz"):
        product_id = _required_string(record, "parent_asin", line_number)
        if product_id not in products:
            raise ValueError(
                f"Review at line {line_number} references unknown product '{product_id}'"
            )
        text_value = record.get("text")
        if not isinstance(text_value, str):
            raise ValueError(f"Expected review text at line {line_number}")
        text = text_value.strip()
        if not text:
            continue
        rating_value = record.get("rating")
        if isinstance(rating_value, bool) or not isinstance(rating_value, (int, float)):
            raise ValueError(f"Expected a numeric rating at line {line_number}")
        if rating_value not in (1, 2, 3, 4, 5):
            raise ValueError(f"Rating must be between 1 and 5 at line {line_number}")
        source_line = record.get("source_line")
        if isinstance(source_line, bool) or not isinstance(source_line, int) or source_line < 1:
            raise ValueError(f"Expected a positive source_line at line {line_number}")
        review_id = f"Electronics:{source_line}"
        if review_id in review_ids:
            raise ValueError(f"Duplicate review ID '{review_id}' at line {line_number}")
        review_ids.add(review_id)
        reviews.append(
            {
                "review_id": review_id,
                "product_id": product_id,
                "text": text,
                "rating": float(rating_value),
            }
        )

    if not products:
        raise ValueError(f"No products found in {directory}")
    if not reviews:
        raise ValueError(f"No reviews with text found in {directory}")
    return reviews, products

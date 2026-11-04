from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import TypedDict

import numpy as np
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from numpy.typing import NDArray
from sentence_transformers import SentenceTransformer

from support.data import ProductRecord, ReviewRecord, load_data
from support.encoder import build_product_vectors, encode_texts, load_encoder
from support.settings import Settings, load_settings


class SearchResult(TypedDict):
    product_id: str
    title: str
    similarity: float
    review_count: int


class AnalysisResult(TypedDict):
    product_id: str
    review_count: int
    rating_counts: dict[str, int]
    rating_proportions: dict[str, float]
    mean_rating: float | None
    median_rating: float | None


class ProductComparison(AnalysisResult):
    mean_difference_from_first: float | None


class ComparisonResult(TypedDict):
    baseline_product_id: str
    products: list[ProductComparison]


@dataclass
class ProductSearchService:
    settings: Settings
    model: SentenceTransformer
    products: dict[str, ProductRecord]
    product_ids: list[str]
    product_vectors: NDArray[np.float32]
    reviews_by_product: dict[str, list[ReviewRecord]]

    @classmethod
    def load(cls) -> ProductSearchService:
        settings = load_settings()
        reviews, products = load_data()
        model = load_encoder(settings)
        product_records = list(products.values())
        product_ids, product_vectors = build_product_vectors(
            model,
            product_records,
            reviews,
            settings.batch_size,
        )
        reviews_by_product: dict[str, list[ReviewRecord]] = {
            product_id: [] for product_id in product_ids
        }
        for review in reviews:
            reviews_by_product[review["product_id"]].append(review)
        return cls(
            settings=settings,
            model=model,
            products=products,
            product_ids=product_ids,
            product_vectors=product_vectors,
            reviews_by_product=reviews_by_product,
        )

    def search(self, query: str, top_k: int) -> list[SearchResult]:
        query_vector = encode_texts(self.model, [query], self.settings.batch_size)[0]
        similarities = self.product_vectors @ query_vector
        candidate_count = min(top_k, len(self.product_ids))
        top_positions = np.argsort(similarities)[::-1][:candidate_count]
        return [
            {
                "product_id": self.product_ids[int(position)],
                "title": self.products[self.product_ids[int(position)]]["title"],
                "similarity": float(similarities[int(position)]),
                "review_count": len(
                    self.reviews_by_product[self.product_ids[int(position)]]
                ),
            }
            for position in top_positions
        ]

    def analyze(self, product_id: str) -> AnalysisResult:
        product_reviews = self.reviews_by_product.get(product_id, [])
        counts = Counter(int(review["rating"]) for review in product_reviews)
        review_count = len(product_reviews)
        rating_counts = {str(rating): counts.get(rating, 0) for rating in range(1, 6)}
        rating_proportions = {
            str(rating): (rating_counts[str(rating)] / review_count if review_count else 0.0)
            for rating in range(1, 6)
        }
        if review_count:
            ratings = np.asarray(
                [review["rating"] for review in product_reviews],
                dtype=np.float64,
            )
            mean_rating: float | None = float(np.mean(ratings))
            median_rating: float | None = float(np.median(ratings))
        else:
            mean_rating = None
            median_rating = None
        return {
            "product_id": product_id,
            "review_count": review_count,
            "rating_counts": rating_counts,
            "rating_proportions": rating_proportions,
            "mean_rating": mean_rating,
            "median_rating": median_rating,
        }


_service: ProductSearchService | None = None
mcp = MCPServer("Amazon Reviews 2023 Electronics")


@mcp.tool()
def search_products(query: str, top_k: int = 5) -> list[SearchResult]:
    if not query.strip():
        raise ToolError("query must not be empty")
    if isinstance(top_k, bool) or not isinstance(top_k, int) or not 1 <= top_k <= 20:
        raise ToolError("top_k must be an integer between 1 and 20")
    if _service is None:
        raise RuntimeError("The product search service has not been initialized")
    return _service.search(query.strip(), top_k)


@mcp.tool()
def analyze_product(product_id: str) -> AnalysisResult:
    if not product_id.strip():
        raise ToolError("product_id must not be empty")
    if _service is None:
        raise RuntimeError("The product search service has not been initialized")
    return _service.analyze(product_id.strip())


@mcp.tool()
def compare_products(product_ids: list[str]) -> ComparisonResult:
    normalized_ids = [product_id.strip() for product_id in product_ids]
    if len(normalized_ids) < 2:
        raise ToolError("At least two product IDs are required")
    if any(not product_id for product_id in normalized_ids):
        raise ToolError("Product IDs must not be empty")
    if len(set(normalized_ids)) != len(normalized_ids):
        raise ToolError("Product IDs must be distinct")
    if _service is None:
        raise RuntimeError("The product search service has not been initialized")

    analyses = [_service.analyze(product_id) for product_id in normalized_ids]
    baseline_mean = analyses[0]["mean_rating"]
    products: list[ProductComparison] = []
    for analysis in analyses:
        mean = analysis["mean_rating"]
        difference = (
            float(mean - baseline_mean)
            if mean is not None and baseline_mean is not None
            else None
        )
        products.append({**analysis, "mean_difference_from_first": difference})
    return {"baseline_product_id": normalized_ids[0], "products": products}


def main() -> None:
    global _service
    _service = ProductSearchService.load()
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()

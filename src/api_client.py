"""Retrieve and validate product data from DummyJSON or local samples."""

from __future__ import annotations

import json
from numbers import Number
from pathlib import Path
from typing import Any

import requests


PRODUCTS_URL = "https://dummyjson.com/products"
PRODUCT_FIELDS = (
    "id",
    "title",
    "category",
    "price",
    "rating",
    "stock",
    "discountPercentage",
)


class ProductAPIError(Exception):
    """Raised when product data cannot be retrieved or validated."""


def fetch_products(limit: int = 30, timeout: int = 10) -> list[dict]:
    """Fetch products from DummyJSON and return simplified product dictionaries."""
    params = {
        "limit": limit,
        "select": ",".join(PRODUCT_FIELDS),
    }

    try:
        response = requests.get(PRODUCTS_URL, params=params, timeout=timeout)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        raise ProductAPIError(f"Could not retrieve products: {exc}") from exc
    except ValueError as exc:
        raise ProductAPIError("The products API returned invalid JSON.") from exc

    return normalize_products_from_payload(payload)


def load_products_from_file(file_path: str | Path) -> list[dict]:
    """Load sample products from a JSON file for offline development."""
    path = Path(file_path)

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ProductAPIError(f"Could not read sample data from {path}.") from exc
    except json.JSONDecodeError as exc:
        raise ProductAPIError(f"Sample data in {path} is not valid JSON.") from exc

    if isinstance(payload, list):
        payload = {"products": payload}

    return normalize_products_from_payload(payload)


def normalize_products_from_payload(payload: Any) -> list[dict]:
    """Validate a product payload and return simplified product dictionaries."""
    if not isinstance(payload, dict):
        raise ProductAPIError("Product response must be a JSON object.")

    raw_products = payload.get("products")
    if not isinstance(raw_products, list) or not raw_products:
        raise ProductAPIError("Product response did not contain any products.")

    return [_normalize_product(product) for product in raw_products]


def _normalize_product(product: Any) -> dict:
    if not isinstance(product, dict):
        raise ProductAPIError("Each product must be a JSON object.")

    missing_fields = [field for field in PRODUCT_FIELDS if field not in product]
    if missing_fields:
        missing = ", ".join(missing_fields)
        raise ProductAPIError(f"Product response is missing fields: {missing}.")

    title = _require_text(product, "title")
    category = _require_text(product, "category")

    return {
        "id": product["id"],
        "title": title,
        "category": category,
        "price": _require_number(product, "price"),
        "rating": _require_number(product, "rating"),
        "stock": _require_number(product, "stock"),
        "discountPercentage": _require_number(product, "discountPercentage"),
    }


def _require_text(product: dict, field: str) -> str:
    value = product[field]
    if not isinstance(value, str) or not value.strip():
        raise ProductAPIError(f"Product field '{field}' must be text.")
    return value


def _require_number(product: dict, field: str) -> Number:
    value = product[field]
    if isinstance(value, bool) or not isinstance(value, Number):
        raise ProductAPIError(f"Product field '{field}' must be numeric.")
    return value


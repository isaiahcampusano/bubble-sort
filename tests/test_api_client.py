import json

import pytest
import requests

from src import api_client
from src.api_client import ProductAPIError


VALID_PRODUCT = {
    "id": 1,
    "title": "Example Product",
    "category": "beauty",
    "price": 9.99,
    "rating": 4.5,
    "stock": 25,
    "discountPercentage": 7.5,
}


class FakeResponse:
    def __init__(self, payload=None, status_code=200, json_error=None):
        self.payload = payload
        self.status_code = status_code
        self.json_error = json_error

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")

    def json(self):
        if self.json_error:
            raise self.json_error
        return self.payload


def test_fetch_products_requests_and_simplifies_products(monkeypatch):
    calls = []

    def fake_get(url, params, timeout):
        calls.append({"url": url, "params": params, "timeout": timeout})
        return FakeResponse({"products": [VALID_PRODUCT]})

    monkeypatch.setattr(api_client.requests, "get", fake_get)

    products = api_client.fetch_products(limit=30, timeout=5)

    assert products == [VALID_PRODUCT]
    assert calls == [
        {
            "url": api_client.PRODUCTS_URL,
            "params": {
                "limit": 30,
                "select": "id,title,category,price,rating,stock,discountPercentage",
            },
            "timeout": 5,
        }
    ]


def test_fetch_products_handles_connection_failures(monkeypatch):
    def fake_get(url, params, timeout):
        raise requests.ConnectionError("network down")

    monkeypatch.setattr(api_client.requests, "get", fake_get)

    with pytest.raises(ProductAPIError, match="Could not retrieve products"):
        api_client.fetch_products()


def test_fetch_products_handles_invalid_json(monkeypatch):
    def fake_get(url, params, timeout):
        return FakeResponse(json_error=ValueError("bad json"))

    monkeypatch.setattr(api_client.requests, "get", fake_get)

    with pytest.raises(ProductAPIError, match="invalid JSON"):
        api_client.fetch_products()


def test_empty_product_response_is_rejected():
    with pytest.raises(ProductAPIError, match="did not contain any products"):
        api_client.normalize_products_from_payload({"products": []})


def test_malformed_response_without_products_is_rejected():
    with pytest.raises(ProductAPIError, match="did not contain any products"):
        api_client.normalize_products_from_payload({"items": [VALID_PRODUCT]})


def test_product_missing_required_field_is_rejected():
    product = dict(VALID_PRODUCT)
    del product["rating"]

    with pytest.raises(ProductAPIError, match="missing fields: rating"):
        api_client.normalize_products_from_payload({"products": [product]})


def test_non_numeric_metric_is_rejected():
    product = dict(VALID_PRODUCT)
    product["rating"] = "excellent"

    with pytest.raises(ProductAPIError, match="must be numeric"):
        api_client.normalize_products_from_payload({"products": [product]})


def test_load_products_from_file_accepts_product_list(tmp_path):
    sample_file = tmp_path / "sample_products.json"
    sample_file.write_text(json.dumps([VALID_PRODUCT]), encoding="utf-8")

    products = api_client.load_products_from_file(sample_file)

    assert products == [VALID_PRODUCT]


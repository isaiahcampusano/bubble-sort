from pathlib import Path

import pytest

from src.bubble_sort import bubble_sort_products


def test_products_are_ranked_from_highest_rating_to_lowest():
    products = [
        {"title": "A", "rating": 3.5},
        {"title": "B", "rating": 4.8},
        {"title": "C", "rating": 4.1},
    ]

    ranked_products, comparisons, swaps = bubble_sort_products(products)

    assert [product["title"] for product in ranked_products] == ["B", "C", "A"]
    assert comparisons == 3
    assert swaps == 2


def test_ascending_sorting_works():
    products = [
        {"title": "A", "rating": 3.5},
        {"title": "B", "rating": 4.8},
        {"title": "C", "rating": 4.1},
    ]

    ranked_products, comparisons, swaps = bubble_sort_products(
        products,
        descending=False,
    )

    assert [product["title"] for product in ranked_products] == ["A", "C", "B"]
    assert comparisons == 3
    assert swaps == 1


def test_empty_list_returns_empty_list():
    ranked_products, comparisons, swaps = bubble_sort_products([])

    assert ranked_products == []
    assert comparisons == 0
    assert swaps == 0


def test_one_product_list_remains_unchanged():
    products = [{"title": "A", "rating": 3.5}]

    ranked_products, comparisons, swaps = bubble_sort_products(products)

    assert ranked_products == products
    assert comparisons == 0
    assert swaps == 0


def test_equal_ratings_retain_original_order():
    products = [
        {"title": "A", "rating": 4.5},
        {"title": "B", "rating": 4.5},
        {"title": "C", "rating": 4.1},
    ]

    ranked_products, _, _ = bubble_sort_products(products)

    assert [product["title"] for product in ranked_products] == ["A", "B", "C"]


def test_original_list_is_not_modified():
    products = [
        {"title": "A", "rating": 3.5},
        {"title": "B", "rating": 4.8},
        {"title": "C", "rating": 4.1},
    ]
    original_products = [dict(product) for product in products]

    ranked_products, _, _ = bubble_sort_products(products)

    assert products == original_products
    assert ranked_products is not products


def test_early_stopping_occurs_on_already_sorted_list():
    products = [
        {"title": "A", "rating": 4.8},
        {"title": "B", "rating": 4.1},
        {"title": "C", "rating": 3.5},
    ]

    ranked_products, comparisons, swaps = bubble_sort_products(products)

    assert [product["title"] for product in ranked_products] == ["A", "B", "C"]
    assert comparisons == 2
    assert swaps == 0


def test_invalid_sorting_field_raises_clear_error():
    products = [{"title": "A", "rating": 3.5}]

    with pytest.raises(ValueError, match="Sort key 'price' was not found"):
        bubble_sort_products(products, sort_key="price")


def test_custom_algorithm_does_not_use_python_sort_helpers():
    source = Path("src/bubble_sort.py").read_text(encoding="utf-8")

    assert "sorted(" not in source
    assert ".sort(" not in source

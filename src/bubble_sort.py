"""Custom bubble sort implementation for product dictionaries."""

from __future__ import annotations


def bubble_sort_products(
    products: list[dict],
    sort_key: str = "rating",
    descending: bool = True,
) -> tuple[list[dict], int, int]:
    """Return ranked products, comparison count, and swap count."""
    ranked_products = list(products)
    comparison_count = 0
    swap_count = 0

    product_count = len(ranked_products)
    if product_count < 2:
        _validate_sort_key(ranked_products, sort_key)
        return ranked_products, comparison_count, swap_count

    _validate_sort_key(ranked_products, sort_key)

    for pass_index in range(product_count - 1):
        swapped_this_pass = False
        last_compare_index = product_count - 1 - pass_index

        for index in range(last_compare_index):
            left_product = ranked_products[index]
            right_product = ranked_products[index + 1]
            left_value = left_product[sort_key]
            right_value = right_product[sort_key]
            comparison_count += 1

            if _should_swap(left_value, right_value, descending):
                ranked_products[index], ranked_products[index + 1] = (
                    right_product,
                    left_product,
                )
                swap_count += 1
                swapped_this_pass = True

        if not swapped_this_pass:
            break

    return ranked_products, comparison_count, swap_count


def _validate_sort_key(products: list[dict], sort_key: str) -> None:
    for product in products:
        if sort_key not in product:
            title = product.get("title", "Unknown product")
            raise ValueError(f"Sort key '{sort_key}' was not found on {title}.")


def _should_swap(left_value: object, right_value: object, descending: bool) -> bool:
    if descending:
        return left_value < right_value
    return left_value > right_value


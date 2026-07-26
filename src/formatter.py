"""Terminal formatting helpers for product rankings."""

from __future__ import annotations

from numbers import Number


def format_original_order(products: list[dict], sort_key: str = "rating") -> str:
    lines = [f"Original product order by {sort_key}:", ""]
    for index, product in enumerate(products, start=1):
        lines.append(
            f"{index:>2}. {product['title']} "
            f"({sort_key}: {_format_metric(product[sort_key], sort_key)})"
        )
    return "\n".join(lines)


def format_ranked_table(products: list[dict], sort_key: str = "rating") -> str:
    if sort_key == "rating":
        headers = ["Rank", "Product", "Category", "Rating", "Price"]
        rows = [
            [
                str(index),
                product["title"],
                product["category"],
                f"{product['rating']:.2f}",
                _format_money(product["price"]),
            ]
            for index, product in enumerate(products, start=1)
        ]
    elif sort_key == "price":
        headers = ["Rank", "Product", "Category", "Price", "Rating"]
        rows = [
            [
                str(index),
                product["title"],
                product["category"],
                _format_money(product["price"]),
                f"{product['rating']:.2f}",
            ]
            for index, product in enumerate(products, start=1)
        ]
    else:
        headers = ["Rank", "Product", "Category", _display_name(sort_key), "Rating", "Price"]
        rows = [
            [
                str(index),
                product["title"],
                product["category"],
                _format_metric(product[sort_key], sort_key),
                f"{product['rating']:.2f}",
                _format_money(product["price"]),
            ]
            for index, product in enumerate(products, start=1)
        ]

    widths = _column_widths(headers, rows)
    rule = "-+-".join("-" * width for width in widths)
    lines = [_format_row(headers, widths), rule]
    lines.extend(_format_row(row, widths) for row in rows)
    return "\n".join(lines)


def format_summary(
    ranked_products: list[dict],
    comparisons: int,
    swaps: int,
    sort_key: str = "rating",
    descending: bool = True,
) -> str:
    lines = [
        "Summary:",
        f"Number of products: {len(ranked_products)}",
        f"Sort metric: {_display_name(sort_key)}",
        f"Sort direction: {'highest to lowest' if descending else 'lowest to highest'}",
        f"Number of comparisons: {comparisons}",
        f"Number of swaps: {swaps}",
    ]

    if ranked_products:
        if sort_key == "rating":
            highest = ranked_products[0] if descending else ranked_products[-1]
            lowest = ranked_products[-1] if descending else ranked_products[0]
            lines.append(
                "Highest-rated product: "
                f"{highest['title']} ({highest['rating']:.2f})"
            )
            lines.append(
                "Lowest-rated product: "
                f"{lowest['title']} ({lowest['rating']:.2f})"
            )
        else:
            top_product = ranked_products[0]
            bottom_product = ranked_products[-1]
            lines.append(
                "Top-ranked product: "
                f"{top_product['title']} "
                f"({_format_metric(top_product[sort_key], sort_key)})"
            )
            lines.append(
                "Bottom-ranked product: "
                f"{bottom_product['title']} "
                f"({_format_metric(bottom_product[sort_key], sort_key)})"
            )

    return "\n".join(lines)


def _column_widths(headers: list[str], rows: list[list[str]]) -> list[int]:
    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))
    return widths


def _format_row(values: list[str], widths: list[int]) -> str:
    return " | ".join(value.ljust(widths[index]) for index, value in enumerate(values))


def _display_name(sort_key: str) -> str:
    names = {
        "rating": "Rating",
        "price": "Price",
        "discountPercentage": "Discount",
        "stock": "Stock",
    }
    return names.get(sort_key, sort_key)


def _format_metric(value: object, sort_key: str) -> str:
    if sort_key == "price" and isinstance(value, Number):
        return _format_money(value)
    if sort_key == "discountPercentage" and isinstance(value, Number):
        return f"{value:.2f}%"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def _format_money(value: Number) -> str:
    return f"${value:.2f}"

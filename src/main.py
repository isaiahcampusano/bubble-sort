"""Command-line entrypoint for Product Performance Ranker."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.api_client import ProductAPIError, fetch_products, load_products_from_file
from src.bubble_sort import bubble_sort_products
from src.formatter import format_original_order, format_ranked_table, format_summary


ALLOWED_SORT_KEYS = ("rating", "price", "discountPercentage", "stock")
DEFAULT_SAMPLE_FILE = Path(__file__).resolve().parents[1] / "data" / "sample_products.json"


def main() -> int:
    args = _parse_args()
    descending = not args.ascending

    try:
        products = _get_products(args)
    except ProductAPIError as exc:
        print(f"Product Performance Ranker could not continue: {exc}")
        return 1

    try:
        ranked_products, comparisons, swaps = bubble_sort_products(
            products,
            sort_key=args.sort_key,
            descending=descending,
        )
    except ValueError as exc:
        print(f"Product Performance Ranker could not rank products: {exc}")
        return 1

    print(format_original_order(products, args.sort_key))
    print()
    print("Ranked products:")
    print()
    print(format_ranked_table(ranked_products, args.sort_key))
    print()
    print(format_summary(ranked_products, comparisons, swaps, args.sort_key, descending))
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rank products from DummyJSON with a custom bubble sort algorithm.",
    )
    parser.add_argument(
        "--sort-key",
        choices=ALLOWED_SORT_KEYS,
        default="rating",
        help="Product field to rank by. Defaults to rating for v1 behavior.",
    )
    parser.add_argument(
        "--ascending",
        action="store_true",
        help="Rank from lowest to highest instead of highest to lowest.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=30,
        help="Number of products to request from DummyJSON.",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Load products from the local sample JSON file instead of the API.",
    )
    parser.add_argument(
        "--sample-file",
        type=Path,
        default=DEFAULT_SAMPLE_FILE,
        help="Path to local sample product data used with --offline or API fallback.",
    )
    return parser.parse_args()


def _get_products(args: argparse.Namespace) -> list[dict]:
    if args.offline:
        print(f"Loading sample products from {args.sample_file}.")
        return load_products_from_file(args.sample_file)

    try:
        print(f"Fetching up to {args.limit} products from DummyJSON.")
        return fetch_products(limit=args.limit)
    except ProductAPIError as exc:
        print(f"API unavailable or invalid: {exc}")
        print(f"Falling back to local sample products from {args.sample_file}.")
        return load_products_from_file(args.sample_file)


if __name__ == "__main__":
    raise SystemExit(main())


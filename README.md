# Product Performance Ranker

Product Performance Ranker is a small Python terminal application that retrieves product data from the public DummyJSON products API and ranks the products with a custom bubble sort algorithm.

The project is primarily an algorithm-learning project. In v1, "performance" means customer rating. It does not claim to measure true business performance.

## Features

- Retrieves product data from DummyJSON.
- Simplifies product JSON into dictionaries with id, title, category, price, rating, stock, and discount percentage.
- Implements stable bubble sort without Python's built-in sort helpers.
- Tracks comparison and swap counts.
- Displays the original product order and the ranked output in a readable terminal table.
- Falls back to local sample data if the API is unavailable.
- Supports v2 ranking fields through the command line: rating, price, discount percentage, and stock.

## Project Structure

```text
product-performance-ranker/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── api_client.py
│   ├── bubble_sort.py
│   └── formatter.py
├── tests/
│   ├── test_bubble_sort.py
│   └── test_api_client.py
└── data/
    └── sample_products.json
```

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

On macOS or Linux, activate the environment with:

```bash
source .venv/bin/activate
```

## Usage

Run the default v1 behavior:

```bash
python -m src.main
```

This ranks products by rating from highest to lowest.

Run with local sample data:

```bash
python -m src.main --offline
```

Choose a v2 ranking field:

```bash
python -m src.main --sort-key price
python -m src.main --sort-key discountPercentage
python -m src.main --sort-key stock
```

Rank lowest to highest:

```bash
python -m src.main --sort-key price --ascending
```

Limit API products:

```bash
python -m src.main --limit 20
```

## Example Output

```text
Ranked products:

Rank | Product                       | Category   | Rating | Price
-----+-------------------------------+------------+--------+--------
1    | Essence Mascara Lash Princess | beauty     | 4.94   | $9.99
2    | Calvin Klein CK One           | fragrances | 4.85   | $49.99

Summary:
Number of products: 20
Sort metric: Rating
Sort direction: highest to lowest
Number of comparisons: 190
Number of swaps: 41
Highest-rated product: Essence Mascara Lash Princess (4.94)
Lowest-rated product: Red Lipstick (2.51)
```

## Algorithm Behavior

Bubble sort repeatedly compares adjacent products and swaps them when they are out of order.

For v1 descending rating sort:

- Compare the product on the left with the product on the right.
- Swap when the left rating is lower than the right rating.
- Do not swap equal ratings, which preserves original order and keeps the algorithm stable.
- Stop early when a complete pass finishes with no swaps.

Time complexity:

- Best case: O(n), when the products are already ordered and early stopping triggers.
- Average case: O(n^2).
- Worst case: O(n^2).

## Testing

```bash
pytest
```

The tests cover ranking direction, ties, empty inputs, one-product input, input preservation, early stopping, invalid sort fields, API success, API failure, empty responses, and malformed responses.

## Limitations

- This is not a production product-recommendation system.
- Ratings, prices, discounts, and stock levels are ranking metrics, not true business performance indicators.
- A defensible performance score would require sales, revenue, conversion rate, returns, margin, and a defined time period.

## Future Versions

- v3: Compare bubble sort against Python's built-in sorting for timing and correctness.
- v4: Build a browser interface that visualizes each comparison and swap.
- v5: Replace the sample API with a real finance or commerce dataset and define a defensible performance score.

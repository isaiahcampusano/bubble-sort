# Product Performance Ranker

Product Performance Ranker v1 is a Python terminal app that fetches product data, ranks products by rating using a custom stable bubble sort, and displays the number of comparisons and swaps performed.

The project includes offline sample data, automated tests, and a small v2 preview with selectable ranking fields such as price, stock, and discount percentage.

## Run

```bash
python -m pip install -r requirements.txt
python -m src.main
```

Offline mode:

```bash
python -m src.main --offline
```

Try another ranking field:

```bash
python -m src.main --offline --sort-key price --ascending
```

## Test

```bash
python -m pytest
```


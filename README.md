# Product Performance Ranker

Product Performance Ranker is a bubble sort project with two interfaces:

- A Python terminal app that fetches product data, ranks products with a custom stable bubble sort, and reports comparison and swap counts.
- A plain HTML/CSS/JavaScript browser visualizer that animates adjacent comparisons, swaps, and sorted passes.

The browser version uses the sample product dataset by default and supports ranking by rating, price, discount percentage, or stock.

## Browser visualizer

Open `index.html` in a browser, or serve the repository root with a local static server:

```bash
python -m http.server 8000
```

Then visit:

```text
http://localhost:8000
```

For GitHub Pages, publish the repository from the `main` branch and `/root` folder. The expected project URL is:

```text
https://isaiahcampusano.github.io/bubble-sort/
```

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

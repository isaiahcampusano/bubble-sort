const FALLBACK_PRODUCTS = [
  { id: 1, title: "Essence Mascara Lash Princess", category: "beauty", price: 9.99, rating: 4.94, stock: 5, discountPercentage: 7.17 },
  { id: 2, title: "Eyeshadow Palette with Mirror", category: "beauty", price: 19.99, rating: 3.28, stock: 44, discountPercentage: 5.5 },
  { id: 3, title: "Powder Canister", category: "beauty", price: 14.99, rating: 3.82, stock: 59, discountPercentage: 18.14 },
  { id: 4, title: "Red Lipstick", category: "beauty", price: 12.99, rating: 2.51, stock: 68, discountPercentage: 19.03 },
  { id: 5, title: "Red Nail Polish", category: "beauty", price: 8.99, rating: 3.91, stock: 71, discountPercentage: 2.46 },
  { id: 6, title: "Calvin Klein CK One", category: "fragrances", price: 49.99, rating: 4.85, stock: 17, discountPercentage: 5.67 },
  { id: 7, title: "Chanel Coco Noir Eau De", category: "fragrances", price: 129.99, rating: 2.76, stock: 41, discountPercentage: 10.64 },
  { id: 8, title: "Dior J'adore", category: "fragrances", price: 89.99, rating: 3.31, stock: 91, discountPercentage: 14.72 },
  { id: 9, title: "Dolce Shine Eau de", category: "fragrances", price: 69.99, rating: 2.68, stock: 3, discountPercentage: 11.47 },
  { id: 10, title: "Gucci Bloom Eau de", category: "fragrances", price: 79.99, rating: 2.69, stock: 93, discountPercentage: 8.9 },
  { id: 11, title: "Annibale Colombo Bed", category: "furniture", price: 1899.99, rating: 4.14, stock: 47, discountPercentage: 0.29 },
  { id: 12, title: "Annibale Colombo Sofa", category: "furniture", price: 2499.99, rating: 3.08, stock: 16, discountPercentage: 18.54 },
  { id: 13, title: "Bedside Table African Cherry", category: "furniture", price: 299.99, rating: 4.48, stock: 16, discountPercentage: 9.58 },
  { id: 14, title: "Knoll Saarinen Executive Chair", category: "furniture", price: 499.99, rating: 4.11, stock: 47, discountPercentage: 15.23 },
  { id: 15, title: "Wooden Bathroom Sink", category: "furniture", price: 799.99, rating: 3.26, stock: 95, discountPercentage: 11.22 },
  { id: 16, title: "Apple", category: "groceries", price: 1.99, rating: 2.96, stock: 9, discountPercentage: 1.97 },
  { id: 17, title: "Beef Steak", category: "groceries", price: 12.99, rating: 2.83, stock: 96, discountPercentage: 17.99 },
  { id: 18, title: "Cat Food", category: "groceries", price: 8.99, rating: 4.13, stock: 13, discountPercentage: 9.57 },
  { id: 19, title: "Chicken Meat", category: "groceries", price: 9.99, rating: 4.61, stock: 69, discountPercentage: 10.46 },
  { id: 20, title: "Cooking Oil", category: "groceries", price: 4.99, rating: 4.01, stock: 22, discountPercentage: 18.89 },
];

const METRICS = {
  rating: { label: "rating", format: (value) => value.toFixed(2) },
  price: { label: "price", format: (value) => `$${value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` },
  discountPercentage: { label: "discount", format: (value) => `${value.toFixed(2)}%` },
  stock: { label: "stock", format: (value) => `${value}` },
};

const elements = {
  metric: document.querySelector("#metric"),
  direction: document.querySelector("#direction"),
  speed: document.querySelector("#speed"),
  start: document.querySelector("#start"),
  step: document.querySelector("#step"),
  reset: document.querySelector("#reset"),
  comparisonCount: document.querySelector("#comparison-count"),
  swapCount: document.querySelector("#swap-count"),
  passCount: document.querySelector("#pass-count"),
  status: document.querySelector("#status"),
  stageTitle: document.querySelector("#stage-title"),
  productTrack: document.querySelector("#product-track"),
  rankedList: document.querySelector("#ranked-list"),
  originalOrder: document.querySelector("#original-order"),
};

const state = {
  originalProducts: [],
  products: [],
  passIndex: 0,
  compareIndex: 0,
  comparisons: 0,
  swaps: 0,
  swappedThisPass: false,
  activeIndices: [],
  activeMode: "idle",
  running: false,
  finished: false,
};

function getMetric() {
  return elements.metric.value;
}

function isDescending() {
  return elements.direction.value === "desc";
}

function getDelay() {
  const max = Number(elements.speed.max);
  const value = Number(elements.speed.value);
  return max - value + Number(elements.speed.min);
}

function shouldSwap(left, right) {
  const metric = getMetric();
  if (isDescending()) {
    return left[metric] < right[metric];
  }
  return left[metric] > right[metric];
}

function metricBounds() {
  const metric = getMetric();
  const values = state.originalProducts.map((product) => product[metric]);
  return {
    min: Math.min(...values),
    max: Math.max(...values),
  };
}

function barHeight(product) {
  const metric = getMetric();
  const bounds = metricBounds();
  if (bounds.max === bounds.min) {
    return 70;
  }
  return 12 + ((product[metric] - bounds.min) / (bounds.max - bounds.min)) * 88;
}

function metricText(product) {
  const metric = getMetric();
  return METRICS[metric].format(product[metric]);
}

function sortedStartIndex() {
  if (state.finished) {
    return 0;
  }
  return state.products.length - state.passIndex;
}

function isIndexSorted(index) {
  return index >= sortedStartIndex();
}

function renderProducts() {
  const items = state.products
    .map((product, index) => {
      const classes = ["product-item"];
      if (state.activeIndices.includes(index)) {
        classes.push(state.activeMode);
      }
      if (isIndexSorted(index)) {
        classes.push("sorted");
      }

      return `
        <article class="${classes.join(" ")}" aria-label="${product.title}, ${metricText(product)}">
          <div class="bar-wrap" aria-hidden="true">
            <div class="bar" style="height: ${barHeight(product)}%"></div>
          </div>
          <strong class="product-name">${product.title}</strong>
          <span class="product-value">${metricText(product)}</span>
        </article>
      `;
    })
    .join("");

  elements.productTrack.innerHTML = items;
}

function renderRankedList() {
  const metric = getMetric();
  elements.rankedList.innerHTML = state.products
    .map(
      (product) => `
        <li>
          <strong>${product.title}</strong>
          <span>${METRICS[metric].label}: ${metricText(product)} &middot; ${product.category}</span>
        </li>
      `,
    )
    .join("");
}

function renderOriginalOrder() {
  elements.originalOrder.innerHTML = state.originalProducts
    .map((product, index) => `<span class="original-chip">${index + 1}. ${product.title}</span>`)
    .join("");
}

function renderStats() {
  elements.comparisonCount.textContent = state.comparisons;
  elements.swapCount.textContent = state.swaps;
  elements.passCount.textContent = state.finished ? state.passIndex : state.passIndex + 1;
  elements.stageTitle.textContent = `Ranking by ${METRICS[getMetric()].label}`;
  elements.start.textContent = state.running ? "Pause" : "Start";
  elements.step.disabled = state.running || state.finished;
  elements.metric.disabled = state.running;
  elements.direction.disabled = state.running;
}

function render(statusText) {
  if (statusText) {
    elements.status.textContent = statusText;
  }
  renderProducts();
  renderRankedList();
  renderStats();
}

function resetSort() {
  state.products = state.originalProducts.map((product) => ({ ...product }));
  state.passIndex = 0;
  state.compareIndex = 0;
  state.comparisons = 0;
  state.swaps = 0;
  state.swappedThisPass = false;
  state.activeIndices = [];
  state.activeMode = "idle";
  state.running = false;
  state.finished = state.products.length < 2;
  render(state.finished ? "Sorted" : "Ready");
}

function sleep(ms) {
  return new Promise((resolve) => {
    window.setTimeout(resolve, ms);
  });
}

function finishSort() {
  state.finished = true;
  state.running = false;
  state.activeIndices = [];
  state.activeMode = "idle";
  render("Sorted");
}

function advancePassIfNeeded() {
  const lastCompareIndex = state.products.length - 1 - state.passIndex;
  if (state.compareIndex < lastCompareIndex) {
    return false;
  }

  if (!state.swappedThisPass || state.passIndex >= state.products.length - 2) {
    finishSort();
    return true;
  }

  state.passIndex += 1;
  state.compareIndex = 0;
  state.swappedThisPass = false;
  render(`Pass ${state.passIndex + 1}`);
  return false;
}

async function stepSort() {
  if (state.finished || advancePassIfNeeded()) {
    return;
  }

  const leftIndex = state.compareIndex;
  const rightIndex = leftIndex + 1;
  const left = state.products[leftIndex];
  const right = state.products[rightIndex];

  state.comparisons += 1;
  state.activeIndices = [leftIndex, rightIndex];
  state.activeMode = "comparing";
  render("Comparing");
  await sleep(getDelay());

  if (shouldSwap(left, right)) {
    state.products[leftIndex] = right;
    state.products[rightIndex] = left;
    state.swaps += 1;
    state.swappedThisPass = true;
    state.activeMode = "swapping";
    render("Swapping");
    await sleep(getDelay());
  }

  state.compareIndex += 1;
  state.activeIndices = [];
  state.activeMode = "idle";

  if (!advancePassIfNeeded()) {
    render("Scanning");
  }
}

async function runSort() {
  if (state.finished) {
    return;
  }

  state.running = true;
  render("Running");

  while (state.running && !state.finished) {
    await stepSort();
    await sleep(80);
  }

  if (!state.finished) {
    render("Paused");
  }
}

function toggleRun() {
  if (state.running) {
    state.running = false;
    render("Paused");
    return;
  }
  runSort();
}

async function loadProducts() {
  try {
    const response = await fetch("data/sample_products.json");
    if (!response.ok) {
      throw new Error("Sample data was not available.");
    }
    const data = await response.json();
    state.originalProducts = data.products;
  } catch (error) {
    state.originalProducts = FALLBACK_PRODUCTS;
  }

  renderOriginalOrder();
  resetSort();
}

elements.start.addEventListener("click", toggleRun);
elements.step.addEventListener("click", stepSort);
elements.reset.addEventListener("click", resetSort);
elements.metric.addEventListener("change", resetSort);
elements.direction.addEventListener("change", resetSort);
elements.speed.addEventListener("input", () => renderStats());

loadProducts();
